---
term: "Coupling Parameter"
canonical_id: "COUPLING_PARAMETER"
symbol: "κ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-014"]
---

---
term: Coupling Parameter
canonical_id: COUPLING_PARAMETER
symbol: κ
aliases: []
parents: [MATH-013, MATH-014]
children: []
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-014
      snippet: |
        From the Yukawa portal (\mathcal L_{\rm int}= g_\ell,\Gamma,\bar\psi_\ell\psi_\ell) with scaling (g_\ell=\kappa(m_\ell/m_e)^p), the finite one-loop shift is
        [
        \boxed{; \Delta a_\ell^{(\Gamma)} = \frac{\alpha}{12\pi^2},\kappa^2,\Big(\frac{m_\ell}{m_e}\Big)^{!2p}, f!\left(\frac{m_\Gamma}{m_\ell}\right),\qquad f(0)=1. ;}
        ]
  editors: [Dictionary Generation Agent]
  review_log: []
triad:
  art: |
    κ is the gain on the feedback loop between a lepton and the Pressuron field. It tunes the intensity of the 'wound-channel' dialogue that generates anomalous magnetic moments, setting the fundamental volume of this new interaction.
  law: |
    The Pressuron-induced anomalous magnetic moment, Δa_ℓ^(Γ), is directly proportional to the square of the coupling parameter, κ². Its value is operationally defined and constrained by requiring that the total predicted g-2 for the muon and electron simultaneously match their respective experimental values for a fixed Mass-Scaling Exponent (p).
  philosophy: |
    κ represents a new fundamental constant of nature within the Pirouette framework, quantifying a non-QED interaction. Unlike the geometric coefficients of the universal series, κ is not derived from first principles but must be determined by fitting to experimental data. Its existence and value serve as a primary test of the Pressuron hypothesis.
pirouette_definition: |
  The Coupling Parameter, κ, is a dimensionless scalar constant that sets the intrinsic strength of the Yukawa-type interaction between a lepton (ψ_ℓ) and the Pressuron field (Γ). It scales the lepton-specific coupling `g_ℓ` via the relation `g_ℓ = κ(m_ℓ/m_e)^p`, where `p` is the Mass-Scaling Exponent. The value of κ is determined by fitting the framework's predictions for leptonic anomalous magnetic moments (a_ℓ) to high-precision experimental data.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: κ
      meaning: Coupling Parameter
      dimensions: "dimensionless"
      default_range: "O(10⁻⁴), empirically fit from g-2 data"
    - name: g_ℓ
      meaning: Lepton-specific Yukawa coupling for lepton ℓ
      dimensions: "dimensionless"
      default_range: "contextual"
    - name: p
      meaning: Mass-Scaling Exponent
      dimensions: "dimensionless"
      default_range: "O(1), typically scanned"
    - name: Δa_ℓ^(Γ)
      meaning: Pressuron one-loop contribution to the anomalous magnetic moment of lepton ℓ
      dimensions: "dimensionless"
      default_range: "contextual"
  measurement:
    procedures:
      - name: Global Fit to Leptonic g-2 Data
        outline: |
          1. Choose a truncation order `N` for the universal QED-like series and priors for its coefficients (C_n).
          2. Select a fixed value for the Mass-Scaling Exponent `p` (e.g., p=1) and scan over the Pressuron mass `m_Γ`.
          3. For each `m_Γ`, solve the equation `a_μ^th(κ) = a_μ^exp` to determine the unique value of `κ` required to match the experimental muon g-2 anomaly.
          4. Using this fitted `κ`, predict the electron g-2 value, `a_e^th(κ)`.
          5. Compare the prediction with the experimental `a_e^exp`. The optimal `κ` is the one that provides the best simultaneous fit to both lepton anomalies.
        expected_signals:
          - A non-zero, real-valued κ that simultaneously reconciles the predicted and experimental values for a_μ and a_e.
          - A stable fit value for κ across different truncation orders (N) of the universal series.
        pitfalls:
          - Inability to find a single κ that fits both electron and muon g-2 data, which would falsify the model's structure.
          - High sensitivity of the fitted κ to provisional universal coefficients (C_n) or the choice of `p`.
