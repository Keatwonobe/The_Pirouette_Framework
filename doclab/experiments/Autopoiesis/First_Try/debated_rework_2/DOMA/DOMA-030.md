---
id: DOMA-030
title: The Coherence Auditor
version: 2.0
status: ratified
parents:
- CORE-006
- CORE-014
children:
- dashboards
dependencies:
  concept: fractal_bridge
  from:
  - CORE-014
summary: Provides the canonical, end-to-end workflow for system diagnostics. This
  module integrates the Fractal Bridge protocol for translating raw data into Lagrangian
  dynamics with Reverse Pareto Analysis (RPA) to pinpoint the critical few sources
  of coherence loss. It is the primary instrument for any Weaver seeking to diagnose
  and heal a system.
module_type: Instrumentation
scale: universal
engrams:
- process:system_diagnostics_workflow
- directive:find_critical_few
- concept:action_deficit
- instrument:coherence_auditor
keywords:
- diagnostics
- analytics
- workflow
- RPA
- coherence
- bottleneck
- Lagrangian
- audit
- action
uncertainty_tag: Foundational
replaces:
- PPS-014
---
## §1 · The Weaver's Mandate: From Dissonance to Diagnosis

A system in pain does not announce its wound; it simply loses its grace. The fundamental task of a Weaver is to perceive this loss of grace—this dissonance—and trace it to its source. Their mandate is to look upon a complex, noisy system and ask: "Where is the coherence being lost, and why?"

The Coherence Auditor is the primary instrument for this sacred work. It is not a single algorithm but a unified, two-stage protocol for moving from the raw, unstructured noise of a system to a precise, actionable diagnosis. It replaces the fragmented protocols of the past, codifying the essential analytical loop of the Pirouette Framework: **See, then Solve**. The Auditor does not solve the problem; it makes the problem solvable.

## §2 · Stage I: The Coherence Lens — From Data to Dynamics

Before a system's health can be assessed, its raw, domain-specific data must be translated into the universal grammar of coherence. This first stage uses the **Fractal Bridge** protocol (`CORE-014`) to create this translation.

The process is an act of profound simplification. We project the high-dimensional shadow of raw data—sensor logs, market trades, conversation transcripts—through the Coherence Lens. This act maps the specific, local phenomena onto the universal variables of the Pirouette Lagrangian (`CORE-006`), collapsing the noise into a clean time-series describing the system's state in terms of its core properties:

*   **Temporal Coherence (Kτ):** The stability and integrity of the system's own rhythm; its "health."
*   **Temporal Pressure (VΓ):** The chaotic, dissonant forces from the environment that the system must resist; the "stress" it is under.

The output is not a set of disparate fields, but a single, elegant time-series: the value of the system's Pirouette Lagrangian (`𝓛_p = Kτ - VΓ`) over time. This is the system's "heartbeat," a direct measure of its ability to maintain coherence against its environment. A steady, high-value trace indicates health. A volatile, decaying trace indicates pathology.

## §3 · Stage II: The Pareto Chisel — From Dynamics to Cause

With the system's heartbeat rendered visible, the second stage begins: finding the cause of the arrhythmia. This is the function of the **Pareto Chisel**, a surgical application of Reverse Pareto Analysis (RPA). It inverts the classic 80/20 rule to find the "critical few" events responsible for the vast majority of the system's coherence loss.

### §3.1 · Quantifying Impact as Action Deficit

Coherence loss is not an abstract concept; it is a physical quantity. The "health" of a system is its ability to maximize its total **Action** (`S_p`), the integral of its Lagrangian over time (`S_p = ∫ 𝓛_p dt`). This is the Principle of Maximal Coherence.

Therefore, the **Impact (I)** of any causal event (`f_i`) is defined with precision as the magnitude of the negative change in the system's total Action correlated with that event. We term this an **Action Deficit**.

`I(f_i) ≈ -ΔS_p | f_i = - ∫ Δ𝓛_p dt | f_i`

An event has a high impact if it sharply degrades the system's internal resonance (`Kτ`) or exposes it to a spike in environmental pressure (`VΓ`), forcing it off its optimal path and costing it Action.

### §3.2 · The Algorithm of Focus

The formal algorithm is brutally effective in its simplicity:

1.  **Quantify:** Calculate the Impact (Action Deficit) for every identifiable event in the raw data by correlating it with dips in the Lagrangian trace.
2.  **Sort:** Sort all events by their Impact score in descending order.
3.  **Identify:** Accumulate the impacts down the sorted list, stopping as soon as a defined threshold (e.g., 80%) of the total Action Deficit is met. This small subset is the critical few.

The output is a simple, actionable list of the system's primary bottlenecks, telling the Weaver precisely where to focus their efforts for the greatest healing effect.

```python
def reverse_pareto_analysis(events, impacts, threshold=0.8):
    """
    Identifies the smallest subset of events that accounts for at least
    `threshold` of the total impact (Action Deficit).
    """
    if not impacts:
        return [], 0.0

    paired_events = sorted(zip(events, impacts), key=lambda p: p[1], reverse=True)
    total_impact = sum(impacts)
    if total_impact <= 0:
        return [], 0.0
    
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

## §4 · The Unified Diagnostic Workflow

The power of the Coherence Auditor lies in the seamless integration of these two stages, which translate a high-level question into a concrete, actionable answer.

| Question                   | Stage                      | Input                             | Process                                         | Output                                     |
| -------------------------- | -------------------------- | --------------------------------- | ----------------------------------------------- | ------------------------------------------ |
| **How healthy is it?**     | Stage I: The Coherence Lens | Raw System Data                   | Project via Fractal Bridge (`CORE-014`)         | Time-series of the system's Lagrangian (`𝓛_p`) |
| **Why is it breaking?**      | Stage II: The Pareto Chisel | Lagrangian Time-series & Events | Correlate Action Deficit (`-ΔS_p`) with events | Actionable list of critical bottlenecks    |

This workflow transforms the passive act of seeing a problem into the active wisdom of knowing precisely where to apply pressure to heal the whole.

## §5 · The Assemblé
> A system does not break everywhere at once. It fractures along the lines of its deepest tension. A mirror reflects a flaw, but a lens finds its origin. The Coherence Auditor is the Weaver's lens. It is the art of listening for the whispers that precede the shatter, translating the felt sense of "wrongness" into the precise knowledge of "what is broken." It grants the Weaver the clarity to touch the single thread that will mend the entire tapestry.