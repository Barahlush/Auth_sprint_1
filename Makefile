SHELL := /bin/bash -O globstar

test:
	pytest tests

lint:
	@echo
	ruff .
	@echo
	blue --check --diff --color .
	@echo
	mypy .
	@echo
	pip-audit


format:
	ruff --silent --exit-zero --fix .
	blue .

build:
	poetry export -f requirements.txt --output auth_service/requirements.txt --without-hashes
	docker-compose build

run:
	cp .env.example .env
	cp .docker.env.example .docker.env
	poetry export -f requirements.txt --output auth_service/requirements.txt --without-hashes
	docker-compose -f docker-compose.yml up --build -d

auto_run_tests_local:
	# Build and spin up main services, and run all tests interactively
	docker-compose -f docker-compose.yml -f tests/docker-compose.yml -f tests/docker-compose.tests.yml up --build

auto_run_tests_in_docker_container:
	# Build and spin up main services with open external ports.
	# Use when you want to run tests locally of debug services directly
	poetry export -f requirements.txt --output tests/requirements.txt --without-hashes
	docker-compose -f docker-compose.yml -f tests/docker-compose.yml up --build -d