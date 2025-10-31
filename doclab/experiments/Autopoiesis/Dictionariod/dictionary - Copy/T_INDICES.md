---
term: "T_indices"
canonical_id: "T_INDICES"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["COSMO-004"]
---

---
term: T_indices
canonical_id: T_INDICES
symbol: T_i
aliases: [T-index, topological index]
parents: [COSMO-004]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: COSMO-004
      lines: "C. Freeze Manifest Template"
      snippet: |
        T_indices:
          allowed: [−2, −1, 0, 1, 2]
          chosen_defaults: {halos: 1}
  editors: [Agent: Self-Authored]
  review_log: []
triad:
  art: |
    The universe is cast from a single mold, yet each star and halo is struck from a unique die. T-indices are the integers stamped upon these cosmic coins, distinguishing one realization from its siblings born of the same universal law.
  law: |
    For a given set of universal parameters (U) defined in a Freeze Manifest, a T-index is a realization-specific integer selected from a finite, pre-approved set (`allowed`) that determines the solution branch for a non-linear structure (e.g., halo profile). A change in a T-index, with all U-parameters held fixed, must produce a measurably different structural solution (e.g., halo concentration, core density).
  philosophy: |
    T-indices separate the universal from the particular. They embody the principle that a single fundamental theory (defined by U-parameters) can admit multiple, discrete, stable solutions for complex objects. This allows the Framework to model cosmic variance and structural diversity without altering the underlying cosmological laws, assigning contingency to specific integer choices within a frozen realization.
pirouette_definition: |
  A set of non-universal, realization-specific integer parameters, denoted T_i, defined within a Freeze Manifest. T_indices are selected from a pre-defined `allowed` list and assigned to specific non-linear structures (e.g., halos, clusters). They function as discrete selectors for different stable solution branches or topological states that can arise from the same universal theory (specified by U_parameters). They are distinct from continuous initial conditions or environmental variables.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: T_i
      meaning: T-index for a specific object `i`
      dimensions: dimensionless
      default_range: '{-2, -1, 0, 1, 2} per COSMO-004'
  measurement:
    procedures:
      - name: Structural Solution Classification
        outline: |
          1. Fix all U-parameters from a Freeze Manifest.
          2. For a target object class (e.g., halos of mass M), numerically solve the governing equations (e.g., `halo_config.yaml` from COSMO-004).
          3. Systematically vary boundary conditions or seeds to find all distinct, stable final profiles.
          4. Assign a unique integer T_i to each stable solution branch, creating a reference library.
          5. Classify an observed/simulated object's T_i by comparing its measured profile to the pre-computed solution library.
        expected_signals: [Discrete jumps in halo properties (e.g., core density, concentration) as a function of T_i, distinct lensing profiles for objects with different T_i but identical mass.]
        pitfalls: [Mistaking continuous environmental variation for a discrete T_i change, numerical solver failing to converge to all stable solutions, leading to an incomplete `allowed` list.]
context_windows:
  - module: COSMO-004
    excerpt: |
      The Freeze Manifest separates universal constants from realization-specific choices. ... `T_indices: allowed: [−2, −1, 0, 1, 2], chosen_defaults: {halos: 1}`. This structure freezes the fundamental physics (`U_parameters`) while allowing for topological variation in the resulting structures.
  - module: COSMO-004
    excerpt: |
      The merge solver configuration specifies the properties of the interacting clusters, including their assigned T-index. `clusters: - mass_Msun: 1.2e15; T_index: 1; gas_fraction: 0.12 ...`. This ensures that the merger dynamics are computed for the correct structural solution branch as specified by the parent Freeze Manifest.
poetic_connections:
  motifs: [discreteness, contingency, realization, topology, identity]
  evocative_lines:
    - "No continuous mass exponents; topology is discrete."
    - "One‑shot global scale set; all U,T frozen thereafter."
  association_matrix:
    - [ "FREEZE_MANIFEST", 0.9 ]
    - [ "U_PARAMETERS", 0.7 ]
    - [ "HALO_SOLUTION", 0.8 ]
formal_mappings:
  candidates:
    - target: "Excited state index (n)"
      domain: QM
      mapping_kind: conceptual
      equation_hint:
      justification: |
        The T-index distinguishes between different stable solutions for a bound system (the halo), analogous to how a principal quantum number `n` distinguishes between different stable energy eigenstates of an atom. The ground state could be T_i=0, with other integers representing distinct 'excited' structural configurations.
      references: []
      confidence: 0.5
  adopted:
    - target: "Topological quantum number (e.g., winding number)"
      domain: QFT|Math
      mapping_kind: conceptual
      equation_hint:
      justification: |
        Like a topological quantum number, a T-index is a discrete integer that classifies solutions into distinct families that cannot be continuously deformed into one another. While the underlying field theory is classical, the resulting stable halo solutions exhibit a quantized, topological-like stability. The explicit mention of "discrete topology" in COSMO-004 supports this mapping.
      references: []
      confidence: 0.7
constraints_and_falsifiers:
  claims:
    - statement: "For a fixed set of U-parameters and halo mass, solutions corresponding to different T-indices are physically distinct and stable over cosmological timescales."
      domain: phenomenology
      falsifier: "Numerical simulations showing that halo solutions with different initial T-indices evolve to the same final state, or that intermediate/fractional T-index states are stable. This would imply the discreteness is a numerical artifact, not a physical feature."
      status: proposed
      links: [COSMO-004]
naming_notes:
  collisions: [The symbol T is commonly used for Temperature or the stress-energy Tensor (T_μν). The subscript 'i' (T_i) and its strict context within a Freeze Manifest are crucial for disambiguation.]
  disambiguation: |
    T_indices are not thermodynamic temperatures. They are parameters *of* a realization, not a measured property *within* it. They are always integers from a small, specified set. They are conceptually paired with U_parameters: 'U' for Universal, 'T' for Topological/Type-specific.
crosslinks:
  near_synonyms: []
  antonyms: [U_PARAMETERS]
  prerequisites: [FREEZE_MANIFEST]
  downstream_effects: [HALO_SOLUTION, MERGER_DYNAMICS]
license: CC-BY-SA-4.0