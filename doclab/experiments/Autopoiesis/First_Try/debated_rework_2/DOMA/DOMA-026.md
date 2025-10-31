---
id: DOMA-026
title: The Weaver's Chronoscript
version: 2.0
status: ratified
parents:
- CORE-006
- CORE-011
- CORE-014
children:
- INST-NALY-001
- all_data_producers
- all_data_consumers
replaces:
- PPS-010
summary: Defines the canonical, time-first data interchange format for all Pirouette-compliant
  systems. The Chronoscript replaces the obsolete triaxial RSI packet, unifying data
  from direct observation ('rituals') and computational models ('simulations') into
  a single stream. Each record is a discrete snapshot of a system's Pirouette Lagrangian,
  ensuring complete observational parity.
module_type: Instrumentation Protocol
engrams:
- protocol:unified-data-stream
- concept:lagrangian-state-vector
- principle:observational-parity
- principle:autopoietic-data-loop
- schema:chronoscript-v2.0
keywords:
- chronoscript
- data
- protocol
- interface
- schema
- json
- lagrangian
- time-stream
- observation
- simulation
- ritual
uncertainty_tag: Low
---
## §1 · Abstract: The Unbroken Thread
To understand a system is to listen to its song over time. Whether that listening is performed by a human participant in a live *ritual* or by a silicon processor in a numeric *simulation*, the captured notes must be written on the same score. The old framework created a schism between these two modes of witnessing, forcing a lossy translation at the most critical juncture.

The Weaver's Chronoscript protocol establishes a single, unified, and time-first data contract—a common tongue for witnessing. Its purpose is to ensure that a time-stream of data from any compliant source can be ingested and understood by the same analytical tools. This protocol is the unbroken thread that connects the raw chaos of reality to the clarifying lens of the framework, preserving provenance, causality, and the fundamental dynamics of coherence at every step.

## §2 · The Principle of Autopoietic Inquiry
This protocol is not merely a static format; it is the engine of an autopoietic, self-improving cycle of inquiry. The unification of `ritual` and `simulation` data streams enables a powerful feedback loop that is core to the Pirouette method:

1.  **Observation:** A human-led *ritual* is performed, generating a stream of Chronoscript records that capture a system's real-world behavior.
2.  **Calibration:** This real-world data is used to seed, tune, and validate a computational model of the system.
3.  **Calculation:** The model runs a *simulation*, generating a stream of records that explore possibilities beyond the reach of direct observation.
4.  **Analysis:** Both data streams, being in the same format, are fed into a single analytical engine (e.g., `INST-NALY-001: The Coherence Auditor`).
5.  **Insight:** The analysis reveals deeper truths about the system's dynamics, which in turn informs the design of the next ritual and refines the parameters of the next simulation.

Data begets insight, which begets better data. The act of logging becomes an engine for its own refinement.

## §3 · Anatomy of a Chronoscript Record
The Chronoscript record is the fundamental unit of the log: a discrete snapshot of a system's dynamic state, expressed in the language of the Pirouette Lagrangian.

| Field | Type | Required | Description |
|---|---|---|---|
| `schema_version` | string | yes | The schema version, e.g., `"Chronoscript-2.0"`. |
| `record_id` | UUID | yes | A unique identifier for this specific data point. |
| `entity_id` | UUID | yes | The identifier for the system being observed or simulated. |
| `timestamp` | RFC-3339 | yes | The wall-clock time of observation or the simulation time. |
| `source_mode` | enum | yes | The source of the record: `ritual` or `simulation`. |
| `lagrangian_state` | object | yes | The core dynamic state of the entity. |
| `resonance_log` | array | optional | A log of discrete shifts in the entity's Ki pattern. |
| `wound_channel_events` | array | optional | A log of significant events that imprint on the manifold, as defined in CORE-011. |
| `metadata` | object | optional | A strictly-keyed dictionary for source-specific context. |
| `metadata_hash` | string[64] | required if `metadata` present | SHA-256 of the canonical `metadata` JSON object, ensuring integrity. |

