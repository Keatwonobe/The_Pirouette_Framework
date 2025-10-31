---
term: "Leptonic coupling"
canonical_id: "LEPTONIC_COUPLING"
symbol: "κ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["XAP-007_pressuraon_constraint_atlas"]
---

---
term: Leptonic coupling
canonical_id: LEPTONIC_COUPLING
symbol: κ
aliases: []
parents: [XAP-007, MATH-013]
children: [XAP-008]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: XAP-007
      lines: "§2"
      snippet: |
        Coupling to leptons | κ | 10⁻⁴–10⁻² | from μ,g-2 fit
  editors: [auto-agent]
  review_log: []
triad:
  art: |
    A subtle whisper between the electron's dance and the vacuum's deep hum. It is the measure of how much the world of matter feels the unseen stiffness of spacetime.
  law: |
    The dimensionless coupling strength κ determines the interaction rate between charged leptons and the pressuron sector. It is directly testable via precision measurements (e.g., muon g-2 anomaly) and missing-energy searches, where interaction cross-sections and decay rates are proportional to κ².
  philosophy: |
    κ quantifies the leakage of Γ-stiffness into the Standard Model, acting as a portal between the cosmological substrate and particle physics. It posits that fundamental particles are not isolated but are weakly 'listening' to the underlying coherence of the vacuum, making the universe's large-scale properties observable at the particle scale.
pirouette_definition: |
  The dimensionless coupling strength, denoted κ, that parameterizes the interaction vertex between a charged lepton (l), an anti-lepton (l̄), and the composite pressuron field operator (ΓΓ). This interaction is a primary portal between the Standard Model's matter sector and Pirouette's superfluid pressuron substrate, mediating energy exchange and generating observable corrections to lepton properties and decay channels.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: κ
      meaning: Leptonic coupling strength
      dimensions: dimensionless
      default_range: 10⁻⁴ – 10⁻²
  measurement:
    procedures:
      - name: Muon Anomaly Measurement (g-2)
        outline: |
          Precisely measure the anomalous magnetic moment (a_μ) of the muon and compare it to the Standard Model prediction. A persistent discrepancy (Δa_μ) can be attributed to new physics, with the pressuron contribution scaling as Δa_μ ∝ κ². The observed anomaly suggests κ ≈ 10⁻³.
        expected_signals: [A deviation Δa_μ ≈ 2.5 × 10⁻⁹.]
        pitfalls: [Uncertainties in Standard Model hadronic contributions, contributions from other new physics.]
      - name: Missing Energy Search at Colliders
        outline: |
          Analyze particle collisions (e.g., e⁺e⁻ → γ + missing energy, B → K + missing energy) for events where energy and momentum are not conserved among visible particles. The rate of such events can constrain the production of invisible pressuron pairs, with the cross section σ ∝ κ².
        expected_signals: [An excess of events at a specific missing mass, consistent with a dipressuron signature.]
        pitfalls: [Irreducible backgrounds from neutrino production, detector hermeticity limitations.]
context_windows:
  - module: XAP-007
    excerpt: |
      Pressurons couple weakly to charged leptons via Γ-exchange. Existing electron-beam experiments (SLAC E137, NA64) exclude κ < 10⁻³ for m_p<30 MeV. Future LDMX or FASER2 runs probing visible and invisible channels may reach κ∼10⁻⁴.
  - module: XAP-007
    excerpt: |
      The muon anomaly contribution is Δa_μ ≈ 2.5×10⁻⁹ κ₋₃², providing a strong motivation for the fiducial range of κ. For flavor-diagonal Γ coupling, the neutrino self-interaction cross section σ_νν ~ κ⁴ E_ν²/m_p⁴, can produce cosmological opacity at low energies.
poetic_connections:
  motifs: [portal, leakage, whisper, echo_in_matter]
  evocative_lines:
    - "bridging theoretical elegance with falsifiable prediction."
    - "leakage of Γ-stiffness into the Standard Model"
  association_matrix:
    - [ "PRESSURON", 0.9 ]
    - [ "MUON_ANOMALY", 0.8 ]
    - [ "GAMMA_STIFFNESS", 0.7 ]
    - [ "FIFTH_FORCE", 0.3 ]
formal_mappings:
  candidates:
    - target: Yukawa coupling (g)
      domain: EFT
      mapping_kind: conceptual
      equation_hint: |
        L_int ⊃ κ (l̄l) (ΓΓ)
      justification: |
        κ is a dimensionless constant setting the interaction strength between fermions (leptons) and a bosonic sector (pressurons). It is analogous to a Standard Model Yukawa coupling, but mediates an interaction with a composite scalar-pair operator (ΓΓ) rather than a fundamental scalar like the Higgs.
      references: []
      confidence: 0.8
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The value of κ consistent with all existing data lies in the range 10⁻⁴–10⁻²."
      domain: phenomenology
      falsifier: "Null results from Belle-II or FASER2 pushing the upper bound on κ below 10⁻⁴ for the entire predicted pressuron mass range (10-30 MeV)."
      status: supported
      links: [XAP-007]
    - statement: "A coupling of κ ≈ 10⁻³ can explain the observed muon g-2 anomaly."
      domain: phenomenology
      falsifier: "A revised Standard Model calculation or the discovery of an alternative new physics source that fully accounts for the Δa_μ discrepancy, leaving no room for a pressuron contribution."
      status: proposed
      links: [XAP-007]
    - statement: "Stellar cooling in Horizontal Branch and Red Giant stars constrains κ < 10⁻⁴ if the pressuron mass is below 3 MeV."
      domain: experiment
      falsifier: "Refined stellar evolution models showing significantly less sensitivity to new energy loss channels via pressuron emission."
      status: supported
      links: [XAP-007]
naming_notes:
  collisions: [The symbol κ is also used for spacetime curvature in GR and for kappa distributions in plasma physics. Context (particle interactions, pressuron sector) is essential.]
  disambiguation: |
    Leptonic coupling (κ) describes the direct interaction strength between leptons and the pressuron field. It is distinct from the fifth-force coupling parameter (ε), which describes the effective long-range interaction strength with bulk matter arising from the pressuron's vacuum expectation value.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [PRESSURON, GAMMA_STIFFNESS]
  downstream_effects: [MUON_ANOMALY, STELLAR_COOLING_BOUNDS, MISSING_ENERGY_SIGNATURES]
license: CC-BY-SA-4.0
---

# Leptonic coupling

## Canonical (Pirouette)
The dimensionless coupling strength, denoted κ, that parameterizes the interaction vertex between a charged lepton (l), an anti-lepton (l̄), and the composite pressuron field operator (ΓΓ). This interaction is a primary portal between the Standard Model's matter sector and Pirouette's superfluid pressuron substrate, mediating energy exchange and generating observable corrections to lepton properties and decay channels.

## EFT-First Summary
In an effective field theory description, the leptonic coupling κ acts as a Yukawa-like coupling constant for a higher-dimensional operator connecting Standard Model leptons to a new, light scalar sector (the pressurons). This interaction term, `κ (l̄l) (ΓΓ)`, is strongly constrained by a combination of high-precision measurements like the muon g-2 anomaly, searches for rare decays and missing energy at colliders, and astrophysical bounds from stellar cooling. Current data favor a value of κ ~ 10⁻³ for a pressuron mass in the 10-30 MeV range.

## Glossary Links
- See also: [PRESSURON](./PRESSURON.md), [MUON_ANOMALY](./MUON_ANOMALY.md), [GAMMA_STIFFNESS](./GAMMA_STIFFNESS.md)