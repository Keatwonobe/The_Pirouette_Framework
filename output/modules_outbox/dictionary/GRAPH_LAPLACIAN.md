---
term: "Graph Laplacian"
canonical_id: "GRAPH_LAPLACIAN"
symbol: "L"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["XAP-002_appendix_addendum_014_016"]
---

---
term: Graph Laplacian
canonical_id: GRAPH_LAPLACIAN
symbol: L
aliases: []
parents: [XAP-002_appendix_addendum_014_016]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: XAP-002_appendix_addendum_014_016
      lines: "XAP-015 Setup"
      snippet: |
        Define graph Laplacian \(L=D-A\) with degree matrix \(D\). Evolution under pure diffusion obeys
        $$\dot S=-L S.$$
  editors: [Automated Ingest Agent]
  review_log: []
triad:
  art: |
    The Laplacian is the invisible web of tensions in a network, smoothing away imbalances. It is the ghost of the system's structure, channeling entropy from where it is abundant to where it is scarce. Its action is a quiet, persistent pull towards equilibrium and harmony.
  law: |
    The rate of change of the system's entropy vector `S` under pure diffusion is given by `Ṡ = -L S`. This dynamic guarantees that local Dark-Residue `Dⱼ` is non-increasing and, consequently, that global Coherence `C` is non-decreasing over time.
  philosophy: |
    The Laplacian embodies the principle of systemic health through local exchange. It formalizes how individual, "altruistic" diffusions, driven by local gradients, necessarily produce a global dividend of increased Coherence. It is the mathematical engine translating local connectivity into system-wide order.
pirouette_definition: |
  The Graph Laplacian `L` is a matrix operator defined as `L = D - A`, where `D` is the diagonal degree matrix and `A` is the adjacency matrix of a system graph `G(V, E)`. It governs the pure diffusion of entropy `S` across the system according to the evolution equation `Ṡ = -L S`. Its application to the entropy state vector guarantees a non-increasing total Dark-Residue `D` and therefore a non-decreasing global Coherence `C`.
operational_definition:
  units: Dimensionless matrix elements. The eigenvalues of L have dimensions of inverse time (`T⁻¹`).
  symbol_table:
    - name: L
      meaning: Graph Laplacian matrix
      dimensions: dimensionless
      default_range: contextual
    - name: S
      meaning: Vector of node entropies
      dimensions: Entropy (e.g., J/K)
      default_range: "[0, ∞)"
    - name: A
      meaning: Adjacency matrix of the system graph
      dimensions: dimensionless
      default_range: "{0, 1} for unweighted graphs"
    - name: D
      meaning: Diagonal degree matrix
      dimensions: dimensionless
      default_range: "non-negative integers"
  measurement:
    procedures:
      - name: Inference from Network Topology
        outline: |
          1. Model the system as a graph `G(V, E)`, identifying all nodes and their connections.
          2. Construct the adjacency matrix `A`, where `Aᵢⱼ = 1` if nodes `i` and `j` are connected (and 0 otherwise).
          3. Construct the degree matrix `D`, a diagonal matrix where `Dᵢᵢ` is the number of connections for node `i`.
          4. Compute the Laplacian matrix as `L = D - A`.
        expected_signals: [Time-series of node entropies `S(t)` showing diffusion, Time-series of global Coherence `C(t)` showing a non-decreasing trend.]
        pitfalls: [Incorrectly mapping the system's true connectivity to the graph model, Assuming pure diffusion when external or non-linear effects are significant.]
context_windows:
  - module: XAP-002_appendix_addendum_014_016
    excerpt: |
      Let \(G(V,E)\) be a connected graph with adjacency \(A=[a_{jk}]\). Node entropies form vector \(S\).
      ...
      Define graph Laplacian \(L=D-A\) with degree matrix \(D\). Evolution under pure diffusion obeys
      $$\dot S=-L S.$$
  - module: XAP-002_appendix_addendum_014_016
    excerpt: |
      For any node j
      $$\dot D_j=-\sum_k a_{jk}(\dot S_j-\dot S_k) = -\sum_k a_{jk}\bigl((LS)_j-(LS)_k\bigr) ≤ 0,$$
      with equality only at equilibrium \(S_i=S_j\;∀i,j\).
      ...
      Thus any diffusion step that lowers local \(D_j\) *necessarily* raises global coherence \(C\).
poetic_connections:
  motifs: [diffusion, smoothing, equilibrium, altruism, coherence]
  evocative_lines:
    - "Altruism—defined as policies accelerating diffusion—maximises the system‑wide \(\dot C\)."
    - "any diffusion step that lowers local \(D_j\) *necessarily* raises global coherence \(C\)."
  association_matrix:
    - [ "COHERENCE", 0.9 ]
    - [ "DARK_RESIDUE", 0.9 ]
    - [ "ENTROPY", 0.8 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Discrete Laplace Operator
      rationale: |
        The Pirouette definition (`L = D - A`) and its role in the diffusion equation (`Ṡ = -L S`) are mathematically identical to the standard definition of the graph Laplacian in spectral graph theory and its role as the generator of the heat flow/diffusion process on a discrete graph. It is the direct analog of the continuous Laplace operator `∇²`.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "In any isolated system governed solely by Pirouette diffusion, global Coherence C is a monotonically non-decreasing function of time."
      domain: phenomenology
      falsifier: "An observation of a closed system where interaction between nodes leads to a sustained decrease in global Coherence C, without external entropy injection or non-diffusive dynamics."
      status: supported
      links: [XAP-002_appendix_addendum_014_016]
naming_notes:
  collisions: [L is the standard symbol for the Lagrangian in classical mechanics.]
  disambiguation: |
    In the Pirouette Framework, `L` as a matrix operator consistently refers to the Graph Laplacian. The Lagrangian, a scalar function of generalized coordinates, is denoted by the calligraphic symbol `ℒ`. The context of operation distinguishes them: the Laplacian acts on a state vector (`L S`), whereas the Lagrangian is evaluated on state variables (`ℒ(q, q̇)`).
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [ADJACENCY_MATRIX, COHERENCE, DARK_RESIDUE]
  downstream_effects: [COHERENCE_DIVIDEND]
license: CC-BY-SA-4.0
---