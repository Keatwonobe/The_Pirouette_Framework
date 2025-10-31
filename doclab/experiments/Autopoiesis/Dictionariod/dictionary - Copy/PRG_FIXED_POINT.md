---
term: "PRG Fixed Point"
canonical_id: "PRG_FIXED_POINT"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["CORE-015_the_fractal_at_the_heart_of_time"]
---

---
term: PRG Fixed Point
canonical_id: PRG_FIXED_POINT
symbol: (K*τ, V*Γ)
aliases: [Scale-Invariant State, Laminar Point, Turbulent Point]
parents: [CORE-015]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: CORE-015
      lines: "L63-L67"
      snippet: |
        * **Exponents:** (d_K, d_\Gamma) (canonical scaling), (\lambda_i) (Jacobian eigenvalues at FP).
        * **Phases:** Laminar (stable FP), Turbulent (saddle), Stagnant (beat freeze: (\beta_\tau\approx 0)).
  editors: [Pirouette-Agent]
  review_log: []
triad:
  art: |
    At the heart of the roaring fractal of time, there are points of profound stillness. These are the fixed points, the eyes of the storm, where the laws of the system become simple and sing the same song at every scale. They are the grooves a system settles into, defining its fundamental character as either a placid stream or a chaotic vortex.
  law: |
    A PRG Fixed Point is a state (K*τ, V*Γ) where the scale derivatives of Coherence and Pressure vanish: β_K(K*τ, V*Γ) = 0 and β_Γ(K*τ, V*Γ) = 0. Near this point, system properties exhibit power-law scaling (e.g., Kτ ~ L^d*_K), with universal exponents determined by the Jacobian of the β-functions at the fixed point. The stability of the point dictates the macroscopic phase of the system.
  philosophy: |
    PRG Fixed Points reveal the universal organizing principles of complex systems, independent of their microscopic details. They are attractors in the abstract space of scale dynamics, representing the fundamental "choices" a system can make for its behavior—e.g., to be ordered or chaotic. By identifying these points, we can understand and predict the emergent, large-scale structure of any system from its scale-flow equations.
pirouette_definition: |
  A specific state, denoted (K*τ, V*Γ), in the parameter space of Coherence (Kτ) and Pressure (VΓ) where the Pirouette Renormalization Group (PRG) flow is stationary. This is the condition where the rates of change of Kτ and VΓ with respect to logarithmic scale (s = ln L) are zero, i.e., the PRG β-functions vanish. The stability of the fixed point, determined by the eigenvalues of the PRG Jacobian matrix at that point, defines the macroscopic phase of the system: a stable fixed point corresponds to a *laminar* phase, while an unstable or saddle fixed point corresponds to a *turbulent* phase.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: (K*τ, V*Γ)
      meaning: The coordinates of the fixed point in the Coherence-Pressure phase space.
      dimensions: dimensionless
      default_range: contextual, derived from system data
    - name: β_X
      meaning: The PRG β-function for a variable X, representing its derivative with respect to logarithmic scale s (dX/ds).
      dimensions: dimensionless
      default_range: contextual
    - name: s
      meaning: Logarithmic scale parameter, s = ln L.
      dimensions: dimensionless
      default_range: >0
  measurement:
    procedures:
      - name: PRG Fixed Point Inference
        outline: |
          1. Collect system data across a range of scales (L_0 < ... < L_n).
          2. At each scale L_i, compute the observables: Coherence Kτ(L_i) (via compressibility) and Pressure VΓ(L_i) (via fluctuation amplitude × coupling).
          3. Numerically estimate the β-functions by calculating the finite differences of observables with respect to logarithmic scale: β_X ≈ ΔX/Δ(ln L).
          4. Fit a model (e.g., polynomial) to the estimated (X, β_X) data points to get an analytical form for the β-functions.
          5. Solve the system of equations β_K(Kτ, VΓ) = 0 and β_Γ(Kτ, VΓ) = 0 to find the coordinates (K*τ, V*Γ) of the fixed point(s).
        expected_signals: [time-series data, spatial data (e.g., images, volumes), network activity]
        pitfalls: [Sensitivity to noise in derivative estimation, finite-size effects from limited scale windows, model-dependence of the β-function fit]
context_windows:
  # Short, trimmed context quotes harvested from modules (3–6 sentences each).
  - module: CORE-015
    excerpt: |
      We posit minimal polynomial β’s near fixed points...
      * **Phases:** Laminar (stable FP), Turbulent (saddle), Stagnant (beat freeze: (\beta_\tau\approx 0)).
      **Predictions:**
      (i) Scaling laws: (K_\tau\sim L^{d_K^*}), (V_\Gamma\sim L^{d_\Gamma^*}).
      (ii) Beat dilation: (\tau_p\sim L^{\zeta_\Gamma d_\Gamma^* - \zeta_K d_K^*}.)
  - module: CORE-015
    excerpt: |
      The PRG heads expose cross-scale dynamics as interpretable dashboards. This allows for monitoring how close a system is to a known fixed point, providing insight into its stability and phase. The objective of the Coherence AI can be seen as steering the system's dynamics towards a desirable (e.g., stable, laminar) fixed point.
