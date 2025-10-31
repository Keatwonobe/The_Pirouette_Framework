---
term: "Dynamic Exponent"
canonical_id: "DYNAMIC_EXPONENT"
symbol: "z_P"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COG-RES-002"]
---

---
term: Dynamic Exponent
canonical_id: DYNAMIC_EXPONENT
symbol: z_P
aliases: []
parents: [COG-RES-002, MATH-026]
children: [COG-RES-003, DOMA-096]
status: draft
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COG-RES-002
      lines: "15-20"
      snippet: |
        From MATH-026, the relevant scaling relations are:

        [\xi_P \propto |T_a - T_c|^{-\nu_P}, \quad \tau_P \propto \xi_P^{z_P}]

        where: ... (z_P): dynamic exponent (~2 for non-conserved ψ)
  editors: [agent: auto-compiler]
  review_log: []
triad:
  art: |
    Like a ripple in a pond, the time it takes for the water to calm depends on the size of the initial splash. The dynamic exponent governs how a system's memory of disruption fades with spreading coherence.
  law: |
    The relaxation time (τ_P) of a system near a critical point scales as a power-law of its correlation length (ξ_P), with the dynamic exponent (z_P) as the exponent. This relationship, τ_P ∝ ξ_P^z_P, is empirically testable via a linear fit on a log-log plot of τ_P versus ξ_P.
  philosophy: |
    The dynamic exponent links the temporal and spatial scales of a system's fluctuations at a critical transition. Its universality implies that diverse systems, from neural networks to magnetic materials, 'slow down' in the same fundamental way, revealing a shared grammar of collective behavior.
pirouette_definition: |
  The dynamic exponent, z_P, is a dimensionless universal scaling exponent that quantifies the power-law relationship between the relaxation time (τ_P) of a system recovering from perturbation and its coherence correlation length (ξ_P) near a second-order phase transition. It is defined by the scaling relation τ_P ∝ ξ_P^z_P. Within Pirouette, it specifically describes the critical slowing of triadic resonance collapse in cognitive systems, where z_P ≈ 2.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: z_P
      meaning: Dynamic Exponent
      dimensions: dimensionless
      default_range: "2.0 ± 0.3"
    - name: τ_P
      meaning: Relaxation Time
      dimensions: T
      default_range: contextual
    - name: ξ_P
      meaning: Coherence Correlation Length
      dimensions: L
      default_range: contextual
  measurement:
    procedures:
      - name: Log-Log Scaling Regression
        outline: |
          1. Induce and perturb a system (e.g., triadic resonance) near its critical point (Γ_c).
          2. For each perturbation event, measure the relaxation time (τ_P) for the system to return to equilibrium (e.g., time for TPCI to recover to 90%).
          3. Simultaneously, measure the spatial correlation length (ξ_P) of the system's fluctuations from the spatial covariance of triad-phase coherence.
          4. Plot log(τ_P) against log(ξ_P) across many events.
          5. The slope of the resulting linear fit is the measured value of z_P.
        expected_signals: [TPCI(t), Spatial Coherence Matrix]
        pitfalls: [Finite-size effects rounding the transition, Difficulty in precisely locating the critical point Γ_c, Noise in τ_P and ξ_P measurements obscuring the linear relationship]
context_windows:
  - module: COG-RES-002
    excerpt: |
      Conscious access, modeled as a triadic resonance state (COG-RES-001), exhibits second-order transition behavior when the control parameter (Γ, cognitive load) approaches its critical value (Γ_c). From MATH-026, the relevant scaling relations are: [ξ_P ∝ |T_a - T_c|⁻ν_P, τ_P ∝ ξ_P^z_P] where ... (z_P): dynamic exponent (~2 for non-conserved ψ).
  - module: COG-RES-002
    excerpt: |
      Aggregate across participants and fit scaling exponents (ν_P, z_P). Compare empirical results to Pirouette-predicted exponents: ν_P ≈ 0.5 ± 0.1, z_P ≈ 2.0 ± 0.3. Visualization: τ_P vs Γ curve forms a cusp; log–log τ_P vs ξ_P yields linear slope z_P.
