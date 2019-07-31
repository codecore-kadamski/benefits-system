# HERE = $(shell pwd)
# VENV = .
# VIRTUALENV = .venv
# BIN = $(VENV)/bin
# PYTHON = $(BIN)/python

# INSTALL = $(BIN)/pip install --no-deps

# .PHONY: all test docs build_extras

# all: build

# $(PYTHON):
# 	$(VIRTUALENV) $(VTENV_OPTS) $(VENV)

# build: $(PYTHON)
# 	$(PYTHON) setup.py develop

# clean:
# 	rm -rf $(VENV)

# test_dependencies:
# 	$(BIN)/pip install flake8 tox

# test: build test_dependencies
# 	$(BIN)/tox

# run:
# 	FLASK_APP=auth-service bin/flask run

# start:  ##  start project in containers
# 	@-docker-compose up --build -d


SHELL := /bin/bash
SERVER_ROOT := c4a_smart
APPS := '${SERVER_ROOT}.apps.$(app)'
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

# migrations: start-db ##  run db migrations : exp. make migrations sleep=2
# 	@-poetry run python manage.py migrate

migrations:  ##  run db migrations : exp. make migrations sleep=2
	@-poetry run python manage.py migrate

init-db:  #  create postgres image for docker
	@-cd ../ && ./scripts/docker_psql.sh init

start-db: #  run postgres container
	@-cd ../ && ./scripts/docker_psql.sh
	@-if [ ! -z $(sleep) ]; then \
		echo -e '${GREEN}Wait ${WAIT} seconds for start postgres ... then migrations will be execute${NC}'; \
	else \
		echo -e '${GREEN}Run db migrations${NC}'; \
	fi
	@-sleep ${WAIT}

start-local-server: #  start server
	@-poetry run gunicorn -b 0.0.0.0:5000

init-users: ##  create defaults users and groups
	@-poetry run python manage.py initusers

start-redis:
	@-../scripts/docker_redis.sh

# start: start-redis start-db migrations init-users start-local-server ##  start local server

start:  ##  start project in containers
	@-docker-compose up --build -d

stop:  #  stop project
	@-docker-compose stop
	@-docker-compose down

develop:  ##  poetry install requirements
	@-poetry install -n

docstyle:  ##  check docstyle
	@-poetry run pydocstyle --ignore=D205,D211,D212,D400 ${SERVER_ROOT}

codestyle:  ##  check codestyle flake8 pep8
	@-poetry run flake8 ${SERVER_ROOT}

test:  ##  runing all tests or specific test by parameter : exp. make test app=vehicles
	@-mkdir -p reports
	@-if [ ! -z $(app) ]; then \
		poetry run coverage run --source=${APPS} ./manage.py test --noinput ${APPS}; \
	else \
		poetry run coverage run --source=${SERVER_ROOT} ./manage.py test --noinput ${SERVER_ROOT}; \
	fi
	@-poetry run coverage report -m --skip-covered
	@-poetry run coverage html

test-coverage:  ##  test-coverage
	@-docker-compose up test-coverage

report-html:  ##  view coverage report in browser
	@-google-chrome htmlcov/index.html


docker-rmi:
	@-docker rmi -f $(docker images)

docker-rm:
	@-docker rm $(docker ps -a -q)