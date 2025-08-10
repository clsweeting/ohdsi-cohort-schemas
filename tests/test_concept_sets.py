"""Test concept set models."""

from ohdsi_cohort_schemas.models.concept_set import ConceptSet, ConceptSetExpression, ConceptSetItem
from ohdsi_cohort_schemas.models.vocabulary import Concept


def test_concept_creation():
    """Test creating a basic concept."""
    concept = Concept(
        concept_id=201826,
        concept_name="Type 2 diabetes mellitus",
        standard_concept="S",
        concept_code="44054006",
        concept_class_id="Clinical Finding",
        vocabulary_id="SNOMED",
        domain_id="Condition"
    )

    assert concept.concept_id == 201826
    assert concept.concept_name == "Type 2 diabetes mellitus"
    assert concept.standard_concept == "S"


def test_concept_set_item_creation():
    """Test creating a concept set item."""
    concept = Concept(
        concept_id=201826,
        concept_name="Type 2 diabetes mellitus",
        standard_concept="S",
        concept_code="44054006",
        concept_class_id="Clinical Finding",
        vocabulary_id="SNOMED",
        domain_id="Condition"
    )

    item = ConceptSetItem(
        concept=concept,
        include_descendants=True,
        include_mapped=False,
        is_excluded=False
    )

    assert item.concept.concept_id == 201826
    assert item.include_descendants is True
    assert item.include_mapped is False
    assert item.is_excluded is False


def test_concept_set_creation():
    """Test creating a complete concept set."""
    concept = Concept(
        concept_id=201826,
        concept_name="Type 2 diabetes mellitus",
        standard_concept="S",
        concept_code="44054006",
        concept_class_id="Clinical Finding",
        vocabulary_id="SNOMED",
        domain_id="Condition"
    )

    item = ConceptSetItem(
        concept=concept,
        include_descendants=True,
        include_mapped=False,
        is_excluded=False
    )

    expression = ConceptSetExpression(items=[item])

    concept_set = ConceptSet(
        id=0,
        name="Type 2 Diabetes",
        expression=expression
    )

    assert concept_set.id == 0
    assert concept_set.name == "Type 2 Diabetes"
    assert len(concept_set.expression.items) == 1
    assert concept_set.expression.items[0].concept.concept_id == 201826


def test_concept_set_from_dict():
    """Test creating concept set from dictionary (JSON-like data)."""
    data = {
        "id": 0,
        "name": "Type 2 Diabetes",
        "expression": {
            "items": [
                {
                    "concept": {
                        "concept_id": 201826,
                        "concept_name": "Type 2 diabetes mellitus",
                        "standard_concept": "S",
                        "concept_code": "44054006",
                        "concept_class_id": "Clinical Finding",
                        "vocabulary_id": "SNOMED",
                        "domain_id": "Condition"
                    },
                    "include_descendants": True,
                    "include_mapped": False,
                    "is_excluded": False
                }
            ]
        }
    }

    concept_set = ConceptSet.model_validate(data)

    assert concept_set.id == 0
    assert concept_set.name == "Type 2 Diabetes"
    assert len(concept_set.expression.items) == 1
    assert concept_set.expression.items[0].concept.concept_id == 201826


def test_concept_set_with_aliases():
    """Test that Circe JSON aliases work correctly."""
    data = {
        "id": 0,
        "name": "Type 2 Diabetes",
        "expression": {
            "items": [
                {
                    "concept": {
                        "CONCEPT_ID": 201826,  # Alias
                        "CONCEPT_NAME": "Type 2 diabetes mellitus",  # Alias
                        "CONCEPT_CODE": "44054006",  # Alias
                        "CONCEPT_CLASS_ID": "Clinical Finding",  # Alias
                        "VOCABULARY_ID": "SNOMED",  # Alias
                        "DOMAIN_ID": "Condition",  # Alias
                        "STANDARD_CONCEPT": "S"  # Alias
                    },
                    "includeDescendants": True,  # Alias
                    "includeMapped": False,      # Alias
                    "isExcluded": False          # Alias
                }
            ]
        }
    }

    concept_set = ConceptSet.model_validate(data)

    assert concept_set.id == 0
    assert concept_set.expression.items[0].concept.concept_id == 201826
    assert concept_set.expression.items[0].include_descendants is True
