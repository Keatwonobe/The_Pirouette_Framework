---
term: "Civic Atrophy"
canonical_id: "CIVIC_ATROPHY"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-044"]
---

---
term: Civic Atrophy
canonical_id: CIVIC_ATROPHY
symbol: 
aliases: ["Coherence Erosion", "The Fraying of the Thread"]
parents: ["DOMA-044"]
children: ["INST-SOC-001_placeholder"]
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-044
      snippet: |
        **Civic Atrophy (Coherence Erosion):** The "fraying of the thread" as the social fabric decays.
        **Symptoms:** The slow decay of public infrastructure, erosion of institutional legitimacy, loss of shared cultural identity, cultural amnesia, increasing social isolation.
        **Diagnosis:** The society's Wound Channel—its collective memory and identity—is failing to hold its pattern against entropy. The society is forgetting how to be itself.
  editors: ["system-agent"]
  review_log: []
triad:
  art: |
    The quiet unraveling of a society's tapestry, as the threads of shared memory and purpose grow thin and snap. It is the hollowing out of a culture, leaving behind a brittle, ghost-like shell.
  law: |
    The rate of Civic Atrophy is proportional to the decay of public trust in core institutions and the loss of intergenerational transmission of civic knowledge, measurable via longitudinal surveys and literacy tests.
  philosophy: |
    Civic Atrophy represents a society's thermodynamic failure to maintain its own complex pattern against entropy. It is the terminal condition where a civilization loses the narrative and structural integrity required to solve novel problems, becoming a ghost of itself long before it physically collapses.
pirouette_definition: |
  A societal pathology diagnosed via the Caduceus Lens, characterized by the slow decay of the social fabric, institutional legitimacy, and shared identity. It is a form of Coherence Erosion where the society's Wound Channel fails to retain its organizing pattern. Symptoms include the degradation of public infrastructure, cultural amnesia, and increasing social isolation, indicating the system is "forgetting how to be itself."
operational_definition:
  units: Dimensionless index (Atrophy Index, A_idx), or as a rate (% decay per year).
  symbol_table:
    - name: A_idx
      meaning: Composite index measuring the degree of Civic Atrophy.
      dimensions: dimensionless
      default_range: "[0, 1], where 1 represents total systemic decay."
  measurement:
    procedures:
      - name: Atrophy Index Calculation
        outline: |
          A composite index derived from longitudinal tracking of normalized, equally-weighted indicators:
          1.  **Institutional Trust:** Public trust in government, media, science, and law (inverted scale).
          2.  **Infrastructure Debt:** Net investment in public infrastructure as a percentage of GDP (inverted scale).
          3.  **Social Capital:** Participation rates in civic/community organizations (inverted scale).
          4.  **Cultural Transmission:** Literacy in core national civics and history among young adults (inverted scale).
        expected_signals: ["Sustained decline in trust metrics", "Negative net investment in infrastructure", "Reduced social participation statistics"]
        pitfalls: ["Difficulty in normalizing disparate data sources", "Lag effects masking the true rate of decay", "Defining 'core' civic knowledge can be politically contentious"]
context_windows:
  - module: DOMA-044
    excerpt: |
      **Civic Atrophy (Coherence Erosion):** The "fraying of the thread" as the social fabric decays.
      **Symptoms:** The slow decay of public infrastructure, erosion of institutional legitimacy, loss of shared cultural identity, cultural amnesia, increasing social isolation.
      **Diagnosis:** The society's Wound Channel—its collective memory and identity—is failing to hold its pattern against entropy. The society is forgetting how to be itself.
  - module: DOMA-044
    excerpt: |
      **To Treat Atrophy:** One must reinforce the channel. This is the foundational work of reinvesting in the civic body—rebuilding infrastructure, reforming education to teach civics and systems literacy, and funding art and culture that strengthen shared identity.
poetic_connections:
  motifs: ["forgetting", "unraveling", "decay", "hollowing", "entropy", "ghost"]
  evocative_lines:
    - "The 'fraying of the thread' as the social fabric decays."
    - "The society is forgetting how to be itself."
    - "The Wound Channel...is failing to hold its pattern against entropy."
  association_matrix:
    - [ "COHERENCE_EROSION", 0.9 ]
    - [ "WOUND_CHANNEL", 0.7 ]
    - [ "COHERENCE_DIVIDEND", -0.8 ]
    - [ "CIVIC_SCLEROSIS", 0.3 ]
formal_mappings:
  candidates:
    - target: Information Entropy (S = -Σ pᵢ log pᵢ)
      domain: Information Theory
      mapping_kind: conceptual
      justification: |
        Civic Atrophy represents the decay of a society's shared information and organizing structure (norms, identity, trust). This is analogous to an increase in information entropy, where a low-entropy state (high coherence, shared context) degrades into a high-entropy state (low coherence, fragmented context) as the information encoded in the 'Wound Channel' is lost.
      confidence: 0.6
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "Societies with a high Atrophy Index (A_idx > 0.6) will demonstrate a statistically significant decrease in their capacity to execute and maintain large-scale, long-term (>20 year) public works projects compared to societies with a low index (A_idx < 0.2), controlling for GDP per capita."
      domain: phenomenology
      falsifier: "Observation of a society with a high Atrophy Index successfully completing multiple complex, multi-decade projects without major institutional reform or a reversal of atrophy indicators."
      status: proposed
      links: ["DOMA-044"]
naming_notes:
  collisions: []
  disambiguation: |
    Civic Atrophy must be distinguished from the other primary pathologies:
    - **Civic Sclerosis** is a pathology of *blockage* (e.g., gridlock, hoarding).
    - **Civic Fever** is a pathology of *turbulent conflict* (e.g., polarization, culture wars).
    - **Civic Atrophy** is a pathology of *decay* and *forgetting* (e.g., crumbling infrastructure, loss of identity). It is a slow hollowing-out, not an acute blockage or a high-energy fight.
crosslinks:
  near_synonyms: ["COHERENCE_EROSION"]
  antonyms: ["COHERENCE_DIVIDEND", "CREATIVE_RESONANCE"]
  prerequisites: ["CIVIC_MANIFOLD", "WOUND_CHANNEL", "CADUCEUS_LENS"]
  downstream_effects: ["CIVIC_SCLEROSIS", "CIVIC_FEVER"]
license: CC-BY-SA-4.0
---