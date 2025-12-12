---
term: "Fluid Mapping"
canonical_id: "FLUID_MAPPING"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["COSMO-004"]
---

---
term: Fluid Mapping
canonical_id: FLUID_MAPPING
symbol: c_{s,eff}², w_Γ
aliases: [Effective Fluid Approximation, Oscillatory Regime Mapping]
parents: [COSMO-004]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: COSMO-004
      lines: "A3"
      snippet: |
        A3. Fluid Mapping (Oscillatory Regime, OPTIONAL)
        When m_Γ ≫ H and the field oscillates rapidly,
        w_Γ ≈ 0,
        c_{s,eff}²(k,a) ≈ (k²/a²) / (4 m_Γ² + k²/a²)
  editors: [system]
  review_log: []
triad:
  art: |
    When a field's frantic hum blurs into a steady pressure, its fine-grained trembling is heard only as the drone of a fluid. The dance of the string becomes the flow of the river, trading detail for distance.
  law: |
    The evolution of a rapidly oscillating scalar field Γ, where its mass `m_Γ` is much greater than the Hubble parameter `H`, can be approximated by the equations of an imperfect fluid with an averaged equation of state `w_Γ ≈ 0` and a scale-dependent effective sound speed `c_{s,eff}² = (k²/a²) / (4 m_Γ² + k²/a²)`. This mapping is valid for modes `k/a ≪ m_Γ`.
  philosophy: |
    To trade the intractable stiffness of a rapidly oscillating field for the smoother, more computationally efficient evolution of a fluid. This mapping embodies the principle of effective theory, coarse-graining over microscopic details to capture macroscopic behavior, thereby enabling simulations to cross vast dynamical ranges without prohibitive cost.
pirouette_definition: |
  A computational and theoretical approximation that maps the dynamics of a scalar field Γ onto those of an imperfect cosmological fluid. The mapping is valid in the oscillatory regime where the field's effective mass `m_Γ = √V_{,ΓΓ}` is significantly larger than the Hubble expansion rate `H` (e.g., `m_Γ/H > 50`). Under this mapping, the field's averaged equation of state approaches that of cold matter (`w_Γ ≈ 0`), and its perturbations are governed by a unique, scale-dependent effective sound speed, `c_{s,eff}²(k,a)`. This replaces the second-order Klein-Gordon equation for field perturbations `δΓ` with first-order fluid equations for density contrast `δ_Γ` and velocity divergence `θ_Γ`.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: m_Γ
      meaning: Effective mass of the Γ field, √V_{,ΓΓ}.
      dimensions: M L T⁻¹ (natural units, ħ=c=1)
      default_range: > 10 MeV
    - name: H
      meaning: Hubble expansion parameter (physical time).
      dimensions: T⁻¹
      default_range: contextual (decreases with time)
    - name: c_{s,eff}²
      meaning: Effective sound speed squared of the Γ fluid.
      dimensions: dimensionless
      default_range: [0, 1]
    - name: k
      meaning: Comoving wavenumber.
      dimensions: L⁻¹
      default_range: 10⁻⁴ – 10¹ Mpc⁻¹
    - name: a
      meaning: Cosmological scale factor.
      dimensions: dimensionless
      default_range: [0, 1]
  measurement:
    procedures:
      - name: Code-Level Regime Switching
        outline: |
          1. In a cosmological Boltzmann code (e.g., CLASS), evolve the full second-order Klein-Gordon equation for Γ and its perturbation δΓ.
          2. At each time step and for each wavenumber k, evaluate the conditions `m_Γ / H > switch_threshold` (e.g., 50) and `k/a < κ_switch * m_Γ` (e.g., 0.5).
          3. If both conditions are met, replace the δΓ evolution with the first-order fluid equations for δ_Γ and θ_Γ using `c_{s,eff}²`.
          4. Compare the final power spectra (CMB, matter) generated using this procedure against a run using the full field equations at all times. The deviation must be below the target tolerance (e.g., 0.2%).
        expected_signals: [Significant reduction in solver computation time, <0.2% change in CMB and matter power spectra.]
        pitfalls: [Choosing a `switch_threshold` that is too low, causing inaccurate evolution before the oscillatory regime is well-established. Applying the mapping to high-k modes where the approximation breaks down, artificially suppressing small-scale power.]
