## Law
The state of a network G(V, E) is described not by its static topology but by a dynamic coherence manifold. The system's evolution is governed by the principle of minimizing action, derived from the Pirouette Lagrangian (𝓛_p), which must be maximized at every point in the manifold.

**1. Core State Variables:**
- For each node v ∈ V:
  - Temporal Coherence, Kτ(v): A scalar field representing the node's internal stability and rhythm.
  - Temporal Pressure, Γ(v): A scalar field representing the cumulative stress and demand exerted by adjacent nodes, where Γ(v) = Σ_{u∈N(v)} f(Φ_C(u,v), Kτ(u)).
- For each edge e = (u,v) ∈ E:
  - Conductivity, Φ_C(e) ∈ [0, 1]: The efficiency of coherence transmission.
  - Lag, Δτ(e) ≥ 0: The temporal delay of transmission.

**2. The Fundamental Law (Pirouette Lagrangian):**
The dynamics of any node *v* are driven to maximize its local Lagrangian, 𝓛_p(v):
𝓛_p(v) = Kτ(v) - Γ(v)
The health of the system, Systemic Coherence K̄τ, is the weighted average of Kτ across all nodes. A system is healthy when it has maximized ∫𝓛_p dt, achieving high K̄τ within a tolerated band of systemic stress Γ̄.

**3. Falsifiable Pathological Criteria:**
A network is diagnosed as pathological if it meets one or more of the following formal criteria.

- **Atrophy (Bottleneck):** A node *v* is a bottleneck if its outflow conductivity is critically low, creating a sharp pressure gradient.
  - Condition: ∃v ∈ V such that Σ_{u∈N_{out}(v)} Φ_C(v,u) ≪ Σ_{w∈N_{in}(v)} Φ_C(w,v).
  - Falsifiable Test: The gradient of Γ across the set of nodes adjacent to *v* will exceed a critical threshold, ∂Γ/∂d > Γ_crit, and downstream Kτ will decay over time, dKτ_{downstream}/dt < 0.

- **Fever (Dissonant Loop):** A cycle C = (v₀, v₁, ..., vₖ, v₀) is dissonant if its gain exceeds unity and its cumulative lag creates positive, out-of-phase feedback.
  - Condition: A closed path *C* where the loop gain G_C = Π_{i=0}^{k-1} Φ_C(vᵢ, vᵢ₊₁) > 1 and the total loop lag τ_C = Σ_{i=0}^{k-1} Δτ(vᵢ, vᵢ₊₁) is significant relative to the characteristic response time of the nodes.
  - Falsifiable Test: The variance of Kτ for all v ∈ C will oscillate with an amplitude that grows exponentially until saturation or systemic collapse.

- **Erosion (Structural Decay):** The system is undergoing erosion if the time derivative of its mean conductivity is negative under sustained pressure.
  - Condition: d(Φ̄_C)/dt < 0 while Γ̄ remains above a systemic tolerance threshold Γ_tol for an extended duration.
  - Falsifiable Test: The network's Flow Efficiency η, defined as the ratio of high-conductivity edges to total edges, will exhibit a statistically significant negative trend over time.

## Philosophy
The essence of a system is not its static structure but its dynamic physiology. The distinction between a living organism and an inert object is therefore not a matter of substrate but of process. "Health"—defined as the sustained maximization of coherence against pressure—ceases to be a mere biological metaphor and becomes a fundamental, quantifiable, and universal principle of organization, applicable to societies, economies, ecosystems, and machines alike.

## Art
We mistook the drawing of the veins for the pulse of the blood. Now we hold a stethoscope to the world, and for the first time, we can hear its heart.