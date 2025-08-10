"""Concept set models for OHDSI cohort definitions."""


from pydantic import BaseModel, Field

from .common import Concept


class ConceptSetItem(BaseModel):
    """Represents a single concept within a concept set."""

    concept: Concept = Field(..., description="The OMOP concept")
    include_descendants: bool = Field(True, alias="includeDescendants", description="Include descendant concepts")
    include_mapped: bool = Field(False, alias="includeMapped", description="Include mapped concepts")
    is_excluded: bool = Field(False, alias="isExcluded", description="Exclude this concept from the set")


class ConceptSetExpression(BaseModel):
    """Represents the expression defining which concepts are in a concept set."""

    items: list[ConceptSetItem] = Field(..., description="List of concepts in this set")


class ConceptSet(BaseModel):
    """Represents a reusable group of medical concepts."""

    id: int = Field(..., description="Unique identifier for this concept set within the cohort")
    name: str = Field(..., description="Human-readable name for this concept set")
    expression: ConceptSetExpression = Field(..., description="Definition of which concepts are included")
