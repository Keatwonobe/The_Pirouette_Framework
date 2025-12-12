---
term: "Chirality"
canonical_id: "CHIRALITY"
symbol: "χ"
aliases: [Handedness]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-196"]
---

---
term: Chirality
canonical_id: CHIRALITY
symbol: χ
aliases: [Handedness]
parents: [DOMA-196]
children: [INST-PHYS-002]
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-196
      snippet: |
        Chirality Index (χ): A measure of the system's net "handedness." A value of χ=0 implies perfect symmetry and zero thrust. Maximum thrust is achieved as χ approaches ±1, creating the steepest possible coherence gradient.
  editors: [local_agent]
  review_log: []
triad:
  art: |
    The subtle, intentional twist in the weave that turns a flat tapestry into a spiral staircase. It is the asymmetry that convinces a placid lake to become a flowing river.
  law: |
    Propulsive thrust along a self-generated geodesic is proportional to the non-zero Chirality Index (χ) of the system's coherence modulator; a perfectly symmetric (χ=0) system cannot produce net thrust.
  philosophy: |
    Chirality is the principle that directed change requires broken symmetry. It elevates a system from mere oscillation to purposeful motion, teaching that progress is not a matter of force, but of introducing a decisive, elegant imbalance.
pirouette_definition: |
  The intrinsic, asymmetric property of a dynamic system that breaks rotational symmetry in its modulation of the local coherence manifold. This engineered handedness imparts a net topological "twist" to the system's Wound Channel, inducing a directed, helical gradient (∇V_Γ) that serves as a propulsive slope. It is quantified by the dimensionless Chirality Index (χ), which ranges from -1 (maximum left-handed twist) to +1 (maximum right-handed twist), with 0 representing a perfectly symmetric, non-propulsive state.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: χ
      meaning: Chirality Index
      dimensions: dimensionless
      default_range: [-1, 1]
  measurement:
    procedures:
      - name: Inferred Chirality via Thrust-Vector Analysis
        outline: |
          Chirality is not measured directly but is inferred from its propulsive effect. A Vorticycle drive is operated in a controlled environment with minimal ambient gradients. The net thrust vector (F) is measured while key operating parameters (rotational frequency ω_rot, phase coherence Δφ, power consumption P) are monitored. The Chirality Index χ is then calculated as the normalized thrust component attributable to the asymmetric phasing of the modulator elements, after accounting for system inefficiencies and resonant effects.
        expected_signals: [A stable, non-zero thrust vector, Power consumption correlated with |F|]
        pitfalls: [Failing to isolate the system from ambient manifold gradients, which can produce confounding thrust. Poor phase coherence (low Δφ) can dissipate energy as temporal turbulence, masking the chiral effect and leading to an underestimate of χ.]
context_windows:
  - module: DOMA-196
    excerpt: |
      The critical innovation is **chirality** (handedness). The chiral phasing of the elements ensures this modulation is asymmetric. On one side of the device, constructive interference creates a region of slightly higher temporal pressure (a "pressure crest"), while on the other, destructive interference creates a region of lower pressure (a "pressure trough"). This establishes a stable gradient ∇V_Γ across the device, creating the slope it will descend.
  - module: DOMA-196
    excerpt: |
      **Chirality (Handedness):** The specific timing and geometry of the rotations impart a net "twist" to the Wound Channel. This topological bias breaks the symmetry of the surrounding manifold, creating a directed gradient. A right-handed weave creates a "forward" slope; a left-handed weave creates a "reverse" one.
poetic_connections:
  motifs: [broken symmetry, the screw's thread, spiral staircase, the subtle twist]
  evocative_lines:
    - "This topological bias breaks the symmetry of the surrounding manifold..."
    - "It is analogous to a screw biting into wood, with the profound difference that the screw is simultaneously creating the wood grain it grips."
  association_matrix:
    - [ "ASYMMETRIC_COHERENCE_GRADIENT", 0.9 ]
    - [ "GEODESIC_PROPULSION", 0.8 ]
    - [ "WOUND_CHANNEL", 0.7 ]
    - [ "SYMMETRY", -1.0 ]
formal_mappings:
  candidates:
    - target: Topological Charge / Winding Number
      domain: Math
      mapping_kind: conceptual
      equation_hint: |
        F ∝ χ ≈ (1/2π) ∮ ∇θ ⋅ dl
      justification: |
        The Pirouette Chirality Index χ behaves as a macroscopic, engineered topological charge. A non-zero χ signifies a non-trivial winding in the phase space of the coherence modulators, which imprints a helical topology onto the Wound Channel. Like a winding number, it is a quantized (in principle) and conserved property of the propulsive process that determines the direction of flow.
      references:
        - title: The Geometry of Physics
          where: T. Frankel, Chapter on Differential Forms and Topology
          date: 2011-11-08
      confidence: 0.5
    - target: Parity Violation
      domain: SM
      mapping_kind: conceptual
      justification: |
        Chirality in Pirouette is a direct analogue to parity violation. A system with χ≠0 is one where the mirror-image process (achieved by reversing the phase relationships) is not identical to the original, resulting in thrust in the opposite direction rather than no thrust. It is an engineered breaking of a fundamental P-symmetry in the system's interaction with the coherence manifold.
      references: []
      confidence: 0.4
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "A system with a Chirality Index of zero (χ=0) cannot produce net geodesic propulsion."
      domain: experiment
      falsifier: "The repeatable observation of sustained, non-zero propulsive thrust from a perfectly symmetric (achiral) coherence modulator operating within a uniform, static ambient coherence manifold."
      status: supported
      links: [DOMA-196]
    - statement: "The direction of the propulsive thrust vector is determined by the sign of the Chirality Index (χ)."
      domain: experiment
      falsifier: "Observing a system generate 'forward' thrust with χ < 0, or observing a reversal of thrust direction without a corresponding change in the sign of χ."
      status: proposed
      links: [DOMA-196]
naming_notes:
  collisions: [The symbol χ is commonly used for magnetic susceptibility in electromagnetism and the Euler characteristic in topology.]
  disambiguation: |
    In the Pirouette Framework, Chirality (χ) is always a dimensionless measure of the *engineered, dynamic asymmetry* of a coherence-modulating system. It is not an intrinsic material property like magnetic susceptibility, nor is it a static topological invariant of a manifold itself. It is the measure of a system's ability to "twist" spacetime.
crosslinks:
  near_synonyms: [HANDEDNESS]
  antonyms: [SYMMETRY, ACHIRALITY]
  prerequisites: [COHERENCE_MANIFOLD, WOUND_CHANNEL, PIROUETTE_LAGRANGIAN]
  downstream_effects: [GEODESIC_PROPULSION, ASYMMETRIC_COHERENCE_GRADIENT]
license: CC-BY-SA-4.0