---
term: "The Sensorium"
canonical_id: "THE_SENSORIUM"
symbol: ""
aliases: [Feedback]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-039"]
---

---
term: The Sensorium
canonical_id: THE_SENSORIUM
symbol: 
aliases: [Feedback]
parents: [DOMA-039]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-039
      lines: "L102-L107"
      snippet: |
        The Sensorium (Feedback):
        Function: To act as the system's proprioception and nervous system. The Sensorium continuously measures the health and rhythm of the engine's internal state—its flow, its coherence, its emergent Ki. It makes the invisible currents of performance and morale visible, providing the real-time data necessary for the system to self-correct and maintain its geodesic.
  editors: [AI-Agent-S2]
  review_log: []
triad:
  art: |
    The Sensorium is the ghost in the machine made manifest, the team’s proprioceptive nerve translating the silent hum of coherence into a visible, actionable signal. It is the part of the body that knows itself.
  law: |
    A system's rate of adaptation is directly proportional to the bandwidth and inversely proportional to the latency of its Sensorium's feedback loop. A dysfunctional Sensorium will always correlate with increased system turbulence and a decay in Laminar Flow.
  philosophy: |
    A team without a Sensorium is blind to its own internal state, navigating by inertia and anecdote. This function establishes an objective basis for self-regulation, replacing subjective 'feel' with shared, verifiable data, enabling the autopoietic system to course-correct before minor dissonances become catastrophic failures.
pirouette_definition: |
  The Sensorium is one of the seven functional roles of the Living Frame, acting as the team's internal nervous system. Its primary function is to continuously measure, interpret, and communicate the internal state of the Coherent Engine—its flow, efficiency, quality, and morale (Internal Coherence, Kτ). By making these invisible dynamics visible, the Sensorium provides the real-time feedback necessary for the system to self-regulate and maintain Laminar Flow.
operational_definition:
  units: Varies by metric (e.g., rate, count, dimensionless ratio); fundamentally information rate (bits/sec).
  symbol_table:
    - name: Kτ
      meaning: Internal Coherence; a composite measure of team health and performance.
      dimensions: dimensionless
      default_range: "[0, 1] or contextual score"
    - name: λ
      meaning: Throughput; rate of value creation.
      dimensions: T⁻¹
      default_range: "e.g., 75 units/day"
    - name: Q
      meaning: Quality; adherence to acceptance criteria.
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: T_h
      meaning: Handle Time; time to process a single work unit.
      dimensions: T
      default_range: "e.g., <= 300 seconds"
  measurement:
    procedures:
      - name: Coherence Monitoring
        outline: |
          1. Identify key performance indicators (KPIs) that serve as proxies for Internal Coherence (Kτ), such as throughput (λ), quality (Q), and handle time (T_h).
          2. Instrument the Crucible's workflow to capture these metrics in real-time or near-real-time.
          3. Synthesize raw data into a simple, high-bandwidth signal (e.g., a shared dashboard) visible to all roles in the Frame.
          4. Ensure the signal's update frequency is significantly higher than the system's characteristic response time (τ_p).
        expected_signals: [Real-time Kτ-proxy dashboards, cycle time histograms, quality trend charts.]
        pitfalls: [Measuring vanity metrics that do not correlate to Kτ, signal latency exceeding the Pirouette Cycle (τ_p) causing overcorrection, overwhelming the team with low-signal data.]
context_windows:
  - module: DOMA-039
    excerpt: |
      To act as the system's proprioception and nervous system. The Sensorium continuously measures the health and rhythm of the engine's internal state—its flow, its coherence, its emergent Ki. It makes the invisible currents of performance and morale visible, providing the real-time data necessary for the system to self-correct and maintain its geodesic.
  - module: DOMA-039
    excerpt: |
      The Sensorium monitors the health and output of this cycle, providing real-time feedback to all parts of the engine. [...] This is not a linear process but a self-sustaining pirouette, a closed loop of action and feedback that, when healthy, gains momentum and stability with every turn.
