---
term: "Materialization"
canonical_id: "MATERIALIZATION"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-002_unifier_&_pirouette_debate_instrument"]
---

---
term: Materialization
canonical_id: MATERIALIZATION
symbol: ⚙️
aliases: [Artifact Generation, Repo Materialization]
parents: [INST-DEB-001]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DYNA-002_unifier_&_pirouette_debate_instrument
      lines: "Section 6"
      snippet: |
        ## 6) Materialization Rules (the three moves)
        ### 6.1 EXPAND
        * Create new module `NEW-<series>-<id>` with `status: draft` and required `tests` section.
        * Add to `/new/` staging; CI prevents `stable` until tests bound and passing.
  editors: [Pirouette Definer Agent]
  review_log: []
triad:
  art: |
    From the friction of minds, a new world is etched into the stone of the repository. Ideas become artifacts, arguments become architecture, and the outcome of debate is made solid.
  law: |
    An accepted debate scorecard (mean score ≥ 0.70, no dimension < 0.60) must be converted into a single, atomic commit containing all repository artifacts (new modules, deprecation stubs, changelogs) and a complete debate dossier, executable via the `inst-deb materialize` command.
  philosophy: |
    To ensure that all changes to the Pirouette framework are the result of structured, transparent, and falsifiable debate. This process prevents arbitrary evolution and creates an immutable, self-documenting record of conceptual progress, converting abstract agreement into concrete, testable reality.
pirouette_definition: |
  The automated process that converts the accepted outcome of a structured debate (INST-DEB-001) into a `Ratified Change Set` of repository artifacts. Materialization executes one of three specific, rule-bound moves—EXPAND, MERGE, or REVISION—to create, modify, or deprecate modules. The entire operation is triggered by a valid Synthesis Scorecard and is subject to automated CI/CD gates that verify schema correctness, linkage, and test binding before a change can be committed.
operational_definition:
  units: Atomic Git Commits
  symbol_table:
    - name: Synthesis Scorecard
      meaning: A machine-readable JSON object (schema 2.4) that contains the debate's final decision, scores, and a digest of the proposed changes. Serves as the primary input.
      dimensions: dimensionless
      default_range: N/A
    - name: Ratified Change Set
      meaning: The complete collection of materialized artifacts, including new or modified module files, deprecation stubs for replaced modules, updated tables of contents, and the debate dossier. Serves as the primary output.
      dimensions: dimensionless
      default_range: N/A
  measurement:
    procedures:
      - name: Command-Line Invocation
        outline: |
          1. Invoke `inst-deb materialize --scorecard <path-to-scorecard.json>`.
          2. The tool parses the scorecard to determine the change type (EXPAND, MERGE, or REVISION).
          3. Based on the type, it executes file operations: creating new module files in `/staging/`, writing deprecation stubs into old files, or generating a semantic diff for a revision.
          4. All generated files, plus the debate dossier, are placed on a new Git branch named `debate/<intent>/<ids>/<YYYYMMDD>`.
          5. A pull request is automatically opened for human review and CI/CD processing.
        expected_signals: [A Git branch with clean diffs, A new pull request, A passing CI check (return code 0)]
        pitfalls: [Schema validation failure in scorecard.json, Git merge conflicts if base modules have changed, CI test binding failure]
context_windows:
  - module: DYNA-002_unifier_&_pirouette_debate_instrument
    excerpt: |
      [NEW_DOCKET] → [BRIEFS_PARALLEL] → [CROSS_EXAM] → [SYNTHESIS_DRAFT]
      → [SCORING_GATE] → {ACCEPT → MATERIALIZE → CI_TESTS → PR}
                         {VETO → ARCHIVE}
                         {HUMAN_REVIEW → QUEUE}
  - module: DYNA-002_unifier_&_pirouette_debate_instrument
    excerpt: |
      ### 6.2 MERGE
      * Produce successor module with `replaces: [A,B,…]`.
      * Write deprecation stubs into A,B with `replaced_by: [SuccessorID]` and short rationale.
      * One PR contains successor + stubs + ToC update.
poetic_connections:
  motifs: [crystallization, inscription, scaffolding, closure, embodiment]
  evocative_lines:
    - "Convert debate into *governed* change."
    - "each run must yield exactly one of {EXPAND, MERGE, REVISION}"
  association_matrix:
    - [ "DEBATE", 0.9 ]
    - [ "RATIFIED_CHANGE_SET", 0.9 ]
    - [ "CI_GATE", 0.7 ]
    - [ "VETO", 0.5 ]
formal_mappings:
  candidates:
    - target: GitOps Pipeline
      domain: Software Engineering
      mapping_kind: operational
      equation_hint: |
        `scorecard.json → inst-deb materialize → git commit`
      justification: |
        Materialization is a GitOps pattern where a declarative configuration file (the Synthesis Scorecard) is the source of truth. An automated operator (`inst-deb`) reconciles the state of the repository with the desired state declared in the configuration, ensuring changes are atomic, versioned, and auditable.
      references:
        - title: Guide To GitOps
          where: https://www.gitops.tech/
          date: 2017-08-01
      confidence: 0.95
  adopted:
    - target: GitOps Pipeline
      rationale: The mapping is direct and operational. The process is declarative, automated, and repository-centric, matching the core tenets of GitOps.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The `inst-deb materialize` process for a MERGE action always produces one successor module and deprecation stubs for all replaced modules within a single atomic commit."
      domain: phenomenology
      falsifier: "Observe a MERGE-labeled commit that either fails to create a successor, fails to deprecate a parent, or splits these actions across multiple non-atomic commits."
      status: proposed
      links: [INST-DEB-001]
    - statement: "A scorecard with a `decision: accept` will never be materialized if any CI gate (e.g., test binding, schema check) fails."
      domain: phenomenology
      falsifier: "Find a ratified change set in the main branch whose corresponding debate dossier shows a CI failure that was bypassed."
      status: proposed
      links: [INST-DEB-001]
naming_notes:
  collisions: ["Materialized View (Databases)"]
  disambiguation: |
    In Pirouette, Materialization refers to the creation of concrete, version-controlled text files (modules, stubs) in a code repository. This is distinct from the database concept of a "materialized view," which is a pre-computed query result stored as a physical table.
crosslinks:
  near_synonyms: [ARTIFACT_GENERATION]
  antonyms: [VETO]
  prerequisites: [DEBATE, ACCEPTED_SCORECARD]
  downstream_effects: [RATIFIED_CHANGE_SET, CI_TESTS]
license: CC-BY-SA-4.0
---

# Materialization

## Canonical (Pirouette)
The automated process that converts the accepted outcome of a structured debate (INST-DEB-001) into a `Ratified Change Set` of repository artifacts. Materialization executes one of three specific, rule-bound moves—EXPAND, MERGE, or REVISION—to create, modify, or deprecate modules. The entire operation is triggered by a valid Synthesis Scorecard and is subject to automated CI/CD gates that verify schema correctness, linkage, and test binding before a change can be committed.

## Software Engineering Analogy
Materialization is an operational implementation of a **GitOps Pipeline**. A declarative file (the `scorecard.json` from a debate) serves as the single source of truth for a desired change. An automated tool (`inst-deb materialize`) acts as the operator, reconciling the repository's state to match the declaration in a single, atomic, and auditable Git commit. This ensures all framework evolution is governed, testable, and version-controlled.

## Glossary Links
- See also: DEBATE, CI_GATE, RATIFIED_CHANGE_SET