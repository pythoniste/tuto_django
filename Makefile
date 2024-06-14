##
# Tuto for Django
#
# @file
# @version 0.1
MAKEFLAGS+="-j 2"

build:
	docker compose build --progress=plain --no-cache

dev:
	docker compose up -d

# end
