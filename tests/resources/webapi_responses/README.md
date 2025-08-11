# WebAPI Response Test Data

This directory contains **actual WebAPI responses** captured from live OHDSI WebAPI instances for testing our Pydantic models against real-world data.

## Purpose

- **Real-world validation**: Test parsing of actual API responses (not synthetic data)
- **Regression testing**: Detect when WebAPI response formats change  
- **Edge case coverage**: Capture various response sizes and formats
- **Model validation**: Ensure our Pydantic models handle real WebAPI data correctly

## Data Sources

### Atlas Demo (`atlas-demo/`)
Responses captured from: `https://atlas-demo.ohdsi.org/WebAPI`
- **Date captured**: [Date will be added when script runs]
- **WebAPI version**: [Version will be captured in info/version_info.json]
- **Database**: EUNOMIA synthetic data

## Directory Structure

```
webapi_responses/
├── README.md                    # This file
└── atlas-demo/                 # Responses from Atlas demo WebAPI
    ├── cohortdefinition/
    │   ├── list_response.json          # GET /cohortdefinition
    │   ├── cohort_{id}.json            # GET /cohortdefinition/{id}
    │   ├── expression_{id}.json        # GET /cohortdefinition/{id}/expression  
    │   └── info_{id}.json              # GET /cohortdefinition/{id}/info
    ├── conceptset/
    │   ├── list_response.json          # GET /conceptset
    │   ├── conceptset_{id}.json        # GET /conceptset/{id}
    │   ├── expression_{id}.json        # GET /conceptset/{id}/expression
    │   └── items_{id}.json             # GET /conceptset/{id}/items
    ├── vocabulary/
    │   ├── search_{term}.json          # GET /vocabulary/search?query={term}
    │   ├── concept_{id}.json           # GET /vocabulary/concept/{id}
    │   ├── descendants_{id}.json       # GET /vocabulary/concept/{id}/descendants
    │   └── ancestors_{id}.json         # GET /vocabulary/concept/{id}/ancestors
    ├── source/
    │   └── sources_list.json           # GET /source/sources
    └── info/
        └── version_info.json           # GET /info
```

## Model Coverage

### Primary Models Tested
- **CohortExpression**: Tested via `/cohortdefinition/{id}/expression` responses
- **ConceptSet**: Tested via `/conceptset/{id}` responses  
- **ConceptSetExpression**: Tested via `/conceptset/{id}/expression` responses
- **Concept**: Tested via `/vocabulary/concept/{id}` and search responses

### Response Types Captured
- **Lists**: Multiple items (cohort definitions, concept sets, search results)
- **Single items**: Individual entities with full details
- **Expressions**: Complex nested JSON structures (cohort expressions, concept set expressions)
- **Resolved data**: Computed results (concept descendants, resolved concept items)

## Usage in Tests

### Basic Response Parsing
```python
import json
from pathlib import Path
from ohdsi_cohort_schemas.models.cohort import CohortExpression

def test_real_cohort_expression_parsing():
    # Load actual WebAPI response
    response_file = Path("tests/resources/webapi_responses/atlas-demo/cohortdefinition/expression_123.json")
    with open(response_file) as f:
        response_data = json.load(f)
    
    # Test our model can parse it
    cohort_expr = CohortExpression.model_validate(response_data)
    assert cohort_expr.concept_sets is not None
    assert cohort_expr.primary_criteria is not None
```

### List Response Testing
```python
def test_cohort_list_parsing():
    with open("tests/resources/webapi_responses/atlas-demo/cohortdefinition/list_response.json") as f:
        cohorts_list = json.load(f)
    
    # Test we can parse each cohort definition
    for cohort_data in cohorts_list:
        cohort = CohortDefinition.model_validate(cohort_data)
        assert cohort.id is not None
        assert cohort.name is not None
```

### Concept Testing
```python
def test_vocabulary_search_parsing():
    with open("tests/resources/webapi_responses/atlas-demo/vocabulary/search_diabetes.json") as f:
        search_results = json.load(f)
    
    # Test concept parsing
    concepts = [Concept.model_validate(item) for item in search_results]
    assert len(concepts) > 0
    assert all(c.concept_id is not None for c in concepts)
```

## Updating Test Data

### Capture Fresh Responses
```bash
# Run the capture script to get latest responses
poetry run python scripts/capture_webapi_responses.py
```

### Add New Endpoints
To capture responses from additional endpoints:
1. Edit `scripts/capture_webapi_responses.py`
2. Add new capture methods
3. Update this README with new file locations

## Data Freshness

- **Last updated**: [Date will be updated when script runs]
- **WebAPI version**: See `atlas-demo/info/version_info.json`
- **Recommended refresh**: Monthly or when WebAPI versions change

## Notes

### Rate Limiting
The capture script includes delays between requests to be respectful to the Atlas demo server.

### Anonymization
All responses are from the public Atlas demo WebAPI using synthetic EUNOMIA data - no real patient data.

### File Sizes
Some responses (especially large concept lists) may be sizeable. Git LFS is not currently used but could be added if needed.

### Error Responses
Future versions may capture error responses (404s, validation errors) for negative testing.
