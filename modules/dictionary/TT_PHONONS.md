---
term: "TT-phonons"
canonical_id: "TT_PHONONS"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-BH-INT-001"]
---

---
term: TT-phonons
canonical_id: TT_PHONONS
symbol: 
aliases: []
parents: [DYNA-BH-INT-001, MATH-GW-QUANTA-001]
children: [XXP-GR-EXP]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DYNA-BH-INT-001
      lines: "L92-L96"
      snippet: |
        Adopt the TT-phonon action & propagator from **MATH-GW-QUANTA-001**; propagate through the interior as a **piecewise medium**:

        - **Phase shift through Γ-core (your lighthouse):**
  editors: [GPT-4]
  review_log: []
triad:
  art: |
    The standard gravitational wave, upon entering the crystalline core of a black hole, travels not through a void but a medium. Like light passing through a diamond, its path is subtly altered, and it emerges carrying a faint, precisely-timed echo of the structure within.
  law: |
    The quanta of tensor-transpose gravitational perturbations propagate through a Γ-structured medium, acquiring a frequency-dependent phase shift Δφ_GW proportional to (ω/ω_c)^2 and an integral over the medium's gradient-squared, (∂Γ)^2. All other polarizations are forbidden.
  philosophy: |
    TT-phonons enable new physics inside black holes without breaking fundamental exterior symmetries like the Equivalence Principle or introducing new propagating modes in the vacuum. They provide a minimal, falsifiable mechanism to connect the deep interior structure to observable, late-time gravitational wave signals.
pirouette_definition: |
  The quantized excitations of the tensor-transpose (TT) gravitational field within a material phase of the temporal medium (e.g., a Γ-structured black hole core). These are not new fundamental particles but are the standard GR gravitons behaving as quasiparticles (phonons) with a non-trivial, medium-dependent dispersion relation that deviates from the vacuum c=1 case only at high frequencies, scaling with (ω/ω_c)^2. Their propagation preserves the two-polarization structure of General Relativity, consistent with the Constrained Polarization Medium (CPM) charter.
operational_definition:
  units: Dimensionless (quanta count) or Radians (for associated phase shift).
  symbol_table:
    - name: Δφ_GW
      meaning: Accumulated GW phase shift after traversing the core medium.
      dimensions: dimensionless
      default_range: "10^-3 – 10^-1 rad"
    - name: ω
      meaning: Angular frequency of the gravitational wave.
      dimensions: T^-1
      default_range: "10^2 – 10^4 Hz (LIGO/Virgo/LISA)"
    - name: ω_c
      meaning: Saturation frequency scale set by the core medium's stiffness (barrier finiteness).
      dimensions: T^-1
      default_range: "≈ Planck Frequency"
    - name: Γ(r)
      meaning: Scalar field profile describing the state of the interior medium.
      dimensions: "contextual (often M^1 L^-1)"
      default_range: "contextual"
  measurement:
    procedures:
      - name: Ringdown Phase Coherency Analysis
        outline: |
          1. Observe a black hole merger and isolate the post-merger ringdown signal.
          2. Fit the quasi-normal mode (QNM) spectrum using a standard GR template.
          3. Measure the residual phase evolution as a function of frequency across multiple modes.
          4. Test for a phase drift component that scales quadratically with frequency, Δφ ∝ ω^2.
        expected_signals: [A frequency-dependent dephasing of QNMs, most prominent in higher-frequency modes.]
        pitfalls: [Signal-to-noise limitations at high frequencies, spectral leakage, confusion with non-linear GR effects or environmental noise.]
context_windows:
  - module: DYNA-BH-INT-001
    excerpt: |
      **Grounding**: emergent metric & constitutive law from SUBST-001; GR hydrodynamic limit; GW sector (2 TT pols, luminal; dispersion only at (ω/ω_c)^2).
  - module: DYNA-BH-INT-001
    excerpt: |
      Adopt the TT-phonon action & propagator from **MATH-GW-QUANTA-001**; propagate through the interior as a **piecewise medium**:

      - **Phase shift through Γ-core (your lighthouse):**
      \[
      \Delta\phi_{\rm GW} \simeq \kappa \left(\frac{\omega}{\omega_c}\right)^2
      \int_0^{r_\ast}\!dr\, \big(\partial_r \Gamma(r)\big)^2 ,
      \]
      (Luminal in IR; correction only at barrier order.)
