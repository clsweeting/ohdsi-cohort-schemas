"""
Example demonstrating optional business logic validation.

This example shows how to use the OHDSI cohort schema library with
both basic schema validation and optional business logic validation.
"""

import json
from pathlib import Path

from ohdsi_cohort_schemas import (
    BusinessLogicValidator,
    # Basic schema validation
    CohortExpression,
    validate_schema_only,
    validate_strict,
    # Business logic validation
    validate_with_warnings,
)


def example_basic_validation():
    """Example of basic schema validation (fast, reliable)."""
    print("=== Basic Schema Validation ===")

    # Load a test file
    test_file = Path(__file__).parent.parent / "tests" / "resources" / "checkers" / "contradictionsCriteriaCheckCorrect.json"

    with open(test_file) as f:
        data = json.load(f)

    # Method 1: Direct Pydantic usage (recommended for production)
    cohort = CohortExpression.model_validate(data)
    print(f"✅ Schema validation passed: {len(cohort.concept_sets)} concept sets")

    # Method 2: Via convenience function (same result)
    validate_schema_only(data)
    print("✅ Same result via convenience function")


def example_business_logic_validation():
    """Example of business logic validation (slower, catches logical errors)."""
    print("\n=== Business Logic Validation ===")

    # Test with a file that has business logic issues
    test_file = Path(__file__).parent.parent / "tests" / "resources" / "checkers" / "contradictionsCriteriaCheckIncorrect.json"

    with open(test_file) as f:
        data = json.load(f)

    # Schema validation passes (structure is correct)
    cohort = validate_schema_only(data)
    print("✅ Schema validation passed")

    # Business logic validation finds issues
    cohort, issues = validate_with_warnings(data)
    if issues:
        print(f"⚠️  Found {len(issues)} business logic issues:")
        for issue in issues:
            print(f"   {issue.severity.upper()}: {issue.field_path}")
            print(f"   Message: {issue.message}")

    # Strict mode raises an error
    try:
        validate_strict(data)
        print("❌ Strict validation unexpectedly passed")
    except (ValueError, Exception) as e:
        print(f"✅ Strict validation caught the issue: {str(e)[:100]}...")


def example_custom_validator():
    """Example of using the validator directly for custom logic."""
    print("\n=== Custom Validator Usage ===")

    test_file = Path(__file__).parent.parent / "tests" / "resources" / "checkers" / "contradictionsCriteriaCheckCorrect.json"

    with open(test_file) as f:
        data = json.load(f)

    # Create cohort with schema validation
    cohort = CohortExpression.model_validate(data)

    # Create custom validator
    validator = BusinessLogicValidator(strict=False)
    issues = validator.validate(cohort)

    if issues:
        print(f"Found {len(issues)} custom validation issues")
    else:
        print("✅ No business logic issues found in correct file")


def example_performance_comparison():
    """Compare performance of different validation approaches."""
    print("\n=== Performance Comparison ===")
    import time

    test_file = Path(__file__).parent.parent / "tests" / "resources" / "checkers" / "contradictionsCriteriaCheckCorrect.json"

    with open(test_file) as f:
        data = json.load(f)

    # Time schema-only validation
    start = time.time()
    for _ in range(100):
        validate_schema_only(data)
    schema_time = time.time() - start

    # Time schema + business validation
    start = time.time()
    for _ in range(100):
        validate_with_warnings(data)
    business_time = time.time() - start

    print(f"Schema only (100x): {schema_time:.4f}s")
    print(f"Schema + business (100x): {business_time:.4f}s")
    print(f"Overhead: {(business_time/schema_time - 1)*100:.1f}%")

    print("\n💡 Recommendation:")
    print("   - Use schema-only validation for production/performance-critical code")
    print("   - Use business logic validation for development/testing/QA")


if __name__ == "__main__":
    example_basic_validation()
    example_business_logic_validation()
    example_custom_validator()
    example_performance_comparison()

    print("\n🎉 Examples completed!")
    print("\n📖 Key Takeaways:")
    print("   1. Schema validation is fast, reliable, and production-ready")
    print("   2. Business logic validation is optional and catches logical errors")
    print("   3. Both approaches can be used together based on your needs")
    print("   4. The library maintains backward compatibility with pure Pydantic usage")
