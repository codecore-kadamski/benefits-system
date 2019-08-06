PROJECT_NAME := front
#SHELL := /bin/bash

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

develop:  ##  poetry install requirements
	@-poetry install -n

create-volumes:
	@echo "#### TIMESTAMP:"`date "+%s %Y-%m-%d %H:%M:%S"`" ####"
	-docker volume create --name=$(PROJECT_NAME)-media-volume

create-network:  ## tworzy ścieć dockera
	@echo "#### TIMESTAMP:"`date "+%s %Y-%m-%d %H:%M:%S"`" ####"
	-docker network create default_net
	-docker network create $(PROJECT_NAME)_test

image: web_image nginx_image  ## tworzy obrazy dockera

web_image:
	@echo "#### TIMESTAMP:"`date "+%s %Y-%m-%d %H:%M:%S"`" ####"
	docker build -t $(PROJECT_NAME):latest --rm . 

nginx_image:
	@echo "#### TIMESTAMP:"`date "+%s %Y-%m-%d %H:%M:%S"`" ####"
	docker build -t $(PROJECT_NAME)_nginx:latest --rm -f Dockerfile.nginx .

run:  ## uruchamia projekt
	docker-compose -f docker-compose-local.yml up
