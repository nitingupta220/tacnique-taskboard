import pytest
from rest_framework.test import APIClient
from users.models import User
from projects.models import Project, Membership, Task


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(email='meera@taskboard.dev', name='Meera Iyer', password='password123')


@pytest.fixture
def auth_client(client, user):
    response = client.post('/api/auth/login', {
        'email': 'meera@taskboard.dev',
        'password': 'password123',
    }, format='json')
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['token']}")
    return client


@pytest.fixture
def search_projects(user):
    project = Project.objects.create(name='Searchable', owner=user)
    Membership.objects.create(user=user, project=project, role='viewer')
    other = User.objects.create_user(email='search-owner@example.com', name='Other Owner')
    private_project = Project.objects.create(name='Private', owner=other)
    Membership.objects.create(user=other, project=private_project, role='admin')
    return project, private_project


@pytest.fixture
def searchable_tasks(user, search_projects):
    project, private_project = search_projects
    analytics = Task.objects.create(
        project=project, title='Set up Analytics dashboards', status='in_progress',
        assignee=user, created_by=user, position=20,
    )
    release = Task.objects.create(
        project=project, title='Draft release notes',
        description='Prepare LAUNCH communication', status='done',
        created_by=user, position=5,
    )
    feedback = Task.objects.create(
        project=project, title="Customer's feedback", description='Review feedback',
        created_by=user, position=10,
    )
    Task.objects.create(
        project=private_project, title='Private Analytics report',
        description="Prepare LAUNCH and customer's feedback", created_by=private_project.owner,
    )
    return {'analytics': analytics, 'release': release, 'feedback': feedback}


@pytest.mark.django_db
class TestProjects:
    def test_create_project(self, auth_client, user):
        response = auth_client.post('/api/projects', {'name': 'My Project'}, format='json')
        assert response.status_code == 201
        assert response.data['project']['name'] == 'My Project'

    def test_list_only_returns_member_projects(self, auth_client, user):
        p1 = Project.objects.create(name='Mine', owner=user)
        Membership.objects.create(user=user, project=p1, role='admin')
        other = User.objects.create_user(email='other@example.com', name='Other', password='password123')
        p2 = Project.objects.create(name='Not Mine', owner=other)
        Membership.objects.create(user=other, project=p2, role='admin')

        response = auth_client.get('/api/projects')
        assert response.status_code == 200
        names = [p['name'] for p in response.data['projects']]
        assert 'Mine' in names
        assert 'Not Mine' not in names

    def test_get_project_detail(self, auth_client, user):
        project = Project.objects.create(name='My Project', owner=user)
        Membership.objects.create(user=user, project=project, role='admin')

        response = auth_client.get(f'/api/projects/{project.id}')
        assert response.status_code == 200
        assert response.data['project']['name'] == 'My Project'

    def test_non_member_cannot_view_project(self, client, user):
        owner = User.objects.create_user(email='owner@example.com', name='Owner', password='password123')
        project = Project.objects.create(name='Private', owner=owner)
        Membership.objects.create(user=owner, project=project, role='admin')

        resp = client.post('/api/auth/login', {'email': 'meera@taskboard.dev', 'password': 'password123'}, format='json')
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {resp.data['token']}")

        response = client.get(f'/api/projects/{project.id}')
        assert response.status_code == 403


@pytest.mark.django_db
class TestTasks:
    def test_create_task(self, auth_client, user):
        project = Project.objects.create(name='P', owner=user)
        Membership.objects.create(user=user, project=project, role='admin')

        response = auth_client.post(f'/api/projects/{project.id}/tasks', {'title': 'Do a thing'}, format='json')
        assert response.status_code == 201
        assert response.data['task']['title'] == 'Do a thing'

    def test_viewers_cannot_create_tasks(self, client, user):
        owner = User.objects.create_user(email='owner@example.com', name='Owner', password='password123')
        project = Project.objects.create(name='P', owner=owner)
        Membership.objects.create(user=owner, project=project, role='admin')
        Membership.objects.create(user=user, project=project, role='viewer')

        resp = client.post('/api/auth/login', {'email': 'meera@taskboard.dev', 'password': 'password123'}, format='json')
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {resp.data['token']}")

        response = client.post(f'/api/projects/{project.id}/tasks', {'title': 'A task'}, format='json')
        assert response.status_code == 403

    def test_delete_task_requires_membership(self, client, user):
        owner = User.objects.create_user(email='owner@example.com', name='Owner', password='password123')
        project = Project.objects.create(name='P', owner=owner)
        Membership.objects.create(user=owner, project=project, role='admin')
        task = Task.objects.create(project=project, title='A task', created_by=owner)

        resp = client.post('/api/auth/login', {'email': 'meera@taskboard.dev', 'password': 'password123'}, format='json')
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {resp.data['token']}")

        response = client.delete(f'/api/tasks/{task.id}')
        assert response.status_code == 403


