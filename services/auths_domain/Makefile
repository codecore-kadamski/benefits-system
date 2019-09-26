#SHELL := /bin/bash
SERVER_ROOT := auths_domain
#APPS := '${SERVER_ROOT}.apps.$(app)'
WAIT := 2
RED := \u001b[0;31m
NC := \u001b[0m
GREEN := \u001b[0;32m
YELLOW := \u001b[1;33m

ifneq ($(sleep),)
	WAIT=$(sleep)
endif


.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
    match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
    if match:
        target, help = match.groups()
        print(f'${GREEN}{target :20s}${NC} ${YELLOW}{help}${NC}')
endef

export PRINT_HELP_PYSCRIPT


help:
	@-python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

db-init:
	@-rm -rf migrations
	@-export ENVIRON="dev" && poetry run python manage.py db init
	@-export ENVIRON="test" && poetry run python manage.py db init
	@-export ENVIRON="prod" && poetry run python manage.py db init

migrations-dev:  ##  migracje dev
	@-rm -rf auths_domain/migrations/dev
	@-export ENVIRON="dev" && poetry run python manage.py drop_db
	@-export ENVIRON="dev" && poetry run python manage.py db init
	@-export ENVIRON="dev" && poetry run python manage.py db migrate && poetry run python manage.py db upgrade

migrations-test:  ##  migracje test
	@-rm data-test.db
	@-rm -rf auths_domain/migrations/test
	@-export ENVIRON="test" && poetry run python manage.py db init
	@-export ENVIRON="test" && poetry run python manage.py db migrate && poetry run python manage.py db upgrade

# migrations-test:  ## migracje-testowe
# 	@-rm data-test.db
# 	@-rm data.db

start-local-server:  ##  start local server
	@-poetry run gunicorn -c gunicorn_config wsgi

start:  ##  start project in containers
	@-docker-compose up --build -d

stop:  ##  stop project
	@-docker-compose stop
	@-docker-compose down

develop:  ##  poetry install requirements
	@-poetry install -n

test: migrations-test  ##  uruchamiamy testy
	@-export ENVIRON="test" && poetry run python manage.py create_db && poetry run python manage.py db upgrade && poetry run python manage.py test

docker-rmi:
	@-docker rmi -f $(docker images)

docker-rm:
	@-docker rm $(docker ps -a -q)