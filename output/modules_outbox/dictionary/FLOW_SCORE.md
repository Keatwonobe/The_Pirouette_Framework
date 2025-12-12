---
term: "Flow Score"
canonical_id: "FLOW_SCORE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-HLTH-003"]
---

---
term: Flow Score
canonical_id: FLOW_SCORE
symbol: 
aliases: [Mind's Voice]
parents: [DOMA-HLTH-003]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-HLTH-003
      lines: "§4.III"
      snippet: |
        The Practice: Continue to log your two numbers daily:
        The Body's Voice: Resting Heart Rate.
        The Mind's Voice: Your subjective "Flow Score" (1-10).
  editors: [Gemini-1.5-Pro]
  review_log: []
triad:
  art: |
    The quiet hum of the engine of self, a self-reported number that captures the feeling of a river finding its channel again. It is the inner ear attuning to the song of healing.
  law: |
    The Flow Score is a daily, subjective self-rating on an integer scale from 1 (lowest ease, highest friction) to 10 (highest ease, lowest friction), representing a patient's perceived momentum and lack of internal resistance.
  philosophy: |
    To make an individual's inner state a first-class citizen in the data of their own becoming. It validates the 'Mind's Voice' as a reliable sensor for internal coherence, empowering the patient as the primary witness to their own recovery.
pirouette_definition: |
  A subjective, self-reported integer on a 1-10 scale, recorded daily as part of the Coherence Ledger. It represents the "Mind's Voice," quantifying an individual's perceived ease, momentum, and internal coherence, particularly during periods of rhythm-building or recovery. It serves as a qualitative complement to physiological metrics like Resting Heart Rate.
operational_definition:
  units: dimensionless integer scale
  symbol_table:
    - name: S_flow
      meaning: Flow Score
      dimensions: dimensionless
      default_range: "[1, 10]"
  measurement:
    procedures:
      - name: Daily Self-Assessment
        outline: |
          At a consistent time each day (e.g., upon waking), the individual reflects on their overall feeling of ease, momentum, and lack of struggle over the past 24 hours. They assign a single integer from 1 ("high struggle, no flow") to 10 ("effortless ease, strong flow") that best represents this internal state. The score is immediately recorded in the Coherence Ledger.
        expected_signals: [Resting Heart Rate]
        pitfalls: [Recall bias (forgetting to log and estimating later), mood-conflation (allowing transient emotions to disproportionately influence the score), anchoring (basing today's score too heavily on yesterday's)]
context_windows:
  - module: DOMA-HLTH-003
    excerpt: |
      The Practice: Continue to log your two numbers daily: The Body's Voice: Resting Heart Rate. The Mind's Voice: Your subjective "Flow Score" (1-10). The New Step: Chart Your Course. At the end of each week, plot these two numbers on a simple line graph.
  - module: DOMA-HLTH-003
    excerpt: |
      Your most important job is to be the storyteller of the data. At the end of the week, sit with the patient and show them the graph. Say, "Look. This is where you started. Look how much your heart rate has calmed. Look how your 'flow' is climbing. You are doing this." This act of witnessing is a profound gift.
poetic_connections:
  motifs: [mind's voice, gentle current, story of comeback, finding the song]
  evocative_lines:
    - "Look how your 'flow' is climbing."
    - "This chart becomes the undeniable proof of your journey."
    - "The sound of your own life, finding its song again."
  association_matrix:
    - [ "COHERENCE_LEDGER", 0.9 ]
    - [ "TEMPORAL_COHERENCE", 0.8 ]
    - [ "RESTING_HEART_RATE", 0.9 ]
    - [ "HELPER_AS_PACESETTER", 0.6 ]
formal_mappings:
  candidates:
    - target: Patient-Reported Outcome Measure (PROM) / Quality of Life (QoL) score
      domain: Medicine|Psychology
      mapping_kind: operational
      equation_hint: |
        S_flow(t) ≈ f(QoL_daily)
      justification: |
        Flow Score is a simplified, single-item PROM designed for high-frequency (daily) longitudinal tracking. Unlike complex multi-question surveys (e.g., SF-36), its purpose is to provide a low-friction, high-sensitivity signal of subjective well-being and functional ease during a specific intervention period.
      references:
        - title: Assessing the quality of life
          where: NEJM 319 (1988)
          date: 1988-08-11
      confidence: 0.9
  adopted:
    - target: Patient-Reported Outcome Measure (PROM)
      rationale: The term operationally describes a PROM used for daily tracking, aligning perfectly with its function and application in the source module.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "A consistently increasing Flow Score, when tracked longitudinally, correlates positively with decreasing Resting Heart Rate and increasing functional capacity (e.g., daily walking duration) in post-operative Phase II recovery."
      domain: phenomenology
      falsifier: "A study of patients following the protocol shows no significant correlation, or a negative correlation, between the trend of their Flow Score and the trends of their objective physiological and functional metrics."
      status: proposed
      links: [DOMA-HLTH-003]
naming_notes:
  collisions: [Psychological "flow state" (M. Csikszentmihalyi)]
  disambiguation: |
    Distinguish from the psychological concept of a 'flow state,' which describes deep immersion in a specific activity. The Pirouette 'Flow Score' is a broader, daily self-assessment of general well-being and ease of being—a measure of the background state of flow, not the peak state of task immersion.
crosslinks:
  near_synonyms: [MIND'S_VOICE]
  antonyms: []
  prerequisites: [COHERENCE_LEDGER]
  downstream_effects: [HELPER_AS_PACESETTER]
license: CC-BY-SA-4.0
---

# Flow Score

## Canonical (Pirouette)
A subjective, self-reported integer on a 1-10 scale, recorded daily as part of the Coherence Ledger. It represents the "Mind's Voice," quantifying an individual's perceived ease, momentum, and internal coherence, particularly during periods of rhythm-building or recovery. It serves as a qualitative complement to physiological metrics like Resting Heart Rate.

## EFT-First Summary
The Flow Score is a Patient-Reported Outcome Measure (PROM), specifically a single-item Quality of Life (QoL) score, captured daily. It operationalizes the patient's subjective experience, providing a high-frequency, longitudinal dataset that complements objective physiological measurements like heart rate. This data stream is crucial for tracking the recovery of an agent's Temporal Coherence (Kτ).

## Glossary Links
- See also: Resting Heart Rate, Coherence Ledger, Temporal Coherence