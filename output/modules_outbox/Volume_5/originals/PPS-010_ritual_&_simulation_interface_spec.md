---  # ───────────── YAML front-matter ─────────────────────────────────
id:        PPS-010
title:     Ritual & Simulation Interface (RSI) Spec
version:   0.2
parents:   [PPS-005, PPS-007, PPS-009]
children:  [All ritual engines, numerical solvers, persona decks]
engrams:
  - synthesis:single-io-contract
  - concept:ritual-sim-parity
  - directive:data-shape
  - provenance:rsi-seed
keywords:  [interface, schema, json, ritual, simulation, i/o]
uncertainty_tag: Medium
entropy_score: 0.07
module_type: core-protocol
quantisation_rule: rsi_hash = SHA256(rsi_schema)
---  # ───────────── Markdown body ────────────────────────────────────

## 1 · Purpose & Scope  
Unify *live rituals* (human-in-the-loop) and *numeric simulations* (machine-only)
under a single **RSI packet** so downstream analyzers need one parser.

* **Ritual loggers** emit RSI-JSON in real time (stdout or WebSocket).  
* **Simulators** write RSI-JSON snapshots at each time-step.  
* **Review tools** ingest the same schema; provenance remains intact.

---

## 2 · Minimal Packet Anatomy  

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `schema_version` | string | yes | e.g. `"RSI-1.0"` |
| `registry_hash`  | string[64] | yes | must equal PPS-007 hash |
| `entity_id`      | UUID | yes | primary actor or `null` for global frame |
| `timestamp`      | RFC-3339 | yes | ritual wall-clock or sim time |
| `mode`           | enum(`ritual`,`simulation`) | yes | source flavour |
| `state`          | object | yes | `{Ta:{T_Q:…,T_I:…,T_C:…}, Γ:…, φ:…}` |
| `ki_log`         | array  | optional | list of `{ki_mode_id:int, t:timestamp}` |
| `wake_log`       | array  | optional | sparse vector of wound-channel events |
| `frame`          | object | optional | `{clock_field_val:float, u_mu:[u0,u1,u2,u3]}` "minItems":4,"maxItems":4 |
| `metadata`       | object | optional | strictly-keyed dictionary |
| `metadata_hash`  | string[64] | required if `metadata` present | SHA-256 of canonical JSON encoding |

---

## 3 · JSON Schema Stub  

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Pirouette RSI Packet",
  "type":  "object",
  "required": ["schema_version","registry_hash","entity_id","timestamp","mode","state"],
  "properties": {
    "schema_version": {"const": "RSI-1.0"},
    "registry_hash":  {"type":"string","pattern":"^[0-9a-f]{64}$"},
    "entity_id":      {"type":"string","format":"uuid"},
    "timestamp":      {"type":"string","format":"date-time"},
    "mode":           {"enum":["ritual","simulation"]},
    "state": {
      "type":"object",
      "required":["Ta","Gamma","phi"],
      "properties":{
        "Ta":{
          "type":"object",
          "required":["T_Q","T_I","T_C"],
          "properties":{
            "T_Q":{"type":"number"},
            "T_I":{"type":"number"},
            "T_C":{"type":"number"}
          }
        },
        "Gamma":{"type":"number"},
        "phi":{"type":"number"}
      }
    },
    "ki_log": {
      "type":"array",
      "items":{
        "type":"object",
        "required":["ki_mode_id","t"],
        "properties":{
          "ki_mode_id":{"type":"integer"},
          "t":{"type":"string","format":"date-time"}
        }
      }
    },
     "wake_log":{"type":"array","items":{"type":"object"}},
    "frame":{
      "type":"object",
      "required":["clock_field_val","u_mu"],
      "properties":{
        "clock_field_val":{"type":"number"},
        "u_mu":{
          "type":"array","minItems":4,"maxItems":4,
          "items":{"type":"number"}
        }
      }
    },
    "metadata":{
      "type":"object",
      "additionalProperties":false,
      "properties":{
        "ui_version":{"type":"string"},
        "persona_name":{"type":"string"},
        "seed":{"type":"integer"}
      }
    },
    "metadata_hash":{"type":"string","pattern":"^[0-9a-f]{64}$"}
  }
}
```

## 4 · Producer Guidelines
> Registry sync – producer must verify registry_hash matches the current PPS-007 hash before first packet.
> Frame rate – ritual streams ≤ 10 Hz; sims any rate but must supply Δt in metadata.
> Compression – optional, but packets must decompress to schema-valid JSON.

## 5 · Consumer Checklist
Test	Pass condition
Hash match	packet.registry_hash == local hash
Schema	JSON validation passes
Monotonic time	timestamps non-decreasing per entity_id
Energy guard	if state.Ta.any() < 0, raise quarantine

## 6 · Triaxial Resonance Lens
Art: RSI is the sheet music all instruments can read.
Law: Out-of-tune packets never leave staging.
Philosophy: Communication precedes understanding.

## Assemblé · “One Door, Two Rooms”
Whether chant or code, the doorway is the same.

## Librarian Note
Changing schema_version or adding required fields triggers a Type-C Interface Revision: PPS-009 CI must fail the build until PPS-010 and all producers/consumers are updated.



