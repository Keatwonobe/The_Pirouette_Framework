---
term: "Temporal Density"
canonical_id: "TEMPORAL_DENSITY"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-Γ-003_pressuron_coupling_to_composite_matter"]
---

---
term: Temporal Density
canonical_id: TEMPORAL_DENSITY
symbol: Implicit (proportional to m_q)
aliases: []
parents: [MATH-Γ-003]
children: [MATH-Γ-004, DYNA-Γ-NUC]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-Γ-003_pressuron_coupling_to_composite_matter
      lines: "§2"
      snippet: |
        At the constituent-quark level, Γ couples to **temporal density** rather than bare charge.
  editors: [Aetherium AI]
  review_log: []
triad:
  art: |
    When quarks hum together, their shared rhythm cancels the loudest parts of the song; only a faint over-tone—the Γ whisper—escapes. The hadron is a silenced drum in the orchestra of time.
  law: |
    The Γ-field contribution to a composite baryon's magnetic moment anomaly is directly proportional to a screening factor and the square of the baryon's mass: Δa_B = η_B (g_Γ²/8π²) (M_B/m_Γ)².
  philosophy: |
    Temporal density extends the Γ-interaction from elementary particles to the complex, composite world of hadrons. It establishes that the Γ-field probes the internal phase structure and mass composition of matter, not just its classical charge, linking sub-nucleonic dynamics to nuclear and astrophysical phenomena.
pirouette_definition: |
  The fundamental source property at the sub-nucleonic scale to which the Γ-field couples. For a constituent quark, temporal density is proportional to its mass (m_i) and determines the strength of its interaction with the pressuron gradient (∂^μ Γ). Within a confined hadron, the net temporal density is coherently suppressed by gluon-mediated phase alignment, resulting in a significantly screened effective coupling.
operational_definition:
  units: Mass (MeV/c²)
  symbol_table:
    - name: m_i
      meaning: Mass of a constituent quark, acting as the measure of its temporal density.
      dimensions: M
      default_range: contextual (e.g., ~340 MeV for u/d quarks)
    - name: η_B
      meaning: Baryonic screening factor, representing the coherence damping of the net temporal density within a hadron.
      dimensions: dimensionless
      default_range: 10⁻⁵ – 10⁻⁶
    - name: Δa_B
      meaning: Additive correction to a baryon's magnetic moment anomaly due to Γ-coupling.
      dimensions: dimensionless
      default_range: 10⁻¹⁰ – 10⁻¹¹
  measurement:
    procedures:
      - name: Indirect via Baryon Magnetic Moment Anomaly
        outline: |
          1. Perform a high-precision measurement of a baryon's (e.g., proton) magnetic moment anomaly, a_B.
          2. Calculate the expected value for a_B from Standard Model QED/QCD contributions to the required precision.
          3. The residual difference, Δa_B = a_B(exp) - a_B(SM), is the signal attributed to the Γ-coupling to the baryon's net temporal density.
          4. Verify the M_B² scaling by comparing residuals from different baryons.
        expected_signals:
          - A non-zero residual Δa_p ~ 10⁻¹⁰ for the proton.
          - A smaller residual Δa_n ~ 10⁻¹¹ for the neutron.
          - A consistent ratio Δa_p / Δa_n ≈ (η_p/η_n)(M_p/M_n)².
        pitfalls:
          - Signal is currently below experimental sensitivity (~10⁻⁸).
          - Theoretical uncertainties in the SM calculation or the screening factor η_B can mask the signal.
          - Other new physics could contribute a confounding signal.
