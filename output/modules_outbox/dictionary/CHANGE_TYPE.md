---
term: "Change Type"
canonical_id: "CHANGE_TYPE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-002_unifier_&_pirouette_debate_instrument"]
---

---
term: Change Type
canonical_id: CHANGE_TYPE
symbol: N/A
aliases: [Debate Outcome, Materialization Rule]
parents: [INST-DEB-001, DYNA-002]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: INST-DEB-001
      lines: "L20"
      snippet: |
        * **Change Type:** EXPAND (new module), MERGE (replace ≥2 with one), REVISION (redline of one).
  editors: [Automated Agent]
  review_log: []
triad:
  art: |
    The framework's metabolism: growth through expansion, wisdom through consolidation, and precision through revision. Each change is a measured, atomic breath in the life of the system, preventing cancerous drift.
  law: |
    Every automated debate must conclude with exactly one of three atomic, repository-altering outcomes—EXPAND, MERGE, or REVISION. Each type is governed by distinct materialization rules and CI/CD gates, ensuring all change is auditable and consistent.
  philosophy: |
    To ensure that all evolution of the framework is discrete, auditable, and purposeful. This model replaces ambiguous, continuous change with a finite set of governed transformations, making governance machine-readable and system growth non-pathological.
pirouette_definition: |
  A `Change Type` is a mandatory classification for the outcome of a Pirouette debate, specifying one of three exclusive and atomic repository operations. These types govern how the system evolves:
  - **EXPAND:** Introduces a new module, increasing the framework's scope.
  - **MERGE:** Consolidates two or more modules into a single successor, increasing parsimony and resolving redundancy.
  - **REVISION:** Updates a single existing module in place, refining its content while preserving its identity.
operational_definition:
  units: Categorical Enum {EXPAND, MERGE, REVISION}
  symbol_table: []
  measurement:
    procedures:
      - name: Docket Intent Specification
        outline: |
          The desired Change Type is declared in the `intent` field of the debate Docket (e.g., `"intent": "MERGE"`). The orchestration engine uses this value to select the appropriate materialization rules (INST-DEB-001 Sec. 6) and CI gates (Sec. 8) upon successful debate completion. The final materialized change must match the initial intent.
        expected_signals:
          - A single JSON key-value pair (`"intent": "EXPAND"|"MERGE"|"REVISION"`) in the input Docket.
          - A `Ratified Change Set` containing artifacts consistent with the specified intent (e.g., a new module for EXPAND, deprecation stubs for MERGE).
        pitfalls:
          - A mismatch between the stated `intent` and the actual changes proposed by synthesis (e.g., a MERGE intent that produces two new modules).
          - An ambiguous change that could be classified as either a MERGE or a major REVISION. The CI gates are designed to flag such cases for human review.
context_windows:
  - module: INST-DEB-001
    excerpt: |
      **Purpose.** Convert debate into *governed* change: each run must yield exactly one of {EXPAND, MERGE, REVISION}, with provenance, tests, and clean diffs.
  - module: INST-DEB-001
    excerpt: |
      **6.2 MERGE**
      - Produce successor module with `replaces: [A,B,…]`.
      - Write deprecation stubs into A,B with `replaced_by: [SuccessorID]` and short rationale.
      - One PR contains successor + stubs + ToC update.
poetic_connections:
  motifs: [Metabolism, Governance, Evolution, Atomicity, Pruning, Grafting]
  evocative_lines:
    - "Convert debate into *governed* change..."
    - "Materialization Rules (the three moves)"
  association_matrix:
    - [ "DEBATE_DOCKET", 0.9 ]
    - [ "RATIFIED_CHANGE_SET", 0.9 ]
    - [ "REPOSITORY_HYGIENE", 0.7 ]
    - [ "PERSONA", 0.5 ]
formal_mappings:
  candidates:
    - target: Database Transaction (INSERT, UPDATE, DELETE)
      domain: Software Engineering
      mapping_kind: operational
      equation_hint: N/A
      justification: |
        The three Change Types map directly to atomic database transaction patterns. EXPAND is an `INSERT` of a new record. REVISION is an `UPDATE` to an existing record. MERGE is a complex transaction involving an `INSERT` for the new module and `UPDATE`s to deprecate the old ones, preserving referential integrity via `replaces`/`replaced_by` fields analogous to foreign keys.
      references: []
      confidence: 0.9
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "Every automated change to the Pirouette module repository must be categorized as exactly one of EXPAND, MERGE, or REVISION."
      domain: theory
      falsifier: "A commit to the main branch altering module content that does not have a corresponding debate dossier with one of the three change types, or a dossier that specifies more than one type."
      status: supported
      links: [INST-DEB-001]
naming_notes:
  collisions: []
  disambiguation: |
    This term refers to the discrete *outcome* of a debate, not the debate process itself. It is distinct from the `intent` field in a Docket, although the `intent` must match the final Change Type for an automated run to be accepted by CI.
crosslinks:
  near_synonyms: [MATERIALIZATION_RULE]
  antonyms: [UNGOVERNED_CHANGE, CONTINUOUS_DRIFT]
  prerequisites: [DEBATE_DOCKET]
  downstream_effects: [MODULE_LIFECYCLE, REPOSITORY_HYGIENE, RATIFIED_CHANGE_SET]
license: CC-BY-SA-4.0
---

# Change Type

## Canonical (Pirouette)
A `Change Type` is a mandatory classification for the outcome of a Pirouette debate, specifying one of three exclusive and atomic repository operations. These types govern how the system evolves:
- **EXPAND:** Introduces a new module, increasing the framework's scope.
- **MERGE:** Consolidates two or more modules into a single successor, increasing parsimony and resolving redundancy.
- **REVISION:** Updates a single existing module in place, refining its content while preserving its identity.

## Software Engineering Analogy
The three Change Types map directly to atomic database transaction patterns. **EXPAND** is an `INSERT` of a new record. **REVISION** is an `UPDATE` to an existing record. **MERGE** is a complex transaction involving an `INSERT` for the new module and `UPDATE`s to deprecate the old ones, preserving referential integrity via `replaces`/`replaced_by` fields analogous to foreign keys. This ensures all changes are discrete and auditable.

## Glossary Links
- See also: DEBATE_DOCKET, RATIFIED_CHANGE_SET, MODULE_LIFECYCLE