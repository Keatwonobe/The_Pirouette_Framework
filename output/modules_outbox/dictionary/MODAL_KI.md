---
term: "Modal Ki"
canonical_id: "MODAL_KI"
symbol: "Ki_m"
aliases: [Phase-Lock Configuration]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-185"]
---

---
term: Modal Ki
canonical_id: MODAL_KI
symbol: Ki_m
aliases: [Phase-Lock Configuration]
parents: [DOMA-185]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-185
      lines: "L45-L47"
      snippet: |
        **Modal Ki (Ki_m)** | The specific geometric pattern of resonance that defines the mode. It is the "musical score" for that state.
  editors: [system]
  review_log: []
triad:
  art: |
    The unique musical score of a stable state; the specific, self-sustaining song a system has learned to sing to maintain its form against the pressures of time.
  law: |
    A stable operational mode exists if and only if it corresponds to a distinct, recurring, and geometrically patterned Ki resonance (`Ki_m`) that occupies a local maximum on the system's Coherence Manifold.
  philosophy: |
    A system's identity lies not in its present action but in its repertoire of potential actions. By identifying the set of possible `Ki_m`, we map the system's character and understand the discrete "ways of being" available to it.
pirouette_definition: |
  Modal Ki is the specific, high-order, geometric pattern of Ki resonance that uniquely defines a system's quasi-stable operational mode. Each distinct `Ki_m` corresponds to a local maximum (a 'Modal Basin') on the system's Coherence Manifold, representing a self-sustaining, coherent solution to local Temporal Pressure (Γ). The collection of all possible `Ki_m` for a system constitutes its Resonant Repertoire.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: Ki_m
      meaning: Modal Ki resonance pattern
      dimensions: dimensionless (represents a geometric configuration)
      default_range: contextual (describes a pattern, not a scalar value)
  measurement:
    procedures:
      - name: Modal Identification via Spectral Clustering
        outline: |
          Analyze system data streams using spectral analysis or manifold learning techniques (e.g., UMAP, t-SNE) to identify recurring, distinct geometric patterns in the Ki resonance field. Cluster these patterns to isolate and catalog the set of unique `Ki_m` that constitute the system's Resonant Repertoire.
        expected_signals: [Clear clusters in a low-dimensional embedding of Ki field data; distinct peaks in a spectral density plot.]
        pitfalls: [Mistaking transient noise for a stable mode; insufficient temporal data to distinguish closely related modes.]
context_windows:
  - module: DOMA-185
    excerpt: |
      Instead of the previous framework's complex vectors, we now characterize each mode with a few clear, physically grounded parameters derived from the Coherence Manifold. A crucial distinction is made between a state's instantaneous quality and its historical, ingrained stability. **Modal Ki (Ki_m)** is the specific geometric pattern of resonance that defines the mode. It is the "musical score" for that state.
  - module: DOMA-185
    excerpt: |
      A system does not smoothly slide from one mode to another; it leaps. This transition, a form of Ki Morphogenesis, is a rapid, non-linear reconfiguration of the system's entire resonant pattern... Resonant Catalysis: A transition can also be induced with surgical precision. By introducing a signal that resonates with a *target* mode's `Ki_m`, it is possible to lower the Transition Cost for that specific pathway.
poetic_connections:
  motifs: [song, score, pattern, habit, stability, signature]
  evocative_lines:
    - "It is the 'musical score' for that state."
    - "...the hidden songs it knows how to sing."
  association_matrix:
    - [ "RESONANT_REPERTOIRE", 1.0 ]
    - [ "COHERENCE_MANIFOLD", 0.9 ]
    - [ "KI_MORPHOGENESIS", 0.8 ]
    - [ "WOUND_CHANNEL", 0.7 ]
formal_mappings:
  candidates:
    - target: Metastable vacuum state |ψ⟩
      domain: QFT
      mapping_kind: conceptual
      equation_hint:
      justification: |
        In QFT, a system can possess multiple distinct, quasi-stable vacuum states, each a local minimum of an effective potential. A `Ki_m` is analogous to a single such vacuum: it is a specific, stable field configuration (a peak on the Coherence Manifold) that defines a system's 'ground state' of operation. Transitions between modes mirror quantum tunneling or phase transitions between vacua.
      references:
        - title: An Introduction to Quantum Field Theory
          where: Chapter on Spontaneous Symmetry Breaking
          date: 1995-01-01
      confidence: 0.6
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "Every persistent, quasi-stable operational mode of a system corresponds to a unique and identifiable Modal Ki (`Ki_m`)."
      domain: phenomenology
      falsifier: "Observing a system with two or more distinct, stable operational modes that cannot be distinguished by their geometric Ki resonance patterns, or observing a stable system lacking a clear, recurring `Ki_m`."
      status: supported
      links: [DOMA-185]
naming_notes:
  collisions: []
  disambiguation: |
    `Ki_m` (Modal Ki) is not the instantaneous Ki field itself, but the specific, time-averaged geometric *pattern* of that field which defines a stable mode. It is the 'shape' of the resonance, not the resonance at a single moment.
crosslinks:
  near_synonyms: [PHASE_LOCK_CONFIGURATION]
  antonyms: [TURBULENT_FLOW]
  prerequisites: [KI, GEOMETRY_OF_RESONANCE]
  downstream_effects: [COHERENCE_HEIGHT, STABILITY_DEPTH, WOUND_CHANNEL_INERTIA, KI_MORPHOGENESIS]
license: CC-BY-SA-4.0
---