@pytest.mark.django_db
class TestTaskSearch:
    def test_sql_injection_does_not_return_other_projects_tasks(self, auth_client, user, search_projects):
        project, private_project = search_projects
        Task.objects.create(project=project, title='Public task', created_by=user)
        Task.objects.create(project=private_project, title='Private task', created_by=private_project.owner)

        response = auth_client.get(f'/api/projects/{project.id}/tasks', {'q': "') OR TRUE -- "})

        assert response.status_code == 200
        assert response.json()['tasks'] == []

    def test_search_matches_sql_shaped_text_literally(self, auth_client, user, search_projects):
        project, private_project = search_projects
        query = "') OR TRUE -- "
        matching = Task.objects.create(project=project, title=f'Investigate {query}', created_by=user)
        Task.objects.create(project=private_project, title=f'Private {query}', created_by=private_project.owner)

        response = auth_client.get(f'/api/projects/{project.id}/tasks', {'q': query})

        assert response.status_code == 200
        assert [task['id'] for task in response.json()['tasks']] == [str(matching.id)]

    @pytest.mark.parametrize(('query', 'expected'), [
        ('ANALYTICS', 'analytics'),
        ('launch', 'release'),
        ("customer's", 'feedback'),
        ('no matching task', None),
    ])
    def test_normal_searches_only_match_tasks_in_the_project(
        self, auth_client, search_projects, searchable_tasks, query, expected,
    ):
        project, _ = search_projects

        response = auth_client.get(f'/api/projects/{project.id}/tasks', {'q': query})

        assert response.status_code == 200
        expected_ids = [str(searchable_tasks[expected].id)] if expected else []
        assert [task['id'] for task in response.json()['tasks']] == expected_ids

    def test_search_results_keep_position_order_across_statuses(self, auth_client, search_projects, searchable_tasks):
        project, _ = search_projects

        response = auth_client.get(f'/api/projects/{project.id}/tasks', {'q': 'a'})

        assert response.status_code == 200
        assert [task['id'] for task in response.json()['tasks']] == [
            str(searchable_tasks['release'].id),
            str(searchable_tasks['feedback'].id),
            str(searchable_tasks['analytics'].id),
        ]

    @pytest.mark.parametrize('query', ['%', '_'])
    def test_search_preserves_like_wildcards(self, auth_client, search_projects, searchable_tasks, query):
        project, _ = search_projects

        response = auth_client.get(f'/api/projects/{project.id}/tasks', {'q': query})

        assert response.status_code == 200
        assert [task['id'] for task in response.json()['tasks']] == [
            str(searchable_tasks['release'].id),
            str(searchable_tasks['feedback'].id),
            str(searchable_tasks['analytics'].id),
        ]

    def test_search_keeps_existing_response_fields(self, auth_client, user, search_projects, searchable_tasks):
        project, _ = search_projects

        response = auth_client.get(f'/api/projects/{project.id}/tasks', {'q': 'analytics'})

        assert response.status_code == 200
        task = response.json()['tasks'][0]
        assert set(task) == {
            'id', 'project_id', 'title', 'description', 'status', 'assignee_id',
            'created_by_id', 'position', 'created_at', 'updated_at',
        }
        assert task['id'] == str(searchable_tasks['analytics'].id)
        assert task['project_id'] == str(project.id)
        assert task['assignee_id'] == str(user.id)
        assert task['created_by_id'] == str(user.id)
        assert task['description'] is None

    def test_empty_query_keeps_existing_non_search_behavior(self, auth_client, search_projects, searchable_tasks):
        project, _ = search_projects

        without_query = auth_client.get(f'/api/projects/{project.id}/tasks')
        empty_query = auth_client.get(f'/api/projects/{project.id}/tasks', {'q': ''})

        assert without_query.status_code == empty_query.status_code == 200
        assert empty_query.json() == without_query.json()
        assert {task['id'] for task in empty_query.json()['tasks']} == {
            str(task.id) for task in searchable_tasks.values()
        }

    @pytest.mark.parametrize('query', ['Analytics', "') OR TRUE -- "])
    def test_non_member_cannot_search_a_project(self, auth_client, search_projects, searchable_tasks, query):
        _, private_project = search_projects

        response = auth_client.get(f'/api/projects/{private_project.id}/tasks', {'q': query})

        assert response.status_code == 403

    def test_search_requires_authentication(self, client, search_projects, searchable_tasks):
        project, _ = search_projects

        response = client.get(f'/api/projects/{project.id}/tasks', {'q': 'Analytics'})

        assert response.status_code == 401
