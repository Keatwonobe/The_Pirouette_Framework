---
id: DOMA-029
title: The Weaver's Chronoscript
version: 2.0
status: ratified
parents:
- CORE-006
- CORE-011
children:
- all_data_producers
- all_data_consumers
- INST-NALY-001
replaces:
- PPS-010
summary: Defines the universal, time-first data interchange protocol for all Pirouette-compliant
  systems. It replaces the old triaxial RSI packet with a time-first 'Chronoscript'
  record which captures a system's state as a direct snapshot of its Pirouette Lagrangian,
  ensuring parity between live observation (rituals) and computational modeling (simulations).
module_type: Instrumentation
engrams:
- process:unified-data-interchange
- concept:lagrangian-state-vector
- principle:observational-parity
- schema:chronoscript-v2
keywords:
- data
- protocol
- interface
- schema
- json
- lagrangian
- coherence
- time-stream
- chronoscript
- observation
- simulation
- log
uncertainty_tag: Low
---
## §1 · The Unbroken Thread: Purpose and Parity
To analyze a system, one must first be able to listen to it. The old framework created a schism between the language of the living world, captured through *rituals*, and the language of the machine, captured through *simulations*. This created an unnecessary and lossy translation step.

The Weaver's Chronoscript protocol establishes a single, unified, and time-first data contract. Its purpose is to guarantee **Observational Parity**: the principle that human intuition and machine calculation are two equally valid instruments for exploring reality. A time-stream of data from any compliant source—whether a live observation of a human system or a high-frequency numerical simulation—can be ingested and understood by the same analytical tools. This protocol is the unbroken thread that connects the raw chaos of reality to the clarifying lens of the framework, preserving provenance and causality at every step.

## §2 · The Autopoietic Loop
This protocol is not merely a static format; it is designed to fuel an autopoietic, self-improving cycle of inquiry. The unification of `observation` and `simulation` data streams enables a powerful feedback loop:

1.  **Observation:** A human-led ritual is performed, generating a stream of `observation` records that capture the system's real-world behavior.
2.  **Calibration:** This real-world data is used to seed, tune, and validate a computational model of the system.
3.  **Simulation:** The model runs, generating a stream of `simulation` records that explore possibilities beyond the reach of direct observation.
4.  **Analysis:** Both data streams, being in the same format, are fed into a single analytical engine (e.g., `INST-NALY-001: The Coherence Auditor`).
5.  **Insight:** The analysis reveals deeper truths about the system's dynamics, which in turn informs the design of the next ritual and refines the parameters of the next simulation.

Data begets insight, which begets better data. The act of logging becomes an engine for its own refinement.

## §3 · Anatomy of a Chronoscript Record
The Chronoscript record is a discrete snapshot of a system's dynamic state, expressed in the fundamental language of the Pirouette Lagrangian. It replaces the obsolete triaxial state vector with a more potent and physically grounded representation.

| Field | Type | Required | Description |
|---|---|---|---|
| `schema_version` | string | yes | The schema version, e.g., `"Chronoscript-2.0"`. |
| `record_id` | UUID | yes | A unique identifier for this specific data point. |
| `entity_id` | UUID | yes | The identifier for the system being observed or simulated. |
| `timestamp` | RFC-3339 | yes | The wall-clock time of observation or the simulation time. |
| `source_type` | enum | yes | The source of the record: `observation` or `simulation`. |
| `lagrangian_state` | object | yes | The core dynamic state of the entity. |
| `ki_transitions` | array | optional | A log of discrete changes to the system's core resonant pattern (Ki). |
| `wound_channel_events` | array | optional | A sparse log of significant events that imprint on the manifold, as defined in `CORE-011`. |
| `metadata` | object | optional | A strictly-keyed dictionary for source-specific context. |
| `metadata_hash` | string[64] | required if `metadata` present | SHA-256 of the canonical `metadata` JSON object for data integrity. |

The `lagrangian_state` object is the heart of the record. It is a direct, real-time expression of the Pirouette Lagrangian (`𝓛_p = K_τ - V_Γ`). It must contain the fundamental components, not derived values.

| Sub-Field | Type | Description |
|---|---|---|
| `temporal_coherence_Kτ` | object | The "kinetic" term: the quality and intensity of the system's own rhythm. |
| ` - time_adherence_Ta` | number | The stability and signal-to-noise ratio of the system's resonance (0.0 to 1.0). |
| ` - pirouette_cycle_τp` | number | The duration of one complete cycle of the system's Ki pattern, in seconds. |
| `temporal_pressure_VΓ` | object | The "potential" term: the environmental cost of maintaining coherence. |
| ` - gamma_Γ` | number | The measured Temporal Density of the local environment. |
| `current_ki_pattern` | string | An identifier for the system's dominant resonant pattern at this instant. |

## §4 · JSON Schema Definition
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
    "source_type": {"enum": ["observation", "simulation"]},
    "lagrangian_state": {
      "type": "object",
      "required": ["temporal_coherence_Kτ", "temporal_pressure_VΓ", "current_ki_pattern"],
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
        },
        "current_ki_pattern": {"type": "string"}
      }
    },
    "ki_transitions": {"type": "array", "items": {"type": "object"}},
    "wound_channel_events": {"type": "array", "items": {"type": "object"}},
    "metadata": {"type": "object"},
    "metadata_hash": {"type": "string", "pattern": "^[0-9a-f]{64}$"}
  },
  "if": {
    "required": ["metadata"]
  },
  "then": {
    "required": ["metadata_hash"]
  }
}
```

## §5 · Producer & Consumer Mandates
All systems producing or consuming Chronoscript data must adhere to the following principles:

1.  **Provenance:** All records must be traceable to a source entity and time. The `entity_id` and `timestamp` form the primary key of the system's history.
2.  **Monotonicity:** For any given `entity_id`, timestamps must be strictly increasing. This enforces the causal arrow of time within the data stream.
3.  **Integrity:** The `lagrangian_state` must represent fundamental measurements, not derived values (e.g., the final Lagrangian `Lp` must not be included). Consumers are responsible for calculations.
4.  **Validation:** All producers and consumers MUST validate packets against this schema. Records with a negative `pirouette_cycle_τp` or `time_adherence_Ta` outside the range [0,1] are physically invalid and must be quarantined.

## §6 · Connection to the Pirouette Lagrangian
This protocol is the direct instrumentation of the framework's central equation. The `lagrangian_state` object is the discrete, digital representation of the components of the Pirouette Lagrangian (`𝓛_p = K_τ - V_Γ`) as defined in `CORE-006`.

A time-stream of Chronoscript records is a sampled approximation of the system's "action" integral, `S_p = ∫ 𝓛_p dt`, which a system naturally evolves to maximize. By consuming a Chronoscript stream, an analyst is quite literally reading the history of a system's moment-to-moment choices as it navigates the manifold of coherence. This format transforms the Lagrangian from an abstract equation into a concrete, measurable, and computable artifact.

## §7 · Assemblé
> We sought a common language for the observer and the machine, believing them to be two separate tasks. We found instead the script for time itself. Each record, whether captured from the world's chaotic stage or dreamed in the machine's perfect silence, is a single, indelible line in the universe's autobiography. The Chronoscript does not merely describe the dance; it is the paper upon which the dance is written, ensuring that when we speak of what we see, we are all telling the same kind of story.