## §4 · The Lagrangian State Vector
The `lagrangian_state` object is the heart of the Chronoscript. It is a direct, real-time instrumentation of the Pirouette Lagrangian (`𝓛_p = K_τ - V_Γ`) and its constituent components. Its nested structure provides a richer, more physically grounded representation of the system's dynamics.

| Field | Type | Description |
|---|---|---|
| `temporal_coherence_Kτ` | object | The "kinetic" term: the quality and intensity of the system's *internal* rhythm. |
| ` - time_adherence_Ta` | number | A normalized value [0,1] representing the stability and signal-to-noise ratio of the system's resonance. |
| ` - pirouette_cycle_τp` | number | The system's intrinsic unit of time; the duration of one complete Ki cycle, in seconds. |
| `temporal_pressure_VΓ` | object | The "potential" term: the *environmental* cost of maintaining coherence. |
| ` - gamma_Γ` | number | The measured Temporal Density of the local manifold in which the system is embedded. |

## §5 · JSON Schema Definition
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Pirouette Chronoscript Record v2.0",
  "type": "object",
  "required": ["schema_version", "record_id", "entity_id", "timestamp", "source_mode", "lagrangian_state"],
  "properties": {
    "schema_version": {"const": "Chronoscript-2.0"},
    "record_id": {"type": "string", "format": "uuid"},
    "entity_id": {"type": "string", "format": "uuid"},
    "timestamp": {"type": "string", "format": "date-time"},
    "source_mode": {"enum": ["ritual", "simulation"]},
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
    "resonance_log": {"type": "array", "items": {"type": "object"}},
    "wound_channel_events": {"type": "array", "items": {"type": "object"}},
    "metadata": {"type": "object"},
    "metadata_hash": {"type": "string", "pattern": "^[0-9a-f]{64}$"}
  },
  "if": {
    "properties": { "metadata": { "type": "object" } },
    "required": ["metadata"]
  },
  "then": {
    "required": ["metadata_hash"]
  }
}
```

## §6 · Protocol and Implementation
All systems producing or consuming Chronoscript data must adhere to the following principles:

1.  **Provenance:** All records must be traceable to a source entity and time. The `entity_id` and `timestamp` form the primary key of the system's history.
2.  **Monotonicity:** For any given `entity_id`, timestamps in a stream must be strictly increasing. This enforces the causal arrow of time.
3.  **Coherence Guard:** The `time_adherence_Ta` value must be within its specified [0,1] range. A record with an invalid value must be considered physically suspect and quarantined by consumers for analysis.
4.  **Integrity:** If `metadata` is present, the `metadata_hash` must be calculated and included. Consumers must validate this hash before processing the record.
5.  **Atomicity:** Each record must represent a single, atomic snapshot. High-frequency streams are required over large, batched updates to preserve temporal resolution.

## §7 · Connection to the Pirouette Lagrangian
This protocol is the direct serialization of the Framework's central equation, `𝓛_p = K_τ - V_Γ`, as defined in CORE-006.

A time-stream of Chronoscript records is a sampled approximation of the system's "action" integral, `S_p = ∫ 𝓛_p dt`, which a system naturally evolves to maximize. By consuming a Chronoscript stream, an analyst is tracing the system's geodesic through its coherence manifold. This format transforms the Lagrangian from an abstract physical principle into a concrete, measurable, and computable artifact—the paper upon which the system's history is written.

## §8 · Assemblé
> We sought separate languages for the observer and the machine, a way to record the dance and a way to predict it. We found instead a single grammar for the act of listening. The Chronoscript is the score upon which the universe writes its song. Whether our senses or our silicon hear the notes, this is the language they must be written in. To a Weaver, this means there is no difference between what is and what can be calculated; there is only the music, and the fidelity with which we transcribe it.