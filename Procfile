web: gunicorn alx_backend_security.wsgi:application
worker: celery -A alx_backend_security worker --loglevel=info
beat: celery -A alx_backend_security beat --loglevel=info
