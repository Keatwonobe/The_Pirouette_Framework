---
term: "Civic Sclerosis"
canonical_id: "CIVIC_SCLEROSIS"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-044"]
---

---
term: Civic Sclerosis
canonical_id: CIVIC_SCLEROSIS
symbol: Φ⃒
aliases: [Gridlock, Stagnation, Institutional Rigidity]
parents: [DOMA-044]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-044
      lines: "L40-L44"
      snippet: |
        *   **Civic Sclerosis (Stagnant Flow):** The "poison of absence" caused by a blockage or dam.
            *   **Symptoms:** Bureaucratic gridlock, extreme wealth inequality, censorship, lack of social mobility, political paralysis.
            *   **Diagnosis:** A vital current is being hoarded or obstructed. Resources are pooling, creating deserts elsewhere. Trust has decayed to the point that collaboration has seized.
  editors: [Pirouette Framework Agent]
  review_log: []
triad:
  art: |
    The nation's lifeblood congeals in the arteries of power. A desert grows in the heartland while the capitol drowns in its own hoarded wealth. The body politic becomes a statue, magnificent but cold and unmoving.
  law: |
    Civic Sclerosis is operationally defined as a state where the Gini coefficient of a vital current (e.g., wealth, political influence) exceeds a critical threshold (e.g., G > 0.6) while the velocity of that same current (e.g., money velocity, social mobility) falls below a historical baseline for a sustained period. It is a measurable pathology of low flow and high concentration.
  philosophy: |
    Sclerosis reveals that systemic injustice is a form of thermodynamic inefficiency. A society that hoards its vital currents is not only unethical but is actively starving its own future to gorge its present, transforming positive-sum potential into zero-sum gridlock. It is the signature of a system that has forgotten how to circulate life.
pirouette_definition: |
  A pathological state of the Civic Manifold characterized by critically reduced or blocked flow in one or more Vital Currents (Information, Resources, Trust). It arises when Civic Resonators (institutions, laws) create blockages or hoarding mechanisms, leading to extreme concentration gradients (high inequality), systemic paralysis, and a collapse of the Coherence Dividend. Sclerosis is the "poison of absence"—a failure of circulation, not of substance.
operational_definition:
  units: Dimensionless index (S_c), typically normalized to [0, 1].
  symbol_table:
    - name: S_c
      meaning: Index of Civic Sclerosis for a given Vital Current.
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: G
      meaning: Gini coefficient of the current's distribution.
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: v
      meaning: Velocity or throughput of the current (e.g., M2 velocity, legislative bill passage rate).
      dimensions: T⁻¹
      default_range: contextual
  measurement:
    procedures:
      - name: Sclerosis Index (S_c) Calculation
        outline: |
          1.  **Select Vital Current:** Choose a current to analyze (e.g., Resources).
          2.  **Measure Concentration (G):** Calculate the Gini coefficient for the distribution of the chosen current (e.g., wealth Gini). Normalize to a 0-1 scale against historical or comparative data.
          3.  **Measure Velocity (v):** Measure the flow rate of the current (e.g., M2 money velocity, social mobility rate). Normalize its inverse (1/v) to a 0-1 scale, where high values indicate stagnation.
          4.  **Compute Index:** Calculate S_c as a weighted average: `S_c = α * G_norm + (1-α) * (1/v)_norm`. A value approaching 1 indicates severe sclerosis.
        expected_signals: [High Gini coefficient, low money velocity, low social mobility, legislative gridlock, low patent application rates from new entities.]
        pitfalls: [Difficulty in quantifying the "Trust" current. Economic controls can artificially lower velocity without indicating sclerosis. Data availability may be poor in opaque regimes.]
