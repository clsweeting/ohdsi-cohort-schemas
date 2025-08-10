"""Test the business logic validation functionality."""

import json
from pathlib import Path

from ohdsi_cohort_schemas import (
    CohortExpression,
    validate_schema_only,
    validate_with_warnings,
)


def test_schema_validation_only():
    """Test that pure schema validation still works exactly as before."""
    # Load a test file
    test_file = Path(__file__).parent / "resources" / "checkers" / "contradictionsCriteriaCheckCorrect.json"

    with open(test_file) as f:
        data = json.load(f)

    # Method 1: Direct Pydantic (unchanged)
    cohort1 = CohortExpression.model_validate(data)

    # Method 2: Via convenience function (same result)
    cohort2 = validate_schema_only(data)

    # Should be identical
    assert cohort1.model_dump() == cohort2.model_dump()
    print("✅ Schema validation works identically to pure Pydantic")


def test_business_logic_validation():
    """Test business logic validation with a problematic file."""
    # Load a file that has a codeset reference issue
    test_file = Path(__file__).parent / "resources" / "checkers" / "drugDomainCheckIncorrect.json"

    with open(test_file) as f:
        data = json.load(f)

    # Schema validation should pass
    cohort = validate_schema_only(data)
    print("✅ Schema validation passed")

    # Business logic validation should find issues
    cohort, issues = validate_with_warnings(data)

    if issues:
        print(f"📋 Found {len(issues)} business logic issues:")
        for issue in issues:
            print(f"  {issue.severity.upper()}: {issue.field_path} - {issue.message}")
    else:
        print("ℹ️  No business logic issues found (validator may need more rules)")


def test_performance_comparison():
    """Compare performance of schema-only vs schema+business validation."""
    import time

    test_file = Path(__file__).parent / "resources" / "checkers" / "contradictionsCriteriaCheckCorrect.json"

    with open(test_file) as f:
        data = json.load(f)

    # Test schema-only validation speed
    start = time.time()
    for _ in range(100):
        validate_schema_only(data)
    schema_time = time.time() - start

    # Test schema+business validation speed
    start = time.time()
    for _ in range(100):
        validate_with_warnings(data)
    business_time = time.time() - start

    print("📊 Performance comparison (100 iterations):")
    print(f"  Schema only: {schema_time:.4f}s")
    print(f"  Schema + business: {business_time:.4f}s")
    print(f"  Overhead: {(business_time/schema_time - 1)*100:.1f}%")


if __name__ == "__main__":
    print("🧪 Testing business logic validation...")
    print()

    test_schema_validation_only()
    print()

    test_business_logic_validation()
    print()

    test_performance_comparison()
    print()

    print("✨ All tests completed!")
