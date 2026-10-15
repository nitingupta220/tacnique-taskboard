"""Server-side bridge to the official Airtable npm client; never writes local data."""
import json
import os
import subprocess
from pathlib import Path

from django.conf import settings
from .models import Task


class ExportError(Exception):
    def __init__(self, message, status_code=503):
        super().__init__(message)
        self.status_code = status_code


def export_project_tasks(project_id):
    if not all((settings.AIRTABLE_API_KEY, settings.AIRTABLE_BASE_ID, settings.AIRTABLE_TABLE_NAME)):
        raise ExportError('Airtable export is not configured on the server.')
    tasks = list(Task.objects.filter(project_id=project_id).select_related('assignee').order_by('id')[:1001])
    if len(tasks) > 1000:
        raise ExportError('A project can export at most 1000 tasks at once.', 400)
    payload = {'projectId': str(project_id), 'tasks': [{
        'id': str(task.id), 'title': task.title, 'description': task.description,
        'status': task.status, 'assignee': task.assignee.name if task.assignee else '',
        'position': task.position,
    } for task in tasks]}
    env = {**os.environ, 'AIRTABLE_API_KEY': settings.AIRTABLE_API_KEY,
           'AIRTABLE_BASE_ID': settings.AIRTABLE_BASE_ID, 'AIRTABLE_TABLE_NAME': settings.AIRTABLE_TABLE_NAME}
    script = Path(settings.BASE_DIR) / 'airtable' / 'exporter.mjs'
    try:
        completed = subprocess.run(
            [settings.AIRTABLE_NODE_BINARY, str(script)], input=json.dumps(payload),
            capture_output=True, text=True, env=env, timeout=150, check=False,
        )
        if completed.returncode:
            raise ExportError('Airtable export could not start. Check the server configuration.')
        result = json.loads(completed.stdout)
        counts = [result[key] for key in ('created', 'updated', 'failed')]
        if not all(type(value) is int and value >= 0 for value in counts):
            raise ValueError('Invalid export counts')
        if result['total'] != len(tasks) or sum(counts) != len(tasks) or len(result['failures']) != result['failed']:
            raise ValueError('Incomplete export results')
        return {key: result[key] for key in ('total', 'created', 'updated', 'failed', 'failures')}
    except (OSError, subprocess.TimeoutExpired, ValueError, KeyError, TypeError):
        # Do not expose subprocess arguments, stderr, SDK errors or credentials.
        raise ExportError('Airtable export is unavailable. Please try again later.') from None
