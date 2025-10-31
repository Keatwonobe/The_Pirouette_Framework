---
term: "Attractor"
canonical_id: "ATTRACTOR"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-139"]
---

---
term: Attractor
canonical_id: ATTRACTOR
symbol: S*
aliases: [Coherence Peak, Stable State, Metastable State]
parents: [DOMA-139]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-139
      snippet: |
        ...defining stable states ('attractors') as peaks of maximal coherence, not valleys of minimal energy.
  editors: [Weaver-Alpha]
  review_log: []
triad:
  art: |
    An attractor is a mountain peak of grace; a state where a system's internal song resonates most clearly and efficiently against the noise of the world.
  law: |
    An attractor is a state S* where the gradient of the Pirouette Lagrangian vanishes (∇𝓛_p(S*) = 0) and the local curvature is negative definite, corresponding to a local maximum on the Coherence Landscape.
  philosophy: |
    Attractors represent the telos of a system not as a descent into inert rest (minimal energy), but as an ascent toward maximal expression, coherence, and stability. They are the goals of a system's drive to become.
pirouette_definition: |
  An attractor is a stable or metastable state of a system, corresponding to a local maximum (a peak) on its Coherence Landscape. It is a configuration S* at which the Pirouette Lagrangian `𝓛_p` is maximized relative to its immediate neighborhood, representing a point of optimal balance between internal harmony (Temporal Coherence, `K_τ`) and imposed pressures (Temporal Pressure, `V_Γ`). Systems naturally evolve towards attractors by ascending the gradient of the landscape (`∇𝓛_p`).
operational_definition:
  units: The state `S` has units specific to the system. The condition of being an attractor is a dimensionless property of that state.
  symbol_table:
    - name: S*
      meaning: An attractor state; a specific vector in the system's state space.
      dimensions: Contextual
      default_range: Contextual
    - name: 𝓛_p
      meaning: The Pirouette Lagrangian, whose value defines the Coherence Landscape elevation.
      dimensions: dimensionless (Coherence)
      default_range: "(-∞, +∞)"
    - name: ∇𝓛_p
      meaning: The gradient of the Coherence Landscape; the Coherence-Seeking Force.
      dimensions: Coherence / State Space Unit
      default_range: Contextual
  measurement:
    procedures:
      - name: Coherence Peak Identification
        outline: |
          1. Define the system's state space `S`.
          2. For each state, calculate Temporal Coherence `K_τ(S)` and Temporal Pressure `V_Γ(S)`.
          3. Construct the Coherence Landscape scalar field `𝓛_p(S) = K_τ(S) - V_Γ(S)`.
          4. Numerically find points S* where `∇𝓛_p(S) = 0` and the Hessian matrix is negative-definite (i.e., local maxima).
        expected_signals: [A local maximum in the scalar field of `𝓛_p`, A zero-crossing in the gradient vector field `∇𝓛_p`]
        pitfalls: [Insufficient state-space resolution may miss narrow attractors, Numerical methods may converge on saddle points instead of true maxima]
context_windows:
  - module: DOMA-139
    excerpt: |
      The New Law (Coherence Maximization): A system seeks the highest point in its Coherence Landscape, defined by the Pirouette Lagrangian `𝓛_p`. The "force" is one of ascent toward greater expression: `F_p ∝ ∇𝓛_p`. Attractors are peaks.
  - module: DOMA-139
    excerpt: |
      Identify Attractors (Peaks): Locate the local maxima of `𝓛_p(S)`. These peaks are the system's stable or metastable states—its points of highest efficiency and most elegant resonance.
poetic_connections:
  motifs: [peak, ascent, resonance, stability, grace, harmony, island_of_stability]
  evocative_lines:
    - "This is not a map of where a thing will die, but a map of where it most truly learns to live."
    - "The Ascent to Grace."
  association_matrix:
    - [ "COHERENCE_LANDSCAPE", 1.0 ]
    - [ "PIROUETTE_LAGRANGIAN", 0.9 ]
    - [ "STABILITY", 0.8 ]
    - [ "POTENTIAL_WELL", -0.9 ]
formal_mappings:
  candidates:
    - target: Stable fixed point / Stable equilibrium
      domain: Dynamical Systems|CM
      mapping_kind: conceptual
      equation_hint: |
        Compare F_p ∝ +∇𝓛_p with F = -∇V
      justification: |
        An attractor represents a state towards which a system evolves and in which it tends to remain, a direct parallel to stable equilibria in classical mechanics and dynamical systems. The crucial difference is that a Pirouette Attractor is a point of *maximal* coherence (`𝓛_p`), whereas a classical attractor is a point of *minimal* potential (`V`). The concept is analogous, but the optimization direction is inverted.
      references:
        - title: "Nonlinear Dynamics and Chaos"
          where: Strogatz, Chapter 2: Fixed Points and Stability
          date: 2014-01-01
      confidence: 0.8
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "A system perturbed from an attractor state S* will spontaneously evolve back towards S* along paths approximating the gradient `∇𝓛_p`."
      domain: phenomenology
      falsifier: "Observation of a system consistently evolving away from a computationally-identified coherence peak towards a region of lower `𝓛_p` without external work being done on the system."
      status: proposed
      links: [DOMA-139, CORE-006]
naming_notes:
  collisions: []
  disambiguation: |
    The Pirouette Attractor is a **peak** of maximal coherence on the Coherence Landscape. This is in direct contrast to the classical mechanics concept of an attractor as a **valley** or minimum in a potential energy landscape. Do not confuse maximizing coherence with minimizing energy.
crosslinks:
  near_synonyms: [COHERENCE_PEAK]
  antonyms: [REPELLER, SADDLE_POINT]
  prerequisites: [COHERENCE_LANDSCAPE, PIROUETTE_LAGRANGIAN]
  downstream_effects: [STABILITY, SYSTEM_EVOLUTION]
license: CC-BY-SA-4.0
---