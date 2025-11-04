# Build and publish commands

.PHONY: build clean test publish testpypi install install-dev lint format typecheck

build:
	python -m build

clean:
	rm -rf dist/ build/ *.egg-info

test:
	python -m pytest

publish:
	python -m twine upload dist/*

testpypi:
	python -m twine upload --repository testpypi dist/*

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

lint:
	ruff check endercom/
	black --check endercom/

format:
	black endercom/
	ruff check --fix endercom/

typecheck:
	mypy endercom/

