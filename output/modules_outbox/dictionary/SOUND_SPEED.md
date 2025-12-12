---
term: "Sound speed"
canonical_id: "SOUND_SPEED"
symbol: "c_s²"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["COSMO-005"]
---

---
term: Sound speed
canonical_id: SOUND_SPEED_SQUARED
symbol: c_s²
aliases: []
parents: [COSMO-005]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: COSMO-005
      lines: "L11-L12"
      snippet: |
        Sound speed & dispersion:
        • c_s^2(a) = ∂p/∂ρ|_{n} = [∂P/∂X]/[m_H ∂n/∂X + …]
  editors: [agent:autocompleter]
  review_log: []
triad:
  art: |
    The whisper of a wave passing through the cosmic sea, its speed set not by water's press but by the internal tension of the superfluid itself. It is the echo of structure, propagating at a rate dictated by the fundamental grammar of P(X).
  law: |
    The squared sound speed, `c_s²`, is the ratio of the change in the superfluid's pressure to the change in its energy density at constant number density, `∂p/∂ρ|_{n}`. It must be non-negative (`c_s² ≥ 0`) to prevent catastrophic gradient instability.
  philosophy: |
    Sound speed governs the superfluid's response to gravity. A high `c_s²` creates a pressure that resists gravitational collapse, suppressing structure formation below a characteristic scale, while a `c_s²` of zero recovers the behavior of Cold Dark Matter.
pirouette_definition: |
  The squared sound speed, `c_s²`, is a scalar function of scale factor `a` that quantifies the intrinsic propagation speed of perturbations within the `gammat_superfluid`. It is derived from the Pressuron function `P(X)` as `c_s²(a) = [∂P/∂X] / [∂ρ/∂X]`, evaluated on the background cosmological trajectory. `c_s²` directly sets the pressure support against gravitational collapse, defining a Jeans-like scale and distinguishing the superfluid from pressureless Cold Dark Matter. In Boltzmann codes, this intrinsic value is modified into a scale-dependent effective sound speed, `c_{s,eff}²(k,a)`, to account for the finite healing length of the fluid.
operational_definition:
  units: dimensionless (in units of c²=1)
  symbol_table:
    - name: c_s²
      meaning: Intrinsic squared sound speed of the superfluid.
      dimensions: dimensionless
      default_range: "[0, 1]; must be ≪ 10⁻⁶ on CMB scales"
    - name: p_Γ
      meaning: Pressure of the superfluid component.
      dimensions: M L⁻¹ T⁻²
      default_range: contextual
    - name: ρ_Γ
      meaning: Energy density of the superfluid component.
      dimensions: M L⁻¹ T⁻²
      default_range: contextual
    - name: P(X)
      meaning: The Pressuron function, defining the fluid's equation of state.
      dimensions: M L⁻¹ T⁻²
      default_range: contextual
    - name: n
      meaning: Background number density of superfluid quanta.
      dimensions: L⁻³
      default_range: contextual
  measurement:
    procedures:
      - name: Cosmological Inference via Boltzmann Solver
        outline: |
          1. Specify the Pressuron model parameters (`PofX_alpha`, `PofX_beta`, etc.).
          2. Evolve the background cosmology in a Boltzmann code to obtain `ρ_Γ(a)` and `p_Γ(a)`.
          3. Numerically compute `c_s²(a) = ∂p/∂ρ` from the background solution.
          4. Evolve linear perturbations using the derived `c_s²` and compare computed CMB and LSS observables against data.
          5. Use a statistical sampler (e.g., MCMC) to constrain the P(X) parameters, which determines the inferred history of `c_s²(a)`.
        expected_signals: [Suppression of small-scale matter power spectrum, Modifications to CMB lensing potential]
        pitfalls: [Degeneracy with other cosmological parameters, Numerical instability if `c_s²` is large or rapidly varying]
context_windows:
  - module: COSMO-005
    excerpt: |
      Sound speed & dispersion:
      • c_s^2(a) = ∂p/∂ρ|_{n} = [∂P/∂X]/[m_H ∂n/∂X + …]
      • Phonon dispersion: ω² = c_s² k² + m_eff² with m_eff² from weak tail breaking; typically m_eff→0 on CMB scales.

      Scale‑dependent effective sound speed used in Boltzmann evolution:
      c_{s,eff}²(k,a) = c_s²(a) / [1 + (k/k_ξ(a))²],  with k_ξ(a)≡1/ξ(a),  ξ(a)=(2 m_H c_s(a))^{−1}.
  - module: COSMO-005
    excerpt: |
      Perturbations (Newtonian gauge, effective fluid):
      ...
      θ_Γ′ = −ℋ θ_Γ + k² Ψ + k² c_{s,eff}² δ_Γ/(1+w_Γ)
      with w_Γ≈0 through recombination (ensure c_{s,eff}² ≪ 10^{−6} on k relevant to ℓ≲2500).
      ...
      Stability & Validation Suite
      • Positivity: ρ_Γ>0, c_s²≥0, c_{s,eff}²≥0; enforce α>0, β∈{0,1/2,1}.
