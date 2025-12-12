---
term: "Yukawa Portal"
canonical_id: "YUKAWA_PORTAL"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-014"]
---

---
term: Yukawa Portal
canonical_id: YUKAWA_PORTAL
symbol: `L_Γ = g_l Γ ψ̄_l ψ_l`
aliases: [Pressuron Coupling, Lepton-Pressuron Interaction]
parents: [MATH-013, MATH-014]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-014
      snippet: |
        From the Yukawa portal (\mathcal L_{\rm int}= g_\ell,\Gamma,\bar\psi_\ell\psi_\ell) with scaling (g_\ell=\kappa(m_\ell/m_e)^p), the finite one-loop shift is...
  editors: [GPT-4]
  review_log: []
triad:
  art: |
    A whispered connection between matter and the geometric stresses it creates. The Yukawa Portal is the seam through which a lepton feels the echo of its own mass, channeled by the Pressuron field.
  law: |
    A scalar field Γ couples universally to lepton mass-density `ψ̄_l ψ_l` via the interaction `L_Γ = g_l Γ ψ̄_l ψ_l`. The dimensionless coupling `g_l` scales with lepton mass as `g_l = κ(m_l/m_e)^p`, leading to a one-loop anomalous magnetic moment correction `Δa_l ∝ α g_l^2`.
  philosophy: |
    This portal grounds the abstract concept of the Pressuron in a measurable, falsifiable interaction. It proposes that the observed lepton mass hierarchy is not an accident but a direct modulator of a new force, providing a distinct phenomenological signature in precision measurements like g-2.
pirouette_definition: |
  The Yukawa Portal is the interaction term `L_Γ = g_l Γ ψ̄_l ψ_l` describing the coupling between the Pressuron scalar field `Γ` and a lepton field `ψ_l`. The dimensionless coupling constant `g_l` is a function of a fundamental parameter `κ` and a mass-scaling exponent `p`, given by `g_l = κ (m_l / m_e)^p`. This interaction generates a one-loop correction `Δa_l^(Γ)` to the lepton's anomalous magnetic moment, which is the primary observational channel for constraining the portal's parameters (`κ`, `p`, `m_Γ`).
operational_definition:
  units: The interaction Lagrangian term `L_Γ` has units of energy density (Mass⁴ in natural units). The coupling `g_l` is dimensionless.
  symbol_table:
    - name: `g_l`
      meaning: Lepton-specific Yukawa coupling
      dimensions: dimensionless
      default_range: `g_l^2 << α`; constrained by g-2 measurements.
    - name: `Γ`
      meaning: The Pressuron scalar field
      dimensions: Mass
      default_range: contextual; typically scanned in the MeV–GeV range for g-2 fits.
    - name: `ψ_l`
      meaning: Lepton Dirac spinor field
      dimensions: Mass^(3/2)
      default_range: N/A
    - name: `κ`
      meaning: Fundamental coupling strength parameter
      dimensions: dimensionless
      default_range: `~10⁻⁴` to `10⁻³` based on g-2 fits.
    - name: `p`
      meaning: Mass-scaling exponent
      dimensions: dimensionless
      default_range: `p=1` is a common theoretical prior.
  measurement:
    procedures:
      - name: Global Fit to Lepton Anomalous Magnetic Moments
        outline: |
          1. Formulate the theoretical prediction for the electron and muon anomalous magnetic moments, `a_e` and `a_μ`, including the universal series and the one-loop contribution `Δa_l^(Γ)` from the Yukawa portal.
          2. For a fixed scaling exponent `p` and Pressuron mass `m_Γ`, solve for the coupling strength `κ` that makes the theoretical `a_μ` match the experimental value `a_μ^exp`.
          3. Using the fitted `κ`, predict the value of `a_e`.
          4. Compare the prediction `a_e^th` with the experimental value `a_e^exp` to test the consistency of the (`p`, `m_Γ`) hypothesis.
          5. Scan over `p` and `m_Γ` to find the best-fit region in parameter space.
        expected_signals:
          - A region in (`κ`, `p`, `m_Γ`) space that simultaneously resolves the muon g-2 anomaly while remaining consistent with the high-precision measurement of electron g-2.
          - A characteristic mass-scaling signature where `Δa_μ / Δa_e ≈ (m_μ/m_e)^(2p)`.
        pitfalls:
          - Degeneracies with uncertainties in the universal Pirouette coefficients (`C_n`).
          - Over-fitting noise if experimental/theoretical uncertainties are underestimated.
