---
term: "Transverse-Traceless (TT) modes"
canonical_id: "TRANSVERSE_TRACELESS_TT_MODES"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-GW-QUANTA-001"]
---

---
term: Transverse-Traceless (TT) modes
canonical_id: TRANSVERSE_TRACELESS_MODES
symbol: h_{ij}^{TT}
aliases: [TT-phonons, radiative gravitational modes, shear modes]
parents: [SUBST-001, MATH-GR-001, GRW-003]
children: [XXP-GR-EXP, DYNA-BH-INT-001]
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-GW-QUANTA-001
      lines: "L5-L7"
      snippet: |
        Quantize the **two transverse-traceless shear modes** of the temporal medium on a Coherence-Preserving Manifold (CPM), define the canonical normalization, propagator, interaction vertices up to barrier-suppressed order...
  editors: [GPT-4 (Pirouette Dictionary Agent)]
  review_log: []
triad:
  art: |
    The medium’s cleanest whisper: a transverse shiver of the loom. These modes carry pure strain across the cosmos, changing only their timing when they graze the lighthouses of the substrate.
  law: |
    The two physical, propagating degrees of freedom of the gravitational field `h_{ij}` are those satisfying the transverse (`∂^i h_{ij}^{TT}=0`) and traceless (`h^{TT}_{ii}=0`) conditions. All other components are non-radiative or gauge artifacts and are excluded on a Coherence-Preserving Manifold.
  philosophy: |
    TT modes represent information escaping to infinity. In Pirouette, they are not just geometric ripples but the quantized shear excitations—TT-phonons—of the temporal medium itself. Their properties probe the medium's elastic and dispersive nature at high energies.
pirouette_definition: |
  The two dynamical degrees of freedom of the metric perturbation `h_{μν}` that describe propagating gravitational radiation on a Coherence-Preserving Manifold (CPM). They are defined by the Transverse-Traceless (TT) gauge conditions (`∂^i h_{ij}^{TT}=0`, `h^{TT}_{ii}=0`, and `h_{0μ}=0`), which isolate the physical shear polarizations (+, ×) from unphysical scalar and vector modes. In the low-energy (IR) limit, they propagate luminally and without dispersion. At energies approaching the substrate barrier scale `ω_c`, they acquire a small, positive dispersion `ω^2 = k^2 [ 1 + ζ (k/ω_c)^2 + ... ]` and can experience phase shifts from interaction with local Γ-structures (Γ-lighthouse effect).
operational_definition:
  units: Dimensionless (strain)
  symbol_table:
    - name: h_{ij}^{TT}
      meaning: The tensor field representing the TT part of the metric perturbation.
      dimensions: dimensionless
      default_range: 10⁻²³–10⁻²⁰ for detected astrophysical events.
    - name: M_*
      meaning: Reduced Planck scale of the temporal medium, setting the coupling strength.
      dimensions: M
      default_range: contextual, ~10¹⁸ GeV
    - name: ω_c
      meaning: Substrate barrier frequency, setting the scale for dispersive effects.
      dimensions: T⁻¹
      default_range: contextual, >10⁴ Hz
    - name: ε^{(λ)}_{ij}(k)
      meaning: Polarization tensor for the plus (λ=+) or cross (λ=×) modes.
      dimensions: dimensionless
      default_range: normalized basis tensor
  measurement:
    procedures:
      - name: Laser Interferometry
        outline: |
          Measure the differential strain induced by a passing wave on the arms of a Michelson interferometer. A network of spatially separated detectors is used to reconstruct the direction and polarization of the incoming wave by correlating arrival times and signal responses.
        expected_signals:
          - An oscillating strain signal `h(t)` with two independent polarization components (`h_+`, `h_×`).
          - For inspiraling sources, a frequency-dependent dephasing relative to pure GR predictions, scaling with `(ω/ω_c)^2`, indicating dispersion from barrier effects.
        pitfalls:
          - Terrestrial and quantum noise can mask the signal.
          - Degeneracies exist between source parameters (e.g., mass, spin) and potential dispersion effects, requiring high-SNR, broadband signals to disentangle.
context_windows:
  - module: MATH-GW-QUANTA-001
    excerpt: |
      We expand the emergent metric about Minkowski on CPM: g_{μν} = η_{μν} + h_{μν}, with ∂^μ J_μ^Γ = 0. We impose the TT gauge on the radiative modes: h_{0μ}=0, ∂^i h_{ij}^{TT}=0, h^{TT}_{ii}=0. At quadratic order the GW sector is luminal and dispersionless in the IR; barrier effects enter at O((ω/ω_c)^2).
  - module: MATH-GW-QUANTA-001
    excerpt: |
      The Γ-structure (lighthouse): a slowly varying Γ-profile modifies the local stiffness and induces a phase shift Δφ_GW ≈ κ (ω/ω_c)^2 ∫_path dr [∂_r Γ(r)]^2. Observables include frequency-dependent dephasing without new polarizations; the effect is handedness-agnostic, affecting both + and × modes equally at leading order.
