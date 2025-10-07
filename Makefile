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

.PHONY: bash
bash:
	docker compose run tuto_django bash

.PHONY: lock
lock:
	docker compose run tuto_django poetry lock

.PHONY: check
check:
	docker compose run tuto_django make check

.PHONY: update
update:
	docker compose run tuto_django make update

# end
