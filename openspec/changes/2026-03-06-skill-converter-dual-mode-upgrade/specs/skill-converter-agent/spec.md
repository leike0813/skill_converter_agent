## MODIFIED Requirements

### Requirement: Converter validates output package against install-time rules
The converter skill MUST validate converted output against the same structural rules required by Skill Runner skill-package installation, with parity to current upstream contracts, validator logic, and engine policy.

#### Scenario: Reject non-installable conversion output with upstream parity
- **WHEN** converted output violates required structure, mode, schema meta, or engine policy constraints
- **THEN** conversion is marked failed with actionable validation errors consistent with upstream validator categories

### Requirement: Converter supports mode-aware conversion analysis
The converter skill MUST independently assess suitability for `auto` and `interactive` execution modes before final conversion decisions.

#### Scenario: Produce independent mode suitability outcomes
- **WHEN** source skill analysis is executed
- **THEN** converter outputs explicit suitability conclusions and evidence for auto and interactive separately
- **AND** converter derives conversion strategy and target execution modes from these assessments
