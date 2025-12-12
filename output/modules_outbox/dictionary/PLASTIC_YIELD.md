---
term: "Plastic Yield"
canonical_id: "PLASTIC_YIELD"
symbol: ""
aliases: [Transformative Flow]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-199"]
---

---
term: Plastic Yield
canonical_id: PLASTIC_YIELD
symbol: Ki → K'i
aliases: [Transformative Flow]
parents: [DOMA-199]
children: []
status: ratified
version: 2.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-199
      lines: "§3"
      snippet: |
        Plastic Yield (Transformative Flow): The pressure is too great or too sustained for the original form to be recovered. The system is forced to abandon its old Ki and discover a new, permanently altered state of resonance that is stable at the higher Γ. It finds a new, quieter song.
  editors: [System]
  review_log: []
triad:
  art: |
    A system, asked a question it cannot answer with its old voice, learns a new, quieter song. Its form becomes a memory of the pressure that taught it to sing differently. A scar is not a mark of damage, but of a choice made to survive.
  law: |
    When a system under Temporal Pressure (Γ) undergoes a state transition (Ki → K'i) and does not revert to its initial state Ki upon removal of Γ, it has undergone Plastic Yield. The new state K'i will have a distinct resonant signature and typically a lower Coherence Budget (Kτ).
  philosophy: |
    Plastic Yield represents survival through irreversible transformation. It is the framework's model for how systems learn, scar, and evolve, demonstrating that identity is not a static property but a negotiated, flowing state that can be permanently altered by experience.
pirouette_definition: |
  The irreversible phase transition of a system under sustained Temporal Pressure (Γ) where the environmental coherence cost (V_Γ) forces it to abandon its initial resonant identity (Ki) for a new, stable, and permanently altered form (K'i). This new state, or 'Transformative Flow', represents a new path of maximal coherence, often at a lower overall Coherence Budget (Kτ), that is sustainable under the new environmental conditions.
operational_definition:
  units: Process
  symbol_table:
    - name: Ki → K'i
      meaning: A transition from an initial resonant identity (Ki) to a new, permanently altered identity (K'i).
      dimensions: Dimensionless (state transition)
      default_range: N/A (represents a discrete event)
  measurement:
    procedures:
      - name: Stress-Return Cycle Test
        outline: |
          1. Characterize the system's initial resonant identity (Ki) and Coherence Budget (Kτ) using Flow Diagnostics (DYN-001).
          2. Apply a controlled, increasing Temporal Pressure (Γ), such as mechanical load or informational complexity.
          3. Monitor the system's state response throughout the loading.
          4. Remove the pressure Γ completely.
          5. Re-measure the system's resonant identity. If the final identity (K'i) is measurably different from the initial (Ki), Plastic Yield has occurred.
        expected_signals: [A permanent shift in the system's primary resonant frequencies, Hysteresis in the pressure-response curve, A measurable decrease in the post-yield Coherence Budget Kτ.]
        pitfalls: [Failing to distinguish from slow elastic recovery (viscoelasticity/creep), Misidentifying chaotic noise from an incipient fracture as a new stable state.]
context_windows:
  - module: DOMA-199
    excerpt: |
      **Plastic Yield (Transformative Flow):** The pressure is too great or too sustained for the original form to be recovered. The system is forced to abandon its old Ki and discover a new, permanently altered state of resonance that is stable at the higher Γ. It finds a new, quieter song. The old identity is irrevocably changed, and it settles into a new, often degraded, laminar flow.
  - module: DOMA-199
    excerpt: |
      **Transform (Plastic)** | New Laminar (Degraded) | The system has permanently changed. It survived the stress but is scarred and operates at a lower level of coherence. | Is the system adaptable? When its primary strategy fails, can it find a new way to be, or is its only other option failure?
poetic_connections:
  motifs: [scarring, irreversible change, survival-as-transformation]
  evocative_lines:
    - "A scar is not a mark of damage, but the memory of a choice made under pressure."
    - "It finds a new, quieter song."
  association_matrix:
    - [ "FRACTURE", 0.7 ]
    - [ "ELASTIC_YIELD", 0.6 ]
    - [ "TEMPORAL_PRESSURE", 0.9 ]
    - [ "COHERENCE_BUDGET", 0.8 ]
formal_mappings:
  candidates:
    - target: Plastic deformation
      domain: CM
      mapping_kind: conceptual
      equation_hint: |
        σ > σ_y (Stress exceeds yield strength)
      justification: |
        Plastic Yield in the Pirouette Framework is a direct generalization of plastic deformation in materials science. The concept extends the physical model of irreversible changes in a material's microstructure (e.g., dislocation motion) to any system—psychological, social, or ecological—that changes its fundamental structure to accommodate stress.
      references:
        - title: Mechanics of Materials
          where: Chapter 2: Stress and Strain
          date: 2020-01-01
      confidence: 0.95
  adopted:
    - target: Plastic Deformation (Continuum Mechanics)
      rationale: The term and operational behavior are a deliberate generalization of the well-understood concept in materials science, providing a powerful physical anchor for its application to non-physical systems.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "Any system that survives a stress exceeding its elastic limit without fracturing must exhibit a measurable, permanent change in its state variables, defining a new identity K'i."
      domain: phenomenology
      falsifier: "Observing a system that repeatedly endures stress well beyond its identifiable elastic limit but consistently returns to its exact original state (Ki) without any evidence of hysteresis, energy dissipation, or structural change. This would violate the coherence cost model."
      status: supported
      links: [DOMA-199]
naming_notes:
  collisions: [Yield (finance), Yield (traffic)]
  disambiguation: |
    Distinct from 'yield' as a rate of return (finance) or 'yielding' as social deference. In Pirouette, Yield is always a dynamic response to pressure on a system's form, categorized as elastic (temporary recovery) or plastic (permanent transformation).
crosslinks:
  near_synonyms: [TRANSFORMATIVE_FLOW]
  antonyms: [ELASTIC_YIELD, RESILIENCE]
  prerequisites: [TEMPORAL_PRESSURE, COHERENCE_BUDGET, PIROUETTE_LAGRANGIAN]
  downstream_effects: [FRACTURE, COHERENCE_DEGRADATION]
license: CC-BY-SA-4.0
---

# Plastic Yield

## Canonical (Pirouette)
The irreversible phase transition of a system under sustained Temporal Pressure (Γ) where the environmental coherence cost (V_Γ) forces it to abandon its initial resonant identity (Ki) for a new, stable, and permanently altered form (K'i). This new state, or 'Transformative Flow', represents a new path of maximal coherence, often at a lower overall Coherence Budget (Kτ), that is sustainable under the new environmental conditions.

## EFT-First Summary
Plastic Yield is the Pirouette Framework's generalization of plastic deformation from continuum mechanics. It describes any irreversible change in a system's structure caused by stress exceeding its elastic limit. This is modeled as a transition to a new stable state (`K'i`) when the "coherence cost" of maintaining the original form becomes unsustainable, forcing the system to find a new, permanently altered configuration that can stably accommodate the pressure.

## Glossary Links
- See also: Elastic Yield, Fracture, Temporal Pressure, Coherence