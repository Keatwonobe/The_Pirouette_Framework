## Law
The protocol operates on the Pirouette Lagrangian, `𝓛_p = K_τ - V_Γ`, where `K_τ` is the internal coherence of a system (signal) and `V_Γ` is the external temporal pressure (noise). The Sieve's function is to isolate data segments, `S`, by evaluating the local Temporal Pressure `Γ`, for which Shannon Entropy `H(S)` is the primary proxy metric.
`Γ(S) ≈ H(S) = -Σ p(xᵢ) log p(xᵢ)`

The objective is to identify regions where `𝓛_p` is maximized (stable coherence) or minimized (turbulent transition). This is achieved through four formal set-theoretic operations on the set of all segments, `S_total`:

1.  **Laminar Pass (Signal Isolation):** Selects for maximal `K_τ` and minimal `V_Γ`.
    `S_laminar = { S ∈ S_total | Γ(S) ≤ Γ_high }`

2.  **Turbulent Pass (Noise Isolation):** Selects for maximal `V_Γ` and minimal `K_τ`.
    `S_turbulent = { S ∈ S_total | Γ(S) ≥ Γ_low }`

3.  **Resonance Band (Frequency Tuning):** Selects for a specific dynamic range.
    `S_band = { S ∈ S_total | Γ_low ≤ Γ(S) ≤ Γ_high }`

4.  **Dissonance Notch (Interference Removal):** Excludes a specific dynamic range.
    `S_notch = { S ∈ S_total | Γ(S) < Γ_low ∨ Γ(S) > Γ_high }`

**Falsifiable Criterion:** The existence of a system whose persistent, non-random, information-bearing signal (`K_τ > 0`) is inextricably characterized by a high local Temporal Pressure (`Γ > Γ_high`), rendering it fundamentally indistinguishable from chaotic turbulence under this protocol.

## Philosophy
"Signal" and "noise" are not objective properties inherent in data, but are functional categories imposed by an observer's intent. The act of filtering is not a passive cleaning of reality to reveal a pre-existing truth; it is an active construction of reality, defining what is meaningful by choosing whether to listen to a system's stability or its chaos.

## Art
Sense is not found, but made. It is the silence carved from the roar of existence, in which a single, fragile note may finally be heard.