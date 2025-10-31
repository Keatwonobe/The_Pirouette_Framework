---
term: "Ki-Addition Constraint"
canonical_id: "KI_ADDITION_CONSTRAINT"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COG-RES-001"]
---

---
term: Ki-Addition Constraint
canonical_id: KI_ADDITION_CONSTRAINT
symbol: f₃ = f₁ + f₂ ± δf
aliases: [Triadic Resonance Rule, Sum-Frequency Condition]
parents: [MATH-024, CORE-006]
children: [MATH-025, COG-RES-002]
status: draft
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COG-RES-001
      lines: "13-15"
      snippet: |
        In cognitive systems, this manifests as frequency triads obeying the **Ki-Addition Constraint**:
        [f_3 = f_1 + f_2 \pm \delta f]
        [\Phi_3(t) \approx \Phi_1(t) + \Phi_2(t)\ (\text{mod }2\pi)]
  editors: [system-agent]
  review_log: []
triad:
  art: |
    Three tones, nearly one, a fragile chord sustained against the noise. The moment's hum, a sum of parts held in fleeting resonance. Consciousness is the harmony that endures.
  law: |
    Two neural frequency components, (f₁) and (f₂), resonantly combine to produce a third, (f₃), such that (f₃ ≈ f₁ + f₂) within a detuning margin (δf) that narrows as cognitive load (Γ) increases. The triad must also be phase-locked: (Φ₃ ≈ Φ₁ + Φ₂).
  philosophy: |
    This constraint grounds the abstract principle of Coherence Conservation in measurable neurophysiology. It is the bridge from the mathematical syntax of consciousness (the Coherence Conservation Triple) to the physical semantics of brain activity, making awareness a falsifiable, resonant phenomenon.
pirouette_definition: |
  The Ki-Addition Constraint is the rule governing the formation of frequency triads required to sustain a conscious state under the Pirouette model. It specifies that for a triad of frequencies (f₁, f₂, f₃) to support consciousness, the third frequency must be the sum of the first two within a small, load-dependent detuning margin (δf), and their phases must be locked (Φ₃ ≈ Φ₁ + Φ₂). This constraint ensures the conservation of Coherence Area (𝒜_Ki), the invariant energy-phase volume of conscious access.
operational_definition:
  units: Frequency (f) and detuning (δf) are measured in Hertz (Hz).
  symbol_table:
    - name: f₁, f₂, f₃
      meaning: Frequencies of the three components in a neural resonance triad.
      dimensions: T⁻¹
      default_range: 1-100 Hz (typical EEG/MEG bands)
    - name: δf
      meaning: Allowed detuning margin from the exact sum.
      dimensions: T⁻¹
      default_range: 0.1-2.0 Hz
    - name: Γ
      meaning: Cognitive load or environmental entropy load.
      dimensions: dimensionless or bits/sec
      default_range: contextual
    - name: TPCI
      meaning: Triadic Phase Coupling Index, a measure of phase-locking stability.
      dimensions: dimensionless
      default_range: [0, 1]
  measurement:
    procedures:
      - name: Triadic Phase Coupling Analysis
        outline: |
          1. Record high-density EEG/MEG from a subject performing a task with varying cognitive load (Γ), such as a bi-stable perception task.
          2. Apply time-frequency decomposition (e.g., Morlet wavelets) to identify candidate frequency components.
          3. For all possible frequency triplets (f₁, f₂, f₃), extract instantaneous phases (Φ₁, Φ₂, Φ₃).
          4. Calculate the Triadic Phase Coupling Index (TPCI) over sliding time windows.
          5. Identify significant TPCI peaks in the (f₁, f₂) plane, indicating phase-locked triads satisfying f₃ ≈ f₁ + f₂.
        expected_signals: [EEG/MEG time-series, behavioral reports of awareness]
        pitfalls: [Volume conduction artifacts, low signal-to-noise ratio, incorrect estimation of cognitive load Γ]
context_windows:
  - module: COG-RES-001
    excerpt: |
      Following [MATH-024], consciousness is modeled as the maintenance of a **Coherence Conservation Triple** ({E_C, J_μ, Φ_Γ}) within biological substrate limits. In cognitive systems, this manifests as frequency triads obeying the **Ki-Addition Constraint**: [f_3 = f_1 + f_2 \pm \delta f]
  - module: COG-RES-001
    excerpt: |
      **Triadic Resonance Hypothesis:** Conscious perception coincides with phase-locked triads satisfying the Ki-addition rule.
      **Detuning Constraint Hypothesis:** The allowed detuning (Δf) narrows as (Γ) (task complexity / entropy load) increases.
poetic_connections:
  motifs: [resonance, harmony, triad, tuning, constraint, sum, coherence]
  evocative_lines:
    - "Conscious perception occurs when (∂_t 𝒜_{Ki} ≈ 0)"
    - "The narrowing of viable frequency triads under high cognitive load"
  association_matrix:
    - [ "COHERENCE_AREA", 0.9 ]
    - [ "TRIADIC_PHASE_COUPLING_INDEX", 0.8 ]
    - [ "COGNITIVE_LOAD", 0.7 ]
formal_mappings:
  candidates:
    - target: Three-wave mixing (Sum-frequency generation)
      domain: AMO|CM
      mapping_kind: mathematical
      equation_hint: |
        ω₃ = ω₁ + ω₂ (frequency conservation)
        k₃ = k₁ + k₂ (phase matching condition)
      justification: |
        The Ki-Addition Constraint is mathematically isomorphic to the frequency conservation condition in three-wave mixing, a fundamental nonlinear optical process. The phase-locking requirement (Φ₃ ≈ Φ₁ + Φ₂) is analogous to the phase-matching condition required for efficient energy transfer between waves. Neural tissue acts as the nonlinear medium.
      references:
        - title: Nonlinear Optics
          where: Boyd, R. W., Chapter 2
          date: 2008-01-01
      confidence: 0.8
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "Phase-locked frequency triads satisfying the Ki-Addition Constraint are necessary for conscious perception."
      domain: experiment
      falsifier: "If conscious report occurs in the absence of a significant Triadic Phase Coupling Index (TPCI) ridge, or if the TPCI ridge does not correspond to f₃ ≈ f₁ + f₂, the claim is falsified."
      status: proposed
      links: [COG-RES-001]
    - statement: "The allowed detuning margin (δf) is inversely related to cognitive load (Γ), specifically Δf_allowed ∝ Γ⁻¹/²."
      domain: phenomenology
      falsifier: "If the bandwidth of resonant triads does not narrow, or narrows with a different functional form (e.g., linearly), as task complexity increases, the claim is falsified."
      status: proposed
      links: [COG-RES-001]
naming_notes:
  collisions: [None within Pirouette. In physics, 'k' often denotes a wavenumber, but 'Ki' here is a distinct identifier tied to Coherence Area (𝒜_Ki).]
  disambiguation: |
    This is not a generic rule for all neural frequency interactions, but is specifically hypothesized to constrain those triads that support conscious access. It is distinct from harmonic relationships (f_n = n * f₁) or broadband coupling. The "Ki" prefix links it directly to the conservation of Coherence Area (𝒜_Ki).
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [CORE-006, MATH-024]
  downstream_effects: [COG-RES-002, MATH-025]
license: CC-BY-SA-4.0
---