---
term: "Pressureless fluid"
canonical_id: "PRESSURELESS_FLUID"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["COSMO-003"]
---

---
term: Pressureless fluid
canonical_id: PRESSURELESS_FLUID_EFFECTIVE
symbol: ⟨ρ_Γ⟩, ⟨p_Γ⟩
aliases: [effective cold dark matter, time-averaged Γ field]
parents: [COSMO-003]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: COSMO-003
      lines: "L15-L17"
      snippet: |
        Γ starts displaced from its minimum in the early universe; Hubble friction freezes it (Γ̇≈0) until H≈m_Γ, after which Γ oscillates and time-averages to a **pressureless fluid**.
  editors: [AI Assistant]
  review_log: []
triad:
  art: |
    A hummingbird's wings, beating too fast to see, blur into a solid presence. From a distance, the frantic oscillation resolves into a quiet, heavy stillness that warps the air around it. This is how the cosmos perceives the Γ field: not as a vibration, but as cold, silent mass.
  law: |
    For a scalar field Γ with potential V(Γ) = ½m_Γ²Γ² + ..., when the oscillation frequency is much greater than the cosmic expansion rate (m_Γ ≫ H), the time-averaged pressure ⟨p_Γ⟩ = ⟨½Γ̇²−V(Γ)⟩ vanishes. The time-averaged energy density ⟨ρ_Γ⟩ = ⟨½Γ̇²+V(Γ)⟩ redshifts as a⁻³, behaving identically to a fluid of non-relativistic particles.
  philosophy: |
    This concept provides a microphysical origin for cold dark matter, replacing a placeholder fluid with the dynamics of a fundamental field. It demonstrates how macroscopic cosmological properties (like pressurelessness) can emerge from time-averaging microscopic oscillations, bridging the quantum and cosmic scales. This mechanism is the first stage of a unified dark sector, where the same field that acts as dark matter later drives cosmic acceleration.
pirouette_definition: |
  The effective, large-scale, time-averaged description of a coherently oscillating scalar field, Γ, valid in the regime where its mass is much greater than the Hubble rate (m_Γ ≫ H). In this limit, its kinetic and potential energies are equipartitioned over each oscillation, causing its equation of state to average to w_Γ ≈ 0. Its energy density redshifts precisely as matter (ρ_Γ ∝ a⁻³), making it operationally indistinguishable from Cold Dark Matter (CDM) in cosmological models.
operational_definition:
  units: Energy density (J·m⁻³)
  symbol_table:
    - name: Γ
      meaning: The fundamental scalar field.
      dimensions: M¹/² L¹/² T⁻¹ (in natural units, M)
      default_range: > M_pl
    - name: m_Γ
      meaning: Mass of the Γ quantum ("pressuron").
      dimensions: M
      default_range: > O(MeV)
    - name: H
      meaning: Hubble expansion rate.
      dimensions: T⁻¹
      default_range: 10⁻⁴² – 10¹⁰ GeV
    - name: w_Γ
      meaning: Equation of state parameter for the Γ field, p_Γ/ρ_Γ.
      dimensions: dimensionless
      default_range: [-1, 1]; time-averages to 0 in the pressureless fluid regime.
    - name: c_s,eff²
      meaning: Effective speed of sound squared for Γ perturbations.
      dimensions: dimensionless
      default_range: ≈ 0 for long-wavelength modes.
  measurement:
    procedures:
      - name: Cosmological Parameter Inference via Boltzmann Code
        outline: |
          1. Implement the dynamics of the Γ field, including its potential V(Γ), into a cosmological Boltzmann code (e.g., CLASS, CAMB) as a new species.
          2. Use a "fluid mapping" approximation where m_Γ ≫ H, which sets w_Γ=0 and c_s,eff²≈0 for the effective fluid.
          3. Compute theoretical predictions for cosmological observables, primarily the Cosmic Microwave Background (CMB) power spectra (TT, TE, EE) and the matter power spectrum P(k).
          4. Perform a Markov Chain Monte Carlo (MCMC) analysis to compare these predictions against observational data (e.g., from Planck, DES, Euclid). The presence and properties of the pressureless fluid are inferred from its gravitational effects on these observables, quantified by parameters like Ω_Γ and its contribution to structure growth.
        expected_signals:
          - A contribution to the total matter density (Ω_m) consistent with measurements of Ω_cdm.
          - An acoustic peak structure in the CMB power spectra characteristic of a cold, non-baryonic matter component.
          - A matter power spectrum shape and growth history (fσ₈(z)) consistent with CDM.
        pitfalls:
          - Numerical instability in the solver when switching between the exact field evolution and the averaged fluid approximation.
          - Degeneracies between Γ-potential parameters and standard cosmological parameters (e.g., H₀, A_s, n_s).
          - The effective fluid approximation breaks down on small scales where c_s,eff² is non-negligible, potentially suppressing small-scale structure compared to standard CDM.
