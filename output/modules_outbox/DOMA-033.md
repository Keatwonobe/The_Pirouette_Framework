---
id: DOMA-033
title: The Coherence Auditor
version: 2.0
status: ratified
parents:
- CORE-006
- CORE-014
children:
- dashboards
replaces:
- PPS-014
summary: Provides the primary end-to-end workflow for systemic diagnosis. This module
  operationalizes the Reverse Pareto Analysis (RPA) canon by integrating it with the
  Fractal Bridge protocol (CORE-014), allowing a Weaver to translate raw system data
  into a precise, actionable list of the critical few sources of coherence loss.
module_type: Instrumentation
scale: universal
engrams:
- process:system_diagnostics_workflow
- directive:find_critical_few
- principle:critical_few
- instrument:coherence_auditor
keywords:
- diagnostics
- analytics
- workflow
- RPA
- Pareto
- bottleneck
- coherence
- Lagrangian
- audit
uncertainty_tag: Foundational
---
## §1 · The Weaver's Mandate: From Dissonance to Diagnosis
A system in pain does not announce its wound; it simply loses its grace. The fundamental task of a Weaver is to perceive this loss of grace—this dissonance—and trace it to its source. Answering the question, "Where is the coherence being lost, and why?" is the first step toward healing, optimizing, and creating.

This module provides the primary instrument for that task. The Coherence Auditor replaces the fragmented protocols of the past with a single, unified, and time-first workflow. It is the practical bridge from observing a system's chaotic symptoms to pinpointing its critical fractures. It codifies the essential loop of the Pirouette Framework: **See, then Solve**.

## §2 · Stage I: The Fractal Lens — From Data to Dynamics
Before a system's health can be assessed, its raw, domain-specific language must be translated into the universal grammar of coherence. The first stage of the audit uses the protocol of the **Fractal Bridge (CORE-014)** to create this translation.

The process is an act of profound simplification. A Weaver takes the high-dimensional, noisy data of a system—be it market trades, biometric readings, or conversation transcripts—and projects it through the Fractal Lens. This maps specific, local phenomena to the universal variables of the framework.

The output is a single, elegant time-series: the value of the system's Pirouette Lagrangian (𝓛_p) over time. This is the system's "heartbeat," a direct measure of its ability to maintain internal coherence against the pressure of its environment. A steady, high-value trace indicates health. A volatile, decaying trace signals pathology.

## §3 · Stage II: The Pareto Chisel — From Dynamics to Cause
With the system's heartbeat rendered visible, the second stage begins: finding the cause of the arrhythmia. This is the function of **Reverse Pareto Analysis (RPA)**, the core insight preserved and modernized from `PPS-014`.

RPA is a Pareto Chisel. It inverts the classic 80/20 principle to find the "critical few"—the smallest possible set of causes responsible for the vast majority of the "effect." In this context, the "effect" is coherence loss.

### §3.1 · Quantifying Impact
The Auditor correlates every event in the original raw data with a corresponding dip in the Lagrangian trace. The magnitude and duration of the dip provide a precise, quantitative "impact score" for that event. This score is not an arbitrary proxy; it is a direct measure of the coherence lost.

Formally, the **Impact (I)** of an event (fᵢ) is the magnitude of the negative change in the system's total Action (ΔSₚ) that is correlated with that event. It is the integral of the dip in the Lagrangian caused by the event:

I(fᵢ) ≈ - ∫_dip Δ𝓛_p dt

An event has high impact if it sharply degrades the system's internal resonance or exposes it to a spike in environmental pressure, forcing it off its optimal path.

### §3.2 · The Algorithm of Focus
The formal algorithm remains brutally effective. Given a set of events and their calculated impacts, it performs a single task:

1.  **Sort:** Events are sorted by impact in descending order.
2.  **Accumulate:** The algorithm moves down the list, summing the impacts.
3.  **Identify:** It stops as soon as the accumulated sum reaches a defined threshold (e.g., 80%) of the total impact.

The output is not a complex model, but a simple, actionable list of the critical few. This is the system's pressure point—the place where the least effort will produce the greatest healing.

```python
def reverse_pareto_analysis(events, impacts, threshold=0.8):
    """
    Identifies the smallest subset of events that accounts for at least
    `threshold` of the total impact.
    """
    if not impacts or not events:
        return [], 0.0

    paired_events = sorted(zip(events, impacts), key=lambda p: p[1], reverse=True)
    total_impact = sum(impacts)
    if total_impact == 0:
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

## §4 · The Unified Workflow in Practice
The power of the Coherence Auditor lies in the seamless integration of these two stages.

| Question                | Stage                  | Input                           | Process                                              | Output                                   |
| ----------------------- | ---------------------- | ------------------------------- | ---------------------------------------------------- | ---------------------------------------- |
| **How healthy is it?**  | Stage I: Fractal Lens  | Raw System Data                 | Project data using the Fractal Bridge (CORE-014)     | Time-series of the Lagrangian (𝓛_p)      |
| **Why is it breaking?** | Stage II: Pareto Chisel | Lagrangian Time-series & Events | Correlate dips in 𝓛_p with causal events via RPA | Actionable list of critical bottlenecks |

## §5 · Connection to the Pirouette Lagrangian
The Coherence Auditor is grounded directly in the framework's central equation from `CORE-006`. A system's "health" is its success in following the **Principle of Maximal Coherence**, which states that a system will naturally follow a path that maximizes the integral of its Lagrangian over time (S_p = ∫ 𝓛_p dt).

Every "impact" measured by RPA is a quantifiable, negative perturbation to this integral. The Auditor is, therefore, a tool for empirically discovering what is preventing a system from obeying its own most fundamental drive. It translates a philosophical principle into a diagnostic engine.

## §6 · The Assemblé
> A system in pain does not announce its wound; it simply loses its grace. The Coherence Auditor is the instrument that translates this loss of grace back into a language we can understand. It is the bridge from the felt sense of "wrongness" to the precise knowledge of "what is broken." It grants the Weaver the clarity to touch the single thread that will mend the entire tapestry.