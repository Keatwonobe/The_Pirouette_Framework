---
term: "Averaged fluid mapping"
canonical_id: "AVERAGED_FLUID_MAPPING"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["COSMO-003"]
---

---
term: Averaged fluid mapping
canonical_id: AVERAGED_FLUID_MAPPING
symbol: 
aliases: []
parents: [COSMO-003]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: COSMO-003
      lines: "L24-L25"
      snippet: |
        Integrate Γ with stiff solver or averaged fluid mapping when m_Γ≫H (toggle by μ≡m_Γ/H threshold).
  editors: [system]
  review_log: []
triad:
  art: |
    Like a hummingbird's wings blurring into a steady hum, the field's frantic oscillations average into a placid, cosmic fluid. This mapping trades microscopic, intractable detail for macroscopic, observable truth.
  law: |
    When the field oscillation frequency `m_Γ` is much greater than the Hubble rate `H` (e.g., `m_Γ/H > 50`), the time-averaged pressure of the Γ field vanishes (⟨p_Γ⟩ ≈ 0), and its effective sound speed `c_s,eff²` approaches zero for super-horizon modes. This approximation is valid if replacing the full field solver with this mapping changes predicted CMB power spectra by less than 0.2%.
  philosophy: |
    To avoid resolving high-frequency dynamics that have negligible large-scale effects, the mapping asserts that a time-averaged description is not just sufficient but computationally superior. It is a pragmatic concession to physical scale separation that elevates the effective, emergent behavior over the exact, microscopic evolution.
pirouette_definition: |
  A numerical technique used in Boltzmann codes to model a rapidly oscillating scalar field, Γ, whose mass `m_Γ` is much larger than the Hubble rate `H`. The mapping replaces the stiff differential equations of the exact field with the evolution equations for an effective fluid with a time-averaged equation of state `w_Γ ≈ 0` and an effective sound speed `c_s,eff²` that approaches zero on large scales (`k/a ≪ m_Γ`). This method significantly improves computational efficiency without compromising accuracy on cosmological observables like CMB spectra.
operational_definition:
  units: Dimensionless (it is a computational procedure)
  symbol_table:
    - name: μ
      meaning: Ratio of field mass to Hubble rate, `m_Γ/H`, used as the switching threshold trigger.
      dimensions: dimensionless
      default_range: Threshold is typically `~50`.
    - name: w_Γ
      meaning: Time-averaged equation of state parameter for the Γ fluid.
      dimensions: dimensionless
      default_range: `≈ 0` in the oscillatory regime.
    - name: c_s,eff²
      meaning: Effective squared sound speed of the Γ fluid, which suppresses small-scale perturbations.
      dimensions: dimensionless
      default_range: `[0, 1]`
  measurement:
    procedures:
      - name: Boltzmann Code Validation
        outline: |
          1. Implement both the full differential equations for Γ perturbations and the averaged fluid equations in a Boltzmann code (e.g., CLASS).
          2. Define a threshold parameter, `use_averaging_threshold` (e.g., 50), which triggers the switch when `m_Γ/H` exceeds it.
          3. During cosmological evolution, solve the fluid equations if `m_Γ/H` is above the threshold; otherwise, solve the full field equations.
          4. Compute CMB spectra and other observables using this hybrid solver.
          5. Validate the mapping by varying the threshold by a factor of 2 and confirming that computed spectra change by less than the target precision (e.g., 0.2%).
        expected_signals: [Consistent CMB TT/TE/EE power spectra matching the ΛCDM limit, Computational logs indicating solver switches at predicted scale factors]
        pitfalls: [Numerical instability at the solver switch point, Incorrect calculation of `c_s,eff²` leading to power spectrum artifacts on small scales]
context_windows:
  - module: COSMO-003
    excerpt: |
      Integrate Γ with stiff solver or averaged fluid mapping when m_Γ≫H (toggle by μ≡m_Γ/H threshold). Match to effective CDM when oscillatory; keep exact background if slow‑rolling.
  - module: COSMO-003
    excerpt: |
      Fluid mapping (oscillatory regime): Treat Γ as an effective fluid with w_Γ≈0, c_s,eff² ≈ ⟨(k²/a²)/(4m_Γ² + (k²/a²))⟩ → 0 on large scales; include small scale suppression if needed. ... Provide both solvers and switch based on m/H and k/a relative to m_Γ.
