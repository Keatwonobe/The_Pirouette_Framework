---
term: "TT-Phonon"
canonical_id: "TT_PHONON"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-GW-QUANTA-001"]
---

---
term: TT-Phonon
canonical_id: TT_PHONON
symbol: h_{ij}^{TT}
aliases: [Graviton, Temporal Shear Mode Quantum]
parents: [SUBST-001, MATH-GR-001, GRW-003]
children: [XXP-GR-EXP, DYNA-BH-INT-001]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-GW-QUANTA-001
      lines: "§2"
      snippet: |
        v_{ij} ≡ (M_*/2) h_{ij}^{TT}  ⇒  S_2 = 1/2 ∫ d^4x [ (∂_t v_{ij})^2 − (∇ v_{ij})^2 ] .
  editors: [agent-lark]
  review_log: []
triad:
  art: |
    The graviton is the medium’s cleanest whisper: a transverse shiver of the loom. When it grazes a Γ-lighthouse, it does not change its voice—only its timing.
  law: |
    A TT-Phonon is a massless, spin-2 excitation with two transverse polarizations (+, ×) that propagates luminally in the IR limit (ω << ω_c). Its dispersion relation is ω² = k²[1 + ζ(k/ω_c)² + ...], where ζ > 0. The detection of any non-transverse polarization or a dispersion relation with ζ ≤ 0 falsifies its canonical model.
  philosophy: |
    The TT-Phonon serves as the fundamental quantum of the gravitational interaction, emerging from the collective shear modes of the temporal medium. It bridges the microscopic physics of the substrate (via ω_c corrections) with macroscopic spacetime curvature, realizing General Relativity in the low-energy limit while providing concrete, falsifiable predictions for new physics at high frequencies.
pirouette_definition: |
  A TT-Phonon is the canonical quantum of the transverse-traceless (TT) tensor field `h_{ij}^{TT}` that describes shear deformations of the temporal medium on a Coherence-Preserving Manifold. It is a massless, spin-2 boson with two polarization states (plus, `+`, and cross, `×`). Its dynamics in the infrared limit (ω << ω_c) recover General Relativity's gravitational waves, while interactions with the substrate introduce a characteristic frequency-dependent dispersion `ω² ≈ k²(1 + ζ(k/ω_c)²)`, and phase shifts when propagating through regions of varying Temporal Pressure (`Γ-lighthouse` effect).
operational_definition:
  units: The field h_{ij}^{TT} is dimensionless. The quantum carries energy (J) and momentum (kg⋅m/s).
  symbol_table:
    - name: h_{ij}^{TT}
      meaning: Transverse-traceless metric perturbation field
      dimensions: dimensionless
      default_range: 10⁻²¹ for typical astrophysical signals
    - name: M_*
      meaning: Reduced Planck scale of the medium
      dimensions: M
      default_range: ≈ 2.435 × 10¹⁸ GeV/c²
    - name: ω_c
      meaning: Substrate cutoff frequency
      dimensions: T⁻¹
      default_range: contextual, constrained by experiment
    - name: ζ
      meaning: Leading-order dispersion coefficient
      dimensions: dimensionless
      default_range: O(1)
  measurement:
    procedures:
      - name: Gravitational Wave Interferometry
        outline: |
          Measure the strain `h(t)` induced on interferometers (e.g., LIGO, LISA) by a passing wave. Decompose the signal into polarization modes (+, ×) and analyze the arrival times of different frequency components from a single broadband source (e.g., binary merger chirp) to constrain the dispersion relation.
        expected_signals:
          - Differential arm length changes oscillating at the wave frequency.
          - For broadband signals, a frequency-dependent time-of-flight delay `Δt ∝ ω²` relative to the luminal prediction, indicating `ζ > 0`.
          - A frequency-dependent phase shift `Δφ ∝ (ω/ω_c)²` relative to GR templates, from propagation through a `Γ-lighthouse`.
        pitfalls:
          - Low signal-to-noise ratio obscuring the dispersion effect.
          - Astrophysical source modeling errors being degenerate with the propagation effect.
context_windows:
  - module: MATH-GW-QUANTA-001
    excerpt: |
      Free propagator in momentum space (TT projector Π_{ij,kl}):
      ⟨ h_{ij}^{TT} h_{kl}^{TT} ⟩_0 (ω,k) = (2/M_*^2) · Π_{ij,kl}(k) / (ω^2 − k^2 + i0^+) .
      Barrier (substrate) corrections enter as ΔL_2 = (1/8ω_c^2) [ c_1 (∂^2 h)^2 + … ], leading to a tiny dispersion ω^2 = k^2 [ 1 + ζ (k/ω_c)^2 + O((k/ω_c)^4) ].
  - module: MATH-GW-QUANTA-001
    excerpt: |
      Γ-structure (lighthouse): a slowly varying Γ-profile modifies the local stiffness and induces a phase shift
      Δφ_GW ≈ κ (ω/ω_c)^2 ∫_path dr [∂_r Γ(r)]^2 .
      Observables: frequency-dependent dephasing without new polarizations; handedness-agnostic (affects both +, × equally at leading order).
