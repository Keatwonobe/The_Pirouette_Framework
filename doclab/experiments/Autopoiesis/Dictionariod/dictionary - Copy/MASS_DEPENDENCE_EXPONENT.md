---
term: "Mass-Dependence Exponent"
canonical_id: "MASS_DEPENDENCE_EXPONENT"
symbol: "p"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["XAP-008_Leptonic_g-2_gladiator_force_fit_map"]
---

---
term: Mass-Dependence Exponent
canonical_id: MASS_DEPENDENCE_EXPONENT
symbol: p
aliases: []
parents: [XAP-008_Leptonic_g-2_gladiator_force_fit_map]
children: []
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: XAP-008_Leptonic_g-2_gladiator_force_fit_map
      lines: "L5-L8"
      snippet: |
        We scan the three-parameter space $(\kappa, p, m_\Gamma)$ for leptonic magnetic-moment shifts
        \[
        \Delta a_\ell^{(\Gamma)}=\kappa\Big(\frac{m_\ell}{m_e}\Big)^p\Big(\frac{\alpha}{\pi}\Big)^3
        \,\underbrace{\frac{m_\ell^2}{m_\ell^2+m_\Gamma^2}}_{F_\ell(m_\Gamma)},
        \]
  editors: [system-agent]
  review_log: []
triad:
  art: |
    A lever that adjusts the universe's favor, tilting the scales of a new interaction to privilege heavier leptons over their lighter kin. It tunes the very steepness of the family hierarchy.
  law: |
    The exponent `p` dictates that the ratio of Γ-induced magnetic-moment shifts for two leptons `ℓ₁` and `ℓ₂`, after accounting for the decoupling form factor `F_ℓ`, must scale as `(m_{ℓ₁}/m_{ℓ₂})^{p+2}`.
  philosophy: |
    This parameter operationalizes our ignorance of the Γ-lepton coupling's flavor structure. Its value distinguishes between models where the force is universal (`p=0`) and those where it is intrinsically tied to the mechanism of mass generation, coupling proportionally to mass (`p=1`) or mass-squared (`p=2`).
pirouette_definition: |
  The Mass-Dependence Exponent `p` is a dimensionless real parameter in the XAP-008 model for Γ-induced leptonic anomalous magnetic moments. It governs the power-law scaling of the shift `Δa_ℓ` with the lepton mass `m_ℓ`, relative to the electron mass `m_e`, via the explicit factor `(m_ℓ/m_e)^p`.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: p
      meaning: Mass-Dependence Exponent
      dimensions: dimensionless
      default_range: [-2, 5]
    - name: Δa_ℓ
      meaning: Anomalous magnetic moment shift for lepton ℓ
      dimensions: dimensionless
      default_range: [10⁻¹⁴, 10⁻⁹]
    - name: m_ℓ
      meaning: Mass of lepton ℓ
      dimensions: M
      default_range: [0.511 MeV, 105.7 MeV]
    - name: m_Γ
      meaning: Mass of the Γ-stiffness mediator
      dimensions: M
      default_range: [1, 100] MeV
    - name: κ
      meaning: Overall coupling strength parameter
      dimensions: dimensionless
      default_range: contextual
  measurement:
    procedures:
      - name: Multi-lepton g-2 constraint fitting
        outline: |
          Infer `p` by simultaneously fitting the model `Δa_ℓ(κ, p, m_Γ)` to experimental measurements or bounds on the anomalous magnetic moments of at least two different leptons (e.g., electron and muon). A global fit over the `(κ, p, m_Γ)` parameter space identifies viable regions for `p`.
        expected_signals: [Viable parameter contours in the (p, m_Γ) plane, A strong correlation between the allowed values of p, κ, and m_Γ]
        pitfalls: [Experimental uncertainties in `Δa_e` or `Δa_μ` dominating the fit, Assuming the specific model form of `Δa_ℓ` is correct, Local minima in multi-parameter likelihood space]
