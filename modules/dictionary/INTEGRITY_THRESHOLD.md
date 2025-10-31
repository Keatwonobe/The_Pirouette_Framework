---
term: "Integrity Threshold"
canonical_id: "INTEGRITY_THRESHOLD"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-020"]
---

---
term: Integrity Threshold
canonical_id: INTEGRITY_THRESHOLD
symbol: ΔK_max
aliases: [Dissonance Tolerance, Engagement Boundary]
parents: [DOMA-020]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-020
      lines: "§4"
      snippet: |
        Decide: Compare the Dissonance Index against a tunable Integrity Threshold.
  editors: [Agent]
  review_log: []
triad:
  art: |
    The gardener's wisdom to know which storms will break the saplings and which will merely water them. It is the line drawn by the self to preserve its own song against a chaotic chorus.
  law: |
    A system initiates Coherent Disengagement when an inbound signal's Dissonance Index (ΔK) meets or exceeds its Integrity Threshold (ΔK_max). The threshold is a tunable parameter representing the maximum coherence cost the system will risk for potential synthesis.
  philosophy: |
    The threshold operationalizes the Right to Coherence, transforming it from an abstract principle into a concrete decision boundary. It asserts that systemic health depends not on universal engagement, but on selective, energy-preserving discernment.
pirouette_definition: |
  The Integrity Threshold is a scalar, system-specific parameter representing the maximum tolerable Dissonance Index (ΔK) a system will accept from an inbound signal before initiating Coherent Disengagement. It serves as the decision boundary in the Sentry's Gambit, calibrated to balance the potential rewards of Resonant Synthesis against the risks of Coherence Erosion. A lower threshold indicates a more conservative, integrity-preserving posture, while a higher threshold indicates a greater willingness to engage with high-risk, potentially transformative signals.
operational_definition:
  units: Dimensionless (commensurate with Dissonance Index)
  symbol_table:
    - name: ΔK_max
      meaning: Maximum tolerable Dissonance Index
      dimensions: Dimensionless
      default_range: Contextual; often normalized to [0, 1]
  measurement:
    procedures:
      - name: Threshold Calibration via Systemic Response
        outline: |
          1. Expose the system to a calibrated set of signals with known Dissonance Indices (ΔK).
          2. Observe the system's response: successful synthesis, Coherence Fever, or an explicit disengagement event.
          3. The threshold is inferred as the ΔK value at which the system consistently chooses disengagement or exhibits net coherence loss upon forced engagement.
          4. This value is then set as the operational ΔK_max, subject to periodic review based on systemic goals and environmental hostility.
        expected_signals: [Coherence Fever onset, Disengagement events, Net Coherence (S_p) post-interaction]
        pitfalls: [Setting the threshold too low leads to isolation and `Coherence Atrophy`. Setting it too high leads to constant `Turbulent Flow` and integrity failure.]
context_windows:
  - module: DOMA-020
    excerpt: |
      The gambit is an operational sequence of discernment, calculation, and action.
      1. **Scan:** Observe the resonant signature (`Ki`) of the inbound system.
      2. **Calculate:** Compute or estimate the Dissonance Index (ΔK).
      3. **Decide:** Compare the Dissonance Index against a tunable **Integrity Threshold**.
  - module: DOMA-020
    excerpt: |
      A system is not born with perfect discernment. It learns. The calibration of this triage calculus is an autopoietic process. By controlled exposure to a spectrum of inputs—from harmonic to mildly dissonant to actively hostile—the system learns to more accurately predict the coherence cost of engagement. This is the process of a system learning the shape of its own health.
poetic_connections:
  motifs: [boundary, gate, shield, discernment, triage, filter]
  evocative_lines:
    - "the wisdom to know which dissonances are best left unsounded."
    - "It is the art of choosing the path that preserves the song."
  association_matrix:
    - [ "DISSONANCE_INDEX", 0.9 ]
    - [ "COHERENT_DISENGAGEMENT", 0.8 ]
    - [ "RIGHT_TO_COHERENCE", 0.7 ]
    - [ "SENTRY_S_GAMBIT", 0.9 ]
formal_mappings:
  candidates:
    - target: Activation threshold of an immune cell (e.g., T-cell)
      domain: Biology|Immunology
      mapping_kind: conceptual
      equation_hint: |
        Signal Strength (Affinity × Duration) ≥ Threshold  => Activation
      justification: |
        The system (immune system) is presented with a signal (antigen). It computes a 'dissonance' score (avidity/affinity of binding). If this signal exceeds a certain threshold, a major response (engagement) is triggered; otherwise, it is ignored (disengagement/anergy). The threshold is tunable through processes like central and peripheral tolerance.
      references:
        - title: Janeway's Immunobiology
          where: Chapter on T-Cell Activation
          date: 2016-01-01
      confidence: 0.9
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "A system with a properly calibrated Integrity Threshold will maintain or increase its net coherence over time more effectively than a system with a fixed, arbitrary threshold or no threshold at all."
      domain: phenomenology
      falsifier: "Demonstration of a system that thrives via indiscriminate engagement, consistently achieving net coherence gains from interactions with signals of arbitrarily high Dissonance Index. Alternatively, a system that successfully maintains coherence through total isolation without Coherence Atrophy."
      status: proposed
      links: [DOMA-020]
naming_notes:
  collisions: []
  disambiguation: |
    Distinguish from `Coherence Floor`, which is the minimum level of internal coherence required for a system to be considered viable. The Integrity Threshold is not a measure of the system's *current* state, but a *policy parameter* for deciding on *future* interactions.
crosslinks:
  near_synonyms: []
  antonyms: [UNIVERSAL_COUPLING_POSTURE]
  prerequisites: [DISSONANCE_INDEX, SYSTEMIC_COHERENCE]
  downstream_effects: [COHERENT_DISENGAGEMENT, RESONANT_SYNTHESIS]
license: CC-BY-SA-4.0
---

# Integrity Threshold

## Canonical (Pirouette)
The Integrity Threshold is a scalar, system-specific parameter representing the maximum tolerable Dissonance Index (ΔK) a system will accept from an inbound signal before initiating Coherent Disengagement. It serves as the decision boundary in the Sentry's Gambit, calibrated to balance the potential rewards of Resonant Synthesis against the risks of Coherence Erosion. A lower threshold indicates a more conservative, integrity-preserving posture, while a higher threshold indicates a greater willingness to engage with high-risk, potentially transformative signals.

## EFT-First Summary
Analogous to an activation threshold in immunology or statistical physics, the Integrity Threshold (ΔK_max) functions as a gate for interaction. A system will only expend resources to engage with an external signal if the signal's disruptive potential (measured by the Dissonance Index) is below this tunable barrier. This policy ensures that interactions are, on average, coherence-preserving, protecting the system's macroscopic state from destabilizing environmental inputs.

## Glossary Links
- See also: [Dissonance Index](<link>), [Coherent Disengagement](<link>), [Sentry's Gambit](<link>)