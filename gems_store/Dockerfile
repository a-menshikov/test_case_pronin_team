FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

COPY ./gems_store .

CMD python3 manage.py migrate && \
    python3 manage.py collectstatic --no-input && \
    gunicorn --bind 0:$WEB_PORT core.wsgi:application
