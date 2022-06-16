"""
WSGI config for VacunAssist project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application


project_folder = os.path.expanduser('~/VacunAssist')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))
application = get_wsgi_application()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VacunAssist.settings')