.PHONY: pre-commit
pre-commit:
	@echo running black
	@black .
	@echo running isort
	@isort .
	@echo running flake8
	@flake8 --max-line-length 91

.PHONY: migrations
migrations:
	@python3 manage.py makemigrations

.PHONY: migrate
migrate:
	@python3 manage.py migrate

.PHONY: database
database:
	@make migrations
	@make migrate

.PHONY: run
run:
	@python3 manage.py runserver