poetic_connections:
  motifs: [shear, whisper, shimmer, lighthouse, loom]
  evocative_lines:
    - "The graviton is the medium’s cleanest whisper: a transverse shiver of the loom."
    - "When it grazes a Γ-lighthouse, it does not change its voice—only its timing."
  association_matrix:
    - [ "Γ-lighthouse", 0.9 ]
    - [ "Temporal Medium", 0.8 ]
    - [ "General Relativity", 0.7 ]
formal_mappings:
  candidates:
    - target: Graviton
      domain: GR|QFT
      mapping_kind: operational
      equation_hint: |
        L_int = − (1/2) h_{ij}^{TT} T_{ij}^{TT}
      justification: |
        The TT-Phonon is a massless spin-2 quantum field whose low-energy effective action, minimal coupling to the stress-energy tensor, and two transverse polarizations exactly match the properties of the graviton in linearized General Relativity. Deviations only appear as higher-order corrections suppressed by the substrate scale ω_c.
      references:
        - title: Spacetime and Geometry
          where: Carroll, J. (2004), Ch. 7
          date: 2004-01-01
      confidence: 0.95
  adopted:
    - target: Graviton
      rationale: |
        The term 'graviton' is adopted as the primary external alias due to the exact correspondence of the TT-Phonon's IR properties (spin-2, massless, two polarizations, universal coupling to T_μν) with the quantum of linearized General Relativity.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "TT-Phonons possess only two polarization modes (+, ×)."
      domain: experiment
      falsifier: "Detection of any scalar, vector, or other tensor polarization in gravitational waves from any source."
      status: proposed
      links: [MATH-GW-QUANTA-001, SUBST-001]
    - statement: "TT-Phonon propagation exhibits a superluminal group velocity at high frequencies, with dispersion `ω² = k² [ 1 + ζ (k/ω_c)² + ...]` and `ζ > 0`."
      domain: phenomenology
      falsifier: "Measurement of subluminal dispersion (ζ < 0), no dispersion (ζ = 0 up to experimental limits), or a different frequency scaling of the dispersion relation."
      status: proposed
      links: [XXP-GR-EXP, MATH-GW-QUANTA-001]
naming_notes:
  collisions: [The symbol h is common for Planck's constant and Hamiltonians; `h_{ij}` is standard for metric perturbations in GR, making context essential.]
  disambiguation: |
    Distinguish from acoustic phonons in a conventional medium. TT-Phonons are excitations *of* the temporal medium (spacetime analog), not propagating *through* it. The 'TT' prefix is critical, specifying the transverse-traceless shear modes that map to GR, as opposed to hypothetical compressive or other modes of the substrate.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [TEMPORAL_MEDIUM, COHERENCE_PRESERVING_MANIFOLD]
  downstream_effects: [GAMMA_LIGHTHOUSE_EFFECT, GRAVITATIONAL_WAVE_DISPERSION]
license: CC-BY-SA-4.0
---

# TT-Phonon

## Canonical (Pirouette)
A TT-Phonon is the canonical quantum of the transverse-traceless (TT) tensor field `h_{ij}^{TT}` that describes shear deformations of the temporal medium on a Coherence-Preserving Manifold. It is a massless, spin-2 boson with two polarization states (plus, `+`, and cross, `×`). Its dynamics in the infrared limit (ω << ω_c) recover General Relativity's gravitational waves, while interactions with the substrate introduce a characteristic frequency-dependent dispersion `ω² ≈ k²(1 + ζ(k/ω_c)²)`, and phase shifts when propagating through regions of varying Temporal Pressure (`Γ-lighthouse` effect).

## EFT-First Summary
In the low-energy effective field theory, the TT-Phonon is identical to the **graviton** of linearized General Relativity. It is a massless spin-2 field `h_{ij}` in the transverse-traceless gauge that couples universally to the stress-energy tensor `T_{ij}`. Pirouette-specific physics emerges as higher-derivative operators suppressed by the substrate cutoff scale `ω_c`, leading to phenomena like weak, superluminal dispersion of gravitational waves at high frequencies.

## Glossary Links
- See also: [Temporal Medium](<placeholder>), [Γ-lighthouse](<placeholder>), [Gravitational Wave Dispersion](<placeholder>)