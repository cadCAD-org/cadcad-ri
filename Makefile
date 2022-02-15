test:
	pytest -s --cov-report term-missing --cov-report html --cov-branch --cov cadcad/

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
