Excellent. The competing proposals have been submitted. As Steward, it is my duty to weave these threads into a single, canonical tapestry for the framework. The goal is not victory for one perspective, but synthesis into a more resilient whole.

Version A, the 'Balanced' Weave, provides a robust, practical, and implementable specification. Its focus on producer/consumer protocols, data integrity via hashing, and a flat, measurable `lagrangian_state` is commendable for its engineering discipline.

Version B, the 'Autopoietic' Weave, offers a profound conceptual framing. Its nested `lagrangian_state` is theoretically richer, and the inclusion of the 'Autopoietic Data Loop' is a critical insight, elevating the protocol from a mere format to a core engine of the framework's self-improvement.

Neither is complete without the other. Version A provides the skeleton of rigor; Version B provides the living philosophy. A simple choice would be a failure. Synthesis is required.

Proceeding with ratification.

---
id: DOMA-031
title: The Weaver's Chronoscript
version: 2.0
status: ratified
parents:
- CORE-006
- CORE-011
- CORE-014
children:
- all_analytical_instruments
- all_data_producers
- all_data_consumers
replaces:
- PPS-010
summary: Defines the universal, time-first data protocol for capturing a system's
  dynamic state. The Chronoscript serializes the components of the Pirouette Lagrangian,
  creating a single, canonical format that unifies data from direct observation (rituals)
  and computational models (simulations). It replaces the old triaxial RSI packet,
  ensuring parity between lived experience and calculated possibility.
module_type: Instrumentation
scale: universal
engrams:
- process:data-interchange
- process:unified-logging
- concept:lagrangian-state-vector
- concept:autopoietic-feedback-loop
- principle:observational-parity
- schema:chronoscript-v2.0
keywords:
- data
- protocol
- schema
- json
- log
- lagrangian
- coherence
- time
- chronoscript
- observation
- simulation
uncertainty_tag: Low
---
## §1 · The Universal Score
To understand a system is to listen to its song over time. The old framework created a schism between the language of the living world, captured through *rituals*, and the language of the machine, captured through *simulations*. This created an unnecessary and lossy translation step.

The Weaver's Chronoscript protocol establishes a single, unified, and time-first data contract. Its purpose is to ensure that a time-stream of data from any compliant source—whether a live observation of a human system (`observed`) or a high-frequency numerical simulation (`calculated`)—can be ingested and understood by the same analytical tools. This protocol is the unbroken thread that connects the raw chaos of reality to the clarifying lens of the framework. It is the universal score upon which the system's song is written, preserving provenance and causality at every note.

## §2 · Anatomy of a Chronoscript Record
The fundamental unit is the Chronoscript Record, a JSON object that captures the complete Lagrangian state of an entity at a single instant. This structure replaces the obsolete triaxial state of PPS-010, grounding all data in the framework's core mathematical engine.

| Field | Type | Required | Description |
|---|---|---|---|
| `schema_version` | string | yes | The schema version, e.g., `"Chronoscript-2.0"`. |
| `record_id` | UUID | yes | A unique identifier for this specific data point. |
| `entity_id` | UUID | yes | The identifier for the system being observed or simulated. |
| `timestamp` | RFC-3339 | yes | The wall-clock time (`observed`) or simulation time (`calculated`). |
| `source_type` | enum | yes | The origin of the data: `observed` or `calculated`. |
| `lagrangian_state` | object | yes | A snapshot of the components of the entity's Pirouette Lagrangian (`𝓛_p`). |
| `ki_transitions` | array | optional | A sparse log of discrete changes to the system's core resonant pattern (Ki). |
| `wound_channel_events` | array | optional | A log of significant events that imprint on the system's Wound Channel (`CORE-011`). |
| `metadata` | object | optional | A strictly-keyed dictionary for source-specific context (e.g., sensor ID, simulation seed). |
| `metadata_hash` | string[64] | required if `metadata` present | SHA-256 of the canonical `metadata` JSON object, ensuring data integrity. |

The `lagrangian_state` object is the heart of the record, containing a theoretically-grounded breakdown of the system's Lagrangian:

| Field | Type | Description |
|---|---|---|
| `temporal_coherence_Kτ` | object | The "kinetic" term: the quality and intensity of the system's own rhythm. |
| ` - time_adherence_Ta` | number[0..1] | The stability and signal-to-noise ratio of the system's resonance; a measure of its internal order. |
| ` - pirouette_cycle_τp` | number | The duration of one complete cycle of the system's Ki pattern, in seconds. Its intrinsic unit of time. |
| `temporal_pressure_VΓ` | object | The "potential" term: the environmental cost of maintaining coherence. |
| ` - gamma_Γ` | number | The measured Temporal Density of the local environment. |