context_windows:
  - module: MATH-Γ-003
    excerpt: |
      At the constituent-quark level, Γ couples to **temporal density** rather than bare charge. For a quark field ( q_i ) with mass ( m_i ) and color current ( j_i^\mu ), the interaction reads […]. Within a confined hadron, this coupling is **screened** by gluon coherence, giving an effective reduction factor ( η_B ≪ 1 ).
  - module: MATH-Γ-003
    excerpt: |
      Inside a baryon, Γ excitation manifests as a **beat pattern** between quark temporal phases. The coherence gradient of these beats defines ( η_B ). When baryons interact coherently (as in dense matter), Γ coupling enhances proportionally to local **phase alignment**, providing a natural link to nuclear binding corrections.
poetic_connections:
  motifs: [temporal phase, coherence, screening, beat pattern, cosmic percussion]
  evocative_lines:
    - "The hadron is thus a silenced drum in the orchestra of time."
    - "When quarks hum together, their shared rhythm cancels the loudest parts of the song."
  association_matrix:
    - [ "Mass", 0.9 ]
    - [ "Coherence", 0.8 ]
    - [ "Γ-field", 0.7 ]
    - [ "Screening", 0.7 ]
formal_mappings:
  candidates:
    - target: Fermion mass (m_f) in axion derivative coupling
      domain: EFT
      mapping_kind: conceptual
      equation_hint: |
        L ⊃ (∂_μ a / f_a) \bar{ψ} γ^μ γ_5 ψ
      justification: |
        In many axion-like-particle (ALP) models, the ALP couples derivatively to the fermion axial-vector current with a strength set by the fermion mass. Temporal density, being proportional to quark mass (m_q), plays an identical role as the source for the Γ-field's derivative coupling.
      references:
        - title: The theory of axions
          where: arXiv:2009.10743
          date: 2020-09-22
      confidence: 0.8
  adopted:
    []
constraints_and_falsifiers:
  claims:
    - statement: "The Γ-field's contribution to hadronic magnetic moment anomalies scales with the square of the baryon mass (Δa_B ∝ M_B²)."
      domain: phenomenology
      falsifier: "Detection of a hadronic magnetic-moment deviation larger than 10⁻⁹ that violates this mass-squared scaling law."
      status: proposed
      links: [MATH-Γ-003]
    - statement: "The net temporal density of a baryon is strongly screened by gluon coherence, with a suppression factor η_B on the order of 10⁻⁵–10⁻⁶."
      domain: theory
      falsifier: "Experimental observation of a Γ-induced correction Δa_B significantly larger than 10⁻⁹ would falsify the composite-screening model."
      status: proposed
      links: [MATH-Γ-003]
naming_notes:
  collisions: []
  disambiguation: |
    Temporal Density is distinct from mass-energy density (T⁰⁰) or charge density. It is the specific source term for the Γ-field's derivative coupling at the quark level, proportional to the quark's rest mass and related to its intrinsic temporal phase oscillation, not its total relativistic energy or electric charge.
crosslinks:
  near_synonyms: []
  antonyms: [CHARGE_DENSITY]
  prerequisites: [PRESSURON]
  downstream_effects: [BARYON_G_FACTOR_ANOMALY, NUCLEAR_COHERENCE]
license: CC-BY-SA-4.0
---

# Temporal Density

## Canonical (Pirouette)
The fundamental source property at the sub-nucleonic scale to which the Γ-field couples. For a constituent quark, temporal density is proportional to its mass (m_i) and determines the strength of its interaction with the pressuron gradient (∂^μ Γ). Within a confined hadron, the net temporal density is coherently suppressed by gluon-mediated phase alignment, resulting in a significantly screened effective coupling.

## EFT-First Summary
Temporal Density is conceptually analogous to the role of fermion mass (m_f) in setting the coupling strength for axion-like particles in Effective Field Theory. In the Pirouette Framework, the Γ-field (an ALP-like scalar) has a derivative coupling to the quark axial-vector current, `∂^μ Γ \bar{q} γ_μ γ_5 q`, and the strength of this interaction is set by the quark's temporal density, which is directly proportional to its mass.

## Glossary Links
- See also: [PRESSURON](<link-not-available>), [BARYON_G_FACTOR_ANOMALY](<link-not-available>)