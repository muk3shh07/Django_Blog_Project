web: gunicorn --bind :8000 --workers 3 my_project_drf.wsgi:application
release: python manage.py collectstatic --noinput 