poetic_connections:
  motifs: [proprioception, nervous_system, feedback_loop, visibility, mirror, self-awareness]
  evocative_lines:
    - "It makes the invisible currents of performance and morale visible."
    - "the system's proprioception and nervous system."
    - "a closed loop of action and feedback"
  association_matrix:
    - [ "INTERNAL_COHERENCE", 0.9 ]
    - [ "LIVING_FRAME", 0.8 ]
    - [ "LAMINAR_FLOW", 0.7 ]
    - [ "SELF_REGULATION", 0.8 ]
formal_mappings:
  candidates:
    - target: State Observer
      domain: Math
      mapping_kind: operational
      equation_hint: |
        dx̂/dt = Ax̂ + Bu + L(y - ŷ)
      justification: |
        In control theory, a state observer estimates the internal state of a system from its inputs and outputs. The Sensorium performs this exact function for the Living Frame, estimating the internal 'state' of coherence (Kτ) from performance outputs, enabling feedback control (self-regulation). The observer gain `L` represents the Sensorium's sensitivity.
      references:
        - title: Modern Control Engineering
          where: Katsuhiko Ogata, Ch. 10
          date: 2010-01-01
      confidence: 0.8
    - target: Proprioception
      domain: Biology
      mapping_kind: conceptual
      justification: |
        Proprioception is an organism's sense of the relative position and movement of its own body parts. The Sensorium provides this "sense of self" for the team-as-organism, allowing it to coordinate its actions and maintain balance (coherence) without constant, top-down intervention for every micro-adjustment.
      references:
        - title: Principles of Neural Science
          where: Kandel et al., Ch. 22
          date: 2012-01-01
      confidence: 0.9
  adopted:
    []
constraints_and_falsifiers:
  claims:
    - statement: "A Living Frame team equipped with a functional Sensorium (e.g., real-time dashboard) will exhibit a statistically significant shorter recovery time from external shocks (spikes in Γ) compared to a team without one (e.g., using weekly reports)."
      domain: experiment
      falsifier: "An A/B test showing no significant difference in the time required to return to baseline Kτ between the two conditions."
      status: proposed
      links: [DOMA-039]
naming_notes:
  collisions: []
  disambiguation: |
    The Sensorium is a *functional role*, not necessarily a single person with the job title 'Analyst'. In smaller Frames, this function might be distributed or rotated among members, but the act of measurement and feedback must be explicitly owned and performed continuously. It is distinct from The Membrane, which senses the *external* environment; the Sensorium senses the *internal* state.
crosslinks:
  near_synonyms: [FEEDBACK_LOOP]
  antonyms: [INFORMATION_SILO, OPERATIONAL_BLINDNESS]
  prerequisites: [LIVING_FRAME, INTERNAL_COHERENCE]
  downstream_effects: [LAMINAR_FLOW, SELF_REGULATION, ADAPTIVE_CAPACITY]
license: CC-BY-SA-4.0
---

# The Sensorium

## Canonical (Pirouette)
The Sensorium is one of the seven functional roles of the Living Frame, acting as the team's internal nervous system. Its primary function is to continuously measure, interpret, and communicate the internal state of the Coherent Engine—its flow, efficiency, quality, and morale (Internal Coherence, Kτ). By making these invisible dynamics visible, the Sensorium provides the real-time feedback necessary for the system to self-regulate and maintain Laminar Flow.

## EFT-First Summary
Operationally, The Sensorium functions as a **State Observer** from control theory, estimating the internal state (Internal Coherence, `Kτ`) of the team system from performance outputs. Conceptually, it is analogous to biological **proprioception**, providing the team-as-organism with a sense of its own position and movement, which is critical for maintaining balance and coordinating action. A high-bandwidth, low-latency Sensorium is a prerequisite for robust self-regulation and resilience.

## Glossary Links
- See also: [Living Frame](...), [Internal Coherence](...), [Laminar Flow](...)