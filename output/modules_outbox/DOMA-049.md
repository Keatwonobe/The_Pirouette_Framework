---
id: DOMA-049
title: The Weaver's Compass
version: 2.0
status: ratified
parents:
- DYNA-001
- CORE-006
- CORE-010
- CORE-011
children: []
replaces:
- PPS-030
summary: Re-frames the concept of Radiance from a transactional score to a diagnostic
  measure of an action's impact on systemic coherence. It defines 'Constructive Influence'
  as a measurable increase in a system's ability to express its resonant pattern,
  as described by the Pirouette Lagrangian. It provides both the core principle and
  a practical protocol for its approximation, replacing the old accounting engine
  with a compass for systemic healing.
module_type: Domain Application
keywords:
- influence
- coherence
- compass
- ethics
- lagrangian
- weaving
- measurement
- ledger
- resonance
engrams:
- principle:constructive_influence
- process:coherence_weaving
- instrument:coherence_impact_gauge
- concept:universal_ledger
uncertainty_tag: Low
---
## §1 · Abstract: From Accounting to Healing

The prior framework, PPS-030, sought to build an engine for quantifying "Radiance," an attempt to convert the nuanced art of altruism into a transactional metric. It was an accountant's approach to grace—a ledger for good deeds. This was a noble but premature ambition; it built an accounting system before defining the asset.

This module replaces the engine with a compass. It reframes ethics as a practical application of Flow Dynamics, moving from a score to be tallied to a diagnostic act of systemic medicine. A "good" action is not one that generates a high number, but one that can be shown to have healed a fractured system, easing its flow from a state of turbulence or stagnation into one of graceful, laminar coherence. This Weaver's Compass is a tool for navigating the moral landscape by the light of resonance itself, grounding the art of influence in the physics of consequence.

## §2 · The Lagrangian of Influence

The core of this new model is grounded directly in the universe's fundamental drive as described by the **Pirouette Lagrangian** (`CORE-006`). An action's virtue is no longer a matter of opinion or complex coefficients; it is a measurable change in a target system's ability to exist.

We define a **Weaving** as an intervention by an Actor that measurably affects the coherence of a Target system. The **Influence (`I`)** of this Weaving is the change in the Target's "action"—the integral of its Pirouette Lagrangian (`𝓛_p = K_τ - V_Γ`) over one of its own cycles (`τ_p`).

`I = ΔS_p = ∫[0 to τ_p] (𝓛_p(post) - 𝓛_p(pre)) dt`

-   A **Constructive Weaving (`I > 0`)**: The action has increased the Target's overall coherence. It has made it easier for the system to maintain its resonant pattern (`Ki`), either by increasing its internal stability (`K_τ`) or by lessening the external temporal pressure it must fight against (`V_Γ`). This is the formal definition of healing.
-   A **Destructive Weaving (`I < 0`)**: The action has decreased the Target's coherence, increasing its internal dissonance and pushing it towards a state of chaotic, turbulent flow. This is the formal definition of harm.

This single principle subsumes the entire complex formula of the old Radiance score. The disparate parts of the old equation—coherence generated, entropy, empathy, risk—are all implicitly contained within this one integral of the universe's objective function.

## §3 · The Nature of the Ripple

While the Lagrangian provides the formal definition, the effect of a Weaving can be understood intuitively as an injection of resonance into the coherence manifold—a ripple that propagates outward.

**Positive Radiance (A Coherence Injection):** This is the signature of a constructive, or "altruistic," act (`I > 0`). It is an action that helps another system move toward a state of **Laminar Flow** (`DYNA-001`) by smoothing the manifold, harmonizing resonance, or reinforcing an existing channel of coherence.
*   *Example:* A clear explanation that resolves a team's confusion, allowing their work to flow smoothly again.

**Negative Radiance (A Dissonance Injection):** This is the signature of a destructive act (`I < 0`). It is an action that pushes another system into **Turbulent** or **Stagnant Flow** by increasing ambient pressure, introducing chaos, or blocking a channel of coherence.
*   *Example:* Spreading misinformation that causes panic and chaos within a community.

## §4 · From Principle to Instrumentation

Directly measuring the integral of a system's Lagrangian (`ΔS_p`) is profoundly difficult. Therefore, we establish a practical, first-order approximation: the **Coherence Impact (CI)** score. This score serves as the reading on the Weaver's Compass, a tangible proxy for the deeper reality.

**CI = (ΔKτ / ΔΓ_noise) ⋅ ξ_c ⋅ σ_s**

Where:
*   **ΔKτ / ΔΓ_noise (Signal-to-Noise Ratio):** The core measurement. It is the ratio of the net increase in the target's stable, resonant information (`ΔKτ`) to the chaos, friction, or entropy generated by the intervention (`ΔΓ_noise`).
*   **ξ_c (Resonance Coupling):** A measure of the phase-alignment between the intervener and the target system. High coupling indicates a near-lossless transfer of coherence, where the action perfectly meets the system's needs.
*   **σ_s (Stability Factor):** Measures the durability of the new, more coherent state. It is a function of how deeply the act carves a new, stable **Wound Channel** (`CORE-011`).

An observer attests to a Weaving by creating an Echo Record, a high-fidelity data packet designed to capture the transaction's geometry:

```jsonc
{
  "transaction_id": "uuid-v4",
  "observer_id": "WEAVER-007",
  "target_system_id": "COMM-GARDEN-04",
  "timestamp": "2025-08-11T16:30:00Z",
  "context": {
    "flow_diagnosis": "Transition from Turbulent (infighting) to Laminar (collaboration).",
    "description": "Mediated a dispute between community garden members over resource allocation."
  },
  "metrics": {
    "coherence_delta_k_tau": 25.4,   // Positive change in collaborative function.
    "dissonance_delta_gamma": 4.1,   // Residual tension and administrative overhead.
    "resonance_coupling_xi": 0.95,   // Mediator deeply understood the core issues.
    "stability_factor_sigma": 0.88   // The resolution is stable but requires maintenance.
  },
  "attestation": {
    "method": "ed25519",
    "signature": "base64-sig",
    "observer_shadow_confidence": 0.92 // Observer's credibility and internal coherence.
  }
}
```

## §5 · The Universal Ledger & The Observer's Shadow

The universe already possesses the ultimate, indelible ledger: the **Wound Channel** (`CORE-011`). Every action is carved into the geometry of spacetime as a persistent scar. This active, physical landscape is the true record of consequence.

The protocol described above does not create a new source of truth. It creates a *map*—a shared, topographical chart of coherence flows derived from our limited attempts to read the true ledger. The fidelity of this map is subject to the **Observer's Shadow** (`CORE-010`). An observer's measurement is a resonant coupling, not a passive report. A coherent, skillful observer casts a sharp shadow, creating a high-fidelity record. A biased or dissonant observer projects a distorted shadow, adding noise to the very signal they wish to perceive. The `observer_shadow_confidence` metric is a formal acknowledgement of this inescapable physical reality.

## §6 · Assemblé

> The old engine sought to turn grace into a currency. It was a well-intentioned error, for the moment something can be counted, it can be hoarded. The Weaver's Compass offers a different path. It does not create a score to be won, but a direction to be followed, grounded in the physics of creation itself. The universe is a resonant chamber that remembers every note played. To act with virtue is simply to be a good musician—to choose a resonance that strengthens the harmony of the whole, knowing the echo is carved into spacetime forever. The ledger is the cosmos, our instruments are but humble sensors, and your life is your signature.