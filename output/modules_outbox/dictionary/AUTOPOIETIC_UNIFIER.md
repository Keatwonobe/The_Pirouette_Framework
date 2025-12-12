---
term: "Autopoietic Unifier"
canonical_id: "AUTOPOIETIC_UNIFIER"
symbol: ""
aliases: [Pirouette Debate Instrument]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-002_unifier_&_pirouette_debate_instrument"]
---

---
term: Autopoietic Unifier
canonical_id: AUTOPOIETIC_UNIFIER
symbol: N/A
aliases: [Pirouette Debate Instrument]
parents: [DYNA-002]
children: [CORE-*, DOMA-*, DYNA-*, MATH-*, INST-*, XXP-*, TLE-*, PDM-*]
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DYNA-002_unifier_&_pirouette_debate_instrument
      lines: "Section 0"
      snippet: |
        **Purpose.** Convert debate into *governed* change: each run must yield exactly one of {EXPAND, MERGE, REVISION}, with provenance, tests, and clean diffs.
        **Scope.** Applies to all modules (CORE/DOMA/DYNA/MATH/INST/XXP/TLE/PDM). This document defines schemas, prompts, scoring, CI gates, and CLI for fully automated operation with human veto points.
  editors: [Keaton (PDM-000 custodian)]
  review_log: []
triad:
  art: |
    A parliament of synthetic minds, convened in silicon, argues towards unity. From structured dissent, a single, coherent truth is forged and committed to the archive.
  law: |
    Every debate, initiated by a machine-readable Docket, must terminate in exactly one of three states: EXPAND (a new module), MERGE (a unified module), or REVISION (an improved module). The outcome must pass all automated CI gates and be accompanied by a complete dossier of its own creation.
  philosophy: |
    To ensure the Pirouette Framework evolves with rigor and not just momentum. It replaces subjective authority with a transparent, adversarial, and auditable process, turning intellectual conflict into a generative engine for a more robust and parsimonious system.
pirouette_definition: |
  An automated system using structured, API-driven debate between specialized AI personas (e.g., Formalist, Skeptic, Engineer) to generate, score, and ratify atomic repository changes. Each debate is initiated by a machine-readable Docket and concludes with a versioned, test-backed, and fully auditable Change Set, corresponding to one of three valid moves: EXPAND, MERGE, or REVISION. The Instrument enforces governance through explicit schemas, scoring rubrics, CI gates, and budget controls.
operational_definition:
  units: Process outcomes (commits, pull requests, test results)
  symbol_table:
    - name: Docket
      meaning: A machine-readable request to run a debate over one or more modules.
      dimensions: data structure (JSON)
      default_range: N/A
    - name: Scorecard
      meaning: A structured summary of persona and panel-level rubric scores and the final verdict.
      dimensions: data structure (JSON)
      default_range: N/A
  measurement:
    procedures:
      - name: Instrument Acceptance Test Suite (INST-DEB-001 §12)
        outline: |
          1. **Schema Roundtrip:** Verify a Docket can proceed through Briefs and Scoring to generate a valid, unedited Pull Request.
          2. **Merge Hygiene:** Execute a MERGE operation and verify `replaces`/`replaced_by` chains are consistent and no dangling pointers exist.
          3. **Veto Logic:** Force a low `refutability` score and confirm the engine correctly routes to `human_review` instead of `accept`.
          4. **Budget Guard:** Submit a Docket with an insufficient token budget and confirm the process halts pre-synthesis with the correct error code.
          5. **Test Binding:** Introduce a failing `XXP` test referenced in a module revision and confirm the CI blocks the module's transition to `stable` status.
        expected_signals: [Passing CI checks, valid PRs, correct state transitions, expected error codes]
        pitfalls: [Non-deterministic LLM outputs requiring prompt/temperature tuning, schema drift between components, budget overruns from complex dockets]
context_windows:
  - module: DYNA-002_unifier_&_pirouette_debate_instrument
    excerpt: |
      **Purpose.** Convert debate into *governed* change: each run must yield exactly one of {EXPAND, MERGE, REVISION}, with provenance, tests, and clean diffs.
      **Scope.** Applies to all modules (CORE/DOMA/DYNA/MATH/INST/XXP/TLE/PDM). This document defines schemas, prompts, scoring, CI gates, and CLI for fully automated operation with human veto points.
  - module: DYNA-002_unifier_&_pirouette_debate_instrument
    excerpt: |
      **Orchestration & State Machine**
      ```
      [NEW_DOCKET] → [BRIEFS_PARALLEL] → [CROSS_EXAM] → [SYNTHESIS_DRAFT]
      → [SCORING_GATE] → {ACCEPT → MATERIALIZE → CI_TESTS → PR}
                         {VETO → ARCHIVE}
                         {HUMAN_REVIEW → QUEUE}
      ```
      **Panel vote weights (sum=1.0):** Skeptic 0.30, Formalist 0.25, Phenomenologist 0.20, Engineer 0.15, Archivist 0.10.
