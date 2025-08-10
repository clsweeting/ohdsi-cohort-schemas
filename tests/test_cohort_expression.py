"""Test basic cohort expression validation."""

import pytest
from ohdsi_cohort_schemas.models.cohort import CohortExpression
from pydantic import ValidationError


def test_minimal_cohort_expression():
    """Test creating a minimal valid cohort expression."""
    data = {
        "ConceptSets": [],
        "PrimaryCriteria": {
            "CriteriaList": [
                {
                    "ConditionOccurrence": {}
                }
            ],
            "ObservationWindow": {
                "PriorDays": 0,
                "PostDays": 0
            },
            "PrimaryCriteriaLimit": {
                "Type": "First"
            }
        }
    }

    cohort = CohortExpression.model_validate(data)

    assert len(cohort.concept_sets) == 0
    assert len(cohort.primary_criteria.criteria_list) == 1
    assert cohort.primary_criteria.observation_window.prior_days == 0
    assert cohort.primary_criteria.primary_criteria_limit.type == "First"


def test_cohort_with_concept_sets():
    """Test cohort expression with concept sets."""
    data = {
        "ConceptSets": [
            {
                "id": 0,
                "name": "Test Concept Set",
                "expression": {
                    "items": [
                        {
                            "concept": {
                                "CONCEPT_ID": 123,
                                "CONCEPT_NAME": "Test Concept",
                                "CONCEPT_CODE": "TEST",
                                "CONCEPT_CLASS_ID": "Test",
                                "VOCABULARY_ID": "Test",
                                "DOMAIN_ID": "Test"
                            },
                            "include_descendants": True,
                            "include_mapped": False,
                            "is_excluded": False
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
        }
    }

    cohort = CohortExpression.model_validate(data)

    assert len(cohort.concept_sets) == 1
    assert cohort.concept_sets[0].name == "Test Concept Set"
    assert len(cohort.concept_sets[0].expression.items) == 1


def test_invalid_cohort_missing_required():
    """Test that validation fails for missing required fields."""
    data = {
        "ConceptSets": []
        # Missing PrimaryCriteria - should fail
    }

    with pytest.raises(ValidationError) as exc_info:
        CohortExpression.model_validate(data)

    errors = exc_info.value.errors()
    assert len(errors) > 0
    assert any("PrimaryCriteria" in str(error["loc"]) for error in errors)


def test_invalid_limit_type():
    """Test validation fails for invalid limit type."""
    data = {
        "ConceptSets": [],
        "PrimaryCriteria": {
            "CriteriaList": [
                {
                    "ConditionOccurrence": {}
                }
            ],
            "ObservationWindow": {
                "PriorDays": 0,
                "PostDays": 0
            },
            "PrimaryCriteriaLimit": {
                "Type": "InvalidType"  # Should fail
            }
        }
    }

    with pytest.raises(ValidationError) as exc_info:
        CohortExpression.model_validate(data)

    errors = exc_info.value.errors()
    assert len(errors) > 0
