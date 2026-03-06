## MODIFIED Requirements

### Requirement: Output package contract parity across modes
For equivalent source skill content, directory mode and zip mode SHALL produce equivalent required contract files and equivalent `execution_modes` semantics derived from the same mode assessment rules.

#### Scenario: Mode parity for contracts and execution modes
- **WHEN** the same source skill content is converted via directory mode and zip mode
- **THEN** generated `assets/runner.json`, `assets/input.schema.json`, `assets/parameter.schema.json`, and `assets/output.schema.json` are equivalent in contract semantics
- **AND** `runner.json.execution_modes` follows the same mapping from the shared mode suitability outcomes

### Requirement: Converted package remains complete and install-ready
Both modes MUST produce a complete install-ready package including bundled protocol reference and conversion report.

#### Scenario: Complete package output in directory mode
- **WHEN** conversion succeeds from directory mode
- **THEN** output includes converted skill directory, install-ready zip, `references/file_protocol.md`, and conversion report
