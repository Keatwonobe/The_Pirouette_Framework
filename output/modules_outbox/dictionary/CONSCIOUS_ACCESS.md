---
term: "Conscious Access"
canonical_id: "CONSCIOUS_ACCESS"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COG-RES-002"]
---

---
term: Conscious Access
canonical_id: CONSCIOUS_ACCESS
symbol: 
aliases: [awareness, triadic resonance state]
parents: [COG-RES-001, MATH-026]
children: [COG-RES-003, DOMA-096]
status: draft
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COG-RES-002
      lines: "§2"
      snippet: |
        Conscious access, modeled as a triadic resonance state (COG-RES-001), exhibits second-order transition behavior when the control parameter (Γ, cognitive load) approaches its critical value (Γ_c).
  editors: [Pirouette Indexer Agent]
  review_log: []
triad:
  art: |
    A delicate chord of neural frequencies, resonating in harmony to illuminate a single, stable moment of experience. It is the fragile coherence that holds a thought against the background noise of the mind.
  law: |
    Conscious Access is present if and only if a sustained, non-zero Triadic Phase Coherence Index (TPCI) is measurable between three or more distinct neural frequency bands, indicating a phase-locked resonance. Its collapse and recovery near a critical threshold exhibit universal scaling dynamics.
  philosophy: |
    To define conscious access not as an intrinsic property but as a dynamic, fragile state of resonant coherence allows it to be studied as a physical system. It reframes abstract questions of awareness into measurable, falsifiable problems of phase stability, critical dynamics, and information flow within a resonant structure.
pirouette_definition: |
  Conscious Access is the metastable state of a cognitive system characterized by a stable, phase-locked triadic resonance between three or more neural frequency components. This state enables the global broadcast and sustained processing of information. Its stability is governed by a control parameter (e.g., cognitive load Γ), and it exhibits critical dynamics, such as critical slowing, near the phase boundary of its collapse into decoherence.
operational_definition:
  units: Dimensionless (state), measured via dimensionless indices (e.g., TPCI) or temporal dynamics (seconds).
  symbol_table:
    - name: TPCI
      meaning: Triadic Phase Coherence Index; measures the degree of phase-locking in the triad.
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: Γ
      meaning: Cognitive Load; control parameter driving the system towards collapse.
      dimensions: dimensionless
      default_range: contextual
    - name: Γ_c
      meaning: Critical Cognitive Load; the value of Γ at which the phase transition occurs.
      dimensions: dimensionless
      default_range: contextual
    - name: τ_P
      meaning: Relaxation Time; characteristic time for the system to recover from a perturbation near Γ_c.
      dimensions: T
      default_range: "10ms - 2s"
    - name: ξ_P
      meaning: Coherence Correlation Length; spatial scale over which triad phases are correlated.
      dimensions: L
      default_range: contextual
    - name: z_P
      meaning: Dynamic Exponent; relates relaxation time to correlation length (τ_P ∝ ξ_P^z_P).
      dimensions: dimensionless
      default_range: "~2.0"
  measurement:
    procedures:
      - name: Triadic Resonance Collapse & Recovery Protocol
        outline: |
          Induce a stable triadic resonance (TPCI > threshold) via closed-loop stimulation. Incrementally increase cognitive load (Γ) until the resonance collapses (TPCI → 0). Measure the recovery time (τ_P) and coherence correlation length (ξ_P) as a function of Γ's proximity to the critical point Γ_c. Fit the scaling exponents z_P and ν_P from the collected data.
        expected_signals: [EEG/MEG, TPCI(t) time series, τ_P(Γ) curves]
        pitfalls: [Subject fatigue altering baseline Γ, Conflating stimulation artifacts with neural signals, Insufficient sampling near the critical point Γ_c]
context_windows:
  - module: COG-RES-002
    excerpt: |
      Conscious access, modeled as a triadic resonance state (COG-RES-001), exhibits second-order transition behavior when the control parameter (Γ, cognitive load) approaches its critical value (Γ_c). The relevant scaling relations are: [ξ_P ∝ |Γ - Γ_c|⁻ν_P, τ_P ∝ ξ_P^z_P].
  - module: COG-RES-002
    excerpt: |
      If triad coherence collapses stochastically without critical slowing, the system may not follow LPF dynamics, and the model of conscious access as a critical phenomenon is weakened. This provides a clear falsification path for the theory.