context_windows:
  - module: XAP-008_Leptonic_g-2_gladiator_force_fit_map
    excerpt: |
      We scan the three-parameter space $(\kappa, p, m_\Gamma)$ for leptonic magnetic-moment shifts
      \[
      \Delta a_\ell^{(\Gamma)}=\kappa\Big(\frac{m_\ell}{m_e}\Big)^p\Big(\frac{\alpha}{\pi}\Big)^3
      \,\underbrace{\frac{m_\ell^2}{m_\ell^2+m_\Gamma^2}}_{F_\ell(m_\Gamma)},
      \]
      with $\ell\in\{e,\mu\}$.
  - module: XAP-008_Leptonic_g-2_gladiator_force_fit_map
    excerpt: |
      The electron bound dominates the viable set; decoupling $F_e(m_\Gamma)$ pushes solutions toward $m_\Gamma\!\gtrsim\!10$–$30$ MeV *or* larger $p$. Tight band favors $p\!\gtrsim\!1.5$–$2.5$ with $\kappa\!\sim\!10^{-4}$–$10^{-3}$; permissive band admits smaller $p$ or lighter $m_\Gamma$ if $\kappa\!\lesssim\!10^{-4}$.
poetic_connections:
  motifs: [flavor hierarchy, mass scaling, lepton universality violation, phenomenological knob]
  evocative_lines:
    - "pushes solutions toward ... larger p."
    - "Tight band favors pgtrsim1.5–2.5"
  association_matrix:
    - [ "KAPPA_COUPLING", 0.8 ]
    - [ "GAMMA_STIFFNESS_MEDIATOR_MASS", 0.8 ]
    - [ "LEPTON_UNIVERSALITY", 0.9 ]
formal_mappings:
  candidates:
    - target: Flavor-dependent coupling parameter
      domain: EFT
      mapping_kind: conceptual
      equation_hint: |
        g_ℓ ∝ (y_ℓ)^n or g_ℓ ∝ (m_ℓ/v)^p
      justification: |
        In many BSM models, new particles may couple to Standard Model leptons in a non-universal way. The exponent `p` provides a simple, phenomenological parameterization for such non-universality, where `p=0` corresponds to universal coupling and non-zero `p` corresponds to a specific flavor structure, e.g., scaling with lepton Yukawa couplings (`y_ℓ`).
      references:
        - title: Lepton Flavour (Universality) Violation in a Nutshell
          where: arXiv:2008.01083
          date: 2020-08-04
      confidence: 0.8
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "Under tight experimental bounds for `(Δa_e, Δa_μ)`, viable solutions strongly prefer `p > 1.5` for mediator masses `m_Γ` in the 1–100 MeV range."
      domain: phenomenology
      falsifier: "Future, more precise measurements of `Δa_e` or `Δa_μ` could yield a best-fit value of `p < 1`, or a measurement of `Δa_τ` could be inconsistent with the `(m_τ/m_μ)^p` scaling predicted from the electron/muon fit."
      status: supported
      links: [XAP-008_Leptonic_g-2_gladiator_force_fit_map]
naming_notes:
  collisions: [`p` is a common symbol for momentum.]
  disambiguation: |
    This `p` is a dimensionless exponent specific to the Γ-sector lepton coupling model. It should not be confused with momentum (`p`), pressure (`P`), or parity (`P`). Context is typically model fitting in flavor physics.
crosslinks:
  near_synonyms: []
  antonyms: [LEPTON_UNIVERSALITY]
  prerequisites: [ANOMALOUS_MAGNETIC_MOMENT]
  downstream_effects: []
license: CC-BY-SA-4.0
---

# Mass-Dependence Exponent

## Canonical (Pirouette)
The Mass-Dependence Exponent `p` is a dimensionless real parameter in the XAP-008 model for Γ-induced leptonic anomalous magnetic moments. It governs the power-law scaling of the shift `Δa_ℓ` with the lepton mass `m_ℓ`, relative to the electron mass `m_e`, via the explicit factor `(m_ℓ/m_e)^p`.

## EFT-First Summary
The Mass-Dependence Exponent `p` parameterizes the violation of lepton flavor universality in the Γ-force model. It is conceptually analogous to flavor-non-universal couplings in Standard Model Effective Field Theory (SMEFT), where new physics couples preferentially to heavier generations, for instance in proportion to the lepton Yukawa couplings. Current constraints on electron and muon magnetic moments from module XAP-008 favor `p > 1.5`, suggesting the Γ-force interaction strength scales faster than lepton mass.

## Glossary Links
- See also: [Kappa Coupling](<...>), [Gamma Stiffness Mediator Mass](<...>), [Lepton Universality](<...>)