context_windows:
  - module: MATH-014
    excerpt: |
      From the Yukawa portal (\mathcal L_{\rm int}= g_\ell,\Gamma,\bar\psi_\ell\psi_\ell) with scaling (g_\ell=\kappa(m_\ell/m_e)^p), the finite one-loop shift is
      [
      \Delta a_\ell^{(\Gamma)} = \frac{\alpha}{12\pi^2},\kappa^2,\Big(\frac{m_\ell}{m_e}\Big)^{!2p}, f!\left(\frac{m_\Gamma}{m_\ell}\right)
      ]
  - module: MATH-014
    excerpt: |
      Minimal-fit algorithm (muon-led)
      1. Choose (N) and priors for (C_1,\ldots,C_N).
      2. Pick a mass-scaling exponent (p) (start with (p=1)); scan (m_\Gamma) in a sensible range.
      3. **Fit (\kappa)** by matching the muon: solve (a_\mu^{\rm th}(\kappa)=a_\mu^{\rm exp}).
      4. **Predict the electron:** plug the fitted (\kappa) into (a_e^{\rm th}); check consistency with (a_e^{\rm exp}).
poetic_connections:
  motifs: [interaction strength, tuning knob, new physics, yukawa portal]
  evocative_lines:
    - "This is the desired pattern."
    - "letting the wound-channel hypothesis be tested against (e/μ) data without dimensional landmines."
  association_matrix:
    - [ "PRESSURON", 0.9 ]
    - [ "MASS_SCALING_EXPONENT", 0.8 ]
    - [ "ANOMALOUS_MAGNETIC_MOMENT", 0.9 ]
formal_mappings:
  candidates:
    - target: Yukawa coupling constant (y)
      domain: EFT
      mapping_kind: mathematical
      equation_hint: |
        L_int = y · Φ · ψ̄ψ   ↔   L_int = g_ℓ · Γ · ψ̄_ℓψ_ℓ, where g_ℓ ∝ κ
      justification: |
        κ functions as the fundamental dimensionless constant in a Yukawa interaction Lagrangian of the form `L_int = g_ℓ Γ ψ-bar_ℓ ψ_ℓ`, where `g_ℓ = κ(m_ℓ/m_e)^p`. In EFT, this corresponds to a new scalar (Γ) coupling to Standard Model fermions (ℓ), with κ playing the role of the base Yukawa coupling `y`.
      confidence: 0.9
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "A single, real-valued κ exists that, for a given mass-scaling exponent `p`, simultaneously reconciles the theoretical predictions for the anomalous magnetic moments of the electron (a_e) and the muon (a_μ) with their experimental values."
      domain: phenomenology
      falsifier: "A global fit to (a_e, a_μ) data yields no real solution for κ, or the best-fit value of κ leads to predictions for other observables (e.g., tau lepton g-2, exotic decays) that are excluded by experimental bounds."
      status: under-test
      links: [MATH-014]
naming_notes:
  collisions: [κ is also used for curvature in differential geometry and for the kappa statistic. Context (particle physics, g-2) is critical.]
  disambiguation: |
    This κ is a fundamental constant of the Pirouette Framework, not to be confused with kinematic variables or form factors. It is always associated with the Pressuron (Γ) field interaction.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [PRESSURON, MASS_SCALING_EXPONENT]
  downstream_effects: [ANOMALOUS_MAGNETIC_MOMENT]
license: CC-BY-SA-4.0
---

# Coupling Parameter

## Canonical (Pirouette)
The Coupling Parameter, κ, is a dimensionless scalar constant that sets the intrinsic strength of the Yukawa-type interaction between a lepton (ψ_ℓ) and the Pressuron field (Γ). It scales the lepton-specific coupling `g_ℓ` via the relation `g_ℓ = κ(m_ℓ/m_e)^p`, where `p` is the Mass-Scaling Exponent. The value of κ is determined by fitting the framework's predictions for leptonic anomalous magnetic moments (a_ℓ) to high-precision experimental data.

## EFT-First Summary
In the language of Effective Field Theory (EFT), the Coupling Parameter κ is a dimensionless Yukawa coupling constant for a new scalar particle, the Pressuron (Γ). It governs the strength of the interaction `L_int ∝ κ Γ ψ-bar ψ`, which provides a mass-dependent contribution to the anomalous magnetic moments of leptons, potentially explaining the muon g-2 anomaly. This term must be fit to experiment, as its value is not predicted by the theory's structure.

## Glossary Links
- See also: [Pressuron](<link>), [Mass-Scaling Exponent](<link>), [Anomalous Magnetic Moment](<link>)