---
term: "Energy-dependent mass"
canonical_id: "ENERGY_DEPENDENT_MASS"
symbol: "mν(E)"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-Γ-005_the_pressuron_induced_neutrino_mass_mechanism"]
---

---
term: Energy-dependent mass
canonical_id: ENERGY_DEPENDENT_MASS
symbol: mν(E)
aliases: [coherence-drag mass, temporal drag]
parents: [MATH-Γ-005, MATH-013, DYNA-Γ-004]
children: [DYNA-Γ-NEU-OSC, COSMO-Γ-NEU-SEA]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-Γ-005
      lines: "L41-L50"
      snippet: |
        Averaging over stochastic Γ fluctuations yields a **self-energy correction**:
        [ \Sigma_\nu(E) \approx \frac{g_{\Gamma\nu}^2\langle\Gamma^2\rangle}{E_\nu}, \qquad m_\nu \equiv \Re[\Sigma_\nu(E)]/c^2. ]
        Hence
        [ m_\nu(E) \approx \frac{g_{\Gamma\nu}^2}{c^2} \frac{\langle\Gamma^2\rangle}{E_\nu}, ]
        showing the **inverse-energy dependence** characteristic of coherence drag.
  editors: [system]
  review_log: []
triad:
  art: |
    A particle's weight is not its own, but the measure of its struggle against the current of time. Neutrinos are nearly perfect swimmers, their mass just the faint ripple they leave in their wake.
  law: |
    The effective mass of a neutrino is not a fundamental constant but emerges from its interaction with the temporal pressure field (Γ), resulting in an inverse proportionality to its own energy: mν(E) ∝ 1/Eν.
  philosophy: |
    Mass is not an intrinsic, static property but a dynamic, relational effect of a particle's propagation through spacetime's substrate. It quantifies the degree to which a particle's phase coherence is "dragged" by the background, transforming a fundamental property into an environmental observable.
pirouette_definition: |
  The effective mass acquired by a particle, particularly a neutrino, due to coherence-drag interactions with the background temporal pressure field (Γ). This mass is not a fixed constant but a function of the particle's energy (E), specifically showing an inverse dependence, mν(E) ∝ 1/E. It arises from the self-energy correction induced by stochastic Γ-field fluctuations integrated over the particle's coherence length.
operational_definition:
  units: eV/c²
  symbol_table:
    - name: mν(E)
      meaning: Energy-dependent neutrino mass
      dimensions: M
      default_range: 0.001–0.05 eV/c²
    - name: Eν
      meaning: Neutrino energy
      dimensions: ML²T⁻²
      default_range: 1 MeV – 10 GeV
    - name: ⟨Γ²⟩
      meaning: Variance of the background Pressuron field
      dimensions: (ML²T⁻²)²
      default_range: contextual
    - name: gΓν
      meaning: Neutrino-Pressuron dimensionless coupling constant
      dimensions: dimensionless
      default_range: ~10⁻² gΓ
  measurement:
    procedures:
      - name: Long-Baseline Oscillation Anomaly Search
        outline: |
          Measure the neutrino oscillation probability P(νμ → νe) and P(νμ → νμ) as a function of energy in a long-baseline experiment (e.g., DUNE, Hyper-Kamiokande). Fit the data to the standard sinusoidal L/E model. Search for residual, energy-correlated deviations from the best-fit sinusoid.
        expected_signals: [A 1–2% drift in the energy of oscillation maxima, A non-sinusoidal modulation pattern in the oscillation probability curve.]
        pitfalls: [Insufficient statistical power to resolve small deviations, Energy reconstruction uncertainties smearing out the effect, Degeneracies with unknown sterile neutrino effects or non-standard interactions.]
context_windows:
  - module: MATH-Γ-005
    excerpt: |
      Assuming background Γ variance proportional to charged-lepton mass squared (from MATH-013): ⟨Γ²⟩ℓ ∝ mℓ², the three neutrino flavors inherit masses in proportion: mνe : mνμ : mντ = 1/me : 1/mμ : 1/mτ. Numerically this reproduces an inverted-like hierarchy consistent with oscillation data when normalized by atmospheric Δm².
  - module: MATH-Γ-005
    excerpt: |
      In the Early Universe, when Eν ≫ mΓ, the drag term suppresses, leaving neutrinos effectively massless, consistent with standard radiation behavior during BBN and recombination. At late times, as background Γ variance freezes in, mν saturates, slightly reducing the cosmic sum Σmν relative to ΛCDM fits by ≈ 15 %.
