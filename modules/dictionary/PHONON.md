---
term: "Phonon"
canonical_id: "PHONON"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["SECT-001"]
---

---
term: Phonon
canonical_id: PHONON
symbol: π
aliases: [collective excitation, sound wave, phase perturbation]
parents: [SECT-001]
children: [SECT-Γ-A-HALO, SECT-Γ-A-CMB]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: SECT-001
      lines: "Section 1"
      snippet: |
        Linearization (phonon): θ = θ_0 + π,  n = n_0 + δn  ⇒
        • Equation: (∂*t^2 − c_s^2 ∇^2 + m_eff^2) π = 0
  editors: [Framework AI Agent]
  review_log: []
triad:
  art: |
    The collective whisper of the superfluid, a sound wave sculpting galaxies from the silent cosmic sea. It is the structure of the whole emerging from the dance of its parts.
  law: |
    The phonon's effective sound speed, `c_s,eff(k)`, sets a scale-dependent Jeans length, `k_J(a)`, which suppresses gravitational collapse on small scales (`k > k_J`) and permits it on large scales, thereby sculpting halo cores and cosmic structure.
  philosophy: |
    The phonon exemplifies the principle of emergent complexity: a simple, heavy microscopic constituent (the pressuron) gives rise to a rich, ultralight collective behavior that governs macroscopic phenomena. It replaces the need for a new fundamental ultralight particle with a dynamic excitation of the cosmic medium itself.
pirouette_definition: |
  A quantized, collective, longitudinal excitation of the cosmic superfluid's phase (`θ`) and number density (`n`), analogous to a sound wave. The phonon field (`π`) is the linearized perturbation of the phase (`θ = θ_0 + π`). Its dynamics, governed by a wave equation with a characteristic sound speed (`c_s`) and effective mass (`m_eff`), control the long-wavelength behavior of the superfluid, including pressure support against gravity, structure formation, and macroscopic drag during mergers.
operational_definition:
  units: Dimensionless (radians)
  symbol_table:
    - name: π
      meaning: Phonon field; linearized perturbation of the superfluid phase `θ`.
      dimensions: dimensionless
      default_range: |π| ≪ 1 (linear regime)
    - name: c_s
      meaning: Phonon sound speed.
      dimensions: L T⁻¹
      default_range: c_s ≪ 10⁻³ c (at recombination)
    - name: m_eff
      meaning: Phonon effective mass, arising from explicit symmetry breaking.
      dimensions: M
      default_range: m_eff ≪ m_H
    - name: k_J
      meaning: Jeans wavenumber, the cutoff scale for structure formation.
      dimensions: L⁻¹
      default_range: contextual; k_J ~ aH/c_s
  measurement:
    procedures:
      - name: Cosmological Structure Analysis
        outline: |
          Infer the scale-dependent sound speed `c_s,eff(k,a)` by measuring the suppression of the matter power spectrum for wavenumbers `k` greater than the Jeans scale `k_J`. This involves a combined fit to galaxy clustering, Lyman-alpha forest, and CMB lensing data using a modified Boltzmann solver (e.g., CLASS) that incorporates the superfluid's P(X) equation of state.
        expected_signals: [A scale-dependent cutoff in the matter power spectrum, A specific mass-independent core size in galactic halos]
        pitfalls: [Degeneracy with warm dark matter models or neutrino mass, Contamination from baryonic feedback effects mimicking cores]
      - name: Galaxy Merger Kinematics
        outline: |
          Measure the spatial offset and velocity-dependent drag between colliding galaxy clusters (e.g., Bullet Cluster analogs). The drag is modeled as a consequence of phonon radiation and interface work, allowing inference of `c_s` and surface tension `σ`.
        expected_signals: [A characteristic scaling of merger offsets with relative velocity consistent with the predicted effective cross-section `(σ/m)_eff`]
        pitfalls: [Complex gas dynamics can dominate the drag signal, Viewing angle uncertainties can bias offset measurements]
context_windows:
  - module: SECT-001
    excerpt: |
      Realize the 17 MeV pressuron as a **microscopic constituent** of a cosmic superfluid whose **collective phonon mode** supplies the ultralight, long‑wavelength dynamics needed for structure formation, without introducing a new fundamental particle. Encode the superfluid in a symmetry‑respecting P(X) EFT; derive halo cores, merger behavior, and CMB‑consistent linear perturbations...
  - module: SECT-001
    excerpt: |
      Linearization (phonon): θ = θ_0 + π,  n = n_0 + δn  ⇒
      • Equation: (∂*t^2 − c_s^2 ∇^2 + m_eff^2) π = 0
      with m_eff^2 ≡ ∂^2 V_tail/∂Γ^2|*{bg} + ε(n_0) capturing weak explicit breaking from the Γ‑tail (COSMO‑Γ‑CMB). Typically m_eff ≪ m_H.
  - module: SECT-001
    excerpt: |
      Linear perturbations (Newtonian gauge):
      • Fluid form with **scale‑dependent** c_s,eff^2(k) from the phonon dispersion:
      c_s,eff^2(k) ≈ c_s^2 · [1 + (k/k_ξ)^2]^{−1},  k_ξ ≡ 1/ξ.
      • Jeans‑like cutoff at k_J ~ aH/c_s where growth is suppressed; choose α,β to match halo core scales while keeping CMB acoustic peaks intact (c_s ≪ 10^{−3} at recombination on relevant k).
