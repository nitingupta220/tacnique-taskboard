import uuid
from datetime import timedelta

import pytest
from django.utils import timezone
from rest_framework.test import APIClient
from projects.models import Comment, Membership, Project, Task
from users.models import User


@pytest.fixture
def comment_thread(db):
    users = {
        role: User.objects.create_user(email=f'{role}@comments.test', name=role.title())
        for role in ('admin', 'member', 'viewer', 'outsider')
    }
    project = Project.objects.create(name='Comment project', owner=users['admin'])
    for role in ('admin', 'member', 'viewer'):
        Membership.objects.create(project=project, user=users[role], role=role)
    task = Task.objects.create(project=project, title='Discuss this', created_by=users['admin'])
    return project, task, users


def client_for(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.mark.django_db
@pytest.mark.parametrize('role', ['admin', 'member', 'viewer'])
def test_project_roles_can_read_comments(comment_thread, role):
    _, task, users = comment_thread
    comment = Comment.objects.create(task=task, author=users['member'], body='First comment')
    response = client_for(users[role]).get(f'/api/tasks/{task.id}/comments')
    assert response.status_code == 200
    assert response.json()['comments'] == [{
        'id': str(comment.id), 'body': 'First comment',
        'author': {'id': str(users['member'].id), 'name': 'Member', 'email': 'member@comments.test'},
        'createdAt': comment.created_at.isoformat().replace('+00:00', 'Z'),
    }]


@pytest.mark.django_db
@pytest.mark.parametrize(('role', 'expected'), [('admin', 201), ('member', 201), ('viewer', 403), ('outsider', 403)])
def test_only_admins_and_members_can_post(comment_thread, role, expected):
    _, task, users = comment_thread
    response = client_for(users[role]).post(f'/api/tasks/{task.id}/comments', {'body': '  A comment  '}, format='json')
    assert response.status_code == expected
    assert Comment.objects.count() == (1 if expected == 201 else 0)
    if expected == 201:
        saved = Comment.objects.get()
        assert saved.body == 'A comment'
        assert saved.author == users[role]
        assert saved.task == task
        assert response.json()['comment']['id'] == str(saved.id)


@pytest.mark.django_db
@pytest.mark.parametrize('method', ['get', 'post'])
def test_non_members_and_anonymous_cannot_access_a_thread(comment_thread, method):
    _, task, users = comment_thread
    for client, status in [(client_for(users['outsider']), 403), (APIClient(), 401)]:
        response = getattr(client, method)(f'/api/tasks/{task.id}/comments', {'body': 'Forbidden'})
        assert response.status_code == status
    assert not Comment.objects.exists()


@pytest.mark.django_db
def test_comments_are_chronological_and_scoped_to_task_and_project(comment_thread):
    project, task, users = comment_thread
    now = timezone.now()
    with pytest.MonkeyPatch.context() as monkeypatch:
        monkeypatch.setattr('django.utils.timezone.now', lambda: now)
        later = Comment.objects.create(task=task, author=users['member'], body='Later')
        monkeypatch.setattr('django.utils.timezone.now', lambda: now - timedelta(days=1))
        first = Comment.objects.create(task=task, author=users['admin'], body='Earlier')
        tied = Comment.objects.create(task=task, author=users['member'], body='Same time')
    other_task = Task.objects.create(project=project, title='Other task', created_by=users['admin'])
    Comment.objects.create(task=other_task, author=users['admin'], body='Other thread')
    private = Project.objects.create(name='Private', owner=users['outsider'])
    private_task = Task.objects.create(project=private, title='Private task', created_by=users['outsider'])
    Comment.objects.create(task=private_task, author=users['outsider'], body='Private comment')
    client = client_for(users['member'])
    response = client.get(f'/api/tasks/{task.id}/comments')
    expected = sorted([first, tied], key=lambda comment: comment.id) + [later]
    assert [comment['id'] for comment in response.json()['comments']] == [str(comment.id) for comment in expected]
    assert client.get(f'/api/tasks/{private_task.id}/comments').status_code == 403
    assert client.post(f'/api/tasks/{private_task.id}/comments', {'body': 'Forbidden'}).status_code == 403


@pytest.mark.django_db
def test_post_cannot_forge_identity_time_or_replace_an_existing_comment(comment_thread):
    _, task, users = comment_thread
    original = Comment.objects.create(task=task, author=users['admin'], body='Original')
    started = timezone.now()
    response = client_for(users['member']).post(f'/api/tasks/{task.id}/comments', {
        'id': str(original.id), 'body': 'A new comment',
        'author': {'id': str(users['admin'].id)}, 'author_id': str(users['admin'].id),
        'createdAt': '2000-01-01T00:00:00Z', 'created_at': '2000-01-01T00:00:00Z',
        'task': str(uuid.uuid4()),
    }, format='json')
    assert response.status_code == 201
    original.refresh_from_db()
    assert original.body == 'Original'
    assert original.author == users['admin']
    new = Comment.objects.exclude(id=original.id).get()
    assert new.id != original.id
    assert new.author == users['member']
    assert new.task == task
    assert new.created_at >= started


@pytest.mark.django_db
@pytest.mark.parametrize('role', ['admin', 'member', 'viewer'])
def test_comments_cannot_be_edited_or_deleted(comment_thread, role):
    _, task, users = comment_thread
    original = Comment.objects.create(task=task, author=users['member'], body='Permanent')
    before = Comment.objects.values().get()
    client = client_for(users[role])
    for method in ('put', 'patch', 'delete'):
        collection = getattr(client, method)(f'/api/tasks/{task.id}/comments', {'body': 'Changed'}, format='json')
        detail = getattr(client, method)(f'/api/tasks/{task.id}/comments/{original.id}', {'body': 'Changed'}, format='json')
        assert collection.status_code == 405
        assert detail.status_code == 404
    assert Comment.objects.values().get() == before


@pytest.mark.django_db
@pytest.mark.parametrize('target', ['task', 'project'])
def test_deleting_parents_cannot_remove_comment_history(comment_thread, target):
    project, task, users = comment_thread
    Comment.objects.create(task=task, author=users['member'], body='Keep history')
    before = Comment.objects.values().get()
    url = f'/api/tasks/{task.id}' if target == 'task' else f'/api/projects/{project.id}'
    response = client_for(users['admin']).delete(url)
    assert response.status_code == 409
    assert Task.objects.filter(id=task.id).exists()
    assert Project.objects.filter(id=project.id).exists()
    assert Comment.objects.values().get() == before


@pytest.mark.django_db
@pytest.mark.parametrize('body', ['', '  \n\t', None, 'x' * 5001], ids=['empty', 'whitespace', 'null', 'too-long'])
def test_invalid_comment_bodies_are_rejected(comment_thread, body):
    _, task, users = comment_thread
    response = client_for(users['member']).post(f'/api/tasks/{task.id}/comments', {'body': body}, format='json')
    assert response.status_code == 400
    assert not Comment.objects.exists()


@pytest.mark.django_db
def test_missing_task_returns_not_found(comment_thread):
    _, _, users = comment_thread
    client = client_for(users['member'])
    url = f'/api/tasks/{uuid.uuid4()}/comments'
    assert client.get(url).status_code == 404
    assert client.post(url, {'body': 'Missing task'}).status_code == 404
