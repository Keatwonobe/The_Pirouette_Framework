---
term: "Inverse-energy dependence"
canonical_id: "INVERSE_ENERGY_DEPENDENCE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-Γ-005_the_pressuron_induced_neutrino_mass_mechanism"]
---

---
term: Inverse-energy dependence
canonical_id: INVERSE_ENERGY_DEPENDENCE
symbol: mₙ ∝ 1/Eₙ
aliases: [coherence drag, energy-dependent mass]
parents: [MATH-Γ-005]
children: [DYNA-Γ-NEU-OSC, COSMO-Γ-NEU-SEA]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-Γ-005
      lines: "§3"
      snippet: |
        Averaging over stochastic Γ fluctuations yields a **self-energy correction**:
        [
        \Sigma_\nu(E) \approx
        \frac{g_{\Gamma\nu}^2\langle\Gamma^2\rangle}{E_\nu},
        \qquad
        m_\nu \equiv \Re[\Sigma_\nu(E)]/c^2.
        ]
        Hence
        [
        m_\nu(E) \approx
        \frac{g_{\Gamma\nu}^2}{c^2},
        \frac{\langle\Gamma^2\rangle}{E_\nu},
        ]
        showing the **inverse-energy dependence** characteristic of coherence drag.
  editors: [GPT-4 Agent]
  review_log: []
triad:
  art: |
    Every neutrino oscillation is a faint echo of temporal drag—the whisper of a particle's coherence feeling the delay of its own passage through spacetime.
  law: |
    The effective mass of a neutrino is inversely proportional to its energy, `m_ν(E) ∝ 1/E_ν`. This relationship predicts a non-sinusoidal, energy-dependent drift of 1–2% in the location of oscillation maxima for GeV-scale neutrinos, falsifiable by long-baseline experiments.
  philosophy: |
    This principle explains the smallness and hierarchy of neutrino masses as an emergent consequence of propagation, not an intrinsic property. It treats mass as a measure of interaction and delay, removing the need for ad-hoc mass scales or sterile states.
pirouette_definition: |
  The defining characteristic of the Pressuron-induced neutrino mass mechanism, where a neutrino's effective mass `m_ν` is inversely proportional to its energy `E_ν`. This arises from treating mass as a coherence-drag effect, a phase retardation caused by stochastic interactions with the background temporal pressure field (Γ). The self-energy correction from these interactions yields a leading term `Σ_ν(E) ∝ 1/E_ν`, which manifests as a real mass.
operational_definition:
  units: The dependence itself is a power-law relationship. The resulting mass `m_ν` is measured in eV/c².
  symbol_table:
    - name: m_ν(E)
      meaning: Energy-dependent neutrino mass
      dimensions: M
      default_range: 0.001–0.05 eV/c²
    - name: E_ν
      meaning: Neutrino energy
      dimensions: M L² T⁻²
      default_range: 1–10 GeV (for terrestrial experiments)
    - name: <Γ²>
      meaning: Variance of the background temporal pressure field
      dimensions: M² L⁴ T⁻⁴
      default_range: contextual; scales with charged lepton mass squared
    - name: g_Γν
      meaning: Neutrino-Pressuron dimensionless coupling constant
      dimensions: dimensionless
      default_range: ~10⁻² g_Γ
  measurement:
    procedures:
      - name: Long-baseline oscillation phase analysis
        outline: |
          1. Generate a wide-band neutrino beam (e.g., 1–10 GeV).
          2. Measure the un-oscillated flavor spectrum at a near detector.
          3. Measure the oscillated flavor spectrum at a far detector (L > 1000 km).
          4. Reconstruct the oscillation probability `P(ν_α → ν_β)` as a function of `L/E`.
          5. Fit the data to a standard sinusoidal oscillation model and to a Pirouette-modified model incorporating `Δm_ij²(E) ∝ (1/E²)`.
        expected_signals:
          - A statistically significant preference (>3σ) for the energy-dependent mass model.
          - A systematic drift in the energy values of oscillation maxima and minima compared to the standard `1/E` prediction, amounting to a 1–2% shift across the beam's energy range.
        pitfalls:
          - Insufficient detector energy resolution to distinguish the drift from statistical fluctuations.
          - Degeneracy with or mis-modeling of energy-dependent matter effects (MSW resonance).
