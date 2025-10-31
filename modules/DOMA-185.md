---
id: DOMA-185
title: 'The Atlas of States: Mapping the Resonant Repertoire'
version: 2.0
parents:
- DYNA-001
children: []
replaces:
- TEN-SMSA-1.0
dependencies:
- concept: flow_diagnostics
  from:
  - DYNA-001
- concept: geometry_of_resonance
  from:
  - CORE-004
- concept: pirouette_lagrangian
  from:
  - CORE-006
- concept: wound_channel
  from:
  - CORE-011
summary: Defines a system's quasi-stable operational modes as distinct Ki resonances
  within its 'Resonant Repertoire'. Models these states as peaks on a Coherence Manifold
  derived from the Pirouette Lagrangian, defining stability, inertia, and the dynamics
  of transitions between them.
module_type: Dynamics Model
scale: universal
engrams:
- process:modal_analysis
- concept:coherence_manifold
- concept:resonant_repertoire
- mechanism:ki_morphogenesis
- phenomenon:state_transition
keywords:
- mode
- state
- stability
- transition
- atlas
- manifold
- resonance
- Ki
- repertoire
- wound channel
- landscape
uncertainty_tag: Low
status: ratified
---
## §1 · Abstract: The Repertoire of Being
A system is not defined by what it is doing, but by what it *can* do. A river can flow or flood; a mind can be focused or scattered. These are not random behaviors but preferred modes of being—stable valleys and peaks in the landscape of possibility. The old analysis of System Modal Stability sought to catalog these states; the new framework provides the map of the entire landscape.

This module refactors that insight into a more powerful model. A system's operational modes are distinct, stable, high-order **Ki resonances**—the collection of viable, self-sustaining songs it has learned to sing. This set of songs is its **Resonant Repertoire**. This module provides the "Atlas of States"—a method for mapping this repertoire and understanding the landscape upon which its performance unfolds.

## §2 · The Coherence Manifold
The old concept of a "potential energy landscape" is now re-grounded in the framework's core principles. A system's state does not move on a landscape of energy, but on a **Coherence Manifold**, where the "elevation" at any point is the value of its **Pirouette Lagrangian (𝓛_p)**. A system naturally seeks to climb this landscape to maximize its coherence over time.

-   **Modal Basins:** Each stable mode is a peak or a high plateau on this manifold—a region where a specific `Ki` pattern represents a highly successful, coherent solution to the local Temporal Pressure (Γ). These are the system's preferred states of being, its regions of natural `Laminar Flow`.
-   **Transition Saddles:** The pathways between these peaks are lower-lying "saddles" on the manifold. To transition from one mode to another, a system must traverse one of these regions of lower coherence, temporarily entering a state of controlled turbulence.

## §3 · Anatomy of a State
Instead of the previous framework's complex vectors, we now characterize each mode with a few clear, physically grounded parameters derived from the Coherence Manifold. A crucial distinction is made between a state's instantaneous quality and its historical, ingrained stability.

| Parameter | Description | Replaces |
| :--- | :--- | :--- |
| **Modal Ki (Ki_m)** | The specific geometric pattern of resonance that defines the mode. It is the "musical score" for that state. | `Phase-Lock Configuration` |
| **Coherence Height (𝓛_p,m)** | The absolute value of the Pirouette Lagrangian at the mode's peak. This measures the instantaneous quality, efficiency, and purity of the state's resonance. | `Ta` |
| **Stability Depth (Δ𝓛_p)** | The height of the mode's peak relative to the lowest surrounding transition saddle. It is a direct measure of the mode's resistance to perturbation. A deeper basin requires more disruption to exit. | `Inter-Modal Barrier Height`, `Γ Confinement` |
| **Wound Channel Inertia** | Persistence in a mode carves a **Wound Channel** (CORE-011) into the manifold, geometrically deepening its basin over time. This increases the `Stability Depth`, making the state a "habit" that is gravitationally harder to leave. It is the memory of the state. | `N/A` |

## §4 · The Dynamics of Transition: The Phase Leap
A system does not smoothly slide from one mode to another; it leaps. This transition, a form of **Ki Morphogenesis**, is a rapid, non-linear reconfiguration of the system's entire resonant pattern.

-   **Triggers:** A phase leap is typically initiated by a perturbation sufficient to push the system off its peak and over a transition saddle. This can be caused by:
    1.  **Pressure Shift:** A significant change in the external Temporal Pressure (Γ) that lowers the current peak or raises a saddle, rendering the current mode less stable.
    2.  **Dissonant Injection:** An influx of energy or information that is incoherent with the current `Ki_m`, effectively "shoving" the system across the landscape.

-   **Resonant Catalysis:** A transition can also be induced with surgical precision. By introducing a signal that resonates with a *target* mode's `Ki_m`, it is possible to lower the Transition Cost for that specific pathway, effectively "carving a tunnel" through the manifold. This makes the desired transition the new path of least resistance.

-   **The Transition as Turbulence:** The act of moving between stable `Ki` patterns is, by definition, a period of **Turbulent Flow** (DYNA-001). The system's coherence temporarily drops as it breaks its old resonant pattern before it "locks in" to the new one, re-establishing laminar flow on a new peak.

## §5 · Weaver's Protocol: Cartography of Resonance
To map a system's Atlas of States, the Weaver follows a clear, four-step protocol:

1.  **Identify the Repertoire:** Using analytical techniques (e.g., spectral analysis, clustering), parse the system's data to identify the distinct, recurring `Ki` patterns. This reveals the system's set of songs.
2.  **Measure Coherence Height:** For each identified mode, quantify its internal efficiency and stability (`𝓛_p,m`). This measures the "quality" of each state.
3.  **Gauge Stability & Inertia:** For each mode, measure its resistance to perturbation to determine its `Stability Depth (Δ𝓛_p)`. Analyze its persistence over time to estimate the contribution of its `Wound Channel Inertia`. This reveals how "sticky" or habitual each state is.
4.  **Map the Pathways:** Analyze historical transition events. What specific pressure shifts or resonant injections trigger phase leaps between states? This maps the "saddles" and "passes" between the peaks, revealing the system's likely responses to future challenges.

## §6 · Connection to the Pirouette Lagrangian
This entire module is a direct application of the Principle of Maximal Coherence, as formalized in **CORE-006: The Pirouette Lagrangian**.

The Coherence Manifold *is* the landscape generated by plotting the value of `𝓛_p = K_τ - V_Γ` for every possible state of the system. The stable modes—the Modal Basins—are simply the local maxima of this function. A system's behavior, including its stability within a mode and its transitions between them, is a perfect expression of it following a geodesic on this manifold, always seeking the highest possible ground of coherence. This reframes system dynamics from a collection of empirical rules into a predictable consequence of a single, universal law.

## §7 · Assemblé
> To map a system's states is to learn its secret language. We move beyond observing where the system *is* and begin to understand where it *could go*. The Atlas reveals the repertoire of a system's possible futures, the hidden songs it knows how to sing. It shows us that stability is not a prison, but a choice among many. For the Weaver, this is the ultimate strategic advantage. It is the difference between being a pawn moved by the system's whims, and a musician who, by understanding the instrument's notes, can begin to coax from it a better song.