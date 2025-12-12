---
term: "Rubric"
canonical_id: "RUBRIC"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-002_unifier_&_pirouette_debate_instrument"]
---

---
term: Rubric
canonical_id: RUBRIC
symbol: N/A
aliases: [Scorecard Criteria, Evaluation Criteria, Debate Virtues]
parents: [INST-DEB-001]
children: []
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: INST-DEB-001
      lines: "L63-L63"
      snippet: |
        "rubric_weights": {"coherence":0.30,"parsimony":0.25,"predictivity":0.20,"refutability":0.15,"continuity":0.10}
  editors: [Keaton, Automated Dictionary Agent]
  review_log: []
triad:
  art: |
    The constitution of reason, a set of virtues guiding change not by force but by balance. It is the compass that keeps the framework true to its own principles of clarity, parsimony, and predictive power.
  law: |
    Every proposed change set must be evaluated against a predefined, weighted rubric. The mean score must exceed a minimum threshold (e.g., 0.70) and no single dimension score may fall below a minimum value (e.g., 0.60) for automated acceptance.
  philosophy: |
    To replace subjective preference with auditable reason. The rubric objectifies the framework's values, ensuring that evolution is driven by measurable improvements in coherence and testability, not by whim or the loudest voice.
pirouette_definition: |
  The set of weighted criteria used by debate Personas to evaluate a proposed change to the Pirouette Framework. A Rubric is defined within a Docket and typically includes dimensions such as coherence, parsimony, predictivity, refutability, and continuity. Each criterion is assigned a weight (summing to 1.0) that determines its influence on the final acceptance score.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: Coherence
      meaning: Internal logical consistency, absence of contradiction, and clear symbolic dependencies.
      dimensions: dimensionless
      default_range: "[0.0, 1.0]"
    - name: Parsimony
      meaning: Simplicity in formalism; minimizing symbols, assumptions, and conceptual overhead (Ockham's Razor).
      dimensions: dimensionless
      default_range: "[0.0, 1.0]"
    - name: Predictivity
      meaning: The capacity of the change to generate new, non-trivial, and testable claims.
      dimensions: dimensionless
      default_range: "[0.0, 1.0]"
    - name: Refutability
      meaning: The clarity of falsification conditions; the ease of designing an experiment or derivation that could disprove the change.
      dimensions: dimensionless
      default_range: "[0.0, 1.0]"
    - name: Continuity
      meaning: Smooth integration with the existing framework; minimizing breaking changes and preserving established lineage.
      dimensions: dimensionless
      default_range: "[0.0, 1.0]"
  measurement:
    procedures:
      - name: Persona Scoring
        outline: |
          During a debate, each Persona evaluates the proposed change against the rubric criteria, assigning a score from 0.0 to 1.0 for each dimension based on its constitution and deliverables. A rationale must be provided for each score. The final score for a change is a weighted average across all personas and dimensions.
        expected_signals: [JSON object (Persona brief, schema 2.3) from each Persona, Aggregated JSON object (Synthesis scorecard, schema 2.4)]
        pitfalls: [Subjective scoring drift, Personas hallucinating justifications for scores, Misinterpretation of a criterion's meaning]
context_windows:
  # Short, trimmed context quotes harvested from modules (3–6 sentences each).
  - module: INST-DEB-001
    excerpt: |
      "intent": "MERGE",               
      "inputs": ["CORE-003", "CORE-004"],
      "thesis": "Collapse duplicate Γ-derivations; adopt single T(x) formalism.",
      "personas": ["Formalist","Phenomenologist","Skeptic","Engineer","Archivist"],
      "rubric_weights": {"coherence":0.30,"parsimony":0.25,"predictivity":0.20,"refutability":0.15,"continuity":0.10},
      "ci": {"require_tests": true, "min_score": 0.70, "min_dimension": 0.60}
  - module: INST-DEB-001
    excerpt: |
      "persona": "Formalist",
      "tests": ["XXP-012 recovers a_e within δ", "XXP-015 preserves COSMO-Γ HALO fits"],
      "scores": {"coherence":0.86,"parsimony":0.78,"predictivity":0.73,"refutability":0.69,"continuity":0.82},
      "verdict": "accept",
      "notes": "EL form provided; no new symbols introduced"
poetic_connections:
  # Lightweight "word-association graph" and sticky lines.
  motifs: [balance, judgment, governance, virtue, compass]
  evocative_lines:
    - "Convert debate into *governed* change."
    - "Expose hidden assumptions; provide counterexample or veto."
  association_matrix:
    # symmetric or directed; weights in [0,1]
    - [ "DOCKET", 0.9 ]
    - [ "PERSONA", 0.8 ]
    - [ "SCORECARD", 0.8 ]
    - [ "SKEPTIC", 0.7 ]
formal_mappings:
  # Candidate alignments to EFT/SM/CM/GR terms, each with justification and refs.
  candidates:
    - target: Loss Function / Objective Function
      domain: Machine Learning
      mapping_kind: conceptual
      equation_hint: |
        Score = Σ w_i * c_i
      justification: |
        The rubric acts as an objective function to be maximized by the synthesis process, guiding it toward desirable states of the repository. The weights `w_i` and criteria scores `c_i` directly define the landscape of preferred outcomes.
      references: []
      confidence: 0.7
  adopted:
    - target: Multi-Criteria Decision Analysis (MCDA)
      rationale: |
        The Pirouette Rubric is a direct implementation of MCDA, where alternatives (proposed changes) are scored against weighted criteria to calculate a utility score for ranking and selection. This is the most precise formal analog.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "A change accepted via a rubric with high scores in coherence and parsimony will result in a smaller, more logically consistent repository state."
      domain: phenomenology
      falsifier: "A series of accepted, high-score changes leads to an increase in repository complexity (e.g., line count, symbol count) without a corresponding increase in predictive power or test coverage."
      status: proposed
      links: [INST-DEB-001]
naming_notes:
  collisions: [Commonly used in education for grading assignments.]
  disambiguation: |
    In Pirouette, a Rubric is not for grading student work but is a machine-readable set of weighted virtues used for automated governance of framework changes. It is the 'objective function' for the debate process, not a subjective evaluation guide.
crosslinks:
  near_synonyms: []
  antonyms: [SUBJECTIVE_PREFERENCE, ARBITRARY_CHANGE]
  prerequisites: [DOCKET, PERSONA]
  downstream_effects: [SCORECARD, RATIFIED_CHANGE_SET]
license: CC-BY-SA-4.0
---

# Rubric

## Canonical (Pirouette)
The set of weighted criteria used by debate Personas to evaluate a proposed change to the Pirouette Framework. A Rubric is defined within a Docket and typically includes dimensions such as coherence, parsimony, predictivity, refutability, and continuity. Each criterion is assigned a weight (summing to 1.0) that determines its influence on the final acceptance score.

## Formal Mappings Summary
The Pirouette Rubric is an operational implementation of Multi-Criteria Decision Analysis (MCDA), where proposed changes are treated as alternatives evaluated against a weighted utility function. The criteria (coherence, parsimony, etc.) serve as the utility dimensions, ensuring that repository evolution maximizes a defined set of intellectual virtues.

## Glossary Links
- See also: DOCKET, PERSONA, SCORECARD