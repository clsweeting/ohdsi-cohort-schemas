#!/usr/bin/env python3
"""
Comprehensive validation against ALL Circe test data.

This module validates our Pydantic models against the complete Circe test suite
to ensure maximum compatibility with OHDSI standards.
"""

import json
from pathlib import Path

import pytest
from ohdsi_cohort_schemas.models.cohort import CohortExpression
from pydantic import ValidationError


def is_cohort_expression(json_data: dict) -> bool:
    """Check if JSON looks like a cohort expression."""
    # CohortExpression should have ConceptSets and PrimaryCriteria
    return isinstance(json_data, dict) and "ConceptSets" in json_data and "PrimaryCriteria" in json_data


def validate_file(json_path: Path) -> tuple[bool, str]:
    """Validate a single JSON file if it's a cohort expression."""

    try:
        # Load JSON
        with open(json_path) as f:
            json_data = json.load(f)

        # Skip if not a cohort expression
        if not is_cohort_expression(json_data):
            return True, "SKIPPED: Not a cohort expression"

        # Validate with Pydantic
        CohortExpression.model_validate(json_data)
        return True, "SUCCESS"

    except json.JSONDecodeError as e:
        return False, f"JSON_ERROR: {e}"

    except ValidationError as e:
        error_summary = []
        for error in e.errors()[:3]:  # Show first 3 errors
            field_path = ".".join(str(x) for x in error["loc"])
            error_summary.append(f"{field_path}: {error['msg']}")
        more = f" (+{len(e.errors())-3} more)" if len(e.errors()) > 3 else ""
        return False, f"VALIDATION_ERROR: {'; '.join(error_summary)}{more}"

    except Exception as e:
        return False, f"UNEXPECTED_ERROR: {e}"


def test_all_circe_data_validates_successfully():
    """Test that all Circe test data validates successfully with our schema."""

    # Find all JSON files in test resources
    test_resources = Path(__file__).parent / "resources"
    json_files = list(test_resources.rglob("*.json"))

    assert json_files, "No JSON files found in tests/resources"

    # Track results by category
    results: dict[str, list[tuple[Path, bool, str]]] = {}
    total_cohort_expressions = 0
    successful_validations = 0

    # Validate each file
    for json_file in sorted(json_files):
        # Get category from path (e.g., "cohortgeneration", "conceptset", "checkers")
        category = json_file.parts[-2] if len(json_file.parts) > 1 else "unknown"

        success, message = validate_file(json_file)

        if category not in results:
            results[category] = []
        results[category].append((json_file, success, message))

        # Count cohort expressions and successes
        if not message.startswith("SKIPPED"):
            total_cohort_expressions += 1
            if success:
                successful_validations += 1

    # Collect all failures for detailed reporting
    failures = []
    for _, category_results in results.items():
        for file_path, success, message in category_results:
            if not success and not message.startswith("SKIPPED"):
                failures.append((file_path.name, message))

    # Print summary for debugging
    print("\nCirce validation summary:")
    print(f"  Total JSON files: {len(json_files)}")
    print(f"  Cohort expressions: {total_cohort_expressions}")
    print(f"  Successfully validated: {successful_validations}")

    if total_cohort_expressions > 0:
        success_rate = (successful_validations / total_cohort_expressions) * 100
        print(f"  Success rate: {success_rate:.1f}%")

    # Assert that all cohort expressions validate successfully
    if failures:
        failure_details = "\n".join([f"  - {name}: {msg[:100]}..." for name, msg in failures[:5]])
        if len(failures) > 5:
            failure_details += f"\n  ... and {len(failures) - 5} more failures"

        pytest.fail(f"{len(failures)} out of {total_cohort_expressions} cohort expressions failed validation:\n" f"{failure_details}")

    # Ensure we actually tested some cohort expressions
    assert total_cohort_expressions > 0, "No cohort expressions found to validate"
    assert successful_validations == total_cohort_expressions, "Not all cohort expressions validated successfully"


if __name__ == "__main__":
    """Run as a standalone script for detailed reporting."""
    import sys

    # Find all JSON files in test resources
    test_resources = Path(__file__).parent / "resources"
    json_files = list(test_resources.rglob("*.json"))

    if not json_files:
        print("❌ No JSON files found in tests/resources")
        sys.exit(1)

    print(f"🔍 Found {len(json_files)} Circe JSON files to validate")
    print("=" * 80)

    # Track results by category
    results: dict[str, list[tuple[Path, bool, str]]] = {}

    # Validate each file
    for json_file in sorted(json_files):
        # Get category from path (e.g., "cohortgeneration", "conceptset", "checkers")
        category = json_file.parts[-2] if len(json_file.parts) > 1 else "unknown"

        success, message = validate_file(json_file)

        if category not in results:
            results[category] = []
        results[category].append((json_file, success, message))

    # Print summary by category
    total_files = 0
    total_success = 0
    total_cohort_expressions = 0

    for category, category_results in sorted(results.items()):
        cohort_files = [r for r in category_results if not r[2].startswith("SKIPPED")]
        success_files = [r for r in category_results if r[1] and not r[2].startswith("SKIPPED")]

        if cohort_files:
            print(f"\n📁 {category.upper()}")
            print(f"   Cohort expressions: {len(cohort_files)}")
            print(f"   ✅ Validated: {len(success_files)}")

            if len(success_files) < len(cohort_files):
                print(f"   ❌ Failed: {len(cohort_files) - len(success_files)}")

                # Show first few failures for debugging
                failures = [r for r in category_results if not r[1]][:3]
                for file_path, _, error in failures:
                    filename = file_path.name
                    # Truncate long error messages
                    error_short = error[:100] + "..." if len(error) > 100 else error
                    print(f"      • {filename}: {error_short}")

        total_files += len(category_results)
        total_success += len([r for r in category_results if r[1]])
        total_cohort_expressions += len(cohort_files)

    # Overall summary
    print("\n" + "=" * 80)
    print("📊 FINAL RESULTS")
    print(f"   Total files processed: {total_files}")
    print(f"   Cohort expressions found: {total_cohort_expressions}")
    print(
        f"   Successfully validated: {len([r for cat_results in results.values() for r in cat_results if r[1] and not r[2].startswith('SKIPPED')])}"
    )

    if total_cohort_expressions > 0:
        success_rate = (
            len([r for cat_results in results.values() for r in cat_results if r[1] and not r[2].startswith("SKIPPED")])
            / total_cohort_expressions
            * 100
        )
        print(f"   Success rate: {success_rate:.1f}%")

        if success_rate == 100.0:
            print("\n🎉 PERFECT SCORE! All cohort expressions validate successfully!")
            print("🚀 Schema library is production-ready for OHDSI ecosystem!")
        elif success_rate >= 90.0:
            print(f"\n✨ EXCELLENT! {success_rate:.1f}% success rate")
            print("📈 Schema library is highly compatible with Circe")
        elif success_rate >= 75.0:
            print(f"\n👍 GOOD! {success_rate:.1f}% success rate")
            print("🔧 Minor schema improvements needed")
        else:
            print(f"\n🔧 NEEDS WORK: {success_rate:.1f}% success rate")
            print("🎯 Schema improvements required")

    success = total_cohort_expressions > 0 and success_rate == 100.0
    sys.exit(0 if success else 1)
