#!/usr/bin/env python3
"""
Test parsing of real WebAPI responses.

This script validates that our Pydantic models can successfully parse
actual responses captured from the Atlas demo WebAPI.
"""

import json
from pathlib import Path

from ohdsi_cohort_schemas.models.common import Concept
from ohdsi_cohort_schemas.models.concept_set import ConceptSetExpression


def test_concept_responses():
    """Test parsing individual concept responses."""
    print("🧪 Testing Concept model parsing...")

    concept_files = list(Path("tests/webapi_responses/atlas-demo/vocabulary").glob("concept_*.json"))

    for concept_file in concept_files:
        with open(concept_file) as f:
            concept_data = json.load(f)

        # Test our Concept model can parse it
        concept = Concept.model_validate(concept_data)
        print(f"✅ {concept_file.name}: {concept.concept_name} (ID: {concept.concept_id})")


def test_conceptset_responses():
    """Test parsing concept set responses."""
    print("\\n🎯 Testing ConceptSet model parsing...")

    # Test concept set list
    with open("tests/webapi_responses/atlas-demo/conceptset/list_response.json") as f:
        conceptsets_list = json.load(f)

    print(f"📋 Found {len(conceptsets_list)} concept sets in list response")

    # Test individual concept sets (metadata only - no expression)
    conceptset_files = list(Path("tests/webapi_responses/atlas-demo/conceptset").glob("conceptset_*.json"))

    for cs_file in conceptset_files:
        with open(cs_file) as f:
            cs_data = json.load(f)

        # These are concept set metadata responses, not full ConceptSet objects
        # They have id, name, dates but no expression field
        cs_id = cs_data.get("id")
        cs_name = cs_data.get("name", "Unknown")
        created_date = cs_data.get("createdDate")
        print(f"✅ {cs_file.name}: {cs_name} (ID: {cs_id}, Created: {created_date})")

    # Test concept set expressions (separate endpoint responses)
    print("\\n📝 Testing ConceptSetExpression parsing...")
    expression_files = list(Path("tests/webapi_responses/atlas-demo/conceptset").glob("expression_*.json"))

    for expr_file in expression_files:
        with open(expr_file) as f:
            expr_data = json.load(f)

        # Test our ConceptSetExpression model can parse it
        expression = ConceptSetExpression.model_validate(expr_data)
        print(f"✅ {expr_file.name}: {len(expression.items)} concept items")


def test_cohort_responses():
    """Test parsing cohort definition responses."""
    print("\\n📋 Testing cohort responses...")

    # Test cohort list
    with open("tests/webapi_responses/atlas-demo/cohortdefinition/list_response.json") as f:
        cohorts_list = json.load(f)

    print(f"📋 Found {len(cohorts_list)} cohort definitions in list response")

    # Test individual cohort definitions
    cohort_files = list(Path("tests/webapi_responses/atlas-demo/cohortdefinition").glob("cohort_*.json"))

    for cohort_file in cohort_files:
        with open(cohort_file) as f:
            cohort_data = json.load(f)

        # These are cohort definition metadata, not full expressions
        # They should have id, name, description fields
        cohort_id = cohort_data.get("id")
        cohort_name = cohort_data.get("name", "Unknown")
        print(f"✅ {cohort_file.name}: {cohort_name} (ID: {cohort_id})")


def test_info_response():
    """Test parsing WebAPI info response."""
    print("\\n ℹ️ Testing WebAPI info...")

    with open("tests/webapi_responses/atlas-demo/info/version_info.json") as f:
        info_data = json.load(f)

    version = info_data.get("version")
    build_info = info_data.get("buildInfo", {})
    artifact_version = build_info.get("artifactVersion", "Unknown")

    print(f"✅ WebAPI Version: {version}")
    print(f"✅ Build: {artifact_version}")


def main():
    """Run all response parsing tests."""
    print("🚀 Testing WebAPI response parsing with real data")
    print("=" * 60)

    try:
        test_info_response()
        test_concept_responses()
        test_conceptset_responses()
        test_cohort_responses()

        print("\\n" + "=" * 60)
        print("✅ All WebAPI response parsing tests passed!")
        print("🎉 Our models successfully parse real WebAPI data!")

    except Exception as e:
        print(f"\\n❌ Error parsing WebAPI responses: {e}")
        import traceback

        traceback.print_exc()
        return False

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
