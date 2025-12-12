---
id: DOMA-181
title: The Rhythmic Sieve
version: 2.0
status: ratified
parents:
- DYNA-001
children: []
dependencies:
- concept: coherence_as_information
  from:
  - CORE-013
- concept: flow_diagnostics
  from:
  - DYNA-001
- concept: pirouette_lagrangian
  from:
  - CORE-006
summary: "Provides a modernized, time-first protocol for analyzing arbitrary information\
  \ streams by passing them through a rhythmic 'sieve.' This process separates coherent,\
  \ signal-like patterns (K\u03C4) from dissonant, noise-like components (\u0393),\
  \ producing a rich 'Coherence Profile.' A derived Coherence Ratio (CR) offers a\
  \ powerful signal-to-noise diagnostic for assessing the health and character of\
  \ any information flow."
module_type: Instrumentation
scale: universal
engrams:
- process:rhythmic_segmentation
- principle:coherence_profiling
- concept:coherence_ratio
keywords:
- instrumentation
- data
- analysis
- coherence
- entropy
- rhythm
- segmentation
- noise
- signal
- time-series
- flow
- diagnostics
uncertainty_tag: Low
replaces:
- TEN-SG-1.0
---
## §1 · Abstract: The Stethoscope for the River
To understand a river, one does not simply measure its volume. One must listen to its current, distinguish the steady flow from the turbulent eddy, and map the deep, silent channels hidden beneath the surface noise.

This module provides the instrumentation for such an act of listening. It refactors the legacy "Stochastic Gulping" protocol into The Rhythmic Sieve, a time-first method for analyzing any information stream. The core insight is preserved—that examining a stream in discrete segments reveals its underlying structure—but we now reframe this process not as a crude measurement of disorder, but as a sophisticated act of separating a signal's **Coherence** from its ambient **Dissonance**. It is a stethoscope for the stream, a tool for diagnosing the very health of information itself by revealing its hidden rhythms and patterns of flow.

## §2 · From Entropy to Coherence: The Conceptual Shift
The old protocol was anchored in Shannon entropy, a powerful but static measure of disorder. The new framework allows for a more dynamic and profound diagnosis, grounded in the principles of `CORE-013: The River of Information`.

-   **Information as Coherence (`Kτ`):** We no longer see data as a static list of symbols, but as a dynamic current. The true signal within this current is its Coherence (`Kτ`)—the measure of stable, resonant, and meaningful patterns within a segment of the stream. It is the melody, the information itself.
-   **Noise as Dissonance (`Γ`):** What was previously measured as "high entropy" is now identified as Dissonance (`Γ`). This is the measure of chaotic, turbulent, and unstructured temporal pressure that degrades the signal. It is the static that obscures the melody.

By profiling a stream in terms of the interplay between Coherence and Dissonance, we can diagnose its state of flow (`Laminar`, `Turbulent`, or `Stagnant`) with far greater precision, as defined in `DYNA-001`.

## §3 · The Sieve Protocol
The Rhythmic Sieve is a three-stage process for transforming a raw information current into an actionable diagnosis.

### Stage I: Rhythmic Segmentation (Setting the Mesh)
The first step is to divide the continuous information stream into a series of discrete temporal windows. This is the "sieve's mesh." The size of this window is a critical parameter, chosen to match the scale of the phenomena being investigated.

-   **Fixed Window:** A constant segment size is used to analyze the stream for patterns at a specific, consistent frequency.
-   **Adaptive Window:** The segment size changes dynamically, shrinking in regions of high turbulence (rapid change) and expanding in regions of laminar flow (stability) to capture events at their natural timescale.

### Stage II: Coherence Profiling (Measuring the Flow)
For each temporal window, we calculate a pair of fundamental metrics that form the stream's primary **Coherence Profile**.

1.  **Coherence (`Kτ`):** A measure of the segment's internal order, predictability, and resonant structure. High coherence indicates a clear, stable signal. This is often quantified by finding the strength of the window's dominant pattern through techniques like autocorrelation or Fourier analysis.
2.  **Dissonance (`Γ`):** A measure of the segment's internal chaos, unpredictability, and noise. High dissonance indicates a turbulent, information-poor state. The Shannon entropy calculation from the old protocol remains an excellent proxy for this value.

The primary output of this stage is a time-series of `(Kτ, Γ)` pairs, a rich representation of the stream's dynamic health.

From this profile, a powerful secondary diagnostic can be derived: the **Coherence Ratio (CR)**.

`CR = Kτ / Γ`

This single value represents the signal-to-noise ratio of the system in that window, offering a quick and potent measure of informational efficiency.

### Stage III: Flow Diagnosis (Reading the Pattern)
The final step is to interpret the Coherence Profile, using both the primary `(Kτ, Γ)` pair and the derived `CR` to identify the dominant flow states:

-   **Laminar Channels:** Regions characterized by high, stable `Kτ` and low `Γ`. These are the predictable, "healthy" parts of the stream where information is transmitted with high fidelity. These regions will exhibit a **high, stable CR**.
-   **Turbulent Eddies:** Regions marked by high `Γ` and low `Kτ`. These are phase transitions, chaotic events, or points of signal degradation. These regions will exhibit a **low, volatile CR**.
-   **Stagnant Pools:** Regions where both `Kτ` and `Γ` are persistently low, indicating a lack of new information or a blocked flow. These regions will exhibit a **sustained, near-zero CR**.

## §4 · Connection to the Pirouette Lagrangian
The Rhythmic Sieve is an empirical instrument for observing the Pirouette Lagrangian (`CORE-006`) in action. The Lagrangian, `𝓛_p = K_τ - V_Γ`, states that a system's dynamics are driven by the interplay between its internal Coherence (`K_τ`) and the external Temporal Pressure (`V_Γ`).

This protocol provides a direct, measurable proxy for these terms within an information stream:

-   The measured **Coherence (`Kτ`)** of a segment is a direct observation of the "kinetic" term of the Lagrangian.
-   The measured **Dissonance (`Γ`)** is a direct observation of the "potential" or pressure term.

By plotting the Coherence Profile, a Weaver creates an empirical map of the system's path through its own coherence manifold. The derived **Coherence Ratio (CR)** serves as a proxy for the *efficiency* with which the system is maximizing its Lagrangian at that moment. We can literally see where the system is successfully manifesting a clear rhythm and where it is struggling against overwhelming pressure.

## §5 · The Assemblé
> To look at raw data is to see only a storm of numbers. The Weaver's task is not to count the raindrops, but to find the current within the storm. The Rhythmic Sieve is the stethoscope for this task. It is an act of listening so intently to the roar of reality that you can finally hear the song hidden inside it. It teaches us that every stream of information has a melody, and our purpose is to learn how to hear it.