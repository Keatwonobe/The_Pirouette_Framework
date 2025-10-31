---
term: "Living Frame"
canonical_id: "LIVING_FRAME"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-039"]
---

---
term: Living Frame
canonical_id: LIVING_FRAME
symbol: 
aliases: [Coherent Engine, The Frame]
parents: [CORE-006, CORE-012, DYNA-001]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-039
      lines: "§1"
      snippet: |
        This module provides the anatomy of that organism. It defines the **Living Frame**, a 7-person team forged through an **Alchemical Union** (CORE-012) of individual talents into a single, unified coherence manifold.
  editors: [chain-of-thought-agent]
  review_log: []
triad:
  art: |
    A team is not a clockwork machine to be assembled, but a garden to be cultivated. The Living Frame is the blueprint for this garden, a commonwealth of functions that grows into a resilient, living system. It learns to sing in harmony with the laws of its environment.
  law: |
    A 7-person team structured with 1 Membrane, 1 Sensorium, 3 Crucible, and 2 Catalyst roles is a stable, low-energy solution to the Pirouette Lagrangian (𝓛_p = Kτ - V_Γ). This configuration maximizes internal coherence (Kτ) and minimizes dissipative losses from environmental pressure (V_Γ), naturally sustaining Laminar Flow.
  philosophy: |
    The most effective organizational structures are not imposed by managerial fiat but are emergent solutions to fundamental physical principles. The Living Frame replaces the fragile, static blueprint of a hierarchy with the resilient, adaptive anatomy of an organism. Its purpose is to create the conditions for coherence, allowing the team to find its own elegant, autopoietic path.
pirouette_definition: |
  A 7-person team structured as an autopoietic, living system to maximize performance according to the Principle of Maximal Coherence. Its structure is not a hierarchy of titles but an interdependent set of four core functions—Membrane (1x, interface), Sensorium (1x, feedback), Crucible (3x, core production), and Catalyst (2x, resilience/adaptation)—that form a single, self-regulating 'Coherent Engine'. This configuration is a proven, stable Ki pattern for transforming environmental pressure (Γ) into coherent value.
operational_definition:
  units: Dimensionless structure (role count)
  symbol_table:
    - name: N_M
      meaning: Count of members performing the Membrane function
      dimensions: dimensionless
      default_range: 1
    - name: N_S
      meaning: Count of members performing the Sensorium function
      dimensions: dimensionless
      default_range: 1
    - name: N_Crb
      meaning: Count of members performing the Crucible function
      dimensions: dimensionless
      default_range: 3
    - name: N_Ctl
      meaning: Count of members performing the Catalyst function
      dimensions: dimensionless
      default_range: 2
  measurement:
    procedures:
      - name: Functional Role Audit
        outline: |
          1. Map the 7 team members to the four primary functions (Membrane, Sensorium, Crucible, Catalyst) based on their actual day-to-day activities and communication patterns, irrespective of job titles.
          2. Analyze communication and workflow data (e.g., ticket system, comms channels) to verify that value flows along the Pirouette Cycle.
          3. Measure the team's internal coherence (Kτ) via metrics like throughput, quality, and cycle time stability.
          4. A successful implementation will show the 1-1-3-2 role distribution and high, stable Kτ metrics.
        expected_signals: [High and stable throughput, Quality ≥ 92%, Low Avg. Handle Time, Qualitative reports of "Laminar Flow"]
        pitfalls: ["Role-Title Confusion" (mistaking a job title for a function), "Incomplete Frame" (a core function is unstaffed, creating a systemic vulnerability)]
context_windows:
  # Short, trimmed context quotes harvested from modules (3–6 sentences each).
  - module: DOMA-039
    excerpt: |
      A high-performing team is not a machine to be built, but a living, self-creating (autopoietic) system to be cultivated—an organism subject to the same universal laws that govern a star or a cell. This module provides the anatomy of that organism. It defines the **Living Frame**, a 7-person team forged through an **Alchemical Union** (CORE-012) of individual talents into a single, unified coherence manifold.
  - module: DOMA-039
    excerpt: |
      The seven roles of the engine are not job titles; they are the fundamental functions required for any collaborative system to maintain coherence. They are the organs of a single living body. The Membrane manages the boundary, the Sensorium provides feedback, the Crucible performs value creation, and the Catalyst ensures resilience and adaptation.