poetic_connections:
  motifs: [ripple, shear, whisper, echo, loom, pure radiation]
  evocative_lines:
    - "The graviton is the medium’s cleanest whisper: a transverse shiver of the loom."
    - "When it grazes a Γ-lighthouse, it does not change its voice—only its timing."
  association_matrix:
    - [ "TT_PHONON", 1.0 ]
    - [ "CPM", 0.9 ]
    - [ "GAMMA_LIGHTHOUSE", 0.7 ]
    - [ "GW_DISPERSION", 0.8 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Gravitational wave modes in the Transverse-Traceless gauge
      domain: GR
      mapping_kind: mathematical
      equation_hint: |
        h_{ij}^{TT}(x) = ∑_{λ=+,×} ∫ d³k [ ε^{(λ)}_{ij}(k) a_{k,λ} e^{-ik·x} + h.c. ]
      justification: |
        The definition of TT modes in Pirouette is identical to that in standard General Relativity. They are the components of the metric perturbation `h_{μν}` that satisfy the transverse and traceless conditions, corresponding to the two physical, propagating polarizations of a gravitational wave. Pirouette reinterprets these modes as excitations of a physical medium rather than pure spacetime geometry, leading to new phenomenological effects at high energy.
      references:
        - title: Spacetime and Geometry
          where: Carroll, J. (2004). Chapter 7.
          date: 2004-01-01
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "All propagating gravitational radiation consists exclusively of the two transverse-traceless modes."
      domain: experiment
      falsifier: "The confirmed detection of a gravitational wave signal with a scalar (breathing) or vector polarization component."
      status: supported
      links: [SUBST-001, MATH-GW-QUANTA-001]
    - statement: "TT modes experience a non-GR, frequency-dependent phase shift proportional to (ω/ω_c)² when propagating through regions of non-trivial Γ-structure."
      domain: phenomenology
      falsifier: "Persistent null results in searches for anomalous, frequency-dependent dephasing in binary inspiral signals, setting limits on ω_c that are inconsistent with other framework constraints."
      status: proposed
      links: [XXP-GR-EXP]
naming_notes:
  collisions: [In other fields, "TT" can refer to T-Tauri stars or other acronyms. In the context of General Relativity or gravitational physics, it unambiguously means Transverse-Traceless.]
  disambiguation: |
    The "TT" designation is a gauge choice, not a distinct type of particle. It is the mathematical procedure for isolating the physical, radiative degrees of freedom (`h_+`, `h_×`) from non-propagating parts of the metric perturbation and from coordinate artifacts.
crosslinks:
  near_synonyms: [TT_PHONON]
  antonyms: [SCALAR_GRAVITON_MODE, VECTOR_GRAVITON_MODE]
  prerequisites: [METRIC_PERTURBATION, GAUGE_INVARIANCE]
  downstream_effects: [GW_DISPERSION, GAMMA_LIGHTHOUSE_EFFECT]
license: CC-BY-SA-4.0
---

# Transverse-Traceless (TT) modes

## Canonical (Pirouette)
The two dynamical degrees of freedom of the metric perturbation `h_{μν}` that describe propagating gravitational radiation on a Coherence-Preserving Manifold (CPM). They are defined by the Transverse-Traceless (TT) gauge conditions (`∂^i h_{ij}^{TT}=0`, `h^{TT}_{ii}=0`, and `h_{0μ}=0`), which isolate the physical shear polarizations (+, ×) from unphysical scalar and vector modes. In the low-energy (IR) limit, they propagate luminally and without dispersion. At energies approaching the substrate barrier scale `ω_c`, they acquire a small, positive dispersion `ω^2 = k^2 [ 1 + ζ (k/ω_c)^2 + ... ]` and can experience phase shifts from interaction with local Γ-structures (Γ-lighthouse effect).

## EFT-First Summary
These modes map directly to the two propagating polarizations of a gravitational wave in standard General Relativity, as described in the Transverse-Traceless (TT) gauge (see Carroll, *Spacetime and Geometry*, Ch. 7). Pirouette adopts this standard IR description but reinterprets the modes as TT-phonons of an underlying temporal medium. This interpretation introduces new, non-GR effects at high energies, such as a small dispersion and anomalous phase shifts, which are suppressed by powers of `(E/ω_c)`.

## Glossary Links
- See also: [TT_PHONON](./tt_phonon.md), [GW_DISPERSION](./gw_dispersion.md), [GAMMA_LIGHTHOUSE_EFFECT](./gamma_lighthouse_effect.md)