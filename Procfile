web: gunicorn wsgi:application
worker: celery -A app.tasks.celery_worker.celery worker --loglevel=info
beat: celery -A app.tasks.celery_worker.celery beat --loglevel=info
