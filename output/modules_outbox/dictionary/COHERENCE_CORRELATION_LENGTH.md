---
term: "Coherence Correlation Length"
canonical_id: "COHERENCE_CORRELATION_LENGTH"
symbol: "ξ_P"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COG-RES-002"]
---

---
term: Coherence Correlation Length
canonical_id: COHERENCE_CORRELATION_LENGTH
symbol: ξ_P
aliases: []
parents: [COG-RES-002, MATH-026]
children: [COG-RES-003, DOMA-096]
status: draft
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COG-RES-002
      lines: "§5"
      snippet: |
        Compute from spatial covariance of triad-phase coherence across electrodes.
        Extract via eigenvalue decomposition of coherence matrices.
  editors: [Agent]
  review_log: []
triad:
  art: |
    The spatial reach of a shared secret within the network's mind. As the system teeters on the brink of collapse, this reach extends, a silent, widening web of coherent whispers.
  law: |
    The coherence correlation length (ξ_P) diverges with a universal power-law exponent (ν_P) as the system's control parameter (Γ) approaches its critical value (Γ_c), according to ξ_P ∝ |Γ - Γ_c|^(-ν_P).
  philosophy: |
    ξ_P serves as the system's primary spatial order parameter, translating local phase relationships into a global measure of informational integration. Its divergence signals the imminent failure of a specific mode of consciousness, making it a key observable for predicting state transitions.
pirouette_definition: |
  The coherence correlation length, ξ_P, is a spatial order parameter that quantifies the characteristic distance over which triad-phase coherence is maintained across a neural network. Defined operationally from the dominant eigenvalue of the spatial coherence covariance matrix, ξ_P is predicted to diverge according to a power law as the system approaches a critical transition (e.g., triadic resonance collapse), serving as a direct, measurable indicator of impending systemic decoherence.
operational_definition:
  units: Length (e.g., meters, electrode spacing units)
  symbol_table:
    - name: ξ_P
      meaning: Coherence Correlation Length
      dimensions: L
      default_range: contextual
    - name: Γ
      meaning: Cognitive Load (control parameter)
      dimensions: dimensionless
      default_range: contextual
    - name: Γ_c
      meaning: Critical Cognitive Load
      dimensions: dimensionless
      default_range: contextual
    - name: ν_P
      meaning: Pirouette scaling exponent for correlation length
      dimensions: dimensionless
      default_range: 0.5 ± 0.1
  measurement:
    procedures:
      - name: Spatial Coherence Covariance Analysis
        outline: |
          1. Record high-density EEG/MEG during a cognitive load ramp experiment.
          2. For a given time window, compute the instantaneous phase of the triad frequencies for all sensors.
          3. Construct a sensor × sensor covariance matrix of the triad-phase coherence.
          4. Extract ξ_P from the eigenvalue decomposition of this matrix (e.g., related to the dominant eigenvalue or a characteristic decay length of the eigenspectrum).
        expected_signals: [High-density EEG, MEG, Triadic Phase Coherence Index (TPCI)]
        pitfalls: [Volume conduction in EEG can artificially inflate correlation length, insufficient sensor density can lead to undersampling of the spatial coherence field.]
context_windows:
  - module: COG-RES-002
    excerpt: |
      Conscious access, modeled as a triadic resonance state (COG-RES-001), exhibits second-order transition behavior when the control parameter (Γ, cognitive load) approaches its critical value (Γ_c). From MATH-026, the relevant scaling relations are: [ξ_P ∝ |Γ - Γ_c|^(-ν_P), τ_P ∝ ξ_P^(z_P)], where (ξ_P) is the coherence correlation length.
  - module: COG-RES-002
    excerpt: |
      Expected Results: The scaling of the correlation length, ξ_P ∝ |Γ−Γ_c|^(-ν_P), establishes coherence domain growth. This confirms a core prediction of the model. The visualization of log–log τ_P vs ξ_P is expected to yield a linear slope equal to the dynamic exponent z_P.
poetic_connections:
  motifs: [criticality, scaling, synchrony, domain growth, web of coherence]
  evocative_lines:
    - "a silent, widening web of coherent whispers"
    - "coherence correlation lengthening"
  association_matrix:
    - [ "RELAXATION_TIME_P", 0.9 ]
    - [ "COGNITIVE_LOAD_GAMMA", 0.8 ]
    - [ "TPCI", 0.7 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Correlation length (ξ)
      domain: SM
      mapping_kind: mathematical
      equation_hint: |
        ξ ∝ |T - T_c|^(-ν)
      justification: |
        The Pirouette term ξ_P is a direct application of the statistical mechanics concept of correlation length to neural network synchrony. It describes the characteristic length scale of fluctuations of an order parameter (triad phase coherence) near a second-order phase transition point, and is predicted to diverge with a universal exponent.
      references:
        - title: Statistical Physics of Fields
          where: M. Kardar, Chapter 4
          date: 2007-06-15
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The coherence correlation length (ξ_P) diverges as cognitive load (Γ) approaches a critical value (Γ_c)."
      domain: experiment
      falsifier: "Experimental data shows no systematic increase in ξ_P as the system approaches triadic resonance collapse, or ξ_P saturates at a finite value."
      status: proposed
      links: [COG-RES-002]
    - statement: "The divergence of ξ_P follows a power law, ξ_P ∝ |Γ−Γ_c|^(-ν_P), with a universal exponent ν_P ≈ 0.5."
      domain: phenomenology
      falsifier: "The scaling of ξ_P with respect to (Γ-Γ_c) is not well-fit by a power law, or the fitted exponent ν_P is statistically inconsistent with the Pirouette universality class prediction."
      status: proposed
      links: [COG-RES-002, MATH-026]
naming_notes:
  collisions: [The symbol ξ is standard for correlation length in statistical mechanics, which is an intentional alignment.]
  disambiguation: |
    Distinguish from Relaxation Time (τ_P), which is a *temporal* measure of critical slowing. ξ_P is the corresponding *spatial* measure. The two are linked by the dynamic exponent z_P via the scaling relation τ_P ∝ ξ_P^(z_P).
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [TRIADIC_PHASE_COHERENCE_INDEX, COGNITIVE_LOAD_GAMMA]
  downstream_effects: [RELAXATION_TIME_P, TRIADIC_RESONANCE_COLLAPSE]
license: CC-BY-SA-4.0
---

# Coherence Correlation Length

## Canonical (Pirouette)
The coherence correlation length, ξ_P, is a spatial order parameter that quantifies the characteristic distance over which triad-phase coherence is maintained across a neural network. Defined operationally from the dominant eigenvalue of the spatial coherence covariance matrix, ξ_P is predicted to diverge according to a power law as the system approaches a critical transition (e.g., triadic resonance collapse), serving as a direct, measurable indicator of impending systemic decoherence.

## EFT-First Summary
In the language of statistical field theory, ξ_P is the correlation length of the order parameter field (ψ) describing triadic resonance. Its divergence near the critical point Γ_c signifies that the mass term in the effective Lagrangian for ψ is approaching zero, leading to long-wavelength, low-energy fluctuations that dominate the system's dynamics. The universal exponent ν_P is derived from the renormalization group flow of this effective theory (see [MATH-026]).

## Glossary Links
- See also: Relaxation Time (τ_P), Dynamic Exponent (z_P), Triadic Resonance Collapse