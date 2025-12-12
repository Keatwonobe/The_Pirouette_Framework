---
term: "Echo Score"
canonical_id: "ECHO_SCORE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-HLTH-004"]
---

---
term: Echo Score
canonical_id: ECHO_SCORE
symbol: Eₑ
aliases: [body response rating]
parents: [DOMA-HLTH-004]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-HLTH-004
      snippet: |
        The Echo Score (1-10): The day after a challenge, rate how your body responded. 1 = "I am exhausted, sore, and feel worse than before." 5 = "I feel a little tired, but a good tired." 10 = "I feel energized, strong, and ready for more."
  editors: [System Agent]
  review_log: []
triad:
  art: |
    The body is a bell. A challenge strikes it, and the Echo Score is the quality of the tone heard the next day—a clear, resonant hum of strength, or a dull, discordant thud of strain.
  law: |
    A post-challenge Echo Score below 5 mandates a reduction in the intensity or duration of the subsequent challenge. A score of 8 or higher permits a marginal, calibrated increase. The score acts as the primary feedback governor on the rate of hormetic stress application.
  philosophy: |
    The Echo Score operationalizes the principle that adaptation occurs during rest, not stress. By shifting the focus of measurement to the day *after* the work, it privileges recovery as the true engine of resilience and teaches the patient to listen to their body's quiet signals of growth.
pirouette_definition: |
  A subjective, ordinal score from 1 (poor) to 10 (excellent) recorded in the Coherence Ledger on the day following a hormetic challenge (e.g., Crucible Walk, Resilience Ritual). It quantifies the patient's integrated physiological and psychological response to the applied stress, serving as the primary feedback signal for calibrating the intensity of future challenges.
operational_definition:
  units: Dimensionless ordinal scale [1, 10].
  symbol_table:
    - name: Eₑ
      meaning: Echo Score
      dimensions: dimensionless
      default_range: [1, 10]
  measurement:
    procedures:
      - name: Post-Challenge Subjective Assessment
        outline: |
          On the morning of the day following a Crucible Walk or Resilience Ritual, the patient and helper discuss and agree upon a single integer score. The assessment is based on the patient's holistic feeling of energy, muscle soreness, mood, and readiness for activity, guided by the benchmark descriptions: 1="exhausted/worse", 5="good tired", 10="energized/strong". The score is recorded in the Coherence Ledger.
        expected_signals: [Patient's subjective report, Helper's objective observations of patient's energy levels and movement quality]
        pitfalls: [Mood bias influencing score, desire for progress creating upward bias, difficulty distinguishing challenge-induced fatigue from other life stressors.]
context_windows:
  - module: DOMA-HLTH-004
    excerpt: |
      Goal 2: Listen to the Echo. After every challenge, we will listen. The body's response—its "echo"—tells us everything we need to know. A feeling of energized fatigue is a "yes." Sharp pain or prolonged exhaustion is a "no."
  - module: DOMA-HLTH-004
    excerpt: |
      The Echo Score (1-10): The day after a challenge, rate how your body responded... Is their Echo Score consistently low after the Resilience Ritual? Perhaps the number of repetitions is too high. Did their Flow Score drop the day after a Crucible Walk? Maybe the "brisk" pace was a little too brisk. The ledger is no longer just a record of the past; it is the blueprint for calibrating the next challenge.
  - module: DOMA-HLTH-004
    excerpt: |
      The "Echo Score" is your subjective measurement of the result. A high score signifies that your body has successfully adapted, increasing its internal Temporal Coherence (Kτ) to a new, higher baseline. You are not just spending energy; you are investing it.
poetic_connections:
  motifs: [listening, resonance, feedback, tempering, blueprint, signal, recovery]
  evocative_lines:
    - "Listen to the Echo."
    - "The growth does not happen during the stress, but in the quiet recovery that follows."
    - "The ledger... is the blueprint for calibrating the next challenge."
  association_matrix:
    - [ "COHERENCE_LEDGER", 0.9 ]
    - [ "COHERENCE_FORGING", 0.8 ]
    - [ "TEMPORAL_COHERENCE", 0.6 ]
    - [ "FLOW_SCORE", 0.5 ]
formal_mappings:
  candidates:
    - target: Perceived Recovery Status (PRS)
      domain: Sports Science
      mapping_kind: operational
      justification: |
        Both PRS and the Echo Score are simple, subjective, ordinal scales (e.g., 0-10) used to assess a patient's state of recovery on the day after a challenge. They serve the same function: to modulate the subsequent training load based on the individual's adaptive response.
      references:
        - title: "Monitoring training status with a new perceived recovery status scale"
          where: "J Strength Cond Res. 2013 Aug;27(8):2257-62."
          date: 2013-08-01
      confidence: 0.8
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "A sustained pattern of high Echo Scores (≥8) following a stable challenge protocol is a leading indicator of an increase in baseline Temporal Coherence (Kτ)."
      domain: phenomenology
      falsifier: "Demonstrating a cohort of patients who report consistently high Echo Scores but show no corresponding objective improvement or stabilization in other Coherence Ledger metrics like Resting Heart Rate or functional exercise capacity over a 4-week period."
      status: proposed
      links: [DOMA-HLTH-004]
naming_notes:
  collisions: []
  disambiguation: |
    The Echo Score is distinct from:
    - **Flow Score**: Which measures the quality of state *during* a calm, rhythmic activity.
    - **Rating of Perceived Exertion (RPE)**: Which measures effort *during* a challenge.
    The Echo Score is a retrospective measure of the body's adaptive *response* on the day *after* a challenge.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [COHERENCE_LEDGER, COHERENCE_FORGING]
  downstream_effects: [CRUCIBLE_WALK, RESILIENCE_RITUAL]
license: CC-BY-SA-4.0