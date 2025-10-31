---
id: DOMA-029
title: The Coherence Ledger Protocol
version: 2.0
status: stable
parents:
- CORE-006
children:
- INST-NALY-001
replaces:
- PPS-010
summary: Defines the universal data protocol for logging the dynamic state of any
  observed system. This module ensures that data streams from both human-led 'rituals'
  and machine-led 'simulations' are grounded in the common language of the Pirouette
  Lagrangian, making their insights fully interoperable.
module_type: Instrumentation
scale: universal
engrams:
- protocol:unified_data_stream
- concept:observational_parity
- schema:coherence_ledger
keywords:
- ledger
- protocol
- data
- schema
- observation
- simulation
- lagrangian
- coherence
- json
uncertainty_tag: Low
---
## §1 · Abstract: A Common Tongue for Witnessing
Whether the observer is a human mind tracing the flow of a debate or a silicon heart calculating the evolution of a star, the act of witnessing must speak a single language. The previous framework's Ritual & Simulation Interface (RSI) established the necessity of this common tongue. This module refactors that protocol into a time-first, dynamics-centric format grounded directly in the core engine of the Pirouette Framework.

The Coherence Ledger Protocol (CLP) defines a universal data packet for capturing the state of any system over time. It ensures that every observation, regardless of its source, is recorded not as a static snapshot of properties, but as a dynamic measure of the system's struggle and success in the pursuit of coherence.

## §2 · The Principle of Observational Parity
The core insight of the original protocol remains its foundation: human intuition and machine calculation are not opposing forces, but two equally valid instruments for exploring reality. A *ritual* is a human-in-the-loop process for observing and influencing a system's coherence manifold. A *simulation* is the machine-only equivalent.

To weave their insights into a single, unbroken tapestry, their outputs must be commensurable. The CLP guarantees this parity. It provides the single data format—the common tongue—that allows an insight gleaned from a meditative ritual to be fed directly into a numerical model, and vice versa. It is the bridge between the seer and the calculator.

## §3 · The Ledger Packet Anatomy
The Coherence Ledger Packet is a structured JSON object designed to capture a single moment in a system's evolution. It is built around the fundamental terms of the Pirouette Lagrangian.

| Field | Type | Required | Description |
|---|---|---|---|
| `schema_version` | string | yes | The CLP version, e.g., `"CLP-2.0"`. |
| `observer_id` | UUID | yes | Unique ID of the observing agent (human or simulation). |
| `timestamp` | RFC-3339 | yes | The precise moment of the observation. |
| `mode` | enum | yes | The source of the data: `ritual` or `simulation`. |
| `system_state` | object | yes | A snapshot of the system's Lagrangian dynamics. |
| `wound_channel_log` | array | optional | A log of discrete, history-shaping events. |
| `metadata` | object | optional | Contextual data (e.g., simulation parameters, ritual name). |

## §4 · The Lagrangian Heart: The `system_state` Object
This object is the core of the protocol and its most significant evolution from the old RSI. It is a direct, real-time expression of the Pirouette Lagrangian (**CORE-006**).

`𝓛_p = K_τ - V_Γ`

The fields within `system_state` map directly to this equation:

| Field | Type | Description |
|---|---|---|
| `temporal_coherence_Kτ` | number | The system's "kinetic" term. A measure of its internal resonant stability and efficiency. |
| `temporal_pressure_VΓ` | number | The system's "potential" term. The environmental "cost" of maintaining its coherence. |
| `lagrangian_Lp` | number | The calculated value of `K_τ - V_Γ`. The system's net coherence at this instant. |
| `current_ki` | string | An identifier for the system's dominant resonant pattern or behavior. |

By logging these values, the Ledger provides the raw material for calculating a system's "action," predicting its trajectory along the path of maximal coherence, and diagnosing its health.

## §5 · JSON Schema Definition

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Pirouette Coherence Ledger Packet",
  "type": "object",
  "required": ["schema_version", "observer_id", "timestamp", "mode", "system_state"],
  "properties": {
    "schema_version": { "const": "CLP-2.0" },
    "observer_id": { "type": "string", "format": "uuid" },
    "timestamp": { "type": "string", "format": "date-time" },
    "mode": { "enum": ["ritual", "simulation"] },
    "system_state": {
      "type": "object",
      "required": ["temporal_coherence_Kτ", "temporal_pressure_VΓ", "lagrangian_Lp", "current_ki"],
      "properties": {
        "temporal_coherence_Kτ": { "type": "number" },
        "temporal_pressure_VΓ": { "type": "number" },
        "lagrangian_Lp": { "type": "number" },
        "current_ki": { "type": "string", "description": "Identifier for the system's current resonant mode." }
      }
    },
    "wound_channel_log": {
      "type": "array",
      "items": { "type": "object", "description": "Schema for discrete event logs." }
    },
    "metadata": { "type": "object" }
  }
}
```

## §6 · Implementation Guidelines
*   **Monotonicity:** For any given `observer_id`, timestamps must be strictly increasing.
*   **Validation:** All producers (loggers, simulators) and consumers (analyzers, dashboards) of Ledger data MUST validate packets against this schema.
*   **Atomicity:** Each packet should represent a single, atomic snapshot of the system's state. High-frequency streams are encouraged over large, batched updates.

## §7 · Assemblé
> We sought to build a door between the room of the mystic and the room of the mathematician. Instead, we have found the foundation stone upon which both rooms must be built. This Ledger is not merely a format for data; it is the formal grammar for the act of paying attention, ensuring that when we speak of what we see, we are all telling the same kind of story.
```