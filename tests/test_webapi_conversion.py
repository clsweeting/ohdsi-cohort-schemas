"""
Test WebAPI format conversion and validation functions.
"""

import json
from pathlib import Path

import pytest
from ohdsi_cohort_schemas import (
    circe_to_webapi_dict,
    validate_schema_only,
    validate_webapi_schema_only,
    validate_webapi_strict,
    validate_webapi_with_warnings,
    webapi_to_circe_dict,
)
from ohdsi_cohort_schemas.validation import CIRCE_TO_WEBAPI_FIELD_MAP, WEBAPI_TO_CIRCE_FIELD_MAP


def test_field_mapping_coverage():
    """Test that field mappings are bidirectional."""
    # Check that every WebAPI field maps to a Circe field
    for webapi_field, circe_field in WEBAPI_TO_CIRCE_FIELD_MAP.items():
        assert webapi_field and circe_field, f"Empty field mapping: {webapi_field} -> {circe_field}"

    # Check that every Circe field maps back to a WebAPI field
    for circe_field, webapi_field in CIRCE_TO_WEBAPI_FIELD_MAP.items():
        assert circe_field and webapi_field, f"Empty reverse mapping: {circe_field} -> {webapi_field}"


def test_key_mapping_examples():
    """Test specific key mappings."""
    test_cases = [
        ("conceptSets", "ConceptSets"),
        ("primaryCriteria", "PrimaryCriteria"),
        ("conceptId", "CONCEPT_ID"),
        ("conceptName", "CONCEPT_NAME"),
        ("includeDescendants", "includeDescendants"),  # stays same
        ("id", "id"),  # stays same
        ("codesetId", "CodesetId"),
        ("drugCodesetId", "DrugCodesetId"),
    ]

    for webapi, expected_circe in test_cases:
        result = WEBAPI_TO_CIRCE_FIELD_MAP.get(webapi, webapi)
        assert result == expected_circe, f"WebAPI->Circe: {webapi} -> {result} (expected: {expected_circe})"

        reverse = CIRCE_TO_WEBAPI_FIELD_MAP.get(expected_circe, expected_circe)
        assert reverse == webapi, f"Circe->WebAPI: {expected_circe} -> {reverse} (expected: {webapi})"


def test_dict_conversion_simple():
    """Test dictionary conversion with simple data."""
    webapi_data = {
        "conceptSets": [
            {
                "id": 1,
                "name": "Test Concept Set",
                "expression": {
                    "items": [
                        {
                            "concept": {
                                "conceptId": 123,
                                "conceptName": "Test Concept",
                                "standardConcept": "S",
                                "invalidReason": "V",
                                "conceptCode": "TEST",
                                "domainId": "Condition",
                                "vocabularyId": "SNOMED",
                                "conceptClassId": "Clinical Finding",
                            },
                            "includeDescendants": True,
                            "isExcluded": False,
                            "includeMapped": False,
                        }
                    ]
                },
            }
        ],
        "primaryCriteria": {
            "criteriaList": [{"conditionOccurrence": {"codesetId": 1}}],
            "observationWindow": {"priorDays": 0, "postDays": 0},
            "primaryCriteriaLimit": {"type": "First"},
        },
        "qualifiedLimit": {"type": "First"},
        "expressionLimit": {"type": "First"},
        "inclusionRules": [],
        "censoringCriteria": [],
    }

    # Convert to Circe format
    circe_data = webapi_to_circe_dict(webapi_data)

    # Check key transformations
    assert "ConceptSets" in circe_data
    assert "PrimaryCriteria" in circe_data
    assert circe_data["ConceptSets"][0]["expression"]["items"][0]["concept"]["CONCEPT_ID"] == 123
    assert circe_data["ConceptSets"][0]["expression"]["items"][0]["concept"]["CONCEPT_NAME"] == "Test Concept"
    assert circe_data["PrimaryCriteria"]["CriteriaList"][0]["ConditionOccurrence"]["CodesetId"] == 1

    # Convert back to WebAPI format
    webapi_back = circe_to_webapi_dict(circe_data)

    # Check round-trip conversion
    assert webapi_back["conceptSets"][0]["id"] == webapi_data["conceptSets"][0]["id"]
    assert webapi_back["conceptSets"][0]["expression"]["items"][0]["concept"]["conceptId"] == 123
    assert webapi_back["primaryCriteria"]["criteriaList"][0]["conditionOccurrence"]["codesetId"] == 1