poetic_connections:
  motifs: [critical slowing, universality, time-space scaling, recovery, system memory]
  evocative_lines:
    - "Sharp collapse + slow recovery"
    - "Detect critical slowing, coherence correlation lengthening, and universality"
  association_matrix:
    - [ "RELAXATION_TIME", 0.9 ]
    - [ "CORRELATION_LENGTH", 0.9 ]
    - [ "CRITICALITY", 0.8 ]
    - [ "UNIVERSALITY_CLASS", 0.7 ]
formal_mappings:
  candidates: []
  adopted:
    - target: z (Dynamic Critical Exponent)
      domain: SM
      mapping_kind: mathematical
      equation_hint: |
        τ ∝ ξ^z
      justification: |
        The Pirouette dynamic exponent z_P is a direct application of the dynamic critical exponent 'z' from the theory of critical phenomena in statistical mechanics. It describes the scaling of relaxation time with correlation length near a continuous phase transition, a concept central to models of dynamic universality classes (e.g., Model A/B in Hohenberg-Halperin classification).
      references:
        - title: Theory of dynamic critical phenomena
          where: Hohenberg, P. C., & Halperin, B. I. (1977). Reviews of Modern Physics, 49(3), 435.
          date: 1977-07-01
      rationale: The term is a direct import from statistical mechanics, with its mathematical definition and conceptual role (linking time and space scaling at criticality) preserved. Pirouette applies it to the specific domain of neuro-cognitive dynamics.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The relationship between relaxation time τ_P and correlation length ξ_P is a power-law, τ_P ∝ ξ_P^z_P, for triadic resonance collapse."
      domain: experiment
      falsifier: "An experimental log-log plot of τ_P vs ξ_P shows a non-linear relationship, or the linear fit is poor (low R²), indicating that a single power-law does not describe the data."
      status: proposed
      links: [COG-RES-002]
    - statement: "The value of the dynamic exponent z_P for triadic resonance collapse is universal, falling within the range 2.0 ± 0.3."
      domain: phenomenology
      falsifier: "Repeated, high-precision measurements consistently find a value of z_P significantly outside the predicted range (e.g., z_P < 1.5 or z_P > 2.5), suggesting the system belongs to a different universality class or that the underlying theory is incorrect."
      status: proposed
      links: [COG-RES-002, MATH-026]
naming_notes:
  collisions: ["`z` is a common symbol for the 3rd spatial coordinate."]
  disambiguation: |
    In Pirouette, `z_P` is always a dimensionless exponent related to dynamics at a phase transition. Context involving correlation length (`ξ_P`) and relaxation time (`τ_P`) confirms this usage, distinguishing it from a spatial coordinate.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [RELAXATION_TIME, CORRELATION_LENGTH, CRITICALITY]
  downstream_effects: [CRITICAL_SLOWING, UNIVERSALITY_CLASS]
license: CC-BY-SA-4.0
---

# Dynamic Exponent

## Canonical (Pirouette)
The dynamic exponent, z_P, is a dimensionless universal scaling exponent that quantifies the power-law relationship between the relaxation time (τ_P) of a system recovering from perturbation and its coherence correlation length (ξ_P) near a second-order phase transition. It is defined by the scaling relation τ_P ∝ ξ_P^z_P. Within Pirouette, it specifically describes the critical slowing of triadic resonance collapse in cognitive systems, where z_P ≈ 2.

## EFT-First Summary
The Dynamic Exponent `z_P` is the Pirouette Framework's application of the dynamic critical exponent `z` from statistical mechanics, which governs the universal scaling relationship between relaxation time (`τ`) and correlation length (`ξ`) near a continuous phase transition (`τ ∝ ξ^z`). It operationalizes the concept of 'critical slowing down' in cognitive systems, where recovery from perturbations becomes increasingly slow as the system approaches a critical threshold. This mapping is adopted from foundational work in dynamic critical phenomena (Hohenberg & Halperin, 1977).

## Glossary Links
- See also: Critical Slowing, Correlation Length, Relaxation Time, Universality Class