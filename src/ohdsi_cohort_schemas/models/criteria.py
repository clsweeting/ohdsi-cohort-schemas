"""Criteria models for different OMOP domains."""

from __future__ import annotations

from pydantic import BaseModel, Field

from .common import (
    Concept,
    DateRange,
    NumericRange,
    Occurrence,
    TextCriteria,
    Window,
)


class CorrelatedCriteria(BaseModel):
    """Represents criteria that must be correlated with the main criteria."""

    type: str = Field(..., alias="Type", description="Logic type (ALL, ANY)")
    criteria_list: list[CriteriaGroup] = Field([], alias="CriteriaList", description="List of criteria")
    demographic_criteria_list: list[DemographicCriteria] = Field([], alias="DemographicCriteriaList")
    groups: list[Group] = Field([], alias="Groups", description="Grouped criteria")


class CriteriaGroup(BaseModel):
    """Wrapper for individual criteria with occurrence and window settings."""

    criteria: AnyCriteria = Field(..., alias="Criteria", description="The actual criteria")
    start_window: Window | None = Field(None, alias="StartWindow", description="Time window relative to index")
    end_window: Window | None = Field(None, alias="EndWindow", description="End time window")
    restrict_visit: bool | None = Field(None, alias="RestrictVisit", description="Restrict to same visit")
    ignore_observation_period: bool | None = Field(None, alias="IgnoreObservationPeriod")
    occurrence: Occurrence | None = Field(None, alias="Occurrence", description="Occurrence count requirements")


class DemographicCriteria(BaseModel):
    """Demographic filtering criteria."""

    age: NumericRange | None = Field(None, alias="Age", description="Age range")
    gender: list[Concept] | None = Field(None, alias="Gender", description="Gender concepts")
    race: list[Concept] | None = Field(None, alias="Race", description="Race concepts")
    ethnicity: list[Concept] | None = Field(None, alias="Ethnicity", description="Ethnicity concepts")
    occurrence_start_date: DateRange | None = Field(None, alias="OccurrenceStartDate")
    occurrence_end_date: DateRange | None = Field(None, alias="OccurrenceEndDate")


class Group(BaseModel):
    """Represents grouped criteria with logic operators."""

    type: str = Field(..., alias="Type", description="Group logic type")
    criteria_list: list[CriteriaGroup] = Field([], alias="CriteriaList")
    demographic_criteria_list: list[DemographicCriteria] = Field([], alias="DemographicCriteriaList")
    groups: list[Group] = Field([], alias="Groups")


# Base criteria class
class BaseCriteria(BaseModel):
    """Base class for all domain-specific criteria."""

    correlated_criteria: CorrelatedCriteria | None = Field(None, alias="CorrelatedCriteria")
    first: bool | None = Field(None, alias="First", description="Use first occurrence only")
    age: NumericRange | None = Field(None, alias="Age", description="Age at event")
    gender: list[Concept] | None = Field(None, alias="Gender", description="Gender restriction")
    provider_specialty: list[Concept] | None = Field(None, alias="ProviderSpecialty")
    visit_type: list[Concept] | None = Field(None, alias="VisitType", description="Visit type restriction")


class ConditionOccurrence(BaseCriteria):
    """Criteria for condition occurrence events."""

    codeset_id: int | None = Field(None, alias="CodesetId", description="Reference to concept set")
    occurrence_start_date: DateRange | None = Field(None, alias="OccurrenceStartDate")
    occurrence_end_date: DateRange | None = Field(None, alias="OccurrenceEndDate")
    condition_type: list[Concept] | None = Field(None, alias="ConditionType")
    stop_reason: TextCriteria | None = Field(None, alias="StopReason")
    condition_source_concept: int | None = Field(None, alias="ConditionSourceConcept")