context_windows:
  - module: COSMO-003
    excerpt: |
      Interpretation: Γ is a classical, coherently oscillating scalar whose quanta (“pressurons”) have mass m_Γ. A galactic‑scale ‘condensate’ need not be a thermal BEC; the cosmological mechanism is **misalignment**: Γ starts displaced from its minimum in the early universe; Hubble friction freezes it (Γ̇≈0) until H≈m_Γ, after which Γ oscillates and time‑averages to a **pressureless fluid**.
  - module: COSMO-003
    excerpt: |
      Fluid mapping (oscillatory regime):
      Treat Γ as an effective fluid with w_Γ≈0, c_s,eff² ≈ ⟨(k²/a²)/(4m_Γ² + (k²/a²))⟩ → 0 on large scales...
      Evolution:
      δ̇_Γ = −(1+w_Γ)(θ_Γ − 3Φ̇) − 3H(c_s,eff² − w_Γ)δ_Γ
      θ̇_Γ = −H θ_Γ + k²Ψ + k² c_s,eff² δ_Γ/(1+w_Γ).
poetic_connections:
  motifs: [vibrational stillness, emergent mass, cosmic hum, frozen field]
  evocative_lines:
    - "Hubble friction freezes it."
    - "time-averages to a pressureless fluid."
  association_matrix:
    - [ "GAMMA_FIELD", 0.9 ]
    - [ "COLD_DARK_MATTER", 0.8 ]
    - [ "COINCIDENCE_MECHANISM", 0.6 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Cold Dark Matter (CDM)
      domain: Cosmology
      mapping_kind: operational
      equation_hint: |
        ρ̇_Γ + 3H(ρ_Γ + p_Γ) = 0  ;  ⟨p_Γ⟩ ≈ 0  =>  ⟨ρ_Γ⟩ ∝ a⁻³
      rationale: |
        In the regime where the field oscillates rapidly compared to the Hubble time (m_Γ ≫ H), its time-averaged equation of state is w ≈ 0 and its energy density dilutes as a⁻³, exactly matching the macroscopic behavior of a cold, non-relativistic, pressureless fluid. The Pirouette validation suite explicitly requires that the cosmological observables generated by the Γ-fluid match standard ΛCDM predictions to within 0.1% in this limit.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The time-averaged dynamics of the Γ field in its quadratic potential are gravitationally indistinguishable from a standard Cold Dark Matter fluid on scales larger than its effective Jeans length."
      domain: phenomenology
      falsifier: "Precision measurements of the small-scale matter power spectrum (e.g., from Lyman-α forest or 21cm cosmology) reveal a cutoff or oscillations inconsistent with the calculated non-zero effective sound speed c_s,eff² of the Γ fluid, showing it deviates from a perfectly pressureless substance."
      status: proposed
      links: [COSMO-003]
    - statement: "The pressureless fluid behavior is a transient cosmological phase, eventually giving way to a dark-energy-like state as the Γ field's amplitude decays into a shallower part of its potential."
      domain: theory
      falsifier: "If CMB, BAO, and SNe data, when fitted with the unified Γ model, still require a separate, independent cosmological constant or dark energy component after the model parameters are anchored and frozen per D3 rules. This would falsify the unification claim."
      status: proposed
      links: [COSMO-003]
naming_notes:
  collisions: []
  disambiguation: |
    This term refers to the *effective, time-averaged behavior* of the Γ field, not the Γ field itself. The Γ field is a dynamic entity with non-zero pressure at any instant, oscillating between purely kinetic and purely potential energy. The "pressureless fluid" is a macroscopic description valid only over many oscillations and on large scales, analogous to how we describe the pressure of a gas without tracking individual molecular collisions.
crosslinks:
  near_synonyms: [COLD_DARK_MATTER]
  antonyms: [RADIATION_FLUID, DARK_ENERGY_FLUID]
  prerequisites: [GAMMA_FIELD, MISALIGNMENT_MECHANISM]
  downstream_effects: [STRUCTURE_FORMATION, COINCIDENCE_MECHANISM]
license: CC-BY-SA-4.0