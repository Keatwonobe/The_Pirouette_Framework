---
term: "Ensemble Coherence"
canonical_id: "ENSEMBLE_COHERENCE"
symbol: "Kτ_ensemble"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-163"]
---

---
term: Ensemble Coherence
canonical_id: ENSEMBLE_COHERENCE
symbol: Kτ_ensemble
aliases: [Global Synchrony, Kuramoto Coherence]
parents: [DOMA-163]
children: [CORE-012]
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-163
      snippet: |
        **Ensemble Coherence (Kτ_ensemble):** This measures the degree of global synchrony. A high value indicates the emergence of a higher-order entity—a "chorus" singing a single note. It is the direct precursor to a full **Alchemical Union (CORE-012)**.
  editors: [autogenerator-v2, analyst-rt]
  review_log: []
triad:
  art: |
    The moment a crowd's murmurs become a single chant. It is the sound of many voices deciding to sing one note, giving birth to a chorus from a cacophony.
  law: |
    A measure of the phase alignment across an ensemble of N≥3 oscillators, quantified as the squared magnitude of the mean-field vector in phase space. A value approaching 1 indicates the formation of a single, unified resonant entity.
  philosophy: |
    Ensemble Coherence provides the quantitative proof that a system has become more than the sum of its parts. It marks the transition from a collection of individuals to a collective entity, a necessary step for the formation of stable, higher-order structures via Alchemical Union.
pirouette_definition: |
  A dimensionless metric, Kτ_ensemble, that quantifies the degree of global phase synchrony across an ensemble of three or more oscillating systems. It is calculated as the square of the Kuramoto order parameter, representing the intensity of the mean-field phase vector. A high value signifies that the individual systems have dissolved their boundaries to form a single, coherent, higher-order entity operating in a state of unified Laminar Flow.
operational_definition:
  units: Dimensionless (normalized from 0 to 1)
  symbol_table:
    - name: Kτ_ensemble
      meaning: Ensemble Coherence
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: N
      meaning: Number of oscillating systems in the ensemble
      dimensions: dimensionless
      default_range: "≥ 3"
    - name: θ_k(t)
      meaning: Instantaneous phase of the k-th oscillator at time t
      dimensions: dimensionless (radians)
      default_range: "[0, 2π)"
    - name: r(t)
      meaning: Kuramoto order parameter; magnitude of the mean-field vector
      dimensions: dimensionless
      default_range: "[0, 1]"
  measurement:
    procedures:
      - name: Mean-Field Phase Vector Analysis
        outline: |
          1. For an ensemble of N systems, simultaneously record their time-series data `x_k(t)`.
          2. For each time series, use an `ExtractionMethod` (e.g., Hilbert transform) to compute the instantaneous phase `θ_k(t)`.
          3. At each time point `t`, treat each oscillator's phase as a unit vector `e^(iθ_k(t))` on the complex plane.
          4. Calculate the centroid (mean-field vector) of these N vectors: `(1/N) * Σ e^(iθ_k(t))`.
          5. The magnitude of this centroid is the order parameter `r(t)`.
          6. The Ensemble Coherence is the square of this magnitude: `Kτ_ensemble(t) = r(t)²`.
        expected_signals: [A time series of Kτ_ensemble values fluctuating between 0 (incoherence) and 1 (perfect synchrony).]
        pitfalls: [Insufficient data length to establish stable phase, signal noise corrupting phase extraction, mistaking transient alignment for a stable locked state.]
context_windows:
  - module: DOMA-163
    excerpt: |
      **Assess the Chorus:** For ensembles of three or more systems, calculate the overall Ensemble Coherence (`Kτ_ensemble`). A value approaching 1 signifies powerful global synchrony, indicating the formation of a collective, higher-order resonant entity.
  - module: DOMA-163
    excerpt: |
      The key observables are re-contextualized:
      *   **Relative Phase (Δθ):** This is no longer just a timing difference. It is the fundamental *geometric coordinate* describing the shape of the new, unified coherence manifold...
      *   **Ensemble Coherence (Kτ_ensemble):** This measures the degree of global synchrony. A high value indicates the emergence of a higher-order entity—a "chorus" singing a single note.
poetic_connections:
  motifs: [chorus, unison, synthesis, emergence, collective, unification]
  evocative_lines:
    - "We were measuring the birth of a single, larger clock from the pieces of two smaller ones."
    - "It is the sound of the universe deciding to become more than the sum of its parts."
  association_matrix:
    - [ "ALCHEMICAL_UNION", 0.9 ]
    - [ "RESONANT_HANDSHAKE", 0.7 ]
    - [ "LAMINAR_FLOW", 0.6 ]
    - [ "DISSONANCE", -1.0 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Kuramoto Order Parameter (squared)
      rationale: |
        The Pirouette formula for Kτ_ensemble is mathematically identical to the square of the Kuramoto order parameter `r`, a standard, well-established metric in the statistical physics of complex systems for quantifying the degree of synchrony in large populations of coupled oscillators. This provides a direct, unambiguous bridge to conventional scientific literature.
      equation_hint: |
        K_τ_ensemble = |(1/N) * Σ_k e^(iθ_k)|² = r²
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "A system exhibiting sustained Kτ_ensemble > 0.9 is in a state of maximal stability and minimal dissonance, functioning as a single entity."
      domain: phenomenology
      falsifier: "Observation of a system with sustained Kτ_ensemble > 0.9 that is demonstrably unstable, inefficient, or whose components can be perturbed without affecting the whole."
      status: supported
      links: [DOMA-163, CORE-006]
naming_notes:
  collisions: [The symbol K is also used for kinetic energy in classical mechanics. The τ subscript firmly places it within the Pirouette coherence family.]
  disambiguation: |
    Ensemble Coherence (Kτ_ensemble) is a global, N-body metric for N≥3. It should not be confused with the stability of a pairwise Relative Phase (Δθ), which describes a Resonant Handshake between two systems. A high Kτ_ensemble implies many stable pairwise relationships, but the reverse is not always true.
crosslinks:
  near_synonyms: []
  antonyms: [DISSONANCE, TURBULENCE]
  prerequisites: [RELATIVE_PHASE, RESONANT_HANDSHAKE]
  downstream_effects: [ALCHEMICAL_UNION, LAMINAR_FLOW]
license: CC-BY-SA-4.0
---

# Ensemble Coherence

## Canonical (Pirouette)
A dimensionless metric, Kτ_ensemble, that quantifies the degree of global phase synchrony across an ensemble of three or more oscillating systems. It is calculated as the square of the Kuramoto order parameter, representing the intensity of the mean-field phase vector. A high value signifies that the individual systems have dissolved their boundaries to form a single, coherent, higher-order entity operating in a state of unified Laminar Flow.

## EFT-First Summary
Ensemble Coherence is operationally defined as the square of the Kuramoto order parameter, a standard tool from the statistical physics of synchronization. This metric quantifies the emergence of collective behavior in a population of coupled oscillators, serving as a direct measure of the system's phase transition from an incoherent to a coherent state. It provides an observable signature for the formation of a unified, macroscopic entity from microscopic components.

## Glossary Links
- See also: Alchemical Union, Dissonance, Laminar Flow, Resonant Handshake