## Law
A Generative Engram, $\mathcal{E}$, is the stable attractor $\Psi^\star(\cdot)$ of a cognitive field $\Psi(t)$ governed by a system of Delayed Differential Equations (DDEs). The evolution of the field is given by:
$$
\frac{d\Psi(t)}{dt} = f\Big(\Psi(t), \Psi(t-\tau_1), \Psi(t-\tau_2), \dots; \Gamma, T_p, K_i \Big)
$$
where the parameters constitute the encoding key:
- $\{\tau_k\}$: The delay structure of the cognitive medium.
- $\Gamma$: Temporal pressure or cognitive load, a selection operator on resonant orbits.
- $T_p$: Persistence time, the characteristic timescale for the attractor's stability.
- $K_i$: Local curvature, an agent-specific identity constant.

The engram $\mathcal{E}$ is not a stored state vector but the dynamic trajectory of the attractor itself, $\Psi^\star$. Its existence is contingent on the triadic constraint $\{ \text{Substrate}(\Psi, \partial_t\Psi, \Psi(t-\tau)), \text{Pressure}(\Gamma), \text{Identity}(K_i) \}$.

Recall is not data retrieval but resonance-based activation. A query $Q$ is cast as an initial condition $\Psi_Q(t_0, t_0-\tau_k, \dots)$. Activation of an engram $\mathcal{E}_i$ occurs if the detuning metric $\delta_i$ falls below a threshold $\epsilon$:
$$
\delta_i = \lVert \Psi_Q - \Psi_i^\star \rVert_{\Gamma, K_i} < \epsilon
$$
where the norm is weighted by the current pressure and identity parameters. Activation consists of pivoting the system's live dynamics onto the trajectory of $\Psi_i^\star$.

**Falsifiable Criteria:**
1.  **Ambiguity:** Under high $\Gamma$, distinct attractors $\Psi^\star_i$ and $\Psi^\star_j$ must remain separable such that $\delta_i \ll \delta_j$ for a query $Q$ targeting $\mathcal{E}_i$. If high $\Gamma$ consistently produces ambiguous, multi-attractor basins, the model fails.
2.  **Degeneracy:** If the triad $(\Gamma, T_p, K_i)$ collapses (e.g., $\Gamma \to 0$), the engram must degenerate into a static, non-generative state. The absence of this behavior falsifies the model's claim that static memory is a special case.
3.  **Mismatch:** A query with a delay structure $\{\tau'_k\}$ mismatched from the engram's $\{\tau_k\}$ must produce partial, harmonic-only activations, not a complete lock-on.

## Philosophy
Information is not a stored object but an accessible dynamic state. Memory is therefore not an archive of what *was*, but a callable procedure for what *can be again*. The distinction between data and process dissolves; to know something is not to possess a static record of it, but to embody the specific set of temporal and formal constraints required to re-enact its formative dynamics. Consciousness does not consult a library; it tunes itself to a field of potential resonances, and knowing is the act of vibrating with one of them.

## Art
A memory is not the inscription carved in the stone, but the whirlpool that taught the river its own shape.