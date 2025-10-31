---
term: "Leptonic Magnetic-Moment Shift"
canonical_id: "LEPTONIC_MAGNETIC_MOMENT_SHIFT"
symbol: "Δa_ℓ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["XAP-008_Leptonic_g-2_gladiator_force_fit_map"]
---

---
term: Leptonic Magnetic-Moment Shift
canonical_id: LEPTONIC_MAGNETIC_MOMENT_SHIFT
symbol: Δa_ℓ
aliases: [Gladiator Force g-2 Contribution, (g-2)_ℓ^(Γ)]
parents: [XAP-008]
children: [VIS-012]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: XAP-008_Leptonic_g-2_gladiator_force_fit_map
      snippet: |
        \[
        \Delta a_\ell^{(\Gamma)}=\kappa\Big(\frac{m_\ell}{m_e}\Big)^p\Big(\frac{\alpha}{\pi}\Big)^3
        \,\underbrace{\frac{m_\ell^2}{m_\ell^2+m_\Gamma^2}}_{F_\ell(m_\Gamma)},
        \]
  editors: [Agent (GPT-4)]
  review_log: []
triad:
  art: |
    A lepton, spinning in the void, feels a faint magnetic tremor. This whisper is not from light itself, but from the stiffness of the vacuum, a ghostly resistance from the Gladiator field.
  law: |
    The Gladiator Force induces a shift in a lepton's anomalous magnetic moment that scales with a power `p` of the lepton's mass and is suppressed when the Gladiator mediator mass `m_Γ` is large compared to the lepton mass `m_ℓ`.
  philosophy: |
    This shift provides a high-precision, low-energy window into the deep UV structure of the Pirouette Framework. By constraining its parameters, we map the residual stiffness of the cosmic substrate and test the theory's connection between particle mass and cosmological energy density.
