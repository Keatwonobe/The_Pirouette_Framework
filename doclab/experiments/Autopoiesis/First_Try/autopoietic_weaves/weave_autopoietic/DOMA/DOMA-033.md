---
id: DOMA-033
title: The Coherence Auditor
version: 2.0
status: stable
parents:
- CORE-006
children:
- dashboards
replaces:
- PPS-014
summary: Provides a complete, end-to-end workflow for system diagnostics. This module
  integrates a protocol for translating raw data into the dynamics of the coherence
  manifold with Reverse Pareto Analysis (RPA) for pinpointing the critical sources
  of coherence loss. It is the primary instrument for any Weaver seeking to diagnose
  and heal a system.
module_type: Instrumentation
scale: universal
engrams:
- process:system_diagnostics_workflow
- concept:critical_few
- principle:coherence_loss_as_action_deficit
keywords:
- diagnostics
- analytics
- workflow
- RPA
- coherence
- bottleneck
- Lagrangian
- audit
uncertainty_tag: Foundational
---
## §1 · The Weaver's Mandate: From Noise to Insight
A Weaver is not a passive observer; they are a diagnostician of reality. Their fundamental task is to look upon a complex, noisy, and often chaotic system and ask: "Where is the coherence being lost, and why?"

This module provides the primary toolkit for answering that question. The Coherence Auditor is not a theoretical sketch but a practical, two-stage protocol for moving from raw, unstructured data to a precise, actionable diagnosis. It operationalizes the core analytical loop of the Pirouette Framework: See, then Solve. It replaces the fragmented approach of earlier protocols with a single, unified instrument.

## §2 · Stage I: Projecting the Shadow · The Coherence Lens
Before a system can be analyzed, its dynamics must be translated into the native language of the framework. We must see how it moves upon the coherence manifold. This is the function of the Coherence Lens.

The process is one of projection. Raw data—sensor logs, market data, transcripts, biometric readings—is a high-dimensional shadow of the system's true state. The lens projects this shadow onto the manifold defined by the Pirouette Lagrangian (CORE-006), collapsing the noise into a clean time-series that tracks the system's "Action" (S_p), the integral of its Lagrangian over its own cycles.

The output is a clear, quantitative trace of the system's health: a measure of how successfully it is navigating its geodesic of maximal coherence. Where the trace is high and stable, the system is in a state of laminar flow. Where it dips, coherence is being lost.

## §3 · Stage II: Finding the Fracture · Reverse Pareto Analysis (RPA)
Once the system's health is rendered visible, we can perform surgery. Reverse Pareto Analysis (RPA) is the surgical tool. It inverts the classic 80/20 rule not just to find the 20% of causes for 80% of the effects, but to find the smallest possible set of events responsible for the majority of the system's Action Deficit.

**§3.1 · The Lagrangian Connection: Quantifying Impact**
In the old framework, impact was an abstract "perturbation." We now define it with physical precision. The **Impact (I)** of any event (f_i) is the magnitude of the negative change in the system's total Action (ΔS_p) that is correlated with that event.

I(f_i) ≈ -ΔS_p | f_i = - ∫ Δ𝓛_p dt | f_i

An event has a high impact if it sharply degrades the system's internal resonance (Kτ) or exposes it to a spike in environmental Temporal Pressure (V_Γ), forcing it off its optimal path. RPA finds the events that are costing the system the most.

**§3.2 · The Algorithm of Focus**
The formal algorithm remains brutally effective. Given a set of events and their calculated impacts, it performs a single task:

1.  **Sort:** Events are sorted by impact in descending order.
2.  **Accumulate:** The algorithm moves down the list, summing the impacts.
3.  **Identify:** It stops as soon as the accumulated sum reaches a defined threshold (e.g., 80%) of the total impact.

The output is not a complex model, but a simple, actionable list: the critical few. This is the system's pressure point—the place where the least effort will produce the greatest healing.

```python
def reverse_pareto_analysis(events, impacts, threshold=0.8):
    """
    Identifies the smallest subset of events that accounts for at least
    `threshold` of the total impact.
    """
    if not impacts:
        return [], 0.0

    paired_events = sorted(zip(events, impacts), key=lambda p: p[1], reverse=True)
    total_impact = sum(impacts)
    target_impact = threshold * total_impact
    
    accumulated_impact = 0.0
    critical_few = []
    
    for event, impact in paired_events:
        if accumulated_impact >= target_impact:
            break
        critical_few.append(event)
        accumulated_impact += impact
        
    return critical_few, accumulated_impact / total_impact
```

## §4 · The Unified Workflow in Practice
The power of the Coherence Auditor lies in the seamless integration of these two stages.

| Question                   | Stage                      | Input             | Process                                         | Output                               |
| -------------------------- | -------------------------- | ----------------- | ----------------------------------------------- | ------------------------------------ |
| **How healthy is it?**     | Stage I: The Coherence Lens | Raw System Data   | Project data onto the Lagrangian manifold       | Time-series of the system's Action (S_p) |
| **Why is it breaking?**      | Stage II: RPA              | Action Time-series & Events | Correlate Action Deficit with causal events | Actionable list of critical bottlenecks |

## §5 · Assemblé
> A system does not break everywhere at once. It fractures along the lines of its deepest tension. RPA is not a tool for finding flaws; it is the art of listening for the whispers that precede the shatter. To find the critical few is to find the precise point where a single touch can heal the whole.

```