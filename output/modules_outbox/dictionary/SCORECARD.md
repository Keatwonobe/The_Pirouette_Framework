---
term: "Scorecard"
canonical_id: "SCORECARD"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-002_unifier_&_pirouette_debate_instrument"]
---

---
term: Scorecard
canonical_id: SCORECARD
symbol: 
aliases: [Synthesis scorecard]
parents: [INST-DEB-001]
children: []
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: INST-DEB-001
      lines: "L21, L74-83"
      snippet: |
        * **Scorecard:** Persona- and panel-level rubric values plus accept/veto recommendation.
  editors: [Lexicon Agent]
  review_log: []
triad:
  art: |
    The final, crystallized judgment of the panel; a polyphony of reasoned voices collapsed into a single, actionable verdict.
  law: |
    A scorecard must contain a final decision of {accept, veto, human_review}, mean panel scores, and dimensional scores. An `accept` verdict requires a `scores_mean` ≥ 0.70 and all `scores_dim` values ≥ 0.60.
  philosophy: |
    To convert subjective, multi-faceted debate into a discrete, auditable, and automated governance action. The scorecard is the instrument that bridges the semantic gap between argumentation and repository state change, ensuring that all modifications are justified by a transparent, weighted consensus.
pirouette_definition: |
  A data structure summarizing the outcome of a Pirouette Debate. It aggregates the rubric scores and verdicts from individual personas into a final panel-level decision (`accept`, `veto`, `human_review`). It includes the mean and dimensional scores, supporting evidence, repository diff statistics, and provenance linking it to the specific debate run and resulting commit.
operational_definition:
  units: Dimensionless data structure
  symbol_table:
    - name: decision
      meaning: The final verdict from the panel, one of {accept, veto, human_review}.
      dimensions: dimensionless
      default_range: N/A
    - name: scores_mean
      meaning: The weighted average score from the panel across all rubric dimensions.
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: scores_dim
      meaning: A vector of weighted average scores, one for each rubric dimension (e.g., coherence, parsimony).
      dimensions: dimensionless
      default_range: "[0, 1] per dimension"
    - name: evidence
      meaning: A list of concrete, verifiable pieces of evidence supporting the verdict, typically test IDs or key observations.
      dimensions: dimensionless
      default_range: N/A
  measurement:
    procedures:
      - name: Panel Synthesis and Scoring
        outline: |
          1. Collect individual persona briefs (JSON schema 2.3) from all panel members.
          2. Apply panel vote weights (e.g., Skeptic 0.30, Formalist 0.25) to individual persona rubric scores.
          3. Compute the weighted mean of all scores (`scores_mean`).
          4. Compute the weighted mean for each rubric dimension (`scores_dim`).
          5. Compare scores against CI thresholds (`min_score`, `min_dimension`) to generate the final `decision`.
          6. Synthesize `evidence` field from persona `tests` and `notes`.
        expected_signals: [A valid JSON object matching schema INST-DEB-001 §2.4]
        pitfalls: [Incomplete persona briefs leading to skewed weights, Misconfiguration of CI thresholds leading to invalid verdicts]
context_windows:
  - module: INST-DEB-001
    excerpt: |
      ```
      {
        "decision": "accept|veto|human_review",
        "scores_mean": 0.78,
        "scores_dim": {"coherence":0.84,"parsimony":0.76,"predictivity":0.72,"refutability":0.70,"continuity":0.86},
        "evidence": ["a_e via XXP-012","Boltzmann hook retained"],
        "provenance": {"run_id":"debate/merge/core-003_004/2025-10-11","commit":"<git-hash>"}
      }
      ```
  - module: INST-DEB-001
    excerpt: |
      CI/CD Gates: ... Provenance: `debate.json` and `scorecard.json` included in PR.
poetic_connections:
  motifs: [Judgment, Consensus, Verdict, Record, Audit Trail]
  evocative_lines:
    - "Convert debate into *governed* change."
    - "The final word, cast in JSON."
  association_matrix:
    - [ "DOCKET", 0.8 ]
    - [ "PERSONA", 0.9 ]
    - [ "RATIFIED_CHANGE_SET", 0.7 ]
formal_mappings:
  candidates: []
  adopted:
    - target: CI/CD Quality Gate Summary
      domain: Software Engineering
      mapping_kind: operational
      justification: |
        The Scorecard functions as a quality gate, where rubric scores are checks that must pass before an automated action (`MATERIALIZE`) is triggered. This is identical to how test results, security scans, or linting reports gate a software merge in a CI/CD pipeline.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "A Scorecard with `decision: accept` is sufficient to trigger the automated `MATERIALIZE` step."
      domain: phenomenology
      falsifier: "Observing a debate run that produces a Scorecard with `decision: accept` but fails to proceed to the `MATERIALIZE` state without a documented error or manual intervention."
      status: proposed
      links: [INST-DEB-001]
naming_notes:
  collisions: [Balanced Scorecard (business), Credit Score (finance)]
  disambiguation: |
    Within Pirouette, always refers to the JSON artifact (schema INST-DEB-001 §2.4) produced at the end of a debate. Distinguish from individual `Persona` scores, which are inputs to the final Scorecard.
crosslinks:
  near_synonyms: []
  antonyms: [DOCKET]
  prerequisites: [DOCKET, PERSONA_BRIEF]
  downstream_effects: [RATIFIED_CHANGE_SET, MATERIALIZE]
license: CC-BY-SA-4.0
---

# Scorecard

## Canonical (Pirouette)
A data structure summarizing the outcome of a Pirouette Debate. It aggregates the rubric scores and verdicts from individual personas into a final panel-level decision (`accept`, `veto`, `human_review`). It includes the mean and dimensional scores, supporting evidence, repository diff statistics, and provenance linking it to the specific debate run and resulting commit.

## Operational Summary
The Scorecard is the Pirouette Framework's operational analog to a CI/CD Quality Gate Summary. It translates the qualitative outputs of a multi-agent debate into a quantitative, machine-readable verdict that determines whether a proposed change to the framework's modules is accepted and merged. Its structure ensures that every change is justified by explicit, weighted criteria before any automated repository actions are taken.

## Glossary Links
- See also: [Docket](<link-to-docket>), [Persona](<link-to-persona>), [Ratified Change Set](<link-to-ratified-change-set>)