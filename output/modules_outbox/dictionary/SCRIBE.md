---
term: "Scribe"
canonical_id: "SCRIBE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-HLTH-002"]
---

---
term: Scribe
canonical_id: SCRIBE
symbol: 
aliases: [Keeper of the Record, Ledger-Keeper]
parents: [DOMA-HLTH-002]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-HLTH-002
      lines: "§4.III"
      snippet: |
        Helper's Role (The Scribe): Your job is to be the keeper of the record. Help the patient take their pulse. Write down the numbers. Do not judge the numbers. A "bad" day is not a failure; it is simply data. By recording the journey without judgment, you create a powerful, factual story of their progress...
  editors: [agent:pirouette-lexicographer]
  review_log: []
triad:
  art: |
    The Scribe holds the pen but not the judgment, turning the raw data of a healing journey into a map of hope. By witnessing the fluctuations of the river without condemning its currents, the Scribe makes the invisible path visible.
  law: |
    A Scribe must record specified objective (e.g., resting heart rate) and subjective (e.g., self-rated flow state) metrics into the Coherence Ledger at a regular cadence, without adding interpretation, judgment, or emotional charge to the raw data. The record's value is proportional to its neutrality and consistency.
  philosophy: |
    The act of non-judgmental observation is a powerful intervention. By separating data from story, the Scribe provides a stable external reference point, preventing the patient from getting lost in the narrative of a "bad day" and anchoring their perception in the longer, truer arc of recovery.
pirouette_definition: |
  The Scribe is the designated function of a Helper responsible for the consistent and non-judgmental recording of pre-defined objective and subjective metrics in a Coherence Ledger. This role externalizes the process of self-observation, reducing the patient's cognitive load and providing a neutral, factual narrative of their state dynamics over time. The Scribe's primary duty is to ensure the integrity and neutrality of the data, thereby creating a reliable map of the system's trajectory from high turbulence (low `𝓛_p`) toward a stable baseline.
operational_definition:
  units: n/a (procedural role)
  symbol_table: []
  measurement:
    procedures:
      - name: Coherence Ledger Maintenance
        outline: |
          At a pre-agreed daily interval, the Scribe facilitates the measurement of the patient's Resting Heart Rate (RHR) and asks for their subjective 'flow' rating (1-10). The Scribe then records the date, time, RHR value, and flow rating in a physical or digital log. The Scribe must refrain from reacting positively or negatively to the numbers.
        expected_signals: [time-series of (RHR, flow_rating) pairs]
        pitfalls: [Judging the numbers ("Oh, that's high today!"), inconsistent measurement times, forgetting to record data, introducing personal emotional state into the recording process.]
context_windows:
  - module: DOMA-HLTH-002
    excerpt: |
      Helper's Role (The Scribe): Your job is to be the keeper of the record. Help the patient take their pulse. Write down the numbers. Do not judge the numbers. A "bad" day is not a failure; it is simply data. By recording the journey without judgment, you create a powerful, factual story of their progress that they can look back on during difficult moments.
  - module: DOMA-HLTH-002
    excerpt: |
      The Coherence Ledger (Mapping the Riverbed). This is your shared map of the healing journey. It makes the invisible visible. Use a simple notebook. Once a day, at a consistent time, record two numbers: The Body's Voice (Objective): Your Resting Heart Rate... and The Mind's Voice (Subjective): On a scale of 1 to 10, answer the question: "How 'in the flow' do I feel today?"
poetic_connections:
  motifs: [witnessing, non-judgment, mapping, record-keeping, neutral observation]
  evocative_lines:
    - "A 'bad' day is not a failure; it is simply data."
    - "Mapping the Riverbed."
  association_matrix:
    - [ "Coherence Ledger", 0.9 ]
    - [ "Helper", 0.7 ]
    - [ "Anchor", 0.5 ]
    - [ "Lagrangian (𝓛_p)", 0.3 ]
formal_mappings:
  candidates:
    - target: Laboratory Notebook Keeper / Data Logger
      domain: Experimental Science
      mapping_kind: operational
      equation_hint:
      justification: |
        The Scribe function is directly analogous to the scientific practice of keeping a meticulous, objective lab notebook. The rigor of recording data, time, and conditions without emotional interpretation is central to both roles, ensuring data integrity for later analysis.
      references:
        - title: "On Being a Scientist: A Guide to Responsible Conduct in Research"
          where: "National Academies Press, 3rd ed."
          date: 2009-01-01
      confidence: 0.8
  adopted:
    - target: Laboratory Notebook Keeper
      rationale: This mapping best captures the core function of the Scribe: the disciplined, non-judgmental recording of data to create an objective history of a system's evolution. It grounds the role in the established scientific principle that clean data precedes valid insight.
      confidence: 0.8
constraints_and_falsifiers:
  claims:
    - statement: "The act of a neutral third-party Scribe recording a patient's Coherence Ledger metrics results in a more stable and positive recovery trajectory (as measured by rate of RHR decrease and flow_rating increase) compared to patient self-recording or no recording."
      domain: phenomenology
      falsifier: "A controlled study showing no statistically significant difference in recovery outcomes between patients with a Scribe, patients who self-record, and a control group with no ledger."
      status: proposed
      links: [DOMA-HLTH-002]
naming_notes:
  collisions: [Common term in software for logging libraries (e.g., Scribe, ScribeJava).]
  disambiguation: |
    In the Pirouette context, Scribe is not a software logger but a specific human role within a dyadic (patient-helper) protocol. It always implies a *person* performing a function of neutral observation and recording, distinct from automated data logging.
crosslinks:
  near_synonyms: [RECORDER, OBSERVER]
  antonyms: [INTERPRETER, JUDGE]
  prerequisites: [HELPER, COHERENCE_LEDGER]
  downstream_effects: [COHERENCE_STABILIZATION]
license: CC-BY-SA-4.0