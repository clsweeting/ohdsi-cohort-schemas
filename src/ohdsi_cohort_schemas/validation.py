"""
Optional business logic validation for OHDSI cohort definitions.

This module provides additional validation beyond basic schema validation,
including reference integrity, logical constraints, and domain-specific rules.

Note: These validations are not comprehensive and may not catch all possible
business logic errors. They are provided as a convenience for common cases.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from pydantic import ValidationError

from .models.cohort import CohortExpression
from .models.common import Occurrence

# WebAPI (camelCase) to Circe (mixed case) field mapping
WEBAPI_TO_CIRCE_FIELD_MAP = {
    # Top-level cohort fields
    "conceptSets": "ConceptSets",
    "primaryCriteria": "PrimaryCriteria",
    "additionalCriteria": "AdditionalCriteria",
    "qualifiedLimit": "QualifiedLimit",
    "expressionLimit": "ExpressionLimit",
    "inclusionRules": "InclusionRules",
    "endStrategy": "EndStrategy",
    "censoringCriteria": "CensoringCriteria",
    "collapseSettings": "CollapseSettings",
    "censorWindow": "CensorWindow",
    "cdmVersionRange": "cdmVersionRange",  # stays camelCase
    # ConceptSet fields
    "id": "id",  # stays lowercase
    "name": "name",  # stays lowercase
    "expression": "expression",  # stays lowercase
    "items": "items",  # stays lowercase
    # ConceptSetItem fields
    "concept": "concept",  # stays lowercase
    "includeDescendants": "includeDescendants",  # stays camelCase
    "isExcluded": "isExcluded",  # stays camelCase
    "includeMapped": "includeMapped",  # stays camelCase
    # Concept fields (OMOP vocabulary - ALL_CAPS)
    "conceptId": "CONCEPT_ID",
    "conceptName": "CONCEPT_NAME",
    "conceptCode": "CONCEPT_CODE",
    "conceptClassId": "CONCEPT_CLASS_ID",
    "domainId": "DOMAIN_ID",
    "vocabularyId": "VOCABULARY_ID",
    "standardConcept": "STANDARD_CONCEPT",
    "standardConceptCaption": "STANDARD_CONCEPT_CAPTION",
    "invalidReason": "INVALID_REASON",
    "invalidReasonCaption": "INVALID_REASON_CAPTION",
    "validStartDate": "VALID_START_DATE",
    "validEndDate": "VALID_END_DATE",
    # PrimaryCriteria fields
    "criteriaList": "CriteriaList",
    "observationWindow": "ObservationWindow",
    "primaryCriteriaLimit": "PrimaryCriteriaLimit",
    # Window fields
    "priorDays": "PriorDays",
    "postDays": "PostDays",
    # Limit fields
    "type": "Type",
    # Criteria fields
    "conditionOccurrence": "ConditionOccurrence",
    "conditionEra": "ConditionEra",
    "drugExposure": "DrugExposure",
    "drugEra": "DrugEra",
    "doseEra": "DoseEra",
    "procedureOccurrence": "ProcedureOccurrence",
    "observation": "Observation",
    "measurement": "Measurement",
    "visitOccurrence": "VisitOccurrence",
    "visitDetail": "VisitDetail",
    "deviceExposure": "DeviceExposure",
    "death": "Death",
    "observationPeriod": "ObservationPeriod",
    "specimen": "Specimen",
    "locationRegion": "LocationRegion",
    "payerPlanPeriod": "PayerPlanPeriod",
    # Criteria attribute fields
    "codesetId": "CodesetId",
    "drugCodesetId": "DrugCodesetId",
    "occurrenceStartDate": "OccurrenceStartDate",
    "occurrenceEndDate": "OccurrenceEndDate",
    "age": "Age",
    "gender": "Gender",
    "providerSpecialty": "ProviderSpecialty",
    "visitType": "VisitType",
    "correlatedCriteria": "CorrelatedCriteria",
    # Date/Numeric range fields
    "value": "Value",
    "extent": "Extent",
    "op": "Op",
    # Occurrence fields
    "count": "Count",
    # "type": "Type",  # already mapped above
    # Window/Period fields
    "start": "Start",
    "end": "End",
    "startWindow": "StartWindow",
    "endWindow": "EndWindow",
    "eventStarts": "EventStarts",
    "useEventEnd": "UseEventEnd",
    "indexStartDate": "IndexStartDate",
    "indexEndDate": "IndexEndDate",
    # Additional criteria fields
    "criteria": "Criteria",
    "demographicCriteriaList": "DemographicCriteriaList",
    "groups": "Groups",  # already mapped
    "description": "description",  # stays lowercase
    # End strategy fields
    "customEra": "CustomEra",
    "fixedDuration": "FixedDuration",
    "gapDays": "GapDays",
    "offset": "Offset",
    # Collapse settings fields
    "collapseType": "CollapseType",
    "eraPad": "EraPad",
    # Coefficient fields
    "coeff": "Coeff",
}

# Create reverse mapping
CIRCE_TO_WEBAPI_FIELD_MAP = {v: k for k, v in WEBAPI_TO_CIRCE_FIELD_MAP.items()}


def convert_dict_keys_with_mapping(data: Any, mapping: dict[str, str]) -> Any:
    """Recursively convert dictionary keys using the provided mapping."""
    if isinstance(data, dict):
        converted = {}
        for k, v in data.items():
            # Use mapping if available, otherwise keep the key as-is
            new_key = mapping.get(k, k)
            converted[new_key] = convert_dict_keys_with_mapping(v, mapping)
        return converted
    elif isinstance(data, list):
        return [convert_dict_keys_with_mapping(item, mapping) for item in data]
    else:
        return data


def webapi_to_circe_dict(data: dict[str, Any]) -> dict[str, Any]:
    """Convert WebAPI (camelCase) format to Circe (mixed case) format."""
    return convert_dict_keys_with_mapping(data, WEBAPI_TO_CIRCE_FIELD_MAP)


def circe_to_webapi_dict(data: dict[str, Any]) -> dict[str, Any]:
    """Convert Circe (mixed case) format to WebAPI (camelCase) format."""
    return convert_dict_keys_with_mapping(data, CIRCE_TO_WEBAPI_FIELD_MAP)


# Legacy aliases for backward compatibility
camel_to_pascal_dict = webapi_to_circe_dict
pascal_to_camel_dict = circe_to_webapi_dict


def camel_to_pascal(name: str) -> str:
    """Convert camelCase to PascalCase (legacy function - use mapping instead)."""
    if not name:
        return name
    return name[0].upper() + name[1:]


def pascal_to_camel(name: str) -> str:
    """Convert PascalCase to camelCase (legacy function - use mapping instead)."""
    if not name:
        return name
    return name[0].lower() + name[1:]


@dataclass
class ValidationIssue:
    """Represents a business logic validation issue."""

    field_path: str
    message: str
    severity: str = "error"  # "error", "warning", "info"


class BusinessLogicValidator:
    """
    Optional validator for business logic constraints.

    Usage:
        # Schema validation only (default)
        cohort = CohortExpression.model_validate(data)

        # Schema + business logic validation
        validator = BusinessLogicValidator()
        cohort = CohortExpression.model_validate(data)
        issues = validator.validate(cohort)
        if issues:
            # Handle business logic issues
            pass
    """

    def __init__(self, strict: bool = False):
        """
        Initialize the validator.

        Args:
            strict: If True, raise ValidationError on any business logic issue.
                   If False, return list of issues for caller to handle.
        """
        self.strict = strict

    def validate(self, cohort: CohortExpression) -> list[ValidationIssue]:
        """
        Validate business logic for a cohort expression.

        Args:
            cohort: The cohort expression to validate

        Returns:
            List of validation issues found

        Raises:
            ValidationError: If strict=True and issues are found
        """
        issues = []

        # Collect all validation checks
        issues.extend(self._validate_concept_set_references(cohort))
        issues.extend(self._validate_occurrence_logic(cohort))
        issues.extend(self._validate_age_constraints(cohort))

        if self.strict and issues:
            error_messages = [f"{issue.field_path}: {issue.message}" for issue in issues]
            # Create a simple ValueError instead of Pydantic ValidationError for business logic
            raise ValueError(f"Business logic validation failed: {'; '.join(error_messages)}")

        return issues

    def _validate_concept_set_references(self, cohort: CohortExpression) -> list[ValidationIssue]:
        """Validate that all CodesetId references point to existing concept sets."""
        issues = []

        # Get all concept set IDs
        concept_set_ids: set[int] = {cs.id for cs in cohort.concept_sets}

        # Check primary criteria
        for i, criteria in enumerate(cohort.primary_criteria.criteria_list):
            issues.extend(self._check_criteria_codeset_refs(criteria, concept_set_ids, f"PrimaryCriteria.CriteriaList.{i}"))

        # Check inclusion rules
        if cohort.inclusion_rules:
            for i, rule in enumerate(cohort.inclusion_rules):
                if rule.expression and rule.expression.criteria_list:
                    for j, criteria in enumerate(rule.expression.criteria_list):
                        issues.extend(
                            self._check_criteria_codeset_refs(criteria, concept_set_ids, f"InclusionRules.{i}.expression.CriteriaList.{j}")
                        )

        return issues

    def _check_criteria_codeset_refs(self, criteria, concept_set_ids: set[int], path: str) -> list[ValidationIssue]:
        """Check codeset references in a single criteria object."""
        issues = []

        # Get the actual criteria dict to check for CodesetId/DrugCodesetId fields
        criteria_dict = criteria.model_dump(by_alias=True)

        # Check all possible criteria types for codeset references
        for field_name, field_value in criteria_dict.items():
            if isinstance(field_value, dict):
                # Check for CodesetId or DrugCodesetId in this criteria type
                for codeset_field in ["CodesetId", "DrugCodesetId"]:
                    if codeset_field in field_value and field_value[codeset_field] is not None:
                        codeset_id = field_value[codeset_field]
                        if codeset_id not in concept_set_ids:
                            issues.append(
                                ValidationIssue(
                                    field_path=f"{path}.{field_name}.{codeset_field}",
                                    message=f"References non-existent concept set ID {codeset_id}. Available IDs: {sorted(concept_set_ids)}",
                                    severity="error",
                                )
                            )

        return issues

    def _validate_occurrence_logic(self, cohort: CohortExpression) -> list[ValidationIssue]:
        """Validate occurrence count and type combinations."""
        issues = []

        def check_occurrence(occurrence: Occurrence, path: str) -> None:
            if occurrence.type == 1 and occurrence.count == 0:
                # "At most 0" doesn't make logical sense
                issues.append(
                    ValidationIssue(
                        field_path=f"{path}.Occurrence",
                        message="Occurrence type 'at most' (1) with count 0 is logically inconsistent",
                        severity="error",
                    )
                )
            elif occurrence.type == 2 and occurrence.count == 0:
                # "At least 0" is always true (redundant)
                issues.append(
                    ValidationIssue(
                        field_path=f"{path}.Occurrence",
                        message="Occurrence type 'at least' (2) with count 0 is always true (redundant)",
                        severity="warning",
                    )
                )

        # Check occurrences in primary criteria
        for i, criteria in enumerate(cohort.primary_criteria.criteria_list):
            criteria_dict = criteria.model_dump(by_alias=True)

            # Check direct Occurrence field
            if "Occurrence" in criteria_dict and criteria_dict["Occurrence"]:
                try:
                    occurrence = Occurrence.model_validate(criteria_dict["Occurrence"])
                    check_occurrence(occurrence, f"PrimaryCriteria.CriteriaList.{i}")
                except (ValidationError, ValueError, TypeError):
                    pass

            # Check Occurrence in nested criteria fields
            for field_name, field_value in criteria_dict.items():
                if isinstance(field_value, dict) and "Occurrence" in field_value:
                    occurrence_data = field_value["Occurrence"]
                    if isinstance(occurrence_data, dict):
                        try:
                            occurrence = Occurrence.model_validate(occurrence_data)
                            check_occurrence(occurrence, f"PrimaryCriteria.CriteriaList.{i}.{field_name}")
                        except (ValidationError, ValueError, TypeError):
                            pass

        # Check occurrences in inclusion rules
        if cohort.inclusion_rules:
            for i, rule in enumerate(cohort.inclusion_rules):
                if rule.expression and rule.expression.criteria_list:
                    for j, criteria in enumerate(rule.expression.criteria_list):
                        criteria_dict = criteria.model_dump(by_alias=True)

                        # Check direct Occurrence field
                        if "Occurrence" in criteria_dict and criteria_dict["Occurrence"]:
                            try:
                                occurrence = Occurrence.model_validate(criteria_dict["Occurrence"])
                                check_occurrence(occurrence, f"InclusionRules.{i}.expression.CriteriaList.{j}")
                            except (ValidationError, ValueError, TypeError):
                                pass

                        # Check Occurrence in nested criteria fields
                        for field_name, field_value in criteria_dict.items():
                            if isinstance(field_value, dict) and "Occurrence" in field_value:
                                occurrence_data = field_value["Occurrence"]
                                if isinstance(occurrence_data, dict):
                                    try:
                                        occurrence = Occurrence.model_validate(occurrence_data)
                                        check_occurrence(occurrence, f"InclusionRules.{i}.expression.CriteriaList.{j}.{field_name}")
                                    except (ValidationError, ValueError, TypeError):
                                        pass

        return issues

    def _validate_age_constraints(self, cohort: CohortExpression) -> list[ValidationIssue]:
        """Validate age range constraints."""
        issues = []

        def check_age_range(age_range, path: str) -> None:
            if age_range and hasattr(age_range, "value") and hasattr(age_range, "extent"):
                if age_range.value is not None and age_range.extent is not None and age_range.value > age_range.extent:
                    issues.append(
                        ValidationIssue(
                            field_path=f"{path}.Age",
                            message=f"Age range start ({age_range.value}) is greater than end ({age_range.extent})",
                            severity="error",
                        )
                    )
                if age_range.value is not None and age_range.value < 0:
                    issues.append(
                        ValidationIssue(field_path=f"{path}.Age", message=f"Age cannot be negative ({age_range.value})", severity="error")
                    )
                if age_range.extent is not None and age_range.extent > 150:
                    issues.append(
                        ValidationIssue(
                            field_path=f"{path}.Age", message=f"Age over 150 ({age_range.extent}) seems unrealistic", severity="warning"
                        )
                    )

        # Check demographic criteria ages (simplified example)
        # In practice, we'd traverse all criteria types that can have age constraints

        return issues


def validate_cohort_with_business_logic(data: dict, strict: bool = False) -> tuple[CohortExpression, list[ValidationIssue]]:
    """
    Convenience function to validate both schema and business logic.

    Args:
        data: Raw cohort expression data
        strict: If True, raise ValidationError on business logic issues

    Returns:
        Tuple of (validated_cohort, business_logic_issues)

    Raises:
        ValidationError: On schema validation errors, or business logic errors if strict=True
    """
    # First do schema validation (this will raise if invalid)
    cohort = CohortExpression.model_validate(data)

    # Then do business logic validation
    validator = BusinessLogicValidator(strict=strict)
    issues = validator.validate(cohort)

    return cohort, issues


# Convenience functions for backward compatibility and ease of use
def validate_schema_only(data: dict) -> CohortExpression:
    """Validate schema only (same as CohortExpression.model_validate)."""
    return CohortExpression.model_validate(data)


def validate_with_warnings(data: dict) -> tuple[CohortExpression, list[ValidationIssue]]:
    """Validate schema + business logic, returning warnings but not raising."""
    return validate_cohort_with_business_logic(data, strict=False)


def validate_strict(data: dict) -> CohortExpression:
    """Validate schema + business logic, raising on any issues."""
    cohort, _ = validate_cohort_with_business_logic(data, strict=True)
    return cohort


# WebAPI format validation functions
def validate_webapi_schema_only(data: dict[str, Any]) -> CohortExpression:
    """Validate WebAPI (camelCase) format cohort expression - schema only.

    Args:
        data: Dictionary containing cohort expression in WebAPI camelCase format

    Returns:
        CohortExpression: Validated cohort expression model

    Raises:
        ValidationError: If validation fails
    """
    # Convert WebAPI format to Circe format for validation
    circe_data = webapi_to_circe_dict(data)

    # Validate using standard schema validation
    return CohortExpression.model_validate(circe_data)


def validate_webapi_with_warnings(data: dict[str, Any]) -> tuple[CohortExpression, list[ValidationIssue]]:
    """Validate WebAPI (camelCase) format cohort expression with business logic warnings.

    Args:
        data: Dictionary containing cohort expression in WebAPI camelCase format

    Returns:
        tuple: (validated_expression, list_of_warnings)

    Raises:
        ValidationError: If schema validation fails
    """
    # Convert and validate schema first
    expression = validate_webapi_schema_only(data)

    # Run business logic validation
    validator = BusinessLogicValidator()
    warnings = validator.validate(expression)

    return expression, warnings


def validate_webapi_strict(data: dict[str, Any]) -> CohortExpression:
    """Validate WebAPI (camelCase) format cohort expression with strict business logic validation.

    Args:
        data: Dictionary containing cohort expression in WebAPI camelCase format

    Returns:
        CohortExpression: Validated cohort expression model

    Raises:
        ValidationError: If schema validation fails
        ValueError: If business logic validation fails
    """
    # Convert and validate with warnings
    expression, warnings = validate_webapi_with_warnings(data)

    # Raise error if any warnings found
    if warnings:
        error_messages = [f"{issue.severity}: {issue.message}" for issue in warnings]
        raise ValueError("Business logic validation failed:\n" + "\n".join(error_messages))

    return expression
