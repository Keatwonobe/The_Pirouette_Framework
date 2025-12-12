---
term: "Maw Population"
canonical_id: "MAW_POPULATION"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["XAP-004_appendix_addendum_A_through_L"]
---

---
term: Maw Population
canonical_id: MAW_POPULATION
symbol: N(f)
aliases: [Event Source Population, Stochastic Background]
parents: [XAP-004, PPS-037]
children: [PPS-037]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: XAP-004_appendix_addendum_A_through_L
      snippet: |
        Annex J – Maw Population Prior & Event‑Rate Curve
        Model: Broken‑power‑law source density N(f) with slope −2.2 above 1 GHz.
        Predicted event rate for strain h ≥ 10⁻²⁵: 0.3 ± 0.1 yr⁻¹.
  editors: [auto-agent-alpha]
  review_log: []
triad:
  art: |
    From the silent dark, countless mouths whisper events into being. The Maw is not one source, but a chorus of cosmic static whose loudest voices are rare, and whose whispers are constant.
  law: |
    The number density of external event sources, `N(f)`, follows a broken power law, decaying with a spectral index of -2.2 for frequencies above 1 GHz.
  philosophy: |
    To understand the signal, one must first characterize the noise. The Maw Population model provides a falsifiable prior for the universe of external influences, preventing the misattribution of stochastic background events to internal system dynamics.
pirouette_definition: |
  The Maw Population is the statistical model of the ensemble of external, non-systemic event sources that can trigger Pirouette state changes. It is characterized by its number density `N(f)` as a function of event frequency `f`. The canonical prior for this population is a broken-power-law distribution with a spectral index of -2.2 above a break frequency of 1 GHz.
operational_definition:
  units: Hz⁻¹ (for number density)
  symbol_table:
    - name: N(f)
      meaning: Maw Population number density per unit frequency
      dimensions: T
      default_range: contextual
    - name: f
      meaning: Event frequency
      dimensions: T⁻¹
      default_range: > 1 GHz
    - name: h
      meaning: Event strain
      dimensions: dimensionless
      default_range: contextual
  measurement:
    procedures:
      - name: Background Event Rate Integration
        outline: |
          Integrate the number of observed external events binned by frequency over a long observation time (≥ 1 year). Fit the resulting distribution `N(f)` to a broken-power-law model to extract the spectral index and break frequency. Compare the integrated rate above a given strain threshold to the model's prediction.
        expected_signals: [Stochastic background of discrete events, Power-law signature in event frequency distribution]
        pitfalls: [Misclassifying internal system noise as external events, Insufficient observation time leading to poor statistics]
context_windows:
  - module: XAP-004_appendix_addendum_A_through_L
    excerpt: |
      **Annex J – Maw Population Prior & Event‑Rate Curve**
      Model: Broken‑power‑law source density N(f) with slope −2.2 above 1 GHz.
      Predicted event rate for strain h ≥ 10⁻²⁵: 0.3 ± 0.1 yr⁻¹.
  - module: XAP-004_appendix_addendum_A_through_L
    excerpt: |
      **Annex K – Power‑Analysis Appendix (§12, PPS‑037)**
      ### Kaon Tail Shift
      • Trigger efficiency 0.02
      • Runtime ≈ 8 months at LHCb (95 % power)
poetic_connections:
  motifs: [stochastic background, cosmic static, external influence, power-law]
  evocative_lines:
    - "Model: Broken‑power‑law source density..."
    - "...whose loudest voices are rare, and whose whispers are constant."
  association_matrix:
    - [ "Γ_thr", 0.3 ]
    - [ "Externality Footprint Tag", 0.5 ]
formal_mappings:
  candidates:
    - target: Stochastic Gravitational-Wave Background (SGWB)
      domain: GR
      mapping_kind: conceptual
      equation_hint: |
        Ω_gw(f) ∝ f^α
      justification: |
        The Maw Population is modeled as a stochastic background of events with a power-law frequency distribution. This is conceptually and mathematically analogous to the astrophysical stochastic gravitational-wave background, which is composed of a superposition of many independent, unresolved sources.
      references:
        - title: Stochastic Gravitational-Wave Backgrounds
          where: Living Reviews in Relativity, 19, 1
          date: 2016-01-11
      confidence: 0.7
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The spectral index of the Maw Population number density N(f) is -2.2 for f > 1 GHz."
      domain: phenomenology
      falsifier: "Direct measurement of the event rate vs. frequency distribution yields a statistically significant deviation from the -2.2 index or reveals a different break frequency."
      status: proposed
      links: [XAP-004, PPS-037]
    - statement: "The integrated event rate for strain h ≥ 10⁻²⁵ is 0.3 ± 0.1 yr⁻¹."
      domain: experiment
      falsifier: "A multi-year observation campaign measures an event rate outside this 95% confidence interval."
      status: proposed
      links: [XAP-004, PPS-037]
naming_notes:
  collisions: [M (Mass), M₀ (Reference Mass)]
  disambiguation: |
    `Maw Population` refers to the statistical ensemble of external event sources, not to be confused with `M`, the symbol for mass used in scaling laws (e.g., Γ(M)).
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: []
  downstream_effects: []
license: CC-BY-SA-4.0
---

# Maw Population

## Canonical (Pirouette)
The Maw Population is the statistical model of the ensemble of external, non-systemic event sources that can trigger Pirouette state changes. It is characterized by its number density `N(f)` as a function of event frequency `f`. The canonical prior for this population is a broken-power-law distribution with a spectral index of -2.2 above a break frequency of 1 GHz.

## EFT-First Summary
The Maw Population is analogous to a stochastic background field, such as the astrophysical gravitational-wave background. It is modeled as a superposition of many unresolved sources whose event rate density follows a power law in frequency, `N(f) ∝ f⁻²·²`, leading to a predictable rate of high-strain events.

## Glossary Links
- See also: Externality Footprint Tag, Γ_thr