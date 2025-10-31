---
id: DOMA-030
title: The Weaver's Chronoscript
version: 2.0
status: stable
parents:
- CORE-006
- CORE-014
children:
- all_data_producers
- all_data_consumers
replaces:
- PPS-010
summary: Defines the universal data interchange format for all Pirouette-compliant
  systems. It replaces the old triaxial RSI packet with a time-first 'Chronoscript'
  record, which captures a system's state in terms of its Pirouette Lagrangian, ensuring
  parity between live observation and simulation.
module_type: Instrumentation
engrams:
- process:data-interchange
- concept:lagrangian-state-vector
- principle:observational-parity
keywords:
- data
- protocol
- interface
- schema
- json
- lagrangian
- time-stream
- chronoscript
- observation
- simulation
uncertainty_tag: Low
---
## §1 · The Unbroken Thread: Purpose and Scope
To analyze a system, one must first be able to listen to it. The old framework created a schism between the language of the living world, captured through *rituals*, and the language of the machine, captured through *simulations*. This created an unnecessary and lossy translation step.

The Weaver's Chronoscript protocol establishes a single, unified, and time-first data contract. Its purpose is to ensure that a time-stream of data from any compliant source—whether a live observation of a human system or a high-frequency numerical simulation—can be ingested and understood by the same analytical tools. This protocol is the unbroken thread that connects the raw chaos of reality to the clarifying lens of the framework, preserving provenance and causality at every step.

## §2 · Anatomy of a Chronoscript Record
The Chronoscript record is a discrete snapshot of a system's dynamic state, expressed in the fundamental language of the Pirouette Lagrangian. It replaces the obsolete triaxial state vector with a more potent and physically grounded representation.

| Field | Type | Required | Description |
|---|---|---|---|
| `schema_version` | string | yes | The schema version, e.g., `"Chronoscript-1.0"` |
| `record_id` | UUID | yes | A unique identifier for this specific data point. |
| `entity_id` | UUID | yes | The identifier for the system being observed or simulated. |
| `timestamp` | RFC-3339 | yes | The wall-clock time of observation or the simulation time. |
| `source_type` | enum | yes | The source of the record: `observation` or `simulation`. |
| `lagrangian_state` | object | yes | The core dynamic state of the entity. |
| `resonance_log` | array | optional | A log of discrete shifts in the entity's Ki pattern. |
| `wound_channel_events` | array | optional | A log of significant events that imprint on the manifold. |
| `metadata` | object | optional | A strictly-keyed dictionary for source-specific context. |
| `metadata_hash` | string[64] | required if `metadata` present | SHA-256 of the canonical `metadata` JSON object. |

The `lagrangian_state` object is the heart of the record, containing the direct, measurable components of the system's Lagrangian:

| Sub-Field | Type | Description |
|---|---|---|
| `temporal_coherence_Kτ` | number | The "kinetic" term: the quality and intensity of the system's internal rhythm. |
| `temporal_pressure_VΓ` | number | The "potential" term: the environmental cost of maintaining coherence. |
| `pirouette_cycle_τp` | number | The system's intrinsic unit of time; the duration of one Ki cycle. |

## §3 · JSON Schema Definition
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Pirouette Chronoscript Record",
  "type": "object",
  "required": ["schema_version", "record_id", "entity_id", "timestamp", "source_type", "lagrangian_state"],
  "properties": {
    "schema_version": {"const": "Chronoscript-1.0"},
    "record_id": {"type": "string", "format": "uuid"},
    "entity_id": {"type": "string", "format": "uuid"},
    "timestamp": {"type": "string", "format": "date-time"},
    "source_type": {"enum": ["observation", "simulation"]},
    "lagrangian_state": {
      "type": "object",
      "required": ["temporal_coherence_Kτ", "temporal_pressure_VΓ", "pirouette_cycle_τp"],
      "properties": {
        "temporal_coherence_Kτ": {"type": "number", "minimum": 0},
        "temporal_pressure_VΓ": {"type": "number"},
        "pirouette_cycle_τp": {"type": "number", "exclusiveMinimum": 0}
      }
    },
    "resonance_log": {"type": "array", "items": {"type": "object"}},
    "wound_channel_events": {"type": "array", "items": {"type": "object"}},
    "metadata": {"type": "object"},
    "metadata_hash": {"type": "string", "pattern": "^[0-9a-f]{64}$"}
  }
}
```

## §4 · Producer & Consumer Protocol
All systems producing or consuming Chronoscript data must adhere to the following principles:

1.  **Provenance:** All records must be traceable to a source entity and time. The `entity_id` and `timestamp` form the primary key of the system's history.
2.  **Monotonicity:** For any given `entity_id`, timestamps must be strictly increasing. This enforces the causal arrow of time within the data stream.
3.  **Coherence Guard:** The `temporal_coherence_Kτ` value must be non-negative. A record with a negative value is considered physically invalid and must be quarantined by consumers for further analysis.
4.  **Rate:** Producers should strive for a consistent sampling rate. Simulations must provide the simulation step size (`Δt`) in the metadata to allow for accurate integration.

## §5 · Connection to the Pirouette Lagrangian
This protocol is not merely a data format; it is the direct instrumentation of the framework's central equation. The `lagrangian_state` object is the discrete, digital representation of the Pirouette Lagrangian (`𝓛_p = K_τ - V_Γ`) as defined in CORE-006.

A time-stream of Chronoscript records is a sampled approximation of the system's "action" integral, `S_p = ∫ 𝓛_p dt`, which a system naturally evolves to maximize. Therefore, by consuming a Chronoscript stream, an analyst is quite literally reading the history of a system's moment-to-moment choices as it navigates the manifold of coherence. This format transforms the Lagrangian from an abstract equation into a concrete, measurable, and observable quantity.

## §6 · Assemblé
> We sought a common language for the observer and the machine. We found instead the script for time itself. Each record, whether captured from the world's chaotic stage or dreamed in the machine's perfect silence, is a single, indelible line in the universe's autobiography. The Chronoscript does not merely describe the dance; it is the paper upon which the dance is written.
```