import runpy
import secrets
import shutil
import subprocess
import sys
import uuid
from datetime import timedelta
from pathlib import Path

import jwt
import pytest
from django.core.exceptions import ImproperlyConfigured
from django.utils import timezone
from rest_framework.test import APIClient
from users.models import User

ROOT = Path(__file__).resolve().parents[2]
PUBLIC_KEYS = ['dev-secret-change-me', 'dev-secret-change-me-in-production']


@pytest.mark.parametrize('key', [None, '', *PUBLIC_KEYS, 'x' * 80, 'django-insecure-' + 'aB0123xyz' * 8, '<unique-long-random-server-secret>' * 3])
def test_missing_weak_or_development_keys_prevent_startup(monkeypatch, key):
    monkeypatch.setenv('PYTHON_DOTENV_DISABLED', '1')
    if key is None:
        monkeypatch.delenv('DJANGO_SECRET_KEY', raising=False)
    else:
        monkeypatch.setenv('DJANGO_SECRET_KEY', key)
    with pytest.raises(ImproperlyConfigured, match='DJANGO_SECRET_KEY must be') as error:
        runpy.run_path(str(ROOT / 'backend/taskboard/settings.py'))
    if key:
        assert key not in str(error.value)


def load_settings(monkeypatch, **overrides):
    environment = {
        'PYTHON_DOTENV_DISABLED': '1', 'DJANGO_SECRET_KEY': secrets.token_urlsafe(64),
        'DJANGO_ENV': 'development', 'DEBUG': 'false', 'DJANGO_ALLOWED_HOSTS': '',
        'DJANGO_CORS_ALLOWED_ORIGINS': '',
    }
    for key, value in {**environment, **overrides}.items():
        monkeypatch.setenv(key, value)
    return runpy.run_path(str(ROOT / 'backend/taskboard/settings.py'))


def test_safe_local_defaults_and_explicit_jwt_signing_key(monkeypatch):
    result = load_settings(monkeypatch)
    assert result['DEBUG'] is False
    assert '*' not in result['ALLOWED_HOSTS']
    assert not result['CORS_ALLOW_ALL_ORIGINS']
    assert not result['SECURE_SSL_REDIRECT']  # local HTTP remains usable
    assert result['SIMPLE_JWT']['SIGNING_KEY'] == result['SECRET_KEY']


@pytest.mark.parametrize('overrides', [
    {'DEBUG': 'true', 'DJANGO_ALLOWED_HOSTS': 'tasks.example.test'},
    {'DJANGO_ALLOWED_HOSTS': ''},
    {'DJANGO_ALLOWED_HOSTS': '*'},
    {'DJANGO_ALLOWED_HOSTS': 'tasks.example.test', 'POSTGRES_PASSWORD': 'taskboard'},
])
def test_production_rejects_unsafe_configuration(monkeypatch, overrides):
    with pytest.raises(ImproperlyConfigured):
        load_settings(monkeypatch, DJANGO_ENV='production', **overrides)


def test_production_configuration_requires_explicit_hosts_and_secures_transport(monkeypatch):
    result = load_settings(monkeypatch, DJANGO_ENV='production',
        DJANGO_ALLOWED_HOSTS='tasks.example.test', POSTGRES_PASSWORD=secrets.token_urlsafe(32))
    assert result['ALLOWED_HOSTS'] == ['tasks.example.test']
    assert result['SECURE_SSL_REDIRECT']
    assert result['SESSION_COOKIE_SECURE'] and result['CSRF_COOKIE_SECURE']
    assert result['SECURE_HSTS_SECONDS'] > 0


@pytest.mark.django_db
@pytest.mark.parametrize('key', PUBLIC_KEYS)
def test_tokens_signed_with_public_development_keys_cannot_impersonate_a_user(key):
    user = User.objects.create_user(email='secure@example.test', name='Secure User')
    now = timezone.now()
    forged = jwt.encode({'user_id': str(user.id), 'token_type': 'access', 'jti': uuid.uuid4().hex,
        'iat': int(now.timestamp()), 'exp': int((now + timedelta(minutes=1)).timestamp())}, key, algorithm='HS256')
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + forged)
    assert client.get('/api/users/me').status_code == 401
    assert client.get('/api/projects').status_code == 401


@pytest.mark.django_db
def test_login_still_issues_a_valid_token_and_security_headers():
    user = User.objects.create_user(email='login@secure.test', name='Login', password='test-login-password')
    client = APIClient()
    response = client.post('/api/auth/login', {'email': user.email, 'password': 'test-login-password'}, format='json')
    assert response.status_code == 200
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.json()['token'])
    me = client.get('/api/users/me')
    assert me.status_code == 200 and me.json()['user']['id'] == str(user.id)
    assert me['X-Content-Type-Options'] == 'nosniff'
    assert me['X-Frame-Options'] == 'DENY'


def test_key_provisioning_is_private_preserves_other_credentials_and_rotates_only_explicitly(tmp_path):
    directory = tmp_path / 'bin'
    directory.mkdir()
    script = directory / 'generate-signing-key'
    shutil.copyfile(ROOT / 'bin/generate-signing-key', script)
    env_path = tmp_path / '.env'
    env_path.write_text('AIRTABLE_API_KEY=private-test-placeholder\n')
    first = subprocess.run([sys.executable, str(script)], capture_output=True, text=True, check=True)
    before = env_path.read_text()
    generated = before.split('DJANGO_SECRET_KEY=', 1)[1].strip()
    assert len(generated) >= 50 and generated not in first.stdout + first.stderr
    assert 'AIRTABLE_API_KEY=private-test-placeholder' in before
    assert env_path.stat().st_mode & 0o777 == 0o600
    subprocess.run([sys.executable, str(script)], capture_output=True, check=True)
    assert env_path.read_text() == before
    rotated = subprocess.run([sys.executable, str(script), '--rotate'], capture_output=True, text=True, check=True)
    after = env_path.read_text()
    assert after != before and 'AIRTABLE_API_KEY=private-test-placeholder' in after
    assert generated not in rotated.stdout + rotated.stderr
