#SHELL := /bin/bash -O globstar

first_run:
	# Команда для первого запуска
	cp .env.example .env
	cp .docker.env.example .docker.env
	docker-compose -f docker-compose.yml up --build -d

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
	poetry export -f requirements.txt --output auth_service/requirements.txt --without-hashes
	docker-compose up --build