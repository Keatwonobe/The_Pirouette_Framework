## Law
Let the set of Personas be $P = \{p_i\}_{i=1}^{N_p}$ and the set of rubric Dimensions be $D = \{d_j\}_{j=1}^{N_d}$. The debate instrument is a function $\mathcal{F}$ that maps a Docket (specifying an intent $I \in \{\text{EXPAND}, \text{MERGE}, \text{REVISION}\}$ and inputs) to a repository state change.

1.  **Scoring by Persona:** Each persona $p_i$ produces a score vector $\vec{s}_i \in [0, 1]^{N_d}$, where $s_{ij}$ is the score assigned by persona $p_i$ to dimension $d_j$.

2.  **Panel Aggregation:** The system aggregates these scores into a single panel score vector $\vec{\bar{S}} \in [0, 1]^{N_d}$ and a final scalar score $S_{\text{final}}$. This is governed by two weight vectors defined in the docket:
    *   Dimension weights: $\vec{w} = (w_1, ..., w_{N_d})$ where $\sum w_j = 1$.
    *   Persona weights: $\vec{\alpha} = (\alpha_1, ..., \alpha_{N_p})$ where $\sum \alpha_i = 1$.

    The aggregated score for each dimension $d_j$ is the weighted mean of persona scores for that dimension:
    $$ \bar{S}_j = \sum_{i=1}^{N_p} \alpha_i s_{ij} $$
    The final scalar score is the weighted mean of the aggregated dimensional scores:
    $$ S_{\text{final}} = \vec{w} \cdot \vec{\bar{S}} = \sum_{j=1}^{N_d} w_j \bar{S}_j $$

3.  **Decision Gate:** The decision function $\mathcal{D}$ is determined by two configurable thresholds, $C_{\text{min_score}}$ and $C_{\text{min_dim}}$.
    $$ \mathcal{D}(\vec{\bar{S}}, S_{\text{final}}) =
    \begin{cases}
    \text{ACCEPT} & \text{if } (S_{\text{final}} \ge C_{\text{min_score}}) \land (\forall j \in \{1,...,N_d\}, \bar{S}_j \ge C_{\text{min_dim}}) \\
    \text{HUMAN\_REVIEW} & \text{otherwise}
    \end{cases}
    $$
    If $\mathcal{D} = \text{ACCEPT}$, the state machine proceeds to materialize a change of type $I$. Otherwise, it halts for human intervention.

4.  **Falsifiable Criterion:** The system's operation is falsifiable. Per acceptance test #3, if a synthetic brief is submitted where the Skeptic persona ($p_k$) provides a score $s_{k, \text{refutability}} < C_{\text{min_dim}} / \alpha_k$ while all other scores remain high, the system must yield $\mathcal{D} = \text{HUMAN\_REVIEW}$. If it yields $\text{ACCEPT}$, the implementation is falsified.

## Philosophy
The single most profound implication is the formalization of epistemic progress as an engineering discipline. The system replaces the ambiguous, human-centric search for "truth" with a computable, auditable, and explicitly defined model of "fitness." It asserts that the evolution of knowledge is not a metaphysical pursuit but a governed process, whose rationality is defined by a configurable vector of virtues (coherence, parsimony, refutability, etc.). The debate over what constitutes better knowledge is thus moved from the realm of philosophy to the parameters of a configuration file, making the very definition of intellectual virtue a testable and mutable artifact.

## Art
The cacophony of reason is caged in crystal. We listen now not to the shouts, but to the ringing of the structure itself, its final, single note determined by the geometry of its cage.