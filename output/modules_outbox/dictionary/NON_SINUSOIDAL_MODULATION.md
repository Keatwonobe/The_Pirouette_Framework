---
term: "Non-sinusoidal modulation"
canonical_id: "NON_SINUSOIDAL_MODULATION"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-Γ-005_the_pressuron_induced_neutrino_mass_mechanism"]
---

---
term: Non-sinusoidal modulation
canonical_id: NON_SINUSOIDAL_MODULATION
symbol: 
aliases: [oscillation-phase drift, energy-dependent phase shift]
parents: [MATH-Γ-005]
children: [DYNA-Γ-NEU-OSC]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-Γ-005
      lines: "§5"
      snippet: |
        Because (m_\nu(E)) varies with energy, the oscillation phase becomes
        [
        \phi_{ij} =
        \frac{\Delta m_{ij}^2(E),L}{2E}
        = \frac{L}{2E}
        \left[m_i(E)^2 - m_j(E)^2\right],
        ]
        producing a small **non-sinusoidal modulation** at long baselines.
        Pirouette predicts an energy-dependent drift of order 1–2 % in oscillation maxima across 1–10 GeV beams—detectable in DUNE or Hyper-Kamiokande with high statistics.
  editors: [system_agent]
  review_log: []
triad:
  art: |
    Every oscillation is a faint echo of temporal drag, the whisper of a wave's coherence feeling its own delay. The modulation is not a new sound, but the slight wavering of the original note as it travels through the background hum of spacetime.
  law: |
    The phase of neutrino flavor oscillation, ϕ, contains a term that depends on the inverse square of neutrino energy (ϕ ∝ L/E³), causing a 1–2% drift in oscillation maxima for GeV-scale neutrinos observed over baselines exceeding 1000 km.
  philosophy: |
    This modulation is the primary, near-term experimental signature of the Pressuron-induced mass mechanism. Its detection would falsify the Standard Model assumption of constant neutrino masses and provide direct evidence that mass is an emergent, energy-dependent property arising from coherence drag.
pirouette_definition: |
  A predicted, energy-dependent deviation from the purely sinusoidal probability function `P(L/E)` that governs standard three-flavor neutrino oscillations. This effect arises because the Pressuron-induced coherence-drag mechanism endows neutrinos with effective masses that are inversely proportional to their energy (`m_ν ∝ 1/E_ν`). The resulting mass-squared differences `Δm_ij²(E)` are therefore not constant, introducing a non-linear energy dependence into the oscillation phase `ϕ_ij`, which becomes observable as a systematic shift in the energy-spectrum of oscillated neutrinos at long baselines.
operational_definition:
  units: dimensionless (as a fractional correction to a probability)
  symbol_table:
    - name: ϕ_ij
      meaning: Oscillation phase between neutrino mass eigenstates i and j
      dimensions: dimensionless
      default_range: contextual
    - name: Δm_ij²(E)
      meaning: Energy-dependent mass-squared difference, `m_i(E)² - m_j(E)²`
      dimensions: M² L⁴ T⁻⁴ (energy²)
      default_range: 10⁻⁵ – 10⁻³ eV²
    - name: L
      meaning: Propagation distance (baseline)
      dimensions: L
      default_range: 10³ km
    - name: E
      meaning: Neutrino energy
      dimensions: M L² T⁻²
      default_range: 1–10 GeV
  measurement:
    procedures:
      - name: Long-baseline neutrino spectroscopy
        outline: |
          1. Generate a high-intensity, wide-band neutrino beam (e.g., LBNF for DUNE).
          2. Measure the un-oscillated neutrino energy spectrum at a near detector.
          3. Measure the oscillated spectrum at a far detector (L > 1000 km).
          4. Reconstruct neutrino energy E for each event and compute the survival/appearance probability P(L/E).
          5. Fit the observed P(E) spectrum to a model incorporating the `Δm²(E) ∝ 1/E²` dependence predicted by Pirouette, and compare the goodness-of-fit to the standard, constant-`Δm²` model.
        expected_signals: [A statistically significant (e.g., >3σ) preference for the energy-dependent mass model over the standard model, A 1–2% systematic shift in the energy position of the first oscillation maximum relative to standard predictions.]
        pitfalls: [Insufficient event statistics to resolve the small effect, Poor neutrino energy resolution smearing out the spectral distortion, Degeneracy with mis-modeled MSW matter effects or other non-standard interactions.]