poetic_connections:
  motifs: [coarse-graining, smoothing, averaging, effective theory, scale separation]
  evocative_lines:
    - "Γ oscillates and time‑averages to a pressureless fluid."
  association_matrix:
    - [ "PRESSURON", 0.8 ]
    - [ "BOLTZMANN_IMPLEMENTATION", 0.9 ]
    - [ "COSMIC_COINCIDENCE", 0.3 ]
formal_mappings:
  candidates:
    - target: WKB Approximation
      domain: Math
      mapping_kind: conceptual
      equation_hint: |
        ψ(x) ≈ A(x) exp[i S(x)/ħ]
      justification: |
        The mapping relies on a separation of scales between the rapid field oscillation (frequency `m_Γ`) and the slow cosmological expansion (frequency `H`). This is the core condition for the WKB method, where one averages over the fast oscillatory phase to find the slow evolution of the amplitude.
      references: []
      confidence: 0.8
  adopted:
    - target: Effective Fluid Description of a Scalar Field
      domain: GR
      mapping_kind: mathematical
      equation_hint: |
        p_Γ = ½Γ̇²−V(Γ), ρ_Γ = ½Γ̇²+V(Γ). For V=½m²Γ², ⟨p_Γ⟩ ≈ 0.
      rationale: |
        This is a standard technique in cosmology. A scalar field oscillating in a quadratic potential has a time-averaged pressure of zero, making it a perfect mathematical model for cold dark matter. The averaged fluid mapping is the direct computational implementation of this principle.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The averaged fluid mapping, when triggered by `m_Γ/H > 50`, accurately reproduces the cosmological effects of an oscillating Γ field, with deviations in CMB power spectra of less than 0.2% compared to a full field solution."
      domain: phenomenology
      falsifier: "Demonstrating that for a physically relevant potential V(Γ), a significant k-mode or time period exists where `m_Γ/H > 50` but the fluid approximation yields >0.2% errors in spectra, indicating a breakdown of the time-averaging assumption due to resonance or other effects."
      status: proposed
      links: [COSMO-003]
naming_notes:
  collisions: ["Fluid mapping" is a general term in hydrodynamics.]
  disambiguation: |
    Distinguish from generic "dark matter fluid models". This mapping is a specific computational approximation for a fundamental scalar field in the `m_Γ ≫ H` regime, derived by time-averaging its oscillatory dynamics, not an axiomatically postulated fluid.
crosslinks:
  near_synonyms: []
  antonyms: [full_field_solver]
  prerequisites: [PRESSURON]
  downstream_effects: [CMB_SPECTRA, MATTER_POWER_SPECTRUM]
license: CC-BY-SA-4.0
---

# Averaged fluid mapping

## Canonical (Pirouette)
A numerical technique used in Boltzmann codes to model a rapidly oscillating scalar field, Γ, whose mass `m_Γ` is much larger than the Hubble rate `H`. The mapping replaces the stiff differential equations of the exact field with the evolution equations for an effective fluid with a time-averaged equation of state `w_Γ ≈ 0` and an effective sound speed `c_s,eff²` that approaches zero on large scales (`k/a ≪ m_Γ`). This method significantly improves computational efficiency without compromising accuracy on cosmological observables like CMB spectra.

## EFT-First Summary
In standard cosmological perturbation theory, a scalar field oscillating rapidly in a quadratic potential behaves as a pressureless fluid (`w=0`), i.e., cold dark matter. The averaged fluid mapping is a direct computational implementation of this principle, treating the Γ field as an effective fluid with `w_Γ ≈ 0` and a non-zero effective sound speed `c_s,eff²` that prevents collapse on scales smaller than the field's effective Jeans length. This is a well-established method for modeling axion-like particles or other oscillating scalar dark matter candidates (see, e.g., Turner, M. S. (1983), Phys. Rev. D, 28(6), 1243).

## Glossary Links
- See also: [PRESSURON](<#>), [COSMIC_COINCIDENCE](<#>)