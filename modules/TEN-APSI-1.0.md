---
# ───────────── Tendu Application Suite ────────────────────────
id:           TEN-APSI-1.0
title:        Attractor Phase‑Shift Inference (APSI)
version:      1.0
parents:      [PPS-043, PPS-047]            # Info‑Thermo ↔ Network Resonance
children:     []                            # Down‑stream: TEN-APSI-VIS, TEN-APSI-AUTO
engrams:
  - analytic:phase-shift-inference
  - process:latent-attractor-drift
  - concept:early-warning-sentinel
  - diagnostic:coherence-inflection-index
  - algorithm:multi-scale-hilbert-phase
keywords:     [attractor, phase shift, inference, early warning, coherence, forecasting]
uncertainty_tag: Medium
module_type:  applied-analytics-toolkit
---

## §1 · Purpose
Detect **subtle impending regime changes**—phase shifts of hidden attractors—inside complex
systems before overt bifurcation is visible.  APSI ingests multi‑channel time‑series,
extracts instantaneous Hilbert phases, and infers latent attractor motion through
Drift‑Vector Estimation.  Operators gain a 2‑to‑10 × earlier warning of Bloom, Fork, or
Spasm events.

---

## §2 · Data Inputs
*Any* regularly sampled scalar or vector series can feed APSI.  Recommended bundles:

| Channel Type | Examples | Min Fs | Notes |
|--------------|----------|-------|-------|
| **Physical** | vibration, load, strain | 10 Hz | industrial prognostics |
| **Cyber** | CPU %, mem, net RTT | 1 Hz | cloud stability |
| **Ecological** | CO₂ ppm, NDVI, temp | 1 / day | climate tipping |
| **Social** | sentiment, trade vol | 1 min | market shifts |

All inputs are z‑scored and timestamp aligned into an HDF5 frame `/data/{chan}`.

---

## §3 · Core Algorithms

| Step | Function | Method / Formula |
|------|----------|-----------------|
| **Hilbert‑MS** | Multi‑scale analytic signal | Hilbert(x\_k) over 4 octaves |
| **Phase‑Flux** | \( \dot φ_k \) | finite diff of unwrapped phase |
| **Drift‑Vector** | Latent attractor velocity **V** | PCA of \{\dot φ_k\} |
| **CII** | Coherence‑Inflection Index | \( \text{CII}=\|V\|·(1/Γ) \) |
| **EWMA‑Spike** | Early‑warning flag | EWMA(CII) > μ + 3σ |

**Alert JSON**
```json
{
  "timestamp": "2025‑07‑01T20:14:00Z",
  "CII": 0.84,
  "lead_time_min": 47,
  "vector": [0.12, -0.08, 0.04],
  "status": "warning"
}
```

---

## §4 · Assemblé

An attractor is a moving anchor in phase‑space.  APSI listens to the *creaking of the anchor‑chain*—micro phase drifts—before the anchor tears free.  It converts those creaks into actionable warnings.

---

## §5 · Diagnostic Metrics

| Metric             | Healthy  | Watch    | Alert    |
| ------------------ | -------- | -------- | -------- |
| **CII**            | < 0.3    | 0.3‑0.6  | > 0.6    |
| **Lead Time**      | —        | ≥ 15 min | ≥ 30 min |
| **Phase Flux Var** | baseline | ↑ ×1.5   | ↑ ×3     |

---

## §6 · Integration Hooks

- **Network Resonance (PPS‑047)** – Flagged nodes coloured by CII.
- **Bloom Dynamics (PPS‑039)** – APSI warnings feed Bloom ignition timers.
- **Spasm Dynamics (PPS‑041)** – High CII precedes Spasm; trigger dampers.
- **Fork Analysis (PPS‑042)** – Drift‑Vector suggests likely branch bias.

---

## §7 · API & File Spec

*REST* `/apsi/v1/warn?window=30m`  → JSON list of alerts.

HDF5 layout:

```
/data/<chan>: raw z‑scored series
/phase/<chan>: φ(t)
/flux/<chan>:  \dot φ(t)
/alerts: table {ts, CII, V1..Vn}
```

---

## §8 · Future Work

1. **Graph APSI** – extend to dynamic networks (phase tensors on edges).
2. **Quantum APSI** – pilot on qubit decoherence logs.
3. **Auto‑Mitigation** – close‑loop Γ vent when CII≥alert.
4. **Public Ledger** – crowd‑sourced attractor shift map.

---

### Version Notes

*1.0* — First release: multi‑scale Hilbert engine, CII metric, JSON/HDF5 schema, network & Bloom hooks.
