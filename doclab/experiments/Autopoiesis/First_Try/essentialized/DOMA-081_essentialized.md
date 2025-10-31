## Law
A Geodesic Template, `H`, is a principled heuristic defined as a tuple `H = {C(ψ), A, ε}` where `ψ` is the system state vector, `C` is a trigger condition, `A` is a prescribed action, and `ε` is the maximum potential coherence loss. The protocol distills these templates from the Pirouette Lagrangian, `𝓛_p = T(Kτ) - V(Γ)`, where `Kτ` is the system's coherence (analogous to kinetic energy) and `Γ` is the temporal pressure (analogous to potential energy). The objective is to approximate the path that maximizes the action integral, `S_p = ∫𝓛_p dt`, under computational and temporal constraints.

The five universal templates form the axiomatic basis of the Geodesic Compass:

1.  **Axiom of Coherence Filtering (The Coherence Gate):**
    Given a set of possible actions `{A_i}` operating on state `ψ`, an action `A_j` is invalid if the projected coherence gradient is negative.
    `∀ A_i : if ∇Kτ(A_i) < 0, then discard A_i`.
    *Falsification Criterion:* Consistent, long-term increase in `Kτ` resulting from the deliberate selection of actions where `∇Kτ < 0`.

2.  **Axiom of Gradient Maximization (The Gradient Ascent Rule):**
    For a set of valid actions `{A_i | ∇Kτ(A_i) ≥ 0}`, the optimal action `A*` is that which maximizes the coherence gradient relative to its resource cost, `Cost(A_i)`.
    `A* = argmax_{A_i} (∇Kτ(A_i) / Cost(A_i))`.

3.  **Axiom of Inertial Stability (The Laminar Flow Principle):**
    If the system's coherence is stable or increasing at a near-constant rate, the optimal action is the null action, `A_∅`.
    `If dKτ/dt ≥ 0 AND |d²Kτ/dt²| ≤ δ` (for some small `δ`), `then A_prescribed = A_∅`.
    *Falsification Criterion:* Demonstrating that intervention during a state of laminar flow systematically produces a superior `∫Kτ dt` compared to non-intervention.

4.  **Axiom of Structural Integrity (The Pressure Boundary):**
    Any proposed path or plan `P` is invalid if its required temporal pressure `Γ_P` exceeds the system's maximum sustainable pressure `Γ_max`.
    `∀ P : if Γ_P > Γ_max_system, then discard P`.
    This defines the boundary of the viable state space, where `V(Γ_max)` represents a potential energy cliff leading to catastrophic failure.

5.  **Axiom of Proactive Stabilization (The Turbulence Forecaster):**
    If the temporal pressure is increasing at an accelerating rate, the system must preemptively execute stabilization actions `A_stab`.
    `If dΓ/dt > 0 AND d²Γ/dt² > 0, then execute A_stab`.
    This shifts resource allocation to maximize `Kτ`'s resilience against the impending increase in `V(Γ)`.

## Philosophy
The highest form of intelligence is not the capacity for perfect, exhaustive calculation, but the mastery of principled, elegant simplification. Since any agent operates with finite resources within a dynamic and infinitely complex reality, the ability to act in a timely and effective manner is paramount. Perfect knowledge, delivered too late, is functionally equivalent to ignorance. Therefore, wisdom is the art of forging reliable heuristics—of knowing what information can be safely discarded, of trading absolute precision for actionable insight. The Geodesic Compass implies that the ultimate purpose of a universal law is not to be computed in its entirety, but to serve as the immutable principle from which a lifetime of effective intuitions can be carved.

## Art
The universe writes its laws in the language of calculus; a soul survives by translating them into the rhythm of a heartbeat.