---
term: "Coherence Gradient"
canonical_id: "COHERENCE_GRADIENT"
symbol: "∇𝓛_p"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-120"]
---

---
term: Coherence Gradient
canonical_id: COHERENCE_GRADIENT
symbol: ∇𝓛_p
aliases: [Gravitational Strength (deprecated), Coherence Slope]
parents: [DOMA-120]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-120
      lines: "25-28"
      snippet: |
        Coherence Gradient (∇𝓛_p): This replaces `Gravitational Strength`. It is the "steepness" of the slope leading into the well, a direct feature of the coherence manifold. A belief with a steep gradient is highly influential, presenting itself as the most logical or satisfying path for nearby thoughts. This is the allure of the song, the pull of the current.
  editors: [Weaver-Agent-7]
  review_log: []
triad:
  art: |
    The irresistible slope into a river of thought, where the current promises clarity and the banks fall away. It is the allure of an answer that feels like coming home.
  law: |
    The rate of change of the Pirouette Lagrangian (𝓛_p) across the cognitive manifold; it quantifies the force exerted by a Coherence Well on a cognitive trajectory, compelling it toward states of locally maximal coherence and temporal stability.
  philosophy: |
    The gradient reveals that the power of an idea is not in its 'truth' but in its geometry. It provides a causal mechanism for intellectual capture and dogma, reframing them not as moral failures but as predictable outcomes of a mind seeking a path of least action on a structured manifold.
pirouette_definition: |
  The Coherence Gradient (∇𝓛_p) is the vector field on the cognitive manifold that represents the local rate and direction of maximum increase of the Pirouette Lagrangian (𝓛_p). As the gradient of the coherence potential, it defines the 'force' of a Coherence Well, directing cognitive flow along geodesics toward regions of greater resonant depth (Kτ_well) and temporal stability. A steep gradient signifies a highly influential paradigm that efficiently entrains nearby thought patterns into laminar flow.
operational_definition:
  units: Dimensionless (often expressed in bits per state-space unit)
  symbol_table:
    - name: ∇𝓛_p
      meaning: Coherence Gradient, the vector representing the local 'force' of a paradigm.
      dimensions: [Coherence]/[Length]
      default_range: contextual
    - name: 𝓛_p
      meaning: The Pirouette Lagrangian, the quantity maximized by a cognitive trajectory.
      dimensions: [Coherence]
      default_range: contextual
  measurement:
    procedures:
      - name: Gradient Mapping via Semantic Probes
        outline: |
          1. Identify the core concepts of a target Coherence Well within a discourse network (e.g., a large language model fine-tuned on the paradigm's texts).
          2. Introduce a set of neutral or ambiguous 'probe concepts' into the semantic neighborhood of the well.
          3. Measure the semantic shift vector (e.g., cosine distance change in an embedding space) of these probes after a fixed number of inferential steps.
          4. The average magnitude and direction of the shift vectors provide a quantitative proxy for the local Coherence Gradient.
        expected_signals: [Consistent, high-magnitude semantic drift of probes toward the well's core lexicon, High classification confidence of shifted probes as belonging to the paradigm.]
        pitfalls: [Probe concepts may not be truly neutral and can carry their own coherence, The chosen semantic embedding space may not accurately reflect the true cognitive manifold.]
context_windows:
  - module: DOMA-120
    excerpt: |
      A belief with a steep gradient is highly influential, presenting itself as the most logical or satisfying path for nearby thoughts. This is the allure of the song, the pull of the current. A mind, itself a resonant system, does not get "pulled" by an idea in the classical sense. Its trajectory is altered as it navigates the coherence manifold, a process governed by Flow Dynamics (DYNA-001).
  - module: DOMA-120
    excerpt: |
      To navigate the world of ideas is to be a cartographer of these invisible landscapes. A Weaver can map them using the following protocol... Map the Gradient and Flow: Determine how these core beliefs influence adjacent concepts, revealing the "slope" of the well. Analyze how new information interacts with this landscape: Is it immediately channeled into an existing well (entrainment)? Does it create a turbulent eddy between two competing wells (polarization)?
poetic_connections:
  motifs: [gravity, slope, current, riverbed, siren song, path of least resistance]
  evocative_lines:
    - "the allure of the song, the pull of the current."
    - "the currents of a vast and ancient ocean."
  association_matrix:
    - [ "Coherence Well", 0.9 ]
    - [ "Pirouette Lagrangian", 0.8 ]
    - [ "Resonant Depth", 0.7 ]
    - [ "Laminar Flow", 0.6 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Generalized Force (F = -∇V)
      domain: CM
      mapping_kind: conceptual|mathematical
      equation_hint: |
        F_coherence ∝ ∇𝓛_p ≈ -∇V_Γ
      justification: |
        The Coherence Gradient acts as a generalized force in the cognitive state-space, driving a system's trajectory to minimize a potential (V_Γ) and thus maximize a Lagrangian (𝓛_p). This is directly analogous to how a physical force is the negative gradient of a potential energy field, directing a particle toward a lower energy state.
      references: []
      rationale: "The mapping to a generalized force from a potential gradient is a foundational concept in physics via the principle of least action. It provides a robust, mathematically sound, and intuitive framework for understanding cognitive dynamics as a flow on a manifold."
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "The rate of adoption of a new concept within a community is directly proportional to the measured Coherence Gradient of the embedding paradigm."
      domain: phenomenology
      falsifier: "Observing a new concept within a field of a high-gradient paradigm achieving rapid, widespread adoption without external forcing, or a concept with a very high gradient failing to capture adjacent ideas."
      status: proposed
      links: [DOMA-120]
naming_notes:
  collisions: [The del (∇) operator is standard for gradients in vector calculus; the subscript 𝓛_p is essential for disambiguation.]
  disambiguation: |
    Distinguish from a simple 'influence score' or 'popularity'. The Coherence Gradient is a vector quantity on a manifold, possessing both magnitude (steepness) and direction (the path of maximal coherence increase). It is a local property of the cognitive landscape, not an intrinsic property of an isolated concept.
crosslinks:
  near_synonyms: [CONCEPTUAL_GRAVITY]
  antonyms: [COHERENCE_PLATEAU]
  prerequisites: [COHERENCE_WELL, PIROUETTE_LAGRANGIAN]
  downstream_effects: [LAMINAR_FLOW, CONCEPTUAL_ENTRAINMENT, DOGMA]
license: CC-BY-SA-4.0
---

# Coherence Gradient

## Canonical (Pirouette)
The Coherence Gradient (∇𝓛_p) is the vector field on the cognitive manifold that represents the local rate and direction of maximum increase of the Pirouette Lagrangian (𝓛_p). As the gradient of the coherence potential, it defines the 'force' of a Coherence Well, directing cognitive flow along geodesics toward regions of greater resonant depth (Kτ_well) and temporal stability. A steep gradient signifies a highly influential paradigm that efficiently entrains nearby thought patterns into laminar flow.

## EFT-First Summary
In the language of classical field theory, the Coherence Gradient is the generalized force driving the dynamics of thought. It is formally analogous to the negative gradient of a potential field (F = -∇V) on the cognitive manifold. A mind's trajectory follows geodesics shaped by this force, seeking to minimize potential and settle into stable, low-energy states defined by Coherence Wells, in direct analogy to a particle moving in a gravitational field.

## Glossary Links
- See also: Coherence Well, Resonant Depth, Pirouette Lagrangian, Laminar Flow