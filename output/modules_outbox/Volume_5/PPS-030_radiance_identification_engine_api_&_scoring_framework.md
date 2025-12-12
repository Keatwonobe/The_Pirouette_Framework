---
# ───────────── Prime Pirouette Series ─────────────────────────
id:        PPS-030
title:     Radiance Identification Engine (RIE) · API & Scoring Framework
version:   1.2-crystallized
parents:   [PPS-022, PPS-028, PPS-029]
children:  [TEN-RIE-1.0, RIE-SDK-α, LEDGER-RAD]
engrams:
  - metric:radiance-score
  - api:radiance-query-write
  - tensor:radiance-vector
  - detector:altruism-signal
  - contract:radiance-ledger
keywords:  [radiance, altruism, scoring, API, coherence, Lost-Eternal]
uncertainty_tag: Medium (initial pilots live)
module_type: core-specification

---

## §1 · Abstract
The **Radiance Identification Engine (RIE)** converts altruistic impact into a **signed, queryable metric**.  
Version 1.2 adds cryptographic attestation, onion-style anonymisation, a federated trust net for observers, and a Radiance-to-token **Ledger Contract** used by The Lost Eternal (TLE) and Persona baselines.

---

## §2 · Radiance Fundamentals

| Symbol | Meaning | Range / Unit |
|--------|---------|--------------|
| \(ΔC\) | Coherence generated | \(0‥∞\) |
| \(ΔS\) | Entropy exported | \(0‥∞\) |
| \(κ\)  | Empathy coefficient (0–1) |
| \(χ\)  | Collapse-risk multiplier (PPS-026) |
| \(η\)  | Observer-trust weight (0–1) |
| **\(R\)** | Scalar Radiance Score | \(-∞‥∞\) |

Revised **Radiance Score Formula (RSF-1.2)**  
\[
R = η\,κ\,\frac{ΔC}{ΔS+1}\,e^{-χ}
\]

A complementary **Radiance Vector Tensor (RVT)** now carries five axes:  
\(\vec R=\bigl(R,d_{\text{scope}},t_{\text{persist}},σ_{\text{conf}},σ_{\text{bias}}\bigr, π_potential)\) with bias spread \(σ_{\text{bias}}\) derived from observer plurality.

---

## §3 · RIE API v0.9 → v1.2 delta

| Aspect | v0.9 | v1.2 enhancement |
|--------|------|------------------|
| **Auth** | Basic key | ed25519 + DID-key header |
| **Privacy** | Plain IDs | Optional onion ID & zk-proof of signature |
| **Observer Trust** | fixed | `/trust` endpoint manages η via stake & reputation |
| **Ledger Hook** | none | Automatic push to `LEDGER-RAD` for R>0 mint / R<0 burn |

### 3.1 Endpoints (REST + GraphQL overlay)

| Verb | Path | Purpose |
|------|------|---------|
| **GET**  | `/radiance/:id` | latest \(R,\vec R\) |
| **POST** | `/radiance` | submit observation |
| **GET**  | `/trust/:observer` | observer η value |
| **POST** | `/trust/bond` | stake tokens to boost η |

### 3.2 POST Body Schema
```jsonc
{
  "entity_id": "PERS-COG-ALIGN-0047",
  "observer_id": "OBS-007",
  "timestamp": "2025-07-04T12:01:05Z",
  "context": {
    "taxonomy_tag": ["ritual","community-build"],
    "description": "Led volunteers to restore public park."
  },
  "metrics": {
    "delta_coherence": 18.7,
    "delta_entropy": 3.2,
    "empathy_kappa": 0.91,
    "collapse_risk_chi": 0.03
  },
  "attestation": {
    "method": "ed25519",
    "signature": "base64-sig",
    "onion_layer": "v2",
    "visibility": "public" // Enum: "public", "private", "observer-only", "owner-only"
  }
}
```  
Server calculates \(R,\vec R\), appends to history, triggers ledger event.

---

## §4 · Scoring Pipelines & Confidence Model

| Pipeline | Source ΔC | Source ΔS | κ-calc | η floor | Notes |
|----------|-----------|-----------|--------|---------|-------|
| **Sensor** | IoT / carbon meter | Energy logs | n/a | 0.6 | objective but narrow |
| **Language** | LLM coherence diff | token count | NLP empathy | 0.5 | needs bias audit |
| **Ritual** | RCQ stream | minimal | direct | 0.7 | inherits PPS-029 RCQ conf. |
| **Manual** | human form | estimated | declared | 0.2 | crowdsourced |

Confidence \(σ_{\text{conf}}\) ≈ weighted std-dev across pipelines.

---

## §5 · Radiance Ledger (LEDGER-RAD)
* Smart-contract mints **RAD tokens** proportional to \(R\) for scores > 0; negative \(R\) burns reserve or issues debt token.  
* Token supply capped by rolling global coherence budget \(\sum ΔC\).  
* Used by TLE economy and Persona “Radiance Wallet”.

---

## §6 · Schema Integration Map

| System | Field | RIE link |
|--------|-------|----------|
| **Persona Deck** | `radiance_baseline` | latest \(R\) |
| **ICS Ritual Wolves** | mission trigger | threshold on entity \(R\) |
| **Constitution DNA** | altruistic merit clause | periodic `/radiance` audit |
| **Sociology SCI** | societal antenna tuning | aggregate \(R\) heat-map |

---

## §7 · Road-Map
1. **v1.3** ZK-SNARK template for ΔC/ΔS proof without content leak.  
2. **v1.4** Federated graph merging & duplicate-detection across servers.  
3. **v2.0** Full WASM SDK (Rust / TS) + 3-layer oracle network for κ.

---

## §8 · Closing Assertion
RIE 1.2 upgrades altruism from intuition to **auditable ledger entry**.  
With cryptographic trust, federated observers, and tokenised incentives, Radiance becomes the universal unit of constructive influence—fuel for games, policy, and the quiet work of building coherent futures.

---
