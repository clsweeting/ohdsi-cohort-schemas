#!/usr/bin/env python3
"""
Validate Circe cohort expression examples from test_data folder.

This script tests our Pydantic models against official Circe JSON examples
that we've copied to our test_data folder for consistent testing.

Run with: poetry run python examples/validate_test_data.py
"""

import json
import sys
from pathlib import Path

from ohdsi_cohort_schemas.models.cohort import CohortExpression
from pydantic import ValidationError


def validate_file(json_path: Path) -> bool:
    """Validate a single JSON file against our CohortExpression model."""

    print("=" * 60)
    print(f"Testing: {json_path.name}")
    print("=" * 60)

    try:
        # Load JSON
        with open(json_path) as f:
            json_data = json.load(f)
        print(f"✅ Loaded JSON ({len(json.dumps(json_data))} chars)")

        # Validate with Pydantic
        cohort_expr = CohortExpression.model_validate(json_data)
        print("✅ Validation successful!")

        # Show some basic info
        print(f"   - Concept sets: {len(cohort_expr.concept_sets)}")
        print(f"   - Inclusion rules: {len(cohort_expr.inclusion_rules)}")

        # Show concept set details
        for i, cs in enumerate(cohort_expr.concept_sets):
            print(f"   - Concept set {i}: '{cs.name}' ({len(cs.expression.items)} concepts)")

        print()
        return True

    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing failed: {e}")
        return False

    except ValidationError as e:
        print("❌ Validation failed:")
        for error in e.errors():
            field_path = ".".join(str(x) for x in error["loc"])
            print(f"     {field_path}: {error['msg']}")
        print()
        return False

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def main():
    """Validate all Circe example files in our test_data folder."""

    # Use our test_data folder with official Circe JSONs
    test_data_path = Path(__file__).parent.parent / "test_data"

    if not test_data_path.exists():
        print(f"❌ Test data folder not found at: {test_data_path}")
        print("   Run: make setup-test-data")
        return False

    # Find all JSON files
    json_files = list(test_data_path.glob("*.json"))

    if not json_files:
        print("❌ No JSON files found in test_data folder")
        return False

    print(f"Found {len(json_files)} official Circe JSON files to validate\n")

    # Validate each file
    success_count = 0
    for json_file in sorted(json_files):
        if validate_file(json_file):
            success_count += 1

    # Summary
    print("=" * 60)
    print(f"SUMMARY: {success_count}/{len(json_files)} files validated successfully")
    print("=" * 60)

    if success_count == len(json_files):
        print("🎉 All tests passed! Our schemas are compatible with Circe.")
    else:
        print("❌ Some tests failed. Schema improvements needed.")

    return success_count == len(json_files)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
