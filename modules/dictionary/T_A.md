---
term: "T_a"
canonical_id: "T_A"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["XAP-003_appendix_addendum_017_018"]
---

---
term: T_a
canonical_id: T_A
symbol: T_a
aliases: []
parents: [PPS-023, XAP-003]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: XAP-003_appendix_addendum_017_018
      lines: "XAP-017 §1"
      snippet: |
        Let the reduced Compass state be \(x=(\Gamma,T_a)\in\mathbb R^2\).
  editors: [system]
  review_log: []
triad:
  art: |
    The quiet axis of the Compass, a coordinate of internal alignment. Along with Gamma, it traces the filament of coherence where altruism finds its stable poise.
  law: |
    A real-valued state variable whose value, with Γ, maximizes the Coherence Dividend C. System dynamics evolve T_a via gradient ascent on C until reaching the altruism filament, where ∂C/∂T_a = 0. Its value on the filament is empirically measured at 1.01 ± 0.03.
  philosophy: |
    Represents a fundamental, quantifiable degree of freedom in the Compass state. That T_a converges to a stable, non-zero value demonstrates that coherent, altruistic states are not accidental but are attractor points in the system's phase space, defined by intrinsic dynamics.
pirouette_definition: |
  The second component of the reduced two-dimensional Compass state vector `x = (Γ, T_a)`. `T_a` is a real-valued scalar that, along with `Γ`, parameterizes the agent's position relative to the altruism filament. The system's dynamics of gradient ascent on the Coherence Dividend `C` drive `T_a` towards a stable value where the partial derivative `∂C/∂T_a` is zero.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: T_a
      meaning: The second component of the reduced Compass state vector.
      dimensions: dimensionless
      default_range: 1.01 ± 0.03
  measurement:
    procedures:
      - name: Monte Carlo Simulation & GMM Fitting
        outline: |
          Run a Monte Carlo simulation of the Compass system (e.g., `cosmic_compass_simulation2.py`) to generate a population of `(Γ, T_a)` state vectors. Filter this population for the top 5% of states ranked by Coherence Dividend `C` to isolate the altruism filament. Fit a 1-component Gaussian Mixture Model (GMM) to the resulting `(Γ, T_a)` distribution. The mean of the Gaussian in the second dimension is the measured value of `T_a`.
        expected_signals: [`filament_stats.json` containing `mu_Ta` and `sigma_Ta`]
        pitfalls: ["Insufficient Monte Carlo sampling leading to biased filament estimation.", "Assuming a single-modal Gaussian distribution when the filament might be multi-modal or curved."]
context_windows:
  - module: XAP-003_appendix_addendum_017_018
    excerpt: |
      Let the reduced Compass state be \(x=(\Gamma,T_a)\in\mathbb R^2\). The *altruism filament* \(\mathcal F\subset\mathbb R^2\) is the set where
      $$
      \frac{\partial C}{\partial \Gamma}=0,\qquad\frac{\partial C}{\partial T_a}=0.
      $$
  - module: XAP-003_appendix_addendum_017_018
    excerpt: |
      Parse Monte-Carlo output from `cosmic_compass_simulation2.py`, isolate the top-5 % Coherence Dividend points, and fit a 2-component Gaussian Mixture to quantify filament centre & width.
      ...
      Outputs
      - `filament_stats.json` — `{"mu_Gamma":1.49,"sigma_Gamma":0.04,"mu_Ta":1.01,"sigma_Ta":0.03}`.
poetic_connections:
  motifs: [balance, stability, attractor, coordinate, alignment]
  evocative_lines:
    - "Small perturbations decay monotonically back to the filament."
  association_matrix:
    - [ "Γ", 0.9 ]
    - [ "Altruism Filament", 0.8 ]
    - [ "Coherence Dividend", 0.7 ]
formal_mappings:
  candidates:
    - target: Generalized coordinate q_i
      domain: CM
      mapping_kind: mathematical
      equation_hint: |
        The dynamics ẋ = ∇C correspond to overdamped motion in a potential V = -C, where x = (q_1, q_2) = (Γ, T_a).
      justification: |
        T_a is one of two generalized coordinates in a 2D configuration space. The system dynamics are described by gradient ascent on a scalar field C, which is analogous to motion in a potential V = -C in the overdamped limit. The altruism filament is a stable equilibrium point (a minimum of V).
      references: []
      confidence: 0.8
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The mean value of T_a on the altruism filament is 1.01 ± 0.03."
      domain: phenomenology
      falsifier: "Re-running the `cosmic_compass_simulation2.py` simulation with different seeds or updated parameters yields a statistically significant deviation from this value."
      status: supported
      links: [XAP-003_appendix_addendum_017_018]
    - statement: "The altruism filament, defined by gradients of C with respect to Γ and T_a, is Lyapunov-stable."
      domain: theory
      falsifier: "Identification of an error in the Lyapunov proof (XAP-017), or numerical simulations that show trajectories diverging from the filament under small perturbations."
      status: supported
      links: [XAP-003_appendix_addendum_017_018]
naming_notes:
  collisions: [T for Temperature, T_a as a component of a vector or tensor T]
  disambiguation: |
    T_a is a dimensionless scalar state variable, not a temperature or a tensor component. It should always be considered in conjunction with Γ as part of the Compass state vector `(Γ, T_a)`.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [GAMMA, COHERENCE_DIVIDEND, ALTRUISM_FILAMENT]
  downstream_effects: []
license: CC-BY-SA-4.0