class DrugExposure(BaseCriteria):
    """Criteria for drug exposure events."""

    codeset_id: int | None = Field(None, alias="CodesetId")
    occurrence_start_date: DateRange | None = Field(None, alias="OccurrenceStartDate")
    occurrence_end_date: DateRange | None = Field(None, alias="OccurrenceEndDate")
    drug_type: list[Concept] | None = Field(None, alias="DrugType")
    stop_reason: TextCriteria | None = Field(None, alias="StopReason")
    refills: NumericRange | None = Field(None, alias="Refills")
    quantity: NumericRange | None = Field(None, alias="Quantity")
    days_supply: NumericRange | None = Field(None, alias="DaysSupply")
    route_concept: list[Concept] | None = Field(None, alias="RouteConcept")
    effective_drug_dose: NumericRange | None = Field(None, alias="EffectiveDrugDose")
    dose_unit: list[Concept] | None = Field(None, alias="DoseUnit")
    lot_number: TextCriteria | None = Field(None, alias="LotNumber")
    drug_source_concept: int | None = Field(None, alias="DrugSourceConcept")


class DrugEra(BaseCriteria):
    """Criteria for drug era events (continuous drug exposure periods)."""

    codeset_id: int | None = Field(None, alias="CodesetId")
    era_start_date: DateRange | None = Field(None, alias="EraStartDate")
    era_end_date: DateRange | None = Field(None, alias="EraEndDate")
    occurrence_count: NumericRange | None = Field(None, alias="OccurrenceCount")
    era_length: NumericRange | None = Field(None, alias="EraLength")
    age_at_start: NumericRange | None = Field(None, alias="AgeAtStart")
    age_at_end: NumericRange | None = Field(None, alias="AgeAtEnd")


class ProcedureOccurrence(BaseCriteria):
    """Criteria for procedure occurrence events."""

    codeset_id: int | None = Field(None, alias="CodesetId")
    occurrence_start_date: DateRange | None = Field(None, alias="OccurrenceStartDate")
    procedure_type: list[Concept] | None = Field(None, alias="ProcedureType")
    modifier: list[Concept] | None = Field(None, alias="Modifier")
    quantity: NumericRange | None = Field(None, alias="Quantity")


class Measurement(BaseCriteria):
    """Criteria for measurement events (lab values, vital signs)."""

    codeset_id: int | None = Field(None, alias="CodesetId")
    occurrence_start_date: DateRange | None = Field(None, alias="OccurrenceStartDate")
    measurement_type: list[Concept] | None = Field(None, alias="MeasurementType")
    operator: list[Concept] | None = Field(None, alias="Operator")
    value_as_number: NumericRange | None = Field(None, alias="ValueAsNumber")
    value_as_concept: list[Concept] | None = Field(None, alias="ValueAsConcept")
    unit: list[Concept] | None = Field(None, alias="Unit")
    range_low: NumericRange | None = Field(None, alias="RangeLow")
    range_high: NumericRange | None = Field(None, alias="RangeHigh")
    measurement_source_concept: int | None = Field(None, alias="MeasurementSourceConcept")
    range_low_ratio: NumericRange | None = Field(None, alias="RangeLowRatio")
    range_high_ratio: NumericRange | None = Field(None, alias="RangeHighRatio")
    abnormal: bool | None = Field(None, alias="Abnormal")


class Observation(BaseCriteria):
    """Criteria for observation events."""

    codeset_id: int | None = Field(None, alias="CodesetId")
    occurrence_start_date: DateRange | None = Field(None, alias="OccurrenceStartDate")
    observation_type: list[Concept] | None = Field(None, alias="ObservationType")
    value_as_number: NumericRange | None = Field(None, alias="ValueAsNumber")
    value_as_string: TextCriteria | None = Field(None, alias="ValueAsString")
    value_as_concept: list[Concept] | None = Field(None, alias="ValueAsConcept")
    qualifier: list[Concept] | None = Field(None, alias="Qualifier")
    unit: list[Concept] | None = Field(None, alias="Unit")
    observation_source_concept: int | None = Field(None, alias="ObservationSourceConcept")


class DeviceExposure(BaseCriteria):
    """Criteria for device exposure events."""

    codeset_id: int | None = Field(None, alias="CodesetId")
    occurrence_start_date: DateRange | None = Field(None, alias="OccurrenceStartDate")
    occurrence_end_date: DateRange | None = Field(None, alias="OccurrenceEndDate")
    device_type: list[Concept] | None = Field(None, alias="DeviceType")
    unique_device_id: TextCriteria | None = Field(None, alias="UniqueDeviceId")
    quantity: NumericRange | None = Field(None, alias="Quantity")
    device_source_concept: int | None = Field(None, alias="DeviceSourceConcept")


