##
# Tuto for Django
#
# @file
# @version 0.1
MAKEFLAGS+="-j 2"

.PHONY: build
build:
	docker compose build

.PHONY: build-dev
build-dev:
	docker compose build --progress=plain --no-cache

.PHONY: dev
dev:
	docker compose up -d

.PHONY: stop
stop:
	docker compose down
# end

.PHONY: debug
debug:
	docker compose run tuto_django bash

.PHONY: bash
bash:
	docker compose exec tuto_django bash

.PHONY: python
python:
	docker compose exec tuto_django poetry run bpython

.PHONY: shell
shell:
	docker compose run tuto_django poetry run python manage.py shell_plus

.PHONY: create_admin
create_admin:
	docker compose run DJANGO_SUPERUSER_PASSWORD=adminadmin poetry run python manage.py createsuperuser --noinput --username admin --email admin@example.com

.PHONY: lock
lock:
	docker compose exec tuto_django poetry lock
	docker compose cp tuto_django:/opt/app/poetry.lock ./poetry.lock

.PHONY: django_ip
django_ip:
	docker inspect   -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' tuto_django > project/internal_django_ip_address.txt

.PHONY: logs
logs:
	docker compose logs tuto_django -f
