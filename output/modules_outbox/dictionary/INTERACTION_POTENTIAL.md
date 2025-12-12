---
term: "Interaction Potential"
canonical_id: "INTERACTION_POTENTIAL"
symbol: "V_Γ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-035"]
---

---
term: Interaction Potential
canonical_id: INTERACTION_POTENTIAL
symbol: V_Γ
aliases: []
parents: [DOMA-035, CORE-006, CORE-008]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-035
      lines: "L68-L72"
      snippet: |
        The interaction between ideas is governed by the Pirouette Lagrangian (CORE-006): 𝓛_p = K_τ - V_Γ. The "force" between two concepts is the gradient in the coherence manifold they collectively create. We can express the interaction potential `V(A, B)` between two concepts, A and B, as a function of their phase relationship `Δφ`: `V(A, B) ∝ - (Kτ_A * Kτ_B / r) * cos(Δφ)`
  editors: [GPT-4]
  review_log: []
triad:
  art: |
    The gravity between ideas. In-phase concepts fall into each other's arms, creating a deep well of shared meaning. Out-of-phase concepts push each other away, creating turbulent, unstable ground where nothing can be built.
  law: |
    The potential energy between two concepts is proportional to the negative product of their temporal coherences and the cosine of their phase difference. Attraction (V_Γ < 0) occurs when concepts are in-phase (Δφ ≈ 0); repulsion (V_Γ > 0) occurs when they are out-of-phase (Δφ ≈ π).
  philosophy: |
    Interaction Potential replaces the metaphor of "forceful arguments" with the geometry of a shared meaning-space. It asserts that attraction and repulsion are not active choices but are necessary consequences of the way coherent concepts shape the manifold, compelling other ideas to follow paths of least resistance.
pirouette_definition: |
  The potential energy term V_Γ within the Pirouette Lagrangian (𝓛_p = K_τ - V_Γ). It quantifies the energy of a relational configuration between two or more concepts, determined by their respective temporal coherences (Kτ), their separation (r) in meaning-space, and their relative phase (Δφ). A negative potential signifies a stable, attractive configuration (a coherence well), while a positive potential signifies an unstable, repulsive configuration.
operational_definition:
  units: Joules (Coherence-space)
  symbol_table:
    - name: V_Γ
      meaning: Interaction potential between concepts.
      dimensions: M L² T⁻² (Energy)
      default_range: contextual
    - name: Kτ
      meaning: Temporal Coherence; the "mass" of a concept.
      dimensions: M L² T⁻² (Energy)
      default_range: > 0
    - name: r
      meaning: Abstract distance between concepts on the coherence manifold.
      dimensions: L (Length)
      default_range: > 0
    - name: Δφ
      meaning: The phase difference between two conceptual resonances.
      dimensions: dimensionless
      default_range: [0, 2π]
  measurement:
    procedures:
      - name: Inferential Potential Mapping
        outline: |
          1. Identify core concepts (A, B) in a corpus or discourse.
          2. Measure the Temporal Coherence (Kτ) of each concept by analyzing its historical depth, repetition, and internal consistency (e.g., citation persistence, structural integrity).
          3. Estimate the phase relationship (Δφ) via semantic similarity and sentiment analysis (e.g., concepts used in synergistic contexts are in-phase; concepts used in oppositional contexts are out-of-phase).
          4. Estimate the distance (r) using topic modeling or word embedding vector distances.
          5. Calculate V_Γ using the governing equation to predict system dynamics.
        expected_signals: [Semantic convergence into a shared lexicon (V_Γ < 0), persistent terminological schism or "flame wars" (V_Γ > 0)]
        pitfalls: [Difficulty in obtaining a non-arbitrary metric for `r`, mistaking semantic similarity for phase coherence, confounding external Temporal Pressure (Γ) changes with interaction dynamics.]
context_windows:
  - module: DOMA-035
    excerpt: |
      The interaction between ideas is governed by the Pirouette Lagrangian (CORE-006): 𝓛_p = K_τ - V_Γ. The "force" between two concepts is the gradient in the coherence manifold they collectively create. We can express the interaction potential `V(A, B)` between two concepts, A and B, as a function of their phase relationship `Δφ`: `V(A, B) ∝ - (Kτ_A * Kτ_B / r) * cos(Δφ)`.
  - module: DOMA-035
    excerpt: |
      Attraction (Constructive Interference): When two concepts are in-phase (`Δφ ≈ 0`), their resonances constructively interfere. The interaction potential becomes strongly negative, creating a deeper, more stable shared basin of meaning. Repulsion (Destructive Interference): When two concepts are out-of-phase (`Δφ ≈ π`), their resonances destructively interfere. The interaction potential becomes positive, creating a region of intense temporal turbulence and dissonance.