## §3 · The Autopoietic Data Loop
This protocol is not merely a static format; it is designed to fuel an autopoietic, self-improving cycle of inquiry. The unification of `observed` and `calculated` data streams enables a powerful feedback loop:

1.  **Observation:** A human-led ritual is performed, generating a stream of `observed` Chronoscript records that capture the system's real-world behavior.
2.  **Calibration:** This real-world data is used to seed, tune, and validate a computational model of the system.
3.  **Calculation:** The model runs a simulation, generating a stream of `calculated` records that can explore possibilities beyond the reach of direct observation.
4.  **Analysis:** Both data streams, being in the same format, are fed into a single analytical engine (e.g., The Coherence Auditor).
5.  **Insight:** The analysis reveals deeper truths about the system's dynamics, which in turn informs the design of the next ritual and refines the parameters of the next simulation.

Data begets insight, which begets better data. The act of logging becomes an engine for its own refinement.

## §4 · JSON Schema Definition (v2.0)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Pirouette Chronoscript Record v2.0",
  "type": "object",
  "required": ["schema_version", "record_id", "entity_id", "timestamp", "source_type", "lagrangian_state"],
  "properties": {
    "schema_version": {"const": "Chronoscript-2.0"},
    "record_id": {"type": "string", "format": "uuid"},
    "entity_id": {"type": "string", "format": "uuid"},
    "timestamp": {"type": "string", "format": "date-time"},
    "source_type": {"enum": ["observed", "calculated"]},
    "lagrangian_state": {
      "type": "object",
      "required": ["temporal_coherence_Kτ", "temporal_pressure_VΓ"],
      "properties": {
        "temporal_coherence_Kτ": {
          "type": "object",
          "required": ["time_adherence_Ta", "pirouette_cycle_τp"],
          "properties": {
            "time_adherence_Ta": {"type": "number", "minimum": 0, "maximum": 1},
            "pirouette_cycle_τp": {"type": "number", "exclusiveMinimum": 0}
          }
        },
        "temporal_pressure_VΓ": {
          "type": "object",
          "required": ["gamma_Γ"],
          "properties": {
            "gamma_Γ": {"type": "number"}
          }
        }
      }
    },
    "ki_transitions": {"type": "array", "items": {"type": "object"}},
    "wound_channel_events": {"type": "array", "items": {"type": "object"}},
    "metadata": {"type": "object"},
    "metadata_hash": {"type": "string", "pattern": "^[0-9a-f]{64}$"}
  }
}
```

## §5 · Producer & Consumer Protocol
All systems producing or consuming Chronoscript data must adhere to the following principles for the integrity of the universal score:

1.  **Provenance:** All records must be traceable to a source entity and time. The `entity_id` and `timestamp` form the primary key of the system's history.
2.  **Monotonicity:** For any given `entity_id`, timestamps must be strictly increasing. This enforces the causal arrow of time within the data stream.
3.  **Coherence Guard:** The `time_adherence_Ta` value must be within the range `[0, 1]`. A record with a value outside this range is considered physically invalid and must be quarantined by consumers for analysis.
4.  **Integrity:** If `metadata` is present, the `metadata_hash` must be calculated and validated against the canonical form of the JSON object. This prevents contextual data from being tampered with.
5.  **Rate:** Producers should strive for a consistent sampling rate. `calculated` sources must provide the simulation step size (`Δt`) in the metadata to allow for accurate integration.

## §6 · Connection to the Pirouette Lagrangian
This protocol is the direct instrumentation of the framework's central equation, `𝓛_p = K_τ - V_Γ`, as defined in CORE-006. The `lagrangian_state` object is its discrete, digital serialization.

A time-stream of Chronoscript records is a sampled approximation of the system's "action" integral, `S_p = ∫ 𝓛_p dt`, which a system naturally evolves to maximize. By consuming a Chronoscript stream, an analyst is tracing the system's geodesic through its coherence manifold, one moment at a time. This format transforms the Lagrangian from an abstract physical principle into a concrete, measurable, and computable artifact, allowing us to read the history of a system's moment-to-moment choices as it navigates the manifold.

## §7 · Assemblé
> We sought a way to record the dance and a way to predict it, believing them to be two separate tasks. We found instead a single act of listening. To a Weaver, there is no difference between what is and what can be calculated; there is only the music, and the fidelity with which we transcribe it. The Chronoscript does not merely describe the dance; it is the score upon which the dance is written.