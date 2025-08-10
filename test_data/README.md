# Test Data - Official Circe JSON Examples

This folder contains **official cohort expression JSON files** copied from the [OHDSI Circe Backend](https://github.com/OHDSI/circe-be) repository test suite. These represent real-world cohort definitions used to validate our Pydantic schema implementation.

> **Recent Update**: We've removed unused `_PREP.json` and `_VERIFY.json` files that were part of the original Circe database testing framework. These files contained CDM table data and expected query results for SQL generation testing, which is not relevant for our JSON schema validation library. Our focus is on validating cohort definition structure and business logic before database execution.

## Files Overview

| File | Description | Status | Key Features |
|------|-------------|--------|--------------|
| `firstOccurrenceTestExpression.json` | ✅ **Working** | Simple cohort with concept set | Empty criteria list, basic structure |
| `allCriteriaExpression.json` | ❌ Needs work | Complex cohort with all criteria types | Demographics, all OMOP domains |
| `simpleInclusionRule.json` | ❌ Needs work | Basic inclusion rule example | ConditionOccurrence criteria |
| `countsExpression.json` | ❌ Needs work | Correlated criteria with counts | Group criteria, occurrence counting |
| `fixedOffsetExpression.json` | ❌ Needs work | Cohort with fixed end strategy | EndStrategy configuration |
| `limitExpression.json` | ❌ Needs work | Cohort with expression limits | Limiting strategies |
| `mixedConceptsetsExpression.json` | ❌ Needs work | Multiple concept sets | Mixed concept set usage |

## Current Validation Status

**✅ 1/7 files validate successfully** (14% coverage)

## Key Schema Insights

### Working Structure
```json
{
  "ConceptSets": [...],
  "PrimaryCriteria": {
    "CriteriaList": [],  // ✅ Empty lists work
    "ObservationWindow": {...},
    "PrimaryCriteriaLimit": {...}
  }
}
```

### Missing Schema Components

1. **Criteria Models** - Need to implement:
   ```json
   "CriteriaList": [
     {
       "Criteria": {
         "ConditionOccurrence": {...}  // ❌ Missing
       }
     }
   ]
   ```

2. **Domain-Specific Criteria** - Need models for:
   - `ConditionOccurrence`
   - `DrugExposure` 
   - `ProcedureOccurrence`
   - `Measurement`
   - `Observation`
   - `VisitOccurrence`
   - `Death`
   - `DeviceExposure`

3. **Demographics Criteria**:
   ```json
   "DemographicCriteriaList": [
     {
       "Gender": [...],
       "Race": [...],
       "Ethnicity": [...]
     }
   ]
   ```

4. **End Strategy Models**:
   ```json
   "EndStrategy": {
     "Type": "...",        // ❌ Missing enum values
     "DateOffset": "..."   // ❌ Wrong type expected
   }
   ```

## Usage

### Validate Against Test Data
```bash
# Run validation script
python examples/validate_test_data.py

# Refresh test data from Circe repo
make setup-test-data
```

### Individual File Testing
```python
from pathlib import Path
import json
from ohdsi_cohort_schemas import CohortExpression

# Load a test file
test_file = Path("test_data/firstOccurrenceTestExpression.json")
with open(test_file) as f:
    data = json.load(f)

# Validate
cohort = CohortExpression.model_validate(data)
print(f"✅ Valid: {cohort.concept_sets[0].name}")
```

## Value Proposition

This test data approach provides:

1. **Real-world validation** - Not synthetic examples
2. **Incremental development** - Fix one file at a time
3. **Regression testing** - Catch schema breaking changes
4. **Coverage tracking** - Clear progress metrics
5. **Canonical examples** - Reference implementations

## Next Steps

1. **Implement missing criteria models** (highest priority)
2. **Add demographic criteria support** 
3. **Fix EndStrategy model**
4. **Add remaining OMOP domain criteria**
5. **Target 100% validation success**

Once all files validate, we'll have a robust, production-ready schema library! 🎯
