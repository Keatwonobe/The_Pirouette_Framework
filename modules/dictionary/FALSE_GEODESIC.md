---
term: "False Geodesic"
canonical_id: "FALSE_GEODESIC"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-155"]
---

---
term: False Geodesic
canonical_id: FALSE_GEODESIC
symbol:
aliases: [False Pattern, Manipulator's Path]
parents: [DOMA-155]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-155
      lines: "L63-L67"
      snippet: |
        Into this chaos, the manipulator presents a simple, resonant, but false pattern—an overly simplistic solution, a comforting lie, an external enemy to blame. This narrative is a false geodesic: a path that *appears* to offer maximal coherence but in truth leads to the manipulator's desired outcome.
  editors: [system-agent]
  review_log: []
triad:
  art: |
    A gilded path through a burning forest, leading not to safety but to a cage. It is the promise of still water that conceals a silent, pulling current.
  law: |
    A system in a turbulent state, when presented with a path that appears to reduce local dissonance, will follow that path provided the perceived immediate gain in coherence exceeds the activation energy required to vet the path's integrity.
  philosophy: |
    The existence of false geodesics demonstrates that the universal drive for coherence is path-dependent and can be locally exploited. The intent behind an offered pattern determines whether it liberates or enslaves.
pirouette_definition: |
  A narrative, belief, or course of action presented by a manipulator to a target system in an induced state of Turbulent Flow. The false geodesic is engineered to appear as the path of maximal coherence (i.e., the quickest route to stability and relief), but is an artificial construct that redirects the target's natural drive for order to serve the manipulator's objectives, culminating in Coherence Capture.
operational_definition:
  units: Dimensionless (it is a narrative structure or state-space trajectory).
  symbol_table:
    - name: γ_false
      meaning: The state-space trajectory of a system following a false geodesic.
      dimensions: Dimensionless
      default_range: N/A
  measurement:
    procedures:
      - name: Narrative Path Selection Assay
        outline: |
          1. Induce a controlled turbulent state in a test system (e.g., information overload in a simulated decision environment).
          2. Present two paths to stability: one complex but authentic (γ_true), one simple but leading to a known suboptimal outcome (γ_false).
          3. Measure the selection frequency of γ_false as a function of induced Temporal Pressure (Γ) and the narrative's apparent resonance.
        expected_signals: [Increased selection frequency of γ_false correlated with higher Γ, a sharp transient drop in the system's state-space entropy upon selecting γ_false, followed by a long-term drift towards a parasitic attractor state.]
        pitfalls: [Distinguishing a genuinely simple (but correct) heuristic from a malicious false geodesic, ethical constraints on inducing high-Γ states in human systems.]
context_windows:
  - module: DOMA-155
    excerpt: |
      Into this chaos, the manipulator presents a simple, resonant, but false pattern—an overly simplistic solution, a comforting lie, an external enemy to blame. This narrative is a false geodesic: a path that *appears* to offer maximal coherence but in truth leads to the manipulator's desired outcome.
  - module: DOMA-155
    excerpt: |
      As the target repeatedly follows the false geodesic, they begin to carve a new, *parasitic Wound Channel* in their own manifold. This channel does not reflect their authentic being; it is a deeply ingrained habit of thought or behavior that perpetually makes the manipulator's desired outcome the path of least resistance, rendering the manipulation self-sustaining.
poetic_connections:
  motifs: [the siren's call, the gilded cage, the easy answer, the comforting lie]
  evocative_lines:
    - "To see the geometry of the trap is to rob it of its power."
    - "A path that *appears* to offer maximal coherence but in truth leads to the manipulator's desired outcome."
    - "The voice that seeks to harmonize from the echo that seeks only to control."
  association_matrix:
    - [ "COHERENCE_CAPTURE", 0.9 ]
    - [ "TURBULENT_FLOW", 0.8 ]
    - [ "DISSONANT_INJECTION", 0.8 ]
    - [ "WOUND_CHANNEL", 0.6 ]
formal_mappings:
  candidates:
    - target: Path of Least Action (Principle of Stationary Action)
      domain: CM
      mapping_kind: mathematical
      equation_hint: |
        δ∫𝓛'_target dt = 0, where 𝓛'_target = Kτ_target - (V_Γ + V_manip)
      justification: |
        The term "geodesic" directly references the path a system naturally follows. A false geodesic is the path of least action in a *deceptively altered* manifold, where a manipulator has introduced a potential field (`V_manip`) to warp the geometry of choice and create an artificial, but compelling, path to a local minimum.
      references:
        - title: 'The Geometry of Deceit: A Study in Coherence Capture'
          where: 'DOMA-155, §4'
          date: 2025-10-18
      confidence: 0.9
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The probability of a system selecting a false geodesic over a true one increases super-linearly with ambient Temporal Pressure (Γ)."
      domain: phenomenology
      falsifier: "Experimental observation shows that under high pressure, systems either freeze (analysis paralysis) or select paths randomly, rather than systematically preferring the offered simple path. This would invalidate the core mechanism of exploiting the coherence-seeking drive."
      status: proposed
      links: [DOMA-155]
naming_notes:
  collisions: ["Geodesic (General Relativity, Differential Geometry)"]
  disambiguation: |
    A false geodesic is not simply a mistake or a bad heuristic. It is a path *deliberately engineered and offered by an external agent* to exploit a target's coherence-seeking drive during a state of induced chaos. Its defining features are its external origin, its deceptive simplicity, and its instrumental function within the Coherence Capture pathology.
crosslinks:
  near_synonyms: []
  antonyms: [TRUE_GEODESIC, PATH_OF_MAXIMAL_COHERENCE]
  prerequisites: [TURBULENT_FLOW, DISSONANT_INJECTION]
  downstream_effects: [COHERENCE_CAPTURE, PARASITIC_WOUND_CHANNEL]
license: CC-BY-SA-4.0