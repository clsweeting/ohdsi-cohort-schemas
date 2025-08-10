"""
Example: Validate real Circe cohort expression from test data

This example loads and validates actual cohort expressions from the
Circe test data to ensure our schemas work with real-world examples.

Run with: poetry run python examples/validate_circe_examples.py
"""

import json
from pathlib import Path

from ohdsi_cohort_schemas import CohortExpression
from pydantic import ValidationError


def load_test_cohort(circe_path: str, test_file: str) -> dict:
    """Load a test cohort from Circe test resources."""
    test_path = Path(circe_path) / "src/test/resources" / test_file

    if not test_path.exists():
        raise FileNotFoundError(f"Test file not found: {test_path}")

    with open(test_path) as f:
        return json.load(f)


def main():
    # Path to the circe-be-master directory
    circe_path = Path(__file__).parent.parent.parent / "circe-be-master"

    if not circe_path.exists():
        print(f"❌ Circe directory not found: {circe_path}")
        print("Please ensure circe-be-master is in the expected location")
        return

    # Test files to validate
    test_files = [
        "cohortgeneration/inclusionRules/simpleInclusionRule.json",
        "cohortgeneration/allCriteria/allCriteriaExpression.json",
        "cohortgeneration/exits/fixedOffsetExpression.json",
    ]

    for test_file in test_files:
        print(f"\n{'='*60}")
        print(f"Testing: {test_file}")
        print("=" * 60)

        try:
            # Load the test cohort
            cohort_json = load_test_cohort(circe_path, test_file)
            print(f"✅ Loaded JSON ({len(json.dumps(cohort_json))} chars)")

            # Validate with our schema
            cohort = CohortExpression.model_validate(cohort_json)
            print("✅ Valid cohort definition!")

            # Print summary
            print(f"   - Concept sets: {len(cohort.concept_sets)}")
            print(f"   - Primary criteria: {len(cohort.primary_criteria.criteria_list)}")
            print(f"   - Inclusion rules: {len(cohort.inclusion_rules)}")

            # Show concept set details
            for i, cs in enumerate(cohort.concept_sets):
                print(f"   - Concept set {i}: '{cs.name}' ({len(cs.expression.items)} concepts)")

            # Show inclusion rules
            for i, rule in enumerate(cohort.inclusion_rules):
                print(f"   - Inclusion rule {i}: '{rule.name}'")

        except FileNotFoundError as e:
            print(f"❌ File not found: {e}")
        except ValidationError as e:
            print("❌ Validation failed:")
            for error in e.errors():
                print(f"     {'.'.join(str(x) for x in error['loc'])}: {error['msg']}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
