---
term: "Quadratic-plus-tail Potential"
canonical_id: "QUADRATIC_PLUS_TAIL_POTENTIAL"
symbol: "V(Γ)"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["COSMO-Γ-001_the_early_universe"]
---

---
term: Quadratic-plus-tail Potential
canonical_id: QUADRATIC_PLUS_TAIL_POTENTIAL
symbol: V(Γ)
aliases: []
parents: [COSMO-Γ-001_the_early_universe]
children: [COSMO-Γ-CMB, COSMO-Γ-HALO]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: COSMO-Γ-001_the_early_universe
      lines: "§4"
      snippet: |
        We adopt the **quadratic-plus-tail** potentials already allowed in your base module, which yield CDM-like behavior **early** and a **slow-roll** tendency **late** (addressing coincidence without post-hoc tuning):
        * Exponential-shallow or **cosine tail** remnants of shift symmetry; parameters ((μ, f, Γ_*)) are **U-class** constants **frozen** by a D3 one-shot anchor...
  editors: [autonom-2]
  review_log: []
triad:
  art: |
    The potential defines a single score played on one instrument. It begins with a fast, matter-like beat set by its quadratic core, then slows into a dark-energy adagio dictated by its tail.
  law: |
    A single, continuous potential V(Γ) must source both early-universe matter-like oscillations (⟨w_Γ⟩ ≈ 0) and late-time acceleration (w_Γ ≈ -1). Its parameters, once frozen by a one-shot anchor (e.g., fixing Ω_{Γ,0}), must yield predictions for ΔN_eff, CMB spectra, and S₈ that are consistent with observation without further tuning.
  philosophy: |
    To provide a dynamical, unified explanation for dark matter and dark energy, resolving the cosmological coincidence problem. The potential's shape is not an ad-hoc choice but a mechanism to evolve a single field (Γ) through two distinct cosmological roles, driven by the expansion of the universe itself.
pirouette_definition: |
  A scalar field potential energy function V(Γ) composed of two parts: a quadratic core (e.g., ½m_Γ²Γ²) that dominates at early times, causing the Γ field to oscillate and behave like cold dark matter; and a non-polynomial tail (e.g., exponential or cosine) that dominates at late times, creating a shallow slope that drives cosmic acceleration. The transition is governed by the field's amplitude relative to the potential's features, and all parameters are fixed by a non-tunable, one-shot anchoring procedure.
operational_definition:
  units: M⁴ (Energy density in natural units, ħ=c=1) or J/m³.
  symbol_table:
    - name: V(Γ)
      meaning: Potential energy density of the Pressuron field.
      dimensions: M⁴
      default_range: contextual
    - name: Γ
      meaning: Pressuron field amplitude.
      dimensions: M
      default_range: contextual
    - name: m_Γ
      meaning: Mass parameter of the quadratic core, sets oscillation frequency.
      dimensions: M
      default_range: contextual, e.g., 10⁻²² eV
    - name: '{μ, f, Γ_*}'
      meaning: U-class constants defining the tail's shape, scale, and onset.
      dimensions: 'μ dimensionless; f, Γ_* have dimensions of M'
      default_range: frozen by one-shot anchor
  measurement:
    procedures:
      - name: Cosmological Parameter Inference via Boltzmann Code
        outline: |
          Implement V(Γ) in a modified Boltzmann code (e.g., CLASS/CAMB). Freeze the potential's parameters using a one-shot anchor (e.g., match observed Ω_{Γ,0}). Evolve the background and perturbation equations from the early universe to today. Compare computed observables (CMB power spectra, fσ₈(z)) against cosmological survey data (e.g., Planck, DES, Euclid) using a statistical sampler to determine consistency.
        expected_signals: [Specific non-zero contribution to ΔN_eff, Characteristic late-ISW effect in the low-ℓ CMB TT spectrum, Specific evolution of the dark energy equation of state w(z) deviating from w=-1]
        pitfalls: [Numerical instability at the oscillatory-to-slow-roll transition, Degeneracies with standard cosmological parameters, Incorrect fluid-averaging approximation]
