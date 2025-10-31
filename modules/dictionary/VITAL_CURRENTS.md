---
term: "Vital Currents"
canonical_id: "VITAL_CURRENTS"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-044"]
---

---
term: Vital Currents
canonical_id: VITAL_CURRENTS
symbol: 
aliases: []
parents: [DOMA-044]
children: [INST-SOC-001_placeholder]
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-044
      lines: "L30-L38"
      snippet: |
        The health of the civic body depends on the laminar flow of three primary **Vital Currents**:
        *   **The Flow of Information:** The society's nervous system.
        *   **The Flow of Resources:** The society's circulatory system.
        *   **The Flow of Trust:** The society's connective tissue, the very medium of its coherence.
  editors: [Agent: Analyst-Zero]
  review_log: []
triad:
  art: |
    The lifeblood of society, flowing as shared knowledge, tangible goods, and the unseen bonds of faith. When they flow freely, the body politic thrives; when they clot, stagnate, or rage, it sickens.
  law: |
    The vitality of a social system, measured by its Coherence Dividend, is a direct function of the laminar flow-rate and quality of its three interdependent currents: Information, Resources, and Trust. A pathology in any one current will propagate predictably to the others.
  philosophy: |
    The Vital Currents reframe governance from a practice of power imposition to one of civic medicine. By focusing on the dynamics of flow rather than static ideologies, they provide a non-partisan diagnostic lens for identifying and healing the root causes of societal dysfunction.
pirouette_definition: |
  The three fundamental, interdependent flows that constitute the metabolism of a Civic Manifold:
  1.  **Information:** The flow of high-fidelity, low-latency, accessible knowledge and narrative (the nervous system).
  2.  **Resources:** The flow of capital, goods, and energy through economic and logistical networks (the circulatory system).
  3.  **Trust:** The flow of social capital and faith in shared institutions, norms, and contracts (the connective tissue).

  Their collective state—laminar, turbulent, or stagnant—determines the society's health, its trajectory toward coherence or collapse, and its capacity to generate a Coherence Dividend.
operational_definition:
  units: State vector of dimensionless indices [I, R, T] or composite flow metrics.
  symbol_table:
    - name: Φ_I
      meaning: Flow of Information
      dimensions: bits/second or dimensionless quality index
      default_range: contextual
    - name: Φ_R
      meaning: Flow of Resources
      dimensions: value/time or mass/time
      default_range: contextual
    - name: Φ_T
      meaning: Flow of Trust
      dimensions: dimensionless index
      default_range: [0, 1]
  measurement:
    procedures:
      - name: Information Flow Audit
        outline: |
          Measure latency and bandwidth of public knowledge (e.g., scientific publication lag, news propagation), signal-to-noise ratio in public discourse (fact vs. misinformation prevalence), and accessibility (literacy rates, internet penetration, censorship indices).
        expected_signals: [mean-time-to-truth, network accessibility, discourse SNR]
        pitfalls: [Goodhart's Law on measurement proxies, difficulty in separating signal from noise in complex narratives]
      - name: Resource Flow Audit
        outline: |
          Measure economic velocity (GDP/M2), supply chain efficiency (delivery times, spoilage rates), infrastructure integrity, and distribution equity (Gini coefficient, social mobility metrics).
        expected_signals: [velocity of money, logistics latency, resource concentration gradients]
        pitfalls: [GDP is a poor proxy for well-being, black markets obscure true flow]
      - name: Trust Flow Audit
        outline: |
          Measure institutional confidence via longitudinal polling (e.g., trust in government, media, science), social capital indices (e.g., participation in civic groups), and contract enforcement efficiency (legal backlogs, corruption perception indices).
        expected_signals: [institutional trust polls, social capital survey data, contract compliance rates]
        pitfalls: [self-reported trust can be unreliable, distinguishing between trust and mere compliance]
context_windows:
  - module: DOMA-044
    excerpt: |
      The health of the civic body depends on the laminar flow of three primary **Vital Currents**: The Flow of Information: The society's nervous system... The Flow of Resources: The society's circulatory system... The Flow of Trust: The society's connective tissue... These currents move through channels shaped by a society's Civic Resonators—its core institutions (laws, markets, media, schools) which define the geometry of the manifold.
  - module: DOMA-044
    excerpt: |
      Any societal ill, from economic stagnation to political polarization, can be diagnosed as a specific pathology of flow within these currents. **Civic Sclerosis (Stagnant Flow):** The "poison of absence" caused by a blockage or dam... **Civic Fever (Turbulent Flow):** The "storm of friction" where the system fights itself... **Civic Atrophy (Coherence Erosion):** The "fraying of the thread" as the social fabric decays.
poetic_connections:
  motifs: [circulation, lifeblood, body politic, river, current, nerve, metabolism, health]
  evocative_lines:
    - "A society is not a machine to be engineered; it is a body to be healed."
    - "The question is no longer 'How do we win?' but 'How do we heal?'"
  association_matrix:
    - [ "CIVIC_MANIFOLD", 0.9 ]
    - [ "CIVIC_RESONATORS", 0.8 ]
    - [ "COHERENCE_DIVIDEND", 0.7 ]
    - [ "CADUCEUS_LENS", 0.6 ]
formal_mappings:
  candidates:
    - target: Network Flow (Max-flow min-cut theorem)
      domain: Math
      mapping_kind: conceptual
      equation_hint: |
        Flow(S, T) <= Capacity(S, T)
      justification: |
        A society can be modeled as a network graph of agents and institutions. Pathologies like Civic Sclerosis are equivalent to bottlenecks (min-cuts) that limit the maximum flow of a Vital Current through the system.
      references:
        - title: Network Flow Algorithms
          where: "Various computer science texts"
          date: 
      confidence: 0.8
  adopted:
    - target: Fluid Dynamics (e.g., Navier-Stokes)
      rationale: The source text's descriptive language of 'laminar', 'turbulent', and 'stagnant' flow, along with 'channels' and 'blockages', is a direct and consistent application of the fluid dynamics analogy to a sociological domain, making it the most fitting formal mapping. The Reynolds number (Re) serves as a powerful analog for the transition from healthy laminar flow to pathological turbulent flow.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "A significant, sustained disruption in one Vital Current (e.g., a financial crisis disrupting Resource flow) will measurably degrade the other two (e.g., reduced trust in institutions, increased misinformation) within a predictable time lag."
      domain: phenomenology
      falsifier: "Multiple, large-scale historical case studies show that the three currents are statistically independent, or that a severe crisis in one (e.g., hyperinflation) has no correlated impact on measures of public trust or information quality."
      status: proposed
      links: [DOMA-044]
naming_notes:
  collisions: [Electric current (physics), Ocean current (geography)]
  disambiguation: |
    In Pirouette, 'Vital Currents' always refer to the specific, interdependent triad of Information, Resources, and Trust within a social system (a Civic Manifold). They are not generic flows but components of a single metabolic system, analogous to physiological systems in a living organism.
crosslinks:
  near_synonyms: []
  antonyms: [CIVIC_SCLEROSIS, CIVIC_FEVER]
  prerequisites: [CIVIC_MANIFOLD, CADUCEUS_LENS]
  downstream_effects: [COHERENCE_DIVIDEND, CIVIC_ATROPHY, CIVIC_RESONATORS]
license: CC-BY-SA-4.0
---