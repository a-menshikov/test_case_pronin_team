SHELL := /bin/bash

up:
	docker compose up

up-d:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build

migrate:
	docker compose exec backend python manage.py migrate

makemigrations:
	docker compose exec backend python manage.py makemigrations

collectstatic:
	docker compose exec backend python manage.py collectstatic

createsuperuser:
	docker compose exec backend python manage.py createsuperuser

full:
	make down && make build && docker image prune -f && make up-d