poetic_connections:
  motifs: [fluidity, pressure, suppression, ripple, stiffness]
  evocative_lines:
    - "...reproduces CDM on CMB scales while generating small‑scale suppression and halo cores."
    - "c_s^2(a) = ∂p/∂ρ|_{n}"
  association_matrix:
    - [ "PRESSURON", 0.9 ]
    - [ "EFFECTIVE_FLUID", 0.8 ]
    - [ "JEANS_SCALE", 0.7 ]
formal_mappings:
  candidates:
    - target: Adiabatic sound speed c_s²
      domain: CM|GR
      mapping_kind: mathematical
      equation_hint: |
        c_s² = (∂p/∂ρ)_S
      justification: |
        The definition `c_s² = ∂p/∂ρ` is the standard expression for the squared speed of sound in a fluid, representing the propagation speed of adiabatic density perturbations. The Pirouette implementation for the P(X) superfluid adopts this definition directly to characterize the phonon modes of the condensate.
      references:
        - title: Cosmological Perturbation Theory
          where: Les Houches Lect.Notes 2003
          date: 2004-03-24
      confidence: 1.0
  adopted:
    - target: Adiabatic sound speed squared (c_s² = ∂p/∂ρ)
      rationale: The term, symbol, and definition are identical to standard usage in fluid dynamics and cosmology for the intrinsic propagation speed of linear perturbations. The module's operational definition is a direct application of this concept to the P(X) superfluid.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The squared sound speed must be non-negative (`c_s² ≥ 0`) for the superfluid to be stable against gradient instabilities."
      domain: theory
      falsifier: "A set of P(X) parameters that provides a good fit to cosmological data but results in `c_s² < 0` for any period of cosmic history would falsify the stability premise of the model."
      status: supported
      links: [COSMO-005]
    - statement: "To match ΛCDM on large scales, `c_{s,eff}²` must be `≪ 10⁻⁶` on scales relevant to primary CMB anisotropies (ℓ≲2500)."
      domain: phenomenology
      falsifier: "A best-fit superfluid model that requires `c_{s,eff}² ≥ 10⁻⁶` on CMB scales would be in tension with Planck data, falsifying the claim that this model can mimic CDM on large scales."
      status: proposed
      links: [COSMO-005]
naming_notes:
  collisions: [`c_s` is a standard symbol for sound speed in many fields; cosmological context is crucial.]
  disambiguation: |
    Distinguish between the intrinsic, background sound speed `c_s²(a)` and the scale-dependent *effective* sound speed `c_{s,eff}²(k,a)` used in the Boltzmann solver. The former is a property of the homogeneous fluid, while the latter includes corrections from the superfluid healing length and governs the evolution of k-modes.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [PRESSURON_FUNCTION, SUPERFLUID_EOS]
  downstream_effects: [EFFECTIVE_SOUND_SPEED, STRUCTURE_SUPPRESSION]
license: CC-BY-SA-4.0
---

# Sound speed

## Canonical (Pirouette)
The squared sound speed, `c_s²`, is a scalar function of scale factor `a` that quantifies the intrinsic propagation speed of perturbations within the `gammat_superfluid`. It is derived from the Pressuron function `P(X)` as `c_s²(a) = [∂P/∂X] / [∂ρ/∂X]`, evaluated on the background cosmological trajectory. `c_s²` directly sets the pressure support against gravitational collapse, defining a Jeans-like scale and distinguishing the superfluid from pressureless Cold Dark Matter. In Boltzmann codes, this intrinsic value is modified into a scale-dependent effective sound speed, `c_{s,eff}²(k,a)`, to account for the finite healing length of the fluid.

## EFT-First Summary
In the effective field theory of the Pressuron superfluid, `c_s²` is the adiabatic sound speed squared, `∂p/∂ρ`. It characterizes the stiffness of the dark matter fluid, controlling the propagation of phonon-like excitations. A non-zero `c_s²` introduces a pressure term that counteracts gravity, suppressing the growth of density perturbations below a Jeans-like scale, while `c_s² → 0` recovers the pressureless behavior of standard Cold Dark Matter (CDM).

## Glossary Links
- See also: `EFFECTIVE_SOUND_SPEED`, `PRESSURON`