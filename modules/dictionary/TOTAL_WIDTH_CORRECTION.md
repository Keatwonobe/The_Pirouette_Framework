---
term: "Total Width Correction"
canonical_id: "TOTAL_WIDTH_CORRECTION"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-Γ-004_the_pressuron_higgs_interaction"]
---

---
term: Total Width Correction
canonical_id: TOTAL_WIDTH_CORRECTION
symbol: ΔΓ_H / Γ_H
aliases: [Higgs width excess, Pressuron-induced width enhancement]
parents: [DYNA-Γ-004]
children: [DYNA-Γ-HIGGS-TAIL]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DYNA-Γ-004
      lines: "§3.1"
      snippet: |
        1. **Total Width Correction**
           [
           \frac{\Delta\Gamma_H}{\Gamma_H}
           \approx \frac{\lambda_{H\Gamma}^2 v^2}{8\pi^2 m_H^2}
           \sim 10^{-3}.
           ]
           A 0.1 %–0.3 % increase in the total width—just below current LHC resolution—should emerge if the coupling exists.
  editors: [auto-formatter]
  review_log: []
triad:
  art: |
    The Higgs, the field that gives mass its inertia, is made to breathe by temporal pressure. This correction is the measurable exhalation, a subtle off-beat in its decay song that reveals a deeper temporal resonance.
  law: |
    The Pressuron-Higgs coupling (λ_HΓ) induces a positive, definite correction to the total decay width of the Higgs boson (Γ_H) of approximately 0.1%–0.3%, directly proportional to the square of the coupling constant.
  philosophy: |
    This correction serves as the primary, most accessible collider signature of the Higgs-Pressuron interaction. Its detection would falsify the view of the electroweak vacuum as static, establishing it as a dynamic medium whose coherence density (the Higgs) is actively modulated by temporal pressure (the Pressuron).
pirouette_definition: |
  The predicted fractional increase in the total decay width of the Higgs boson, ΔΓ_H / Γ_H, arising from the gauge-invariant coupling (λ_HΓ) between the Higgs field (H) and the Pressuron field (Γ). The correction is caused by new loop-level decay channels and a shift in the Higgs self-energy.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: ΔΓ_H
      meaning: Change in the Higgs total decay width due to Pressuron coupling.
      dimensions: M (Energy)
      default_range: 4–12 keV
    - name: Γ_H
      meaning: Standard Model prediction for the Higgs total decay width.
      dimensions: M (Energy)
      default_range: ~4.1 MeV
    - name: λ_HΓ
      meaning: Dimensionless Higgs-Pressuron mixing constant.
      dimensions: dimensionless
      default_range: contextual
    - name: v
      meaning: Higgs vacuum expectation value.
      dimensions: M (Energy)
      default_range: 246 GeV
  measurement:
    procedures:
      - name: Off-Shell Production Rate Analysis (Hadron Colliders)
        outline: |
          At the LHC, measure the rate of off-shell Higgs production (e.g., in H* → ZZ → 4l) at high invariant mass. The ratio of off-shell to on-shell event yields is proportional to the total width Γ_H. Compare the inferred width to the Standard Model prediction to isolate ΔΓ_H.
        expected_signals: [A measured total width Γ_H(meas) that is 1.001 to 1.003 times Γ_H(SM).]
        pitfalls: [Large experimental uncertainties from jet energy scales; model dependence of off-shell couplings; statistical limitations.]
      - name: Direct Resonance Scan (Lepton Colliders)
        outline: |
          At a future lepton collider (e.g., ILC, FCC-ee), perform a high-resolution scan of the e+e- → ZH cross-section across the Higgs mass peak. The width of the reconstructed resonance curve directly yields Γ_H.
        expected_signals: [A Breit-Wigner width systematically larger than the SM prediction by 0.1%–0.3%.]
        pitfalls: [Requires exquisite control of beam energy spread and luminosity calibration.]
