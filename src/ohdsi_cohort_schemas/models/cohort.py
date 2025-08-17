"""Main cohort expression model."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from .common import (
    CensorWindow,
    CollapseSettings,
    Limit,
    ObservationWindow,
)
from .concept_set import ConceptSet
from .criteria import CriteriaGroup, DemographicCriteria, Group, PrimaryCriteriaItem


class InclusionRule(BaseModel):
    """Represents an inclusion rule for additional cohort filtering."""

    name: str = Field(..., description="Name of the inclusion rule")
    description: str | None = Field(None, description="Detailed description of the rule")
    expression: CriteriaExpression | None = Field(None, description="The criteria expression")


class CriteriaExpression(BaseModel):
    """Represents a logical expression of criteria."""

    type: str = Field(..., alias="Type", description="Logic type (ALL, ANY)")
    criteria_list: list[CriteriaGroup] = Field([], alias="CriteriaList", description="List of criteria")
    demographic_criteria_list: list[DemographicCriteria] = Field([], alias="DemographicCriteriaList")
    groups: list[Group] = Field([], alias="Groups", description="Grouped criteria")


class PrimaryCriteria(BaseModel):
    """Represents the primary criteria that define the index event."""

    model_config = ConfigDict(populate_by_name=True)

    criteria_list: list[PrimaryCriteriaItem] = Field(..., alias="CriteriaList", description="Primary qualifying criteria")
    observation_window: ObservationWindow = Field(..., alias="ObservationWindow", description="Observation window around index")
    primary_criteria_limit: Limit = Field(..., alias="PrimaryCriteriaLimit", description="How to select among multiple events")


class DateOffsetStrategy(BaseModel):
    """Date offset strategy configuration."""

    date_field: str = Field(..., alias="DateField", description="Which date field to use")
    offset: int = Field(..., alias="Offset", description="Number of days offset")


class EndStrategy(BaseModel):
    """Defines how cohort periods end."""

    type: str | None = Field(None, alias="Type", description="End strategy type")
    days_offset: int | None = Field(None, alias="DaysOffset", description="Days offset for fixed strategies")
    date_offset: DateOffsetStrategy | None = Field(None, alias="DateOffset", description="Date offset strategy")


class CensoringCriteria(BaseModel):
    """Represents criteria for censoring observation periods."""

    # This would be defined based on the actual Circe schema
    pass


class CohortExpression(BaseModel):
    """
    Represents a complete OHDSI/Circe cohort expression.

    This is the root model that contains all components needed to define
    a cohort: concept sets, primary criteria, inclusion rules, etc.
    """

    concept_sets: list[ConceptSet] = Field(..., alias="ConceptSets", description="Reusable concept definitions")
    primary_criteria: PrimaryCriteria = Field(..., alias="PrimaryCriteria", description="Index event definition")
    qualified_limit: Limit | None = Field(None, alias="QualifiedLimit", description="Limit after primary criteria")
    expression_limit: Limit | None = Field(None, alias="ExpressionLimit", description="Final expression limit")
    inclusion_rules: list[InclusionRule] = Field([], alias="InclusionRules", description="Additional filtering rules")
    end_strategy: EndStrategy | None = Field(None, alias="EndStrategy", description="How cohort periods end")
    censoring_criteria: list[CensoringCriteria] = Field([], alias="CensoringCriteria", description="Censoring rules")
    collapse_settings: CollapseSettings | None = Field(None, alias="CollapseSettings", description="Era collapse settings")
    censor_window: CensorWindow | None = Field(None, alias="CensorWindow", description="Censoring window")

    class Config:
        """Pydantic configuration."""

        validate_by_name = True
        use_enum_values = True


# Update forward references
InclusionRule.model_rebuild()
