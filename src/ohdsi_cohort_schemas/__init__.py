"""
OHDSI Cohort Schemas

Pydantic models for validating OHDSI/Circe cohort definition schem    webapi_to_circe_dict,
]

__version__ = "0.4.0".

Basic Usage (Schema Validation Only):
    from ohdsi_cohort_schemas import CohortExpression

    cohort = CohortExpression.model_validate(json_data)

Advanced Usage (Schema + Business Logic Validation):
    from ohdsi_cohort_schemas import validate_with_warnings, validate_strict

    # Get warnings but don't raise errors
    cohort, issues = validate_with_warnings(json_data)
    for issue in issues:
        print(f"Warning: {issue.message}")

    # Raise errors on business logic issues
    cohort = validate_strict(json_data)
"""

from .models.cohort import CohortExpression

# from .models.criteria import (
#     ConditionOccurrence,
#     DrugExposure,
#     DrugEra,
#     ProcedureOccurrence,
#     Measurement,
#     Observation,
#     DeviceExposure,
#     Death,
#     VisitOccurrence,
#     VisitDetail,
#     ObservationPeriod,
#     Specimen,
# )
from .models.common import (
    DateRange,
    Limit,
    NumericRange,
    Occurrence,
    Window,
)
from .models.concept_set import ConceptSet, ConceptSetExpression, ConceptSetItem
from .models.vocabulary import Concept

# Optional business logic validation
from .validation import (
    BusinessLogicValidator,
    ValidationIssue,
    camel_to_pascal_dict,
    circe_to_webapi_dict,
    pascal_to_camel_dict,
    validate_cohort_with_business_logic,
    validate_schema_only,
    validate_strict,
    validate_webapi_schema_only,
    validate_webapi_strict,
    validate_webapi_with_warnings,
    validate_with_warnings,
    webapi_to_circe_dict,
)

__version__ = "0.3.0"
__all__ = [
    # Main models
    "CohortExpression",
    "ConceptSet",
    "ConceptSetExpression",
    "ConceptSetItem",
    "Concept",
    # Common types
    "Limit",
    "Window",
    "DateRange",
    "NumericRange",
    "Occurrence",
    # Business logic validation
    "BusinessLogicValidator",
    "ValidationIssue",
    "camel_to_pascal_dict",
    "circe_to_webapi_dict",
    "pascal_to_camel_dict",
    "validate_cohort_with_business_logic",
    "validate_schema_only",
    "validate_webapi_schema_only",
    "validate_webapi_strict",
    "validate_webapi_with_warnings",
    "validate_with_warnings",
    "validate_strict",
    "webapi_to_circe_dict",
]
