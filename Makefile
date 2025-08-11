.PHONY: help install test lint format type-check validate-examples clean build publish docs

# Default target
help:
	@echo "Available commands:"
	@echo "  install           Install dependencies with Poetry"
	@echo "  test             Run tests with pytest"
	@echo "  test-cov         Run tests with coverage reporting"
	@echo "  lint             Run linting with ruff"
	@echo "  format           Format code with black"
	@echo "  type-check       Run type checking with mypy"
	@echo "  validate-examples Run example validation scripts"
	@echo "  validate-all-circe Validate against ALL Circe test data (223 files)"
	@echo "  check-all        Run all checks (lint, format, type-check, test)"
	@echo "  clean            Clean build artifacts"
	@echo "  build            Build package"
	@echo "  publish          Publish to PyPI"
	@echo "  docs             Build documentation"

# Development setup
install:
	poetry install
	poetry run pre-commit install

# Testing
test:
	poetry run pytest

test-cov:
	poetry run pytest --cov=src/ohdsi_cohort_schemas --cov-report=html --cov-report=term-missing

# Code quality
lint:
	poetry run ruff check src tests examples

format:
	poetry run black src tests examples

format-check:
	poetry run black --check src tests examples

type-check:
	poetry run mypy src

# Examples
validate-examples:
	poetry run python examples/basic_validation.py
	poetry run python examples/validate_test_data.py

validate-all-circe:
	poetry run python tests/test_all_circe_data.py

# Combined checks
check-all: lint format-check type-check test

# Build and publish
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build: clean
	poetry build

publish: build
	poetry publish

# Documentation (placeholder for future)
docs:
	@echo "Documentation build not yet implemented"

# Development helpers
fix:
	poetry run ruff check --fix src tests examples
	poetry run black src tests examples

# Install in development mode
dev-install:
	poetry install
	poetry run pip install -e .
