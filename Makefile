.PHONY: setup
setup:
	pip install -r requirements.txt

.PHONY: setup-dev
setup-dev:
	pip install -r requirements-dev.txt

.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete

.PHONY: lint
lint:
	flake8 .

.PHONY: format
format:
	black .

.PHONY: test
test:
	pytest -v

.PHONY: serve
serve:
	uvicorn app:app --reload

.PHONY: coverage
coverage:
	coverage run -m pytest
	coverage report

.PHONY: help
help:
	@echo "clean - remove Python artifacts"
	@echo "lint - check style with flake8"
	@echo "format - format code with black"
	@echo "test - run tests with pytest"
	@echo "serve - start the development server with uvicorn"
