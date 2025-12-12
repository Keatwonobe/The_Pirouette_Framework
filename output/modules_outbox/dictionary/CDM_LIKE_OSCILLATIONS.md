---
term: "CDM-like Oscillations"
canonical_id: "CDM_LIKE_OSCILLATIONS"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["COSMO-Γ-001_the_early_universe"]
---

---
term: CDM-like Oscillations
canonical_id: CDM_LIKE_OSCILLATIONS
symbol: ⟨w_Γ⟩ ≈ 0
aliases: [Matter-like Oscillations, Pressureless Fluid Mimicry]
parents: [COSMO-Γ-001_the_early_universe]
children: [COSMO-Γ-CMB, COSMO-Γ-HALO]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: COSMO-Γ-001_the_early_universe
      lines: "§2"
      snippet: |
        Thereafter (Γ) oscillates and time-averages to a pressureless fluid ( ( \langle p_\Gamma \rangle \simeq 0 ) ), i.e., CDM-like behavior.
  editors: [GPT-4 (Pirouette Agent)]
  review_log: []
triad:
  art: |
    Γ begins frozen, takes its first breath when H ~ m_Γ, and then beats like a hidden metronome that matter can’t hear—a rhythm that dictates the gravitational assembly of the cosmos.
  law: |
    When the Hubble rate H is much smaller than the pressuron mass m_Γ, the Γ field oscillates rapidly around its potential minimum, causing its time-averaged equation of state to vanish: ⟨w_Γ⟩ ≡ ⟨p_Γ⟩/⟨ρ_Γ⟩ ≈ 0. Its energy density thus redshifts as ρ_Γ ∝ a⁻³.
  philosophy: |
    To enable unification. This mechanism allows a single field, Γ, to fulfill the dynamical role of Cold Dark Matter in the early universe before transitioning to its late-time role as dark energy, thus addressing the cosmic coincidence problem with a single, continuous history.
pirouette_definition: |
  The early-universe dynamical regime of the Γ field, occurring when H ≪ m_Γ. After being released from initial Hubble friction (see: Misalignment), Γ oscillates rapidly about the minimum of its potential V(Γ). Over a timescale of many oscillations, the kinetic and potential energy contributions to the pressure average out (⟨p_Γ⟩ ≈ 0), causing the field's total energy density to scale as a⁻³, dynamically mimicking a pressureless fluid like Cold Dark Matter. This behavior is foundational to the Γ-field's role as a unified dark sector candidate.
operational_definition:
  units: ⟨ρ_Γ⟩ has units of energy density (J m⁻³). ⟨w_Γ⟩ is dimensionless.
  symbol_table:
    - name: Γ
      meaning: Pressuron field
      dimensions: M
      default_range: contextual
    - name: m_Γ
      meaning: Mass of the Pressuron
      dimensions: M
      default_range: contextual
    - name: H
      meaning: Hubble parameter
      dimensions: T⁻¹
      default_range: contextual
    - name: ρ_Γ, p_Γ
      meaning: Energy density and pressure of Γ
      dimensions: M L⁻¹ T⁻²
      default_range: contextual
    - name: w_Γ
      meaning: Equation of state of Γ
      dimensions: dimensionless
      default_range: [-1, 1]
    - name: ⟨...⟩
      meaning: Time average over many oscillation periods (t >> m_Γ⁻¹)
      dimensions: N/A
      default_range: N/A
  measurement:
    procedures:
      - name: Cosmological Parameter Inference via Boltzmann Code
        outline: |
          Integrate the full Γ-field equations of motion within a modified Boltzmann code (e.g., CLASS, CAMB). Fit the resulting CMB (TT/TE/EE/lensing) and Large-Scale Structure (galaxy clustering, weak lensing) power spectra to observational data (e.g., from Planck, DES, Euclid). The inference on cosmological parameters (Ω_c, H_0, etc.) will constrain the properties of the Γ field (m_Γ, initial amplitude) that produce the CDM-like phase.
        expected_signals: [A matter-radiation equality epoch and subsequent growth of structure consistent with standard ΛCDM, A small contribution to ΔN_eff, Scale-dependent deviations in the matter power spectrum]
        pitfalls: [Numerical instability in the solver when m_Γ ≫ H, Incorrect application of the averaged-fluid mapping, Degeneracies with other cosmological parameters]
context_windows:
  - module: COSMO-Γ-001_the_early_universe
    excerpt: |
      Thereafter (Γ) oscillates and time-averages to a pressureless fluid ( ( \langle p_\Gamma \rangle \simeq 0 ) ), i.e., CDM-like behavior. Implementation follows the averaged-fluid mapping when (m_\Gamma \gg H) with a stiff solver fallback.
  - module: COSMO-Γ-001_the_early_universe
    excerpt: |
      We adopt the **quadratic-plus-tail** potentials already allowed in your base module, which yield CDM-like behavior **early** and a **slow-roll** tendency **late** (addressing coincidence without post-hoc tuning).
