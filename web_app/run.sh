#!/bin/sh

python manage.py makemigrations
python manage.py migrate

python manage.py collectstatic --noinput

#rm celery*.pid

#celery multi start 1 -c 4 -A super_news -B --logfile=/code/logs/%nI.log --loglevel=debug

gunicorn -b 0.0.0.0:8000 --reload -w 4 super_news.wsgi

python manage.py check_permissions

#mkdir {media,django_cache}