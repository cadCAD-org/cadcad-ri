test:
	pytest -s -vv --cov-report term-missing --cov-report html --cov-branch --cov cadcad/

lint:
	@echo
	isort --diff -c .
	@echo
	black --diff --color .
	@echo
	flake8 .
	@echo
	mypy .

format:
	isort .
	black -q .
