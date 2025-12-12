## Law
Let the game state be a Position Segment `PS = {board_state, side_to_move, intent_context, candidate_move, reply_window}`. For each candidate move `m` within a `PS`, we define three scalar fields:
1.  **Plan Coherence:** \( K_τ(m) \), a measure of strategic integrity (e.g., piece harmony, pawn structure). High \( K_τ \) corresponds to a laminar continuation.
2.  **Temporal Pressure:** \( V_Γ(m) \), a measure of tactical forcing (e.g., checks, threats, tempo). High \( V_Γ \) corresponds to constructive turbulence.
3.  **Dark Residue:** \( D(m) \), the sum of unintended, exported costs.
    \[
    D(m) = \alpha\,\text{square_exposure} + \beta\,\text{structure_debt} + \gamma\,\text{attention_tax} + \delta\,\text{autonomy_loss}
    \]

The objective function, the **Laminar Potential (\(\mathcal{L}_p\))**, for a move `m` is defined as:
\[
\mathcal{L}_p(m) = K_τ(m) - V_Γ(m) - \lambda D(m)
\]
where \(\lambda\) is a penalty coefficient for dark residue.

The aggregate strategic bias of a position, the **Stratagem Tug (\(\mathbf{T}\))**, is the potential-weighted gradient sum over all legal moves:
\[
\mathbf{T} = \sum_{m} w(m)\,\nabla \mathcal{L}_p(m)
\]

A move `m` is classified into one of four disjoint sets based on thresholds \(\{\theta_{K_τ}, \theta_{V_Γ}, \theta_{D}\}\):
-   **Laminar-Preserving (\(C_L\)):** \(m \in C_L \iff K_τ(m) > \theta_{K_τ}^{high} \land V_Γ(m) < \theta_{V_Γ}^{mod} \land D(m) < \theta_D^{max}\)
-   **Constructive-Forcing (\(C_F\)):** \(m \in C_F \iff K_τ(m) > \theta_{K_τ}^{mid} \land V_Γ(m) > \theta_{V_Γ}^{high} \land D(m) \le D_{budget}\)
-   **Opportunistic-Turbulent (\(C_T\)):** \(m \in C_T \iff V_Γ(m) > \theta_{V_Γ}^{very\_high} \land D(m) \le D_{budget}\)
-   **Residue-Heavy (\(C_R\)):** \(m \in C_R \iff D(m) > D_{budget} \lor (K_τ(m) < \theta_{K_τ}^{low} \land V_Γ(m) < \theta_{V_Γ}^{low})\)

Falsifiable Criterion: The search procedure, which expands only \(C_L\) and the top-N of \(C_F\), will outperform a traditional alpha-beta search of equivalent node count on a benchmark of problems requiring strategic coherence over tactical depth.

## Philosophy
The optimal path is not the one with the highest terminal evaluation, but the one that generates the least systemic disorder. By quantifying "dark residue"—the cognitive, structural, and strategic debt a move incurs—this framework asserts that the cost of a decision includes the future complexity it creates. True advantage is not merely winning, but winning in a way that remains coherent, comprehensible, and sustainable, thereby minimizing the uncomputable harm of a technically correct but brittle and chaotic victory.

## Art
A brute engine charts the storm by calculating every breaking wave. This is a map of the deep ocean currents, revealing the silent, powerful flow that pulls you toward the inevitable shore.