test:
	pytest -s -vv --cov-report term-missing --cov-report html --cov-branch --cov cadcad/

lint:
	@echo
	isort --diff -c .
	@echo
	black --diff --color .
	@echo
	flake8 .

format:
	isort .
	black -q .
