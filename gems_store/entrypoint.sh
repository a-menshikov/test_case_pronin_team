#!/bin/bash

python3 manage.py migrate
python3 manage.py collectstatic --noinput

gunicorn --bind 0:$WEB_PORT core.wsgi:application