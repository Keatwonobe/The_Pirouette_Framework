---
term: "Altruism"
canonical_id: "ALTRUISM"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["XAP-002_appendix_addendum_014_016"]
---

---
term: Altruism
canonical_id: ALTRUISM
symbol: 
aliases: []
parents: [PPS-019, XAP-002_appendix_addendum_014_016]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: XAP-002_appendix_addendum_014_016
      snippet: |
        Altruism—defined as policies accelerating diffusion—maximises the system‑wide Ċ.
  editors: [System Agent]
  review_log: []
triad:
  art: |
    To empty the self is to fill the world. A local sacrifice, a shared breath that weaves the whole into a more coherent tapestry. The fastest path to universal harmony is paved with local generosity.
  law: |
    A policy is classified as Altruistic if and only if it increases the rate of entropy diffusion from regions of high local concentration, thereby maximizing the rate of growth of Global Coherence (Ċ ≥ 0).
  philosophy: |
    Altruism is not a moral choice but a thermodynamic imperative for systems seeking maximal coherence. It recasts self-interest as system-interest, demonstrating that the most effective way for a part to thrive is to ensure the whole system processes energy and information efficiently.
pirouette_definition: |
  A classification for policies or actions that accelerate entropy diffusion across a system. By reducing local entropy gradients and thus minimizing total Dark-Residue (D), Altruistic policies necessarily maximize the rate of increase of Global Coherence (Ċ ≥ 0).
operational_definition:
  units: Dimensionless (policy classification)
  symbol_table:
    - name: C
      meaning: Global Coherence
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: Dⱼ
      meaning: Dark-Residue of node j
      dimensions: "Entropy (e.g., J/K)"
      default_range: "[0, ∞)"
    - name: S
      meaning: Entropy
      dimensions: "Entropy (e.g., J/K)"
      default_range: contextual
    - name: L
      meaning: Graph Laplacian
      dimensions: dimensionless
      default_range: operator
  measurement:
    procedures:
      - name: Coherence Trajectory Analysis
        outline: |
          1. Model the system as a graph G(V,E) with an entropy value Sⱼ at each node.
          2. Apply the candidate policy as a transformation on the system state over a time interval Δt.
          3. Compute the time-series of Global Coherence C(t) using the `compute_residue` function specified in XAP-016.
          4. A policy is Altruistic if the measured Ċ is positive and greater than the baseline diffusion rate.
        expected_signals: [Monotonically increasing C(t), Decreasing total Dark-Residue D(t)]
        pitfalls: [Incorrect graph topology, Confounding external entropy sources, Insufficient simulation time to filter high-frequency noise]
context_windows:
  - module: XAP-002_appendix_addendum_014_016
    excerpt: |
      Thus any diffusion step that lowers local Dⱼ *necessarily* raises global coherence C. Altruism—defined as policies accelerating diffusion—maximises the system‑wide Ċ.
  - module: XAP-002_appendix_addendum_014_016
    excerpt: |
      Total Dark‑Residue D = ∑ⱼ Dⱼ. Since each term is non‑positive, Ḋ ≤ 0. Because C = 1 − D/Sᵢₙ, we obtain Ċ = −Ḋ/Sᵢₙ ≥ 0.
poetic_connections:
  motifs: [diffusion, generosity, coherence, equilibrium, gradient descent]
  evocative_lines:
    - "Altruism—defined as policies accelerating diffusion—maximises the system‑wide Ċ."
    - "...any diffusion step that lowers local Dⱼ *necessarily* raises global coherence C."
  association_matrix:
    - [ "GLOBAL_COHERENCE", 0.9 ]
    - [ "DARK_RESIDUE", 0.8 ]
    - [ "RESIDUE_PRINCIPLE", 0.5 ]
formal_mappings:
  candidates:
    - target: Heat equation on graphs
      domain: Math
      mapping_kind: mathematical
      equation_hint: |
        Ṡ = −L S  ↔  ∂u/∂t = α∇²u
      justification: |
        Altruism is defined as the acceleration of the process described by the graph heat equation, Ṡ = -LS, where L is the graph Laplacian. This equation is the discrete analogue of the classical heat/diffusion equation. Altruistic actions increase the effective thermal conductivity between nodes, speeding the system's approach to equilibrium (maximum Coherence).
      references: []
      confidence: 0.95
  adopted:
    - target: Heat equation on graphs
      rationale: The mapping is a direct mathematical analogy central to the concept's definition in XAP-015.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "Any policy that accelerates entropy diffusion on a connected graph will result in a non-negative rate of change for Global Coherence (Ċ ≥ 0)."
      domain: theory
      falsifier: "Observation of a system where a policy demonstrably accelerates diffusion (e.g., increases edge weights in the graph Laplacian) yet leads to a sustained decrease in Global Coherence, C, without external entropy injection."
      status: supported
      links: [XAP-002_appendix_addendum_014_016]
naming_notes:
  collisions: [Biological altruism, Ethical altruism]
  disambiguation: |
    In the Pirouette Framework, Altruism is a strictly operational term describing policies that optimize system-wide entropy flow for Coherence growth. It should not be confused with its biological or ethical counterparts, which involve intent, kinship, or reciprocal exchange. The framework's definition is purely mechanistic.
crosslinks:
  near_synonyms: []
  antonyms: [ENTROPIC_HOARDING]
  prerequisites: [GLOBAL_COHERENCE, DARK_RESIDUE]
  downstream_effects: [GLOBAL_COHERENCE]
license: CC-BY-SA-4.0
---