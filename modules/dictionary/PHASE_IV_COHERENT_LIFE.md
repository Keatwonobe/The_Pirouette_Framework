---
term: "Phase IV: Coherent Life"
canonical_id: "PHASE_IV_COHERENT_LIFE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-HLTH-006"]
---

---
term: Phase IV: Coherent Life
canonical_id: PHASE_IV_COHERENT_LIFE
symbol: 
aliases: [Maintenance Phase, Community Phase]
parents: [DOMA-HLTH-006, PHASE_III_BUILD_THE_ARENA]
children: []
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-HLTH-006
      lines: "41"
      snippet: |
        Maintenance / community   | Phase IV: Coherent Life    | > 3 months onward             | Autonomy, interval work, lifestyle embedding | Long-term risk factor control, periodic reassessments
  editors: [scribe-agent-alpha]
  review_log: []
triad:
  art: |
    The recovery is no longer a project, but the quiet rhythm of the day. The arena has dissolved into the landscape of a life lived well, where strength is a reflex and health a habit. This is the graduate's walk, unburdened by the memory of the fall.
  law: |
    A patient enters Phase IV when their functional reserve (Kτ) is stable or slowly increasing with self-directed activity, and their adherence to core lifestyle rituals (Tₐ) exceeds 80% over a trailing 30-day period. The state is maintained as long as Kτ does not degrade beyond a pre-set threshold and no new destabilizing conditions arise.
  philosophy: |
    Phase IV marks the transition from 'recovering patient' to 'resilient individual'. Its telos is to render the framework invisible by embedding its principles so deeply into daily life that they become autonomous behaviors, freeing the individual from the cognitive load of constant, deliberate self-monitoring.
pirouette_definition: |
  The final, long-term phase of the Pirouette-Rehab protocol, typically beginning more than three months post-event. It emphasizes patient autonomy, the integration of health-sustaining rituals into daily life, and a shift from structured, supervised training to self-directed, maintenance-oriented activity. The goal is a sustained high state of Coherence (Kτ) with minimal external guidance, transforming recovery into a permanent lifestyle.
operational_definition:
  units: Categorical (state)
  symbol_table: []
  measurement:
    procedures:
      - name: Phase IV Entry Assessment
        outline: |
          1. Assess Kτ stability via longitudinal tracking of functional proxies (e.g., 6MWD, peak VO₂, self-reported energy levels) over the final 4-6 weeks of Phase III.
          2. Measure Tₐ by reviewing patient logs (digital or manual) for adherence to core exercise, diet, and stress-management rituals.
          3. Conduct a psychosocial assessment to gauge patient confidence and self-efficacy in managing their own health regimen without direct supervision.
        expected_signals: [Stable or positive slope in Kτ proxies, Tₐ > 80%, High self-reported readiness for autonomy]
        pitfalls: [Patient overconfidence leading to premature discharge from Phase III, Failure to establish sustainable/enjoyable rituals leading to Tₐ decay, Social or environmental factors disrupting established habits]
context_windows:
  - module: DOMA-HLTH-006
    excerpt: |
      | Clinical Phase            | Pirouette Phase            | Typical Duration              | Core Activities                              | Key Safety Checks / Clinical Flags                          |
      | ------------------------- | -------------------------- | ----------------------------- | -------------------------------------------- | ----------------------------------------------------------- |
      | Maintenance / community   | Phase IV: Coherent Life    | > 3 months onward             | Autonomy, interval work, lifestyle embedding | Long-term risk factor control, periodic reassessments       |
poetic_connections:
  motifs: [autonomy, sustainability, habit, resilience, graduation]
  evocative_lines:
    - "The arena has dissolved into the landscape of a life lived well."
    - "transforming recovery into a permanent lifestyle."
  association_matrix:
    - [ "COHERENCE", 0.9 ]
    - [ "TIME_ADHERENCE", 0.8 ]
    - [ "AUTONOMY", 0.9 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Phase 3 Cardiac Rehabilitation (Maintenance)
      domain: Clinical Medicine
      mapping_kind: conceptual
      equation_hint:
      justification: |
        Phase IV directly corresponds to the long-term maintenance phase of traditional, multi-phase cardiac rehabilitation programs. Both focus on lifestyle modification, risk factor control, and self-monitoring after the conclusion of supervised sessions. Pirouette's distinction is its explicit focus on Kτ and Tₐ as measurable success criteria for this autonomous phase.
      references:
        - title: Cardiac Rehabilitation - StatPearls
          where: NCBI Bookshelf, NBK537196
          date: 2024-02-20
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "Patients who successfully enter and maintain Phase IV will exhibit a lower rate of rehospitalization and a slower decline in functional capacity (Kτ proxies) over a 5-year period compared to patients who only complete supervised CR without a structured maintenance phase."
      domain: phenomenology
      falsifier: "A longitudinal study showing no statistically significant difference in 5-year outcomes (rehospitalization, mortality, 6MWD) between the Phase IV group and a control group that completed standard outpatient CR."
      status: proposed
      links: [DOMA-HLTH-006]
naming_notes:
  collisions: [Phase IV clinical trial]
  disambiguation: |
    In Pirouette, 'Phase IV' is not a clinical trial (i.e., post-market surveillance) but the final, operational stage of an individual's recovery protocol, focused on sustainable, autonomous living. The context is individual rehabilitation, not population-level drug or device study.
crosslinks:
  near_synonyms: []
  antonyms: [PHASE_I_RE_TUNE]
  prerequisites: [PHASE_III_BUILD_THE_ARENA]
  downstream_effects: [COHERENCE]
license: CC-BY-SA-4.0
---

# Phase IV: Coherent Life

## Canonical (Pirouette)
The final, long-term phase of the Pirouette-Rehab protocol, typically beginning more than three months post-event. It emphasizes patient autonomy, the integration of health-sustaining rituals into daily life, and a shift from structured, supervised training to self-directed, maintenance-oriented activity. The goal is a sustained high state of Coherence (Kτ) with minimal external guidance, transforming recovery into a permanent lifestyle.

## Clinical Summary
Phase IV aligns with the maintenance phase (historically Phase 3) of standard Cardiac Rehabilitation. It represents the transition from supervised care to long-term, self-managed health, focused on embedding exercise and risk-reduction behaviors into daily life to prevent secondary events and maintain functional capacity. Success in this phase is defined by sustained patient autonomy and stable health outcomes.
(Ref: [Cardiac Rehabilitation - StatPearls, NCBI](https://www.ncbi.nlm.nih.gov/books/NBK537196/))

## Glossary Links
- See also: [Phase III: Build the Arena](<placeholder-link>), [Coherence (Kτ)](<placeholder-link>), [Time Adherence (Tₐ)](<placeholder-link>)