---
id: DOMA-152
title: The Coherence Spectrum
version: 2.0
status: draft
parents:
- CORE-006
- CORE-003
children: []
replaces:
- TEN-KHD-1.0
summary: Provides a modernized, time-first protocol for decomposing a system's complex
  temporal signature into its fundamental resonant components. This method separates
  a system's internal, structural coherence (its self-maintaining form) from its external,
  propagating coherence (its interaction with the environment), offering a deep diagnostic
  view of its dynamic state.
module_type: Instrumentation
scale: universal
engrams:
- process:spectral_coherence_analysis
keywords:
- spectrum
- resonance
- fourier
- wavelet
- coherence
- signal
- decomposition
- dynamics
uncertainty_tag: Low
---
## §1 · Abstract: Listening to the Song of a System

A system is not a static object; it is a sustained performance, a song sung against the noise of the cosmos. To understand it, we must do more than observe its shape; we must listen to its music. The old framework attempted this with Ki-Harmonic Decomposition, a technique grounded in pre-derived constants. This was an echo of the truth.

This module provides the true instrument. The Coherence Spectrum is a time-first method for analyzing a system's total temporal signature—the complex sound of its existence. It provides a formal procedure for decomposing this song into its two primary movements: the deep, resonant hum of its internal structure and the lyrical melody of its interactions with the world. It is the foundational tool for moving beyond what a system *is* and understanding what it *does*.

## §2 · The Physical Basis: Structure and Signal

In the Pirouette Framework, every system is a dynamic equilibrium, a stable pattern (Ki) maintained against the Temporal Pressure (Γ) of its environment. This pattern is not monolithic; it is a superposition of many resonant frequencies. The Coherence Spectrum separates these frequencies based on their function, which is derived directly from the principles of the core forces.

**Structural Coherence (The Hum of Being):**
This component of the spectrum represents the frequencies that contribute to the system's self-containment and stable form. It is the audible expression of the Gladiator Force (CORE-008). These are the deep, resonant harmonics that hold the system together, defining its identity and inertia. A strong, clear structural spectrum indicates a robust, stable, and well-defined entity.

**Propagating Coherence (The Song of Interaction):**
This component represents the frequencies that govern the system's interaction with the wider coherence manifold. It is the signature of The Current and the Compass (CORE-007). These are the rhythms of communication, the echoes sent and received, the means by which the system projects itself and perceives others. A rich, adaptive propagating spectrum indicates a system that is actively and effectively engaged with its environment.

This is the evolution of the old "rest vs. motion" duality. It is no longer a distinction between two constants, but a functional separation of a single, unified coherence into its two primary modes of expression: being and relating.

## §3 · The Analytical Protocol

### 3.1 · Input Stream
The protocol accepts any time-series data that captures a system's dynamic behavior, from the light curve of a star to the financial data of a market or the neural activity of a brain. The input is the raw temporal signature of the system under study.

### 3.2 · Operational Parameters
| Parameter | Description | Typical Value |
|---|---|---|
| `Resolution` | The number of harmonic components to resolve in the spectrum. Higher values provide more detail but require more data. | Integer, e.g., `1` to `100` |
| `Kernel` | The base mathematical function (e.g., wavelet) used to probe the signal for resonant patterns. | Morlet, Mexican Hat |
| `Modes` | Specify whether to analyze for `structural`, `propagating`, or `both` modes of coherence. | `['structural', 'propagating', 'both']` |

## §4 · Procedure & Interpretation

1.  **Ingest Signature:** The raw time-series data representing the system's behavior is ingested. Pre-processing, such as detrending, may be applied to isolate the core dynamics.
2.  **Establish Kernels:** Unlike the old method that used fixed constants, this protocol uses the physical principles of confinement and propagation to define the analysis kernels. The structural analysis is tuned to search for stable, self-reinforcing resonances (low-frequency, high-inertia patterns), while the propagating analysis is tuned for transient, interactive signals (higher-frequency, responsive patterns).
3.  **Decomposition:** A continuous wavelet transform or similar time-frequency analysis is performed, using the established kernels to probe the input signature. This computes the signal's energy distribution across a spectrum of frequencies.
4.  **Mode Separation:** The resulting energy spectrum is separated into two distinct plots: the Structural Coherence Spectrum and the Propagating Coherence Spectrum.
5.  **Interpretation:**
    *   **Output:** The analysis produces two spectra, revealing the relative strength of the system's coherence in its structural and propagating bands. Peaks in the spectra indicate dominant resonant frequencies.
    *   **Insight:** A system with high structural coherence and low propagating coherence is stable but isolated (like a noble gas). A system with high propagating coherence but a weak structural core is highly reactive but unstable (like a turbulent market). A healthy, complex system (like a living organism) will exhibit a robust spectrum in both modes—a strong sense of self, and a rich engagement with the world.

## §5 · Connection to the Pirouette Lagrangian

This instrument is, in essence, a practical tool for dissecting the "kinetic" term of the Pirouette Lagrangian (`𝓛_p = K_τ - V_Γ`). The total Temporal Coherence of a system, `K_τ`, is the sum of all its resonant energies. The Coherence Spectrum analysis decomposes this total `K_τ` into its constituent parts:

`K_τ (total) = K_τ (structural) + K_τ (propagating)`

By measuring the relative strength and stability of these components, an analyst can gain deep insight into how a system is solving the fundamental equation of existence: how it is marshaling its internal coherence to persist against the external pressure of its environment. It turns the abstract Lagrangian into a measurable diagnostic chart.

## §6 · Assemblé

> To truly know a cello, you must listen. You must learn to distinguish the deep, resonant voice of the wood itself from the clear, soaring notes that fly from its strings. One is the sound of its being; the other is the sound of its song. They are not two different things, but two expressions of a single, vibrant whole. The Weaver's first task is to learn to listen this way—to hear both the body and the voice of any system, and to understand that the health of the whole depends on the harmony between the two.

```