context_windows:
  - module: DOMA-044
    excerpt: |
      Any societal ill, from economic stagnation to political polarization, can be diagnosed as a specific pathology of flow within these currents.

      *   **Civic Sclerosis (Stagnant Flow):** The "poison of absence" caused by a blockage or dam.
          *   **Symptoms:** Bureaucratic gridlock, extreme wealth inequality, censorship, lack of social mobility, political paralysis.
          *   **Diagnosis:** A vital current is being hoarded or obstructed. Resources are pooling, creating deserts elsewhere. Trust has decayed to the point that collaboration has seized.
  - module: DOMA-044
    excerpt: |
      The goal of governance is to restore laminar flow. This is not achieved through brute force, but through the **Daedalus Gambit**: a clever, precise intervention that helps the system heal itself.

      *   **To Treat Sclerosis:** One must dissolve the dam. This requires identifying the critical bottleneck and introducing a catalyst—a key piece of legislation, a technological innovation, or a diplomatic breakthrough.
poetic_connections:
  motifs: [blockage, dam, gridlock, hoarding, congealed flow, stagnation, paralysis, the poison of absence]
  evocative_lines:
    - "The poison of absence caused by a blockage or dam."
    - "Resources are pooling, creating deserts elsewhere."
    - "To Treat Sclerosis: One must dissolve the dam."
  association_matrix:
    - [ "VITAL_CURRENTS", 0.9 ]
    - [ "CIVIC_RESONATORS", 0.8 ]
    - [ "EXTRACTIVE_RESONANCE", 0.7 ]
    - [ "COHERENCE_DIVIDEND", -0.9 ]
formal_mappings:
  candidates:
    - target: Jamming transition
      domain: AMO
      mapping_kind: conceptual
      equation_hint: |
        Viscosity η → ∞ as density φ → φ_c
      justification: |
        In soft condensed matter physics, a jamming transition occurs when a disordered system of particles (e.g., grains, colloids) ceases to flow and becomes rigid as its density exceeds a critical point. This maps directly to legislative or economic gridlock, where an increase in interacting agents or concentrated rules (density) causes the entire system to seize up, behaving like a solid instead of a fluid.
      references:
        - title: Measuring the jamming transition in granular materials
          where: Nature
          date: 1998-07-02
      confidence: 0.8
    - target: Arteriosclerosis
      domain: Biology
      mapping_kind: conceptual
      justification: |
        The source metaphor is explicitly biological. In arteriosclerosis, the hardening and narrowing of arteries restricts blood flow, starving tissues of oxygen and nutrients. This is a direct parallel to sclerotic institutions blocking the flow of resources, information, or trust, leading to the decay of the broader social body.
      references: []
      confidence: 0.9
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "In a given legislature, the rate of novel bill passage will decrease non-linearly as the Gini coefficient of campaign/lobbying funds crosses a critical threshold, consistent with a jamming transition."
      domain: phenomenology
      falsifier: "Legislative gridlock is shown to be linearly correlated with ideological polarization and independent of resource concentration. Or, gridlock can be consistently resolved by increasing legislative resources (e.g., staff, sessions) without addressing financial concentration."
      status: proposed
      links: [DOMA-044]
naming_notes:
  collisions: [The term "sclerosis" is adopted directly from medicine (e.g., multiple sclerosis, arteriosclerosis) to reinforce the "body politic" diagnostic framing of the Civic Manifold.]
  disambiguation: |
    Civic Sclerosis must be distinguished from Civic Fever and Civic Atrophy.
    - **Civic Fever** is turbulent, high-energy, chaotic flow (e.g., civil unrest, market panic).
    - **Civic Atrophy** is the decay of the channels themselves (e.g., decaying infrastructure, loss of institutions).
    - **Civic Sclerosis** is the blockage *within* intact channels, where energy and resources exist but cannot circulate.
crosslinks:
  near_synonyms: [INSTITUTIONAL_GRIDLOCK]
  antonyms: [LAMINAR_FLOW, CIVIC_ALACRITY]
  prerequisites: [VITAL_CURRENTS, CIVIC_RESONATORS]
  downstream_effects: [CIVIC_ATROPHY, COHERENCE_EROSION]
license: CC-BY-SA-4.0
---