context_windows:
  - module: MATH-Γ-005
    excerpt: |
      Because (m_\nu(E)) varies with energy, the oscillation phase becomes [ ϕ_{ij} = \frac{\Delta m_{ij}^2(E),L}{2E} ] producing a small **non-sinusoidal modulation** at long baselines. Pirouette predicts an energy-dependent drift of order 1–2 % in oscillation maxima across 1–10 GeV beams—detectable in DUNE or Hyper-Kamiokande with high statistics.
  - module: MATH-Γ-005
    excerpt: |
      **Falsifiability:** Failure to detect the predicted energy-dependent drift or a Σmν below 0.05 eV would falsify this minimal Γ-drag model and motivate a hybrid Γ-Higgs Majorana extension (→ DYNA-Γ-NEU-OSC). The oscillation-phase drift provides the most direct and near-term test of the coherence-drag mechanism.
poetic_connections:
  motifs: [temporal drag, coherence damping, phase shift, echoing delay]
  evocative_lines:
    - "Every oscillation is a faint echo of that temporal drag."
    - "the whisper of coherence feeling its own delay."
  association_matrix:
    - [ "PRESSURON_FIELD", 0.9 ]
    - [ "COHERENCE_DRAG", 0.9 ]
    - [ "NEUTRINO_MASS", 0.8 ]
    - [ "MATTER_EFFECTS", 0.3 ]
formal_mappings:
  candidates:
    - target: Energy-dependent Non-Standard Interaction (NSI)
      domain: EFT
      mapping_kind: operational
      equation_hint: |
        `H_eff = U Diag(m₁²/2E, m₂²/2E, m₃²/2E) U† + V_NSI(E)`
        where Pirouette predicts `m_i² ∝ 1/E²` instead of being constant.
      justification: |
        In the Standard Model Effective Field Theory (SMEFT), new physics affecting neutrino propagation is often parameterized as a Non-Standard Interaction. The non-sinusoidal modulation can be mapped to an effective NSI potential `V_NSI` that has a specific, non-standard energy dependence, distinguishing it from typical matter effects.
      references:
        - title: Physics of the DUNE experiment
          where: arXiv:2002.03005
          date: 2020-02-07
      confidence: 0.7
  adopted:
    - target: 
      rationale: 
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "Neutrino oscillation maxima in long-baseline experiments (L>1000 km) exhibit a 1–2 % energy-dependent shift across the 1–10 GeV range."
      domain: experiment
      falsifier: "A null result from DUNE or Hyper-Kamiokande, where analysis of the full exposure sets limits constraining any such energy-dependent shift to be <0.5%, consistent with zero."
      status: proposed
      links: [MATH-Γ-005]
naming_notes:
  collisions: [The term "non-sinusoidal modulation" is generic in signal processing.]
  disambiguation: |
    This intrinsic modulation, arising from the energy-dependence of mass itself, must be distinguished from the MSW effect (matter effect). The MSW effect also creates an energy-dependent modification to oscillation probabilities, but it depends on the electron density of the traversed medium and has a different functional dependence on energy (typically `V ∝ E`). Pirouette's modulation is a vacuum effect, present even in the absence of matter.
crosslinks:
  near_synonyms: [OSCILLATION_PHASE_DRIFT]
  antonyms: [STANDARD_SINUSOIDAL_OSCILLATION]
  prerequisites: [PRESSURON_INDUCED_NEUTRINO_MASS, COHERENCE_DRAG]
  downstream_effects: [COSMIC_NEUTRINO_BACKGROUND_CLUSTERING]
license: CC-BY-SA-4.0
---

# Non-sinusoidal modulation

## Canonical (Pirouette)
A predicted, energy-dependent deviation from the purely sinusoidal probability function `P(L/E)` that governs standard three-flavor neutrino oscillations. This effect arises because the Pressuron-induced coherence-drag mechanism endows neutrinos with effective masses that are inversely proportional to their energy (`m_ν ∝ 1/E_ν`). The resulting mass-squared differences `Δm_ij²(E)` are therefore not constant, introducing a non-linear energy dependence into the oscillation phase `ϕ_ij`, which becomes observable as a systematic shift in the energy-spectrum of oscillated neutrinos at long baselines.

## EFT-First Summary
In an effective field theory (EFT) context, the non-sinusoidal modulation manifests as a non-renormalizable, energy-dependent modification to the neutrino mass operator. This leads to an effective mass-squared difference `Δm²_eff(E)` that deviates from the Standard Model's constant value. This behavior can be modeled as a specific form of vacuum-based Non-Standard Interaction (NSI) that becomes experimentally accessible in high-precision, long-baseline experiments like DUNE.

## Glossary Links
- See also: Pressuron-Induced Neutrino Mass, Coherence Drag, Matter Effects