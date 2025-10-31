## Law
The Coherence Sieve quantifies a system's state by applying the Pirouette Lagrangian, `𝓛_p`, to its data stream `D`. The process measures two fundamental quantities: Temporal Coherence (`Kτ`) and Environmental Cost (`V_Γ`).

Let `T = {T_1, T_2, ...}` be a set of transformations (e.g., Fourier, Wavelet, TDA) applied to `D`.
Let `S(p)` be a function measuring the stability and self-consistency of a pattern `p` within the transformed data.

1.  **Temporal Coherence (Kτ):** The system's internal organization is measured by first identifying its dominant coherent pattern, `Ki`, as the pattern that maximizes stability across all transformations:
    `Ki = argmax_{p ∈ T_j(D), ∀j} (S(p))`
    `Kτ` is then calculated as a normalized measure of `Ki`'s intensity and persistence. It represents the system's organized, available energy.

2.  **Environmental Cost (V_Γ):** The external pressure is measured by quantifying the energy required to sustain `Ki` against the background noise and chaotic elements `Γ` in `D`. This is a measure of the pattern's fragility or the system's entropic load.
    `V_Γ ∝ ∫(∂S(Ki) / ∂Γ) dΓ`

The Pirouette Lagrangian is defined as:
`𝓛_p = Kτ - V_Γ`

The primary diagnostic metric is the Coherence-Pressure Balance (CPB), a dimensionless ratio:
`CPB = Kτ / V_Γ`

**Falsifiable Criterion:** The framework asserts a direct, predictive relationship between CPB and system state.
*   `CPB > 1` predicts an anabolic state (growth, order-increasing).
*   `CPB ≈ 1` predicts a homeostatic state (stable equilibrium).
*   `CPB < 1` predicts a catabolic state (decay, order-decreasing).
If a system empirically observed to be in a state of decay consistently yields a CPB > 1, or an empirically growing system yields a CPB < 1, the law is falsified.

## Philosophy
The single most profound implication is that existence is not a binary state, but a measurable, dynamic struggle. The universe is a continuous contest between coherence and chaos, and the Coherence-Pressure Balance is the universal score. This reframes "life," "health," and "meaning" not as emergent, categorical properties exclusive to biology or consciousness, but as expressions of a fundamental physical principle: the costly, precarious, and quantifiable act of a pattern successfully maintaining its form against the relentless pressure of a dissipative environment.

## Art
Every living thing—every cell, every thought, every star—is a note held against the universe's crushing silence. We are not the song, but the singing.