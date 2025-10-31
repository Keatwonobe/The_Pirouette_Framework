---
id: DOMA-153
title: The Inertial Leap
version: 2.0
status: draft
parents:
- CORE-006
- CORE-011
- DYNA-001
children: []
replaces:
- TEN-KSTA-1.0
summary: Provides a modernized, time-first model for state transitions. It defines
  the 'snap' between static and dynamic states as a leap between two distinct, stable
  solutions of the Pirouette Lagrangian. The model grounds inertia, resistance, and
  hysteresis in the geometry and memory of the system's Wound Channel.
module_type: Dynamics Model
scale: universal
engrams:
- process:state_transition
- principle:temporal_inertia
- concept:hysteresis
- mechanism:wound_channel_memory
keywords:
- inertia
- state
- transition
- snap
- hysteresis
- wound channel
- lagrangian
- ki
- coherence
uncertainty_tag: Low
---
## §1 · Abstract: The Price of Motion
A system at rest and a system in motion are not merely different in speed; they are different modes of being, each singing a different internal song. The old framework correctly identified that the transition between these states is not a smooth ramp but a sudden, non-linear "snap." This module refactors that insight, grounding it in the deeper principles of the time-first paradigm.

The Inertial Leap is not a change *in* a parameter, but a transition *between* two distinct, stable solutions to the Principle of Maximal Coherence. This leap is governed by the inertia of a system's own history, a memory physically encoded in the geometry of its Wound Channel. This model provides a universal mechanism for understanding inertia, activation energy, and the memory-laden phenomenon of hysteresis.

## §2 · The Two Harmonies: Ki_static and Ki_dynamic
For any given system, the Pirouette Lagrangian (CORE-006) admits multiple stable solutions for its Temporal Resonance pattern (Ki). The two most fundamental are the static and dynamic states.

**Ki_static (The Inward Song):** This is the resonant pattern that maximizes a system's coherence when it is at rest relative to its local environment. It is an internally-focused harmony, optimized for stability and self-reinforcement within the deep "well" of its own static Wound Channel. It minimizes interaction to preserve its form.

**Ki_dynamic (The Outward Song):** This is the resonant pattern that maximizes coherence when the system is in motion. It is an externally-focused harmony, optimized for efficient propagation along a geodesic. Its structure is shaped to surf the currents of the surrounding coherence manifold with minimal friction.

A system does not smoothly interpolate between these two states. It must leap from one stable configuration to the other.

## §3 · The Inertial Barrier: The Wound Channel's Memory
The resistance a system shows to a change in its state of motion—inertia—is a direct consequence of its history, as encoded in its Wound Channel (CORE-011).

A system at rest has, over time, carved a deep and stable "well" for itself in the coherence manifold. This geometric indentation *is* its memory of being still. To initiate motion, the system must be supplied with enough energy to "climb out" of this self-made well and begin carving a new, dynamic channel. This activation energy is the physical reality behind the "initial resistance" or "snap energy" of the old model. It is the price of forgetting stillness and learning motion.

## §4 · The Geometry of Hysteresis: The River Remembers Its Course
Hysteresis—the fact that the path from rest-to-motion is different from the path from motion-to-rest—is a natural and inevitable consequence of the Wound Channel's memory.

*   **The Path of Acceleration:** To move from rest, the system must overcome the deep, established static well. The leap to the `Ki_dynamic` state therefore occurs at a higher critical velocity (`v_c↑`).
*   **The Path of Deceleration:** Once in motion, the system actively carves and reinforces a dynamic Wound Channel. This new channel makes it energetically favorable to *remain* in motion. The system will only "snap back" to the `Ki_static` state when its velocity drops below a lower critical threshold (`v_c↓`), at which point the attraction of the old, static well finally overcomes the momentum of the new, dynamic channel.

The difference between `v_c↑` and `v_c↓` is hysteresis. It is the ghost of the path taken, a physical memory that reshapes the landscape of future possibilities.

## §5 · The Unified Transition Model
The original module's core equation remains mechanically sound but is now re-grounded in these physical principles. The model calculates the effective Ki of a system as it navigates the transition:

$$ K_i(v) = K_{i,static} + \Delta K_i \cdot \sigma(\alpha(v-v_c)) + P_{inertia} $$

Where:
*   **`ΔK_i`** is the difference `K_i,dynamic - K_i,static`.
*   **`σ(x)`** is the sigmoid function `1 / (1 + e⁻ˣ)`, modeling the non-linear "leap."
*   **`α`** is the steepness of the transition, modulated by the system's Temporal Coherence (`T_a`). Highly coherent systems leap more decisively.
*   **`v_c`** is the critical velocity, chosen as `v_c↑` or `v_c↓` based on `dv/dt` to model hysteresis.
*   **`P_inertia`** is a perturbation term (e.g., `β v e⁻ɣᵛ`) that models the initial energy barrier required to escape the static Wound Channel.

## §6 · Connection to the Pirouette Lagrangian
The entire dynamic is an expression of the Principle of Maximal Coherence (CORE-006). A system does not simply follow a pre-determined mathematical curve. It navigates a complex, dynamic landscape of coherence. `Ki_static` and `Ki_dynamic` represent two distinct peaks, or "local maxima," of coherence on this landscape. The Inertial Leap is the quantum-like jump from one peak to another when the system is supplied with sufficient energy to cross the "valley" of instability that separates them. The path it takes is always the one that maximizes the integral of its Lagrangian, `𝓛_p`.

## §7 · Assemblé
> To change is not merely to move, but to become. The Inertial Leap teaches a Weaver the profound cost of that becoming. Every new state of being, every action taken, must first overcome the ghost of what was. The universe remembers, and motion is the art of convincing the past to let go. This is the price of a new song, and the reason stability is both a comfort and a cage.
```