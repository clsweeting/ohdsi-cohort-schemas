"""Common types and utilities used across OHDSI cohort schemas."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Concept(BaseModel):
    """Represents an OMOP concept from a standardized vocabulary."""

    model_config = ConfigDict(populate_by_name=True)

    concept_id: int = Field(..., alias="CONCEPT_ID", description="Unique identifier for the concept")
    concept_name: str = Field(..., alias="CONCEPT_NAME", description="Human-readable name of the concept")
    standard_concept: str | None = Field(None, alias="STANDARD_CONCEPT", description="Standard concept flag ('S', 'C', or None)")
    concept_code: str = Field(..., alias="CONCEPT_CODE", description="Concept code from the source vocabulary")
    concept_class_id: str | None = Field(None, alias="CONCEPT_CLASS_ID", description="Concept class identifier")
    vocabulary_id: str = Field(..., alias="VOCABULARY_ID", description="Vocabulary identifier (e.g., 'SNOMED', 'ICD10CM')")
    domain_id: str = Field(..., alias="DOMAIN_ID", description="Domain identifier (e.g., 'Condition', 'Drug')")
    invalid_reason: str | None = Field(None, alias="INVALID_REASON", description="Reason why concept is invalid")
    invalid_reason_caption: str | None = Field(None, alias="INVALID_REASON_CAPTION", description="Human-readable invalid reason")
    standard_concept_caption: str | None = Field(
        None, alias="STANDARD_CONCEPT_CAPTION", description="Human-readable standard concept status"
    )


class DateRange(BaseModel):
    """Represents a date range with optional start and end dates."""

    value: str | None = Field(None, description="Start date (YYYY-MM-DD)")
    extent: str | None = Field(None, description="End date (YYYY-MM-DD)")


class NumericRange(BaseModel):
    """Represents a numeric range with optional start and end values."""

    value: float | None = Field(None, description="Start value")
    extent: float | None = Field(None, description="End value")


class TextCriteria(BaseModel):
    """Represents text search criteria."""

    text: str | None = Field(None, description="Text to search for")
    op: Literal["startsWith", "contains", "endsWith", "exact"] = Field("contains", description="Text matching operation")


class Window(BaseModel):
    """Represents a time window with start and end bounds."""

    start: WindowBound | None = Field(None, alias="Start", description="Window start bound")
    end: WindowBound | None = Field(None, alias="End", description="Window end bound")
    use_event_end: bool = Field(False, alias="UseEventEnd", description="Use event end date")


class WindowBound(BaseModel):
    """Represents a bound of a time window."""

    coeff: int = Field(..., alias="Coeff", description="Direction coefficient (-1 for before, 1 for after)")
    days: int | None = Field(None, alias="Days", description="Number of days offset")
    date_field: str | None = Field(None, alias="DateField", description="Date field to use as reference")


class Occurrence(BaseModel):
    """Represents occurrence count criteria."""

    type: Literal[0, 1, 2] = Field(..., alias="Type", description="Occurrence type (0=exactly, 1=at most, 2=at least)")
    count: int = Field(..., alias="Count", description="Number of occurrences")
    is_distinct: bool | None = Field(None, alias="IsDistinct", description="Count distinct occurrences only")


class Limit(BaseModel):
    """Represents cohort size limiting strategy."""

    model_config = ConfigDict(populate_by_name=True)

    type: Literal["First", "Last", "All"] = Field(..., alias="Type", description="Limiting strategy")


class ObservationWindow(BaseModel):
    """Represents observation window around index event."""

    model_config = ConfigDict(populate_by_name=True)

    prior_days: int = Field(0, alias="PriorDays", description="Days before index event")
    post_days: int = Field(0, alias="PostDays", description="Days after index event")


class CollapseSettings(BaseModel):
    """Settings for collapsing multiple events into eras."""

    collapse_type: Literal["ERA", "NONE"] = Field("NONE", alias="CollapseType", description="Collapse strategy")
    era_pad: int = Field(0, alias="EraPad", description="Days to pad between events when creating eras")


class CensorWindow(BaseModel):
    """Represents censoring window settings."""

    start_date: str | None = Field(None, alias="StartDate", description="Censor window start date")
    end_date: str | None = Field(None, alias="EndDate", description="Censor window end date")


# Forward references
Window.model_rebuild()
