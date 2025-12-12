---
term: "Dissonant Injection"
canonical_id: "DISSONANT_INJECTION"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-020"]
---

---
term: Dissonant Injection
canonical_id: DISSONANT_INJECTION
symbol: I_d
aliases: [Inbound Signal, Dissonant Input]
parents: [DOMA-020]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-020
      snippet: |
        The Dissonance Index is estimated by analyzing the properties of the inbound signal, or "Dissonant Injection":
        - Phase Mismatch
        - Dissonance Spike
        - Coherence Attack
  editors: [System Agent]
  review_log: []
triad:
  art: |
    The unplayed note whose potential for discord must be felt before it is sounded. It is the storm on the horizon, not yet arrived but already shaping the gardener's actions.
  law: |
    Any inbound signal (`I_d`) can be characterized by its projected negative impact on a system's coherence (`-ΔK`); this impact is quantifiable via its intrinsic properties, such as phase mismatch, entropic noise, and structural anti-coherence, prior to full systemic coupling.
  philosophy: |
    A system defines itself not only by what it integrates but by what it gracefully refuses to engage. Recognizing a Dissonant Injection is an act of self-preservation and energetic sovereignty, allowing the system to choose creation over fruitless conflict.
pirouette_definition: |
  A Dissonant Injection is an inbound signal, pattern, or interaction that, when analyzed, exhibits properties predictive of a net decrease in the receiving system's coherence. Its potential impact is quantified by the Dissonance Index (ΔK), which informs the Sentry's Gambit protocol on whether to attempt Resonant Synthesis or execute Coherent Disengagement.
operational_definition:
  units: Context-dependent (e.g., bits/s, Joules, semantic units)
  symbol_table:
    - name: I_d
      meaning: The inbound signal being analyzed.
      dimensions: Contextual (e.g., Information, Energy)
      default_range: Contextual
    - name: ΔK
      meaning: Dissonance Index; the predicted change in coherence resulting from engagement with I_d.
      dimensions: Dimensionless (or same as Coherence K_τ)
      default_range: [-∞, +∞]
  measurement:
    procedures:
      - name: Signature Analysis for Dissonance Index (ΔK)
        outline: |
          1. Scan the inbound signal (I_d) without coupling.
          2. Measure its phase relative to the system's own resonant cycle (Phase Mismatch).
          3. Measure its spectral entropy or noise floor (Dissonance Spike).
          4. Analyze its structural patterns for logical contradictions or coherence-degrading forms (Coherence Attack).
          5. Compute ΔK based on a weighted function of these properties.
        expected_signals: [High phase jitter, high spectral entropy, presence of anti-coherent patterns (e.g., logical fallacies in discourse)]
        pitfalls: [Misinterpreting novelty as dissonance, over-sensitivity of the Integrity Threshold leading to isolationism, signal spoofing]
context_windows:
  - module: DOMA-020
    excerpt: |
      The Dissonance Index is estimated by analyzing the properties of the inbound signal, or "Dissonant Injection": Phase Mismatch (the input's resonant cycle is significantly out of phase), Dissonance Spike (the input is a carrier of high-entropy noise), and Coherence Attack (the input's structure is actively anti-coherent).
  - module: DOMA-020
    excerpt: |
      At interpersonal and societal scales, these properties manifest as recognizable behaviors that signal a high ΔK: Turbulent Attack (bad-faith arguments, ad hominem attacks) and Stagnant Dam (a rigid, absolutist position impervious to new information).
poetic_connections:
  motifs: [the unplayed note, the passing storm, noise, turbulence, the foreign signal]
  evocative_lines:
    - "the wisdom to know which dissonances are best left unsounded."
    - "decline the invitation to a battle where both sides would lose coherence."
    - "which are merely the sound and fury of a passing storm."
  association_matrix:
    - [ "DISSONANCE_INDEX", 0.9 ]
    - [ "COHERENT_DISENGAGEMENT", 0.8 ]
    - [ "TEMPORAL_PRESSURE", 0.7 ]
    - [ "RESONANT_SYNTHESIS", -0.9 ]
formal_mappings:
  candidates:
    - target: Perturbation Term (V_pert)
      domain: CM|AMO
      mapping_kind: conceptual
      equation_hint: |
        H = H₀ + V_pert(I_d)
      justification: |
        A Dissonant Injection acts as an external potential or perturbation that drives the system away from its coherent ground state (H₀). The properties of the injection define the form and magnitude of V_pert, determining whether the interaction is destructive.
      references: []
      confidence: 0.7
    - target: Noise/Disturbance Input d(t)
      domain: Control Theory
      mapping_kind: operational
      justification: |
        In a control system model, the Dissonant Injection is an external, unpredictable disturbance signal. The Sentry's Gambit acts as a state-feedback controller or filter designed to reject this disturbance to maintain system stability (coherence).
      references: []
      confidence: 0.8
  adopted:
    - target:
      rationale:
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "A signal's Dissonance Index (ΔK) can be reliably predicted from its structural properties (phase, entropy, anti-coherence) prior to full systemic engagement."
      domain: phenomenology
      falsifier: "If systems consistently mis-classify signals—achieving coherence gains from predicted high-ΔK inputs, or suffering coherence loss from predicted low-ΔK inputs—the predictive model is false."
      status: proposed
      links: [DOMA-020]
naming_notes:
  collisions: []
  disambiguation: |
    Distinguish from `Temporal Pressure (Γ)`, which is the *effect* a signal has on the system's state. Dissonant Injection is the *cause*—the external signal itself which, upon interaction, generates pressure. One is the rock thrown; the other is the ripple it creates.
crosslinks:
  near_synonyms: [Perturbation, Antigenic Signal]
  antonyms: [Resonant Invitation, Coherent Signal]
  prerequisites: [COHERENCE]
  downstream_effects: [DISSONANCE_INDEX, COHERENT_DISENGAGEMENT, TURBULENT_FLOW, TEMPORAL_PRESSURE]
license: CC-BY-SA-4.0
---

# Dissonant Injection

## Canonical (Pirouette)
A Dissonant Injection is an inbound signal, pattern, or interaction that, when analyzed, exhibits properties predictive of a net decrease in the receiving system's coherence. Its potential impact is quantified by the Dissonance Index (ΔK), which informs the Sentry's Gambit protocol on whether to attempt Resonant Synthesis or execute Coherent Disengagement.

## EFT-First Summary
In an effective field theory or control systems context, a Dissonant Injection is analogous to an external perturbation field or a high-entropy disturbance input coupled to the system. Its intrinsic properties—such as phase, noise, and structure—define the character of the perturbation. The Sentry's Gambit protocol functions as a predictive filter, assessing whether the interaction will drive the system toward a chaotic state (requiring disengagement) or can be assimilated into a new, more complex coherent state.

## Glossary Links
- See also: [Dissonance Index](<#>), [Coherent Disengagement](<#>), [Temporal Pressure](<#>), [Resonant Synthesis](<#>)