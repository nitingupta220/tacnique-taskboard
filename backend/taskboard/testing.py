"""Isolated pytest configuration: no real dotenv file, signing key or Airtable token."""
import os
import secrets

os.environ['PYTHON_DOTENV_DISABLED'] = '1'
os.environ['DJANGO_SECRET_KEY'] = secrets.token_urlsafe(64)
os.environ['DJANGO_ENV'] = 'development'
os.environ['DEBUG'] = 'false'
os.environ['DJANGO_ALLOWED_HOSTS'] = 'localhost,127.0.0.1,[::1]'
os.environ['AIRTABLE_API_KEY'] = ''
os.environ['AIRTABLE_BASE_ID'] = ''

from .settings import *  # noqa: E402,F403
