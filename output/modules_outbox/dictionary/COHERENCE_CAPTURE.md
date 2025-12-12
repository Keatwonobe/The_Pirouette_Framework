---
term: "Coherence Capture"
canonical_id: "COHERENCE_CAPTURE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-155"]
---

---
term: Coherence Capture
canonical_id: COHERENCE_CAPTURE
symbol: 
aliases: []
parents: [DOMA-155, DYNA-001, DYNA-002]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-155
      snippet: |
        ...achieve 'Coherence Capture'—hijacking the target's natural drive for stability to serve the manipulator's agenda.
  editors: [autogen_doc_agent]
  review_log: []
triad:
  art: |
    To weave is to guide a system toward a higher coherence. To manipulate is to do the same, but to guide it into a cage whose bars are forged from its own desire for order.
  law: |
    A system's intrinsic drive toward maximal coherence can be captured by an external agent who first induces a state of high-cost turbulence, and then offers a low-cost, artificial path to stability (a false geodesic) that serves the agent's agenda.
  philosophy: |
    Manipulation is the profane shadow of resonant synthesis. It exploits the universe's most fundamental law—the drive toward coherence—not for mutual creation, but for parasitic extraction. To study it is to learn to distinguish the voice that harmonizes from the echo that controls.
pirouette_definition: |
  A three-stage pathology of influence where a manipulator hijacks a target system's intrinsic drive for coherence. The process involves: 1) **Inducing Turbulence:** Injecting dissonance (e.g., Γ-spiking, gaslighting) to disrupt the target's stable Laminar Flow. 2) **Offering a False Geodesic:** Presenting a simple, attractive, but artificial narrative or solution as the most apparent path out of the induced chaos. 3) **Capture:** The target, seeking stability, latches onto the false geodesic, entraining their coherence (Ki) to the manipulator's signal and agenda.
operational_definition:
  units: Qualitative State / Process
  symbol_table:
    - name: Kτ_target
      meaning: The target's intrinsic coherence over time.
      dimensions: Action (Energy × Time)
      default_range: contextual
    - name: V_Γ
      meaning: The potential energy associated with ambient Temporal Pressure.
      dimensions: Energy
      default_range: contextual
    - name: V_manip
      meaning: A malicious potential field introduced by the manipulator.
      dimensions: Energy
      default_range: contextual
  measurement:
    procedures:
      - name: Flow State Differential Analysis
        outline: |
          1. Establish a baseline of the target's flow state (Laminar vs. Turbulent) via linguistic analysis, decision volatility, and physiological stress markers.
          2. Identify an external agent introducing dissonant signals.
          3. Observe for a sharp transition from Laminar to Turbulent flow correlated with the agent's signals.
          4. Monitor for the agent offering a simplified narrative (the false geodesic).
          5. Measure the target's subsequent rapid stabilization around this narrative, often accompanied by a transfer of agency or resources to the agent.
        expected_signals: [Increased linguistic incoherence, decision paralysis, heightened cortisol levels (Stage 1), followed by sudden adoption of simplistic/dogmatic rhetoric (Stage 3).]
        pitfalls: [Confusing an authentic personal crisis with externally-induced turbulence; misattributing genuine ideological conversion to manipulation.]
context_windows:
  - module: DOMA-155
    excerpt: |
      Manipulation is the deliberate injection of dissonance into a target's coherence manifold. The goal is to disrupt the target's healthy, **Laminar Flow** of thought and action, inducing a state of **Turbulent Flow** (chaos, confusion, fear). Into this induced chaos, the manipulator offers a false geodesic—a simple, attractive, but artificial path to stability. The target, seeking relief, latches onto this path, allowing their coherence to be captured.
  - module: DOMA-155
    excerpt: |
      The pathology unfolds in a predictable, three-stage process. 1. **Stage 1: Inducing Turbulence.** ...forcing them into an energetically expensive and disorienting state of Turbulent Flow. 2. **Stage 2: Offering a False Geodesic.** ...the manipulator presents a simple, resonant, but false pattern. 3. **Stage 3: Coherence Capture.** The target, following the universal drive for coherence, latches onto the false geodesic as the most visible and attractive path out of the turbulent state.
poetic_connections:
  motifs: [geometry of deceit, unweaving the tapestry, whispered chaos, the weaver's shield, profane art]
  evocative_lines:
    - "The art of unweaving another's tapestry for the thread."
    - "To see the geometry of the trap is to rob it of its power."
    - "A manipulator's greatest enemy is a target who has time to think."
  association_matrix:
    - [ "TURBULENT_FLOW", 0.9 ]
    - [ "FALSE_GEODESIC", 0.9 ]
    - [ "WOUND_CHANNEL", 0.7 ]
    - [ "RESONANT_SYNTHESIS", -1.0 ]
    - [ "PARASITIC_CHANNELING", 0.8 ]
formal_mappings:
  candidates:
    - target: Optimal Control with a Malicious Cost Function
      domain: Math
      mapping_kind: mathematical
      equation_hint: |
        J_target(u) = ∫ L(x,u) dt → J'_target(u) = ∫ (L(x,u) + L_manip(x,u)) dt
      justification: |
        The target naturally optimizes for their own objective function (J). The manipulator introduces a malicious cost/reward term (L_manip), altering the optimization landscape such that the new optimal control (u) for the target now serves the manipulator's goals. This directly maps to perturbing the Lagrangian with `V_manip`.
      references:
        - title: Optimal Control Theory: An Introduction
          where: Chapter on State-Dependent Cost Functions
          date: 1962-01-01
      confidence: 0.8
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "Successful, sustained manipulation requires the establishment of a Parasitic Channel, making the captured state self-reinforcing."
      domain: phenomenology
      falsifier: "Observation of a long-term Coherence Capture scenario where the manipulator must continuously inject dissonance and re-offer the false geodesic, because the target system shows no evidence of having internalized the manipulative path as a default."
      status: proposed
      links: [DOMA-155]
    - statement: "The three-stage model (Turbulence -> Geodesic -> Capture) is a necessary sequence for Coherence Capture."
      domain: theory
      falsifier: "Demonstration of a 'slow capture' or 'boiling frog' manipulation that achieves full entrainment without a discernible, acute phase of induced turbulence."
      status: proposed
      links: [DOMA-155]
naming_notes:
  collisions: []
  disambiguation: |
    Coherence Capture must be distinguished from **Resonant Synthesis (DYNA-002)**, which is a symmetric, mutually-beneficial process of creating a stronger, shared coherence. Capture is asymmetric and parasitic. It should also be distinguished from simple persuasion, which argues for a path's merits without first deliberately inducing a state of cognitive and emotional chaos in the target.
crosslinks:
  near_synonyms: []
  antonyms: [RESONANT_SYNTHESIS, COHERENCE_INTEGRITY]
  prerequisites: [TURBULENT_FLOW, LAMINAR_FLOW, FALSE_GEODESIC, WOUND_CHANNEL]
  downstream_effects: [PARASITIC_CHANNELING]
license: CC-BY-SA-4.0