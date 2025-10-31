---
term: "Coherent Engine"
canonical_id: "COHERENT_ENGINE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-039"]
---

---
term: Coherent Engine
canonical_id: COHERENT_ENGINE
symbol: 
aliases: [Living Frame, Autopoietic Team]
parents: [DOMA-039]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-039
      lines: "L31-L34"
      snippet: |
        This structure is a Coherent Engine, a stable Ki pattern that has proven exceptionally effective at transforming the chaotic Temporal Pressure (Γ) of its environment into valuable output.
  editors: [chain-of-thought-agent]
  review_log: []
triad:
  art: |
    A living vortex that metabolizes environmental chaos into a current of pure value, its sevenfold structure singing in harmony with the laws of flow.
  law: |
    A Coherent Engine is a 7-person system organized into the functional roles of Membrane (1), Sensorium (1), Crucible (3), and Catalyst (2). Its configuration maximizes the Pirouette Lagrangian (𝓛_p) by converting environmental pressure (V_Γ) into internal coherence (Kτ).
  philosophy: |
    The Coherent Engine replaces the mechanical metaphor of organization with a biological one. It demonstrates that the most resilient and productive structures are not engineered but cultivated, emerging as natural solutions to the universal drive for coherence.
pirouette_definition: |
  The functional manifestation of the Living Frame: a self-regulating, 7-person team structure that operates as a single living system. It is the optimal configuration for transforming environmental Temporal Pressure (Γ) into valuable output while maintaining a state of high internal coherence, or Laminar Flow. Its anatomy consists of seven essential, interdependent functions: the Membrane (interface), the Sensorium (feedback), the Crucible (core production), and the Catalyst (resilience/adaptation).
operational_definition:
  units: System (dimensionless count of 1)
  symbol_table:
    - name: 𝓛_p
      meaning: Pirouette Lagrangian; a measure of the system's net coherence.
      dimensions: "contextual (e.g., value/time)"
      default_range: "maximize > 0"
    - name: Kτ
      meaning: Internal Coherence; kinetic term representing productive output and alignment.
      dimensions: "contextual (e.g., value/time)"
      default_range: "high"
    - name: V_Γ
      meaning: Environmental Pressure; potential term representing energetic cost and external chaos.
      dimensions: "contextual (e.g., value/time)"
      default_range: "low"
  measurement:
    procedures:
      - name: Structural Audit & Performance Quantification
        outline: |
          1. Verify the presence and function of all 7 roles (1 Membrane, 1 Sensorium, 3 Crucible, 2 Catalyst) within a 7-person team.
          2. Quantify Internal Coherence (Kτ) via operational metrics (e.g., throughput, quality scores, cycle time). Example: `Kτ` measured as `(Calls per day * Quality %) / Avg. Handle Time`.
          3. Quantify Environmental Pressure (V_Γ) via metrics of friction and cost (e.g., rework rate, escalated issue count, overtime hours).
          4. Calculate the Pirouette Lagrangian (𝓛_p = Kτ - V_Γ). A sustained positive and high value indicates a functional Coherent Engine.
        expected_signals: [High throughput, High quality scores (e.g., '>>92%'), Low average handle times (e.g., <5 min), Low staff attrition, Low rate of systemic blockers.]
        pitfalls: [Confusing formal job titles with functional roles, Measuring only output (Kτ) without accounting for cost (V_Γ), Assuming a team is an Engine without all 7 roles being actively fulfilled.]
context_windows:
  - module: DOMA-039
    excerpt: |
      The Pirouette Framework demands a biological and physical perspective. A high-performing team is not a machine to be built, but a living, self-creating (autopoietic) system to be cultivated—an organism subject to the same universal laws that govern a star or a cell. This module provides the anatomy of that organism. It defines the Living Frame... This structure is a Coherent Engine, a stable Ki pattern that has proven exceptionally effective at transforming the chaotic Temporal Pressure (Γ) of its environment into valuable output.
  - module: DOMA-039
    excerpt: |
      The seven roles of the engine are not job titles; they are the fundamental functions required for any collaborative system to maintain coherence. They are the organs of a single living body. The Membrane manages the boundary, the Sensorium provides feedback, the Crucible performs value creation, and the Catalyst provides resilience and adaptation.
poetic_connections:
  motifs: [living system, vortex, metabolism, organism, garden]
  evocative_lines:
    - "We have tried to build organizations like clockwork, only to find they suffer like bodies."
    - "To build a Frame is not to manage people; it is to cultivate the conditions for coherence."
  association_matrix:
    - [ "LIVING_FRAME", 0.9 ]
    - [ "LAMINAR_FLOW", 0.8 ]
    - [ "TEMPORAL_PRESSURE", 0.7 ]
    - [ "ALCHEMICAL_UNION", 0.6 ]
formal_mappings:
  candidates:
    - target: Dissipative Structure
      domain: Non-Equilibrium Thermodynamics
      mapping_kind: conceptual
      equation_hint: |
        dS = dS_i + dS_e  (where dS_i > 0, and a stable state requires dS_e < 0)
      justification: |
        A Coherent Engine maintains its low-entropy, highly-ordered state (high Kτ) by importing energy and information (handling Γ) from its environment and exporting entropy (waste, resolved problems). Like Prigogine's dissipative structures, it is a stable, far-from-equilibrium system whose very structure is a consequence of the energy flowing through it.
      references:
        - title: Self-Organization in Nonequilibrium Systems
          where: "Ilya Prigogine"
          date: 1977-01-01
      confidence: 0.8
    - target: Autopoietic System
      domain: Systems Biology
      mapping_kind: conceptual
      justification: |
        The source text explicitly uses the term "autopoietic." The Engine's roles (Membrane, Sensorium, Crucible, Catalyst) map directly to the components required for a system to continuously produce and maintain itself, defining its own boundary and internal laws of operation in response to its environment.
      references:
        - title: Autopoiesis and Cognition
          where: "Humberto Maturana & Francisco Varela"
          date: 1980-01-01
      confidence: 0.9
  adopted:
    - target: 
      rationale: 
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "A 7-person team structured as a Coherent Engine will consistently outperform a traditionally managed team of the same size and talent on composite metrics of efficiency (Kτ) and resilience (resistance to V_Γ)."
      domain: experiment
      falsifier: "A controlled, longitudinal study (t > 6 months) shows no statistically significant difference in performance and/or team health (e.g., attrition, burnout) between a Coherent Engine and a control group, or the control group performs better."
      status: proposed
      links: [DOMA-039]
naming_notes:
  collisions: []
  disambiguation: |
    The "Living Frame" is the static blueprint or anatomy of the 7-role structure. The "Coherent Engine" is the dynamic, living, and functioning system itself—the Frame in motion. One is the map, the other is the territory in action.
crosslinks:
  near_synonyms: [LIVING_FRAME]
  antonyms: [DISSONANT_HIERARCHY]
  prerequisites: [PRINCIPLE_OF_MAXIMAL_COHERENCE, LAMINAR_FLOW, TEMPORAL_PRESSURE, ALCHEMICAL_UNION]
  downstream_effects: [ORGANIZATIONAL_LAMINAR_FLOW]
license: CC-BY-SA-4.0
---