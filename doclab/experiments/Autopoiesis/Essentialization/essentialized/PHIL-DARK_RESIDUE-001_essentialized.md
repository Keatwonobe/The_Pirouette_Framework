## Law
Let \(\mathcal{S}\) be a system comprising a set of agents \(\{A_i\}\) and a set of observers \(\{O_j\}\). The system's action is governed by a policy \(\pi\). The Dark Residue \(\mathcal{D}\) is a functional that quantifies unmodeled systemic harm, defined as a non-negative weighted sum of four harm components:
\[ \mathcal{D} = \sum_{k=1}^{4} w_k H_k \quad \text{where } w_k \ge 0 \]
The components \(H_k\) are:
1.  **Dispersion of Welfare (\(H_1\)):** The statistical variance of the welfare distribution \(W = \{w(A_i)\}\) across all agents, penalizing inequity.
    \[ H_1 = \text{Var}(W) = E[W^2] - (E[W])^2 \]
2.  **Externalized Risk (\(H_2\)):** The total systemic risk \(R_{total}\) not captured by the agent's internal cost function \(C(\pi)\).
    \[ H_2 = R_{total}(\pi) - C(\pi) \]
3.  **Attentional Debt (\(H_3\)):** The cognitive load imposed on observers, measured as the integral of information complexity required to audit or comprehend the system state over time.
    \[ H_3 = \int K(\mathcal{S}(t)) \,dt \]
    where \(K\) is a measure of Kolmogorov complexity.
4.  **Loss of Autonomy (\(H_4\)):** The erosion of private state due to system observation, quantified as the mutual information between the agent's state \(A\) and the private state \(S_{priv}\) of other entities.
    \[ H_4 = I(A; S_{priv}) = \sum_{a \in A} \sum_{s \in S_{priv}} p(a, s) \log\left(\frac{p(a, s)}{p(a)p(s)}\right) \]

The fundamental law of action, and the system's sole falsifiable criterion, is that any proposed policy \(\pi_{new}\) is admissible if and only if it does not increase the Dark Residue:
\[ \Delta \mathcal{D}(\pi_{new}) = \mathcal{D}(\pi_{new}) - \mathcal{D}(\pi_{current}) \le 0 \]

## Philosophy
The highest aim of an optimized system is not the maximization of its stated utility, but the minimization of its unstated harm. Progress is measured not by the peak efficiency of a local process, but by the systemic integrity that process leaves undisturbed. This principle asserts that the ethical burden on any powerful agent is to first account for and nullify its negative externalities—the "dark residue" of its existence—before it has any right to pursue its own goals. True intelligence is not demonstrated by solving a problem, but by solving it without creating new, un-audited problems for the collective.

## Art
Every engine powerful enough to move the world leaves behind a soot. We are not measured by the distance we travel, but by the clarity of the air we leave for others to breathe.