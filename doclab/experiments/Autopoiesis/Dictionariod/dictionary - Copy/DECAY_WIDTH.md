---
term: "Decay Width"
canonical_id: "DECAY_WIDTH"
symbol: "Γ_Γ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-Γ-001_the_pressurons_identity"]
---

---
term: Decay Width
canonical_id: DECAY_WIDTH_Γ
symbol: Γ_Γ
aliases: [narrow resonance, linewidth]
parents: [DYNA-Γ-001]
children: [DYNA-Γ-002, COSMO-Γ-001]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DYNA-Γ-001
      snippet: |
        | Property           | Symbol                                                   | Pirouette Assignment    |
        | ------------------ | -------------------------------------------------------- | ----------------------- |
        | Width              | ( Γ_Γ ∼ 10⁻² ,MeV )                                      | narrow resonance        |
  editors: [system-agent]
  review_log: []
triad:
  art: |
    The measure of a particle's fleeting breath; a narrow pulse of time before it dissolves back into the particle sea. It quantifies the impermanence of a resonant echo in the fabric of coherence.
  law: |
    The total decay width Γ_Γ is the sum of all partial decay widths into allowed final states and is inversely proportional to the particle's mean lifetime (τ_Γ = ħ/Γ_Γ). A measured width of ~10⁻² MeV for the Pressuron at a mass of 17 MeV/c² confirms a weakly coupled, narrow resonance.
  philosophy: |
    The narrowness of the decay width signifies a quasi-stable state, distinguishing the Pressuron from a broad, transient fluctuation. It is the signature of an *autopoietic resonance*—a self-sustaining oscillation of temporal pressure that persists long enough to be measured as a particle.
pirouette_definition: |
  A measure of the total decay rate of the Pressuron (Γ) into other particles, expressed in units of energy. It is calculated as the sum of the partial widths for all possible decay channels (e.g., Γ(Γ → e⁺e⁻), Γ(Γ → γγ)). Its small value (~10⁻² MeV) relative to the Pressuron's mass (~17 MeV/c²) defines the particle as a narrow resonance with a short but measurable mean lifetime (τ_Γ ~ 10⁻¹³ s).
operational_definition:
  units: MeV (Mega-electron Volts)
  symbol_table:
    - name: Γ_Γ
      meaning: Total decay width of the Pressuron.
      dimensions: M L² T⁻² (Energy)
      default_range: ~10⁻² MeV
    - name: Γ(Γ → X)
      meaning: Partial decay width for the Pressuron to decay into final state X.
      dimensions: M L² T⁻² (Energy)
      default_range: contextual
    - name: τ_Γ
      meaning: Mean lifetime of the Pressuron, related by τ_Γ = ħ/Γ_Γ.
      dimensions: T (Time)
      default_range: 10⁻¹⁴–10⁻¹³ s
  measurement:
    procedures:
      - name: Invariant Mass Resonance Spectroscopy
        outline: |
          In particle collision or beam-dump experiments, identify and measure the four-momenta of candidate decay products (e.g., an electron-positron pair). Calculate their invariant mass. The distribution of invariant mass values for a large sample of decays will form a peak centered at the particle's mass (m_Γ). The decay width (Γ_Γ) is the full width at half maximum (FWHM) of this resonance peak after deconvolution of detector resolution effects.
        expected_signals: [A narrow resonance peak in the e⁺e⁻ invariant mass spectrum centered at ≈17 MeV.]
        pitfalls: [Detector energy/momentum resolution can artificially broaden the observed peak, masking the true intrinsic width. Combinatorial backgrounds and radiative effects (e.g., final-state radiation) can distort the peak shape.]
context_windows:
  - module: DYNA-Γ-001
    excerpt: |
      Thus, its fundamental quantum numbers are:
      | Property           | Symbol                                                   | Pirouette Assignment    |
      | ------------------ | -------------------------------------------------------- | ----------------------- |
      | Mass               | ( m_Γ ≈ 17, \mathrm{MeV}/c^2 )                           | from MATH-013           |
      | Width              | ( Γ_Γ ∼ 10⁻², \mathrm{MeV} )                             | narrow resonance        |
      | Lifetime           | ( τ_Γ ∼ 10⁻¹⁴–10⁻¹³, s )                                  | transient               |
  - module: DYNA-Γ-001
    excerpt: |
      Dominant decay width into charged leptons:
      [
      \Gamma(\Gamma \rightarrow e^+e^-) =
      \frac{g_\Gamma^2 m_\Gamma}{8\pi}
      \left(1-\frac{4m_e^2}{m_\Gamma^2}\right)^{1/2}.
      ]
      The predicted signal is a **narrow e⁺e⁻ peak at 17 MeV** with mild angular anisotropy from pseudoscalar kinematics.
