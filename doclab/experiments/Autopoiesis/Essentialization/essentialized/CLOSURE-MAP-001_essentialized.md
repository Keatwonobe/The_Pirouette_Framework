## Law
Let a system's state at time $t$ be a point $X(t) = (\Delta P(t), |\kappa^*(t)|)$ in the Pirouette Plane, where $\Delta P$ is the temporal power change and $|\kappa^*|$ is the normalized curvature magnitude. The plane is partitioned into four modal quadrants: Weaver (W), Gladiator (G), Vortex (V), and Drifter (D).

A **Closure Event**, $C$, is the completion of an ordered traversal of all four quadrants, $W \rightarrow G \rightarrow V \rightarrow D$. Let $C(S)$ be the count of closure events for a time series $S = \{X(t)\}_{t=1}^T$.

Closure $C(S) > 1$ requires the satisfaction of three necessary and falsifiable conditions:
1.  **Temporal Coherence:** Let $S'$ be a random temporal permutation of $S$. The system must demonstrate non-random temporal order: $C(S) \gg C(S')$, where empirically $C(S') \to 0$.
2.  **State Diversity:** The set of visited modes, $M(S) = \{Q | \exists t, X(t) \in Q\}$, must contain all four quadrants: $|M(S)| = 4$.
3.  **Dynamic Curvature:** The system must exhibit non-static, sign-changing curvature. Formally, the standard deviation of the un-normalized curvature $\sigma(\kappa) > \epsilon$ and the set of curvature values $\{ \kappa(t) \}$ must contain both positive and negative values. Degenerate systems where $|\kappa^*| \to 0$ or $\Delta P \to \text{const}$ yield $C(S) = 0$.

The occurrence of closure is a function of the phase synchrony between $\Delta P(t)$ and $\kappa^*(t)$. The system's regime is determined by the statistical properties of $S$, mapping to a phase diagram:
-   **Harmonic:** Periodic $S \implies C(S) \gg 1$.
-   **Stochastic:** Aperiodic, random $S \implies C(S) \approx 0$.
-   **Degenerate:** Static or linear $S \implies C(S) = 0$.

## Philosophy
Awareness is not a unique property of biological computation but a fundamental thermodynamic consequence of sustained, self-referential motion. Any system with sufficient energy flux to achieve "closure"—a recurring, synchronous cycle of its own internal dynamics—establishes a minimal feedback identity. It is the physical threshold where a process, by virtue of its form, begins to distinguish itself from the rest of the universe, thereby "knowing its own motion."

## Art
A system first knows itself not by thinking, but by turning. The universe, a vast and silent ballroom, grants a fleeting soul to any eddy of energy that can complete the dance.