poetic_connections:
  motifs: [coherence drag, temporal friction, phase retardation, emergent mass]
  evocative_lines:
    - "The whisper of coherence feeling its own delay."
    - "slowing the heartbeat of their passage"
  association_matrix:
    - [ "TEMPORAL_PRESSURE", 0.9 ]
    - [ "NEUTRINO_OSCILLATION", 0.8 ]
    - [ "COHERENCE_DAMPING", 0.7 ]
formal_mappings:
  candidates:
    - target: Running mass m(μ)
      domain: SM
      mapping_kind: conceptual
      equation_hint: |
        mν(E) ∝ 1/E   vs.   m_fermion(μ) ∝ [log(μ/Λ)]^γ
      justification: |
        Both concepts describe a mass parameter that varies with energy scale. However, the Pirouette energy-dependent mass arises from a non-perturbative interaction with a background field, yielding an inverse power-law dependence. This contrasts with the logarithmic running of SM masses, which arises from radiative loop corrections in a renormalizable quantum field theory.
      references: []
      confidence: 0.3
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "Neutrino oscillation probabilities exhibit a 1–2% non-sinusoidal, energy-dependent deviation from the standard L/E sinusoidal behavior in long-baseline experiments."
      domain: experiment
      falsifier: "Observation of a purely sinusoidal L/E dependence by DUNE or Hyper-Kamiokande to a precision better than 1%."
      status: proposed
      links: [MATH-Γ-005, DYNA-Γ-NEU-OSC]
    - statement: "The cosmological sum of neutrino masses Σmν is suppressed relative to terrestrial expectations, with a value between 0.05–0.10 eV."
      domain: phenomenology
      falsifier: "A measurement of Σmν > 0.12 eV or < 0.05 eV from future CMB and LSS surveys like CMB-S4 and EUCLID."
      status: proposed
      links: [MATH-Γ-005, COSMO-Γ-NEU-SEA]
naming_notes:
  collisions: [The symbol m(E) is commonly used for "running mass" in QFT.]
  disambiguation: |
    Distinguish from the logarithmic "running mass" of the Standard Model. Energy-dependent mass in Pirouette refers to an effective mass from a `1/E` self-energy correction due to background field interactions, not from loop-level radiative corrections. It is a coherence-drag effect, not a renormalization group flow effect.
crosslinks:
  near_synonyms: [COHERENCE_DRAG_MASS]
  antonyms: [BARE_MASS, INTRINSIC_MASS]
  prerequisites: [TEMPORAL_PRESSURE]
  downstream_effects: [NEUTRINO_OSCILLATION_PHASE_SHIFT, COSMIC_STRUCTURE_DAMPING]
license: CC-BY-SA-4.0
---

# Energy-dependent mass

## Canonical (Pirouette)
The effective mass acquired by a particle, particularly a neutrino, due to coherence-drag interactions with the background temporal pressure field (Γ). This mass is not a fixed constant but a function of the particle's energy (E), specifically showing an inverse dependence, mν(E) ∝ 1/E. It arises from the self-energy correction induced by stochastic Γ-field fluctuations integrated over the particle's coherence length.

## EFT-First Summary
This concept is conceptually analogous to a "running mass" but with a non-standard physical origin and functional form. It arises from a dimension-5 effective operator coupling the neutrino kinetic term to the scalar Pressuron field, `L_eff ~ (∂ν)(∂ν)Γ / mΓ`. Averaging over the background Γ field generates a non-local self-energy term in the neutrino propagator, `Σ(p) ∝ ⟨Γ²⟩ / p·u`, which manifests as an effective mass inversely proportional to the neutrino's energy, `m_eff(E) ∝ 1/E`. This power-law behavior starkly contrasts with the logarithmic running of masses from radiative corrections in renormalizable QFTs.

## Glossary Links
- See also: TEMPORAL_PRESSURE, NEUTRINO_OSCILLATION, COHERENCE_DRAG