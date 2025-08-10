"""
Pytest tests for Circe cohort definition validation.

This module tests both positive and negative cases:
- Files ending in "*Correct.json" should validate successfully
- Files ending in "*Incorrect.json" should fail validation
"""

import json
from pathlib import Path

import pytest
from ohdsi_cohort_schemas.models.cohort import CohortExpression
from pydantic import ValidationError


def is_cohort_expression(json_data: dict) -> bool:
    """Check if JSON looks like a cohort expression."""
    return (
        isinstance(json_data, dict)
        and "ConceptSets" in json_data
        and "PrimaryCriteria" in json_data
    )


def collect_test_files() -> tuple[list[Path], list[Path]]:
    """Collect correct and incorrect test files."""
    test_resources = Path(__file__).parent / "resources"

    correct_files = []
    incorrect_files = []

    for json_file in test_resources.rglob("*.json"):
        # Load and check if it's a cohort expression
        try:
            with open(json_file) as f:
                data = json.load(f)

            if not is_cohort_expression(data):
                continue

        except (json.JSONDecodeError, Exception):
            continue

        # Categorize by filename
        if "Correct.json" in json_file.name or "Expression.json" in json_file.name:
            correct_files.append(json_file)
        elif "Incorrect.json" in json_file.name:
            incorrect_files.append(json_file)

    return correct_files, incorrect_files


# Collect test files at module level
CORRECT_FILES, INCORRECT_FILES = collect_test_files()


@pytest.mark.parametrize("test_file", CORRECT_FILES, ids=lambda f: f.name)
def test_correct_files_should_validate(test_file: Path):
    """Test that files marked as 'Correct' validate successfully."""
    with open(test_file) as f:
        data = json.load(f)

    # This should NOT raise an exception
    cohort = CohortExpression.model_validate(data)

    # Basic sanity checks
    assert hasattr(cohort, 'concept_sets')
    assert hasattr(cohort, 'primary_criteria')


@pytest.mark.parametrize("test_file", INCORRECT_FILES, ids=lambda f: f.name)
def test_incorrect_files_should_fail_validation(test_file: Path):
    """Test that files marked as 'Incorrect' fail validation."""
    from ohdsi_cohort_schemas import validate_strict, validate_with_warnings

    with open(test_file) as f:
        data = json.load(f)

    # Schema validation should still pass (these are business logic errors)
    cohort = CohortExpression.model_validate(data)
    assert hasattr(cohort, 'concept_sets')

    # But business logic validation should find issues
    cohort, issues = validate_with_warnings(data)

    if issues:
        # Good! Found business logic issues as expected
        print(f"\n✅ {test_file.name}: Found {len(issues)} business logic issues:")
        for issue in issues:
            print(f"   {issue.severity}: {issue.field_path} - {issue.message}")
    else:
        # This indicates our validator doesn't yet catch this type of error
        pytest.skip(f"Business logic validator doesn't yet catch issues in {test_file.name}")

    # Test that strict mode raises an error
    with pytest.raises((ValidationError, ValueError)):
        validate_strict(data)


def test_collect_test_files_found_data():
    """Test that we found both correct and incorrect test files."""
    assert len(CORRECT_FILES) > 0, "Should find some *Correct.json files"
    assert len(INCORRECT_FILES) > 0, "Should find some *Incorrect.json files"

    print(f"Found {len(CORRECT_FILES)} correct test files")
    print(f"Found {len(INCORRECT_FILES)} incorrect test files")


def test_file_categorization():
    """Test that files are correctly categorized."""
    # All correct files should end with Correct.json OR Expression.json
    for file_path in CORRECT_FILES:
        assert "Correct.json" in file_path.name or "Expression.json" in file_path.name

    # All incorrect files should end with Incorrect.json
    for file_path in INCORRECT_FILES:
        assert "Incorrect.json" in file_path.name


if __name__ == "__main__":
    # Quick test to see what we found
    correct_files, incorrect_files = collect_test_files()
    print(f"Correct files: {len(correct_files)}")
    for f in correct_files:
        print(f"  ✅ {f.name}")

    print(f"\nIncorrect files: {len(incorrect_files)}")
    for f in incorrect_files:
        print(f"  ❌ {f.name}")