poetic_connections:
  motifs: [resonance, interference, gravity well, harmony, dissonance, orbital mechanics]
  evocative_lines:
    - "The geometry of synergy and the drive toward an Alchemical Union."
    - "A spike in temporal turbulence and dissonance."
    - "The law that bends a conversation toward a foundational truth."
  association_matrix:
    - [ "TEMPORAL_COHERENCE", 0.9 ]
    - [ "PHASE", 0.9 ]
    - [ "COHERENCE_MANIFOLD", 0.8 ]
    - [ "ALCHEMICAL_UNION", 0.6 ]
formal_mappings:
  candidates:
    - target: Gravitational Potential Energy
      domain: CM
      mapping_kind: mathematical
      equation_hint: |
        V_g = -G * (m1 * m2 / r)  <==>  V_Γ ∝ - (Kτ_A * Kτ_B / r)
      justification: |
        The mathematical form is a direct analogue, with Temporal Coherence (Kτ) playing the role of mass (m). This aligns with the "Gravity of Meaning" model where influence arises from the curvature of the coherence manifold induced by "massive" concepts. The `cos(Δφ)` term is an additional degree of freedom not present in classical gravity.
      references:
        - title: The Gravity of Meaning
          where: DOMA-035 §1
          date: 2025-10-18
      confidence: 0.8
    - target: Dipole-Dipole Interaction Potential
      domain: E&M
      mapping_kind: conceptual
      equation_hint: |
        V_dipole ∝ (1/r^3) * [p1·p2 - 3(p1·r̂)(p2·r̂)]
      justification: |
        The dependence on relative orientation (`cos(Δφ)`) is conceptually similar to the interaction between two dipoles, which can be attractive or repulsive based on how they are aligned. This captures the phase-dependent nature of V_Γ better than the purely attractive gravitational potential.
      references:
        - title: Introduction to Electrodynamics
          where: Griffiths, Ch. 3-4
          date: 1981-01-01
      confidence: 0.6
  adopted:
    - target: Gravitational Potential Energy (with phase modulation)
      rationale: The parent module DOMA-035 explicitly and repeatedly frames the interaction in terms of gravity and mass. While imperfect, this is the intended and most generative mapping within the Pirouette Framework. The phase term is treated as a uniquely Pirouettan modification to the classical analogue.
      confidence: 0.85
constraints_and_falsifiers:
  claims:
    - statement: "In a discourse with low, stable background Temporal Pressure, the semantic distance between two concepts with a calculated V_Γ < 0 will decrease over time, while the distance between two concepts with V_Γ > 0 will increase or remain large."
      domain: phenomenology
      falsifier: "A statistically significant observation of high-coherence, in-phase concepts (`cos(Δφ) ≈ 1`) actively diverging, or out-of-phase concepts (`cos(Δφ) ≈ -1`) converging, in a controlled information environment."
      status: proposed
      links: [DOMA-035]
naming_notes:
  collisions: [V (common physics symbol for potential energy), U (alternative physics symbol for potential energy)]
  disambiguation: |
    V_Γ must be distinguished from the ambient Temporal Pressure (Γ). Γ is the background scalar field property of the manifold itself, analogous to temperature or pressure. V_Γ is the relational potential energy *between specific concepts* existing on that manifold. A high-Γ environment can amplify the effects of V_Γ.
crosslinks:
  near_synonyms: []
  antonyms: [KINETIC_COHERENCE]
  prerequisites: [TEMPORAL_COHERENCE, PHASE, COHERENCE_MANIFOLD]
  downstream_effects: [NARRATIVE_GEODESIC, ALCHEMICAL_UNION]
license: CC-BY-SA-4.0
---

# Interaction Potential

## Canonical (Pirouette)
The potential energy term V_Γ within the Pirouette Lagrangian (𝓛_p = K_τ - V_Γ). It quantifies the energy of a relational configuration between two or more concepts, determined by their respective temporal coherences (Kτ), their separation (r) in meaning-space, and their relative phase (Δφ). A negative potential signifies a stable, attractive configuration (a coherence well), while a positive potential signifies an unstable, repulsive configuration.

## EFT-First Summary
The Interaction Potential V_Γ serves a role analogous to the **Gravitational Potential Energy** in classical mechanics, as defined in DOMA-035. Its mathematical form, `V_Γ ∝ - (Kτ_A * Kτ_B / r)`, directly maps Temporal Coherence (Kτ) to mass. A key distinction is the additional `cos(Δφ)` modulation factor, meaning the interaction can be attractive (gravitational) or repulsive based on the phase alignment of the concepts, a feature more akin to dipole interactions in electromagnetism.

## Glossary Links
- See also: [Temporal Coherence](<link>), [Phase](<link>), [Coherence Manifold](<link>), [Pirouette Lagrangian](<link>)