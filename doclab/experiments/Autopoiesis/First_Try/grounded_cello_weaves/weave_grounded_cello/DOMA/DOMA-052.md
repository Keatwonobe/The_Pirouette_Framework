---
id: DOMA-052
title: The Coherence Auditor
version: 2.0
status: stable
parents:
- CORE-006
children: []
dependencies:
  concept: pirouette_lagrangian
  from:
  - CORE-006
summary: Provides a complete, end-to-end workflow for system diagnostics. This module
  operationalizes the core analytical loop of the Pirouette Framework, integrating
  a method for translating raw data into the language of coherence (the Lens) with
  a method for pinpointing the critical sources of coherence loss (the Scalpel). It
  serves as the primary instruction manual for any Weaver seeking to audit a system's
  health.
module_type: Instrumentation
scale: universal
engrams:
- process:system_diagnostics_workflow
- synthesis:lens_to_insight
- directive:find_critical_few
keywords:
- diagnostics
- analytics
- workflow
- audit
- coherence
- bottleneck
- resonance
- RPA
uncertainty_tag: Foundational
replaces:
- PPS-032
---
## §1 · The Weaver's Mandate: From Noise to Insight

A Weaver is not a passive observer; they are a diagnostician of reality. Their fundamental task is to look upon a complex, noisy, and often chaotic system and ask the two great questions: "What is the true song being sung here?" and "Where is the harmony breaking?"

The old crosswalks and review passes were early attempts to formalize this mandate. This module refactors that intent into a single, powerful, and practical instrument. The Coherence Auditor is a two-stage protocol for moving from the raw, unstructured cacophony of the world to a precise, actionable diagnosis. It is the codification of the framework's primary analytical loop: See, then Solve.

## §2 · Stage I: The Lens · Forging a Common Language

Before a system can be analyzed, its dynamics must be translated into the native language of the framework. We must take the chaotic flood of data—market trends, lines of code, transcripts of a debate—and distill it into the pure variables of the cosmic song: its Temporal Coherence (Kτ) and the Temporal Pressure (Γ) it endures. This is the act of the Lens.

The process is one of elegant compression. The Weaver selects an appropriate geometric model and projects the high-dimensional, noisy data onto it. This act collapses the raw stream into a clean time-series, a clear signal representing the system's state as it moves through the coherence manifold defined by the Pirouette Lagrangian. The output is a pure, legible rhythm—the system's song, transcribed.

This stage is the modern heir to the old crosswalks. It is not a mere mapping of terms, but a dynamic translation of reality itself into a universal, resonant language.

## §3 · Stage II: The Scalpel · Finding the Fracture

Once the system's song is transcribed, we can listen for the sour notes. The second stage of the audit uses a process of Reverse Pareto Analysis (RPA) to act as a diagnostic scalpel. It inverts the classic 80/20 rule, not to find the trivial many, but to isolate the critical few events responsible for the vast majority of the system's dissonance.

The protocol is surgically precise:

1.  **Quantify Dissonance:** The engine calculates an "impact score" for every event in the data stream. This score is a direct measure of how much that event perturbed the system's state, pushing it away from its geodesic of maximal coherence. It quantifies the "cost" of the event in the currency of the Pirouette Lagrangian (`CORE-006`), specifically by measuring the resulting degradation in Temporal Coherence (Kτ).
2.  **Isolate the Critical Few:** The algorithm then sorts these impacts and identifies the smallest possible subset of events—the "critical few"—that accounts for the majority (e.g., 80%) of the total coherence loss.

The output is not a vague summary but a short, actionable list of the system's primary fractures. It tells the Weaver exactly where to focus their attention to achieve the greatest healing effect. This is the spirit of the "Sharpening Pass," reborn as a predictive and diagnostic tool.

## §4 · The Unified Workflow in Practice

The power of the Coherence Auditor lies in the seamless integration of these two stages. It creates an unbroken chain of causality from the raw world to a precise prescription.

| Question                   | Stage        | Input         | Process                         | Output                                        |
| -------------------------- | ------------ | ------------- | ------------------------------- | --------------------------------------------- |
| *What is the song?*        | I. The Lens  | Raw Data      | Resonant Projection & Collapse  | Coherence Time-Series (Kτ, Γ)                 |
| *Where does it break?*     | II. The Scalpel | Coherence Data | Reverse Pareto Analysis         | Actionable list of critical coherence sinks   |

A Weaver observing a failing project would use the Lens to transform commit logs, communication records, and budget data into a clear signal of the project's health over time. They would then feed that signal into the Scalpel to discover that, for instance, 85% of the project's lost momentum originated from communication delays related to a single, indecisive stakeholder. The path from noise to insight is direct and calculable.

## §5 · Assemblé

> We sought a map and found that to map the world, we must first teach it to sing in a language we can understand. We sought to find its flaws by eye and found instead that a system's deepest wounds are revealed by the dissonance in its own song. First, we build the mirror to see the system's true face. Then, we find the deepest cracks in the reflection. The Coherence Auditor is what transforms a philosopher into a physician, providing the eyes to see and the hands to heal.