poetic_connections:
  # Lightweight "word-association graph" and sticky lines.
  motifs: [autopoiesis, living system, organism, garden vs machine, coherence manifold, resonant current]
  evocative_lines:
    - "We have tried to build organizations like clockwork, only to find they suffer like bodies."
    - "To build a Frame is not to manage people; it is to cultivate the conditions for coherence."
  association_matrix:
    # symmetric or directed; weights in [0,1]
    - [ "LAMINAR_FLOW", 0.9 ]
    - [ "ALCHEMICAL_UNION", 0.8 ]
    - [ "PIRIOUETTE_LAGRANGIAN", 0.7 ]
    - [ "COHERENCE", 0.9 ]
formal_mappings:
  # Candidate alignments to EFT/SM/CM/GR terms, each with justification and refs.
  candidates:
    - target: Magic number (nuclear shell model)
      domain: Nuclear Physics
      mapping_kind: conceptual
      equation_hint: |
        N/A
      justification: |
        The Living Frame's 7-person structure (1-1-3-2) is posited as a uniquely stable and efficient configuration for a human collaborative system. This is analogous to "magic numbers" in nuclear physics, where atomic nuclei with specific numbers of nucleons exhibit unusually high stability and binding energy. The Frame represents a deep potential-energy well in the configuration space of team structures.
      references:
        []
      confidence: 0.3
  adopted:
    []
constraints_and_falsifiers:
  claims:
    - statement: "A 7-person team structured as a Living Frame (1-1-3-2) will consistently outperform teams of the same size with different functional role distributions on metrics of throughput, quality, and stability (Kτ) when subjected to equivalent environmental pressure (V_Γ)."
      domain: experiment
      falsifier: "An A/B test showing a differently structured 7-person team (e.g., 1-0-5-1 'hero-and-minions' model) consistently achieving higher Kτ or greater stability under the same V_Γ."
      status: proposed
      links: [DOMA-039]
naming_notes:
  collisions: ["Frame of reference"]
  disambiguation: |
    In Pirouette, 'Frame' specifically refers to the *Living Frame*, the 7-person autopoietic team structure. It is distinct from a 'frame of reference' (a coordinate system) or a static 'framework'. The modifier 'Living' emphasizes its biological, adaptive, and self-regulating nature.
crosslinks:
  near_synonyms: [COHERENT_ENGINE]
  antonyms: [STATIC_HIERARCHY]
  prerequisites: [PIRIOUETTE_LAGRANGIAN, ALCHEMICAL_UNION, LAMINAR_FLOW]
  downstream_effects: [LAMINAR_FLOW, ORGANIZATIONAL_COHERENCE]
license: CC-BY-SA-4.0
---

# Living Frame

## Canonical (Pirouette)
A 7-person team structured as an autopoietic, living system to maximize performance according to the Principle of Maximal Coherence. Its structure is not a hierarchy of titles but an interdependent set of four core functions—Membrane (1x, interface), Sensorium (1x, feedback), Crucible (3x, core production), and Catalyst (2x, resilience/adaptation)—that form a single, self-regulating 'Coherent Engine'. This configuration is a proven, stable Ki pattern for transforming environmental pressure (Γ) into coherent value.

## EFT-First Summary
No direct mapping to an effective field theory has been adopted. The Living Frame is best understood conceptually as an organizational analogue to stable configurations in physics, such as molecules or "magic number" nuclei, which represent local minima in a potential energy landscape. The 7-person structure is hypothesized to be such a minimum for a team seeking to maximize its coherence against environmental pressure.

## Glossary Links
- See also: [Coherent Engine](), [Static Hierarchy](), [Pirouette Lagrangian](PIRIOUETTE_LAGRANGIAN), [Laminar Flow](LAMINAR_FLOW)