context_windows:
  - module: COSMO-004
    excerpt: |
      A3. Fluid Mapping (Oscillatory Regime, OPTIONAL)
      When m_Γ ≫ H and the field oscillates rapidly,
      w_Γ ≈ 0,
      c_{s,eff}²(k,a) ≈ (k²/a²) / (4 m_Γ² + k²/a²)
      Evolution equations:
      δ̇_Γ = −(1 + w_Γ)(θ_Γ − 3 Φ̇) − 3H (c_{s,eff}² − w_Γ) δ_Γ
      θ̇_Γ = −H θ_Γ + k² Ψ + k² c_{s,eff}² δ_Γ/(1 + w_Γ)
  - module: COSMO-004
    excerpt: |
      Switching (optional): when m_Γ/H > switch_threshold and k/a < κ_switch m_Γ, route to fluid mapping branch using c_{s,eff}².
poetic_connections:
  motifs: [coarse-graining, effective theory, computational efficiency, stiffness, emergent fluid]
  evocative_lines:
    - "When m_Γ ≫ H and the field oscillates rapidly..."
    - "route to fluid mapping branch"
  association_matrix:
    - [ "FIELD_OSCILLATION", 0.9 ]
    - [ "EFFECTIVE_SOUND_SPEED", 1.0 ]
    - [ "COMPUTATIONAL_STIFFNESS", 0.7 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Effective Sound Speed (c_s²)
      domain: GR
      mapping_kind: mathematical
      equation_hint: |
        c_{s,eff}²(k,a) = (k²/a²) / (4 m_Γ² + k²/a²)
      justification: |
        The derived `c_{s,eff}²` plays the mathematical role of a sound speed in the fluid perturbation equations, governing the balance between pressure support (from the `k² c_{s,eff}² δ_Γ` term) and gravitational collapse (from the `k² Ψ` term). Unlike a simple fluid where `c_s²` is constant, here it is explicitly derived from the underlying field theory and depends on both scale and time.
      references:
        - title: "Cosmology"
          where: "S. Weinberg, Chapter on Scalar Field Perturbations"
          date: 2008-01-01
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "For a Γ-field cosmology with parameters from COSMO-004/D1, the Fluid Mapping with `switch_threshold_m_over_H=50.0` reproduces the full field evolution's CMB and matter power spectra to within 0.2%."
      domain: phenomenology
      falsifier: "A direct numerical experiment comparing two CLASS runs: one with the switch enabled and one with `switch_threshold_m_over_H` set to an arbitrarily large value. A resulting C_l or P(k) difference exceeding 0.2% would falsify the claim for this parameter set."
      status: supported
      links: [COSMO-004]
naming_notes:
  collisions: []
  disambiguation: |
    Distinguish from a fundamental perfect fluid. The Fluid Mapping describes an *effective* or *emergent* fluid whose properties (`w_Γ`, `c_{s,eff}²`) are derived by averaging the underlying field dynamics. Its scale-dependent sound speed is a key feature absent in simple perfect fluids like baryons before decoupling.
crosslinks:
  near_synonyms: [EFFECTIVE_FLUID_APPROXIMATION]
  antonyms: [FULL_FIELD_EVOLUTION]
  prerequisites: [SCALAR_FIELD_COSMOLOGY, KLEIN_GORDON_EQUATION]
  downstream_effects: [POWER_SPECTRUM_CALCULATION, COMPUTATIONAL_STABILITY]
license: CC-BY-SA-4.0
---