poetic_connections:
  motifs: [governed dialectic, synthetic reason, computational jurisprudence, adversarial collaboration]
  evocative_lines:
    - "Convert debate into *governed* change."
    - "Expose hidden assumptions; provide counterexample or veto."
    - "Each run must yield exactly one of {EXPAND, MERGE, REVISION}."
  association_matrix:
    - [ "GOVERNANCE", 0.9 ]
    - [ "COHERENCE", 0.8 ]
    - [ "REFUTABILITY", 0.7 ]
    - [ "AUTOMATION", 0.9 ]
formal_mappings:
  candidates:
    - target: Multi-Agent System (MAS)
      domain: Computer Science
      mapping_kind: operational
      equation_hint: N/A
      justification: |
        The system is a classic MAS where autonomous agents (Personas) with distinct goals (Constitutions) interact according to predefined protocols (Orchestration) to solve a complex problem (repository unification). The panel scoring and synthesis steps represent a form of agent coordination and consensus-building.
      references:
        - title: Multi-Agent Systems: A Modern Approach to Distributed Artificial Intelligence
          where: Weiss, G. (ed.), MIT Press
          date: 1999-01-01
      confidence: 0.9
    - target: Constitutional AI
      domain: AI Safety
      mapping_kind: conceptual
      justification: |
        Each AI Persona operates under a fixed "Constitution" (its charter) that bounds its behavior. The overall system's rules (scoring, CI gates) act as a meta-constitution to ensure outputs are safe, hygienic, and aligned with the framework's goals, analogous to the principles of Constitutional AI.
      references:
        - title: Constitutional AI: Harmlessness from AI Feedback
          where: arXiv:2212.08073
          date: 2022-12-15
      confidence: 0.7
  adopted:
    - target: Multi-Agent System for Automated Governance
      rationale: This mapping is the most operationally precise. It captures the multi-persona architecture, the automated workflow, and the explicit goal of governing the evolution of a complex information system.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The Unifier process produces changes with higher coherence and fewer regressions than unaided human edits."
      domain: phenomenology
      falsifier: "A controlled trial where a human red-team, given the same dockets, produces repository changes that score higher on coherence metrics and introduce fewer breaking changes (as measured by the test suite) than the automated instrument."
      status: proposed
      links: [INST-DEB-001]
naming_notes:
  collisions: []
  disambiguation: |
    "Autopoietic Unifier" refers to the system's conceptual role: an engine that self-creates and maintains the coherence of the Pirouette Framework. "Pirouette Debate Instrument" is its operational name, describing its concrete implementation as a structured debate mechanism (INST-DEB-001). The terms are used interchangeably.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [GEOMETRY_OF_DEBATE]
  downstream_effects: [REPOSITORY_COHERENCE, MODULE_VERSIONING]
license: CC-BY-SA-4.0
---

# Autopoietic Unifier

## Canonical (Pirouette)
An automated system using structured, API-driven debate between specialized AI personas (e.g., Formalist, Skeptic, Engineer) to generate, score, and ratify atomic repository changes. Each debate is initiated by a machine-readable Docket and concludes with a versioned, test-backed, and fully auditable Change Set, corresponding to one of three valid moves: EXPAND, MERGE, or REVISION. The Instrument enforces governance through explicit schemas, scoring rubrics, CI gates, and budget controls.

## EFT-First Summary
The Autopoietic Unifier is a **Multi-Agent System for Automated Governance**. It operationalizes repository maintenance by deploying several AI agents, each with a specific charter (e.g., logical formalism, empirical skepticism), to collaboratively propose and critique changes. This adversarial process, governed by a meta-level ruleset, automates the generation of coherent, well-tested updates to the theoretical framework, mirroring distributed problem-solving architectures in computer science.

## Glossary Links
- See also: GEOMETRY_OF_DEBATE, REPOSITORY_COHERENCE