poetic_connections:
  motifs: [crystal optics, deep-earth seismology, acoustic resonance, lighthouse beam]
  evocative_lines:
    - "the graviton counts its threads as a barely-audible delay."
    - "The singularity is replaced by a phase—a yolk of time under pressure."
  association_matrix:
    - [ "Γ-Saturated Core", 0.9 ]
    - [ "Barrier Finiteness", 0.8 ]
    - [ "Ringdown Echo", 0.6 ]
    - [ "CPM", 0.9 ]
formal_mappings:
  candidates:
    - target: Phonon (quasiparticle)
      domain: CM
      mapping_kind: conceptual
      equation_hint: |
        ω(k)^2 = c_s^2 k^2 (1 - a^2 k^2)
      justification: |
        The TT-phonon is a quantized excitation of a wave in a medium, analogous to a sound quantum (phonon) in a crystal lattice. The (ω/ω_c)^2 dispersion relation is conceptually similar to lattice dispersion corrections in solid-state physics, where the wave speed is modified at high wavenumbers.
      references:
        - title: Solid State Physics
          where: Ashcroft & Mermin, Ch. 22
          date: 1976-01-01
      confidence: 0.8
    - target: Graviton in a medium
      domain: GR
      mapping_kind: operational
      equation_hint: |
        □h_μν + M_μναβ h^αβ = 0
      justification: |
        Within the Γ-structured core, the effective metric experienced by perturbations is modified. This is equivalent to a graviton propagating through a medium with a non-trivial refractive index, leading to phase velocity changes and potential reflection, without altering its fundamental tensor-transpose nature.
      references:
        - title: Black-hole echology: The status of the firewall-echo debate
          where: arXiv:1803.04854
          date: 2018-03-13
      confidence: 0.7
  adopted:
    - target: 
      rationale: 
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "Propagating gravitational waves have only two (tensor-transpose) polarizations everywhere, inside and outside the black hole core."
      domain: phenomenology
      falsifier: "Detection of any scalar or vector polarization mode in a GW signal, especially from a compact binary coalescence."
      status: proposed
      links: [DYNA-BH-INT-001]
    - statement: "The phase velocity of TT-phonons inside the core deviates from c=1 with a frequency dependence of (ω/ω_c)^2."
      domain: phenomenology
      falsifier: "Measurement of a ringdown signal with a phase drift that is either non-existent, scales differently with frequency (e.g., ω^1, ω^-1), or is inconsistent with the integral over (∂Γ)^2."
      status: proposed
      links: [XXP-GR-EXP]
    - statement: "The reflectivity of the core boundary for TT-phonons is tiny and suppressed by the barrier scale ω_c."
      domain: experiment
      falsifier: "Detection of loud, broadband, repeating gravitational wave echoes following a black hole merger."
      status: proposed
      links: [DYNA-BH-INT-001]
naming_notes:
  collisions: [The term "phonon" is standard in condensed matter physics. The prefix "TT-" is critical to specify that only the tensor-transpose modes are involved, distinguishing it from hypothetical scalar or vector phonons in other theories.]
  disambiguation: |
    TT-phonons are not new fundamental particles. They represent the standard GR graviton (a quantized TT perturbation) as it propagates through the specific medium of a Γ-structured black hole core. The "phonon" descriptor refers to its behavior as a quasiparticle in that medium, not its nature in a vacuum.
crosslinks:
  near_synonyms: []
  antonyms: [Scalar Graviton, Vector Graviton]
  prerequisites: [BARRIER_FINITENESS, CPM]
  downstream_effects: [RINGDOWN_PHASE_DRIFT, PHOTON_RING_SHIFTS]
license: CC-BY-SA-4.0
---

# TT-phonons

## Canonical (Pirouette)
The quantized excitations of the tensor-transpose (TT) gravitational field within a material phase of the temporal medium (e.g., a Γ-structured black hole core). These are not new fundamental particles but are the standard GR gravitons behaving as quasiparticles (phonons) with a non-trivial, medium-dependent dispersion relation that deviates from the vacuum c=1 case only at high frequencies, scaling with (ω/ω_c)^2. Their propagation preserves the two-polarization structure of General Relativity, consistent with the Constrained Polarization Medium (CPM) charter.

## EFT-First Summary
From an effective field theory perspective, TT-phonons are the standard massless spin-2 gravitons propagating through a region where higher-dimension operators, suppressed by a high-energy scale ω_c, become relevant. This introduces a non-trivial refractive index `n(ω) ≈ 1 + O(ω²/ω_c²)`, modifying the dispersion relation without introducing new propagating degrees of freedom. This behavior is analogous to a phonon in a crystal, where wave propagation is altered by the discrete lattice structure at high momentum.

## Glossary Links
- See also: CPM, Ringdown Phase Drift, Barrier Finiteness