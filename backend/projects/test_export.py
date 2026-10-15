import json
from types import SimpleNamespace
from unittest.mock import patch

import pytest
from rest_framework.test import APIClient
from users.models import User
from projects.models import Project, Membership, Task


@pytest.fixture(autouse=True)
def fake_airtable_settings(settings):
    # Never allow automated tests to use the real ignored .env credentials.
    settings.AIRTABLE_API_KEY = 'test-secret'
    settings.AIRTABLE_BASE_ID = 'appTestOnly'
    settings.AIRTABLE_TABLE_NAME = 'Tasks'


@pytest.fixture
def export_project(db):
    user = User.objects.create_user(email='export@example.test', name='Exporter')
    project = Project.objects.create(name='Export project', owner=user)
    Membership.objects.create(user=user, project=project, role='admin')
    Task.objects.create(project=project, title='Export me', description='Details', created_by=user)
    client = APIClient()
    client.force_authenticate(user=user)
    return client, project, user


@pytest.mark.django_db
def test_export_requires_server_configuration(export_project, settings):
    settings.AIRTABLE_API_KEY = ''
    settings.AIRTABLE_BASE_ID = ''
    client, project, _ = export_project
    response = client.post(f'/api/projects/{project.id}/export')
    assert response.status_code == 503
    assert 'error' in response.json()


@pytest.mark.django_db
@pytest.mark.parametrize(('role', 'expected'), [('admin', 200), ('member', 200), ('viewer', 403), (None, 403)])
def test_export_authorization(export_project, role, expected):
    client, project, user = export_project
    if role is None:
        Membership.objects.filter(project=project).delete()
    else:
        Membership.objects.filter(project=project).update(role=role)
    result = {'total': 1, 'created': 1, 'updated': 0, 'failed': 0, 'failures': []}
    with patch('projects.airtable_export.subprocess.run', return_value=SimpleNamespace(returncode=0, stdout=json.dumps(result))) as run:
        response = client.post(f'/api/projects/{project.id}/export')
    assert response.status_code == expected
    assert run.call_count == (1 if expected == 200 else 0)


@pytest.mark.django_db
def test_export_requires_authentication(export_project):
    _, project, _ = export_project
    with patch('projects.airtable_export.subprocess.run') as run:
        response = APIClient().post(f'/api/projects/{project.id}/export')
    assert response.status_code == 401
    run.assert_not_called()


@pytest.mark.django_db
def test_export_uses_server_tasks_only_and_returns_partial_results(export_project):
    client, project, user = export_project
    own = Task.objects.get(project=project)
    private = Project.objects.create(name='Other', owner=user)
    Task.objects.create(project=private, title='Not exported', created_by=user)
    result = {'total': 1, 'created': 0, 'updated': 0, 'failed': 1,
              'failures': [{'taskId': str(own.id), 'title': own.title, 'error': 'Rejected field values.'}]}
    with patch('projects.airtable_export.subprocess.run', return_value=SimpleNamespace(returncode=0, stdout=json.dumps(result))) as run:
        response = client.post(f'/api/projects/{project.id}/export', {'tasks': ['untrusted client task']}, format='json')
    assert response.status_code == 200
    assert response.json() == result
    payload = json.loads(run.call_args.kwargs['input'])
    assert [t['id'] for t in payload['tasks']] == [str(own.id)]
    assert payload['projectId'] == str(project.id)
    assert 'test-secret' not in ' '.join(run.call_args.args[0])
    assert run.call_args.kwargs['env']['AIRTABLE_API_KEY'] == 'test-secret'


@pytest.mark.django_db
@pytest.mark.parametrize(('count', 'expected'), [(1000, 200), (1001, 400)])
def test_export_task_limit(export_project, count, expected):
    client, project, user = export_project
    Task.objects.bulk_create([Task(project=project, title=f'Task {i}', created_by=user) for i in range(count - 1)])
    result = {'total': count, 'created': count, 'updated': 0, 'failed': 0, 'failures': []}
    with patch('projects.airtable_export.subprocess.run', return_value=SimpleNamespace(returncode=0, stdout=json.dumps(result))) as run:
        response = client.post(f'/api/projects/{project.id}/export')
    assert response.status_code == expected
    if expected == 200:
        assert len(json.loads(run.call_args.kwargs['input'])['tasks']) == 1000
    else:
        run.assert_not_called()


@pytest.mark.django_db
def test_node_failure_does_not_expose_credentials(export_project):
    client, project, _ = export_project
    with patch('projects.airtable_export.subprocess.run', return_value=SimpleNamespace(returncode=1, stdout='test-secret', stderr='test-secret')):
        response = client.post(f'/api/projects/{project.id}/export')
    assert response.status_code == 503
    assert 'test-secret' not in response.content.decode()
