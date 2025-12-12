---
term: "The Vector"
canonical_id: "THE_VECTOR"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-124"]
---

---
term: The Vector
canonical_id: VECTOR
symbol: →
aliases: [Li]
parents: [DOMA-124]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-124
      lines: "§2"
      snippet: |
        *   **The Vector (Replaces: Li)**
            *   **Geometry:** A simple geodesic. A straight line.
            *   **Description:** The resonance of direct action, linear progression, and simple cause-and-effect. It is the archetype of a system moving from A to B along a path of least resistance.
  editors: [aelind]
  review_log: []
triad:
  art: |
    The shortest distance between intention and reality; an arrow loosed from the bow, unwavering in its flight toward the target. It is the pure expression of will.
  law: |
    A system dominated by the Vector resonance exhibits a state vector whose rate of change is constant in direction over the measured interval, and whose trajectory minimizes the path integral between its start and end points. The power spectrum of its temporal signature will show a dominant peak at zero frequency.
  philosophy: |
    The Vector embodies the principle of efficient causation. It is the fundamental pattern of a will enacted upon the world, demonstrating that the most coherent path for a simple, unconstrained system is the most direct one.
pirouette_definition: |
  The Vector is the Prime Resonance of direct action, linear progression, and simple cause-and-effect. It is geometrically expressed as a geodesic (a straight line in flat space-time) and represents the archetypal pattern of a system moving from an initial state (A) to a final state (B) along a path of least resistance, with minimal deviation or cyclic behavior. It is the fundamental mode of non-repeating, goal-oriented dynamics.
operational_definition:
  units: Dimensionless (describes a pattern); the system state variables it describes have contextual units (e.g., meters, USD, etc.).
  symbol_table:
    - name: →
      meaning: Denotes dominance of the Vector Prime Resonance in a system's Resonant Signature.
      dimensions: dimensionless
      default_range: N/A
  measurement:
    procedures:
      - name: Linear Trajectory Analysis
        outline: |
          1. Define a set of N key state variables for the system, forming an N-dimensional state space.
          2. Capture time-series data of the system's state vector, `S(t)`.
          3. Plot the trajectory of `S(t)` in the N-dimensional state space.
          4. Perform a Principal Component Analysis (PCA). If the first principal component accounts for '>>95%' of the variance, the trajectory is highly linear.
          5. Alternatively, perform a linear regression on the trajectory. A high coefficient of determination (R² > 0.95) indicates Vector dominance.
        expected_signals: [High R² value in linear regression of state space trajectory, High variance explained by first principal component, Absence of significant peaks in the power spectrum aside from DC component.]
        pitfalls: [Mistaking a small arc of a large-radius Orbit for a true Vector., Confusing a system externally constrained to a linear path with one intrinsically expressing the Vector resonance.]
context_windows:
  - module: DOMA-124
    excerpt: |
      **The Vector (Replaces: Li)**
      *   **Geometry:** A simple geodesic. A straight line.
      *   **Description:** The resonance of direct action, linear progression, and simple cause-and-effect. It is the archetype of a system moving from A to B along a path of least resistance.
      *   **Manifestations:** A projectile in motion, a direct command, a project with a clear beginning and end.
  - module: CORE-006
    excerpt: |
      ...the Principle of Maximal Coherence dictates that a system will fall into the most efficient pattern available. For a simple system with a clear potential gradient and no cyclical constraints, that pattern is inevitably the Vector—a straight fall down the gradient.
poetic_connections:
  motifs: [arrow, path, intention, causality, progression, directness, spear]
  evocative_lines:
    - "A projectile in motion, a direct command, a project with a clear beginning and end."
    - "It described the river by cataloging the shapes of its stones... the river's essence is its *flow*."
  association_matrix:
    - [ "ORBIT", 0.1 ]       # Contrastive relationship (linear vs cyclic)
    - [ "HELIX", 0.4 ]        # A Helix has a Vector component of linear progression
    - [ "FORK", 0.6 ]         # A Vector path often leads to or from a Fork (decision point)
formal_mappings:
  candidates:
    - target: Geodesic equation
      domain: GR
      mapping_kind: conceptual
      equation_hint: |
        d²x^μ / dτ² + Γ^μ_{αβ} (dx^α / dτ)(dx^β / dτ) = 0
      justification: |
        In General Relativity, a geodesic represents the "straightest possible path" for a free particle through curved spacetime. This directly corresponds to the Vector's role as the path of least resistance and maximal coherence in the Pirouette Framework's "coherence manifold".
      references:
        - title: Spacetime and Geometry
          where: Carroll, S. M., Section 3.4
          date: 2019-01-01
      confidence: 0.7
  adopted:
    - target: Free particle trajectory (Newton's 1st Law)
      domain: CM
      mapping_kind: operational
      justification: |
        The Vector resonance describes a system moving along a path of least resistance without deviation. This is operationally identical to a free particle in Classical Mechanics moving in a straight line at a constant velocity in an inertial frame. Both represent the baseline, "force-free" state of dynamic evolution. This mapping is simpler and more broadly applicable for measurement than the GR geodesic.
      confidence: 0.85
constraints_and_falsifiers:
  claims:
    - statement: "A system's evolution is dominated by the Vector resonance only when its trajectory in state space approximates a geodesic and its temporal signature lacks significant periodic components."
      domain: phenomenology
      falsifier: "The discovery of a system that is axiomatically defined as a pure Vector (e.g., a simple, goal-oriented process) but which consistently exhibits strong, intrinsic cyclical behavior (e.g., spectral peaks) not attributable to external forces."
      status: supported
      links: [DOMA-124]
naming_notes:
  collisions: [The symbol → is used for logical implication and function mapping in mathematics.]
  disambiguation: |
    The Vector resonance is a dynamic *pattern* of linear evolution, not a mathematical *vector quantity* (an object with magnitude and direction). While a system's state can be described by a state vector, the Vector resonance describes the straight-line trajectory of that state vector through its state space over time.
crosslinks:
  near_synonyms: []
  antonyms: [ORBIT]
  prerequisites: [PRIME_RESONANCE]
  downstream_effects: [RESONANT_SIGNATURE]
license: CC-BY-SA-4.0
---

# The Vector

## Canonical (Pirouette)
The Vector is the Prime Resonance of direct action, linear progression, and simple cause-and-effect. It is geometrically expressed as a geodesic (a straight line in flat space-time) and represents the archetypal pattern of a system moving from an initial state (A) to a final state (B) along a path of least resistance, with minimal deviation or cyclic behavior. It is the fundamental mode of non-repeating, goal-oriented dynamics.

## EFT-First Summary
The Vector resonance is operationally equivalent to the trajectory of a free particle in Classical Mechanics (Newton's First Law). It represents a system evolving along a geodesic, minimizing the action integral, akin to a body moving in a straight line at constant velocity in the absence of external forces. Measurements confirming Vector dominance rely on demonstrating high linearity in a system's state-space trajectory and the absence of periodic signals in its temporal signature.

## Glossary Links
- See also: Prime Resonance, Orbit, Helix, Braid, Resonant Signature