poetic_connections:
  motifs: [resonance, collapse, criticality, coherence, phase transition, fragile stability]
  evocative_lines:
    - "Sharp collapse + slow recovery"
    - "the dynamic scaling of triadic resonance collapse"
    - "a cusp in the recovery time curve"
  association_matrix:
    - [ "Triadic Resonance", 0.9 ]
    - [ "Cognitive Load (Γ)", 0.8 ]
    - [ "Criticality", 0.7 ]
    - [ "Decoherence", 0.6 ]
formal_mappings:
  candidates:
    - target: Second-order phase transition
      domain: SM
      mapping_kind: mathematical
      equation_hint: |
        τ ∝ |T - T_c|⁻ᶻᵛ
      justification: |
        The collapse of conscious access is modeled as a phase transition where cognitive load (Γ) acts as the control parameter (analogous to temperature). The system exhibits hallmarks of criticality, including divergence of relaxation time (critical slowing) and correlation length, governed by universal scaling exponents, mirroring phenomena in condensed matter systems like the Ising model.
      references:
        - title: MATH-026
          where: Pirouette Framework
          date: 
      confidence: 0.9
  adopted:
    - target: Second-order phase transition
      rationale: The entire experimental design in COG-RES-002 is predicated on this mapping, providing a rich, predictive, and falsifiable framework for studying awareness dynamics.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "The recovery time (τ_P) of conscious access diverges with a power-law relationship as cognitive load (Γ) approaches a critical value (Γ_c)."
      domain: experiment
      falsifier: "Measurement shows τ_P remains constant or changes non-systematically as Γ approaches the point of triadic collapse."
      status: proposed
      links: [COG-RES-002]
    - statement: "The scaling exponents (ν_P, z_P) governing the collapse of conscious access are universal, matching predictions from renormalization group analysis in MATH-026."
      domain: phenomenology
      falsifier: "Measured exponents vary significantly between individuals or experimental conditions, or they do not match the predicted values (ν_P ≈ 0.5, z_P ≈ 2.0)."
      status: proposed
      links: [COG-RES-002, MATH-026]
naming_notes:
  collisions: [The term "conscious access" is used widely in neuroscience and philosophy of mind with varying definitions.]
  disambiguation: |
    In Pirouette, 'Conscious Access' specifically refers to the operational definition of a stable triadic resonance, a measurable physical state. This should be distinguished from broader philosophical or cognitive science definitions which may not be tied to a specific, falsifiable physical mechanism.
crosslinks:
  near_synonyms: [TRIADIC_RESONANCE]
  antonyms: [DECOHERENCE, INATTENTION]
  prerequisites: [TRIADIC_RESONANCE, TPCI]
  downstream_effects: [TRIADIC_MANIFOLDS, CADUCEUS_LENS]
license: CC-BY-SA-4.0
---

# Conscious Access

## Canonical (Pirouette)
Conscious Access is the metastable state of a cognitive system characterized by a stable, phase-locked triadic resonance between three or more neural frequency components. This state enables the global broadcast and sustained processing of information. Its stability is governed by a control parameter (e.g., cognitive load Γ), and it exhibits critical dynamics, such as critical slowing, near the phase boundary of its collapse into decoherence.

## EFT-First Summary
Conscious Access is modeled as the ordered phase of a system described by an effective field theory, where the order parameter is the triadic coherence field. The system's 'temperature' is analogous to cognitive load Γ. As Γ approaches a critical value Γ_c, the system undergoes a second-order phase transition into a disordered (decoherent) state. The dynamics near this critical point are governed by universal scaling laws, with the relaxation time (τ_P) and correlation length (ξ_P) diverging, consistent with renormalization group predictions for systems in the Landau-Ginzburg-Wilson universality class.

## Glossary Links
- See also: [[Triadic Resonance]], [[Cognitive Load]], [[Criticality]]