poetic_connections:
  motifs: [wave, collective, sound, medium, resonance, structure]
  evocative_lines:
    - "vacuum as fuzzy baseline that creeps like the CMB"
    - "collective phonon mode supplies the ultralight, long‑wavelength dynamics"
  association_matrix:
    - [ "SUPERFLUID", 0.95 ]
    - [ "PRESSURON", 0.9 ]
    - [ "SOUND_SPEED_CS", 0.9 ]
    - [ "JEANS_SCALE", 0.8 ]
formal_mappings:
  candidates:
    - target: Scalar field (in cosmology)
      domain: EFT
      mapping_kind: mathematical
      equation_hint: |
        (∂_t^2 − c_s^2 ∇^2 + m_eff^2) π = 0
      justification: |
        In the linear regime, the phonon field `π` obeys a Klein-Gordon equation, behaving as a classical scalar field with a specific sound speed `c_s < 1` and effective mass `m_eff`. This allows its effects to be implemented in cosmological perturbation theory by modifying the fluid equations to include a scale-dependent pressure, rather than adding a new fundamental field component.
      references: []
      confidence: 0.9
  adopted:
    - target: Phonon (in condensed matter/superfluidity)
      rationale: |
        The framework explicitly models the cosmic dark sector as a non-relativistic superfluid. The "phonon" is not an analogy but a direct application of the term for the collective sound-wave excitation (Goldstone mode) in this medium, inheriting its properties like the dispersion relation and sound speed from the underlying P(X) Lagrangian.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The phonon sound speed is sufficiently low (c_s ≪ 10⁻³ c) at recombination to leave CMB acoustic peaks unaltered on measured scales (ℓ ≲ 2500)."
      domain: phenomenology
      falsifier: "Precise CMB measurements detect an anomalous phase shift or damping in the TT/TE/EE power spectra inconsistent with the model's predictions for a given set of frozen P(X) parameters."
      status: proposed
      links: [SECT-001, SECT-Γ-A-CMB]
    - statement: "The phonon-induced effective pressure creates galactic halo cores with a nearly universal surface density Σ₀."
      domain: phenomenology
      falsifier: "A large survey of galaxy rotation curves and density profiles fails to find a constant surface-density relation, or finds one that scales strongly with halo mass."
      status: proposed
      links: [SECT-001, COSMO-Γ-HALO]
    - statement: "Phonon radiation is the primary macroscopic drag mechanism in halo mergers, producing an effective cross-section (σ/m)_eff ≲ 0.2 cm² g⁻¹."
      domain: phenomenology
      falsifier: "Observations of merging clusters require a significantly larger cross-section or a scaling with velocity that is inconsistent with interface dynamics and phonon radiation."
      status: proposed
      links: [SECT-001, COSMO-Γ-MERGE]
naming_notes:
  collisions: [The symbol `π` is also the mathematical constant pi.]
  disambiguation: |
    Distinguish the Pirouette Phonon (`π`), a collective mode of the heavy pressuron superfluid, from a fundamental ultralight scalar particle. The phonon is an emergent, not fundamental, degree of freedom, and its properties (`c_s`, `m_eff`) are determined by the superfluid's equation of state (`P(X)`), not by a fixed particle mass.
crosslinks:
  near_synonyms: [SOUND_WAVE, COLLECTIVE_EXCITATION]
  antonyms: [PRESSURON]
  prerequisites: [SUPERFLUID, PRESSURON, P_OF_X_LAGRANGIAN]
  downstream_effects: [HALO_CORE, JEANS_SCALE, MERGER_DRAG]
license: CC-BY-SA-4.0
---

# Phonon

## Canonical (Pirouette)
A quantized, collective, longitudinal excitation of the cosmic superfluid's phase (`θ`) and number density (`n`), analogous to a sound wave. The phonon field (`π`) is the linearized perturbation of the phase (`θ = θ_0 + π`). Its dynamics, governed by a wave equation with a characteristic sound speed (`c_s`) and effective mass (`m_eff`), control the long-wavelength behavior of the superfluid, including pressure support against gravity, structure formation, and macroscopic drag during mergers.

## EFT-First Summary
The Phonon is the Goldstone boson of the spontaneously broken U(1) symmetry in the cosmic superfluid's P(X) effective field theory. In the linear regime, it behaves as a scalar field `π` obeying a Klein-Gordon equation with a characteristic sound speed `c_s` and a small effective mass `m_eff`. This sound speed introduces an effective pressure that counteracts gravity on small scales, creating a Jeans-like cutoff in the matter power spectrum and sourcing the cores of dark matter halos.

## Glossary Links
- See also: [[PRESSURON]], [[SUPERFLUID]], [[HALO_CORE]]