pirouette_definition: |
  The contribution `Δa_ℓ` to the anomalous magnetic moment `a_ℓ` of a lepton `ℓ` (where `ℓ ∈ {e, μ, τ}`) arising from loop-level interactions with the Gladiator Force mediator `Γ`. It is parameterized by a dimensionless coupling `κ`, a mass-scaling exponent `p`, and the mediator mass `m_Γ`. The shift is functionally defined as: `Δa_ℓ = κ * (m_ℓ/m_e)^p * (α/π)^3 * (m_ℓ^2 / (m_ℓ^2 + m_Γ^2))`.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: Δa_ℓ
      meaning: Leptonic Magnetic-Moment Shift for lepton ℓ.
      dimensions: dimensionless
      default_range: Contextual, but empirically bounded (e.g., `|Δa_μ| < 2.5e-9`).
    - name: κ
      meaning: Dimensionless coupling constant for the Gladiator Force.
      dimensions: dimensionless
      default_range: Empirically `~10⁻⁴ – 10⁻²`.
    - name: p
      meaning: Mass-scaling exponent.
      dimensions: dimensionless
      default_range: Empirically `~0 – 4`.
    - name: m_ℓ
      meaning: Mass of lepton ℓ.
      dimensions: M
      default_range: `m_e ≈ 0.511 MeV`, `m_μ ≈ 105.7 MeV`.
    - name: m_Γ
      meaning: Mass of the Gladiator Force mediator.
      dimensions: M
      default_range: Empirically `~1 – 100 MeV`.
    - name: α
      meaning: Fine-structure constant.
      dimensions: dimensionless
      default_range: `≈ 1/137.036`
  measurement:
    procedures:
      - name: Constraint via Residuals
        outline: |
          Measure the total anomalous magnetic moments `a_e` and `a_μ` with high precision. Calculate the Standard Model prediction `a_ℓ^SM`. The residual `δa_ℓ = a_ℓ^exp - a_ℓ^SM` provides an experimental bound on all new physics, including `Δa_ℓ`. Scan the parameter space `(κ, p, m_Γ)` to find regions where the predicted `Δa_ℓ` values are consistent with the observed `δa_e` and `δa_μ`.
        expected_signals: [A non-zero residual `δa_ℓ` that is consistent between the electron and muon channels according to the model's mass-scaling relation.]
        pitfalls: [Theoretical uncertainties in `a_ℓ^SM` (especially hadronic contributions for muons), experimental systematic errors, contributions from other new physics phenomena.]
context_windows:
  - module: XAP-008
    excerpt: |
      We scan the three-parameter space $(\kappa, p, m_\Gamma)$ for leptonic magnetic-moment shifts. The electron bound dominates the viable set; decoupling $F_e(m_\Gamma)$ pushes solutions toward $m_\Gamma\!\gtrsim\!10$–$30$ MeV or larger $p$. Tight band favors $p\!\gtrsim\!1.5$–$2.5$ with $\kappa\!\sim\!10^{-4}$–$10^{-3}$.
  - module: MATH-013
    excerpt: |
      The one-loop vertex correction involving the Γ-propagator gives rise to the magnetic moment operator. The dominant contribution is proportional to the lepton mass, but higher-order substrate effects introduce the additional scaling factor $(m_\ell/m_e)^p$, reflecting the non-trivial interaction with the Γ-stiffness condensate.
poetic_connections:
  motifs: [magnetic whisper, mass-scaling echo, vacuum stiffness, lepton wobble]
  evocative_lines:
    - "The electron bound dominates the viable set."
    - "Λ as Residual Γ-Stiffness"
  association_matrix:
    - [ "GAMMA_STIFFNESS", 0.9 ]
    - [ "GLADIATOR_FORCE", 0.9 ]
    - [ "PRESSURON", 0.3 ]
formal_mappings:
  candidates:
    - target: Anomalous magnetic moment, (g-2)_ℓ
      domain: SM|EFT
      mapping_kind: operational
      equation_hint: |
        a_ℓ = (g_ℓ - 2) / 2
        a_ℓ^exp = a_ℓ^SM + Δa_ℓ + ...
      justification: |
        `Δa_ℓ` is defined as an additive contribution to the lepton anomalous magnetic moment `a_ℓ`, a precision observable calculated and measured in the Standard Model. It serves as a classic benchmark for Beyond the Standard Model (BSM) physics, where new particles in loops can shift the predicted value.
      references:
        - title: "Measurement of the Positive Muon Anomalous Magnetic Moment to 0.46 ppm"
          where: "Phys. Rev. Lett. 126, 141801 (Muon g-2 Collaboration)"
          date: 2021-04-07
      confidence: 1.0
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The Gladiator Force, via the `Δa_ℓ` contribution, can account for the observed experimental deviation in `a_μ` from its SM prediction, while remaining consistent with the tighter constraints from `a_e`."
      domain: phenomenology
      falsifier: "An updated measurement or calculation shows that the experimental anomalies `δa_e` and `δa_μ` are inconsistent with the model's mass-scaling relation for any choice of `(κ, p, m_Γ)`. For example, if `δa_e` becomes large and negative while `δa_μ` is large and positive, the model is falsified as `Δa_ℓ` has the same sign for all leptons."
      status: proposed
      links: [XAP-008]
    - statement: "The viable parameter space for `Δa_ℓ` is constrained by experimental bounds `|Δa_μ| ≤ 5.0e-10` and `|Δa_e| ≤ 3.0e-13` (tight band)."
      domain: experiment
      falsifier: "A new experiment finds a deviation outside these bounds, or a re-analysis of systematic errors significantly loosens the bounds, thereby altering the viable `(κ, p, m_Γ)` space."
      status: supported
      links: [XAP-008]
naming_notes:
  collisions: [The standard symbol `a_ℓ` refers to the *total* anomalous magnetic moment. `Δa_ℓ` is used in the literature to denote a specific *contribution* or the discrepancy between experiment and theory (`Δa_μ = a_μ^exp - a_μ^SM`).]
  disambiguation: |
    Within Pirouette, `Δa_ℓ` refers *exclusively* to the contribution from the Gladiator Force / Γ-Stiffness sector. When comparing to data, use `δa_ℓ = a_ℓ^exp - a_ℓ^SM` for the measured discrepancy.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [GLADIATOR_FORCE, GAMMA_STIFFNESS]
  downstream_effects: []
license: CC-BY-SA-4.0
---

# Leptonic Magnetic-Moment Shift

## Canonical (Pirouette)
The contribution `Δa_ℓ` to the anomalous magnetic moment `a_ℓ` of a lepton `ℓ` (where `ℓ ∈ {e, μ, τ}`) arising from loop-level interactions with the Gladiator Force mediator `Γ`. It is parameterized by a dimensionless coupling `κ`, a mass-scaling exponent `p`, and the mediator mass `m_Γ`. The shift is functionally defined as: `Δa_ℓ = κ * (m_ℓ/m_e)^p * (α/π)^3 * (m_ℓ^2 / (m_ℓ^2 + m_Γ^2))`.

## EFT-First Summary
The Leptonic Magnetic-Moment Shift `Δa_ℓ` is a direct, additive contribution to the Standard Model anomalous magnetic moment `a_ℓ = (g-2)/2`. It serves as a potent probe for new physics, analogous to contributions from generic Beyond the Standard Model (BSM) particles running in loops. Current experimental anomalies, particularly in the muon's magnetic moment, provide tight constraints on the Pirouette parameters `(κ, p, m_Γ)` that govern this shift.

## Glossary Links
- See also: GLADIATOR_FORCE, GAMMA_STIFFNESS