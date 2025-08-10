# Contributing to OHDSI Cohort Schemas

We welcome contributions! This document explains how to contribute to the OHDSI Cohort Schemas project.

## Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/clsweeting/ohdsi-cohort-schemas.git
   cd ohdsi-cohort-schemas
   ```

2. **Install Poetry** (if not already installed):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **Install dependencies**:
   ```bash
   poetry install
   ```

4. **Install pre-commit hooks**:
   ```bash
   poetry run pre-commit install
   ```

## Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src/ohdsi_cohort_schemas

# Run specific test file
poetry run pytest tests/test_concept_sets.py
```

## Code Style

We use several tools to maintain code quality:

- **Black**: Code formatting
- **Ruff**: Linting and import sorting
- **MyPy**: Static type checking

Run all checks:
```bash
# Format code
poetry run black src tests examples

# Lint code
poetry run ruff check src tests examples

# Type checking
poetry run mypy src
```

## Adding New Models

When adding support for new Circe schema elements:

1. **Add the Pydantic model** in the appropriate file under `src/ohdsi_cohort_schemas/models/`
2. **Use Field aliases** for Circe JSON compatibility (e.g., `alias="CamelCase"`)
3. **Add comprehensive docstrings** explaining the field purpose
4. **Include the model** in `__init__.py` exports
5. **Write tests** in the `tests/` directory
6. **Add examples** in the `examples/` directory

### Example Model Structure

```python
class NewCriteria(BaseCriteria):
    """Represents criteria for new domain events."""
    
    codeset_id: Optional[int] = Field(None, alias="CodesetId", description="Reference to concept set")
    occurrence_date: Optional[DateRange] = Field(None, alias="OccurrenceDate", description="Date range")
    custom_field: Optional[str] = Field(None, alias="CustomField", description="Custom field description")
```

## Testing Against Circe Examples

To ensure compatibility with real Circe expressions:

1. **Download Circe test data** (if not already available)
2. **Run validation examples**:
   ```bash
   poetry run python examples/validate_circe_examples.py
   ```
3. **Add new test cases** for any schema elements you discover

## Documentation

- **Update README.md** if adding major features
- **Add docstrings** to all new classes and methods
- **Include examples** in docstrings when helpful
- **Update type hints** and ensure MyPy passes

## Pull Request Process

1. **Create a feature branch** from `main`
2. **Make your changes** following the style guidelines
3. **Add/update tests** for your changes
4. **Ensure all checks pass**:
   ```bash
   poetry run pytest
   poetry run black --check src tests examples
   poetry run ruff check src tests examples
   poetry run mypy src
   ```
5. **Update documentation** as needed
6. **Submit a pull request** with a clear description

## Schema Evolution

When updating schemas to match new Circe versions:

1. **Identify changes** in the Circe schema
2. **Update models** to match new structure
3. **Maintain backwards compatibility** when possible
4. **Add migration helpers** if breaking changes are needed
5. **Document changes** in the changelog

## Release Process

1. **Update version** in `pyproject.toml`
2. **Update CHANGELOG.md** with new features/fixes
3. **Create a git tag** with the version number
4. **Build and publish** to PyPI:
   ```bash
   poetry build
   poetry publish
   ```

## Getting Help

- **Open an issue** for bugs or feature requests
- **Join discussions** in the GitHub Discussions tab
- **Ask questions** in the OHDSI Forums

Thank you for contributing!
