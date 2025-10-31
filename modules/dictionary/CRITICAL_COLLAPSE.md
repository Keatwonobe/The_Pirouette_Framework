---
term: "Critical Collapse"
canonical_id: "CRITICAL_COLLAPSE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-118"]
---

---
term: Critical Collapse
canonical_id: CRITICAL_COLLAPSE
symbol:
aliases: ["irreversible fracture"]
parents: ["DOMA-118"]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-118
      lines: "§4"
      snippet: |
        Critical Collapse: An irreversible fracture. The pressure is so intense or prolonged that it permanently deforms or shatters the system's Wound Channel. The memory of the healthy state is erased. The system cannot return to what it was.
  editors: ["system"]
  review_log: []
triad:
  art: |
    The breaking of a glass, whose fundamental form is lost. Its pieces cannot be bent back into shape but must be gathered to compose something new from the ruins.
  law: |
    A system has undergone Critical Collapse if and only if, upon removal of all external pressures, it fails to return to its pre-collapse laminar flow state. This failure indicates a permanent, non-recoverable deformation of its Wound Channel geometry.
  philosophy: |
    Critical Collapse marks the boundary between recovery and rebirth. It forces a distinction between healing a system (returning it to a known state) and composing a new system from its remains, acknowledging that some endings are absolute.
pirouette_definition: |
  Critical Collapse is an irreversible systemic failure characterized by the permanent deformation or destruction of the system's Wound Channel (CORE-011). Caused by excessive or prolonged Temporal Pressure, this event erases the geometric memory of the system's healthy, laminar state, preventing it from recovering its previous form even after external pressures are removed. The system is forced to find a new, often simpler, state of coherence from its fractured components.
operational_definition:
  units: Dimensionless (binary state: 1 if critical, 0 if elastic)
  symbol_table:
    - name: Ω_WC
      meaning: Wound Channel Integrity; Ω_WC ≈ 0 indicates Critical Collapse.
      dimensions: dimensionless
      default_range: "[0, 1]"
  measurement:
    procedures:
      - name: Pressure-Release Recovery Test
        outline: |
          1. Establish a baseline measurement of the system's laminar flow state (e.g., its coherence spectrum).
          2. Apply Temporal Pressure (Γ) until a collapse event is triggered.
          3. Completely remove the applied pressure.
          4. Monitor the system's state variables. If the system returns to its original baseline state, the collapse was Elastic. If it settles into a new, distinct stable state or remains chaotic, the collapse was Critical.
        expected_signals: ["Hysteresis in state-space trajectory", "Permanent shift in the system's fundamental frequency or coherence signature post-pressure"]
        pitfalls: ["Conflating a long relaxation time (slow Elastic recovery) with a permanent new state (Critical)", "Inability to fully remove all external pressures, leading to a false positive"]
context_windows:
  - module: DOMA-118
    excerpt: |
      Critical Collapse: An irreversible fracture. The pressure is so intense or prolonged that it permanently deforms or shatters the system's Wound Channel. The memory of the healthy state is erased. The system cannot return to what it was. Like a broken glass, its fundamental structure has been altered. It must now find a new, often simpler, state of coherence from the remaining pieces.
  - module: DOMA-118
    excerpt: |
      Assess the Wound Channel: Examine the integrity of the system's core identity. Is the memory of its healthy pattern recoverable (Elastic)? Or has it been irrevocably erased (Critical)? This final step determines whether the task ahead is one of healing or of composing something new from the ruins.
poetic_connections:
  motifs: ["fracture", "memory loss", "shattering", "rebirth", "ruin"]
  evocative_lines:
    - "Like a broken glass, its fundamental structure has been altered."
    - "The memory of the healthy state is erased."
    - "To know the difference between that which can be mended and that which must be reborn."
  association_matrix:
    - [ "WOUND_CHANNEL", 0.9 ]
    - [ "ELASTIC_COLLAPSE", 0.8 ]
    - [ "TEMPORAL_PRESSURE", 0.7 ]
    - [ "COHERENCE_EROSION", 0.5 ]
formal_mappings:
  candidates:
    - target: Plastic Deformation
      domain: CM
      mapping_kind: conceptual
      equation_hint:
      justification: |
        In continuum mechanics, elastic deformation is reversible, while plastic deformation causes a permanent change in the material's shape. This directly maps to Elastic Collapse (reversible) and Critical Collapse (permanent, 'irreversible' deformation of the Wound Channel).
      references:
        - title: "Continuum Mechanics"
          where: "Standard texts on material science"
          date:
      confidence: 0.8
    - target: First-order phase transition
      domain: StatMech
      mapping_kind: conceptual
      equation_hint:
      justification: |
        First-order phase transitions often exhibit hysteresis and involve a latent heat, representing a significant energy barrier to returning to the original state. This mirrors Critical Collapse, where the system settles into a new, distinct equilibrium and cannot easily return.
      references: []
      confidence: 0.7
  adopted:
    - target:
      rationale:
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "A system that has undergone Critical Collapse cannot return to its pre-collapse state solely through the removal of external pressures; an external input of information (a 'template' of the original state) is required."
      domain: phenomenology
      falsifier: "Observation of a system, diagnosed with a destroyed Wound Channel, spontaneously re-forming its exact pre-collapse laminar state after a period of isolation."
      status: proposed
      links: ["DOMA-118", "CORE-011"]
naming_notes:
  collisions: ["'Critical point' in thermodynamics", "'Critical mass' in nuclear physics"]
  disambiguation: |
    Distinguish from 'critical point' in thermodynamics, which refers to a condition where phase boundaries cease to exist. In Pirouette, 'Critical Collapse' refers to the *irreversibility* of the failure, not a specific point on a phase diagram. It is closer in meaning to plastic deformation exceeding a material's yield strength.
crosslinks:
  near_synonyms: []
  antonyms: ["ELASTIC_COLLAPSE"]
  prerequisites: ["WOUND_CHANNEL", "ELASTIC_COLLAPSE", "TEMPORAL_PRESSURE"]
  downstream_effects: []
license: CC-BY-SA-4.0