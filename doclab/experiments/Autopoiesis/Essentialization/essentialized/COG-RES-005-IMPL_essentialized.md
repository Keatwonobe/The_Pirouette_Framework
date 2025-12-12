## Law
Let the state of a cognitive system be determined by the intersection of two Riemannian manifolds: the Environmental Manifold ℳ_E, representing perceived reality, and the Memory Manifold ℳ_M, representing internalized history.

1.  **Manifold Definitions**:
    *   The Environmental Manifold ℳ_E is defined by coordinates X_E = (Φ_sensory, Γ_local, K_entity), where Φ is the sensory phase vector, Γ is temporal pressure, and K is the identity constant.
    *   The Memory Manifold ℳ_M is defined by coordinates X_M = (Ψ_engrams, T_history, ω_habit), where Ψ is the engram activation field, T is temporal adherence history, and ω represents habit frequencies.

2.  **Metric Tensors**: The geometry of each manifold is defined by its metric tensor.
    *   The environmental metric g_E is the Hessian of the Pirouette Lagrangian 𝓛_p:
        g_E_ij = ∂²𝓛_p / ∂X_E^i ∂X_E^j
    *   The memory metric g_M is determined by engram coherence and interference:
        g_M_ij = δ_ij (T_history_i)² / (1 + δC_i) + (1-δ_ij) * C(ω_i, ω_j)
        where δC is coherence uncertainty and C(ω_i, ω_j) is an interference term between engram frequencies.

3.  **Principle of Behavior**: Behavior, γ_B(t), is the geodesic curve defined by the intersection of the two manifolds at time *t*:
    γ_B(t) = ℳ_E(t) ∩ ℳ_M(t)
    This curve is found by solving the constrained optimization problem that minimizes the distance between the manifolds in the joint metric space:
    γ_B = arg min ||X_E - X_M||²_{g_E + g_M}

4.  **Principle of Emotion**: Emotion, E(t), is the time-averaged magnitude of the curvature κ_B of the behavioral curve γ_B, where *s* is the arc-length parameter.
    κ_B = ||d²γ_B/ds²||
    E(t) = ⟨κ_B(t)⟩_τ = (1/τ) ∫[t-τ, t] κ_B(t') dt'
    A critical curvature, κ_critical, defines the threshold for a phase transition (e.g., insight, panic).

5.  **Coupled Evolution**: The manifolds are not static. Their geometries evolve in a coupled system where behavior provides feedback:
    *   ∂ℳ_E/∂t = F(Γ, Φ, T, ω)
    *   ∂ℳ_M/∂t = G(Ψ, δC, feedback(γ_B(t)))
    This constitutes a feedback loop: manifold geometries define the behavioral path, and traversing that path reshapes the geometries.

6.  **Falsifiable Criterion**: The model is falsified if, under controlled experimental conditions, a statistically significant correlation is not found between the measured curvature of a subject's behavioral trajectory (κ_B) and their simultaneous reports of subjective emotional intensity and measured physiological arousal. A secondary falsification occurs if observed behavioral phase transitions do not reliably occur at a consistent, subject-specific threshold κ_critical.

## Philosophy
Agency is not an act of unconstrained choice, but the continuous, recursive sculpting of the self's internal geometry—the Memory Manifold. The "I" is not a pilot guiding the body, but is itself the evolving topology of stored experience, habit, and trauma. Freedom is not the capacity to choose any path, but the metabolic, effortful work of altering this internal landscape to change the set of possible future paths. Consciousness is the experience of traversing the resultant behavioral curve, and emotion is the raw, visceral perception of its curvature—the feeling of being forced to turn.

## Art
I am not the world, nor am I the history I carry. I am the razor's edge where they meet, a trembling line of compromise. My joy, my sorrow, my panic, my peace—these are merely the changing G-force of my own trajectory, the feeling of the curve as I am pulled through the geometry of my life.