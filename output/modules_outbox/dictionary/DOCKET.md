---
term: "Docket"
canonical_id: "DOCKET"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-002_unifier_&_pirouette_debate_instrument"]
---

---
term: Docket
canonical_id: DOCKET
symbol: N/A
aliases: [Debate Request]
parents: [INST-DEB-001]
children: []
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DYNA-002_unifier_&_pirouette_debate_instrument
      lines: "INST-DEB-001 Sections 1, 2.2"
      snippet: |
        * **Docket:** A machine-readable request to run a debate over one or more modules.
        ```json
        {
          "inst_id": "INST-DEB-001",
          "intent": "MERGE",
          "inputs": ["CORE-003", "CORE-004"],
          "thesis": "Collapse duplicate Γ-derivations; adopt single T(x) formalism.",
          "constraints": {"no-new-symbols": true, "pin-ids": ["MATH-018"]},
          "personas": ["Formalist","Phenomenologist","Skeptic","Engineer","Archivist"],
          "rubric_weights": {"coherence":0.30,"parsimony":0.25,"predictivity":0.20,"refutability":0.15,"continuity":0.10},
          "budget": {"max_tokens": 80000, "max_cost_usd": 6.00},
          "ci": {"require_tests": true, "min_score": 0.70, "min_dimension": 0.60},
          "metadata": {"requester": "Keaton", "ts": "2025-10-11T00:00:00Z"}
        }
        ```
  editors: [Automated Agent, Keaton]
  review_log: []
triad:
  art: |
    A sealed letter to the future, demanding a duel of ideas. It is the formal glove thrown down, the writ that commands concepts to stand trial and prove their worthiness to remain.
  law: |
    A Docket is a versioned, machine-readable JSON object that specifies an intent (EXPAND, MERGE, REVISION), target modules, a thesis, constraints, and resources, thereby triggering a debate instance. Each valid Docket submitted to the instrument must yield exactly one of {ACCEPT, VETO, HUMAN_REVIEW}.
  philosophy: |
    To transform unstructured argument into governed, atomic, and auditable change. The Docket ensures that every modification to the framework is intentional, contested, and recorded, preventing conceptual drift and enabling safe, monotonic progress.
pirouette_definition: |
  A Docket is a machine-readable request, formatted as a versioned JSON object, that initiates a debate instance within the Pirouette framework. It specifies a change type (`intent`), input `modules`, a central `thesis` for the debate, operational `constraints` (e.g., `no-new-symbols`), a panel of `personas`, `rubric_weights` for scoring, and resource `budget` limitations. Its purpose is to convert a proposal for change into a fully-specified, automated, and governed process that yields a Ratified Change Set.
operational_definition:
  units: N/A (data structure)
  symbol_table:
    - name: intent
      meaning: The type of change requested {EXPAND, MERGE, REVISION}.
      dimensions: "enum"
      default_range: "contextual"
    - name: inputs
      meaning: An array of module IDs targeted by the debate.
      dimensions: "list[string]"
      default_range: "contextual"
    - name: thesis
      meaning: A concise, falsifiable statement motivating the change.
      dimensions: "string"
      default_range: "contextual"
    - name: constraints
      meaning: A key-value object of rules the debate and its outputs must follow.
      dimensions: "object"
      default_range: "contextual"
    - name: budget
      meaning: Resource limits (e.g., tokens, cost) for the debate execution.
      dimensions: "object"
      default_range: "contextual"
  measurement:
    procedures:
      - name: Docket Validation and Execution
        outline: |
          1. A JSON file matching the Docket schema is submitted to the `inst-deb run` CLI.
          2. The CLI validates the file against the canonical JSON schema defined in INST-DEB-001.
          3. If valid, the CLI parses the parameters to initiate the parallel persona briefing stage of the debate.
        expected_signals: [Successful run initiation (return code 0), Generation of debate dossier]
        pitfalls: [Schema validation failure (return code 2), Budget exceeded pre-flight check (return code 5), Missing input module files]
