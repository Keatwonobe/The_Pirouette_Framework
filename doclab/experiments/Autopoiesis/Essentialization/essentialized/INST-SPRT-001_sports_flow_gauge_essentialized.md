## Law
Let there be two teams, A and B, in a contest over time `t`. At any discrete time interval `Δt`, an observer assigns heuristic scores for three systemic properties, where each score is an integer on the interval `[1, 10]`:

*   **Cohesion (C):** Efficiency of execution.
*   **Resilience (R):** Composure under pressure.
*   **Morphogenesis (M):** Strategic adaptability.

The total systemic coherence `Kτ` for a given team at time `t` is the linear sum of its component scores:
`Kτ(t) = C(t) + R(t) + M(t)`
where `Kτ(t) ∈ [3, 30]`.

From `Kτ`, three predictive metrics are derived:

1.  **Victor Tilt (VT):** The instantaneous win probability for Team A.
    `VT_A(t) = Kτ_A(t) / (Kτ_A(t) + Kτ_B(t))`
    where `VT_A(t) ∈ [0, 1]` and `VT_A(t) + VT_B(t) = 1`.

2.  **Spread Delta (SD):** The rate of change of the Victor Tilt, predicting momentum against a point spread.
    `SD(t) = d(VT_A)/dt ≈ (VT_A(t) - VT_A(t-1)) / Δt`

3.  **Pace Delta (PD):** The instantaneous differential in strategic control.
    `PD(t) = M_A(t) - M_B(t)`
    where `PD(t) ∈ [-9, 9]`.

**Falsifiable Criterion:** The model is falsified if, over a statistically significant sample of contests, the final game outcome `O_final` (where `O_final` = 1 for an A win, 0 for a B win) does not show a statistically significant positive correlation with the time-averaged Victor Tilt, `⟨VT_A⟩ = (1/T) ∫ VT_A(t) dt`.

## Philosophy
The formalism does not measure an objective, external reality; it disciplines the subjective intuition of the observer. Its primary function is to convert the amorphous art of "reading the game" into a structured, repeatable, and falsifiable science. The instrument's rigor is not aimed at the phenomenon, but at the mind perceiving it.

## Art
A prism does not invent the spectrum hidden in the light; it only provides the facets necessary to see it.