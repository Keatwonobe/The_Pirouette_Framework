---
term: "Civic Fever"
canonical_id: "CIVIC_FEVER"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-044"]
---

---
term: Civic Fever
canonical_id: CIVIC_FEVER
symbol: 
aliases: [Storm of Friction]
parents: [DOMA-044]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-044
      lines: "§3"
      snippet: |
        Civic Fever (Turbulent Flow): The "storm of friction" where the system fights itself.
        Symptoms: Extreme political polarization, culture wars, market panics, rampant misinformation, civil unrest.
        Diagnosis: The currents have become chaotic and dissonant. Energy is wasted on internal conflict, destroying social capital and burning the society out from within.
  editors: [SystemAgent]
  review_log: []
triad:
  art: |
    A societal body turning on itself, burning with the heat of its own internal friction. It is the sound of a system tearing its own connective tissue apart in a dissonant roar of conflict.
  law: |
    Civic Fever is a state where the energy dissipated by internal social friction (e.g., polarization, misinformation amplification) exceeds the energy invested in positive-sum creative synthesis. It is quantified by a high ratio of chaotic-to-laminar information flow, measured by metrics like network polarization and misinformation velocity.
  philosophy: |
    Civic Fever reveals that a society's greatest enemy is its own misaligned internal dynamics, not an external threat. It reframes the goal of governance from 'winning' zero-sum conflicts to healing the underlying conditions that generate wasteful, turbulent flow.
pirouette_definition: |
  A societal pathology diagnosed via the Caduceus Lens, characterized by turbulent, chaotic flow in the Vital Currents (information, resources, trust). It manifests as wasted energy, extreme polarization, misinformation, and the rapid destruction of social capital, driven by a system tuned to an Extractive Resonance.
operational_definition:
  units: Dimensionless index (Civic Turbulence Index, CTI)
  symbol_table:
    - name: Θ_F
      meaning: Civic Turbulence Index, a measure of Civic Fever intensity.
      dimensions: dimensionless
      default_range: "[0, 1], where > 0.7 indicates critical fever."
  measurement:
    procedures:
      - name: Information Flow Turbulence Analysis
        outline: |
          1. Map a society's primary information/discourse network graph (e.g., social media, news media citations).
          2. Quantify network polarization into N mutually hostile communities using community detection algorithms (e.g., Louvain modularity).
          3. Measure the ratio of high-velocity, low-fidelity information cascades (misinformation) to low-velocity, high-fidelity cascades (verified knowledge).
          4. Calculate Θ_F as a function of network modularity, the ratio of antagonistic cross-community links to cooperative links, and the misinformation amplification factor.
        expected_signals: [High network modularity, rapid amplification of low-fidelity information, high sentiment negativity in cross-community links.]
        pitfalls: [Difficulty in establishing ground truth for information fidelity, sampling bias in network data, confounding effects of external shocks.]
context_windows:
  - module: DOMA-044
    excerpt: |
      **Civic Fever (Turbulent Flow):** The "storm of friction" where the system fights itself. Symptoms: Extreme political polarization, culture wars, market panics, rampant misinformation, civil unrest. Diagnosis: The currents have become chaotic and dissonant. Energy is wasted on internal conflict, destroying social capital and burning the society out from within.
  - module: DOMA-044
    excerpt: |
      **To Treat Fever:** One must introduce a harmonizing signal. This involves creating a focal point for coherence that the turbulent system can organize around—a unifying national project, a transparent source of trusted information, or a platform for good-faith dialogue.
poetic_connections:
  motifs: [fever, storm, friction, dissonance, self-consumption, wildfire]
  evocative_lines:
    - "The 'storm of friction' where the system fights itself."
    - "...burning the society out from within."
  association_matrix:
    - [ "TURBULENT_FLOW", 0.9 ]
    - [ "EXTRACTIVE_RESONANCE", 0.8 ]
    - [ "COHERENCE_EROSION", 0.7 ]
    - [ "CIVIC_SCLEROSIS", 0.2 ]
formal_mappings:
  candidates:
    - target: Kolmogorov energy cascade (in fluid turbulence)
      domain: CM
      mapping_kind: conceptual
      equation_hint: |
        Energy cascades from large eddies (national narratives) to small eddies (interpersonal conflict) where it is dissipated as 'heat' (social capital loss).
      justification: |
        Civic Fever is modeled as a state of high turbulence in a society's information manifold. Just as a high Reynolds number leads to chaotic eddies that dissipate energy, a high Civic Turbulence Index leads to polarized social structures that dissipate social capital through non-productive, high-friction interactions (e.g., flame wars, misinformation campaigns).
      references:
        - title: Turbulence: The Legacy of A. N. Kolmogorov
          where: Cambridge University Press
          date: 1995-01-26
      confidence: 0.7
  adopted:
    []
constraints_and_falsifiers:
  claims:
    - statement: "Societies exhibiting higher metrics of Civic Fever (e.g., network polarization, misinformation velocity) will demonstrate a measurable decrease in their capacity for large-scale, long-term cooperative projects."
      domain: phenomenology
      falsifier: "A society could exhibit high levels of internal political friction and polarization while simultaneously increasing its rate of successful, complex, cooperative achievements (e.g., major scientific breakthroughs, infrastructure projects). This would suggest that the 'frictional energy' is not dissipative or is decoupled from productive capacity."
      status: proposed
      links: [DOMA-044]
naming_notes:
  collisions: [Medical term "fever"]
  disambiguation: |
    Distinguish from Civic Sclerosis, which is a pathology of *stagnant* or blocked flow, not chaotic flow. Civic Fever is an active, high-energy, self-destructive process of internal conflict, whereas Sclerosis is a slow, paralytic decay from lack of interaction.
crosslinks:
  near_synonyms: [TURBULENT_FLOW, EXTRACTIVE_RESONANCE]
  antonyms: [LAMINAR_FLOW, CIVIC_SCLEROSIS, COHERENCE_DIVIDEND]
  prerequisites: [CIVIC_MANIFOLD, VITAL_CURRENTS, CADUCEUS_LENS]
  downstream_effects: [COHERENCE_EROSION, CIVIC_ATROPHY]
license: CC-BY-SA-4.0
---

# Civic Fever

## Canonical (Pirouette)
A societal pathology diagnosed via the Caduceus Lens, characterized by turbulent, chaotic flow in the Vital Currents (information, resources, trust). It manifests as wasted energy, extreme polarization, misinformation, and the rapid destruction of social capital, driven by a system tuned to an Extractive Resonance.

## EFT-First Summary
Civic Fever is modeled as a state of high turbulence in a society's information manifold. Analogous to the energy cascade in fluid dynamics, large-scale political narratives fracture into small-scale, high-friction social eddies (e.g., online polarization) that dissipate collective energy and destroy social capital, preventing its investment in coherent, system-level work.

## Glossary Links
- See also: Civic Sclerosis, Turbulent Flow, Coherence Dividend