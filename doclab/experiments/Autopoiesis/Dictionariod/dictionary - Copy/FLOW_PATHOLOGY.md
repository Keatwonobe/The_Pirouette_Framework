---
term: "Flow Pathology"
canonical_id: "FLOW_PATHOLOGY"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-118"]
---

---
term: Flow Pathology
canonical_id: FLOW_PATHOLOGY
symbol: 
aliases: [Coherence Collapse, Systemic Collapse]
parents: [DOMA-118]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-118
      lines: "§3"
      snippet: |
        Applying the Caduceus Lens (DYNA-003) to a dying system reveals that collapse is not a single event, but the terminal destination of one of three distinct pathological journeys.
  editors: [System Agent]
  review_log: []
triad:
  art: |
    A system forgetting its song. A state where the feedback loops that once maintained form become accelerants for unraveling, pushing the system off its coherent path until it can no longer find its way back.
  law: |
    A state is pathologically diagnosed when a system's rate of coherence loss (dKτ/dt) is negative and accelerating, or when flow diagnostics (DYNA-001) classify its state as predominantly Turbulent, Stagnant, or Erosive, predicting either elastic or critical collapse.
  philosophy: |
    To study collapse is not to court despair, but to learn the grammar of endings. It reframes failure from a mechanical event to a dynamic process, granting the wisdom to know when to mend a system and when to compose something new from the ruins.
pirouette_definition: |
  A state of compromised coherence where a system can no longer solve the Pirouette Lagrangian optimization problem, causing it to deviate from its path of maximal coherence and enter a feedback loop of degradation leading to systemic collapse. A flow pathology is diagnosed as one of three primary forms: **Turbulence** (rapid, chaotic self-cancellation), **Stagnation** (catastrophic blockage of a critical flow), or **Erosion** (the slow, cumulative decay of coherence). The severity of the pathology determines whether the resulting collapse is recoverable (Elastic) or irreversible (Critical).
operational_definition:
  units: Qualitative Classification (Turbulent, Stagnant, Erosive)
  symbol_table: []
  measurement:
    procedures:
      - name: Pathological Diagnosis via Flow Mapping
        outline: |
          1. Map the system's vital flows (energy, information, resources).
          2. Apply Flow Diagnostics (DYNA-001) to time-series data from these flows to classify the dominant state.
          3. Trace the cascade of failure from the initial point of pathological flow.
          4. Assess the integrity of the system's Wound Channel (CORE-011) to distinguish between a recoverable (Elastic) or irreversible (Critical) collapse.
        expected_signals:
          - **Turbulence:** High-frequency, low-coherence, high-amplitude fluctuations in system outputs; rapid energy expenditure with low work output.
          - **Stagnation:** Signal starvation or pressure overload in subsystems; a critical metric flatlining while upstream pressure builds catastrophically.
          - **Erosion:** A steady increase in the noise-to-signal ratio over time; gradual decay of a core performance metric.
        pitfalls:
          - Misdiagnosing a symptom for the cause (e.g., treating a Turbulent market crash without identifying the underlying Stagnant liquidity freeze).
          - Assuming reversibility based on symptom relief, without assessing the underlying Wound Channel for permanent damage.
context_windows:
  - module: DOMA-118
    excerpt: |
      Collapse begins when a system can no longer solve this optimization problem. When the pressure becomes too great or its internal resonance falters, it is knocked off its geodesic. The feedback loops that once maintained its form become accelerants for its own unraveling. The system is no longer solving for existence; it is solving for zero.
  - module: DOMA-118
    excerpt: |
      The most important question in any collapse is that of reversibility. This is determined by the integrity of the system's **Wound Channel**—the geometric memory of its healthy, coherent state... Elastic Collapse... is recoverable... Critical Collapse... is an irreversible fracture where the memory of the healthy state is erased.
