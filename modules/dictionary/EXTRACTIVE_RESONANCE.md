---
term: "Extractive Resonance"
canonical_id: "EXTRACTIVE_RESONANCE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-044"]
---

---
term: Extractive Resonance
canonical_id: EXTRACTIVE_RESONANCE
symbol: Ω_E
aliases: [Zero-Sum Resonance, High Entropy State, Civic Fever]
parents: [DOMA-044]
children: [INST-SOC-001_placeholder]
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-044
      lines: "L102-L106"
      snippet: |
        The Extractive Resonance (High Entropy Export): A society tuned to this frequency operates on zero-sum principles. Its resonators amplify conflict, reward short-term extraction, and concentrate power. It is an inefficient `entropy pump` that consumes its own social capital to survive, manifesting as `Turbulent Flow` and a trajectory of collapse.
  editors: [Cognitive Synthesis Agent]
  review_log: []
triad:
  art: |
    The dissonant hum of a society devouring itself. Every gain is another's loss, and the only shared project is the dismantling of the future.
  law: |
    A system is in Extractive Resonance when its Gini coefficient and its Political Polarization Index both exhibit a positive first derivative over one generational cycle (~20 years), while its Social Trust Index exhibits a negative first derivative.
  philosophy: |
    Extractive Resonance is the formal diagnosis for a societal death spiral. It frames pathologies like inequality and polarization not as separate political issues, but as correlated symptoms of a single thermodynamic disease: the failure to generate and sustain coherence.
pirouette_definition: |
  A stable, self-reinforcing state of a `Civic Manifold` where its `Civic Resonators` (institutions) are tuned to amplify zero-sum, high-entropy dynamics. This state is characterized by `Turbulent Flow` of its vital currents (information, resources, trust), the systematic consumption of social capital, and a thermodynamic trajectory toward systemic collapse. It is the direct antithesis of `Creative Resonance`.
operational_definition:
  units: Dimensionless state descriptor, quantified by a vector of social indicators.
  symbol_table:
    - name: Ω_E
      meaning: A binary or continuous variable indicating the degree to which a system is in Extractive Resonance.
      dimensions: dimensionless
      default_range: [0, 1] where 1 is maximum resonance.
  measurement:
    procedures:
      - name: Societal Entropy Rate Analysis
        outline: |
          1.  Acquire longitudinal time-series data (>20 years) for:
              a. Gini Coefficient (Resource Flow turbulence).
              b. Political Polarization Index (e.g., DW-NOMINATE score divergence, legislative voting cohesion) (Information Flow turbulence).
              c. Social Trust Index (e.g., World Values Survey "most people can be trusted" metric) (Trust Flow decay).
          2.  Calculate the first derivative (rate of change) for each series.
          3.  The system is diagnosed with Ω_E > 0.5 if d(Gini)/dt > 0, d(Polarization)/dt > 0, and d(Trust)/dt < 0, sustained over at least one decade.
        expected_signals: [Increasing wealth inequality, escalating partisan hostility, declining public trust in institutions.]
        pitfalls: [Data latency, difficulty in isolating endogenous dynamics from exogenous shocks (e.g., war, pandemic), ambiguity in quantifying "polarization".]
context_windows:
  - module: DOMA-044
    excerpt: |
      A society's Civic Resonators are always tuned to one of two fundamental frequencies, which determines its thermodynamic fate. The Extractive Resonance (High Entropy Export): A society tuned to this frequency operates on zero-sum principles. Its resonators amplify conflict, reward short-term extraction, and concentrate power. It is an inefficient `entropy pump` that consumes its own social capital to survive, manifesting as `Turbulent Flow` and a trajectory of collapse.
  - module: DOMA-044
    excerpt: |
      Civic Fever (Turbulent Flow): The "storm of friction" where the system fights itself. Symptoms: Extreme political polarization, culture wars, market panics, rampant misinformation, civil unrest. Diagnosis: The currents have become chaotic and dissonant. Energy is wasted on internal conflict, destroying social capital and burning the society out from within.
poetic_connections:
  motifs: [entropy pump, self-consumption, dissonance, fever, turbulent flow, zero-sum]
  evocative_lines:
    - "The storm of friction where the system fights itself."
    - "It is an inefficient `entropy pump` that consumes its own social capital to survive."
    - "A dysfunctional manifold...creates a misalignment where a citizen must degrade the collective's coherence...to maximize their own."
  association_matrix:
    - [ "TURBULENT_FLOW", 0.9 ]
    - [ "CIVIC_FEVER", 0.9 ]
    - [ "SOCIAL_CAPITAL", -0.8 ]
    - [ "ZERO_SUM", 0.7 ]
formal_mappings:
  candidates:
    - target: Dissipative System with Runaway Feedback
      domain: CM|Thermodynamics
      mapping_kind: conceptual
      equation_hint: |
        dS/dt > 0, where S is internal systemic entropy.
      justification: |
        Extractive Resonance describes a system that increases its internal entropy (disorder, conflict) by consuming its own ordered structures (social capital, trust). This is analogous to a dissipative system with a runaway positive feedback loop, where energy inputs are inefficiently converted into work and primarily serve to increase the system's temperature and entropy, leading to its eventual structural failure.
      references:
        - title: Non-equilibrium Thermodynamics
          where: Prigogine, I. (1977)
          date: 1977-01-01
      confidence: 0.4
  adopted:
    - target:
      rationale:
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "Societies in a state of Extractive Resonance (as defined by the Societal Entropy Rate Analysis) will exhibit a negative correlation between national R&D spending as a percentage of GDP and long-term economic growth."
      domain: phenomenology
      falsifier: "Observing a statistically significant cohort of nations in Ω_E that demonstrate that high R&D spending still produces long-term growth, implying that capital is not being primarily misallocated or consumed by friction."
      status: proposed
      links: [DOMA-044]
naming_notes:
  collisions: ["Resonance (Physics): Refers to the amplification of vibrations in a system at a specific frequency. That is a direct mechanistic analogy, but here the 'frequency' is a mode of social organization, not a physical oscillation."]
  disambiguation: |
    Extractive Resonance is not a physical vibration. It is a stable, self-reinforcing mode of societal organization, where institutions (`Civic Resonators`) amplify behaviors (extraction, conflict) that define the mode. It is a "resonance" in the sense of a system locking into and reinforcing a specific pattern of behavior.
crosslinks:
  near_synonyms: [CIVIC_FEVER]
  antonyms: [CREATIVE_RESONANCE, COHERENCE_DIVIDEND]
  prerequisites: [CIVIC_MANIFOLD, CIVIC_RESONATORS, TURBULENT_FLOW]
  downstream_effects: [CIVIC_ATROPHY, CIVIC_SCLEROSIS, WOUND_CHANNEL_DECAY]
license: CC-BY-SA-4.0
---