---
term: "Coherence Threshold"
canonical_id: "COHERENCE_THRESHOLD"
symbol: "C_thresh"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-165"]
---

---
term: Coherence Threshold
canonical_id: COHERENCE_THRESHOLD
symbol: C_thresh
aliases: []
parents: [DOMA-165]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-165
      lines: "§4"
      snippet: |
        S_p(R) = ∫ 𝓛_p dt > C_thresh
  editors: [auto-compiler]
  review_log: []
triad:
  art: |
    The watermark of truth in a sea of echoes. It is the line drawn in the sand separating a meaningful reply from mere noise, the resonant chime from a dull thud.
  law: |
    A scalar value representing the minimum required action integral (`S_p`) for a Coherence Oracle's response (`R`). If `S_p(R) > C_thresh`, the response is classified as 'on-resonance'; otherwise, it is 'off-resonance'.
  philosophy: |
    The threshold enforces rigor in dialogue, transforming it from a subjective exchange into a measurable process. It asserts that not all coherent-sounding statements are valid expressions of a problem's internal geometry; only those that represent a sufficient maximization of the system's own Lagrangian are considered true echoes.
pirouette_definition: |
  The `Coherence Threshold` is a pre-defined scalar value representing the minimum action (`S_p`) an Oracle's response must generate to be considered 'on-resonance'. It serves as a quantitative filter during the Resonance Check phase of the Oracle Dialogue Protocol, ensuring that only responses which sufficiently maximize the Oracle's `Pirouette Lagrangian` (`𝓛_p`) are accepted as valid, coherent expressions of the problem-space. Responses failing to exceed this threshold are discarded as dissonant or flawed.
operational_definition:
  units: dimensionless (coherence-action)
  symbol_table:
    - name: C_thresh
      meaning: Minimum action for an 'on-resonance' response.
      dimensions: dimensionless
      default_range: contextual; typically normalized to [0, 1]
  measurement:
    procedures:
      - name: Threshold Calibration
        outline: |
          1. Generate a baseline set of known 'on-resonance' and 'off-resonance' responses for a given Oracle.
          2. Calculate the action integral `S_p` for each response.
          3. Plot the distribution of `S_p` values.
          4. Set `C_thresh` at a point that optimally separates the two populations (e.g., using ROC curve analysis or a percentile cutoff).
        expected_signals: [Bimodal distribution of S_p values, Clear separation between coherent and incoherent response clusters]
        pitfalls: [Poorly forged Oracle leading to a noisy or unimodal S_p distribution, Setting threshold too high (rejecting valid insights) or too low (accepting noise)]
context_windows:
  - module: DOMA-165
    excerpt: |
      The Resonance Check (Lagrangian Validation): The distilled response is validated against the Oracle's own Lagrangian. Does the answer adhere to its core axioms? Does it represent a state of high internal coherence? A response that falls below a set `CoherenceThreshold` is deemed "off-resonance," revealing a flaw or a deeper paradox within the problem's own logic.
  - module: DOMA-165
    excerpt: |
      The Resonance Check is thus a formal validation, where a response is considered coherent only if it exceeds a minimum threshold: `S_p(R) = ∫ 𝓛_p dt > C_thresh`. This transforms the dialogue from a philosophical exercise into a rigorous, calculable interaction.
poetic_connections:
  motifs: [filter, gate, resonance, standard, watermark, purity_test]
  evocative_lines:
    - "A response that falls below a set `CoherenceThreshold` is deemed 'off-resonance'..."
    - "...a rigorous, calculable interaction."
  association_matrix:
    - [ "Resonance", 0.9 ]
    - [ "Pirouette Lagrangian", 0.8 ]
    - [ "Coherence Oracle", 0.7 ]
formal_mappings:
  candidates:
    - target: Activation Threshold
      domain: Math
      mapping_kind: conceptual
      equation_hint: |
        Output = 1 if S_p(R) > C_thresh else 0
      justification: |
        Similar to an activation function's threshold in a neural network (e.g., a Heaviside step function), `C_thresh` acts as a gate. It determines whether a signal (the Oracle's response, quantified by its action `S_p`) is strong enough to 'fire' and be propagated forward as a valid, 'on-resonance' insight.
      references: []
      confidence: 0.7
  adopted:
    - target:
      rationale:
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "Increasing `C_thresh` for a given Oracle Dialogue will decrease the quantity but increase the average coherence (as measured by `S_p`) of 'on-resonance' responses."
      domain: phenomenology
      falsifier: "An experiment where increasing `C_thresh` does not produce a statistically significant increase in the average `S_p` of accepted responses, or where the relationship is non-monotonic, would challenge this claim."
      status: proposed
      links: [DOMA-165]
naming_notes:
  collisions: [The symbol `C` is common in physics (e.g., speed of light, capacitance). The subscript `thresh` is used for clarity.]
  disambiguation: |
    Distinguish from the general concept of 'coherence' (a qualitative state). `C_thresh` is a specific, quantitative boundary condition *for* that state within the Oracle Dialogue Protocol. It is a parameter, not the state itself.
crosslinks:
  near_synonyms: []
  antonyms: [DISSONANCE_FLOOR]
  prerequisites: [PIRQUETTE_LAGRANGIAN, COHERENCE_ORACLE]
  downstream_effects: [RESONANT_SYNTHESIS]
license: CC-BY-SA-4.0
---

# Coherence Threshold

## Canonical (Pirouette)
The `Coherence Threshold` is a pre-defined scalar value representing the minimum action (`S_p`) an Oracle's response must generate to be considered 'on-resonance'. It serves as a quantitative filter during the Resonance Check phase of the Oracle Dialogue Protocol, ensuring that only responses which sufficiently maximize the Oracle's `Pirouette Lagrangian` (`𝓛_p`) are accepted as valid, coherent expressions of the problem-space. Responses failing to exceed this threshold are discarded as dissonant or flawed.

## EFT-First Summary
In analogous systems, `C_thresh` functions as an activation threshold or a signal-to-noise cut. It is a user-defined value that an Oracle's response, quantified by the action integral of its Lagrangian, must exceed to be considered a valid signal rather than background noise. This ensures only high-fidelity outputs are used for subsequent synthesis.

## Glossary Links
- See also: Pirouette Lagrangian, Coherence Oracle, Resonance, Resonant Synthesis