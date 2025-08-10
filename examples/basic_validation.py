"""
Example: Basic cohort validation using OHDSI Cohort Schemas

This example shows how to validate a simple cohort definition
using the Pydantic models.
"""

from ohdsi_cohort_schemas import CohortExpression
from pydantic import ValidationError


def main():
    # Example cohort JSON (simplified)
    cohort_json = {
        "ConceptSets": [
            {
                "id": 0,
                "name": "Type 2 Diabetes",
                "expression": {
                    "items": [
                        {
                            "concept": {
                                "CONCEPT_ID": 201826,
                                "CONCEPT_NAME": "Type 2 diabetes mellitus",
                                "STANDARD_CONCEPT": "S",
                                "CONCEPT_CODE": "44054006",
                                "CONCEPT_CLASS_ID": "Clinical Finding",
                                "VOCABULARY_ID": "SNOMED",
                                "DOMAIN_ID": "Condition"
                            },
                            "includeDescendants": True,
                            "includeMapped": False,
                            "isExcluded": False
                        }
                    ]
                }
            }
        ],
        "PrimaryCriteria": {
            "CriteriaList": [
                {
                    "ConditionOccurrence": {
                        "CodesetId": 0
                    }
                }
            ],
            "ObservationWindow": {
                "PriorDays": 0,
                "PostDays": 0
            },
            "PrimaryCriteriaLimit": {
                "Type": "First"
            }
        },
        "QualifiedLimit": {
            "Type": "First"
        },
        "ExpressionLimit": {
            "Type": "First"
        },
        "InclusionRules": [],
        "CensoringCriteria": []
    }

    try:
        # Validate the cohort definition
        cohort = CohortExpression.model_validate(cohort_json)
        print("✅ Valid cohort definition!")
        print(f"   - Concept sets: {len(cohort.concept_sets)}")
        print(f"   - Primary criteria: {len(cohort.primary_criteria.criteria_list)}")
        print(f"   - Inclusion rules: {len(cohort.inclusion_rules)}")

        # Access typed data
        diabetes_cs = cohort.concept_sets[0]
        print(f"   - First concept set: '{diabetes_cs.name}' with {len(diabetes_cs.expression.items)} concepts")

    except ValidationError as e:
        print("❌ Validation errors:")
        for error in e.errors():
            print(f"  - {error['loc']}: {error['msg']}")

    # Example of invalid cohort
    print("\n" + "="*50)
    print("Testing invalid cohort...")

    invalid_cohort_json = {
        "ConceptSets": [],  # Missing required concept set
        "PrimaryCriteria": {
            "CriteriaList": [
                {
                    "ConditionOccurrence": {
                        "CodesetId": 0  # References non-existent concept set
                    }
                }
            ],
            "ObservationWindow": {
                "PriorDays": 0,
                "PostDays": 0
            },
            "PrimaryCriteriaLimit": {
                "Type": "InvalidType"  # Invalid limit type
            }
        }
    }

    try:
        CohortExpression.model_validate(invalid_cohort_json)
        print("❌ This should have failed validation!")
    except ValidationError as e:
        print("✅ Correctly caught validation errors:")
        for error in e.errors():
            print(f"  - {'.'.join(str(x) for x in error['loc'])}: {error['msg']}")


if __name__ == "__main__":
    main()
