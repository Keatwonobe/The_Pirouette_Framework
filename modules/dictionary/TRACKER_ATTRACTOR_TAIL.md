---
term: "Tracker/attractor tail"
canonical_id: "TRACKER_ATTRACTOR_TAIL"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["COSMO-003"]
---

---
term: Tracker/attractor tail
canonical_id: TRACKER_ATTRACTOR_TAIL
symbol: 
aliases: [Shallow potential tail, Coincidence tail]
parents: [COSMO-003]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: COSMO-003
      lines: "Section 5"
      snippet: |
        Mechanism: **tracker/attractor tail** appended to quadratic core of V(Γ), consistent with D2 (analytic, local, scale-covariant). [...] Coincidence arises because slow-roll only turns on when the oscillation amplitude decays into the tail—set by μ, not by arbitrary time.
  editors: [Gemini-1.5-Pro]
  review_log: []
triad:
  art: |
    As the cosmic ringing of the Γ-field fades, its potential flattens into a vast, shallow plain, guiding the universe's expansion into a quiet, accelerating eternity. This is not a new force appearing from nowhere, but the final, exhausted state of an ancient one.
  law: |
    A scalar field potential V(Γ) possesses a tracker/attractor tail if its late-time evolution, for a range of initial conditions, produces a dark energy equation of state w_Γ ≈ -1 and density Ω_Γ ≈ 0.7 today, driven solely by the potential's analytic form and not by fine-tuned timing. The transition from w_Γ ≈ 0 to w_Γ ≈ -1 must be triggered dynamically when the field's oscillation amplitude redshifts into the tail region.
  philosophy: |
    The tail embodies the principle of dynamical resolution, replacing the fine-tuned "cosmic alarm clock" of ΛCDM with an inevitable, attractor-driven mechanism. It posits that dark energy is not a separate substance but the final, quiescent state of the same field that constituted dark matter, thus solving the coincidence problem by making the two phenomena phases of a single entity.
pirouette_definition: |
  A shallow, non-quadratic extension to the core potential V(Γ) of a dark-matter-like scalar field. The tail is constructed to be subdominant during the early, high-amplitude oscillatory phase (where Γ behaves as pressureless matter, w_Γ ≈ 0), but becomes dominant at late times as the field's oscillation amplitude decays due to Hubble expansion. This transition causes the field to enter a slow-roll regime, dynamically evolving its equation of state towards w_Γ ≈ -1 and sourcing cosmic acceleration, thereby providing a unified solution to the dark matter/dark energy coincidence problem.
operational_definition:
  units: Potential V(Γ) is in units of energy density (e.g., eV⁴ or M_pl⁴). Parameters μ, m_Γ have units of energy (eV), while Γ, Γ_*, and f are field values (M_pl).
  symbol_table:
    - name: V(Γ)
      meaning: Full scalar field potential, including core and tail.
      dimensions: M L⁻¹ T⁻²
      default_range: "contextual"
    - name: m_Γ
      meaning: Mass term setting the scale of the quadratic core (CDM-like phase).
      dimensions: M
      default_range: O(MeV) - O(GeV)
    - name: μ
      meaning: Energy scale governing the height of the potential tail.
      dimensions: M L^(1/4) T^(-1/2) (as μ⁴ is energy density)
      default_range: "1.0e-33 eV (per COSMO-003)"
    - name: Γ_*, f
      meaning: Field scale governing the width/flatness of the potential tail.
      dimensions: M L T⁻¹ (in natural units)
      default_range: "≫ M_pl"
  measurement:
    procedures:
      - name: Cosmological Parameter Inference
        outline: |
          Perform a joint Bayesian analysis of cosmological observables, primarily CMB temperature/polarization anisotropies (from a modified Boltzmann code like CLASS), Baryon Acoustic Oscillations (BAO), and Type Ia Supernovae (SNe) luminosity distances. The analysis fits the unified Γ model (with a specific tail functional form) to data, constraining tail parameters like μ and Γ_*.
        expected_signals: [Specific evolution of the dark energy equation of state w(z), Late-time Integrated Sachs-Wolfe (ISW) effect distinct from ΛCDM, Characteristic scale-dependent suppression or enhancement of the growth of structure fσ_8(z).]
        pitfalls: [Numerical instabilities in the Boltzmann solver at the transition between oscillatory and slow-roll regimes, Strong degeneracies between tail parameters and other cosmological parameters (e.g., H₀, Ω_b).]
