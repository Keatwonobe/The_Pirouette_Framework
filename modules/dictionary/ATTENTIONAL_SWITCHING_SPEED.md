---
term: "Attentional Switching Speed"
canonical_id: "ATTENTIONAL_SWITCHING_SPEED"
symbol: "$T_a$"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["XCM-001_Interruptable_cognition"]
---

---
term: Attentional Switching Speed
canonical_id: ATTENTIONAL_SWITCHING_SPEED
symbol: $T_a$
aliases: [Cognitive switching speed, Task-set switching latency]
parents: [XCM-001]
children: [XCM-004]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: XCM-001
      lines: "L20-L22"
      snippet: |
        The core of the framework (high φ, fast-switching Tₐ) is preserved.
  editors: [system]
  review_log: []
triad:
  art: |
    The mind as a hummingbird, flitting from one bloom of thought to the next without losing a drop of nectar. It is the grace of a sudden turn, the pivot that reveals a new landscape.
  law: |
    The time cost, $T_a$, of disengaging from Task A and achieving baseline proficiency in an unrelated Task B is a non-zero, measurable quantity. A lower $T_a$ indicates higher cognitive fluidity and is a primary objective of Interruptive Cognition training.
  philosophy: |
    Cognitive inertia is a liability in a high-stochasticity environment. Cultivating a low $T_a$ is not merely about multitasking, but about achieving a state of interruptible flow, enabling an agent to reorient and synthesize fragmented inputs into coherent action without cognitive collapse.
pirouette_definition: |
  The characteristic time, $T_a$, required for a cognitive agent to fully disengage from a prior attentional state or task-set and re-engage with a new, distinct one. Within the Pirouette framework, it is a primary measure of cognitive plasticity and resilience against decoherence. It is measured as the latency between a switch-cue and the return to a pre-defined performance baseline on the new task.
operational_definition:
  units: seconds (s)
  symbol_table:
    - name: $T_a$
      meaning: The time interval required to switch attentional state.
      dimensions: T
      default_range: 0.2 s - 5 s
  measurement:
    procedures:
      - name: Task-Set Interruption Latency Protocol
        outline: |
          1. Subject performs a baseline cognitive task (e.g., logic puzzle) to a stable performance level ($P_{base,1}$).
          2. An interruption cue (e.g., auditory 'cognitive chirp') is presented, followed immediately by a second, unrelated task (e.g., fractal reassembly).
          3. $T_a$ is measured as the time from the interruption cue to the point where the subject's performance on the second task reaches 90% of its own established baseline ($0.9 \times P_{base,2}$).
          4. The protocol is repeated with varied task pairs to establish a mean $T_a$.
        expected_signals: [EEG P300 component, Response time (RT) curves, Post-switch error rate spikes]
        pitfalls: [Conflation of switch cost with task difficulty, Practice effects artificially lowering $T_a$ in-session, Subject fatigue]
context_windows:
  - module: XCM-001
    excerpt: |
      Interruptive cognition arises as a compensatory adaptation in high-disruption minds. However, certain non-destructive training environments may simulate the benefits of such disruption if... the subject is taught to synthesize fragmented thought states into insight paths [and] the core of the framework (high φ, fast-switching Tₐ) is preserved.
  - module: XCM-001
    excerpt: |
      We hypothesize that a group trained using this method: Exhibits decreased $T_a$ (faster switching) under high-stochasticity environments, adapts quickly to fractured input domains (multi-agent, multi-signal), can maintain multi-phase attention and resolve contradictions quickly, [and] develops resilience to decoherence attacks.
poetic_connections:
  motifs: [fluidity, fracture, synthesis, pivot, lightning, interruption]
  evocative_lines:
    - "How do we train someone to think like lightning without being struck by it?"
    - "What did you rebuild, and how?"
  association_matrix:
    - [ "COGNITIVE_PLASTICITY", 0.9 ]
    - [ "DECOHERENCE_RESISTANCE", 0.7 ]
    - [ "INTERRUPTIVE_COGNITION", 0.9 ]
formal_mappings:
  candidates:
    - target: Task-switching cost (Switch Cost)
      domain: Cognitive Psychology
      mapping_kind: operational
      justification: |
        Task-switching paradigms in cognitive psychology directly measure the time penalty (switch cost) incurred when shifting between tasks with different rule-sets. $T_a$ is an operationalization of this switch cost, framed within Pirouette as a trainable capacity for resilience rather than just an innate cognitive limitation.
      references:
        - title: "Resolving task-set competition: The switch-cost paradigm"
          where: "Psychological Research, 73(4), 2009"
          date: 2009-07-01
      confidence: 0.9
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "Training protocols outlined in XCM-001 can produce a statistically significant decrease in an individual's mean $T_a$ compared to control groups."
      domain: experiment
      falsifier: "A longitudinal study showing no significant difference in $T_a$ between the XCM-001 training group and a control group engaged in general cognitive training (e.g., standard puzzles)."
      status: proposed
      links: [XCM-001]
naming_notes:
  collisions: [$T$ is often used for Temperature or a generic Time period. The subscript 'a' is critical.]
  disambiguation: |
    Distinguish from simple reaction time (RT). $T_a$ measures the *cost of switching* an entire cognitive set, not the speed of responding to a simple stimulus within an established set. It includes the time to disengage, reconfigure, and re-engage.
crosslinks:
  near_synonyms: [SWITCH_COST]
  antonyms: [COGNITIVE_INERTIA, ATTENTIONAL_FIXITY]
  prerequisites: [TASK_SET, COGNITIVE_STATE]
  downstream_effects: [DECOHERENCE_RESISTANCE, ADAPTIVE_COGNITION]
license: CC-BY-SA-4.0