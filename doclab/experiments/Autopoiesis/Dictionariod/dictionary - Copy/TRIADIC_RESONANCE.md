---
term: "Triadic Resonance"
canonical_id: "TRIADIC_RESONANCE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COG-RES-001"]
---

---
term: Triadic Resonance
canonical_id: TRIADIC_RESONANCE
symbol: ℜ₃
aliases: [Triad-Locking, Ki-Addition Resonance]
parents: [MATH-024, CORE-006]
children: [MATH-025, COG-RES-002]
status: candidate
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COG-RES-001
      lines: "L15-L22"
      snippet: |
        Following [MATH-024], consciousness is modeled as the maintenance of a **Coherence Conservation Triple** ({E_C, J_\mu, \Phi_\Gamma}) within biological substrate limits. In cognitive systems, this manifests as frequency triads obeying the **Ki-Addition Constraint**:
        [f_3 = f_1 + f_2 \pm \delta f]
        [\Phi_3(t) \approx \Phi_1(t) + \Phi_2(t)\ (\text{mod }2\pi)]
  editors: [Pirouette Framework Agent]
  review_log: []
triad:
  art: |
    Three notes of neural activity, held in phase, create the chord of awareness. When their harmony is sustained against the noise of the world, a moment of consciousness crystallizes.
  law: |
    A state of triadic resonance exists when three frequency bands `(f₁, f₂, f₃)` satisfy the Ki-addition constraint `f₃ = f₁ + f₂ ± δf` and maintain stable phase-locking `Φ₃ ≈ Φ₁ + Φ₂`, resulting in a Triadic Phase Coupling Index (TPCI) approaching 1.
  philosophy: |
    Triadic Resonance provides a concrete, physicalist substrate for phenomenal consciousness, moving it from an ineffable property to a measurable, dynamical state. It posits that the 'what-it-is-likeness' of experience is isomorphic to the geometry of this conserved coherence area.
pirouette_definition: |
  Triadic Resonance is a state of stable, non-linear phase-locking among three distinct neural frequency bands `(f₁, f₂, f₃)` that conform to the Ki-addition constraint `(f₃ ≈ f₁ + f₂)` and `(Φ₃ ≈ Φ₁ + Φ₂)`. This resonance is hypothesized to be the primary mechanism for conscious access, binding disparate neural information into a unified percept. The stability and allowed detuning `(δf)` of the triad are constrained by the cognitive load `(Γ)` on the system, and its persistence relies on the conservation of the Coherence Area `(A_Ki)`.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: TPCI
      meaning: Triadic Phase Coupling Index
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: fₖ
      meaning: Frequency of neural band k
      dimensions: T⁻¹
      default_range: "1-150 Hz"
    - name: Φₖ
      meaning: Instantaneous phase of band k
      dimensions: dimensionless
      default_range: "[0, 2π] rad"
    - name: δf
      meaning: Frequency detuning allowance
      dimensions: T⁻¹
      default_range: "contextual, load-dependent"
    - name: Γ
      meaning: Cognitive / entropy load
      dimensions: dimensionless or T⁻¹ (bits/sec)
      default_range: "contextual"
  measurement:
    procedures:
      - name: Triadic Phase Coupling Index (TPCI) Measurement
        outline: |
          1. Record neural activity using high-density EEG/MEG.
          2. Apply a time-frequency decomposition (e.g., Morlet wavelets) to identify candidate frequency bands `(f₁, f₂, f₃)`.
          3. Extract the instantaneous phase `(Φ₁, Φ₂, Φ₃)` for each band.
          4. Calculate the triadic phase relationship `ΔΦ(t) = Φ₃(t) - Φ₁(t) - Φ₂(t)`.
          5. Compute the TPCI as the magnitude of the mean complex vector over a time window: `TPCI = |⟨e^(iΔΦ(t))⟩|`.
        expected_signals: [A TPCI value significantly greater than zero (e.g., > 0.5) during periods of reported conscious perception, correlated with behavioral report.]
        pitfalls: [Volume conduction artifacts in EEG creating spurious coupling, Improper time-frequency resolution, Insufficient signal-to-noise ratio.]
