---
term: "Mass-Scaling Exponent"
canonical_id: "MASS_SCALING_EXPONENT"
symbol: "p"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-014"]
---

---
term: Mass-Scaling Exponent
canonical_id: MASS_SCALING_EXPONENT
symbol: p
aliases: []
parents: [MATH-014]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-014
      lines: "§2"
      snippet: |
        From the Yukawa portal (L_int= g_ℓ,Γ,ψ̄_ℓψ_ℓ) with scaling (g_ℓ=κ(m_ℓ/m_e)^p), the finite one-loop shift is...
  editors: [GPT-4]
  review_log: []
triad:
  art: |
    The exponent that teaches a whisper to become a shout as mass increases. It tunes the voice of each lepton in the cosmic choir, ensuring heavier notes resonate more strongly with the Pressuron field.
  law: |
    The Yukawa-like coupling strength (g_ℓ) of a lepton (ℓ) to the Pressuron (Γ) scales as a power law with the lepton's mass (m_ℓ) relative to the electron mass (m_e), governed by the exponent p: g_ℓ = κ * (m_ℓ/m_e)^p.
  philosophy: |
    Encapsulates the hypothesis that mass is not merely inertia but an active 'charge' for the Pressuron field. A non-zero `p` asserts that the framework's new interactions are not flavor-blind, but are intimately and dynamically linked to the mass hierarchy itself, providing a natural explanation for observed flavor non-universality.
pirouette_definition: |
  The Mass-Scaling Exponent, `p`, is a dimensionless real number that defines the power-law relationship between a lepton's mass `m_ℓ` and its coupling strength `g_ℓ` to the Pressuron field. It is a fundamental free parameter of the lepton-Pressuron interaction sector, constrained by comparing predicted anomalous magnetic moments (`a_e`, `a_μ`) with experimental data.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: p
      meaning: Mass-Scaling Exponent
      dimensions: dimensionless
      default_range: [0, 2] (p=1 is a key benchmark)
    - name: g_ℓ
      meaning: Lepton-Pressuron coupling strength for lepton ℓ
      dimensions: dimensionless
      default_range: contextual
    - name: κ
      meaning: Base coupling strength (value for the electron)
      dimensions: dimensionless
      default_range: contextual
    - name: m_ℓ
      meaning: Mass of lepton ℓ
      dimensions: M
      default_range: contextual
    - name: m_e
      meaning: Mass of the electron
      dimensions: M
      default_range: 0.511 MeV/c²
  measurement:
    procedures:
      - name: Multi-lepton g-2 Anomaly Fit
        outline: |
          1. Assume a value for the exponent `p` (e.g., scan values from 0 to 2).
          2. Use the experimental value of the muon's anomalous magnetic moment (`a_μ^exp`) to fit the base coupling `κ` for the chosen `p` and a given Pressuron mass `m_Γ`.
          3. With the fitted `κ` and assumed `p`, predict the electron's anomaly (`a_e^th`).
          4. Compare the prediction `a_e^th` with its experimental value `a_e^exp`.
          5. The optimal value of `p` is the one that minimizes the residuals for both `a_e` and `a_μ` simultaneously.
        expected_signals: [A value or narrow range for `p` (e.g., `p ≈ 1`) that brings theoretical predictions for both electron and muon g-2 into agreement with experiment.]
        pitfalls: [Degeneracy with other model parameters (m_Γ, κ), Insufficient experimental precision to resolve `p`, The underlying power-law model may be an incomplete description.]
context_windows:
  - module: MATH-014
    excerpt: |
      From the Yukawa portal (L_int= g_ℓ,Γ,ψ̄_ℓψ_ℓ) with scaling (g_ℓ=κ(m_ℓ/m_e)^p), the finite one-loop shift is
      [ Δa_ℓ^(Γ) = (α/12π²)*κ²*(m_ℓ/m_e)^(2p)*f(m_Γ/m_ℓ) ]
      A useful integral representation for the shape function is...
  - module: MATH-014
    excerpt: |
      **Scaling:** for (p=1) and light (Γ), (Δa_μ^(Γ) / Δa_e^(Γ)≈ (m_μ/m_e)^2), giving natural muon enhancement while respecting electron bounds.