context_windows:
  - module: MATH-014
    excerpt: |
      From the Yukawa portal (\mathcal L_{\rm int}= g_\ell,\Gamma,\bar\psi_\ell\psi_\ell) with scaling (g_\ell=\kappa(m_\ell/m_e)^p), the finite one-loop shift is
      [
      \boxed{; \Delta a_\ell^{(\Gamma)} = \frac{\alpha}{12\pi^2},\kappa^2,\Big(\frac{m_\ell}{m_e}\Big)^{!2p}, f!\left(\frac{m_\Gamma}{m_\ell}\right),\qquad f(0)=1. ;}
      ]
  - module: MATH-014
    excerpt: |
      014v2 fuses a clean universal QED skeleton with the pressuron one-loop in a way that is fit-stable, uncertainty-aware, and fully explicit—letting the wound-channel hypothesis be tested against (e/μ) data without dimensional landmines.
poetic_connections:
  motifs: [mass hierarchy, resonant leak, echo, wound-channel]
  evocative_lines:
    - "The anatomy of an echo."
    - "The geometry of coherence is not just a beautiful idea, but a true map of reality."
  association_matrix:
    - [ "PRESSURON", 0.9 ]
    - [ "G_MINUS_2", 0.8 ]
    - [ "MASS_SCALING", 0.7 ]
formal_mappings:
  candidates:
    - target: Standard Model Yukawa interaction (`L_Y = -y_f H ψ̄_L f_R + h.c.`)
      domain: SM
      mapping_kind: mathematical
      equation_hint: |
        `g_l Γ ψ̄_l ψ_l`  <-->  `y_f H ψ̄_f ψ_f`
      justification: |
        Both terms describe the interaction between a scalar field (Pressuron `Γ`, Higgs `H`) and a fermion bilinear. However, the Pirouette portal couples to `ψ̄ψ` (a scalar density), while the SM Higgs couples to `ψ̄_L ψ_R` (a chiral structure) to generate mass. The Pirouette coupling constant `g_l` is itself dependent on the lepton mass, unlike the fundamental SM Yukawa `y_f`.
      references:
        - title: An Introduction to Quantum Field Theory
          where: Chapter 20
          date: 1995-10-12
      confidence: 0.8
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The Yukawa Portal, with a single set of parameters (`κ`, `p`, `m_Γ`), can simultaneously explain the muon g-2 anomaly and remain consistent with the electron g-2 measurement."
      domain: phenomenology
      falsifier: "No combination of `p` and `m_Γ` can be found where the `κ` required to fit `a_μ` produces a prediction for `a_e` that lies within experimental bounds. Alternatively, future precision measurements of `a_τ` or direct searches for `Γ` rule out the entire favored parameter space."
      status: under-test
      links: [MATH-014]
    - statement: "The mass-scaling exponent `p` is approximately 1, indicating the coupling is proportional to lepton mass."
      domain: theory
      falsifier: "The best-fit value for `p` from global lepton data is statistically inconsistent with 1 (e.g., `p=0` or `p=2`)."
      status: proposed
      links: [MATH-014]
naming_notes:
  collisions: [The term "Yukawa" is ubiquitous in physics for any interaction of the form `scalar-fermion-antifermion`.]
  disambiguation: |
    This term specifically refers to the interaction with the Pirouette Framework's Pressuron (`Γ`) scalar, not the Standard Model Higgs boson. The key distinctions are the scalar `ψ̄ψ` Lorentz structure (vs. the SM's chiral `ψ̄_L ψ_R`) and the mass-dependent coupling constant `g_l`.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [PRESSURON, G_MINUS_2]
  downstream_effects: [LEPTON_ANOMALY]
license: CC-BY-SA-4.0
---

# Yukawa Portal

## Canonical (Pirouette)
The Yukawa Portal is the interaction term `L_Γ = g_l Γ ψ̄_l ψ_l` describing the coupling between the Pressuron scalar field `Γ` and a lepton field `ψ_l`. The dimensionless coupling constant `g_l` is a function of a fundamental parameter `κ` and a mass-scaling exponent `p`, given by `g_l = κ (m_l / m_e)^p`. This interaction generates a one-loop correction `Δa_l^(Γ)` to the lepton's anomalous magnetic moment, which is the primary observational channel for constraining the portal's parameters (`κ`, `p`, `m_Γ`).

## EFT-First Summary
In effective field theory, the Yukawa Portal is a renormalizable dimension-4 operator `g_l Γ ψ̄_l ψ_l` coupling a new scalar singlet `Γ` (the Pressuron) to the Standard Model leptons `ψ_l`. Unlike the SM Higgs, this interaction is diagonal in flavor and couples to the scalar density `ψ̄ψ`. Its primary phenomenological impact is a one-loop contribution to the lepton anomalous magnetic moments, providing a potential explanation for the muon g-2 anomaly that can be tested by comparing its predictions for electrons and muons.

## Glossary Links
- See also: [[PRESSURON]], [[G_MINUS_2]], [[MASS_SCALING]]