context_windows:
  - module: COSMO-003
    excerpt: |
      **Coincidence Problem: Symmetry‑Compliant Tail**
      Goal: explain ρ_DM ~ ρ_DE today without tuning.
      Mechanism: **tracker/attractor tail** appended to quadratic core of V(Γ), consistent with D2 (analytic, local, scale‑covariant). [...]
      Coincidence arises because slow‑roll only turns on when the oscillation amplitude decays into the tail—set by μ, not by arbitrary time.
  - module: COSMO-003
    excerpt: |
      If m_Γ≈O(MeV), Γ begins oscillating extremely early (T≫MeV); it behaves like CDM thereafter. Late‑time DE behavior requires a shallow tail in V(Γ) that slows the background today (see Sec. 5).
poetic_connections:
  motifs: [Decay, Exhaustion, Attractor, Unification, Hidden landscape, Quiescence]
  evocative_lines:
    - "slow-roll only turns on when the oscillation amplitude decays into the tail"
    - "a symmetry-compliant route to the coincidence problem"
  association_matrix:
    - [ "COINCIDENCE_PROBLEM", 0.9 ]
    - [ "PRESSURON_POTENTIAL", 0.8 ]
    - [ "DYNAMICAL_RESOLUTION", 0.7 ]
formal_mappings:
  candidates:
    - target: Quintessence / Tracker fields
      domain: GR
      mapping_kind: conceptual|mathematical
      equation_hint: |
        V(φ) = M⁴ e^(-αφ/M_pl)  or  V(φ) = M^(4+n) φ^(-n)
      justification: |
        The tracker/attractor tail is a specific implementation of a quintessence model where the scalar field potential drives late-time acceleration. Unlike generic quintessence, the tail is explicitly joined to a quadratic, matter-like potential, unifying two cosmic roles. The "tracker" or "attractor" nature refers to the late-time, stable fixed point in phase space that drives w→-1, a feature shared with classic tracker models.
      references:
        - title: "Cosmological Tracker Solutions"
          where: "Phys. Rev. D 59, 123504"
          date: 1999-05-20
      confidence: 0.9
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The unified Γ-field with a tracker/attractor tail provides a description of cosmological evolution (from CMB to late-time acceleration) that is competitive with or superior to the standard ΛCDM model."
      domain: phenomenology
      falsifier: "A Bayesian evidence comparison from a joint analysis of CMB, BAO, and SNe data decisively favors a two-fluid (ΛCDM) model. Alternatively, the best-fit tail parameters required to match late-time data may destroy the required w_Γ≈0 behavior at early times."
      status: proposed
      links: [COSMO-003]
naming_notes:
  collisions: [The term "tracker field" is widely used in cosmology literature.]
  disambiguation: |
    Distinguish from classic "tracker" models where the scalar field's energy density tracks the background radiation or matter density for a prolonged period. In the Pirouette context, the "tracker/attractor" property specifically refers to the late-time evolution towards a de Sitter-like fixed point (w_Γ ≈ -1) once the field amplitude has decayed sufficiently to enter the shallow tail of the potential.
crosslinks:
  near_synonyms: []
  antonyms: [COSMOLOGICAL_CONSTANT]
  prerequisites: [PRESSURON, MISALIGNMENT_MECHANISM]
  downstream_effects: [LATE_ISW_EFFECT, COSMIC_ACCELERATION]
license: CC-BY-SA-4.0
---

# Tracker/attractor tail

## Canonical (Pirouette)
A shallow, non-quadratic extension to the core potential V(Γ) of a dark-matter-like scalar field. The tail is constructed to be subdominant during the early, high-amplitude oscillatory phase (where Γ behaves as pressureless matter, w_Γ ≈ 0), but becomes dominant at late times as the field's oscillation amplitude decays due to Hubble expansion. This transition causes the field to enter a slow-roll regime, dynamically evolving its equation of state towards w_Γ ≈ -1 and sourcing cosmic acceleration, thereby providing a unified solution to the dark matter/dark energy coincidence problem.

## EFT-First Summary
The tracker/attractor tail is a specific form of a **Quintessence** potential, where a scalar field drives cosmic acceleration. Unlike generic models, it is explicitly appended to a massive quadratic potential, `½ m_Γ² Γ²`, which governs the field's early behavior as Cold Dark Matter. The tail, often modeled as an exponential or cosine function, creates a late-time dynamical attractor in the field's phase space, forcing the equation of state `w` towards -1. This construction attempts to unify the dark matter and dark energy phenomena within a single degree of freedom.

Reference: P. J. Steinhardt, L. Wang, I. Zlatev, "Cosmological Tracker Solutions", [Phys. Rev. D 59, 123504 (1999)](https://doi.org/10.1103/PhysRevD.59.123504).

## Glossary Links
- See also: PRESSURON, COINCIDENCE_PROBLEM, MISALIGNMENT_MECHANISM