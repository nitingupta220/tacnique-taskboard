from pathlib import Path
from datetime import timedelta
import os
from dotenv import load_dotenv
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

# Load local server configuration without overriding deployed environment values.
load_dotenv(BASE_DIR.parent / '.env', override=False)

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '').strip()
if (
    len(SECRET_KEY) < 50 or len(set(SECRET_KEY)) < 8
    or SECRET_KEY.lower().startswith(('dev-secret', 'django-insecure-', 'change-me', 'replace-me', 'your-secret', '<'))
):
    raise ImproperlyConfigured('DJANGO_SECRET_KEY must be a unique random secret of at least 50 characters.')

ENVIRONMENT = os.environ.get('DJANGO_ENV', 'development')
if ENVIRONMENT not in ('development', 'production'):
    raise ImproperlyConfigured('DJANGO_ENV must be development or production.')
IS_PRODUCTION = ENVIRONMENT == 'production'
DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'
ALLOWED_HOSTS = [host.strip() for host in os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',') if host.strip()]
if IS_PRODUCTION:
    if DEBUG or not ALLOWED_HOSTS or any('*' in host for host in ALLOWED_HOSTS):
        raise ImproperlyConfigured('Production requires DEBUG=false and explicit DJANGO_ALLOWED_HOSTS without wildcards.')
    database_password = os.environ.get('POSTGRES_PASSWORD', '')
    if len(database_password) < 16 or len(set(database_password)) < 8:
        raise ImproperlyConfigured('Production requires a strong POSTGRES_PASSWORD of at least 16 characters.')
else:
    ALLOWED_HOSTS = ALLOWED_HOSTS or ['localhost', '127.0.0.1', '[::1]']

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'rest_framework',
    'corsheaders',
    'users',
    'projects',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'taskboard.urls'
WSGI_APPLICATION = 'taskboard.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'taskboard'),
        'USER': os.environ.get('POSTGRES_USER', 'taskboard'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'taskboard'),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}

AUTH_USER_MODEL = 'users.User'
APPEND_SLASH = False

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

SIMPLE_JWT = {
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in os.environ.get('DJANGO_CORS_ALLOWED_ORIGINS', '').split(',') if origin.strip()]
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS
SECURE_SSL_REDIRECT = IS_PRODUCTION
SESSION_COOKIE_SECURE = IS_PRODUCTION
CSRF_COOKIE_SECURE = IS_PRODUCTION
SECURE_HSTS_SECONDS = 31536000 if IS_PRODUCTION else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = IS_PRODUCTION
SECURE_HSTS_PRELOAD = IS_PRODUCTION
X_FRAME_OPTIONS = 'DENY'

AIRTABLE_API_KEY = os.environ.get('AIRTABLE_API_KEY', '')
AIRTABLE_BASE_ID = os.environ.get('AIRTABLE_BASE_ID', '')
AIRTABLE_TABLE_NAME = os.environ.get('AIRTABLE_TABLE_NAME', 'Tasks')
AIRTABLE_NODE_BINARY = os.environ.get('AIRTABLE_NODE_BINARY', 'node')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_TZ = True
