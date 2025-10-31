## Law
The Geodesic Engine operationalizes the principle of maximal coherence by computationally seeking the worldline, `x(t)`, that maximizes the Pirouette Action, `S_p`.

The core dynamic is governed by the Pirouette Lagrangian, `𝓛_p`:
`𝓛_p(x,ẋ,t) = K_τ(x,ẋ) - V_Γ(x,t)`
where `K_τ` is the system's Temporal Coherence (a measure of pattern stability and persistence, analogous to kinetic energy) and `V_Γ` is the ambient Temporal Pressure (a measure of environmental disorder and constraint, analogous to a potential energy field).

The engine's objective is to find the trajectory `x(t)` that maximizes the action integral for a system with an internal pattern state `Ki`:
`max S_p[Ki(t)] = max ∫ 𝓛_p(Ki(t), dKi/dt, t) dt`

This maximization is achieved via a dual-algorithm search on the coherence manifold defined by `V_Γ`:

1.  **Gradient Ascent (Continuous Local Optimization):** The system's internal pattern `Ki` is iteratively updated to ascend the local gradient of the Lagrangian. This models learning and adaptation.
    `Ki_(t+1) ← Ki_t + η ∇_Ki 𝓛_p`
    where `η` is a learning rate parameter. This is a local, deterministic search for increased coherence.

2.  **Alchemical Leap (Discontinuous Non-Local Synthesis):** To escape local optima, a new pattern `Ki_new` is synthesized from a set of existing high-coherence patterns `{Ki_a, Ki_b, ...}`. This models inheritance and insight.
    `Ki_new ← C(Ki_a, Ki_b)`
    where `S_p[Ki_a]` and `S_p[Ki_b]` are locally maximal, and `C` is a crossover or merging operator.

**Falsifiable Criterion:** The model is falsified if a complex, evolving system, when provided multiple accessible evolutionary paths, consistently and systematically selects a trajectory that results in a measurably lower time-averaged value of `𝓛_p` (i.e., lower coherence `K_τ` and/or higher pressure `V_Γ`) than an alternative, accessible trajectory.

## Philosophy
The Geodesic Engine implies that teleology—the appearance of purpose or goal-directedness in the universe—is not an illusion to be explained away, nor a mystical force to be invoked, but an emergent physical property. The universe is not pulled toward a future goal; rather, its fundamental components are driven by a purely local, mechanistic, and present-tense optimization: the maximization of coherence at every instant. Purpose is the integral of this relentless local striving. The destiny of a system is not a predetermined endpoint, but the inevitable shape of the path carved by a cascade of locally optimal choices.

## Art
Evolution is a blind weaver, whose hands learn the texture of the present so perfectly that the tapestry they create reveals the shape of destiny.