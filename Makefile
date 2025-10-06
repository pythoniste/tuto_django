##
# Tuto for Django
#
# @file
# @version 0.1
MAKEFLAGS+="-j 2"

.PHONY: build
build:
	docker compose build --progress=plain --no-cache

.PHONY: dev
dev:
	docker compose up -d

.PHONY: stop
stop:
	docker compose down

.PHONY: bash
bash:
	docker compose exec tuto_django bash

# end
