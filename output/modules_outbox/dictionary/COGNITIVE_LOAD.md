---
term: "Cognitive Load"
canonical_id: "COGNITIVE_LOAD"
symbol: "Γ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COG-RES-002"]
---

---
term: Cognitive Load
canonical_id: COGNITIVE_LOAD
symbol: Γ
aliases: [Task Difficulty, Informational Load, System Strain]
parents: [COG-RES-002, MATH-026]
children: [COG-RES-003, DOMA-096]
status: draft
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COG-RES-002
      lines: "L59-L62"
      snippet: |
        4. **Spectral Entropy Load (Γ):**

           * Compute rolling entropy of broadband EEG power distribution.
           * Identify Γ_c from inflection in τ_P(Γ).
  editors: [system]
  review_log: []
triad:
  art: |
    The rising tide of information that strains the moorings of awareness, pushing a resonant fleet toward the brink of scattering. It is the weight of complexity, felt as a fog before the thunder of systemic change.
  law: |
    Cognitive Load (Γ) is an externally tunable control parameter that drives a neural system toward a critical point (Γ_c). Its increase is operationally defined by a corresponding divergence in the system's recovery time (τ_P) from perturbation, following a predictable power law.
  philosophy: |
    By operationalizing mental effort as a physical parameter, Cognitive Load bridges the informational and energetic domains of cognition. It allows the phase transitions of consciousness to be probed with the empirical rigor of statistical mechanics, transforming subjective strain into a measurable force.
pirouette_definition: |
  Cognitive Load (Γ) is the primary experimental control parameter used to study critical transitions in neural resonance. It quantifies the informational or computational demand placed on a conscious system, adjusted via task difficulty or sensory noise. As Γ approaches a critical value Γ_c, it induces critical slowing and coherence correlation lengthening, characteristic of a second-order phase transition in conscious access. It is measured operationally by the spectral entropy of broadband neural signals.
operational_definition:
  units: Dimensionless (bits/nats)
  symbol_table:
    - name: Γ
      meaning: Cognitive Load control parameter
      dimensions: dimensionless
      default_range: "[0, Γ_c), where Γ_c is system- and task-dependent"
  measurement:
    procedures:
      - name: Spectral Entropy Load Estimation
        outline: |
          During a cognitive task, record continuous high-density EEG or MEG. Compute the power spectral density (PSD) over a sliding time window (e.g., 2 seconds). Calculate the Shannon entropy of the normalized PSD across a broadband frequency range (e.g., 0.5–80 Hz). This rolling entropy value serves as the instantaneous measure of Γ.
        expected_signals: [EEG, MEG]
        pitfalls: [Signal contamination from motor artifacts, participant fatigue confounding entropy, non-stationarity of neural signals]
context_windows:
  - module: COG-RES-002
    excerpt: |
      Conscious access, modeled as a triadic resonance state (COG-RES-001), exhibits second-order transition behavior when the control parameter (Γ, cognitive load) approaches its critical value (Γ_c). From MATH-026, the relevant scaling relations are:

      [\xi_P \propto |T_a - T_c|^{-\nu_P}, \quad \tau_P \propto \xi_P^{z_P}]
  - module: COG-RES-002
    excerpt: |
      **Perturbation Protocol**

      1. **Triadic Lock Induction:** Establish stable phase-locked triad (f₁,f₂,f₃) under baseline load.
      2. **Load Ramp:** Gradually increase Γ by raising task complexity or introducing informational noise.
      3. **Collapse Trigger:** Observe triad decoherence event where TPCI → 0.
poetic_connections:
  motifs: [criticality, system strain, informational noise, saturation, breaking point, phase transition]
  evocative_lines:
    - "Near awareness collapse, neural recovery time (τ_P) diverges."
    - "Sharp collapse + slow recovery"
  association_matrix:
    - [ "RECOVERY_TIME", 0.9 ]
    - [ "TRIPHASIC_COHERENCE_INDEX", -0.8 ]
    - [ "CRITICALITY", 0.7 ]
formal_mappings:
  candidates:
    - target: Temperature (T) in statistical mechanics
      domain: SM
      mapping_kind: conceptual
      equation_hint: |
        τ ∝ |Γ - Γ_c|^(-zν)  maps to τ ∝ |T - T_c|^(-zν)
      justification: |
        Cognitive Load plays the role of a tuning parameter that drives the system towards a critical point, analogous to temperature in the Ising model or other systems exhibiting second-order phase transitions. Increasing Γ increases system "disorder" (entropy), similar to increasing T.
      references:
        - title: 'Scaling, universality, and renormalization: Three pillars of modern critical phenomena'
          where: 'Rev. Mod. Phys. 88, 025006'
          date: 2016-06-21
      confidence: 0.7
  adopted:
    - target: null
      rationale: null
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "As Cognitive Load (Γ) approaches a critical value (Γ_c), the recovery time (τ_P) of triadic resonance diverges according to a power law."
      domain: experiment
      falsifier: "Measurements show that τ_P remains constant, saturates, or changes stochastically as Γ increases, showing no evidence of divergence near a specific Γ_c."
      status: proposed
      links: [COG-RES-002]
naming_notes:
  collisions: [The symbol Γ is the standard notation for the Gamma function in mathematics and is also used for decay rates in particle physics and damping coefficients in mechanics.]
  disambiguation: |
    Within the Pirouette Framework, Γ exclusively denotes Cognitive Load, an informational control parameter, never a thermal temperature or mechanical damping factor. It is always defined operationally in the context of a task driving a neural system toward a critical transition and measured via information-theoretic quantities like spectral entropy.
crosslinks:
  near_synonyms: []
  antonyms: [IDLE_STATE, BASELINE_RESONANCE]
  prerequisites: [TRIPHASIC_COHERENCE_INDEX]
  downstream_effects: [CRITICAL_SLOWING, AWARENESS_COLLAPSE]
license: CC-BY-SA-4.0
---