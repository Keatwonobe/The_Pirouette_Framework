---
term: "Oscillation-phase drift"
canonical_id: "OSCILLATION_PHASE_DRIFT"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-Γ-005_the_pressuron_induced_neutrino_mass_mechanism"]
---

---
term: Oscillation-phase drift
canonical_id: OSCILLATION_PHASE_DRIFT
symbol: δφ_E
aliases: [energy-dependent phase shift, non-sinusoidal modulation]
parents: [MATH-Γ-005]
children: [DYNA-Γ-NEU-OSC]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-Γ-005
      lines: "§5"
      snippet: |
        Because m_ν(E) varies with energy, the oscillation phase becomes
        [ φ_{ij} = \frac{\Delta m_{ij}^2(E),L}{2E} = \frac{L}{2E} \left[m_i(E)^2 - m_j(E)^2\right], ]
        producing a small non-sinusoidal modulation at long baselines. Pirouette predicts an energy-dependent drift of order 1–2 % in oscillation maxima across 1–10 GeV beams—detectable in DUNE or Hyper-Kamiokande with high statistics.
  editors: [auto-agent]
  review_log: []
triad:
  art: |
    Every oscillation is a faint echo of temporal drag. It is the whisper of a wave's coherence feeling its own delay, a heartbeat of spacetime slightly slowed by its own motion.
  law: |
    The energy location of neutrino oscillation maxima systematically shifts by 1–2% across the 1–10 GeV energy range, as a direct consequence of the inverse-energy dependence of neutrino mass (m_ν ∝ 1/E_ν). This deviation from a pure sinusoidal probability curve is a primary test of the coherence-drag mass mechanism.
  philosophy: |
    This effect provides a definitive, falsifiable test distinguishing the Pressuron-induced mass mechanism from standard constant-mass terms or sterile neutrino models. Its detection would confirm that mass is not a static property but a dynamic interaction with the temporal background.
pirouette_definition: |
  The energy-dependent shift in the phase of neutrino flavor oscillations, resulting from the inverse-energy scaling of neutrino masses (m_ν ∝ 1/E_ν) predicted by the Pressuron coherence-drag mechanism. This manifests as a small, non-sinusoidal modulation in the oscillation probability curve, causing the location of probability maxima and minima to drift as a function of neutrino energy.
operational_definition:
  units: dimensionless (fractional shift)
  symbol_table:
    - name: δφ_E
      meaning: Fractional energy-dependent deviation from standard oscillation phase maxima
      dimensions: dimensionless
      default_range: 0.01–0.02 (for 1–10 GeV beams)
    - name: φ_ij(E)
      meaning: Total oscillation phase between flavors i, j as a function of energy
      dimensions: radians
      default_range: contextual
    - name: m_ν(E)
      meaning: Energy-dependent neutrino mass
      dimensions: M (or eV/c²)
      default_range: 0.001–0.05 eV/c²
  measurement:
    procedures:
      - name: Long-Baseline Neutrino Spectroscopy
        outline: |
          Measure the ν_μ → ν_e appearance or ν_μ disappearance probability as a function of reconstructed neutrino energy (E) over a long baseline (L > 1000 km). Compare the observed energy values of the first and second oscillation maxima to the predictions of the standard three-flavor model with constant Δm². The drift is the systematic shift in the energy `E_max` of these maxima relative to the standard sinusoidal prediction.
        expected_signals: [A ~1-2% shift in the energy of the P(ν_μ → ν_e) maximum between the 1-3 GeV and 3-10 GeV bins in DUNE or Hyper-Kamiokande.]
        pitfalls: [Insufficient energy resolution blurring the peak location., Systematic uncertainties in neutrino energy reconstruction mimicking a shift., Degeneracies with non-standard matter effects.]
