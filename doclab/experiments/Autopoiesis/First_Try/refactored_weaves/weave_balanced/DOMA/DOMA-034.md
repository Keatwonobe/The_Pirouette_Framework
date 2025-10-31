---
id: DOMA-034
title: The Coherence Auditor
version: 2.0
status: stable
parents:
- CORE-006
children:
- dashboards
dependencies:
  concept: pirouette_lagrangian
  from:
  - CORE-006
summary: Provides a complete, end-to-end workflow for system diagnostics. This module
  integrates the translation of raw data into Pirouette terms with Reverse Pareto
  Analysis (RPA) to pinpoint the critical few sources of coherence loss. It serves
  as the primary instruction manual for any Weaver seeking to audit a system's health.
module_type: Instrumentation
scale: universal
engrams:
- process:system_diagnostics_workflow
- process:bottleneck_analysis
- principle:critical_few
keywords:
- diagnostics
- analytics
- workflow
- RPA
- coherence
- audit
- bottleneck
- lagrangian
uncertainty_tag: Low
replaces:
- PPS-014
---
## §1 · The Weaver's Mandate: From Noise to Insight
A Weaver is not a passive observer; they are a diagnostician of reality. Their fundamental task is to look upon a complex, noisy, and often chaotic system and ask: "Where is the coherence being lost, and why?" Answering this question is the first step toward healing, optimizing, and creating.

This module provides the primary toolkit for that task. The Coherence Auditor is not a single algorithm but a practical, two-stage protocol for moving from the raw, unstructured noise of a system to a precise, actionable diagnosis. It is the operational heart of the Pirouette Framework, codifying the essential loop: **See, then Solve**.

## §2 · Stage 1: Ingesting Reality
Before a system can be analyzed, its dynamics must be translated into the native language of the framework. Raw data—sensor logs, market trades, conversation transcripts—is a shadow of reality. We must find the body that casts it. This first stage turns the "what is happening" of raw data into the "how it resonates" of field dynamics.

This process involves projecting the high-dimensional, noisy data stream onto a lower-dimensional manifold that captures its essential dynamics. The output is a clean time-series describing the system's state in terms of its core properties:

*   **Temporal Coherence (Kτ):** The stability and integrity of the system's own rhythm. This is its "health."
*   **Temporal Pressure (VΓ):** The chaotic, dissonant forces from the environment that the system must resist. This is the "stress" it is under.

This translation provides the direct inputs for the Pirouette Lagrangian (`CORE-006`), allowing us to see how well the system is navigating its path of maximal coherence.

## §3 · Stage 2: Finding the Fracture
Once the system's dynamics are expressed in the language of coherence, we can perform surgery. The second stage uses **Reverse Pareto Analysis (RPA)** to pinpoint the source of instability. It inverts the classic 80/20 rule to find the critical few causes—the 20%—responsible for the vast majority—the 80%—of the system's coherence loss.

The protocol is as follows:

1.  **Quantify Impact:** First, we calculate an "impact score" for every event or feature in the data. This score measures how much each event perturbed the system's Temporal Coherence (Kτ). A high-impact event is one that caused a sharp, negative shock to the system's health.
2.  **Sort and Sum:** The events are sorted in descending order of their impact. We then create a cumulative sum, identifying the smallest possible subset of events that accounts for a majority (e.g., 80%) of the total coherence loss.
3.  **Generate Diagnosis:** The output is not a complex chart, but a simple, actionable list of the system's primary bottlenecks. It tells the Weaver exactly where to focus their attention to achieve the greatest healing effect with the least effort.

RPA is the instrument that turns the "how it resonates" of the field data into the "why it's breaking" of a concrete diagnosis.

## §4 · Connection to the Pirouette Lagrangian
This entire workflow is directly grounded in the framework's central equation from `CORE-006`, the Pirouette Lagrangian: `𝓛_p = Kτ - VΓ`.

The fundamental law is the **Principle of Maximal Coherence**: a healthy system naturally follows a path that maximizes the integral of this Lagrangian over time. "Coherence loss," therefore, is a quantitative drop in this integral.

The impact score calculated in Stage 2 is a direct measure of an event's negative contribution to `∫𝓛_p dt`. An event with high impact is one that forces the system far from its optimal path, its geodesic. RPA is thus a surgical tool for identifying the precise moments and causes that prevent a system from realizing its full potential for stable, efficient existence. By fixing the few critical issues RPA identifies, we restore the system's ability to maximize its own coherence.

## §5 · The Assemblé
> A mirror reflects a flaw, but a lens finds its origin. The Coherence Auditor is the Weaver's lens. It is the tool that transforms the passive act of seeing a problem into the active wisdom of knowing precisely where to apply pressure to heal the whole. To audit a system is to learn its deepest vulnerabilities, and in that knowledge lies the power to make it unbreakable.
```