context_windows:
  - module: MATH-Γ-005
    excerpt: |
      Averaging over stochastic Γ fluctuations yields a **self-energy correction**:
      [ \Sigma_\nu(E) \approx \frac{g_{\Gamma\nu}^2\langle\Gamma^2\rangle}{E_\nu}, \qquad m_\nu \equiv \Re[\Sigma_\nu(E)]/c^2. ]
      Hence [ m_\nu(E) \approx \frac{g_{\Gamma\nu}^2}{c^2}, \frac{\langle\Gamma^2\rangle}{E_\nu}, ]
      showing the **inverse-energy dependence** characteristic of coherence drag.
  - module: MATH-Γ-005
    excerpt: |
      Because `m_ν(E)` varies with energy, the oscillation phase becomes
      [ \phi_{ij} = \frac{\Delta m_{ij}^2(E),L}{2E} = \frac{L}{2E} \left[m_i(E)^2 - m_j(E)^2\right], ]
      producing a small **non-sinusoidal modulation** at long baselines. Pirouette predicts an energy-dependent drift of order 1–2 % in oscillation maxima across 1–10 GeV beams—detectable in DUNE or Hyper-Kamiokande with high statistics.
poetic_connections:
  motifs: [coherence drag, temporal retardation, phase echo, slowing heartbeat]
  evocative_lines:
    - "slowing the heartbeat of their passage"
    - "Every oscillation is a faint echo of that temporal drag: the whisper of coherence feeling its own delay."
  association_matrix:
    - [ "PRESSURON_FIELD", 0.9 ]
    - [ "NEUTRINO_MASS", 0.9 ]
    - [ "COHERENCE_DRAG", 0.8 ]
    - [ "OSCILLATION_PHASE", 0.7 ]
formal_mappings:
  candidates:
    - target: Momentum-dependent self-energy Σ(p)
      domain: EFT
      mapping_kind: mathematical
      equation_hint: |
        m_eff² = p² + m₀² + Re[Σ(p)]  ;  Pirouette implies Σ(p) ~ 1/E
      justification: |
        The inverse-energy dependence arises from a non-standard self-energy correction to the neutrino propagator, derived from a derivative coupling to a background field. Unlike standard logarithmic or polynomial running of parameters in QFT, this `1/E` behavior is a distinct feature of the coherence-drag mechanism. It models mass not as a fundamental parameter `m₀` but as an entirely emergent effect from Σ(p).
      references: []
      confidence: 0.4
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "Neutrino oscillation probability deviates from a purely sinusoidal `L/E` dependence due to the `m_ν ∝ 1/E_ν` relationship, causing a 1–2% energy-dependent drift in oscillation maxima for GeV-scale neutrinos."
      domain: phenomenology
      falsifier: "Null result in high-precision, long-baseline experiments (DUNE, Hyper-K) searching for non-sinusoidal energy dependence in oscillation patterns, with data fitting the standard mass model within errors."
      status: proposed
      links: [MATH-Γ-005]
    - statement: "In the early universe, high-energy neutrinos were effectively massless due to this dependence, behaving as standard radiation."
      domain: theory
      falsifier: "Cosmological observations (e.g., from BBN or CMB) requiring significant neutrino mass at high temperatures (T >> eV)."
      status: proposed
      links: [MATH-Γ-005, COSMO-Γ-002]
naming_notes:
  collisions: [Running mass (QFT)]
  disambiguation: |
    This is distinct from the standard "running mass" in Quantum Field Theory, which typically describes a logarithmic energy dependence arising from renormalization group evolution. Pirouette's inverse-energy dependence is a power-law (`E⁻¹`) effect stemming directly from a physical coherence-drag mechanism, not from integrating out virtual particle loops.
crosslinks:
  near_synonyms: [COHERENCE_DRAG_EFFECT]
  antonyms: [INTRINSIC_MASS]
  prerequisites: [PRESSURON_FIELD, TEMPORAL_DRAG]
  downstream_effects: [OSCILLATION_PHASE_DRIFT, COSMIC_NEUTRINO_MASS_SUPPRESSION]
license: CC-BY-SA-4.0
---

# Inverse-energy dependence

## Canonical (Pirouette)
The defining characteristic of the Pressuron-induced neutrino mass mechanism, where a neutrino's effective mass `m_ν` is inversely proportional to its energy `E_ν`. This arises from treating mass as a coherence-drag effect, a phase retardation caused by stochastic interactions with the background temporal pressure field (Γ). The self-energy correction from these interactions yields a leading term `Σ_ν(E) ∝ 1/E_ν`, which manifests as a real mass.

## EFT-First Summary
In an effective field theory context, the inverse-energy dependence can be modeled as an unconventional, momentum-dependent self-energy term `Σ(p)` added to the neutrino propagator. This term, which scales as `1/E`, originates from a derivative coupling to the background Pressuron field. Unlike standard "running mass" which exhibits logarithmic scaling, this power-law dependence is a unique prediction of the coherence-drag mechanism.

## Glossary Links
- See also: [Pressuron Field](PRESSURON_FIELD), [Coherence Drag](COHERENCE_DRAG), [Neutrino Oscillation](NEUTRINO_OSCILLATION)