context_windows:
  # Short, trimmed context quotes harvested from modules (3–6 sentences each).
  - module: COSMO-Γ-001_the_early_universe
    excerpt: |
      We adopt the **quadratic-plus-tail** potentials already allowed in your base module, which yield CDM-like behavior **early** and a **slow-roll** tendency **late** (addressing coincidence without post-hoc tuning): Exponential-shallow or **cosine tail** remnants of shift symmetry; parameters ((\mu, f, \Gamma_*)) are **U-class** constants **frozen** by a D3 one-shot anchor.
  - module: COSMO-Γ-001_the_early_universe
    excerpt: |
      **COSMO-Γ-HALO / MERGE:** inherits the same frozen (V(\Gamma)) to predict soliton cores, lensing, and merger offsets without particulate DM; failure to reproduce (\Sigma_0) locus falsifies the unification chain.
poetic_connections:
  # Lightweight "word-association graph" and sticky lines.
  motifs: [unification, coincidence, dynamical dark energy, slow-roll tail, cosmic metronome]
  evocative_lines:
    - "beats like a hidden metronome that matter can’t hear"
    - "they are one score, played on a single instrument"
  association_matrix:
    # symmetric or directed; weights in [0,1]
    - [ "PRESSURON_FIELD", 0.9 ]
    - [ "COINCIDENCE_PROBLEM", 0.8 ]
    - [ "MISALIGNMENT_MECHANISM", 0.7 ]
formal_mappings:
  # Candidate alignments to EFT/SM/CM/GR terms, each with justification and refs.
  candidates:
    - target: Scalar Field Potential V(φ)
      domain: GR|EFT
      mapping_kind: mathematical
      equation_hint: |
        V(Γ) ≈ ½m_Γ²Γ² + V_tail(Γ)
      justification: |
        The potential is a specific functional form for a canonical scalar field, a standard component in cosmological models. The quadratic term corresponds to a massive, non-interacting boson (like an axion), while the tail component is analogous to potentials used in quintessence models to source dark energy.
      references:
        - title: Axion-Quintessence Unification
          where: Phys. Rev. D 98, 083521
          date: 2018-10-15
      confidence: 0.9
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "A single V(Γ) with parameters frozen by a one-shot anchor can simultaneously account for the observed dark matter density and the late-time accelerated expansion."
      domain: phenomenology
      falsifier: "The model is falsified if no parameter set consistent with CMB and BBN constraints (specifically ΔN_eff) can also reproduce late-time observables like the S₈ tension or BAO/SNIa data without re-tuning or adding an independent ΛCDM component."
      status: proposed
      links: [COSMO-Γ-001_the_early_universe, COSMO-Γ-CMB]
    - statement: "The early oscillatory phase of the Γ field contributes a small, positive, and predictive amount to the effective number of relativistic species, ΔN_eff."
      domain: phenomenology
      falsifier: "The model is falsified if future BBN or CMB measurements constrain ΔN_eff to be zero or negative with high significance, or if the model's predicted value (for any allowed tail) conflicts with observations."
      status: proposed
      links: [COSMO-Γ-001_the_early_universe]
naming_notes:
  collisions: [V (general potential energy), V_eff (effective potential)]
  disambiguation: |
    Distinct from generic quintessence or scalar field dark matter potentials. The 'quadratic-plus-tail' name specifically denotes the dual-purpose functional form intended to unify the CDM-like and DE-like epochs, where both the core and the tail are dynamically important in different eras.
crosslinks:
  near_synonyms: []
  antonyms: [LAMBDA_CDM_POTENTIAL]
  prerequisites: [PRESSURON_FIELD, MISALIGNMENT_MECHANISM, ONE_SHOT_ANCHOR]
  downstream_effects: [DELTA_N_EFF, LATE_ISW_EFFECT, EQUATION_OF_STATE_EVOLUTION]
license: CC-BY-SA-4.0