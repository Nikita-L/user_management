.PHONY: up restart logs down logs build shell bash format test ps stats


up:
	docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . up -d

restart:
	docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . restart api

logs:
	docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . logs -f

down:
	docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . down --remove-orphans

build:
	docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . build

shell:
	docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . exec api python

bash:
	docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . exec api bash

format:
	docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . exec api pre-commit run --all-files

test:
	docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . exec api pytest -vv .

ps:
	docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . ps

stats:
	docker stats
