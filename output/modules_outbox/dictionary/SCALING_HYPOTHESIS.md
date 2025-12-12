---
term: "Scaling hypothesis"
canonical_id: "SCALING_HYPOTHESIS"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-013"]
---

---
term: Scaling hypothesis
canonical_id: SCALING_HYPOTHESIS
symbol: p
aliases: [mass-dependent coupling, Yukawa scaling]
parents: [MATH-013]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-013
      lines: "30-35"
      snippet: |
        **Scaling hypothesis:** heavier leptons couple more strongly to temporal pressure,
        [
        g_\ell=\kappa\left(\frac{m_\ell}{m_e}\right)^p,\qquad p\ge 0,
        ]
        with base strength (\kappa\equiv g_e). Default working choice: **(p=1)** (linear mass scaling)...
  editors: [AetherScribe-9]
  review_log: []
triad:
  art: |
    The heavier the bell, the louder it rings when struck by the storm of the Temporal Forge. A particle's mass is its audibility.
  law: |
    The dimensionless coupling `g_l` of a lepton `l` to the Temporal Pressure field (Γ) scales as a power `p` of its mass `m_l` relative to the electron mass `m_e`. The relationship is a testable power law: `g_l = κ(m_l/m_e)^p`, where `κ` is the base coupling of the electron.
  philosophy: |
    Mass is not merely a passive property but an active measure of a particle's receptivity to the background Temporal Pressure. This hypothesis links the lepton mass hierarchy to the observed hierarchy of anomalous magnetic moments, turning a set of seemingly arbitrary constants into a unified, predictive principle.
pirouette_definition: |
  The Scaling hypothesis is the postulate that the coupling strength `g_l` between a lepton `l` and the Pressuron field (the quantum of Temporal Pressure Γ) is not a universal constant but depends on the lepton's mass `m_l`. This dependence is parameterized by a dimensionless exponent `p` and a base coupling constant `κ` (defined as the electron's coupling, `g_e`), following the power-law relationship `g_l = κ(m_l/m_e)^p`. This hypothesis provides a direct, falsifiable mechanism to explain the observed difference in the anomalous magnetic moments of the electron and the muon.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: p
      meaning: The scaling exponent that dictates how strongly the lepton-Pressuron coupling depends on lepton mass.
      dimensions: dimensionless
      default_range: "p ≥ 0; baseline theoretical model assumes p=1."
    - name: g_l
      meaning: Dimensionless coupling strength of lepton `l` to the Pressuron field.
      dimensions: dimensionless
      default_range: contextual
    - name: κ
      meaning: Base coupling strength, defined as the electron's coupling to the Pressuron (`κ ≡ g_e`).
      dimensions: dimensionless
      default_range: "Constrained by Δa_e; typically O(10⁻⁴ – 10⁻⁵)."
  measurement:
    procedures:
      - name: Leptonic g-2 Anomaly Ratio
        outline: |
          1. Precisely measure the anomalous magnetic moments, `a_e` and `a_mu`, for the electron and muon.
          2. Attribute the discrepancies from Standard Model predictions, `Δa_e` and `Δa_mu`, to the Pressuron contribution.
          3. Form the ratio `R = Δa_mu / Δa_e`.
          4. In the limit of a light Pressuron (`m_Γ << m_e`), this ratio is given by `R ≈ (m_mu/m_e)^(2p)`.
          5. Solve for the exponent: `p = ln(R) / (2 * ln(m_mu/m_e))`. This gives a direct measurement of `p`.
        expected_signals: ["A non-zero value for `p`, with `p=1` being the baseline prediction.", "A consistent value of `κ` derived independently from `Δa_e` and `Δa_mu` once `p` is fixed."]
        pitfalls: ["Measurement precision for `a_e` and `a_mu` limits the precision of `p`.", "Other new physics could contribute to `a_l`, contaminating the signal.", "A non-negligible Pressuron mass `m_Γ` introduces a secondary dependence that must be co-fitted."]
context_windows:
  - module: MATH-013
    excerpt: |
      We model the lepton as a Dirac field (ψ_ℓ) and take a **Yukawa-type** portal to the pressuron (Γ)... **Scaling hypothesis:** heavier leptons couple more strongly to temporal pressure, `g_ℓ = κ(m_ℓ/m_e)^p`, with `p ≥ 0`. The base strength is `κ ≡ g_e`. Our default working choice is **(p=1)** (linear mass scaling), but we keep `p` symbolic for generality.
  - module: MATH-013
    excerpt: |
      Using the scaling `g_ℓ = κ(m_ℓ/m_e)^p`, the predicted contribution to the anomalous magnetic moment becomes `Δa_ℓ = (α/12π²)κ²(m_ℓ/m_e)^(2p)f(m_Γ/m_ℓ)`. For a given `p` and Pressuron mass `m_Γ`, the experimental target for the muon anomaly `Δa_μ` fixes the value of the base coupling `κ`. The framework's consistency can then be checked against the constraint from the electron's anomaly, `Δa_e`.
poetic_connections:
  motifs: [mass as resonance, hierarchy, audibility, acoustic weight, echo]
  evocative_lines:
    - "The anomalous song of the muon is... the sound of a heavy particle being buffeted by the ceaseless storm of the Temporal Forge."
    - "heavier leptons couple more strongly to temporal pressure"
  association_matrix:
    - [ "TEMPORAL_PRESSURE", 0.9 ]
    - [ "ANOMALOUS_MAGNETIC_MOMENT", 0.9 ]
    - [ "MASS", 0.8 ]
    - [ "PRESSURON", 0.7 ]
formal_mappings:
  candidates:
    - target: Minimal Flavor Violation (MFV) / Yukawa Proportionality
      domain: EFT
      mapping_kind: conceptual
      equation_hint: |
        Y_f ∝ m_f / v
      justification: |
        In the Standard Model Effective Field Theory, MFV is an assumption that all new flavor-violating interactions are proportional to the SM Yukawa matrices. The Scaling Hypothesis with p=1 (`g_l ∝ m_l`) is a direct implementation of this principle for a new lepton-scalar interaction, ensuring that the new physics respects the approximate flavor symmetries of the SM.
      references:
        - title: "An Introduction to Minimal Flavor Violation"
          where: "arXiv:1006.1737"
          date: 2010-06-08
      confidence: 0.8
  adopted:
    - target:
      rationale:
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "The exponent `p` is a universal constant for all leptons (e, μ, τ)."
      domain: phenomenology
      falsifier: "The value of `p` inferred from the (electron, muon) system's `g-2` anomalies differs significantly from the value inferred from the (muon, tau) system."
      status: proposed
      links: [MATH-013]
    - statement: "The value of the exponent `p` is exactly 1 (linear scaling)."
      domain: theory
      falsifier: "A high-precision global fit to `a_e`, `a_mu`, and `a_τ` (if measured) yields a best-fit value of `p` that is statistically inconsistent with 1."
      status: proposed
      links: [MATH-013]
naming_notes:
  collisions: ["`p` is the standard symbol for momentum."]
  disambiguation: |
    In the context of lepton-Pressuron interactions, `p` refers to the dimensionless scaling exponent. In kinematic expressions or Lagrangians, momentum is typically denoted by a four-vector `p^μ` or `k^μ` to avoid confusion.
crosslinks:
  near_synonyms: []
  antonyms: [UNIVERSAL_COUPLING]
  prerequisites: [TEMPORAL_PRESSURE, LEPTONIC_ANOMALOUS_MAGNETIC_MOMENT, PRESSURON]
  downstream_effects: [FIFTH_FORCE_CONSTRAINTS]
license: CC-BY-SA-4.0
---