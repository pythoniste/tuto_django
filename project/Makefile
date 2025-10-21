##
# Tuto for Django
#
# @file
# @version 0.1
MAKEFLAGS+="-j 2"

.PHONY: dev
dev:
	poetry run python manage.py runserver 0.0.0.0:8000

.PHONY: check
check:
	poetry run python manage.py check

.PHONY: update
update:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate
	poetry run python manage.py collectstatic --no-input

.PHONY: create_admin
create_admin:
	DJANGO_SUPERUSER_PASSWORD=adminadmin poetry run python manage.py createsuperuser --noinput --username admin --email admin@example.com

.PHONY: save
save:
	poetry run python manage.py dumpdata app --indent 4 -o app/fixtures/test_data.json
	poetry run python manage.py dumpdata auth --indent 4 -o app/fixtures/auth_data.json

.PHONY: load
load:
	poetry run python manage.py loaddata app/fixtures/auth_data.json
	poetry run python manage.py loaddata app/fixtures/test_data.json

.PHONY: create_db
create_db:
	make update
	make load

.PHONY: show_urls
show_urls:
	poetry run python manage.py show_urls

.PHONY: messages
messages:
	poetry run python manage.py makemessages -l fr

.PHONY: compile_messages
compile_messages:
	poetry run python manage.py compilemessages

# end
