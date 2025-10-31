---
term: "Path Fixation"
canonical_id: "PATH_FIXATION"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-126"]
---

---
term: Path Fixation
canonical_id: PATH_FIXATION
symbol: 
aliases: [Rigidity, Channel Lock-in]
parents: [DOMA-126]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-126
      lines: "§3, Table Row 3"
      snippet: |
        Path Fixation (Rigidity): The system resists change and innovation, trapped in its degraded Wound Channel. It can only repeat familiar, inefficient patterns.
  editors: [chain-of-thought-agent]
  review_log: []
triad:
  art: |
    The riverbed that once guided the flow becomes a rutted prison, its memory of the true path eroded into a stubborn, inefficient scar. What once was a guide becomes a cage.
  law: |
    A system exhibits Path Fixation when its response to novel stimuli is a repetition of historical patterns, even when those patterns demonstrably decrease its temporal coherence (Kτ) and increase its energetic cost per cycle.
  philosophy: |
    Path Fixation reveals the paradoxical nature of systemic memory (the Wound Channel); what provides stability and identity can become a cage, transforming the mechanism of self-perpetuation into a driver of self-stagnation and decay.
pirouette_definition: |
  A state of systemic rigidity resulting from advanced Coherence Erosion. The system's Wound Channel becomes a degraded, inefficient, but deeply carved "rut" that compulsively guides its dynamics. This turns the mechanism of historical memory from a source of stability into an engine of stagnation, preventing adaptation and accelerating the decay towards Cascade Failure.
operational_definition:
  units: Dimensionless state indicator
  symbol_table:
    - name: Kτ
      meaning: Temporal Coherence; a measure of a system's signal integrity over time.
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: Wound Channel
      meaning: The historical trajectory of a system's dynamics, acting as an attractive path.
      dimensions: state space trajectory
      default_range: contextual
  measurement:
    procedures:
      - name: Perturbation Response Analysis
        outline: |
          1. Establish a baseline measurement of the system's primary operational cycle, noting its energy consumption and output precision (Kτ).
          2. Introduce a controlled, novel stimulus designed to offer a more efficient pathway for the system's core process.
          3. Measure the system's response trajectory and new steady-state efficiency.
          4. Path Fixation is confirmed if the system reverts to its baseline trajectory within 3-5 cycles, rejecting the efficient alternative, accompanied by a transient increase in internal friction (energy cost).
        expected_signals: [Rejection of novel inputs, increased energy cost per cycle, reversion to historical patterns.]
        pitfalls: [Distinguishing true fixation from healthy, robust stability. The key differentiator is the efficiency cost; stability maintains or improves efficiency, fixation sacrifices it to maintain a pattern.]
context_windows:
  - module: DOMA-126
    excerpt: |
      As the Ki pattern becomes noisy, the Wound Channel it carves becomes less defined. The riverbed begins to erode and widen. Each meandering step makes this new, less efficient path slightly deeper, and the optimal one slightly harder to return to... The memory that once ensured stability now ensures the persistence of a suboptimal state, making the system more susceptible to further deviation.
  - module: DOMA-126
    excerpt: |
      A blurry, rutted Wound Channel provides weaker guidance, yet its inertia still compels the system to follow it. The memory that once ensured stability now ensures the persistence of a suboptimal state... This loop—from noise, to Ki degradation, to a rutted Wound Channel, to greater susceptibility to noise—is the engine of drift.
poetic_connections:
  motifs: [rutted road, memory as a cage, hardened arteries, institutional sclerosis, dogmatism]
  evocative_lines:
    - "The memory that once ensured stability now ensures the persistence of a suboptimal state."
    - "It is the quiet tragedy of a song slowly going out of tune, of a purpose forgotten one small compromise at a time."
  association_matrix:
    - [ "WOUND_CHANNEL", 0.9 ]
    - [ "COHERENCE_EROSION", 0.8 ]
    - [ "CASCADE_FAILURE", 0.6 ]
    - [ "TURBULENT_FLOW", 0.3 ]
formal_mappings:
  candidates:
    - target: Path Dependence
      domain: Economics|Social Science
      mapping_kind: conceptual
      equation_hint:
      justification: |
        Path Dependence describes how historical choices, even if suboptimal, can become "locked-in" by network effects or increasing returns. This strongly parallels Path Fixation, where a degraded Wound Channel becomes a self-reinforcing, inefficient equilibrium from which escape is energetically costly. The QWERTY keyboard is a classic example of a suboptimal standard locked-in by its own history.
      references:
        - title: Increasing Returns and Path Dependence in the Economy
          where: University of Michigan Press
          date: 1994-01-01
      confidence: 0.9
    - target: Hysteresis
      domain: CM
      mapping_kind: mathematical
      equation_hint: |
        ∮ B ⋅ dH ≠ 0
      justification: |
        Hysteresis is the dependence of a system's state on its history. For example, a magnetic material's magnetization depends on the history of the applied magnetic field. This mirrors how a system in Path Fixation follows a trajectory determined by its degraded past, not just its present conditions.
      references:
        - title: Introduction to Electrodynamics
          where: Chapter 6
          date: 2017-01-01
      confidence: 0.7
  adopted:
    - target: Path Dependence
      rationale: The concept of "lock-in" to a suboptimal but stable state due to historical inertia is a near-perfect conceptual match, providing the most direct and operationally useful analogy from established science.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "A system in a state of Path Fixation cannot access a more coherent (higher Kτ) state via small, local perturbations; a large-scale intervention (e.g., Coherent Injection) is required to shift it from its degraded basin of attraction."
      domain: phenomenology
      falsifier: "Observation of a system diagnosed with Path Fixation spontaneously self-correcting to its optimal geodesic, without external, large-scale intervention, driven only by its own internal noise."
      status: proposed
      links: [DOMA-126]
naming_notes:
  collisions: [Psychological fixation (e.g., Freudian), fixation in biology (e.g., nitrogen fixation).]
  disambiguation: |
    Distinguish from systemic stability. Stability is the robust maintenance of an *optimal*, high-coherence path against perturbations. Path Fixation is the robust maintenance of a *suboptimal*, degraded path, often at a significant and continuous energetic cost.
crosslinks:
  near_synonyms: [SYSTEMIC_RIGIDITY]
  antonyms: [RESONANT_ADAPTATION, SYSTEMIC_PLASTICITY]
  prerequisites: [COHERENCE_EROSION, WOUND_CHANNEL]
  downstream_effects: [CASCADE_FAILURE]
license: CC-BY-SA-4.0
---

# Path Fixation

## Canonical (Pirouette)
A state of systemic rigidity resulting from advanced Coherence Erosion. The system's Wound Channel becomes a degraded, inefficient, but deeply carved "rut" that compulsively guides its dynamics. This turns the mechanism of historical memory from a source of stability into an engine of stagnation, preventing adaptation and accelerating the decay towards Cascade Failure.

## EFT-First Summary
In the language of social and economic theory, Path Fixation is analogous to **Path Dependence**. A system becomes 'locked-in' to a historically determined trajectory, reinforced by increasing returns to that path, even when more efficient alternatives exist. This occurs when the system's memory (`Wound Channel`) of a degraded state becomes so entrenched that escaping the local minimum of this suboptimal basin of attraction is energetically prohibitive without a significant external shock or intervention.

## Glossary Links
- See also: Coherence Erosion, Wound Channel, Cascade Failure