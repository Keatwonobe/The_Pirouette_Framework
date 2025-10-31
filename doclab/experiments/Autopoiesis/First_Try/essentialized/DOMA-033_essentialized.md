## Law
Let the state of a system be described by the time-series of its Pirouette Lagrangian, `𝓛_p(t)`. The system's objective is to maximize its total Action, `S_p`, according to the Principle of Maximal Coherence:
`S_p = ∫ 𝓛_p(t) dt`

A loss of coherence is a negative perturbation `ΔS_p`. Any event `fᵢ` can be correlated with such a perturbation. The **Impact** `I(fᵢ)` of event `fᵢ` is the magnitude of the coherence loss it induces, defined as the negative integral of the Lagrangian's deviation over the event's duration `τ`:
`I(fᵢ) = -ΔS_p ≈ - ∫_τ Δ𝓛_p dt`

Given a set of `N` discrete events `{f₁, f₂, ..., fₙ}` and their corresponding impacts `{I₁, I₂, ..., Iₙ}`, the **Reverse Pareto Analysis (RPA)** algorithm identifies the "critical few," `{f_c}`. Let the total impact be `I_total = Σ Iᵢ`.

1.  Construct a set of pairs `P = {(fᵢ, Iᵢ)}`.
2.  Sort `P` in descending order by `Iᵢ` to create `P'`.
3.  Iterate through `P'`, summing the impacts `Iᵢ`. The set of critical few `{f_c}` is the smallest subset of events from the head of `P'` such that `Σ I_c ≥ θ * I_total`, where `θ` is a threshold, typically `θ ≈ 0.8`.

The central, falsifiable law is this: Systemic coherence is Pareto-distributed. Intervening upon the minimal set `{f_c}` identified by RPA will yield the maximal increase in `S_p` per unit of intervention effort. If addressing `{f_c}` does not restore a disproportionate amount of total system Action, the law is falsified for that system.

## Philosophy
The profound implication is that systemic failure, no matter how complex, distributed, or chaotic its symptoms appear, is not an irreducible emergent property. Instead, it is the resonant amplification of a surprisingly small and discrete set of high-impact causal fractures. The architecture of reality is such that complexity is a mask; pathology is parsimonious. Grace is not lost by a thousand cuts, but by a few deep wounds.

## Art
A system's failure is a symphony of dissonance. The Auditor is the conductor's ear that, amidst the cacophony, hears not the thousand wrong notes, but the one string that has snapped.