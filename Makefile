#SHELL := /bin/bash -O globstar

test:
	pytest tests

lint:
	@echo
	poetry run ruff .
	@echo
	poetry run blue --check --diff --color .
	@echo
	poetry run mypy .
	@echo
	poetry run pip-audit --ignore PYSEC-2022-42969


format:
	poetry run ruff --silent --exit-zero --fix .
	poetry run blue .

build:
	poetry export -f requirements.txt --output auth_service/requirements.txt --without-hashes
	docker-compose build

run:
	cp .env.example .env
	cp .docker.env.example .docker.env
	poetry export -f requirements.txt --output auth_service/requirements.txt --without-hashes
	docker-compose -f docker-compose.yml up --build

run_dev:
	# Build and spin up main services with open external ports.
	# Use when you want to run tests locally of debug services directly
	cp .env.example .env
	cp tests/.env.test.example tests/.docker.env
	poetry export -f requirements.txt --output auth_service/requirements.txt --without-hashes
	poetry export -f requirements.txt --output tests/requirements.txt --without-hashes
	docker-compose -f docker-compose.yml -f tests/docker-compose.yml up --build -d