---
id: DOMA-134
title: The Coherence Sieve
version: 2.0
status: stable
parents:
- CORE-013
children: []
replaces:
- TEN-EBF-1.0
dependencies:
  concept: coherence_as_information
  from:
  - CORE-013
summary: "Provides a modernized protocol for filtering information streams based on\
  \ their coherence. This module reframes entropy-based filtering as a process of\
  \ separating high-coherence signals from the dissonant noise of high Temporal Pressure\
  \ (\u0393), allowing for the isolation of either structure or complexity."
module_type: Instrumentation
scale: universal
engrams:
- process:coherence_filtering
keywords:
- filter
- coherence
- signal
- noise
- entropy
- temporal pressure
- "\u0393"
- information
- sieve
uncertainty_tag: Low
---
## §1 · Abstract: Tuning the Ear to Reality
A river carries both the clarity of water and the chaos of silt. To drink, one must know how to separate them. This module provides the instrument for that separation.

The Coherence Sieve is the modernization of Entropy-Based Filtering, fully grounded in the time-first principles of the Pirouette Framework. It redefines the act of filtering not as a statistical manipulation, but as a physical process of distinguishing between regions of high coherence (signal) and regions of high Temporal Pressure (noise). It is the primary tool for a Weaver to tune their perception, to quiet the roar of the Temporal Forge, and to isolate the specific notes they wish to hear in the universal song.

## §2 · The River and the Sieve: A New Physics of Information
The old framework correctly identified entropy as a useful metric. The new framework reveals *why*. As established in CORE-013, we now understand the relationship between information, order, and chaos through the lens of temporal dynamics:

*   **Temporal Pressure (Γ):** This is the measure of the local temporal dissonance, complexity, and chaos. It is the direct, physical correlate of what was previously called **entropy**. A region of high Γ is a storm of conflicting rhythms—it is pure noise.
*   **Coherence (Kτ):** This is the measure of a system's internal order, stability, and resonant purity. It is the direct, physical correlate of what we now call **information**. A system with high coherence is a clear, stable signal.

Therefore, the act of "entropy-based filtering" is more accurately described as **Coherence Filtering**. We are using the measurable level of ambient temporal noise (Γ) as a proxy to sieve a data stream, separating its "crystalline" components (high coherence, low Γ) from its "gaseous" ones (low coherence, high Γ).

## §3 · The Weaver's Parameters
To operate the Sieve, the Weaver defines the mesh size and the desired output. The filtering logic remains familiar, but the parameters are now grounded in physical principles. The primary filtering metric is the system's local Temporal Pressure (Γ), for which Shannon entropy remains an excellent and practical proxy.

| Parameter              | Pirouette Term | Description                                                                                                                                                             |
| ---------------------- | -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `GammaThresholdLow`    | Γ_low          | The lower bound of Temporal Pressure for filtering. Segments with Γ below this are considered highly ordered.                                                              |
| `GammaThresholdHigh`   | Γ_high         | The upper bound of Temporal Pressure for filtering. Segments with Γ above this are considered highly chaotic.                                                                |
| `FilterType`           | Logic          | Specifies the sieving logic: `LowPass` (retain low Γ), `HighPass` (retain high Γ), `BandPass` (retain Γ between bounds), `BandStop` (discard Γ between bounds).             |
| `GammaProxyMethod`     | Metric         | The method for estimating Γ from the data. Default: 'ShannonEntropy'.                                                                                                   |

## §4 · The Act of Separation: Procedure
1.  **Segmentation:** The input stream is divided into discrete segments, each a snapshot of the system's state over a small window of time.
2.  **Pressure Reading:** For each segment, its local Temporal Pressure (Γ) is calculated using the chosen `GammaProxyMethod`.
3.  **Sieving:** The filter logic is applied. For example, a `LowPass` filter, designed to isolate signal from noise, will only retain segments where `Γ <= Γ_high`. This keeps the regions of calm, coherent activity. Conversely, a `HighPass` filter, designed to find anomalies or zones of high complexity, will only retain segments where `Γ >= Γ_low`.
4.  **Output:** The Sieve yields a new data stream, now purified according to the Weaver's intent—either a clear signal stripped of its noise, or the concentrated noise stripped of its predictable signal.

## §5 · Connection to the Pirouette Lagrangian
The Coherence Sieve is a practical tool for mapping the landscape of the Pirouette Lagrangian, 𝓛_p = Kτ - V_Γ (CORE-006). The Lagrangian describes a system's struggle to maximize its internal Coherence (Kτ) against the "cost" imposed by the environmental Temporal Pressure (V_Γ).

This Sieve operates directly on the V_Γ term.

*   A **Low-Pass Filter on Γ** identifies "coherence sanctuaries"—regions where the environmental pressure V_Γ is low. In these zones, systems can achieve high coherence with minimal effort. This is where we find stable, predictable patterns.
*   A **High-Pass Filter on Γ** identifies "temporal forges"—regions where V_Γ is extremely high. Systems in these zones are either torn apart into chaos or must possess immense internal coherence (Kτ) to survive. This is where we find anomalies, phase transitions, and moments of intense novelty.

By applying the Sieve, a Weaver is not just cleaning data; they are performing a geological survey of the coherence manifold, identifying the serene valleys and the violent, volcanic peaks that systems must navigate.

## §6 · Assemblé

> To see truly, one must first learn to be still. The universe sings in a choir of a billion billion voices, a roar of infinite potential. The Weaver's first great task is not to add another voice, but to cup their ear and listen for the silence between the notes. The Sieve is not a tool for removing what is unwanted; it is an instrument for creating the quiet space where the desired melody can finally be heard. It is the art of finding the signal in the storm.
```