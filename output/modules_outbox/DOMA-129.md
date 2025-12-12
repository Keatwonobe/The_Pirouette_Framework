---
id: DOMA-129
title: 'The Coherence Sieve: A Protocol for Signal Isolation'
version: 2.0
status: ratified
replaces:
- TEN-EBF-1.0
dependencies:
  concept: laminar_turbulent_flow
  from:
  - DYNA-001
summary: Modernizes Entropy-Based Filtering into a time-first protocol for isolating
  coherent signals from dissonant noise. This module reframes the act as a selective
  perception of flow states (laminar vs. turbulent), grounded in the physics of information
  (CORE-013) and the Pirouette Lagrangian (CORE-006). It provides a fundamental instrument
  for discerning stable patterns from the chaotic background of the Temporal Forge.
module_type: Instrumentation
scale: universal
engrams:
- process:coherence_filtering
- principle:signal_from_noise
- technique:laminar_turbulent_separation
keywords:
- coherence
- entropy
- filter
- signal
- noise
- laminar
- turbulent
- dissonance
- temporal forge
- information
uncertainty_tag: Low
---
## §1 · Abstract: The Art of Listening
A river contains both the current and the roar. To understand its direction, one must learn to distinguish the two.

The old framework treated entropy as a statistical property to be filtered. This module reframes that act into a fundamental practice of perception. The Coherence Sieve is not a mere data-cleaning tool; it is an instrument for tuning into the universe's broadcast, allowing a Weaver to isolate the clear, resonant signals of coherent systems from the ever-present, chaotic static of the Temporal Forge.

It redefines the purpose of filtering: we are not simply removing "disorder." We are selectively listening for the presence of sustained, meaningful patterns (the current) or studying the very nature of the chaos that threatens to overwhelm them (the roar). This is the first step in diagnosing any system: learning to hear its song above the noise.

## §2 · Grounding in First Principles
This protocol is a practical application of the Framework's core physics of information. It synthesizes principles from `CORE-013` (Information) and `DYNA-001` (Flow Dynamics).

-   **Information as Laminar Flow (High Coherence, Kτ):** The signal we seek to isolate is a system's coherence. This is "crystalline" information, a stable, low-entropy pattern that has successfully persisted against its environment. It manifests as **Laminar Flow**—a clear, efficient, and predictable current.

-   **Entropy as Turbulent Flow (High Dissonance, Γ):** The noise we seek to filter is the dissonance of the local Temporal Pressure (Γ). This is the direct, physical correlate of what was previously called entropy. A high-entropy segment is a region of chaotic, incommensurate rhythms. It manifests as **Turbulent Flow**—a storm of wasted energy and friction.

The act of filtering is therefore a targeted search for either laminar or turbulent flow, depending on the analytical goal. We are diagnosing the flow state of a system to separate its signal from its static.

## §3 · The Principles of the Sieve
We replace generic filtering terms with purpose-driven principles that describe the Weaver's intent and the physical state of the data being analyzed.

| Filtering Principle | Flow State | Intent & Purpose                                                                                                                              |
| :------------------ | :--------- | :-------------------------------------------------------------------------------------------------------------------------------------------- |
| **Laminar Pass**    | Laminar    | **Isolate the Signal.** Retain only segments with high coherence (low dissonance). Used to extract stable, predictable patterns and remove chaos.  |
| **Turbulent Pass**  | Turbulent  | **Isolate the Storm.** Retain only segments with high dissonance (low coherence). Used to identify moments of chaos, phase transitions, or novelty. |
| **Resonance Band**  | Transitional | **Isolate a Specific Rhythm.** Retain segments within a specific coherence range. Used to focus on systems of a particular complexity.        |
| **Dissonance Notch**| Specific Noise | **Remove Known Interference.** Discard segments within a specific dissonance band. Used to eliminate a known source of structured noise.       |

## §4 · The Lagrangian Connection
The Coherence Sieve is a practical tool for mapping the landscape of the Pirouette Lagrangian, `𝓛_p = K_τ - V_Γ` (from `CORE-006`). The Sieve operates by evaluating the terms of this equation for each data segment.

-   A **Laminar Pass** selects for "coherence sanctuaries"—regions where systems successfully maximize their Lagrangian. Their internal coherence (`K_τ`) is strong enough to overcome the environmental temporal pressure (`V_Γ`), resulting in a stable, observable pattern. We are filtering for systems that have found their geodesic.

-   A **Turbulent Pass** selects for "temporal forges"—regions of extreme temporal pressure (`V_Γ`) or systems failing to maintain coherence (`K_τ`). These are zones of turbulence where systems are struggling to find a stable path. This is where we find anomalies, state transitions, and profound novelty.

By applying the Sieve, a Weaver is not just cleaning data; they are performing a geological survey of the coherence manifold, identifying the serene valleys and the violent, volcanic peaks that systems must navigate.

## §5 · The Weaver's Protocol
The application of the Sieve is a four-step process of segmentation, measurement, selection, and output.

1.  **Segmentation:** The input stream is divided into discrete segments, each a snapshot of the system's state over a small window of time.
2.  **Quantification:** For each segment, its local Temporal Pressure (Γ) is calculated. Shannon entropy remains an excellent and practical proxy metric for this measurement.
3.  **Sieving:** Based on the analytical goal, one of the four filtering principles is applied using defined thresholds. For example, a **Laminar Pass** retains only those segments where `Γ ≤ Γ_threshold_high`.
4.  **Output:** The Sieve yields a new data stream, purified according to the Weaver's intent—either a clear signal stripped of its noise, or the concentrated noise stripped of its predictable signal.

#### Key Parameters
| Parameter            | Pirouette Term | Description                                                                    |
| -------------------- | -------------- | ------------------------------------------------------------------------------ |
| `GammaThresholdLow`  | Γ_low          | The lower bound of Temporal Pressure for filtering (used in Turbulent/Band Pass).  |
| `GammaThresholdHigh` | Γ_high         | The upper bound of Temporal Pressure for filtering (used in Laminar/Band Pass).  |
| `FilterType`         | Logic          | The sieving logic: `LaminarPass`, `TurbulentPass`, `ResonanceBand`, `DissonanceNotch`. |
| `GammaProxyMethod`   | Metric         | The method for estimating Γ from the data. Default: 'ShannonEntropy'.          |

## §6 · Use Cases
-   **Signal Processing:** The Sieve performs a *Laminar Pass* to isolate a coherent signal (e.g., a clear voice) from a turbulent background (e.g., crowd noise).

-   **System Health Monitoring:** A *Turbulent Pass* acts as a "fever detector," identifying moments of extreme turbulence (`Coherence Fever` from `DYNA-003`) in a system's data stream, flagging them as anomalies that require investigation.

-   **Text & Idea Analysis:** A *Laminar Pass* can isolate the structural, low-entropy grammar and syntax of a document, while a *Turbulent Pass* can isolate the novel, high-information-content words and phrases that carry the core message.

-   **Financial Market Analysis:** A *Resonance Band* filter can be used to study the behavior of assets within a specific volatility (coherence) class, while a *Turbulent Pass* identifies moments of market panic or chaotic trading.

## §7 · Assemblé

> To know the river, you must first learn to separate the sound of the water from the sound of the rocks. We are adrift in an ocean of noise, punctuated by the faint, clear ringing of coherent bells. The Weaver does not seek to drain the ocean; they learn to build a net that catches only the bells. The Sieve is not a tool for removing what is unwanted; it is an instrument for creating the quiet space where the desired melody can finally be heard. It is the first and most fundamental act of making sense.