def test_webapi_validation_functions():
    """Test WebAPI validation functions."""
    webapi_data = {
        "conceptSets": [
            {
                "id": 1,
                "name": "Test Concept Set",
                "expression": {
                    "items": [
                        {
                            "concept": {
                                "conceptId": 123,
                                "conceptName": "Test Concept",
                                "standardConcept": "S",
                                "invalidReason": "V",
                                "conceptCode": "TEST",
                                "domainId": "Condition",
                                "vocabularyId": "SNOMED",
                                "conceptClassId": "Clinical Finding",
                            },
                            "includeDescendants": True,
                        }
                    ]
                },
            }
        ],
        "primaryCriteria": {
            "criteriaList": [{"conditionOccurrence": {"codesetId": 1}}],
            "observationWindow": {"priorDays": 0, "postDays": 0},
            "primaryCriteriaLimit": {"type": "First"},
        },
        "qualifiedLimit": {"type": "First"},
        "expressionLimit": {"type": "First"},
        "inclusionRules": [],
        "censoringCriteria": [],
    }

    # Test schema-only validation
    cohort = validate_webapi_schema_only(webapi_data)
    assert cohort is not None
    assert len(cohort.concept_sets) == 1
    assert cohort.concept_sets[0].id == 1

    # Test validation with warnings
    cohort, warnings = validate_webapi_with_warnings(webapi_data)
    assert cohort is not None
    # There should be no warnings for this simple valid cohort
    assert len(warnings) == 0

    # Test strict validation
    cohort = validate_webapi_strict(webapi_data)
    assert cohort is not None


def test_real_circe_file_conversion():
    """Test conversion with a real Circe JSON file."""
    circe_file = Path(__file__).parent / "resources" / "checkers" / "eventsProgressionCheckCorrect.json"

    if not circe_file.exists():
        pytest.skip("Test file not found")

    with open(circe_file) as f:
        circe_data = json.load(f)

    # Validate original Circe format
    cohort_circe = validate_schema_only(circe_data)
    assert cohort_circe is not None

    # Convert to WebAPI format
    webapi_data = circe_to_webapi_dict(circe_data)

    # Validate WebAPI format
    cohort_webapi = validate_webapi_schema_only(webapi_data)
    assert cohort_webapi is not None

    # Convert back to Circe format
    circe_back = webapi_to_circe_dict(webapi_data)

    # Validate round-trip
    cohort_roundtrip = validate_schema_only(circe_back)
    assert cohort_roundtrip is not None

    # Check data integrity
    assert len(circe_data.get("ConceptSets", [])) == len(circe_back.get("ConceptSets", []))
    if circe_data.get("ConceptSets"):
        assert circe_data["ConceptSets"][0]["id"] == circe_back["ConceptSets"][0]["id"]


def test_unknown_fields_preserved():
    """Test that unknown fields are preserved during conversion."""
    webapi_data = {
        "conceptSets": [],
        "primaryCriteria": {
            "criteriaList": [],
            "observationWindow": {"priorDays": 0, "postDays": 0},
            "primaryCriteriaLimit": {"type": "First"},
        },
        "qualifiedLimit": {"type": "First"},
        "expressionLimit": {"type": "First"},
        "inclusionRules": [],
        "censoringCriteria": [],
        "unknownField": "should be preserved",
        "nestedUnknown": {"someField": "also preserved", "deepNested": {"evenDeeper": "still here"}},
    }

    # Convert to Circe format
    circe_data = webapi_to_circe_dict(webapi_data)

    # Unknown fields should be preserved
    assert circe_data["unknownField"] == "should be preserved"
    assert circe_data["nestedUnknown"]["someField"] == "also preserved"
    assert circe_data["nestedUnknown"]["deepNested"]["evenDeeper"] == "still here"

    # Convert back
    webapi_back = circe_to_webapi_dict(circe_data)

    # Unknown fields should still be there
    assert webapi_back["unknownField"] == "should be preserved"
    assert webapi_back["nestedUnknown"]["someField"] == "also preserved"
    assert webapi_back["nestedUnknown"]["deepNested"]["evenDeeper"] == "still here"