poetic_connections:
  motifs: [hidden metronome, cosmic drumbeat, misalignment, unification]
  evocative_lines:
    - "beats like a hidden metronome that matter can’t hear"
    - "...one score, played on a single instrument."
  association_matrix:
    - [ "Misalignment", 0.9 ]
    - [ "Dark Energy Tail", 0.7 ]
    - [ "Coincidence Problem", 0.8 ]
formal_mappings:
  candidates:
    - target: Oscillating scalar field (Fuzzy Dark Matter, Axion-like Particle)
      domain: Cosmology
      mapping_kind: mathematical
      equation_hint: |
        For V(φ) ≈ ½m²φ², ⟨w_φ⟩ = ⟨½φ̇² - ½m²φ²⟩ / ⟨½φ̇² + ½m²φ²⟩ → 0
      justification: |
        This behavior is the canonical mechanism by which a coherently oscillating scalar field, like an axion or other light boson, can form the cold dark matter component of the universe. The time-averaged equation of state approaches zero for a quadratic potential.
      references:
        - title: Cosmological evolution of a scalar field with a V = ½m²φ² potential
          where: Turner, M. S. (1983). Phys. Rev. D, 28(6), 1243.
          date: 1983-09-15
      confidence: 0.95
  adopted:
    - target: Oscillating scalar field as CDM
      rationale: The dynamics described in COSMO-Γ-001_the_early_universe are a direct implementation of this well-established cosmological mechanism.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The early-universe CDM-like Oscillations of the Γ field are sufficient to explain the observed Cold Dark Matter density and its effects on BBN and the CMB without requiring a separate, particulate CDM species."
      domain: phenomenology
      falsifier: "If CMB and LSS data, given a Γ field whose parameters are frozen by late-time observables (e.g., Ω_Γ,0), require a non-zero density for an independent CDM fluid (Ω_cdm > 0) at >5σ significance."
      status: proposed
      links: [COSMO-Γ-001_the_early_universe, COSMO-Γ-CMB]
    - statement: "The transition into the oscillatory phase produces a calculable, small, positive contribution to the effective number of relativistic species, ΔN_eff < 0.3."
      domain: phenomenology
      falsifier: "Future BBN and CMB measurements constrain ΔN_eff to a value inconsistent with the range predicted by the allowed class of V(Γ) potentials and one-shot anchorings."
      status: proposed
      links: [COSMO-Γ-001_the_early_universe]
naming_notes:
  collisions: []
  disambiguation: |
    This term describes the *early-time behavior* of the Γ field, not the field itself. It must be distinguished from the field's late-time behavior as a slow-rolling "Dark Energy Tail". The mechanism is "CDM-like," but the underlying physics is that of a scalar field, not a collection of massive particles.
crosslinks:
  near_synonyms: [MISALIGNMENT_MECHANISM]
  antonyms: [VACUUM_LIKE_ENERGY, SLOW_ROLL_TAIL]
  prerequisites: [MISALIGNMENT]
  downstream_effects: [DARK_ENERGY_TAIL, SOLITON_CORES]
license: CC-BY-SA-4.0
---

# CDM-like Oscillations

## Canonical (Pirouette)
The early-universe dynamical regime of the Γ field, occurring when H ≪ m_Γ. After being released from initial Hubble friction (see: Misalignment), Γ oscillates rapidly about the minimum of its potential V(Γ). Over a timescale of many oscillations, the kinetic and potential energy contributions to the pressure average out (⟨p_Γ⟩ ≈ 0), causing the field's total energy density to scale as a⁻³, dynamically mimicking a pressureless fluid like Cold Dark Matter. This behavior is foundational to the Γ-field's role as a unified dark sector candidate.

## EFT-First Summary
In standard cosmological and effective field theory language, CDM-like Oscillations correspond to the well-understood behavior of a coherently oscillating scalar field (such as an axion-like particle) in an expanding universe. When the field's mass (`m_Γ`) is much larger than the Hubble rate (`H`), for a simple quadratic potential (`V(Γ) ≈ ½m_Γ²Γ²`), its energy density redshifts as pressureless matter (`ρ_Γ ∝ a⁻³`). This allows a fundamental scalar field to constitute the Cold Dark Matter component of the cosmos (Turner 1983).

## Glossary Links
- See also: Misalignment, Dark Energy Tail, Coincidence Problem