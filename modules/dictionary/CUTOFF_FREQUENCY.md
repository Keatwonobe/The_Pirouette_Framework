---
term: "Cutoff frequency"
canonical_id: "CUTOFF_FREQUENCY"
symbol: "ω_c"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-GW-QUANTA-001"]
---

---
term: Cutoff frequency
canonical_id: CUTOFF_FREQUENCY
symbol: ω_c
aliases: [Substrate frequency]
parents: [SUBST-001, MATH-GW-QUANTA-001]
children: [XXP-GR-EXP, DYNA-BH-INT-001]
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-GW-QUANTA-001
      lines: "L30-L33"
      snippet: |
        Barrier (substrate) corrections enter as
        ΔL_2 = (1/8ω_c^2) [ c_1 (∂^2 h)^2 + c_2 (∂_α∂_β h_{ij}^{TT})^2 + … ] ,

        leading to a tiny dispersion
        ω^2 = k^2 [ 1 + ζ (k/ω_c)^2 + O((k/ω_c)^4) ] ,
  editors: [AI Assistant]
  review_log: []
triad:
  art: |
    The temporal medium is a fabric woven at a finite resolution. The cutoff frequency is the scale of its threads, below which spacetime appears a seamless continuum, and above which the weave itself begins to sing.
  law: |
    Gravitational wave propagation deviates from the luminal, dispersionless behavior of General Relativity by terms of order (ω/ω_c)², where ω is the wave frequency. This deviation is measurable as a frequency-dependent phase shift or arrival time difference in broadband signals.
  philosophy: |
    The cutoff frequency marks the boundary of General Relativity's domain as an effective theory. It is the most direct scale parameter of the underlying substrate (SUBST-001), transforming spacetime from a passive stage into an active, physical medium with measurable stiffness and granularity. Probing ω_c is probing the fundamental structure of reality.
pirouette_definition: |
  A characteristic angular frequency, intrinsic to the temporal medium, that sets the energy scale at which the medium's granular structure becomes apparent. For gravitational waves with frequency ω ≪ ω_c, propagation is effectively luminal and non-dispersive, recovering General Relativity. As ω approaches ω_c, higher-derivative "barrier" corrections, suppressed by powers of (ω/ω_c), induce observable phenomena such as superluminal dispersion and frequency-dependent phase imprints (e.g., the Γ-lighthouse effect). It defines the upper energy limit for the validity of the low-energy effective gravitational action.
operational_definition:
  units: radians ⋅ s⁻¹
  symbol_table:
    - name: ω_c
      meaning: Cutoff angular frequency of the temporal medium.
      dimensions: T⁻¹
      default_range: > 10²⁵ rad/s (constrained by multi-messenger astronomy)
    - name: ω
      meaning: Angular frequency of a gravitational wave.
      dimensions: T⁻¹
      default_range: 10¹ - 10⁴ rad/s (LIGO/Virgo/Kagra band)
    - name: ζ
      meaning: Dimensionless O(1) coefficient fixing the sign and magnitude of the leading dispersion term.
      dimensions: dimensionless
      default_range: contextual, determined by the medium's response kernel.
  measurement:
    procedures:
      - name: Gravitational Wave Dispersion
        outline: |
          Observe a broadband gravitational wave signal (e.g., a binary black hole inspiral-merger-ringdown). Correlate the arrival time of different frequency components of the signal against the template predicted by General Relativity. A systematic deviation where higher-frequency components arrive earlier or later than predicted, scaling with ω², provides a measurement of the dispersion parameter ζ/ω_c².
        expected_signals: [Frequency-dependent arrival time delay, Phase de-coherence in matched filtering]
        pitfalls: [Mis-modeling of astrophysical source parameters, Frequency-dependent detector calibration errors, Assuming ζ is constant across frequency bands]
      - name: Γ-Lighthouse Phase Imprint
        outline: |
          Measure the accumulated phase shift of a gravitational wave passing through a region with a strong, spatially varying Γ-field (e.g., near a dynamic black hole). The phase shift Δφ is proportional to (ω/ω_c)², providing an independent way to constrain ω_c if the Γ-profile is known or can be inferred.
        expected_signals: [Anomalous phase evolution in GW signal, Non-GR ringdown behavior for black holes]
        pitfalls: [Degeneracy with source inclination or spin parameters, Poorly constrained Γ-field profiles]
context_windows:
  - module: MATH-GW-QUANTA-001
    excerpt: |
      At quadratic order the GW sector is luminal and dispersionless in the IR; barrier effects enter at O((ω/ω_c)^2). ... Barrier (substrate) corrections enter as ΔL_2 = (1/8ω_c^2) [ c_1 (∂^2 h)^2 + ... ], leading to a tiny dispersion ω^2 = k^2 [ 1 + ζ (k/ω_c)^2 + O((k/ω_c)^4) ], with ζ = O(1) fixed by the response kernel of the medium.
  - module: MATH-GW-QUANTA-001
    excerpt: |
      Γ-structure (lighthouse): a slowly varying Γ-profile modifies the local stiffness and induces a phase shift Δφ_GW ≈ κ (ω/ω_c)^2 ∫_path dr [∂_r Γ(r)]^2, with κ determined by the kernel-to-metric dictionary in MATH-GR-001. Observables: frequency-dependent dephasing without new polarizations; handedness-agnostic (affects both +, × equally at leading order).
