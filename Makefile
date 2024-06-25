SHELL=/bin/bash -e

.PHONY: help
help:
	@echo - make black ----------- Format code
	@echo - make isort ----------- Sort imports
	@echo - make clean ----------- Clean virtual environment
	@echo - make coverage -------- Run tests coverage
	@echo - make docs ------------ Make docs
	@echo - make readme-preview -- Readme preview
	@echo - make lint ------------ Run lint
	@echo - make test ------------ Run test
	@echo - make typecheck ------- Typecheck
	@echo - make venv ------------ Create virtual environment

.PHONY: isort
isort:
	@isort --profile black pzp tests examples setup.py

.PHONY: black
black: isort
	@black -S pzp tests examples setup.py

.PHONY: clean
clean:
	-rm -rf build dist
	-rm -rf *.egg-info
	-rm -rf bin lib share pyvenv.cfg

.PHONY: coverage
coverage:
	@pytest --cov --cov-report=term-missing

.PHONY: docs
docs:
	@mkdocs build
	@mkdocs gh-deploy

.PHONY: venv
readme-preview:
	@. bin/activate; grip 0.0.0.0:8080

.PHONY: lint
lint:
	@flake8 pzp tests

.PHONY: test
test:
	@pytest

.PHONY: typecheck
typecheck:
	@mypy --strict --no-warn-unused-ignores pzp

.PHONY: venv
venv:
	python3 -m virtualenv . || python3 -m venv .
	. bin/activate; pip install -Ur requirements.txt
	. bin/activate; pip install -Ur requirements-dev.txt
