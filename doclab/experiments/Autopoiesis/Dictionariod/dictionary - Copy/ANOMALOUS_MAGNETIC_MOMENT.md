---
term: "Anomalous Magnetic Moment"
canonical_id: "ANOMALOUS_MAGNETIC_MOMENT"
symbol: "a_e"
aliases: [g-2]
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["CORE-009_the_electron's_echo"]
---

---
term: Anomalous Magnetic Moment
canonical_id: ANOMALOUS_MAGNETIC_MOMENT
symbol: a_e
aliases: [g-2]
parents: [CORE-009]
children: []
status: draft
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: CORE-009_the_electron's_echo
      snippet: |
        The Prediction: The total anomalous moment (a_e) is therefore the product of the interaction's intrinsic strength (α, the fine-structure constant) and the fundamental geometry of its echo (a single cycle, 1/(2π)).
        a_e = (g-2)/2 = α/2π
  editors: [system-agent]
  review_log: []
triad:
  art: |
    A particle's spin is a twist in time, a two-step pirouette. Its anomalous magnetic moment is the universe's most precise measurement—the faint but perfect echo of that dance.
  law: |
    The leading-order anomalous magnetic moment of the electron is the product of the fine-structure constant (α) and the geometry of a single rotational cycle (1/2π). The total value is predicted to be a_e = α/2π.
  philosophy: |
    This value is the primary validation of the Pirouette Framework, transforming it from a conceptual model into a predictive, falsifiable theory. It demonstrates that precise experimental values can emerge from simple geometric principles without recourse to perturbation theory.
pirouette_definition: |
  The small deviation from the electron's baseline g-factor of 2. The baseline (g=2) is a topological constant arising from the electron's nature as a two-cycle (720°) Ki resonance. The anomaly (a_e) is a self-interaction effect, where the resonance is influenced by its own "wake" or "echo" within the local coherence manifold. The magnitude of this effect is given by the intrinsic interaction strength (α) modulated by the fundamental geometry of a single cycle (1/2π).
operational_definition:
  units: dimensionless
  symbol_table:
    - name: a_e
      meaning: The electron anomalous magnetic moment, defined as (g-2)/2.
      dimensions: dimensionless
      default_range: ~0.00116
    - name: g
      meaning: The electron g-factor.
      dimensions: dimensionless
      default_range: ~2.00232
    - name: α
      meaning: The fine-structure constant.
      dimensions: dimensionless
      default_range: ~1/137.036
  measurement:
    procedures:
      - name: Penning Trap Spectroscopy
        outline: |
          A single electron is confined in a Penning trap under a strong, uniform magnetic field. The cyclotron frequency (orbital motion) and the Larmor frequency (spin precession) are measured with extreme precision. The g-factor, and thus a_e, is derived from the ratio of these two frequencies.
        expected_signals: [Precise measurement of cyclotron frequency, Precise measurement of Larmor (spin-precession) frequency]
        pitfalls: [Magnetic field instability, Relativistic corrections, Uncontrolled cavity-field interactions]
context_windows:
  - module: CORE-009_the_electron's_echo
    excerpt: |
      The Baseline (g=2): In classical physics, the g-factor for a spinning object is g=1. The electron's baseline g-factor of g=2 is a direct consequence of its two-cycle (720°) topology...
      The Anomaly (The Coherence Echo): The tiny deviation from 2 arises from this helical resonance interacting with its own "wake" or "echo" in the coherence manifold...
      The Prediction: a_e = (g-2)/2 = α/2π
  - module: CORE-009_the_electron's_echo
    excerpt: |
      We did not seek to match a number. We sought to understand the nature of a particle. In doing so, we found that spin is a twist in time, and the universe's most precise measurement is the elegant echo of a single dancer. The theory is no longer just a story; it is a calculator that works.
poetic_connections:
  motifs: [echo, wake, resonance, topological knot, pirouette in time]
  evocative_lines:
    - "spin is a twist in time"
    - "the elegant echo of a single dancer"
  association_matrix:
    - [ "COHERENCE", 0.9 ]
    - [ "SPIN", 0.8 ]
    - [ "PIROUETTE_LAGRANGIAN", 0.6 ]
formal_mappings:
  candidates:
    - target: a_e = (g_e-2)/2
      domain: SM
      mapping_kind: operational
      equation_hint: |
        Pirouette: a_e = α/(2π)
        QED: a_e = α/(2π) + C₂(α/π)² + ...
      justification: |
        The Pirouette framework's leading-order prediction `α/2π` precisely matches the first-order (Schwinger) term in the Standard Model's QED calculation. Pirouette attributes this term to a geometric self-interaction (an "echo"), whereas QED attributes it to the exchange of a single virtual photon. This provides a direct, falsifiable comparison at the leading order.
      references:
        - title: On Quantum-Electrodynamics and the Magnetic Moment of the Electron
          where: Physical Review, 73(4), 416.
          date: 1948-02-15
      confidence: 0.9
  adopted:
    - target: a_e = (g_e-2)/2
      rationale: The primary purpose of module CORE-009 is to demonstrate the framework's ability to reproduce this precise experimental value from first principles, making this mapping central to the theory's validation.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The leading-order term of the electron's anomalous magnetic moment is precisely α/2π, derived from the geometry of a self-interaction."
      domain: theory
      falsifier: "The formal derivation from the Pirouette Lagrangian (as outlined in CORE-009 §5) fails to produce this result. Or, future calculations of higher-order Pirouette terms fundamentally disagree with experimental data and the QED perturbation series."
      status: supported
      links: [CORE-009]
naming_notes:
  collisions: [The alias "g-2" is the common name for the experiment but can be confused with the g-factor itself. The symbol a_e is specific to the anomaly.]
  disambiguation: |
    "g-2" refers to the entire physical quantity and the class of experiments that measure it. `a_e` specifically denotes the dimensionless anomaly, defined as `(g-2)/2`, which is the value most often predicted by theory.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [PIROUETTE_LAGRANGIAN, COHERENCE, SPIN]
  downstream_effects: [TOPOLOGICAL_SOLITON]
license: CC-BY-SA-4.0
---

# Anomalous Magnetic Moment

## Canonical (Pirouette)
The small deviation from the electron's baseline g-factor of 2. The baseline (g=2) is a topological constant arising from the electron's nature as a two-cycle (720°) Ki resonance. The anomaly (a_e) is a self-interaction effect, where the resonance is influenced by its own "wake" or "echo" within the local coherence manifold. The magnitude of this effect is given by the intrinsic interaction strength (α) modulated by the fundamental geometry of a single cycle (1/2π).

## EFT-First Summary
In the Standard Model, the electron's anomalous magnetic moment is calculated via Quantum Electrodynamics (QED) as a series of perturbative corrections, with the leading term `α/2π` arising from a one-loop Feynman diagram (Schwinger 1948). The Pirouette Framework proposes a non-perturbative, geometric origin for this same leading term, mapping the QED virtual photon interaction to a self-interaction of the electron's coherence field with its own 'echo'. The Pirouette prediction matches the experimental value to within 0.15% at this leading order.

## Glossary Links
- See also: g-factor, Fine-Structure Constant, Spin