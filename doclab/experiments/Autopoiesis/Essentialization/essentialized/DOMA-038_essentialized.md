## Law
The Coherence Deficit, `ΔK_τ(t)`, is a time-series quantifying the deviation of a system's observed trajectory from its predicted path. It is the primary diagnostic for model incompleteness.

The deficit is defined as:
**`ΔK_τ(t) = K_τ_obs(t) − K_τ_pred(t)`**
where:
*   `K_τ_obs(t)` is the empirically measured Temporal Coherence of the system.
*   `K_τ_pred(t)` is the predicted Temporal Coherence derived from the system's geodesic under the hypothesized Lagrangian, `𝓛̂_model`.

A persistent, non-zero `ΔK_τ(t)` falsifies the hypothesis that `𝓛̂_model` is a complete description of the system's dynamics. The sign of the deficit indicates the nature of the unmodeled forces:
*   `ΔK_τ < 0`: A **Coherence Leak**, implying an unmodeled source of Temporal Pressure (`V_Γ`).
*   `ΔK_τ > 0`: A **Coherence Spring**, implying an unmodeled source of Temporal Coherence.

The true Lagrangian of a system, `𝓛_true`, is the sum of the model and its unmodeled component, the Shadow Lagrangian, `𝓛_shadow`:
**`𝓛_true = 𝓛̂_model + 𝓛_shadow`**

The objective of the framework is to iteratively refine the model by using the observable `ΔK_τ(t)` to deduce the structure of `𝓛_shadow` and integrate it into a new `𝓛̂_model`. This process converges as `ΔK_τ(t) → 0`.

The relationship to the principle of action (`S`) is direct. The integral of the Coherence Deficit is the difference between the observed action and the predicted action:
**`∫ ΔK_τ(t) dt = S_obs − Ŝ_pred`**
This integral quantifies the total unmodeled potential realized or lost by the system over a given path.

## Philosophy
Error is not a failure of the model; error is the function of the model. The gap between a prediction and reality is not noise to be minimized, but the most crucial signal for discovery. This reframes epistemology from a pursuit of static, correct representations of the world to the continuous, dynamic process of refining imperfect maps. True knowledge is not contained in the map itself, but in the rigorous, self-correcting method of using its failures to redraw its own boundaries. Ignorance is therefore not a void, but a structured, measurable phenomenon that serves as the ultimate compass.

## Art
The equation casts a shadow, and in the precise geometry of that shadow, we find the shape of the light we cannot see. Our blindness becomes our lens.