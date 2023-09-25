#!/bin/bash
python3 manage.py migrate
python3 manage.py collectstatic --no-input
gunicorn --bind 0:$WEB_PORT core.wsgi:application