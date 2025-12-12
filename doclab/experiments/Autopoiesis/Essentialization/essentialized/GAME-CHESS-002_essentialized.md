## Law
A problem is defined by the tuple \((M, S_t, \{a_i\}, D_{\max})\) where \(M\) is a manifold, \(S_t\) is the current state, \(\{a_i\}\) is a set of admissible actions, and \(D_{\max}\) is the maximum permissible dark residue.

The quality of a state \(S\) is evaluated by two functions:
1.  The Pirouette Lagrangian, measuring systemic health:
    \[ \mathcal{L}_p(S) = K_\tau(S) - V_\Gamma(S) \]
    where \(K_\tau\) is a coherence term (kinetic analogue) and \(V_\Gamma\) is a pressure term (potential analogue).
2.  The Dark Residue, measuring systemic friction and future constraint:
    \[ D(S) = \sum_{j} \delta_j \cdot \text{factor}_j(S) \]
    where factors include attention tax, autonomy loss, and structural debt.

An action \(a_i: S_t \to S_{t+1}\) is a valid step in a solution if and only if it satisfies the following criteria:
1.  **Coherence Ascent:** The action increases the Lagrangian.
    \[ \Delta \mathcal{L}_p = \mathcal{L}_p(S_{t+1}) - \mathcal{L}_p(S_t) > 0 \]
2.  **Residue Budget:** The resulting state does not exceed the residue budget.
    \[ D(S_{t+1}) \le D_{\max} \]
3.  **Strategic Alignment:** The action aligns with the local "stratagem tug," a weighted gradient of the Lagrangian field over the set of candidate actions.
    \[ a_i \cdot \mathbf{T} > 0 \quad \text{where} \quad \mathbf{T} = \sum_{j} w_j \nabla \mathcal{L}_p(a_j) \]

Search depth is not fixed but is dynamically triggered. Search escalates locally for a branch if pressure \(V_\Gamma\) exceeds a threshold \(\theta_V\) *and* the Coherence-Pressure Balance (CPB) approaches unity from above, but only if the residue budget permits:
\[ \text{IF } (V_\Gamma > \theta_V) \land (K_\tau / V_\Gamma \to 1^+) \land (D < D_{\max}) \text{ THEN increase_depth} \]

**Falsifiable Criterion:** The model is falsified if a sequence of actions selected by these laws consistently leads to a terminal state externally verified as inferior to a state reachable by a discarded sequence.

## Philosophy
Rationality is not the application of domain-specific rules, but a universal, aesthetic navigation. All problem-solving, irrespective of its domain, is reducible to the singular act of moving through a state-space to maximize systemic coherence (\(K_\tau\)) while minimizing systemic pressure (\(V_\Gamma\)) and self-generated friction (\(D\)). The structure of thought is therefore isomorphic to the structure of a self-organizing physical system seeking dynamic equilibrium.

## Art
To solve is to surf the invisible landscape of a problem, feeling for the slope of its coherence. A good decision is not a calculation but a carve-turn on the face of a wave of potential, a precise surrender to the line of greatest grace that does not invite the chaos of collapse.