context_windows:
  - module: MATH-Γ-005
    excerpt: |
      Because m_ν(E) varies with energy, the oscillation phase becomes... producing a small non-sinusoidal modulation at long baselines. Pirouette predicts an energy-dependent drift of order 1–2 % in oscillation maxima across 1–10 GeV beams—detectable in DUNE or Hyper-Kamiokande with high statistics.
  - module: MATH-Γ-005
    excerpt: |
      Failure to detect the predicted energy-dependent drift or a Σmν below 0.05 eV would falsify this minimal Γ-drag model and motivate a hybrid Γ-Higgs Majorana extension (→ DYNA-Γ-NEU-OSC).
poetic_connections:
  motifs: [temporal drag, coherence echo, phase retardation]
  evocative_lines:
    - "slowing the heartbeat of their passage"
    - "Every oscillation is a faint echo of that temporal drag"
  association_matrix:
    - [ "TEMPORAL_DRAG", 0.9 ]
    - [ "PRESSURON", 0.7 ]
    - [ "COHERENCE_DAMPING", 0.5 ]
formal_mappings:
  candidates:
    - target: Deviation from standard P(ν_α → ν_β)
      domain: SM
      mapping_kind: operational
      equation_hint: |
        P(E) ≈ sin²[1.27 Δm²(const) L/E]  →  P(E) ≈ sin²[1.27 Δm²(1/E) L/E]
      justification: |
        In the Standard Model, neutrino mass-squared differences (Δm²) are energy-independent constants. The oscillation-phase drift corresponds to a non-zero energy derivative, d(Δm²)/dE ≠ 0, which is a null effect in the SM but a core prediction of the Pirouette coherence-drag mechanism.
      references:
        - title: Review of Particle Physics
          where: Particle Data Group, "Neutrino Mass, Mixing, and Oscillations"
          date: 2024-08-01
      confidence: 0.3
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The energy of neutrino oscillation maxima shifts by 1–2% over the 1–10 GeV range in long-baseline experiments."
      domain: experiment
      falsifier: "A null result (shift < 0.1% after accounting for systematics) in DUNE or Hyper-K with full experimental statistics."
      status: proposed
      links: [MATH-Γ-005]
naming_notes:
  collisions: [The term "phase drift" is common in electronics and signal processing but is distinguished here by its specific physical origin and energy dependence.]
  disambiguation: |
    Distinguish from 'decoherence', which describes the loss of oscillation amplitude (a reduction in the height of probability maxima). Oscillation-phase drift describes a shift in the *location* of the maxima, not a change in their amplitude.
crosslinks:
  near_synonyms: [ENERGY_DEPENDENT_PHASE_SHIFT]
  antonyms: [SINUSOIDAL_OSCILLATION]
  prerequisites: [PRESSURON_INDUCED_NEUTRINO_MASS_MECHANISM]
  downstream_effects: [RELIC_NEUTRINO_CLUSTERING]
license: CC-BY-SA-4.0
---

# Oscillation-phase drift

## Canonical (Pirouette)
The energy-dependent shift in the phase of neutrino flavor oscillations, resulting from the inverse-energy scaling of neutrino masses (m_ν ∝ 1/E_ν) predicted by the Pressuron coherence-drag mechanism. This manifests as a small, non-sinusoidal modulation in the oscillation probability curve, causing the location of probability maxima and minima to drift as a function of neutrino energy.

## EFT-First Summary
In standard particle physics, neutrino oscillation probability depends on constant mass-squared differences (Δm²). The Pirouette Framework predicts that these Δm² values are not constant but depend inversely on neutrino energy (E), a consequence of its Pressuron-induced mass mechanism. This leads to an "oscillation-phase drift," a measurable, non-standard deviation of 1–2% in the location of oscillation maxima for GeV-scale experiments like DUNE, providing a key falsifiable test against the Standard Model.

## Glossary Links
- See also: [Pressuron](./pressuron.md), [Temporal Drag](./temporal_drag.md), [Neutrino Mass Hierarchy](./neutrino_mass_hierarchy.md)