poetic_connections:
  motifs: [hierarchy, amplification, flavor, scaling-law, resonance]
  evocative_lines:
    - "...the wound-channel mass-scaling story."
    - "The anatomy of an echo."
  association_matrix:
    - [ "BASE_COUPLING_STRENGTH_KAPPA", 0.9 ]
    - [ "LEPTON_G_MINUS_2_ANOMALY", 0.9 ]
    - [ "PRESSURON", 0.8 ]
    - [ "LEPTON_MASS", 1.0 ]
formal_mappings:
  candidates:
    - target: Minimal Flavor Violation (MFV) Yukawa Scaling
      domain: EFT
      mapping_kind: conceptual
      equation_hint: |
        g_ℓ = κ(m_ℓ/m_e)^p  <-->  Y_f ∝ (m_f/v)^n
      justification: |
        In both Pirouette and MFV-like EFTs, the coupling of new physics to Standard Model fermions is not arbitrary but is assumed to be proportional to the existing fermion mass hierarchy. This suppresses flavor-changing neutral currents and provides a predictive structure. The Mass-Scaling Exponent `p` is analogous to the power of the mass insertion in such models.
      references:
        - title: "New physics and flavour"
          where: arXiv:0801.1826
          date: 2008-01-11
      confidence: 0.7
  adopted:
    - target: Minimal Flavor Violation (MFV) Yukawa Scaling
      rationale: The mapping is conceptually strong and provides a well-understood context for interpreting the physical meaning and constraints on `p`.
      confidence: 0.7
constraints_and_falsifiers:
  claims:
    - statement: "A single, universal value of `p` (hypothesized to be near 1) can simultaneously explain the measured anomalous magnetic moments of both the electron and the muon via the Pressuron contribution."
      domain: phenomenology
      falsifier: "No value of `p` can be found that brings the theoretical predictions for `a_e` and `a_μ` into agreement with their respective experimental values within a 3σ confidence level. This would indicate the simple power-law scaling is incorrect or incomplete."
      status: under-test
      links: [MATH-014]
naming_notes:
  collisions: [momentum (p)]
  disambiguation: |
    The symbol `p` is reserved for the Mass-Scaling Exponent within the context of Pirouette's interaction Lagrangians and their phenomenological consequences. In kinematic contexts, momentum is denoted by `k` or explicitly as a four-vector `p^μ` to avoid ambiguity.
crosslinks:
  near_synonyms: []
  antonyms: [FLAVOR_UNIVERSAL_COUPLING]
  prerequisites: [BASE_COUPLING_STRENGTH_KAPPA, LEPTON_G_MINUS_2_ANOMALY]
  downstream_effects: [MUON_G_MINUS_2_PREDICTION, ELECTRON_G_MINUS_2_PREDICTION]
license: CC-BY-SA-4.0
---

# Mass-Scaling Exponent

## Canonical (Pirouette)
The Mass-Scaling Exponent, `p`, is a dimensionless real number that defines the power-law relationship between a lepton's mass `m_ℓ` and its coupling strength `g_ℓ` to the Pressuron field. It is a fundamental free parameter of the lepton-Pressuron interaction sector, constrained by comparing predicted anomalous magnetic moments (`a_e`, `a_μ`) with experimental data.

## EFT-First Summary
The Mass-Scaling Exponent `p` functionally aligns with the concept of Minimal Flavor Violation (MFV) in Beyond-the-Standard-Model EFTs. It postulates that new physics couples to leptons with a strength proportional to a power of their mass, `g_ℓ ∝ (m_ℓ)^p`. This naturally explains why new effects, like contributions to g-2, are much larger for the muon than the electron. The specific value of `p` is a key unknown parameter to be determined by fitting to precision measurements.

## Glossary Links
- See also: [[Pressuron]], [[Base Coupling Strength (κ)]], [[Lepton g-2 Anomaly]]