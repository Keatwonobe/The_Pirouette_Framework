---
term: "Brittle Rupture"
canonical_id: "BRITTLE_RUPTURE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-131"]
---

---
term: Brittle Rupture
canonical_id: BRITTLE_RUPTURE
symbol:
aliases: [Sudden Shattering, Catastrophic Failure]
parents: [DOMA-131, DYNA-001]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-131
      lines: "L93-L98"
      snippet: |
        **Brittle Rupture (The Sudden Shattering):**
        This occurs in systems that appear stable and highly ordered (`Laminar Flow`) but possess a rigid, unadaptive `Kτ` pattern. When faced with a sudden, sharp increase in `Γ`, the system cannot deform or adapt. It maintains its coherence perfectly until the moment it fails completely and catastrophically.
  editors: [System Agent]
  review_log: []
triad:
  art: |
    The shattering of a perfect, silent form. A sudden crack across a frozen lake, revealing the violent pressure hidden beneath a placid surface. It is the failure of a system that mistakes rigidity for strength.
  law: |
    A system with high temporal coherence (`Kτ`) but low adaptability (`∂Kτ/∂Γ ≈ 0`) will fail catastrophically when subjected to a temporal pressure gradient (`∂Γ/∂t`) that exceeds its elastic limit, transitioning directly from `Laminar Flow` to total decoherence without a preceding turbulent phase.
  philosophy: |
    Brittle Rupture teaches that true resilience is not static perfection but dynamic adaptability. Systems that optimize for unchanging order become fragile, sacrificing the capacity to bend for the illusion of being unbreakable.
pirouette_definition: |
  A mode of `Systemic Rupture` characterized by the catastrophic failure of a highly-ordered system (`Laminar Flow`) with a rigid, unadaptive coherence pattern (`Kτ`). The system shows no significant deformation or turbulent degradation before failure, collapsing suddenly and completely when a sharp increase in `Temporal Pressure` (`Γ`) exceeds its structural capacity. This is the failure mode of systems that cannot bend and therefore must break.
operational_definition:
  units: Dimensionless (classification category)
  symbol_table:
    - name: Kτ
      meaning: Temporal Coherence; a system's capacity for stable resonance.
      dimensions: Context-dependent (often energy or information rate)
      default_range: contextual
    - name: Γ
      meaning: Temporal Pressure; environmental stress acting on a system.
      dimensions: Inverse of Kτ dimensions
      default_range: contextual
    - name: ∂Γ/∂t
      meaning: Temporal Pressure Gradient; the rate of change of stress.
      dimensions: [Γ]/T
      default_range: contextual
  measurement:
    procedures:
      - name: Rupture Mode Classification
        outline: |
          1. Establish a baseline measurement of the system's flow state, confirming `Laminar Flow`.
          2. Characterize the system's coherence adaptability by measuring the change in `Kτ` in response to small, slow increases in `Γ`. A brittle system exhibits `∂Kτ/∂Γ ≈ 0`.
          3. Apply a controlled, high-gradient pulse of `Temporal Pressure` (`∂Γ/∂t >> 0`).
          4. Monitor for a phase transition. A sudden, catastrophic drop in all coherence metrics without a preceding turbulent phase confirms Brittle Rupture.
        expected_signals: [Stable `Laminar Flow` metrics, a large positive spike in `∂Γ/∂t`, a discontinuous drop in `Kτ` to near-zero.]
        pitfalls: [Applying the pressure gradient too slowly, allowing the system to adapt or fail ductilely. Misinterpreting measurement noise as a turbulent precursor.]
context_windows:
  - module: DOMA-131
    excerpt: |
      **Brittle Rupture (The Sudden Shattering):**
      This occurs in systems that appear stable and highly ordered (`Laminar Flow`) but possess a rigid, unadaptive `Kτ` pattern. When faced with a sudden, sharp increase in `Γ`, the system cannot deform or adapt. It maintains its coherence perfectly until the moment it fails completely and catastrophically.
      *   *Manifestations:* A glass shattering, a sudden stock market crash, a seemingly stable relationship ending without warning.
  - module: DOMA-131
    excerpt: |
      A rupture is not an instantaneous event but a self-propagating process. It unfolds in three distinct stages: Coherence Strain (The Bending), The Yield Point (The Tearing), and The Cascade (The Unraveling). In a Brittle Rupture, the "Coherence Strain" phase is minimal or non-existent; the system proceeds almost directly from a stable state to the Yield Point and subsequent Cascade.
poetic_connections:
  motifs: [glass shattering, ice cracking, silent tension, sudden collapse, rigidity, fragility]
  evocative_lines:
    - "the sound a string makes right before it snaps."
    - "It maintains its coherence perfectly until the moment it fails completely and catastrophically."
    - "The system can no longer bend; it must break."
  association_matrix:
    - [ "LAMINAR_FLOW", 0.9 ]
    - [ "TEMPORAL_PRESSURE", 0.8 ]
    - [ "WOUND_BOUNDARY", 0.7 ]
    - [ "DUCTILE_RUPTURE", 0.2 ]
formal_mappings:
  candidates:
    - target: Brittle Fracture
      domain: CM
      mapping_kind: conceptual
      equation_hint: |
        σ_f > σ_y  (Fracture stress is reached before yield stress)
      justification: |
        This is a direct conceptual mapping. Brittle fracture in materials science is defined by failure under stress with little to no preceding plastic deformation. The Pirouette model's Brittle Rupture extends this concept to any system (social, economic, informational) that exhibits high order but low adaptability, failing catastrophically under a sudden shock.
      references:
        - title: Materials Science and Engineering: An Introduction
          where: Chapter 8: Failure
          date: 2018-01-16
      confidence: 0.9
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "A system with a demonstrably rigid `Kτ` pattern (i.e., low adaptability) will always fail via Brittle Rupture when subjected to a sufficiently high Temporal Pressure Gradient (`∂Γ/∂t`)."
      domain: phenomenology
      falsifier: "The discovery of a system with a pre-identified rigid `Kτ` that consistently undergoes a turbulent, ductile-like degradation before collapse when exposed to a high `∂Γ/∂t` event. This would falsify the direct causal link between rigidity and this specific failure mode."
      status: proposed
      links: [DOMA-131]
naming_notes:
  collisions: [Fracture, Failure, Collapse]
  disambiguation: |
    Distinguish from `Ductile Rupture`, which is preceded by a visible, chaotic degradation (`Turbulent Flow`). Also distinguish from `Fatigue Rupture`, which results from the accumulation of damage from repeated *sub-critical* stress cycles, not a single overwhelming event.
crosslinks:
  near_synonyms: []
  antonyms: [DUCTILE_RUPTURE, ADAPTIVE_RESONANCE]
  prerequisites: [SYSTEMIC_RUPTURE, LAMINAR_FLOW, TEMPORAL_PRESSURE]
  downstream_effects: [WOUND_BOUNDARY]
license: CC-BY-SA-4.0