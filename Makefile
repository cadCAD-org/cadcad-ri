test:
	pytest --cov-report term-missing --cov-report html --cov-branch --cov app/

lint:
	@echo
	isort --diff -c .
	@echo
	yapf --diff .
	@echo
	flake8 .
	@echo
	mypy .

format:
	isort .
	yapf --in-place .
