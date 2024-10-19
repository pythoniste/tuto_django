##
# Tuto for Django
#
# @file
# @version 0.1
MAKEFLAGS+="-j 2"

.PHONY: dev
dev:
	poetry run python manage.py runserver 0.0.0.0:8000

.PHONY: update
update:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate
	poetry run python manage.py collectstatic --noinput

.PHONY: dump
dump:
	poetry run python manage.py dumpdata app  -o app/fixtires/test_data.json --indent 4

.PHONY: load
load:
	poetry run python manage.py loaddata test_data

.PHONY: check
check:
	poetry run python manage.py check

.PHONY: create_admin
create_admin:
	DJANGO_SUPERUSER_PASSWORD=adminadmin poetry run python manage.py createsuperuser --noinput --username admin --email admin@example.com

.PHONY: test_unit
test_unit:
	poetry run python manage.py test

.PHONY: test_behave
test_behave:
	poetry run python manage.py behave

.PHONY: test_all
test_all:
	make test_unit
	make test_behave