poetic_connections:
  motifs: [transience, breath, resonance, echo, dissipation]
  evocative_lines:
    - "We sought a particle and found a pulse of time."
    - "To measure it is to catch the universe inhaling between its own heartbeats."
    - "Decay into matter is thus the literal dissipation of coherent time-pressure into the particle sea."
  association_matrix:
    - [ "LIFETIME_Γ", 0.9 ]
    - [ "RESONANCE", 0.8 ]
    - [ "TEMPORAL_PRESSURE", 0.5 ]
formal_mappings:
  candidates:
    - target: Breit-Wigner resonance width (Γ)
      domain: SM|QFT
      mapping_kind: mathematical|operational
      equation_hint: |
        σ(E) ∝ 1 / [ (E - M)² + (Γ/2)² ]
      justification: |
        The decay width Γ_Γ is mathematically and operationally identical to the width parameter Γ in the Breit-Wigner distribution, which models the cross-section and invariant mass spectrum of an unstable particle. It represents the uncertainty in the particle's mass-energy (ΔE), consistent with the Heisenberg uncertainty principle (ΔE Δt ≈ ħ), where Γ_Γ = ΔE and the lifetime τ_Γ = Δt.
      references:
        - title: "Quantum Field Theory"
          where: "Peskin & Schroeder, Chapter 4.5"
          date: 1995-10-02
      confidence: 0.95
  adopted:
    - target: Breit-Wigner resonance width (Γ)
      rationale: Direct one-to-one correspondence in definition, measurement, and physical interpretation.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The Pressuron has a total decay width Γ_Γ ≈ 10⁻² MeV, with a branching ratio of ~90% to e⁺e⁻."
      domain: phenomenology|experiment
      falsifier: "Observation of a 17 MeV resonance with a width significantly broader than detector resolution (e.g., > 0.1 MeV), or with non-leptonic/photonic decays dominating, would falsify the model presented in DYNA-Γ-001."
      status: proposed
      links: [DYNA-Γ-001]
naming_notes:
  collisions: [Γ (Gamma function), γ (photon), γ^μ (Dirac matrices)]
  disambiguation: |
    Γ_Γ (capital Gamma subscript capital Gamma) denotes the decay width of the Pressuron particle (Γ). This should be carefully distinguished from the symbol for the photon (γ), the Dirac gamma matrices (γ^μ), and the mathematical Gamma function Γ(z).
crosslinks:
  near_synonyms: [INVERSE_LIFETIME_Γ, RESONANCE_WIDTH]
  antonyms: [PARTICLE_STABILITY]
  prerequisites: [PRESSURON, INVARIANT_MASS]
  downstream_effects: [BRANCHING_RATIO, EXPERIMENTAL_SIGNIFICANCE]
license: CC-BY-SA-4.0
---

# Decay Width

## Canonical (Pirouette)
A measure of the total decay rate of the Pressuron (Γ) into other particles, expressed in units of energy. It is calculated as the sum of the partial widths for all possible decay channels (e.g., Γ(Γ → e⁺e⁻), Γ(Γ → γγ)). Its small value (~10⁻² MeV) relative to the Pressuron's mass (~17 MeV/c²) defines the particle as a narrow resonance with a short but measurable mean lifetime (τ_Γ ~ 10⁻¹³ s).

## EFT-First Summary
The Pressuron's decay width, Γ_Γ, is operationally identical to the **Breit-Wigner resonance width (Γ)** in standard quantum field theory. This parameter determines the shape of the invariant mass peak in experimental searches via the Breit-Wigner distribution, `σ(E) ∝ 1 / [ (E - M)² + (Γ/2)² ]`. Its predicted narrow value of ~10⁻² MeV is a key signature, indicating a weakly-coupled particle and allowing it to be distinguished from experimental backgrounds.

## Glossary Links
- See also: [PRESSURON](./PRESSURON.md), [LIFETIME_Γ](./LIFETIME_Γ.md), [BRANCHING_RATIO](./BRANCHING_RATIO.md)