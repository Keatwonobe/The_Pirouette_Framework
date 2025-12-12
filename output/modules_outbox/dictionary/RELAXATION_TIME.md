---
term: "Relaxation Time"
canonical_id: "RELAXATION_TIME"
symbol: "τ_P"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COG-RES-002"]
---

---
term: Relaxation Time
canonical_id: RELAXATION_TIME
symbol: τ_P
aliases: []
parents: [COG-RES-002]
children: [COG-RES-003, DOMA-096, SOCIO-FIELD-003]
status: draft
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COG-RES-002
      lines: "§5"
      snippet: |
        1. Relaxation Time (τ_P):
           * Defined as time between TPCI minimum and 90% recovery.
           * Measure across multiple Γ-load ramps.
  editors: [system]
  review_log: []
triad:
  art: |
    Like the quiet moment after a bell is struck, it is the time the ringing coherence takes to re-emerge from the noise of its own disruption. It is the breath between the fall and the rise.
  law: |
    The relaxation time (τ_P) of triadic resonance scales as a power law with the coherence correlation length (ξ_P), diverging as the cognitive load parameter (Γ) approaches its critical value (Γ_c). The dynamic scaling exponent (z_P) is a universal constant predicted to be ~2.0.
  philosophy: |
    Relaxation time quantifies the inertia or 'stickiness' of a conscious state. A long τ_P signifies a system near a critical threshold where recovery is slow and fragile, revealing the underlying physics of cognitive stability and the universality of phase transitions in awareness.
pirouette_definition: |
  Relaxation Time (τ_P) is the empirically measured duration required for a collapsed triadic resonance to recover to a significant fraction (e.g., 90%) of its pre-collapse coherence level (TPCI). It is a key observable in the study of dynamic criticality in conscious access, predicted to diverge at a critical threshold of cognitive load (Γ_c) according to a universal scaling law τ_P ∝ ξ_P^z_P.
operational_definition:
  units: seconds (s)
  symbol_table:
    - name: τ_P
      meaning: Relaxation Time
      dimensions: T
      default_range: 10⁻³ – 10¹ s
    - name: TPCI
      meaning: Triadic Phase Coherence Index
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: ξ_P
      meaning: Coherence Correlation Length
      dimensions: L
      default_range: contextual
    - name: Γ
      meaning: Spectral Entropy Load (cognitive load parameter)
      dimensions: dimensionless
      default_range: contextual
    - name: z_P
      meaning: Dynamic Exponent
      dimensions: dimensionless
      default_range: ~2.0
  measurement:
    procedures:
      - name: Collapse-Recovery Perturbation Protocol
        outline: |
          1. Induce a stable triadic resonance (TPCI > threshold) via closed-loop stimulation.
          2. Apply a controlled cognitive load ramp (Γ) to trigger a coherence collapse (TPCI → 0).
          3. Reduce Γ and measure the time interval from the TPCI minimum to its recovery to 90% of the initial baseline value.
          4. Repeat across multiple load levels to map the τ_P(Γ) curve and fit scaling laws.
        expected_signals: [High-density EEG/MEG, TPCI(t) time series, Γ(t) time series]
        pitfalls: [Confounding physiological artifacts corrupting TPCI, Inaccurate identification of the true TPCI minimum, Participant fatigue altering baseline recovery capacity]
context_windows:
  - module: COG-RES-002
    excerpt: |
      Conscious access, modeled as a triadic resonance state (COG-RES-001), exhibits second-order transition behavior when the control parameter (Γ, cognitive load) approaches its critical value (Γ_c). From MATH-026, the relevant scaling relations are: [ξ_P ∝ |Γ - Γ_c|⁻ν_P, τ_P ∝ ξ_P^z_P] where (τ_P) is the relaxation time of awareness recovery.
  - module: COG-RES-002
    excerpt: |
      Fit τ_P vs ξ_P on log–log scale. The expected slope is z_P. A key expected result is that the τ_P vs Γ curve forms a cusp at the critical point Γ_c, confirming critical slowing. The τ_P divergence is predicted as τ_P ∝ |Γ−Γ_c|⁻ᶻ_Pν_P.