class Death(BaseCriteria):
    """Criteria for death events."""

    codeset_id: int | None = Field(None, alias="CodesetId")
    occurrence_start_date: DateRange | None = Field(None, alias="OccurrenceStartDate")
    death_type: list[Concept] | None = Field(None, alias="DeathType")


class VisitOccurrence(BaseCriteria):
    """Criteria for visit occurrence events."""

    codeset_id: int | None = Field(None, alias="CodesetId")
    occurrence_start_date: DateRange | None = Field(None, alias="OccurrenceStartDate")
    occurrence_end_date: DateRange | None = Field(None, alias="OccurrenceEndDate")
    visit_type: list[Concept] | None = Field(None, alias="VisitType")
    visit_source_concept: int | None = Field(None, alias="VisitSourceConcept")
    visit_length: NumericRange | None = Field(None, alias="VisitLength")


class VisitDetail(BaseCriteria):
    """Criteria for visit detail events."""

    codeset_id: int | None = Field(None, alias="CodesetId")
    occurrence_start_date: DateRange | None = Field(None, alias="OccurrenceStartDate")
    occurrence_end_date: DateRange | None = Field(None, alias="OccurrenceEndDate")
    visit_detail_type: list[Concept] | None = Field(None, alias="VisitDetailType")
    visit_detail_source_concept: int | None = Field(None, alias="VisitDetailSourceConcept")


class ObservationPeriod(BaseCriteria):
    """Criteria for observation period events."""

    period_start_date: DateRange | None = Field(None, alias="PeriodStartDate")
    period_end_date: DateRange | None = Field(None, alias="PeriodEndDate")
    period_type: list[Concept] | None = Field(None, alias="PeriodType")
    user_defined_period: DateRange | None = Field(None, alias="UserDefinedPeriod")
    age_at_start: NumericRange | None = Field(None, alias="AgeAtStart")
    age_at_end: NumericRange | None = Field(None, alias="AgeAtEnd")
    period_length: NumericRange | None = Field(None, alias="PeriodLength")


class Specimen(BaseCriteria):
    """Criteria for specimen events."""

    codeset_id: int | None = Field(None, alias="CodesetId")
    occurrence_start_date: DateRange | None = Field(None, alias="OccurrenceStartDate")
    specimen_type: list[Concept] | None = Field(None, alias="SpecimenType")
    quantity: NumericRange | None = Field(None, alias="Quantity")
    unit: list[Concept] | None = Field(None, alias="Unit")
    anatomic_site: list[Concept] | None = Field(None, alias="AnatomicSite")
    disease_status: list[Concept] | None = Field(None, alias="DiseaseStatus")
    source_id: TextCriteria | None = Field(None, alias="SourceId")


# Union type for any criteria
AnyCriteria = (
    ConditionOccurrence
    | DrugExposure
    | DrugEra
    | ProcedureOccurrence
    | Measurement
    | Observation
    | DeviceExposure
    | Death
    | VisitOccurrence
    | VisitDetail
    | ObservationPeriod
    | Specimen
)


class PrimaryCriteriaItem(BaseModel):
    """Direct criteria item for primary criteria (no Criteria wrapper)."""

    condition_occurrence: ConditionOccurrence | None = Field(None, alias="ConditionOccurrence")
    drug_exposure: DrugExposure | None = Field(None, alias="DrugExposure")
    drug_era: DrugEra | None = Field(None, alias="DrugEra")
    procedure_occurrence: ProcedureOccurrence | None = Field(None, alias="ProcedureOccurrence")
    measurement: Measurement | None = Field(None, alias="Measurement")
    observation: Observation | None = Field(None, alias="Observation")
    device_exposure: DeviceExposure | None = Field(None, alias="DeviceExposure")
    death: Death | None = Field(None, alias="Death")
    visit_occurrence: VisitOccurrence | None = Field(None, alias="VisitOccurrence")
    visit_detail: VisitDetail | None = Field(None, alias="VisitDetail")
    observation_period: ObservationPeriod | None = Field(None, alias="ObservationPeriod")
    specimen: Specimen | None = Field(None, alias="Specimen")


# Update forward references
CorrelatedCriteria.model_rebuild()
CriteriaGroup.model_rebuild()
Group.model_rebuild()
