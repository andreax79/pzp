SHELL=/bin/bash -e

.PHONY: help
help:
	@echo - make black ------ Format code
	@echo - make clean ------ Clean virtual environment
	@echo - make coverage --- Run tests coverage
	@echo - make docs ------- Make docs
	@echo - make lint ------- Run lint
	@echo - make test ------- Run test
	@echo - make typecheck -- Typecheck
	@echo - make venv ------- Create virtual environment

.PHONY: black
black:
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
	python3 -m virtualenv .
	. bin/activate; pip install -Ur requirements.txt
	. bin/activate; pip install -Ur requirements-dev.txt
