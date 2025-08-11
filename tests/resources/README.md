# Circe-be test data 

`/tests/resources` contains a subset of the test data used by OHDSI Circe Be: 

https://github.com/OHDSI/circe-be/tree/master/src/test/resources

These are primarily JSON files - structured test data for OHDSI cohort definitions, concept sets, criteria, etc.

Behold the glorious mix of PascalCase, camelCase & snake_case in some of the JSON keys. 

Key folders:
- /checkers - Positive & negative validation tests
- /cohortgeneration - Official cohort expression examples (used by validate_test_data.py)
- /conceptset - Concept set expressions (dupilumab, dupixent drug examples)
- /criteria - Criteria definitions and SQL templates
- /versioning - Version-specific test cases
- /datasets - Test dataset examples
- /windowcriteria - Time window criteria examples

Note: The /cohortgeneration folder contains the main cohort expression test files
that our validation scripts use to test Pydantic schema compatibility.

