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

.PHONY: restart
restart:
	docker compose restart tuto_django tuto_django_celery tuto_django_celery_beat

.PHONY: bash
bash:
	docker compose run tuto_django bash

.PHONY: python
python:
	docker compose exec tuto_django poetry run bpython

.PHONY: shell
shell:
	docker compose run tuto_django poetry run python manage.py shell_plus

.PHONY: logs
logs:
	docker compose logs tuto_django -f

.PHONY: logs_celery
logs_celery:
	docker compose logs tuto_django_celery -f

.PHONY: logs_beat
logs_beat:
	docker compose logs tuto_django_celery_beat -f

.PHONY: create_admin
create_admin:
	docker compose run tuto_django make create_admin

.PHONY: lock
lock:
	docker compose run tuto_django poetry lock

.PHONY: check
check:
	docker compose run tuto_django make check

.PHONY: update
update:
	docker compose run tuto_django make update

.PHONY: django_ip
django_ip:
	docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' tuto_django > project/internal_django_ip_address.txt

.PHONY: graph_app_models
graph_app_models:
	docker compose run tuto_django poetry run python manage.py graph_models app --pydot -o doc/models/app.png

.PHONY: graph_app_models
graph_project_models:
	docker compose run tuto_django poetry run python manage.py graph_models --pydot -a -g -o doc/models/project.png

.PHONY: save
save:
	docker compose run tuto_django make save

.PHONY: load
load:
	docker compose run tuto_django make load

.PHONY: reset
reset:
	make stop
	docker volume rm tuto_django_pg_data
	docker compose run tuto_django make create_db
	make dev

.PHONY: show_urls
show_urls:
	docker compose run tuto_django make show_urls

.PHONY: messages
messages:
	docker compose run tuto_django make messages

.PHONY: compile_messages
compile_messages:
	docker compose run tuto_django make compile_messages

.PHONY: import_games
import_games:
	docker compose run tuto_django make import_games

.PHONY: export_games
export_games:
	docker compose run tuto_django make export_games

.PHONY: test_unit
test_unit:
	docker compose run tuto_django make test_unit

.PHONY: test_e2e
test_e2e:
	docker compose run tuto_django make test_e2e

.PHONY: test_all
test_all:
	make test_unit
	make test_e2e

# end
