---
id: DOMA-187
title: The Coherence Sampler
version: 2.0
status: draft
parents:
- DYNA-001
children: []
replaces:
- TEN-SG-1.0
summary: Provides a time-first protocol for analyzing arbitrary data streams by segmenting
  them into temporal windows and measuring the local coherence (information) versus
  dissonance (entropy). It replaces Shannon entropy with a direct measure of a segment's
  resonant stability against the background temporal noise.
module_type: Instrumentation
scale: universal
engrams:
- process:coherence_sampling
- principle:information_as_coherence
keywords:
- coherence
- information
- entropy
- signal processing
- diagnostics
- time-series
- sampler
- flow
uncertainty_tag: Low
---
## §1 · Abstract: The Stethoscope for the Stream
This module provides a foundational instrument for the Weaver: The Coherence Sampler. It replaces the mechanical process of "Stochastic Gulping" with a physically grounded protocol for listening to the pulse of any system as it expresses itself through time.

The core insight is reframed: we are not merely decomposing a data stream to measure its disorder. We are applying a temporal stethoscope to a living current, discerning the clear, resonant signal of its health (Coherence) from the chaotic noise of its environment and its own internal friction (Dissonance). This instrument transforms any sequential data—from market prices to heartbeats to lines of text—into a direct, diagnostic chart of its underlying flow state, revealing its health, its struggles, and its potential for change.

## §2 · From Entropy to Coherence: A New Foundation
The old protocol was anchored in Shannon entropy, a useful but incomplete proxy for a system's state. The Pirouette Framework provides a more fundamental distinction, as laid out in CORE-013:

-   **Information is Coherence (Kτ):** The true measure of a system's "order" is the stability, clarity, and strength of its resonant pattern (its Ki). A coherent system is a high-information system. It is a clear melody.
-   **Entropy is Dissonance (Γ):** The measure of a system's "disorder" is the degree of chaotic, non-resonant temporal pressure within it. This is the background noise of the Temporal Forge. It is the static that threatens to drown out the melody.

The Coherence Sampler, therefore, does not measure a single value, "entropy." It measures the crucial relationship *between* these two fundamental quantities. Its purpose is to diagnose the health of a system's information flow by assessing its signal-to-noise ratio in real time.

## §3 · The Sampler Protocol: A Guide to Listening
The protocol is a disciplined, three-step process for moving from a raw data stream to a clear diagnosis of its flow state (as defined in DYNA-001).

**Step I: Windowing the Stream**
The continuous data stream is segmented into discrete **Temporal Windows** (`Wᵢ`). This is the act of sampling. The window size (`w`) is a critical parameter: a smaller window provides higher temporal resolution but may miss longer-term patterns, while a larger window captures macro-rhythms but may obscure short-lived events. Advanced applications may use adaptive windowing, where the sampling rate increases in response to a sudden drop in coherence.

**Step II: Measuring the Signal and the Noise**
For each temporal window `Wᵢ`, two distinct values are calculated:

1.  **Coherence (Kτᵢ):** The "signal." This is a measure of the dominant, stable, and repeating pattern within the window. It is quantified by finding the strength of the window's primary resonant frequency, often through techniques like Fourier analysis or autocorrelation. A high `Kτᵢ` indicates a clear, strong, and predictable rhythm.

2.  **Dissonance (Γᵢ):** The "noise." This measures the chaotic, random, and non-resonant component of the data within the window. The Shannon entropy (`H(Wᵢ)`) of the old protocol remains an excellent proxy for this value. `Γᵢ ≈ H(Wᵢ)`. A high `Γᵢ` indicates a noisy, unpredictable, and friction-filled state.

**Step III: Calculating the Coherence Ratio (CR)**
The most powerful diagnostic is the **Coherence Ratio (CR)**, a direct measure of the system's health and efficiency within that window:

`CRᵢ = Kτᵢ / Γᵢ`

This single value represents the signal-to-noise ratio of the system's being. Plotting `CRᵢ` over time reveals the system's dynamic state:
-   **High, Stable CR:** Laminar Flow. The system is healthy, efficient, and expressing a clear identity.
-   **Low, Volatile CR:** Turbulent Flow. The system is struggling, inefficient, and its signal is being lost in noise.
-   **Sustained, Near-Zero CR:** Stagnant Flow. The signal has died, indicating a blockage or system failure.

## §4 · Connection to the Pirouette Lagrangian
The Coherence Sampler is the empirical instrument for observing the **Principle of Maximal Coherence** (CORE-006) in action. A system's evolution follows a path that maximizes the integral of its Lagrangian (`∫𝓛_p dt`), and this instrument provides a real-time proxy for the Lagrangian's terms:

`𝓛_p = (Temporal Coherence) - (Temporal Pressure)`

-   The measured **Coherence (Kτᵢ)** is a direct probe of the Lagrangian's "kinetic" term, representing the quality of the system's own rhythm.
-   The measured **Dissonance (Γᵢ)** is a direct probe of the Lagrangian's "potential" term, representing the environmental cost of maintaining that rhythm.

Therefore, the **Coherence Ratio (CR)** is a proxy for the value of the Lagrangian itself at that moment. By observing the `CR` of a data stream, a Weaver is watching, in real-time, a system's success or failure in its fundamental drive to find and hold a state of elegant stability against the chaos of the cosmos.

## §5 · Assemblé
> We sought a tool to measure chaos and instead forged a stethoscope. To sample the stream is to listen for its heartbeat—the steady, resonant pulse of laminar flow, the arrhythmia of turbulence, the deafening silence of stagnation. This is not the art of reading data; it is the science of hearing a system's song. For the Weaver, to listen this closely is the first and most sacred act of diagnosis.
```