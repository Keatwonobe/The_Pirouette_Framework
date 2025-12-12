---
term: "Ratified Change Set"
canonical_id: "RATIFIED_CHANGE_SET"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-002_unifier_&_pirouette_debate_instrument"]
---

---
term: Ratified Change Set
canonical_id: RATIFIED_CHANGE_SET
symbol: Δ̂
aliases: []
parents: [INST-DEB-001]
children: [CORE-*, DOMA-*, DYNA-*, MATH-*, INST-*, XXP-*, TLE-*, PDM-*]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DYNA-002_unifier_&_pirouette_debate_instrument
      snippet: |
        * **Ratified Change Set:** Materialized repo artifacts + debate dossier + commit tag.
  editors: [Keaton (PDM-000 custodian)]
  review_log: []
triad:
  art: |
    The crystallization of argument into archive. A debate's ghost, sealed in the amber of the repository, carrying the complete, verifiable memory of its own creation.
  law: |
    A Ratified Change Set is the sole valid output of an `accept` verdict from a debate governed by INST-DEB-001. It must contain a versioned diff, passing CI tests, and a complete provenance dossier linking it to a unique debate run identifier.
  philosophy: |
    To ensure the framework evolves not by fiat or accretion, but through structured, falsifiable reasoning. Each change set is a self-contained, auditable proof of its own necessity, preventing conceptual drift and ensuring every modification strengthens the whole.
pirouette_definition: |
  The atomic, committable package resulting from a successful Pirouette Debate. It comprises three mandatory components: 1) the materialized repository artifacts (new/modified modules, deprecation stubs), 2) the complete debate dossier (docket, persona briefs, final scorecard), and 3) the linking Git commit tag. A change set is considered ratified only after passing all CI/CD gates defined in INST-DEB-001.
operational_definition:
  units: N/A (data package)
  symbol_table:
    - name: Δ̂
      meaning: A single, ratified change set.
      dimensions: Information
      default_range: N/A
  measurement:
    procedures:
      - name: CI Gate Validation
        outline: |
          Execute the CI/CD pipeline against a proposed change set. The procedure validates: 1) schema conformance of all dossier components (docket, scorecard), 2) referential integrity of module links (parents, replaces, replaced_by), 3) successful binding and execution of all specified `XXP-*` tests, and 4) inclusion of the `debate.json` and `scorecard.json` in the commit artifacts.
        expected_signals: [A `return code: 0` from the `inst-deb materialize` command, A passing CI run, A Git tag of form `debate-run-<epoch>`]
        pitfalls: [Incomplete provenance dossier, Failed or unbound `XXP-*` tests, Schema drift between the instrument and the change set's components]
context_windows:
  - module: DYNA-002_unifier_&_pirouette_debate_instrument
    excerpt: |
      **Purpose.** Convert debate into *governed* change: each run must yield exactly one of {EXPAND, MERGE, REVISION}, with provenance, tests, and clean diffs.
      ...
      * **Ratified Change Set:** Materialized repo artifacts + debate dossier + commit tag.
  - module: DYNA-002_unifier_&_pirouette_debate_instrument
    excerpt: |
      **6) Materialization Rules (the three moves)**
      **6.1 EXPAND** Create new module `NEW-<series>-<id>` with `status: draft` and required `tests` section.
      **6.2 MERGE** Produce successor module with `replaces: [A,B,…]`. Write deprecation stubs into A,B with `replaced_by: [SuccessorID]`.
      **6.3 REVISION** Keep same id, bump `version`. Attach semantic redline (machine diff + human-readable summary).
poetic_connections:
  motifs: [crystallization, provenance, atomic change, governance, audit trail]
  evocative_lines:
    - "Convert debate into *governed* change"
    - "each run must yield exactly one of {EXPAND, MERGE, REVISION}"
  association_matrix:
    - [ "DOCKET", 0.9 ]
    - [ "SCORECARD", 0.9 ]
    - [ "PERSONA", 0.7 ]
formal_mappings:
  candidates:
    - target: Git Commit
      domain: Software Engineering
      mapping_kind: conceptual
      justification: |
        A Git commit is an atomic snapshot of changes to a repository. A Ratified Change Set is a specialized, heavily-governed type of commit that also bundles its own justification (the debate dossier), making it conceptually analogous but with a stricter information content requirement.
      confidence: 0.9
  adopted:
    - target: Pull Request (Git)
      rationale: |
        The Pull Request is the most direct operational analog, representing a proposed atomic change that is subject to automated checks (CI gates) and human review before being incorporated into the main repository state. The dossier is included in the PR as a verifiable artifact.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "Every change to a `stable` module in the Pirouette repository must originate from exactly one Ratified Change Set."
      domain: theory
      falsifier: "Discovering a direct commit to a stable module on the main branch that does not have a corresponding `debate-run-*` tag and a complete, valid provenance dossier."
      status: proposed
      links: [INST-DEB-001]
naming_notes:
  collisions: [Common term "changeset" in version control systems like Mercurial or TFS.]
  disambiguation: |
    Distinct from a generic version control 'changeset' or 'commit'. A Pirouette Ratified Change Set is a specific data package including not just the code diff, but the entire machine-readable debate dossier (docket, briefs, scorecard) that generated it.
crosslinks:
  near_synonyms: []
  antonyms: [UNSTRUCTURED_COMMIT]
  prerequisites: [DOCKET, PIRIOUETTE_DEBATE_INSTRUMENT]
  downstream_effects: [MODULE_REVISION, MODULE_EXPANSION, MODULE_MERGE]
license: CC-BY-SA-4.0
---

# Ratified Change Set

## Canonical (Pirouette)
The atomic, committable package resulting from a successful Pirouette Debate. It comprises three mandatory components: 1) the materialized repository artifacts (new/modified modules, deprecation stubs), 2) the complete debate dossier (docket, persona briefs, final scorecard), and 3) the linking Git commit tag. A change set is considered ratified only after passing all CI/CD gates defined in INST-DEB-001.

## EFT-First Summary
Operationally, a Ratified Change Set is analogous to a governed Pull Request in a software repository. It packages a proposed code change (the module diff) with its full justification and validation data (the debate dossier), ensuring that every modification is atomic, audited, and passes automated quality gates before integration.

## Glossary Links
- See also: [Docket](<glossary_link_placeholder>), [Scorecard](<glossary_link_placeholder>), [Persona](<glossary_link_placeholder>)