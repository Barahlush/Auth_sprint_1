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
	poetry export -f requirements.txt --output auth_service/requirements.txt --without-hashes
	docker-compose up --build