poetic_connections:
  motifs: [recovery, echo, aftermath, slowing, resonance, fragility]
  evocative_lines:
    - "Sharp collapse + slow recovery"
    - "Confirms critical slowing"
  association_matrix:
    - [ "CRITICAL_SLOWING", 0.9 ]
    - [ "COHERENCE_CORRELATION_LENGTH", 0.8 ]
    - [ "COGNITIVE_LOAD", 0.7 ]
formal_mappings:
  candidates:
    - target: Relaxation time (τ) near a critical point
      domain: SM
      mapping_kind: mathematical
      equation_hint: |
        τ ∝ |T - T_c|⁻ᶻᶼ
      justification: |
        The concept is a direct analogue of relaxation time in statistical mechanical systems undergoing a second-order phase transition. The predicted divergence near a critical point ("critical slowing down") and power-law scaling with correlation length are hallmark features of critical dynamics, as described by dynamic renormalization group theory.
      references:
        - title: Theory of dynamic critical phenomena
          where: Reviews of Modern Physics, 49(2), 435
          date: 1977-04-01
      confidence: 0.9
  adopted:
    - target: Critical relaxation time (τ) in statistical mechanics
      rationale: The module's theoretical foundation (MATH-026) and experimental design (COG-RES-002) are explicitly constructed to test for dynamic critical phenomena, making the mapping to statistical mechanics' relaxation time not just an analogy but a central, testable hypothesis.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "τ_P diverges as a power-law as the cognitive load Γ approaches a critical value Γ_c."
      domain: experiment
      falsifier: "Experimental data shows τ_P remains bounded, saturates, or scales non-universally (e.g., exponentially) as Γ approaches Γ_c."
      status: proposed
      links: [COG-RES-002]
    - statement: "The scaling relation τ_P ∝ ξ_P^z_P holds with a universal dynamic exponent z_P ≈ 2.0 ± 0.3."
      domain: phenomenology
      falsifier: "The best-fit exponent from log-log plots of τ_P vs ξ_P significantly deviates from the predicted value across multiple experimental paradigms and participants."
      status: proposed
      links: [COG-RES-002, MATH-026]
naming_notes:
  collisions: [The symbol τ is widely used in physics for various time constants and other quantities (e.g., proper time, torque, shear stress). Context (specifically, the subscript 'P' for Pirouette) is crucial for disambiguation.]
  disambiguation: |
    Distinguish from generic neural time constants (e.g., membrane time constant τ_m). τ_P is a collective, emergent dynamic property of a macroscopic system near a critical point, not a property of individual components.
crosslinks:
  near_synonyms: [RECOVERY_TIME, CRITICAL_SLOWING_TIME]
  antonyms: [COHERENCE_LIFETIME, REACTION_TIME]
  prerequisites: [TRIADIC_RESONANCE, COGNITIVE_LOAD, COHERENCE_CORRELATION_LENGTH]
  downstream_effects: [LAMINAR_TURBULENT_TRANSITION, CASCADE_RECOVERY]
license: CC-BY-SA-4.0
---

# Relaxation Time

## Canonical (Pirouette)
Relaxation Time (τ_P) is the empirically measured duration required for a collapsed triadic resonance to recover to a significant fraction (e.g., 90%) of its pre-collapse coherence level (TPCI). It is a key observable in the study of dynamic criticality in conscious access, predicted to diverge at a critical threshold of cognitive load (Γ_c) according to a universal scaling law τ_P ∝ ξ_P^z_P.

## EFT-First Summary
Relaxation Time (τ_P) is the direct operational analog of the critical relaxation time in statistical mechanics. It quantifies the 'critical slowing down' of awareness recovery near a second-order phase transition driven by cognitive load, where its divergence is governed by universal dynamic scaling exponents. Its behavior provides evidence for consciousness operating as a system near a critical point.

## Glossary Links
- See also: [Critical Slowing](./CRITICAL_SLOWING.md), [Coherence Correlation Length](./COHERENCE_CORRELATION_LENGTH.md), [Dynamic Exponent](./DYNAMIC_EXPONENT.md)