context_windows:
  - module: DYNA-Γ-004
    excerpt: |
      A 0.1 %–0.3 % increase in the total width—just below current LHC resolution—should emerge if the coupling exists... At resonance, the two fields share energy, letting the Higgs “breathe” in time: a periodic modulation of its vacuum expectation value.
  - module: DYNA-Γ-004
    excerpt: |
      A null result at sensitivities... better than 0.1 % on total width would **exclude** this baseline coupling and require a tensor or derivative re-formulation (→ DYNA-Γ-HIGGS-TAIL).
poetic_connections:
  motifs: [Higgs breath, temporal resonance, off-beat song, collider signature]
  evocative_lines:
    - "When experiments detect that subtle off-beat in the Higgs’s song, Pirouette’s resonance will have spoken through the collider’s roar."
    - "Where H curves the energy of space, Γ bends the rhythm of time—two halves of a single heartbeat."
  association_matrix:
    - [ "HIGGS_FIELD", 0.9 ]
    - [ "PRESSURON", 0.8 ]
    - [ "COLLIDER_PHENOMENOLOGY", 0.7 ]
    - [ "DILEPTON_BRANCHING_ENHANCEMENT", 0.4 ]
formal_mappings:
  candidates:
    - target: Scalar Singlet Portal (EFT)
      domain: EFT
      mapping_kind: mathematical
      equation_hint: |
        L ⊃ λ_HS |H|²S²  →  ΔΓ_H
      justification: |
        The interaction Lagrangian `λ_HΓ H†H Γ²` is a specific realization of a "Higgs portal" model, where a new scalar singlet (the Pressuron, Γ) couples to the Higgs doublet squared. Integrating out the Pressuron at low energies generates effective operators that modify Higgs properties, including its propagator and total decay width. This is a canonical BSM scenario.
      references:
        - title: "The Higgs portal for dark matter"
          where: "Patt & Pietroni, New J. Phys. 11 (2009)"
          date: 2009-10-21
      confidence: 0.8
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The Pressuron-Higgs coupling induces a positive correction to the total Higgs width of 0.1%–0.3%."
      domain: phenomenology
      falsifier: "A measurement of Γ_H with <0.1% uncertainty that is consistent with the Standard Model prediction, or a measurement showing a decrease in the width."
      status: proposed
      links: [DYNA-Γ-004]
naming_notes:
  collisions: [The primary symbol for the Pressuron field is Γ, which is also the standard symbol for decay width. Context is critical.]
  disambiguation: |
    Always distinguish between Γ (the Pressuron field) and Γ_H (the Higgs boson's total decay width). The correction itself is the *ratio* ΔΓ_H / Γ_H.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [PRESSURON, HIGGS_FIELD, HIGGS_PRESSURON_COUPLING]
  downstream_effects: [DILEPTON_BRANCHING_ENHANCEMENT, RESONANT_PRODUCTION_TAIL]
license: CC-BY-SA-4.0
---

# Total Width Correction

## Canonical (Pirouette)
The **Total Width Correction** is the predicted fractional increase in the total decay width of the Higgs boson, ΔΓ_H / Γ_H, arising from the gauge-invariant coupling (λ_HΓ) between the Higgs field (H) and the Pressuron field (Γ). The correction is caused by new loop-level decay channels and a shift in the Higgs self-energy. It serves as a primary, high-precision test for the interaction between the electroweak vacuum and temporal pressure.

## EFT-First Summary
In the language of effective field theory, the Pirouette framework's Higgs-Pressuron coupling is a scalar singlet portal interaction. The Pressuron (Γ), acting as a new scalar, couples to the Standard Model via the Higgs boson (`λ_HΓ H†H Γ²`). This portal induces a calculable, positive-definite shift in the Higgs total decay width, predicted to be at the 10⁻³ level. This makes the total width a sensitive probe, testable with projected precision at the HL-LHC and future lepton colliders.

## Glossary Links
- See also: [Pressuron](./pressuron.md), [Higgs-Pressuron Coupling](./higgs_pressuron_coupling.md), [Dilepton Branching Enhancement](./dilepton_branching_enhancement.md)