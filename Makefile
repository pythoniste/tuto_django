##
# Tuto for Django
#
# @file
# @version 0.1
MAKEFLAGS+="-j 2"

.PHONY: build
build:
	docker compose build

.PHONY: build
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

.PHONY: lock
lock:
	docker compose exec tuto_django poetry lock
	docker compose cp tuto_django:/opt/app/poetry.lock ./poetry.lock
