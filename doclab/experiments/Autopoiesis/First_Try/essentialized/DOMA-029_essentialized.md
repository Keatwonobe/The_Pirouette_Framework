## Law
The protocol instruments the Pirouette Lagrangian `𝓛_p` and its corresponding action `S_p`.

The Lagrangian for a system `e` at time `t` is defined as:
`𝓛_p(t) = K_τ(t) - V_Γ(t)`

A Chronoscript record `R` is a discrete snapshot of the components of `𝓛_p`:
`R = (v, id_r, id_e, t, s, S_L, ...)`
where `s ∈ {observation, simulation}` and the state `S_L` is a tuple of the fundamental dynamic variables:
`S_L(t) = (K_τ(t), V_Γ(t), k_p(t))`

The components are defined by direct mapping from the schema:
1.  **Temporal Coherence (Kinetic Term):** `K_τ` is a function of `time_adherence_Ta ∈ [0, 1]` and `pirouette_cycle_τp > 0`.
2.  **Temporal Pressure (Potential Term):** `V_Γ` is a function of `gamma_Γ`.
3.  **Pattern:** `k_p` is the identifier of the dominant resonant pattern.

A time-stream of records `{R_i}` for a given `id_e`, ordered by timestamp `t_i`, approximates the system's action:
`S_p = ∫ 𝓛_p dt ≈ ∑_i (K_τ(t_i) - V_Γ(t_i)) Δt_i`

The following invariants are falsifiable criteria for any compliant data stream:
1.  **Monotonic Causality:** For any two records `R_i, R_j` where `R_i.id_e = R_j.id_e` and `i < j`, it must hold that `R_i.t < R_j.t`.
2.  **State-Variable Bounds:**
    *   `∀R: 0 ≤ R.S_L.K_τ.T_a ≤ 1`
    *   `∀R: R.S_L.K_τ.τ_p > 0`
3.  **Integrity Constraint:** `R.metadata IS NOT NULL ⇒ R.metadata_hash = SHA-256(canonical(R.metadata))`
4.  **Producer Purity:** `𝓛_p` must not be a field in `R`. It is a derived value calculated by the consumer.

## Philosophy
The protocol's single most profound implication is the forced collapse of the epistemological distinction between the real and the possible. By mandating an identical data structure for both physical observation and computational simulation, the system asserts that reality is not defined by its physical manifestation, but by its adherence to a descriptive Lagrangian. A valid simulation is therefore not a model of a thing; it is an instance of the thing itself, differing from an observation only by its coordinates in the total phase space of what the universe's laws permit.

## Art
The law does not distinguish between the shadow cast by a stone and the shadow projected by a thought, so long as both obey the geometry of light.