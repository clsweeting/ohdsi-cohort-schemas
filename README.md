# OHDSI Cohort Schemas

[![PyPI version](https://badge.fury.io/py/ohdsi-cohort-schemas.svg)](https://badge.fury.io/py/ohdsi-cohort-schemas)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Pydantic models for validating **OHDSI/Circe cohort definition schemas**. This library provides comprehensive type-safe validation for OHDSI cohort expressions, enabling:

- **IDE Support**: Full autocompletion and type checking for cohort definitions
- **Schema Validation**: Catch errors before sending to WebAPI
- **Documentation**: Living documentation via Pydantic models  
- **Interoperability**: Consistent schema validation across tools

> **Attribution**: This library is based on the cohort expression schema from the [OHDSI Circe](https://github.com/OHDSI/circe-be) project. Test data and schema structures are derived from the official Circe backend test suite to ensure compatibility with OHDSI standards.

## Installation

```bash
pip install ohdsi-cohort-schemas
```

## Quick Start

```python
from ohdsi_cohort_schemas import CohortExpression, validate_schema_only, validate_with_warnings

# Quick schema validation (fast, Pydantic-only)
try:
    cohort = validate_schema_only(cohort_json)
    print("✅ Valid schema!")
except ValidationError as e:
    print(f"❌ Schema errors: {e}")

# Full validation with business logic checks (comprehensive)
cohort, warnings = validate_with_warnings(cohort_json)
print("✅ Valid cohort definition!")
if warnings:
    print("⚠️ Warnings:")
    for warning in warnings:
        print(f"  - {warning.message}")
```

## WebAPI Format Support (NEW in v0.2.0)

This library now supports **WebAPI camelCase format** in addition to the native Circe mixed-case format. This enables seamless integration with OHDSI WebAPI clients.

### Format Differences

- **Circe Format**: Mixed case (PascalCase + camelCase + ALL_CAPS)
  ```json
  {
    "ConceptSets": [{"id": 1, "expression": {"items": [{"concept": {"CONCEPT_ID": 123}}]}}],
    "PrimaryCriteria": {"CriteriaList": [{"ConditionOccurrence": {"CodesetId": 1}}]}
  }
  ```

- **WebAPI Format**: Consistent camelCase
  ```json
  {
    "conceptSets": [{"id": 1, "expression": {"items": [{"concept": {"conceptId": 123}}]}}],
    "primaryCriteria": {"criteriaList": [{"conditionOccurrence": {"codesetId": 1}}]}
  }
  ```

### WebAPI Validation Functions

```python
from ohdsi_cohort_schemas import (
    validate_webapi_schema_only,
    validate_webapi_with_warnings,
    validate_webapi_strict,
    webapi_to_circe_dict,
    circe_to_webapi_dict
)

# Validate WebAPI camelCase format directly
cohort = validate_webapi_schema_only(webapi_json)

# Get warnings for WebAPI format
cohort, warnings = validate_webapi_with_warnings(webapi_json)

# Strict validation (raises on warnings)
cohort = validate_webapi_strict(webapi_json)

# Format conversion
circe_format = webapi_to_circe_dict(webapi_json)
webapi_format = circe_to_webapi_dict(circe_json)
```

### Building Cohorts Programmatically

```python
from ohdsi_cohort_schemas import CohortExpression, ConceptSet, ConceptSetItem, Concept

# Define a concept set
concept = Concept(
    concept_id=201826,
    concept_name="Type 2 diabetes mellitus",
    standard_concept="S",
    concept_code="44054006",
    concept_class_id="Clinical Finding",
    vocabulary_id="SNOMED",
    domain_id="Condition"
)

concept_set_item = ConceptSetItem(
    concept=concept,
    include_descendants=True,
    include_mapped=False,
    is_excluded=False
)

concept_set = ConceptSet(
    id=0,
    name="Type 2 Diabetes",
    expression=ConceptSetExpression(items=[concept_set_item])
)

# Build a complete cohort expression
cohort_expression = CohortExpression(
    concept_sets=[concept_set],
    primary_criteria=...,  # Define primary criteria
    inclusion_rules=[],    # Optional inclusion rules
    censoring_criteria=[]  # Optional censoring criteria
)
```

## Features

### Complete Schema Coverage
- ✅ **ConceptSets** - Medical concept definitions with descendants
- ✅ **PrimaryCriteria** - Index event definitions  
- ✅ **InclusionRules** - Additional filtering criteria
- ✅ **CensoringCriteria** - Observation period requirements
- ✅ **All Criteria Types** - Conditions, drugs, procedures, measurements, etc.
- ✅ **Time Windows** - Complex temporal relationships
- ✅ **Demographics** - Age, gender, race, ethnicity filters

### Validation Features
- **Dual Validation Modes**: Fast schema-only validation or comprehensive business logic validation
- **Schema Validation**: Pure Pydantic validation for structure and types
- **Business Logic Validation**: Semantic checks for logical consistency and OHDSI best practices
- **Type Safety**: Full static type checking with mypy
- **Runtime Validation**: Comprehensive Pydantic validation
- **Custom Validators**: Domain-specific validation rules
- **Error Messages**: Clear, actionable validation errors
- **JSON Schema**: Generate JSON schemas for other tools

## Documentation

### Core Models

#### CohortExpression
The root model representing a complete cohort definition:

```python
class CohortExpression(BaseModel):
    concept_sets: List[ConceptSet]
    primary_criteria: PrimaryCriteria
    qualified_limit: Optional[Limit] = None
    expression_limit: Optional[Limit] = None
    inclusion_rules: List[InclusionRule] = []
    end_strategy: Optional[EndStrategy] = None
    censoring_criteria: List[CensoringCriteria] = []
    collapse_settings: Optional[CollapseSettings] = None
    censor_window: Optional[CensorWindow] = None
```

#### ConceptSet
Defines reusable groups of medical concepts:

```python
class ConceptSet(BaseModel):
    id: int
    name: str
    expression: ConceptSetExpression

class ConceptSetExpression(BaseModel):
    items: List[ConceptSetItem]

class ConceptSetItem(BaseModel):
    concept: Concept
    include_descendants: bool = True
    include_mapped: bool = False
    is_excluded: bool = False
```

#### Criteria Types
Support for all OMOP domain criteria:

- `ConditionOccurrence` - Medical conditions
- `DrugExposure` - Medication exposures  
- `DrugEra` - Continuous drug exposure periods
- `ProcedureOccurrence` - Medical procedures
- `Measurement` - Lab values and vital signs
- `Observation` - Clinical observations
- `DeviceExposure` - Medical device usage
- `Death` - Death events
- `VisitOccurrence` - Healthcare encounters
- `VisitDetail` - Detailed visit information
- `ObservationPeriod` - Data availability periods
- `Specimen` - Biological specimen collection

## Library Scope

This library focuses specifically on **cohort expression validation** - the clinical logic that defines patient selection criteria. It validates the `expression` portion of cohort definitions, which contains:

- `ConceptSets` - Medical concept definitions
- `PrimaryCriteria` - Index event definitions  
- `InclusionRules` - Additional filtering criteria
- `CensoringCriteria` - Observation period requirements

### What This Library Does NOT Handle

This library intentionally does **not** handle WebAPI metadata such as:
- Cohort metadata (`id`, `name`, `description`)
- Permission management (`hasWriteAccess`, `tags`)
- User tracking (`createdBy`, `modifiedBy`)
- Timestamps (`createdDate`, `modifiedDate`)

These concerns are handled by API client libraries (like `ohdsi-webapi-client`) that focus on the full WebAPI response structure while using this library for the clinical validation of the `expression` field.

### Integration Example

```python
# WebAPI client handles full response
cohort_response = {
    "id": 123,
    "name": "My Cohort",
    "hasWriteAccess": true,
    "expression": {
        "ConceptSets": [...],     # ← This library validates this part
        "PrimaryCriteria": {...}  # ← And this part
    }
}

# Extract and validate just the expression
from ohdsi_cohort_schemas import validate_webapi_schema_only
validated_expression = validate_webapi_schema_only(cohort_response["expression"])
```

## JSON Format Support

This library supports two different JSON field naming conventions, reflecting the different contexts where cohort definitions are used:

### Database Format (ALL_CAPS)
Used by Circe backend test data and internal cohort processing:
```json
{
  "concept": {
    "CONCEPT_ID": 201826,
    "CONCEPT_NAME": "Type 2 diabetes mellitus",
    "VOCABULARY_ID": "SNOMED"
  }
}
```

### WebAPI Format (camelCase)  
Used by OHDSI WebAPI JSON responses and web applications:
```json
{
  "concept": {
    "conceptId": 201826,
    "conceptName": "Type 2 diabetes mellitus", 
    "vocabularyId": "SNOMED"
  }
}
```

### Why Two Formats?

- **Circe Backend Test Data**: Uses ALL_CAPS because it matches **OMOP CDM database column names** (which are traditionally UPPERCASE in SQL databases)

- **WebAPI JSON Responses**: Uses camelCase because it follows **standard JSON/JavaScript conventions** for web APIs

- **Different Purposes**:
  - **Circe**: Internal cohort definition processing (matches database schema)
  - **WebAPI**: External API communication (matches web standards)

The library provides separate validation functions for each format to ensure seamless integration with both contexts.

### Validation Examples

#### Database Format Validation (ALL_CAPS)
For Circe test data and database-formatted JSON:

```python
from ohdsi_cohort_schemas import validate_db_schema, validate_db_with_warnings
from pydantic import ValidationError

# Fast schema validation - structure and types only
try:
    cohort = validate_db_schema(circe_json)  # ALL_CAPS format
    print("✅ Valid schema!")
except ValidationError as e:
    print(f"❌ Schema errors: {e}")

# Full validation with business logic checks
result = validate_db_with_warnings(circe_json)
if result.is_valid:
    print("✅ Valid cohort definition!")
    if result.warnings:
        print("⚠️ Warnings:")
        for warning in result.warnings:
            print(f"  - {warning}")
else:
    print("❌ Validation failed:")
    for error in result.errors:
        print(f"  - {error}")
```

#### WebAPI Format Validation (camelCase)
For WebAPI responses and web application JSON:

```python
from ohdsi_cohort_schemas import validate_webapi_schema_only, validate_webapi_with_warnings

# Fast schema validation for WebAPI format
try:
    cohort = validate_webapi_schema_only(webapi_json)  # camelCase format
    print("✅ Valid WebAPI schema!")
except ValidationError as e:
    print(f"❌ Schema errors: {e}")

# Full validation with business logic checks
result = validate_webapi_with_warnings(webapi_json)
if result.is_valid:
    print("✅ Valid cohort definition!")
    if result.warnings:
        print("⚠️ Warnings:")
        for warning in result.warnings:
            print(f"  - {warning}")
else:
    print("❌ Validation failed:")
    for error in result.errors:
        print(f"  - {error}")
```

#### Legacy API (Backward Compatibility)
The original functions are still available and work with database format:

```python
from ohdsi_cohort_schemas import validate_schema_only, validate_with_warnings, validate_strict

# Legacy functions (equivalent to validate_db_* functions)
try:
    cohort = validate_schema_only(circe_json)
    print("✅ Valid schema!")
except ValidationError as e:
    print(f"❌ Schema errors: {e}")

# Validation with warnings for best practices
cohort, warnings = validate_with_warnings(circe_json)
print("✅ Valid cohort definition!")
if warnings:
    print("⚠️ Warnings:")
    for warning in warnings:
        print(f"  - {warning.message}")

# Strict validation - warnings treated as errors
try:
    cohort = validate_strict(circe_json)
    print("✅ Perfect cohort definition!")
except ValidationError as e:
    print(f"❌ Validation failed: {e}")
```

#### Advanced Business Logic Validation
```python
from ohdsi_cohort_schemas import BusinessLogicValidator

# Custom validation with specific rules
validator = BusinessLogicValidator()
issues = validator.validate(cohort_json)

errors = [issue for issue in issues if issue.severity == 'error']
warnings = [issue for issue in issues if issue.severity == 'warning']

print(f"Found {len(errors)} errors and {len(warnings)} warnings")
for issue in errors:
    print(f"❌ {issue.rule}: {issue.message}")
for issue in warnings:
    print(f"⚠️ {issue.rule}: {issue.message}")
```

#### Legacy Validation API
```python
from ohdsi_cohort_schemas import CohortExpression
from pydantic import ValidationError

# Direct Pydantic validation (legacy approach)
try:
    cohort = CohortExpression.model_validate(cohort_json)
    print("✅ Valid schema!")
except ValidationError as e:
    print(f"❌ Schema errors:")
    for error in e.errors():
        print(f"  - {error['loc']}: {error['msg']}")
```

#### JSON Schema Generation
```python
from ohdsi_cohort_schemas import CohortExpression

# Generate JSON schema for other tools
schema = CohortExpression.model_json_schema()

# Save for use in other languages/tools
import json
with open("cohort_schema.json", "w") as f:
    json.dump(schema, f, indent=2)
```

## Test Data & Validation

### Test Data Structure

Our comprehensive test suite uses official JSON examples from the [OHDSI Circe project](https://github.com/OHDSI/circe-be) to ensure compatibility with real-world cohort definitions:

```
tests/resources/
├── checkers/                 # Business logic validation test cases
│   ├── *Correct.json        # Valid cohorts (should pass validation)
│   └── *Incorrect.json      # Invalid cohorts (should fail validation)
├── conceptset/              # Standalone concept set expressions
└── cohortgeneration/        # Complete cohort definitions
```

### Test Categories

- **Schema Validation Tests**: All JSON files are validated against our Pydantic models
- **Business Logic Tests**: Files ending with `Correct.json` should pass all validation rules
- **Negative Tests**: Files ending with `Incorrect.json` should fail business logic validation
- **Concept Set Tests**: Standalone concept set expressions for testing concept-related logic

### Data Source Attribution

The test data originates from the official [Circe test resources](https://github.com/OHDSI/circe-be/tree/master/src/test/resources), ensuring our validation logic handles the same edge cases and patterns that the official OHDSI tools encounter.

> **Note**: We've removed `_PREP.json` and `_VERIFY.json` files from the original Circe test suite as these are used for database-level testing of SQL generation, not JSON schema validation. Our library focuses on validating cohort definition structure and business logic before database execution.

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## Attribution & License

### Schema Source
This library implements Pydantic models for the cohort expression schema defined by the [OHDSI Circe](https://github.com/OHDSI/circe-be) project. The schema structures, field definitions, and validation logic are derived from the official Circe backend to ensure full compatibility with OHDSI standards.

### Test Data
The validation test suite uses official JSON examples from the [Circe test resources](https://github.com/OHDSI/circe-be/tree/master/src/test/resources/cohortgeneration) to ensure our implementation correctly handles real-world cohort definitions.

### OHDSI Ecosystem Compatibility
- **License**: Apache 2.0 (matching OHDSI ecosystem standards)
- **Standards**: Fully compatible with OHDSI WebAPI and ATLAS
- **OMOP CDM**: Supports the OMOP Common Data Model vocabulary standards
- **Interoperability**: Designed for seamless integration with other OHDSI tools

### Acknowledgments
We gratefully acknowledge:
- **[OHDSI Collaborative](https://www.ohdsi.org/)** for developing and maintaining the Circe cohort expression standards
- **[Pydantic](https://pydantic.dev/)** for providing the validation framework
- **OHDSI Community** for the open-source ecosystem that makes this work possible

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