context_windows:
  - module: INST-DEB-001
    excerpt: |
      **Purpose.** Convert debate into *governed* change: each run must yield exactly one of {EXPAND, MERGE, REVISION}, with provenance, tests, and clean diffs.
      **Scope.** Applies to all modules... This document defines schemas, prompts, scoring, CI gates, and CLI for fully automated operation with human veto points.
  - module: INST-DEB-001
    excerpt: |
      [NEW_DOCKET] → [BRIEFS_PARALLEL] → [CROSS_EXAM] → [SYNTHESIS_DRAFT]
      → [SCORING_GATE] → {ACCEPT → MATERIALIZE → CI_TESTS → PR}
                         {VETO → ARCHIVE}
                         {HUMAN_REVIEW → QUEUE}
poetic_connections:
  motifs: [governance, initiation, contest, summons, trial, writ]
  evocative_lines:
    - "Convert debate into *governed* change."
    - "A machine-readable request to run a debate over one or more modules."
  association_matrix:
    - [ "PERSONA", 0.9 ]
    - [ "SCORECARD", 0.8 ]
    - [ "RATIFIED_CHANGE_SET", 0.7 ]
formal_mappings:
  candidates:
    - target: Pull Request / Merge Request
      domain: Software Engineering
      mapping_kind: conceptual
      justification: |
        Both initiate a formal process to change a codebase, require review (by personas vs. humans), and are gated by CI checks. The Docket is a structured precursor that *generates* the Pull Request artifact as its final output upon acceptance.
      references: []
      confidence: 0.9
    - target: API Request
      domain: Computer Science
      mapping_kind: operational
      justification: |
        A Docket is a structured data object sent to an endpoint (the debate instrument CLI) to trigger a deterministic, state-changing computational process. Its schema functions as the API contract for the debate service.
      references: []
      confidence: 0.8
    - target: Writ of Certiorari
      domain: Law
      mapping_kind: conceptual
      justification: |
        It is a formal request for a higher authority (the debate panel) to review a specific issue (the thesis) and render a binding judgment. It establishes the scope and terms of the review, compelling a structured response.
      references: []
      confidence: 0.6
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "A valid Docket, when processed by INST-DEB-001, will always result in one of three final states: ACCEPT, VETO, or HUMAN_REVIEW."
      domain: phenomenology
      falsifier: "An execution run that hangs indefinitely, produces an ambiguous state, or fails to create an auditable artifact in the repository."
      status: proposed
      links: [INST-DEB-001]
    - statement: "The `constraints` field within a Docket, such as `no-new-symbols`, is binding on all persona outputs and the final synthesized module."
      domain: theory
      falsifier: "A synthesized module from a constrained run introduces new symbols, and the CI gate fails to block the change."
      status: under-test
      links: [INST-DEB-001]
naming_notes:
  collisions: [Legal docket (a calendar of court cases or a summary of a case)]
  disambiguation: |
    In Pirouette, a Docket is not a log of events but the *initiating request* for a single, atomic debate. It is the input specification, not the output record (which is the debate dossier and Scorecard).
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [MODULE, PERSONA]
  downstream_effects: [PERSONA_BRIEF, SCORECARD, RATIFIED_CHANGE_SET]
license: CC-BY-SA-4.0
---

# Docket

## Canonical (Pirouette)
A Docket is a machine-readable request, formatted as a versioned JSON object, that initiates a debate instance within the Pirouette framework. It specifies a change type (`intent`), input `modules`, a central `thesis` for the debate, operational `constraints` (e.g., `no-new-symbols`), a panel of `personas`, `rubric_weights` for scoring, and resource `budget` limitations. Its purpose is to convert a proposal for change into a fully-specified, automated, and governed process that yields a Ratified Change Set.

## EFT-First Summary
The Docket operationalizes theory development by framing proposed changes as precise, falsifiable requests. Analogous to submitting a specific model Lagrangian to a computational pipeline for constraint analysis, a Docket packages a thesis (e.g., "Collapse duplicate Γ-derivations") and constraints (e.g., "no-new-symbols") for automated evaluation against specified criteria (e.g., `coherence`, `parsimony`). This enforces a rigorous, auditable workflow for extending or simplifying the framework's formal structure.

## Glossary Links
- See also: Persona, Scorecard, Ratified Change Set