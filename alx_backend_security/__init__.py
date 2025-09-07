import os
from django.core.wsgi import get_wsgi_application
from .celery import app as celery_app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_security.settings')

application = get_wsgi_application()

__all__ = ('celery_app',)