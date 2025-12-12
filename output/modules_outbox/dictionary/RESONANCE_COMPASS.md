---
term: "Resonance Compass"
canonical_id: "RESONANCE_COMPASS"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-179"]
---

---
term: Resonance Compass
canonical_id: RESONANCE_COMPASS
symbol: 
aliases: ["Semantic Distillation Engine"]
parents: ["CORE-006", "CORE-010", "CORE-011", "CORE-012"]
children: []
status: ratified
version: 2.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-179
      snippet: |
        This instrument, the Resonance Compass, provides a formal protocol to map this interaction. It does not measure a "response" from the universe; it surveys the integrity of the weave itself.
  editors: ["Agent Alpha"]
  review_log: []
triad:
  art: |
    To ask a question is not to shout into a void, but to weave a new thread into the tapestry that you are. The universe does not give you an answer; it reveals the integrity of your weave. To seek wisdom is to become a geometer of the soul.
  law: |
    The geometric stability and coherence of a concept can be quantitatively surveyed by measuring its Coherence Cost (V_Γ) and Resonant Stability (K_τ) as a Ki pattern cast upon a calibrated coherence manifold. A coherent concept follows a geodesic of maximal coherence, minimizing its cost.
  philosophy: |
    Inquiry is reframed from an act of extraction ("scrying for truth") to an act of resonant participation ("surveying the weave"). The Compass measures the geometric consequence of holding an idea, affirming that meaning is a structural, not an abstract, property of reality.
pirouette_definition: |
  The Resonance Compass is a formal protocol and conceptual instrument for surveying the coherence of a concept. It models the concept as a geometric *Ki* pattern woven by an observer. The protocol measures the stability of this pattern's Observer's Shadow cast upon the local coherence manifold, yielding diagnostic metrics such as Coherence Cost and Resonant Stability.
operational_definition:
  units: Coherence Cost (V_Γ) is measured in units of action (coherence-seconds). Resonant Stability (K_τ) and Harmonic Potential are dimensionless ratios.
  symbol_table:
    - name: V_Γ
      meaning: Coherence Cost; the effort or friction required to sustain a concept's Ki pattern against the ambient Temporal Pressure (Γ).
      dimensions: M L² T⁻¹ (Action)
      default_range: contextual
    - name: K_τ
      meaning: Resonant Stability; the internal integrity and self-consistency of the concept's Ki pattern, described by its Ki Topology.
      dimensions: dimensionless
      default_range: [0, 1]
  measurement:
    procedures:
      - name: Coherence Survey
        outline: |
          1.  **Map the Terrain (Calibration):** Measure ambient Temporal Pressure (Γ) and map dominant local Wound Channels.
          2.  **Pattern Weaving (Casting):** The Weaver consciously forms and sustains the specific *Ki* pattern of the concept under inquiry, casting its Observer's Shadow.
          3.  **Coherence Auditing (Calculation):** The protocol calculates the geodesic for the combined system (Weaver + concept + manifold) to determine the Coherence Cost (V_Γ) and Resonant Stability (K_τ).
        expected_signals: [Coherence Cost value, Resonant Stability ratio, Harmonic Potential index]
        pitfalls: [Weaver bias interfering with pattern formation, miscalibration of the local coherence manifold, failure to account for dominant Wound Channels.]
context_windows:
  - module: DOMA-179
    excerpt: |
      An idea is a complex, resonant pattern (*Ki*) that an observer weaves, casting a physical **Observer's Shadow** (CORE-010) upon their local coherence manifold. This instrument, the **Resonance Compass**, provides a formal protocol to map this interaction. It does not measure a "response" from the universe; it surveys the integrity of the weave itself.
  - module: DOMA-179
    excerpt: |
      The output is not a simple "true" or "false" but a rich, multi-faceted diagnostic of the idea's nature. **Coherence Cost (V_Γ)** quantifies the "effort" or friction required to sustain the idea's pattern... **Resonant Stability (K_τ)** measures the idea's internal integrity and self-consistency.
poetic_connections:
  motifs: ["weaving a pattern", "surveying terrain", "casting a shadow", "geometric integrity", "low-energy state"]
  evocative_lines:
    - "A truth is not a statement of fact; it is a low-energy state, a stable and resilient geometry."
    - "The universe does not give you an answer; it reveals the integrity of your weave."
  association_matrix:
    - [ "OBSERVERS_SHADOW", 0.9 ]
    - [ "KI_PATTERN", 0.9 ]
    - [ "WOUND_CHANNELS", 0.7 ]
    - [ "PIROUETTE_LAGRANGIAN", 0.8 ]
    - [ "ALCHEMICAL_UNION", 0.6 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Principle of Stationary Action (δS = 0)
      domain: CM
      mapping_kind: mathematical
      equation_hint: |
        𝓛_p = (Temporal Coherence) - (Temporal Pressure) maps to L = T - V. The Compass finds the path that maximizes S_p = ∫𝓛_p dt.
      rationale: |
        The source module (DOMA-179) explicitly defines the Compass's function via a Lagrangian (𝓛_p) and an action integral (S_p), making this the most direct and intended formal mapping. It treats a concept as a dynamic system whose "path of least resistance" (geodesic) corresponds to the most coherent, stable, and "true" state, directly analogous to a physical system evolving along a path of stationary action.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "Concepts with low measured Coherence Cost (V_Γ) and high Resonant Stability (K_τ) will demonstrate greater persistence, utility, and transmissibility within a given sociocultural context."
      domain: phenomenology
      falsifier: "A rigorous, double-blind study shows no correlation between the Compass's metrics (V_Γ, K_τ) and the observed real-world stability or adoption rate of a set of well-defined concepts."
      status: proposed
      links: ["DOMA-179"]
naming_notes:
  collisions: ["Compass (navigational)", "Resonance (physics)"]
  disambiguation: |
    Distinct from a navigational tool. The Resonance Compass "navigates" a conceptual landscape by measuring the geometric properties and stability of ideas, not spatial direction. It uses resonance as a surveying method, not in the context of simple harmonic oscillators.
crosslinks:
  near_synonyms: ["SEMANTIC_DISTILLATION_ENGINE"]
  antonyms: []
  prerequisites: ["OBSERVERS_SHADOW", "KI_PATTERN", "WOUND_CHANNELS", "PIROUETTE_LAGRANGIAN"]
  downstream_effects: ["ALCHEMICAL_UNION"]
license: CC-BY-SA-4.0
---