poetic_connections:
  # Lightweight "word-association graph" and sticky lines.
  motifs: [attractor, phase transition, scale-invariance, eye of the storm, universality, critical point]
  evocative_lines:
    - "the fractal at the heart of time"
    - "baking it into AI objectives yields models that keep their story straight across scales"
  association_matrix:
    # symmetric or directed; weights in [0,1]
    - [ "COHERENCE_K_TAU", 0.9 ]
    - [ "PRESSURE_V_GAMMA", 0.9 ]
    - [ "UNIVERSALITY_CLASS", 0.8 ]
    - [ "WOUND_CHANNEL", 0.5 ]
formal_mappings:
  # Candidate alignments to EFT/SM/CM/GR terms, each with justification and refs.
  candidates:
    []
  adopted:
    - target: Renormalization Group (RG) Fixed Point
      domain: EFT|CM
      mapping_kind: mathematical|conceptual
      equation_hint: |
        d g_i / d(ln L) = β_i({g_j}). At a fixed point g*, β_i(g*) = 0.
      justification: |
        The Pirouette Renormalization Group (PRG) is an explicit generalization of the Wilsonian RG. The PRG variables Kτ and VΓ are analogous to coupling constants (g_i), logarithmic scale (s = ln L) is the flow parameter, and the PRG β-functions describe how these effective "couplings" change with scale. A PRG fixed point corresponds to a scale-invariant effective theory, which in condensed matter physics defines a phase of matter or a critical point.
      references:
        - title: The renormalization group and the ε expansion
          where: Physics Reports, 12(2), 75-199
          date: 1974-06-01
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The stability of a PRG fixed point (laminar vs. turbulent) correctly predicts the macroscopic stability of the corresponding system phase."
      domain: phenomenology
      falsifier: "Discovering a system that is empirically stable and robust, yet its measured PRG parameters correspond to a saddle (turbulent) fixed point, or vice-versa."
      status: proposed
      links: [CORE-015]
    - statement: "Systems near the same type of PRG fixed point belong to the same universality class, exhibiting identical scaling exponents regardless of their microscopic composition."
      domain: theory
      falsifier: "Finding two systems that flow to the same PRG fixed point but exhibit significantly different, non-universal scaling exponents in measurements."
      status: proposed
      links: [CORE-015]
naming_notes:
  collisions: [Fixed point (dynamical systems), Fixed-point theorem (mathematics)]
  disambiguation: |
    A "PRG Fixed Point" is not a fixed point in physical space or time. It is a point in the abstract parameter space of a system's description (Coherence, Pressure) that remains unchanged under a transformation of observation scale (zooming in or out). It describes scale-invariance, not temporal or spatial immobility.
crosslinks:
  near_synonyms: [CRITICAL_POINT, SCALE_INVARIANT_POINT]
  antonyms: [SCALE_DEPENDENT_STATE, TRANSIENT_BEHAVIOR]
  prerequisites: [COHERENCE_K_TAU, PRESSURE_V_GAMMA, PIROUETTE_RENORMALIZATION_GROUP]
  downstream_effects: [UNIVERSALITY_CLASS, PIROUETTE_LAGRANGIAN]
license: CC-BY-SA-4.0
---

# PRG Fixed Point

## Canonical (Pirouette)
A specific state, denoted (K*τ, V*Γ), in the parameter space of Coherence (Kτ) and Pressure (VΓ) where the Pirouette Renormalization Group (PRG) flow is stationary. This is the condition where the rates of change of Kτ and VΓ with respect to logarithmic scale (s = ln L) are zero, i.e., the PRG β-functions vanish. The stability of the fixed point, determined by the eigenvalues of the PRG Jacobian matrix at that point, defines the macroscopic phase of the system: a stable fixed point corresponds to a *laminar* phase, while an unstable or saddle fixed point corresponds to a *turbulent* phase.

## EFT-First Summary
A PRG Fixed Point is the direct analog of a Renormalization Group (RG) Fixed Point in effective field theory and condensed matter physics. It represents a scale-invariant theory where the "coupling constants" of the system (here, Coherence Kτ and Pressure VΓ) cease to change with observation scale. These points define the universal macroscopic phases of a system, such as ordered (laminar) or critical (turbulent), and the scaling behavior of observables near these points is governed by universal exponents.

## Glossary Links
- See also: [COHERENCE_K_TAU](./coherence_k_tau.md), [PRESSURE_V_GAMMA](./pressure_v_gamma.md), [PIROUETTE_RENORMALIZATION_GROUP](./pirouette_renormalization_group.md)