## MODIFIED Requirements

### Requirement: Converter logic is prompt-first and SKILL.md-driven
The converter skill MUST define conversion orchestration in `SKILL.md`, including independent mode suitability assessment (`auto` / `interactive`) before conversion classification and strategy execution.

#### Scenario: Mode-first semantic conversion flow executed from SKILL.md
- **WHEN** the converter skill is invoked
- **THEN** the skill first determines auto suitability and interactive suitability independently
- **AND** only then resolves classification and conversion strategy through staged prompt flow