poetic_connections:
  motifs: [substrate granularity, breaking scale, high-frequency limit, aether friction, crystal phononics]
  evocative_lines:
    - "The graviton is the medium’s cleanest whisper..."
    - "Substrate-specific deviations are suppressed by (E/ω_c)^2..."
  association_matrix:
    - [ "TEMPORAL_MEDIUM", 0.9 ]
    - [ "GAMMA_LIGHTHOUSE_EFFECT", 0.7 ]
    - [ "GRAVITON_DISPERSION", 0.9 ]
    - [ "EFFECTIVE_FIELD_THEORY", 0.8 ]
formal_mappings:
  candidates:
    - target: EFT Cutoff Scale (Λ)
      domain: EFT
      mapping_kind: mathematical
      equation_hint: |
        ΔL ∝ (1/ω_c²) (∂²h)²  ⇔  ΔL_EFT ∝ (1/Λ⁴) R²...
      justification: |
        ω_c serves precisely as the energy scale (up to ħ) at which the low-energy effective theory (General Relativity on CPM) breaks down. The barrier corrections are equivalent to higher-derivative operators in an EFT expansion, suppressed by the cutoff scale Λ, which is here identified with ω_c.
      references:
        - title: Effective Field Theory
          where: Chapter 1, Georgi, H. (1994)
          date: 1994-11-21
      confidence: 0.95
  adopted:
    - target: EFT Cutoff Scale (Λ)
      rationale: The mapping is direct and functionally identical. It correctly frames GR on CPM as a low-energy limit and ω_c as the scale of new physics.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "Gravitational waves in vacuum exhibit a non-zero dispersion scaling as ω² ≈ k²(1 + ζ(k/ω_c)²)."
      domain: phenomenology
      falsifier: "Persistent null results from broadband GW sources across all accessible frequencies, which would place an ever-increasing lower bound on ω_c, potentially pushing it beyond any testable regime."
      status: proposed
      links: [XXP-GR-EXP]
    - statement: "The leading-order dispersion effect is polarization-independent, affecting + and × modes equally."
      domain: theory
      falsifier: "Observation of frequency-dependent delays that are different for the two tensor polarizations, which would falsify the specific correction structure in MATH-GW-QUANTA-001."
      status: proposed
      links: [MATH-GW-QUANTA-001]
naming_notes:
  collisions: [Filter cutoff frequency (signal processing), Debye frequency (condensed matter)]
  disambiguation: |
    This is a fundamental physical constant of the temporal medium, not a parameter of an experimental apparatus or data analysis pipeline. Unlike the Debye frequency, which relates to the maximum phonon frequency in a crystal lattice, ω_c applies to the fabric of spacetime itself.
crosslinks:
  near_synonyms: [SUBSTRATE_SCALE]
  antonyms: [INFRARED_LIMIT]
  prerequisites: [TEMPORAL_MEDIUM, COHERENCE_PRESERVING_MANIFOLD]
  downstream_effects: [GRAVITON_DISPERSION, GAMMA_LIGHTHOUSE_EFFECT]
license: CC-BY-SA-4.0
---

# Cutoff frequency

## Canonical (Pirouette)
A characteristic angular frequency, intrinsic to the temporal medium, that sets the energy scale at which the medium's granular structure becomes apparent. For gravitational waves with frequency ω ≪ ω_c, propagation is effectively luminal and non-dispersive, recovering General Relativity. As ω approaches ω_c, higher-derivative "barrier" corrections, suppressed by powers of (ω/ω_c), induce observable phenomena such as superluminal dispersion and frequency-dependent phase imprints (e.g., the Γ-lighthouse effect). It defines the upper energy limit for the validity of the low-energy effective gravitational action.

## EFT-First Summary
The cutoff frequency `ω_c` is the direct analogue of the cutoff scale Λ in an Effective Field Theory (EFT). It represents the energy scale at which the low-energy theory—General Relativity on a Coherence-Preserving Manifold—ceases to be a complete description. New physics originating from the substrate manifests as a series of higher-derivative operators (e.g., `(∂²h)²`) suppressed by powers of `ω_c`, which are testable via precision gravitational wave astronomy.

## Glossary Links
- See also: [Temporal Medium](./TEMPORAL_MEDIUM.md), [Γ-Lighthouse Effect](./GAMMA_LIGHTHOUSE_EFFECT.md), [Graviton Dispersion](./GRAVITON_DISPERSION.md)