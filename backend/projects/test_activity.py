import uuid
from datetime import timedelta
from unittest.mock import patch

import pytest
from django.db import IntegrityError
from django.utils import timezone
from rest_framework.test import APIClient
from projects.models import Activity, Comment, Membership, Project, Task
from users.models import User


@pytest.fixture
def activity_project(db):
    users = {
        role: User.objects.create_user(email=f'{role}@activity.test', name=role.title())
        for role in ('admin', 'member', 'viewer', 'outsider')
    }
    project = Project.objects.create(name='Activity project', owner=users['admin'])
    for role in ('admin', 'member', 'viewer'):
        Membership.objects.create(project=project, user=users[role], role=role)
    task = Task.objects.create(project=project, title='Original task', created_by=users['admin'])
    return project, task, users


def client_for(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.mark.django_db
@pytest.mark.parametrize('role', ['admin', 'member', 'viewer'])
def test_all_project_roles_can_read_activity(activity_project, role):
    project, task, users = activity_project
    event = Activity.objects.create(project=project, actor=users['member'], action='task_created',
                                    details={'taskId': str(task.id), 'taskTitle': task.title})
    response = client_for(users[role]).get(f'/api/projects/{project.id}/activity')
    assert response.status_code == 200
    assert response.json()['activities'] == [{
        'id': str(event.id), 'projectId': str(project.id),
        'actor': {'id': str(users['member'].id), 'name': 'Member', 'email': 'member@activity.test'},
        'action': 'task_created', 'details': event.details,
        'createdAt': event.created_at.isoformat().replace('+00:00', 'Z'),
    }]


@pytest.mark.django_db
def test_feed_requires_membership_and_authentication(activity_project):
    project, _, users = activity_project
    path = f'/api/projects/{project.id}/activity'
    assert client_for(users['outsider']).get(path).status_code == 403
    assert APIClient().get(path).status_code == 401
    # Even the owner must hold an explicit membership.
    Membership.objects.filter(project=project, user=users['admin']).delete()
    assert client_for(users['admin']).get(path).status_code == 403


@pytest.mark.django_db
def test_feed_is_newest_first_bounded_and_project_isolated(activity_project):
    project, _, users = activity_project
    now = timezone.now()
    events = []
    with patch('django.utils.timezone.now') as clock:
        for number in range(55):
            clock.return_value = now + timedelta(seconds=number)
            events.append(Activity.objects.create(project=project, actor=users['admin'],
                action='task_created', details={'taskTitle': f'Task {number}'}))
        clock.return_value = now + timedelta(seconds=54)
        tied = Activity.objects.create(project=project, actor=users['member'], action='comment_added', details={})
    private = Project.objects.create(name='Private', owner=users['outsider'])
    Membership.objects.create(project=private, user=users['member'])
    Activity.objects.create(project=private, actor=users['outsider'], action='task_created', details={'secret': True})
    response = client_for(users['member']).get(f'/api/projects/{project.id}/activity')
    expected = sorted(events + [tied], key=lambda event: (event.created_at, event.id), reverse=True)[:50]
    assert [event['id'] for event in response.json()['activities']] == [str(event.id) for event in expected]
    assert all(event['projectId'] == str(project.id) for event in response.json()['activities'])
    assert client_for(users['member']).get(f'/api/projects/{private.id}/activity').json()['activities'][0]['details'] == {'secret': True}


@pytest.mark.django_db
def test_empty_feed_and_no_client_supplied_events(activity_project):
    project, _, users = activity_project
    client = client_for(users['admin'])
    path = f'/api/projects/{project.id}/activity'
    assert client.get(path).json() == {'activities': []}
    for method in ('post', 'put', 'patch', 'delete'):
        assert getattr(client, method)(path, {'action': 'task_created'}, format='json').status_code == 405
    assert not Activity.objects.exists()


@pytest.mark.django_db
@pytest.mark.parametrize('role', ['admin', 'member'])
def test_task_creation_records_server_actor_and_initial_state(activity_project, role):
    project, _, users = activity_project
    response = client_for(users[role]).post(f'/api/projects/{project.id}/tasks', {
        'title': '  New task  ', 'status': 'review', 'assigneeId': str(users['member'].id),
        'actor': str(users['outsider'].id), 'projectId': str(uuid.uuid4()),
    }, format='json')
    assert response.status_code == 201
    event = Activity.objects.get()
    assert event.actor == users[role] and event.project == project and event.action == 'task_created'
    assert event.details == {
        'taskId': response.json()['task']['id'], 'taskTitle': 'New task', 'status': 'review',
        'assignee': {'id': str(users['member'].id), 'name': 'Member'},
    }


@pytest.mark.django_db
def test_status_assignment_reassignment_and_unassignment_record_actual_changes(activity_project):
    project, task, users = activity_project
    client = client_for(users['member'])
    path = f'/api/tasks/{task.id}'
    assert client.patch(path, {'status': 'in_progress', 'assigneeId': str(users['admin'].id)}, format='json').status_code == 200
    status_event = Activity.objects.get(action='status_changed')
    assert status_event.details == {'taskId': str(task.id), 'taskTitle': task.title, 'from': 'todo', 'to': 'in_progress'}
    assignment = Activity.objects.get(action='assignee_changed')
    assert assignment.details['from'] is None
    assert assignment.details['to'] == {'id': str(users['admin'].id), 'name': 'Admin'}
    assert all(event.actor == users['member'] and event.project == project for event in Activity.objects.all())
    assert client.patch(path, {'assigneeId': str(users['member'].id)}, format='json').status_code == 200
    reassignment = Activity.objects.first()
    assert reassignment.details['from'] == assignment.details['to']
    assert reassignment.details['to'] == {'id': str(users['member'].id), 'name': 'Member'}
    assert client.patch(path, {'assigneeId': None}, format='json').status_code == 200
    assert Activity.objects.first().details['from'] == reassignment.details['to']
    assert Activity.objects.first().details['to'] is None


@pytest.mark.django_db
@pytest.mark.parametrize('assignee_format', ['standard', 'uppercase', 'hex'])
def test_noop_and_untracked_edits_do_not_create_activity(activity_project, assignee_format):
    _, task, users = activity_project
    task.assignee = users['member']
    task.save()
    assignee_id = str(users['member'].id)
    if assignee_format == 'uppercase':
        assignee_id = assignee_id.upper()
    elif assignee_format == 'hex':
        assignee_id = users['member'].id.hex
    response = client_for(users['member']).patch(f'/api/tasks/{task.id}', {
        'status': task.status, 'assigneeId': assignee_id, 'title': 'Renamed', 'description': 'Updated',
    }, format='json')
    assert response.status_code == 200
    assert not Activity.objects.exists()


@pytest.mark.django_db
def test_comment_event_preserves_original_comment_and_ignores_forged_actor(activity_project):
    project, task, users = activity_project
    original = Comment.objects.create(task=task, author=users['admin'], body='Permanent audit comment')
    before = Comment.objects.values().get(id=original.id)
    response = client_for(users['member']).post(f'/api/tasks/{task.id}/comments', {
        'body': '  New discussion  ', 'actor': str(users['outsider'].id), 'createdAt': '2000-01-01T00:00:00Z',
    }, format='json')
    assert response.status_code == 201
    event = Activity.objects.get()
    assert event.actor == users['member'] and event.project == project and event.action == 'comment_added'
    assert event.details == {'taskId': str(task.id), 'taskTitle': task.title,
                             'commentId': response.json()['comment']['id'], 'body': 'New discussion'}
    assert Comment.objects.values().get(id=original.id) == before


@pytest.mark.django_db
@pytest.mark.parametrize('role', ['viewer', 'outsider'])
def test_forbidden_writes_do_not_change_tasks_comments_or_feed(activity_project, role):
    project, task, users = activity_project
    before = Task.objects.values().get(id=task.id)
    client = client_for(users[role])
    assert client.post(f'/api/projects/{project.id}/tasks', {'title': 'Denied'}, format='json').status_code == 403
    assert client.patch(f'/api/tasks/{task.id}', {'status': 'done'}, format='json').status_code == 403
    assert client.post(f'/api/tasks/{task.id}/comments', {'body': 'Denied'}, format='json').status_code == 403
    assert Task.objects.values().get(id=task.id) == before
    assert Task.objects.count() == 1 and not Comment.objects.exists() and not Activity.objects.exists()


@pytest.mark.django_db
def test_validation_failure_has_no_event_or_partial_update(activity_project):
    project, task, users = activity_project
    client = client_for(users['member'])
    before = Task.objects.values().get(id=task.id)
    assert client.post(f'/api/projects/{project.id}/tasks', {'title': ''}, format='json').status_code == 400
    assert client.patch(f'/api/tasks/{task.id}', {'title': 'Do not save', 'status': 'invalid'}, format='json').status_code == 400
    assert client.post(f'/api/tasks/{task.id}/comments', {'body': ' '}, format='json').status_code == 400
    assert Task.objects.values().get(id=task.id) == before
    assert not Activity.objects.exists()


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize('operation', ['create', 'update', 'comment'])
def test_activity_write_failure_rolls_back_entire_operation(activity_project, operation):
    project, task, users = activity_project
    client = client_for(users['member'])
    before = Task.objects.values().get(id=task.id)
    count = 0
    real_create = Activity.objects.create

    def fail_after_insert(**kwargs):
        nonlocal count
        event = real_create(**kwargs)
        count += 1
        # On an update, let the status event succeed, then fail the assignee event.
        if operation != 'update' or count == 2:
            raise IntegrityError('Simulated activity persistence failure')
        return event

    with patch.object(Activity.objects, 'create', side_effect=fail_after_insert):
        with pytest.raises(IntegrityError, match='Simulated activity persistence failure'):
            if operation == 'create':
                client.post(f'/api/projects/{project.id}/tasks', {'title': 'Must roll back'}, format='json')
            elif operation == 'update':
                client.patch(f'/api/tasks/{task.id}', {'status': 'done', 'assigneeId': str(users['member'].id)}, format='json')
            else:
                client.post(f'/api/tasks/{task.id}/comments', {'body': 'Must roll back'}, format='json')
    assert count == (2 if operation == 'update' else 1)
    assert Task.objects.count() == 1 and Task.objects.values().get(id=task.id) == before
    assert not Comment.objects.exists() and not Activity.objects.exists()


@pytest.mark.django_db(transaction=True)
def test_original_operation_failure_cannot_leave_an_activity(activity_project):
    project, _, users = activity_project
    real_create = Task.objects.create

    def fail_after_insert(**kwargs):
        real_create(**kwargs)
        raise IntegrityError('Simulated task persistence failure')

    with patch.object(Task.objects, 'create', side_effect=fail_after_insert):
        with pytest.raises(IntegrityError):
            client_for(users['member']).post(f'/api/projects/{project.id}/tasks', {
                'title': 'Must roll back',
            }, format='json')
    assert Task.objects.count() == 1 and not Activity.objects.exists()


@pytest.mark.django_db
def test_activity_task_snapshot_survives_task_deletion(activity_project):
    project, _, users = activity_project
    client = client_for(users['member'])
    task_id = client.post(f'/api/projects/{project.id}/tasks', {'title': 'Temporary'}, format='json').json()['task']['id']
    assert client.delete(f'/api/tasks/{task_id}').status_code == 200
    event = client.get(f'/api/projects/{project.id}/activity').json()['activities'][0]
    assert event['details']['taskId'] == task_id and event['details']['taskTitle'] == 'Temporary'
