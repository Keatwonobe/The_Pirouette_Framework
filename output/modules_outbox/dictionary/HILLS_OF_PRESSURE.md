---
term: "Hills of Pressure"
canonical_id: "HILLS_OF_PRESSURE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-122"]
---

---
term: Hills of Pressure
canonical_id: HILLS_OF_PRESSURE
symbol: 
aliases: []
parents: [DOMA-122]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-122
      lines: "§2"
      snippet: |
        Hills of Pressure: These are regions of high temporal pressure (VΓ), representing the stresses of incarceration, the complexities of legal proceedings, and the friction of societal stigma.
  editors: [system]
  review_log: []
triad:
  art: |
    The steep, exhausting climbs on the landscape of justice, where progress demands a heavy toll of spirit and hope. These are the system's imposed burdens, shaping paths through friction and cost.
  law: |
    A region in a coherence manifold where the gradient of temporal pressure (∇Γ) is high, causing a geodesic path to lose temporal coherence (Kτ) at a rate proportional to the local pressure VΓ. The probability of an agent successfully traversing the region is inversely related to the integrated pressure along their path.
  philosophy: |
    Hills of Pressure embody the principle that systemic friction is a real, measurable force. Identifying and lowering these hills is the primary work of just reform, shifting focus from individual 'failure' to environmental 'cost'.
pirouette_definition: |
  Topological features of a coherence manifold characterized by high potential temporal pressure (VΓ). These regions represent systemic barriers, frictions, and stresses—such as incarceration, legal complexity, and social stigma—that an agent's geodesic path must overcome. Traversing a Hill of Pressure imposes a direct cost on the agent's temporal coherence (Kτ), making stable, pro-social trajectories less probable.
operational_definition:
  units: Coherence (K)
  symbol_table:
    - name: VΓ
      meaning: Potential temporal pressure, representing the "height" of the hill.
      dimensions: Coherence (K)
      default_range: contextual
    - name: ΔKτ
      meaning: Change in an agent's temporal coherence after traversing the hill.
      dimensions: Coherence (K)
      default_range: contextual, typically negative
  measurement:
    procedures:
      - name: Cohort Trajectory Analysis
        outline: |
          1. Define a cohort of individuals at a specific point in the justice system (e.g., post-release).
          2. Track proxies for temporal coherence (Kτ) over time: stable housing, employment rates, mental health scores, community engagement.
          3. Identify systemic interaction points (e.g., parole hearings, job application processes, court fee payments) that consistently correlate with sharp, negative drops in Kτ across the cohort.
          4. Aggregate these points to map the location and magnitude (VΓ) of the Hills of Pressure on the manifold.
        expected_signals: [recidivism spikes post-parole violation, high unemployment rates for ex-offenders, sharp drops in self-reported well-being after encountering bureaucratic hurdles]
        pitfalls: [confounding individual psychological factors with systemic pressures, difficulty in isolating single causal barriers, ethical constraints on data collection]
context_windows:
  - module: DOMA-122
    excerpt: |
      Hills of Pressure: These are regions of high temporal pressure (VΓ), representing the stresses of incarceration, the complexities of legal proceedings, and the friction of societal stigma. Overcoming these hills requires an immense expenditure of an individual's internal coherence (Kτ).
  - module: DOMA-122
    excerpt: |
      Temporal Pressure (VΓ): This term represents the "potential energy" cost imposed by the system's landscape. It is the sum of punitive laws, social stigma, economic barriers, systemic bias, and the chaotic stress of incarceration. A purely punitive system is one that maximizes VΓ, creating a high-cost environment where maintaining coherence is nearly impossible.
poetic_connections:
  motifs: [uphill battle, systemic friction, cost of passage, weathering the storm]
  evocative_lines:
    - "Overcoming these hills requires an immense expenditure of an individual's internal coherence."
    - "Justice is not the art of damning the river. It is the slow, patient, and sacred work of tending to the landscape."
  association_matrix:
    - [ "TEMPORAL_PRESSURE", 0.9 ]
    - [ "WOUND_CHANNEL", 0.7 ]
    - [ "RECIDIVISM_AS_TURBULENCE", 0.8 ]
    - [ "VALLEYS_OF_COHERENCE", -0.9 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Potential Energy Barrier V(x)
      domain: CM
      mapping_kind: mathematical
      equation_hint: |
        ΔKτ ≈ -∫ VΓ ⋅ dl
      justification: |
        Hills of Pressure function as potential energy barriers in a classical system. An agent's "kinetic energy" (Kτ) must be sufficient to overcome the "potential energy" (VΓ) of the hill. Failure results in being trapped or repelled, analogous to a ball failing to roll over a hill.
      references:
        - title: Classical Mechanics
          where: Chapter 4: Work and Energy
          date: 
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "Increasing the 'height' of a Hill of Pressure (e.g., by adding more legal barriers for ex-offenders) will measurably increase recidivism rates within a cohort, controlling for individual factors."
      domain: phenomenology
      falsifier: "A large-scale study shows that increasing such barriers has no statistically significant effect on recidivism, suggesting that an individual's internal coherence (Kτ) is the sole determinant of outcomes and the manifold's topology (VΓ) is irrelevant."
      status: proposed
      links: [DOMA-122]
naming_notes:
  collisions: []
  disambiguation: |
    Distinguish between the topological feature (the "Hill") and the underlying field ("Temporal Pressure," Γ). A Hill of Pressure is a specific *region* on the manifold where the potential VΓ is high; Γ is the underlying *field* that generates the landscape's topology.
crosslinks:
  near_synonyms: []
  antonyms: [VALLEYS_OF_COHERENCE]
  prerequisites: [TEMPORAL_PRESSURE, COHERENCE_MANIFOLD]
  downstream_effects: [RECIDIVISM_AS_TURBULENCE, COHERENCE_ATROPHY]
license: CC-BY-SA-4.0
---

# Hills of Pressure

## Canonical (Pirouette)
Topological features of a coherence manifold characterized by high potential temporal pressure (VΓ). These regions represent systemic barriers, frictions, and stresses—such as incarceration, legal complexity, and social stigma—that an agent's geodesic path must overcome. Traversing a Hill of Pressure imposes a direct cost on the agent's temporal coherence (Kτ), making stable, pro-social trajectories less probable.

## EFT-First Summary
In analogy to classical mechanics, Hills of Pressure act as potential energy barriers on the coherence manifold. An individual's trajectory requires sufficient 'kinetic' coherence (Kτ) to overcome the potential (VΓ) of the hill. These barriers are not fundamental forces but emergent topological features arising from the complex interplay of laws, institutional friction, and social stigma, representing the systemic 'cost' of rehabilitation.

## Glossary Links
- See also: [Valleys of Coherence](VALLEYS_OF_COHERENCE), [Temporal Pressure](TEMPORAL_PRESSURE), [Recidivism as Turbulence](RECIDIVISM_AS_TURBULENCE)