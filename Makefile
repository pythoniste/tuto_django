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

.PHONY: bash
bash:
	docker compose run tuto_django bash

.PHONY: lock
lock:
	docker compose run tuto_django poetry lock
	docker compose cp tuto_django:/opt/app/poetry.lock ./poetry.lock
