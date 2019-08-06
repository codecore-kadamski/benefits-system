SHELL := /bin/bash

RED := \u001b[0;31m
NC := \u001b[0m
GREEN := \u001b[0;32m
YELLOW := \u001b[1;33m

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

start:  ##  start project in containers
	@-docker volume create --name=front-media-volume
	@-docker-compose up --build -d

stop:  ##  stop project
	@-docker-compose stop
	@-docker-compose down

docker-rmi:  ##  usuwanie obrazów 
	@-docker rmi -f $$(docker images)

docker-rm:  ##  usuwanie kontenerów
	@-docker rm -f $$(docker ps -a -q)