poetic_connections:
  motifs: [a forgotten song, an unraveling thread, a fever, a blockage, a slow rust, a fracture]
  evocative_lines:
    - "A system does not merely break; it first forgets its own song."
    - "To understand the anatomy of a fracture is to know the difference between that which can be mended and that which must be reborn."
  association_matrix:
    - [ "SYSTEMIC_COLLAPSE", 0.9 ]
    - [ "WOUND_CHANNEL", 0.8 ]
    - [ "TURBULENT_FLOW", 0.7 ]
    - [ "STAGNANT_FLOW", 0.7 ]
    - [ "COHERENCE_EROSION", 0.7 ]
    - [ "LAMINAR_FLOW", -0.9 ]
formal_mappings:
  candidates:
    - target: Pathological states in dynamical systems
      domain: Math
      mapping_kind: conceptual
      equation_hint: |
        dx/dt = F(x)
      justification: |
        Flow Pathologies represent basins of attraction in a system's state space that lead to collapse. Turbulence is a chaotic attractor with high energy dissipation; Stagnation is a non-productive fixed point (e.g., gridlock in network flow); and Erosion is the slow drift towards a high-entropy, decoherent state.
      references:
        - title: Nonlinear Dynamics and Chaos
          where: S. Strogatz
          date: 2014-01-01
      confidence: 0.8
    - target: Modes of cell death (necrosis, apoptosis)
      domain: Biology
      mapping_kind: conceptual
      justification: |
        The pathologies mirror distinct biological failure modes. Turbulence is analogous to necrosis (violent, chaotic cell rupture), Stagnation to ischemia (cell death from blocked blood flow), and Erosion to apoptosis or cellular senescence (programmed or age-related decline).
      confidence: 0.6
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "All systemic collapses can be classified as resulting from one or a combination of the three primary flow pathologies: Turbulence, Stagnation, or Erosion."
      domain: theory
      falsifier: "The discovery of a systemic collapse mode that cannot be described by these dynamics, such as a collapse occurring with no detectable change in flow characteristics, or a novel fourth pathology with distinct diagnostic signals."
      status: proposed
      links: [DOMA-118]
naming_notes:
  collisions: []
  disambiguation: |
    "Flow Pathology" refers to the dynamic state of decline, not the terminal event of collapse itself. The outcome of a pathology is either an Elastic Collapse (recoverable) or a Critical Collapse (irreversible), distinguished by the state of the Wound Channel. The three diagnoses (Turbulence, Stagnation, Erosion) are specific types of the general condition.
crosslinks:
  near_synonyms: [SYSTEMIC_COLLAPSE, COHERENCE_COLLAPSE]
  antonyms: [LAMINAR_FLOW, SYSTEMIC_HEALTH]
  prerequisites: [FLOW_DIAGNOSTICS, PIROUETTE_LAGRANGIAN, WOUND_CHANNEL]
  downstream_effects: [ELASTIC_COLLAPSE, CRITICAL_COLLAPSE]
license: CC-BY-SA-4.0
---

# Flow Pathology

## Canonical (Pirouette)
A state of compromised coherence where a system can no longer solve the Pirouette Lagrangian optimization problem, causing it to deviate from its path of maximal coherence and enter a feedback loop of degradation leading to systemic collapse. A flow pathology is diagnosed as one of three primary forms: **Turbulence** (rapid, chaotic self-cancellation), **Stagnation** (catastrophic blockage of a critical flow), or **Erosion** (the slow, cumulative decay of coherence). The severity of the pathology determines whether the resulting collapse is recoverable (Elastic) or irreversible (Critical).

## EFT-First Summary
In dynamical systems theory, a Flow Pathology corresponds to a system entering a basin of attraction that leads to collapse. **Turbulence** maps to chaotic attractors characterized by high, inefficient energy dissipation. **Stagnation** maps to non-productive fixed points, such as gridlock in network flow models or states of high potential energy behind a barrier. **Erosion** is analogous to the slow, irreversible increase of entropy as described by the Second Law of Thermodynamics, representing a system's drift towards a high-entropy, decoherent state.

## Glossary Links
- See also: [Systemic Collapse](<#>), [Laminar Flow](<#>), [Wound Channel](<#>), [Turbulence](<#>), [Stagnation](<#>), [Erosion](<#>)