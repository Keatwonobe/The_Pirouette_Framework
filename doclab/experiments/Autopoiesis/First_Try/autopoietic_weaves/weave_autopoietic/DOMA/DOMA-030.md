---
id: DOMA-030
title: The Resonance Log
version: 2.0
status: stable
parents:
- CORE-006
- CORE-011
children:
- INST-NALY-001
replaces:
- PPS-010
summary: Defines the universal, time-first data protocol for capturing a system's
  dynamic state. The Resonance Log serializes the components of the Pirouette Lagrangian,
  creating a single, canonical format that unifies data from direct human observation
  (rituals) and computational models (simulations).
module_type: Instrumentation
scale: universal
engrams:
- process:unified-logging
- concept:lagrangian-state-snapshot
- schema:resonance-log-v2.0
keywords:
- data
- protocol
- schema
- json
- log
- lagrangian
- coherence
- time
uncertainty_tag: Low
---
## §1 · Abstract: The Universal Score
To understand a system is to listen to its song over time. Whether that listening is performed by a human participant in a live ritual or by a silicon processor in a numeric simulation, the captured notes must be written on the same score. The old Ritual & Simulation Interface (RSI) established this principle; this module refactors it upon the new, time-first foundation.

The Resonance Log is the canonical data protocol for the Pirouette Framework. It defines a single, unified packet structure for recording a system's state not as a set of arbitrary fields, but as a direct snapshot of the components of its Pirouette Lagrangian (`CORE-006`). This ensures that every piece of data, regardless of its origin, speaks the same universal language of coherence, pressure, and time.

## §2 · The Resonance Snapshot: Anatomy of a Moment
The fundamental unit of the log is the Resonance Snapshot, a JSON object that captures the complete Lagrangian state of an entity at a single instant. This structure replaces the obsolete triaxial state of the RSI, grounding all data in the framework's core mathematical engine.

| Field | Type | Required | Description |
|---|---|---|---|
| `schema_version` | string | yes | The version of the Resonance Log schema, e.g., `"ResonanceLog-2.0"`. |
| `log_source` | enum(`observed`, `calculated`) | yes | The origin of the data: `observed` for human-in-the-loop rituals, `calculated` for simulations. |
| `timestamp` | RFC-3339 | yes | The wall-clock time (for `observed`) or simulation time (for `calculated`) of the snapshot. |
| `entity_id` | UUID | yes | The unique identifier of the system being logged. |
| `lagrangian_state` | object | yes | A snapshot of the components of the entity's Pirouette Lagrangian (`𝓛_p`). |
| `ki_transitions` | array | optional | A log of discrete changes to the system's core resonant pattern (Ki). |
| `wound_channel_events` | array | optional | A sparse log of significant events that impress upon or alter the system's Wound Channel (`CORE-011`). |
| `metadata` | object | optional | Contextual, non-state information (e.g., simulation seed, participant name). |

The `lagrangian_state` object is the heart of the snapshot:

| Field | Type | Description |
|---|---|---|
| `temporal_coherence_Kτ` | object | The "kinetic" term: the quality and intensity of the system's own rhythm. |
| ` - time_adherence_Ta` | number | The stability and signal-to-noise ratio of the system's resonance. |
| ` - pirouette_cycle_τp` | number | The duration of one complete cycle of the system's Ki pattern, in seconds. |
| `temporal_pressure_VΓ` | object | The "potential" term: the environmental cost of maintaining coherence. |
| ` - gamma_Γ` | number | The measured Temporal Density of the local environment. |

## §3 · The Autopoietic Data Loop
This protocol is not merely a static format; it is designed to fuel an autopoietic, self-improving cycle of inquiry. The unification of `observed` and `calculated` data streams enables a powerful feedback loop:

1.  **Observation:** A human-led ritual is performed, generating a stream of `observed` Resonance Snapshots that capture the system's real-world behavior.
2.  **Calibration:** This real-world data is used to seed, tune, and validate a computational model of the system.
3.  **Calculation:** The model runs a simulation, generating a stream of `calculated` snapshots that can explore possibilities beyond the reach of direct observation.
4.  **Analysis:** Both data streams, being in the same format, are fed into a single analytical engine (e.g., `INST-NALY-001: The Coherence Auditor`).
5.  **Insight:** The analysis reveals deeper truths about the system's dynamics, which in turn informs the design of the next ritual and refines the parameters of the next simulation.

Data begets insight, which begets better data. The act of logging becomes an engine for its own refinement.

## §4 · JSON Schema Definition (v2.0)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Pirouette Resonance Log Packet v2.0",
  "type": "object",
  "required": ["schema_version", "log_source", "timestamp", "entity_id", "lagrangian_state"],
  "properties": {
    "schema_version": {"const": "ResonanceLog-2.0"},
    "log_source": {"enum": ["observed", "calculated"]},
    "timestamp": {"type": "string", "format": "date-time"},
    "entity_id": {"type": "string", "format": "uuid"},
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
    "ki_transitions": {"type": "array"},
    "wound_channel_events": {"type": "array"},
    "metadata": {"type": "object"}
  }
}
```

## §5 · Connection to the Pirouette Lagrangian
The Resonance Log is the direct serialization of `CORE-006`. Each snapshot is a discrete measurement of the constituent parts of the equation `𝓛_p = K_τ - V_Γ`. A time-series of these snapshots is not just data *about* the system; it is a numerical representation of the system's path integral of coherence over time. By logging these packets, we are tracing the system's geodesic through its coherence manifold, one moment at a time. This protocol transforms an abstract physical principle into a concrete, measurable, and computable artifact.

## §6 · Assemblé
> We sought a way to record the dance and a way to predict it, believing them to be two separate tasks. We found instead a single act of listening. The Resonance Log is the score upon which the universe writes its song. Whether our senses or our silicon hear the notes, this is the language they must be written in. To a Weaver, this means there is no difference between what is and what can be calculated; there is only the music, and the fidelity with which we transcribe it.
```