context_windows:
  - module: COG-RES-001
    excerpt: |
      The Triadic Resonance Hypothesis states that conscious perception coincides with phase-locked triads satisfying the Ki-addition rule. The Detuning Constraint Hypothesis posits that the allowed detuning `(δf)` narrows as cognitive load `(Γ)` increases. The Area Conservation Hypothesis claims that `A_Ki` remains approximately constant across content transitions within continuous awareness.
  - module: COG-RES-001
    excerpt: |
      If no TPCI ridge forms at triad frequencies, the triadic resonance model fails. If `A_Ki` varies unpredictably during stable awareness, coherence conservation is violated. If `Δf_allowed` does not narrow with `Γ`, the detuning constraint is falsified.
poetic_connections:
  motifs: [harmony, chord, locking, coherence, binding, tripod]
  evocative_lines:
    - "Consciousness is modeled as the maintenance of a Coherence Conservation Triple."
    - "A sharp TPCI ridge in the `(f₁, f₂)` plane."
  association_matrix:
    - [ "COHERENCE_AREA", 0.9 ]
    - [ "CONSCIOUS_ACCESS", 0.8 ]
    - [ "COGNITIVE_LOAD", 0.6 ]
formal_mappings:
  candidates:
    - target: Three-wave mixing
      domain: AMO|Plasma Physics
      mapping_kind: mathematical
      equation_hint: |
        ω₃ = ω₁ + ω₂  (energy conservation)
        k₃ = k₁ + k₂  (momentum/phase conservation)
      justification: |
        The Ki-addition rule for frequencies `(f₃ = f₁ + f₂)` and the phase-locking constraint `(Φ₃ ≈ Φ₁ + Φ₂)` are mathematically analogous to the energy and momentum (phase-matching) conservation conditions for three-wave mixing in non-linear media. In this mapping, neural populations act as the non-linear medium, and phase-locked frequency bands are analogous to coherent wave packets.
      references:
        - title: Nonlinear Optics
          where: Boyd, R. W.
          date: 2008-01-01
      confidence: 0.8
  adopted:
    - target:
      rationale:
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "Conscious perception is directly subserved by the formation of phase-locked neural frequency triads."
      domain: experiment
      falsifier: "Failure to observe a significant increase in the Triadic Phase Coupling Index (TPCI) selectively during periods of conscious report in bi-stable perception tasks."
      status: under-test
      links: [COG-RES-001]
    - statement: "The allowed frequency detuning `(δf)` for a stable triad narrows as cognitive load `(Γ)` increases, following `δf ∝ Γ⁻¹/²`."
      domain: phenomenology
      falsifier: "Observing that the bandwidth of resonant triads is either insensitive to cognitive load or follows a different functional form."
      status: proposed
      links: [COG-RES-001]
    - statement: "The Coherence Area `(A_Ki)` is conserved across transitions in conscious content, provided awareness is maintained."
      domain: theory
      falsifier: "Measurement of Coherence Area Variance (CAV) showing significant, content-dependent fluctuations during periods of continuous, stable awareness."
      status: proposed
      links: [COG-RES-001, MATH-024]
naming_notes:
  collisions: [The term 'resonance' is used broadly in neuroscience (e.g., stochastic resonance, structural resonance). Triadic Resonance is specific to this non-linear, three-frequency phase-locking phenomenon.]
  disambiguation: |
    Distinguish from simple cross-frequency coupling (CFC), which typically involves two frequencies (e.g., phase-amplitude coupling). Triadic Resonance requires phase-phase-phase coupling among three distinct bands satisfying the Ki-addition rule.
crosslinks:
  near_synonyms: [TRIAD_LOCKING]
  antonyms: [DECOHERENCE_STATE]
  prerequisites: [COHERENCE_AREA, KI_ADDITION_CONSTRAINT]
  downstream_effects: [CONSCIOUS_ACCESS, BINDING_PROBLEM_SOLUTION]
license: CC-BY-SA-4.0
---