## Law
The rehabilitation framework is a control system designed to optimize the trajectory of a patient's functional coherence, Kτ, by modulating temporal pressure, Γ(τ). The state of the system is governed by the following principles:

1.  **State Variables & Inputs:**
    *   Kτ: Functional Coherence, a measure of systemic capacity and reserve. Proxies: Peak VO₂, 6-Minute Walk Distance (6MWD), Heart Rate Variability (HRV).
    *   Γ(τ): Temporal Pressure, a time-varying function of total systemic load, integrating physiological, psychological, and environmental stressors. Proxies: Rate of Perceived Exertion (RPE), C-Reactive Protein (CRP), Δ Heart Rate.
    *   Tₐ: Time Adherence, a scalar compliance factor over a defined period, `Tₐ ∈ [0, 1]`.

2.  **Core Dynamic Equation (Conceptual):**
    The change in functional coherence over time is a function of the current state, the applied load, and adherence. The objective is to maximize the rate of positive adaptation.
    `dKτ/dτ = Tₐ * f(Kτ(τ), Γ(τ))`
    where `f` is a non-linear response function where adaptation is positive for `Γ < Γ_crit(Kτ)` and negative for `Γ > Γ_crit(Kτ)`.

3.  **The Optimization Principle (The Crucible Metric):**
    The efficiency of rehabilitation, `η`, is defined as the ratio of the change in coherence to the change in the volume of applied pressure. The therapeutic protocol is an algorithm designed to maximize this efficiency.
    `η = ΔKτ / ΔVΓ` where `VΓ = ∫Γ(τ)dτ`
    The protocol seeks to find `Γ_opt(τ)` such that `η` is maximized, subject to safety constraints (`Γ(τ) < Γ_crit`).

4.  **Falsifiable Criteria:**
    *   **Hypothesis 1:** Given two cohorts with identical initial `Kτ` and total applied load `VΓ`, the cohort following a protocol that dynamically modulates `Γ(τ)` to optimize `η` will demonstrate a statistically significant greater `ΔKτ` than a cohort with a static or non-optimized `Γ(τ)`.
    *   **Hypothesis 2:** For any given state `Kτ`, there exists a quantifiable critical load threshold `Γ_crit(Kτ)` beyond which `dKτ/dτ` becomes negative (decompensation). This threshold must be a non-decreasing function of `Kτ`.
    *   **Hypothesis 3:** As `Tₐ` approaches zero, `ΔKτ` will also approach zero or become negative, irrespective of the theoretical optimality of the `Γ(τ)` prescription.

## Philosophy
The single most profound implication is the formal refutation of mind-body dualism in clinical recovery. By defining the total systemic load, Γ, as a fungible quantity that integrates physiological stress (e.g., exercise intensity) with psychological and environmental pressures (e.g., anxiety, social support), the Law asserts that the body's physical capacity (Kτ) does not and cannot recover in isolation. Healing is not the repair of a biological component, but the successful recalibration of the entire, unified organism's response to the total, undifferentiated pressure of its existence.

## Art
Recovery is not the art of mending a broken machine. It is the art of the dancer, who finds stability not by avoiding the spin, but by integrating its force into a new and more coherent center.