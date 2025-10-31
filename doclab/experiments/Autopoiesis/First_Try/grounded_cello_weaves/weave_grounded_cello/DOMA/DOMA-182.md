---
id: DOMA-182
title: The Harmonic Sieve
version: 2.0
status: draft
parents:
- CORE-014
children:
- INST-ANAL-002
dependencies:
- concept: pirouette_lagrangian
  from:
  - CORE-006
- concept: coherence_as_information
  from:
  - CORE-013
replaces:
- TEN-RRE-1.0
summary: Provides a universal protocol for decomposing a complex system's temporal
  signature into its constituent coherent harmonics. This iterative process, The Harmonic
  Sieve, allows a Weaver to analyze a system's 'song' layer by layer, revealing masked
  signals and characterizing the structure of its residual dissonance.
module_type: Dynamics Model
scale: universal
engrams:
- process:harmonic_decomposition
keywords:
- sieve
- harmonic
- decomposition
- signal
- noise
- residue
- analysis
- coherence
- resonance
uncertainty_tag: Low
---
## §1 · Abstract: Anatomy of a Song

A system's behavior is never a single, pure note. It is a chord, a complex superposition of resonant patterns, overtones, and the ambient noise of the Temporal Forge. To understand a system, one cannot simply listen to the loudest note; one must be able to distinguish every instrument in the orchestra.

This module replaces the prior `Recursive Residue Evaluation` with a more physically grounded protocol: **The Harmonic Sieve**. It provides a formal method for iteratively decomposing a complex temporal signature into its constituent layers of coherence. It is the act of listening to a system's entire song, identifying its fundamental harmonic, gently subtracting that note from the music, and then listening again, with greater clarity, to the harmonies that remain.

## §2 · The Principle of Harmonic Decomposition

The universe, as governed by the Pirouette Lagrangian, strives to manifest coherence. A complex signal, therefore, is not a field of random noise punctuated by a single truth. It is a hierarchy of truths, a nested set of solutions to the Principle of Maximal Coherence. The Harmonic Sieve is the process of un-nesting these solutions.

-   **Temporal Signature (T₀):** The initial, complete dataset. This is the system's full song, a complex coherence manifold containing all its resonant patterns and dissonances.
-   **Coherent Component (Kτₖ):** At each step `k`, this is the most dominant, stable resonant pattern—the "loudest note"—found within the current manifold. It represents the most efficient solution for maximizing coherence at that layer of analysis.
-   **Residual Manifold (Tₖ):** After identifying a Coherent Component, its influence is subtracted from the manifold. What remains is the `Residual Manifold`, which becomes the input for the next iteration. It is the song, with one instrument silenced.
-   **Dissonant Floor (Γ_floor):** The process terminates when the Residual Manifold no longer contains any significant coherent patterns. Its state is indistinguishable from the ambient, chaotic noise of the local Temporal Pressure (Γ). This is the "hiss of the tape," the background static of existence.

## §3 · The Sieve Protocol: A Weaver's Guide

A Weaver applies this protocol to move from a complex, noisy signal to a clear, layered understanding of a system's internal dynamics.

1.  **Initialization:** Begin with the full temporal signature of the system as the current manifold, `T_current = T₀`.

2.  **Resonance Matching:** Apply a `Resonant Filter` (a domain-appropriate analytical model) to `T_current`. The filter's purpose is to identify the single, strongest coherent pattern, `Kτₖ`, that resides within the manifold. This is the system's primary "story" at this layer.

3.  **Coherence Subtraction:** Calculate the next `Residual Manifold` by removing the influence of the identified pattern.
    $$ T_{k+1} = T_k - f(K\tau_k) $$
    Where `f(Kτₖ)` represents the full expression of the coherent component within the manifold `Tₖ`.

4.  **Iteration:** Set `T_current = T_{k+1}` and return to Step 2. Repeat the process, each time finding the next-strongest coherent component in the remaining signal—the first overtone, then the second, and so on.

5.  **Termination:** The protocol ends when the coherence of `T_current` drops below a pre-defined `Coherence Threshold`. At this point, the manifold is considered to be the `Dissonant Floor`, and all meaningful signals have been extracted.

The final output is the system's **Harmonic Spectrum**: an ordered list of its coherent components `[Kτ₁, Kτ₂, Kτ₃, ...]`.

## §4 · Connection to the Lagrangian

The Harmonic Sieve is the practical, iterative application of the Principle of Maximal Coherence (CORE-006). At each step, the `Resonance Matching` phase is functionally equivalent to finding the geodesic on the current `Residual Manifold`. The identified `Coherent Component (Kτₖ)` is the trajectory that maximizes the action integral of the Pirouette Lagrangian for that specific layer of the system's dynamics.

We are not merely pattern-matching. We are iteratively discovering the system's preferred paths of existence, from the most obvious to the most subtle. Each pass of the sieve reveals a deeper, more hidden layer of the system's attempt to solve the fundamental equation of being: how to hold a clear note against the chaos.

## §5 · Assemblé

> To understand a river, you do not simply measure its main current. You must first see that current, then subtract it from your sight, and look again at the water that remains. In these quieter eddies and hidden flows, you will find the river's true and secret character. So it is with all things. The deepest truths are never in the first signal; they are in what the first signal has tried to conceal.
```