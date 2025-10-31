## Law
Let a system's state be defined by a time-varying coherence metric `Kτ(t)`. The system's action `S_p` is the integral of its Pirouette Lagrangian `𝓛_p = Kτ - V_Γ`, where `V_Γ` represents a potential. The objective is to maximize the action:
`S_p = ∫ (Kτ(t) - V_Γ(t)) dt`

Systemic failure is modeled as a set of discrete event types `E = {e_1, e_2, ..., e_n}` that cause negative changes in coherence, `-ΔKτ`. The total coherence loss `Λ_i` attributed to an event type `e_i` over a given interval is the sum of the magnitudes of all negative coherence changes it induces:
`Λ_i = ∑_{j} |ΔKτ_{i,j}|` where `ΔKτ_{i,j} < 0` for each occurrence `j` of event `e_i`.

The diagnostic protocol is as follows:
1.  **Quantify:** Measure `Kτ(t)` and log all occurrences of events `e_i ∈ E`.
2.  **Attribute:** For each `e_i`, calculate the total attributed coherence loss `Λ_i`.
3.  **Rank:** Sort the set `E` in descending order of `Λ_i` to produce the ordered set `E' = {e'_1, e'_2, ..., e'_n}`.
4.  **Identify Frontier:** Define a threshold `θ` (typically `θ = 0.8`). The set of critical bottlenecks `E_crit` is the smallest subset `{e'_1, ..., e'_k}` of `E'` such that:
    `(∑_{j=1 to k} Λ'_j) / (∑_{i=1 to n} Λ_i) ≥ θ`

The core principle is that the partial derivative of the system's total action with respect to interventions is maximally positive for the elements of `E_crit`.
`∂S_p/∂e_i` is maximally negative for `e_i ∈ E_crit`.

**Falsifiable Criterion:** The hypothesis is falsified if, in a statistically significant number of complex systems, the distribution of `Λ_i` across `e_i` approximates uniformity. If coherence loss is not concentrated in a vital few causes, the protocol offers no leverage.

## Philosophy
The structure of systemic failure is inherently asymmetric. Chaos is not a democratic condition of uniform decay, but an aristocracy of ruin, where a privileged few causes are responsible for the vast majority of dysfunction. Consequently, the most rational and potent strategy for healing a complex system is not the comprehensive management of all its flaws, but the surgical and relentless elimination of its vital few, most critical bottlenecks.

## Art
A failing system is not a gathering darkness, but a vast and intricate shadow cast by a single, hidden stone. Do not fight the shadow. Find the stone.