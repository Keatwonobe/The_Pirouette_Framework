---
term: "Decoupling Function"
canonical_id: "DECOUPLING_FUNCTION"
symbol: "F_ℓ(m_Γ)"
aliases: [Decoupling Kernel]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["XAP-008_Leptonic_g-2_gladiator_force_fit_map"]
---

---
term: Decoupling Function
canonical_id: DECOUPLING_FUNCTION
symbol: F_ℓ(m_Γ)
aliases: [Decoupling Kernel]
parents: ['XAP-008_Leptonic_g-2_gladiator_force_fit_map']
children: []
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
  editors: [Automated Agent]
  review_log: []
triad:
  art: |
    A heavy pressuron's song, heard only by those massive enough to resonate. For the light electron, it is but a distant hum, a force decoupled from its world.
  law: |
    The function F_ℓ(m_Γ) = m_ℓ² / (m_ℓ² + m_Γ²) quantifies the suppression of a Γ-mediated interaction for a lepton ℓ. In the limit where the pressuron is much heavier than the lepton (m_Γ >> m_ℓ), the function and its effect scale as (m_ℓ/m_Γ)².
  philosophy: |
    The Decoupling Function implements a core principle of effective field theory: heavy new physics can be hidden from low-energy probes. It allows a single new force to address the muon g-2 anomaly while naturally respecting the much tighter constraints from the electron g-2, simply by virtue of the electron's smaller mass.
pirouette_definition: |
  A dimensionless form factor, F_ℓ(m_Γ) = m_ℓ² / (m_ℓ² + m_Γ²), that modulates the strength of the pressuron (Γ) force's contribution to a lepton's anomalous magnetic moment. It suppresses the interaction for leptons (ℓ) with mass m_ℓ much smaller than the pressuron mass m_Γ, ensuring that new physics effects scale with lepton mass and naturally satisfy stringent low-energy constraints.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: F_ℓ(m_Γ)
      meaning: Decoupling Function for lepton ℓ
      dimensions: dimensionless
      default_range: [0, 1]
    - name: m_ℓ
      meaning: Mass of the lepton (e.g., electron, muon)
      dimensions: M
      default_range: mₑ ≈ 0.511 MeV, m_μ ≈ 105.7 MeV
    - name: m_Γ
      meaning: Mass of the pressuron
      dimensions: M
      default_range: 1–100 MeV
  measurement:
    procedures:
      - name: Leptonic g-2 Anomaly Fit
        outline: |
          Infer the value of F_ℓ(m_Γ), and thus constrain m_Γ, by performing a global fit of a model's free parameters to experimental measurements of the electron and muon anomalous magnetic moments (Δa_e, Δa_μ). The function's value is determined by the ratio of observed effects on different leptons.
        expected_signals: [A significant Δa_μ accompanied by a suppressed Δa_e, consistent with F_μ/F_e > (m_μ/m_e) for a given model.]
        pitfalls: [Model degeneracy (other new physics could contribute to g-2), uncertainty in experimental measurements of Δa_ℓ.]
context_windows:
  - module: XAP-008_Leptonic_g-2_gladiator_force_fit_map
    excerpt: |
      The electron bound dominates the viable set; decoupling F_e(m_Γ) pushes solutions toward m_Γ≳10–30 MeV *or* larger p.
poetic_connections:
  motifs: [scale separation, mass hierarchy, screening, resonance]
  evocative_lines:
    - "decoupling F_e(m_Γ) pushes solutions toward m_Γ≳10–30 MeV"
  association_matrix:
    - [ "Pressuron", 0.9 ]
    - [ "Lepton Mass", 0.9 ]
    - [ "Anomalous Magnetic Moment", 0.8 ]
formal_mappings:
  candidates:
    - target: Kinematic suppression factor
      domain: EFT
      mapping_kind: mathematical
      equation_hint: |
        F ~ (low_scale)² / ((low_scale)² + (high_scale)²)
      justification: |
        The function has the mathematical structure of a momentum- or mass-dependent suppression factor common in loop calculations in Quantum Field Theory. It acts analogously to how a heavy virtual particle in a loop diagram (with mass m_Γ) has its effects suppressed at energy scales (here represented by m_ℓ) far below its mass. This is a specific realization of the Appelquist-Carazzone decoupling theorem.
      references:
        - title: The Appelquist-Carazzone Decoupling Theorem
          where: Phys. Rev. D 11, 2856
          date: 1975-05-15
      confidence: 0.9
  adopted:
    []
constraints_and_falsifiers:
  claims:
    - statement: "The Γ-force contribution to Δa_ℓ is suppressed for m_ℓ << m_Γ according to F_ℓ(m_Γ) = m_ℓ² / (m_ℓ² + m_Γ²)."
      domain: phenomenology
      falsifier: "An observation of a significant Δa_e from the Γ-force that is not suppressed relative to Δa_μ in a way consistent with this function, given an independently determined pressuron mass m_Γ >> m_e."
      status: proposed
      links: ['XAP-008_Leptonic_g-2_gladiator_force_fit_map']
naming_notes:
  collisions: [The symbol 'F' is overloaded, commonly representing force or generic functions. The subscript 'ℓ' and argument 'm_Γ' are essential for disambiguation.]
  disambiguation: |
    This is not a fundamental force law, but a derived form factor emerging from a loop-level calculation specific to the Γ-lepton interaction. It should not be confused with tree-level propagator effects, though it shares a similar mathematical structure.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [PRESSURON]
  downstream_effects: [ANOMALOUS_MAGNETIC_MOMENT]
license: CC-BY-SA-4.0
---

# Decoupling Function

## Canonical (Pirouette)
A dimensionless form factor, F_ℓ(m_Γ) = m_ℓ² / (m_ℓ² + m_Γ²), that modulates the strength of the pressuron (Γ) force's contribution to a lepton's anomalous magnetic moment. It suppresses the interaction for leptons (ℓ) with mass m_ℓ much smaller than the pressuron mass m_Γ, ensuring that new physics effects scale with lepton mass and naturally satisfy stringent low-energy constraints.

## EFT-First Summary
In effective field theory, the Decoupling Function is a kinematic suppression factor that arises from loop diagrams involving a heavy mediator (the pressuron, with mass m_Γ). It embodies the Appelquist-Carazzone decoupling theorem, ensuring that heavy virtual particles have suppressed effects on low-energy observables like the anomalous magnetic moment of light leptons (with mass m_ℓ). This allows new physics to explain the muon g-2 anomaly while remaining consistent with stringent electron g-2 constraints, as the effect is naturally smaller for the lighter electron.

## Glossary Links
- See also: Pressuron, Anomalous Magnetic Moment