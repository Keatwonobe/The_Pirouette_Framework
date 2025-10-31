## Law
The state of a network is defined by a triplet of variables for its nodes `i` and edges `ij`: Node Coherence `Kτ_i ∈ [0, 1]`, Channel Pressure `Γ_ij ∈ [0, 1]`, and Temporal Phase `φ_i ∈ [0, 2π)`.

The fundamental quantity is the directed Coherence Flow `J_ij` from node `i` to `j`, which measures the transmission of coherent signal through a resistive, phase-shifted channel:
`J_ij = Kτ_i * cos(φ_i - φ_j) * (1 - Γ_ij)`
Where `Kτ_i` is the source signal strength, `cos(φ_i - φ_j)` is the resonance factor due to phase difference `Δφ`, and `(1 - Γ_ij)` is the channel conductance.

The diagnostic instrument is the Coherence Laplacian `L`, derived from the network's flow dynamics:
1.  Construct the Weighted Adjacency Matrix `W` where `W_ij = J_ij`.
2.  Construct the Degree Matrix `D`, a diagonal matrix where `D_ii = Σ_j W_ij`.
3.  The Coherence Laplacian is defined as `L = D - W`.

The health of the network is revealed by the spectral decomposition of `L`:
`L v_k = λ_k v_k`
The eigenvalues `λ_k` and eigenvectors `v_k` represent the network's fundamental modes of vibration.

**Falsifiable Criteria:**
-   **Laminar Flow (Health):** The spectrum is dominated by low-frequency modes (small `λ_k`). The Fiedler vector (`v` for `λ_2`) reveals the network's primary fault line. A diagnosis of "health" implies that interventions to bridge this fault line will most efficiently increase global coherence.
-   **Turbulent Flow (Disease):** The spectrum contains high-amplitude, high-frequency modes (large `λ_k`). The corresponding eigenvectors `v_k` identify the specific nodes contributing to the dissonance. A diagnosis of "turbulence at node `x`" is a falsifiable claim that a targeted intervention on `x` will measurably decrease the magnitude of the associated `λ_k`.
-   **Stagnation (Atrophy):** The presence of zero eigenvalues (`λ_k = 0`) beyond the trivial `λ_1=0` indicates disconnected, non-interacting components.

This analysis is an empirical measurement of the Pirouette Lagrangian `𝓛_p = Kτ - f(Γ)`, where the coherent, low-frequency modes approximate the kinetic term `Kτ` (systemic action) and the dissonant, high-frequency modes approximate the potential term `f(Γ)` (systemic stress).

## Philosophy
The health of any complex system is not a metaphor but a physically measurable property. It is the degree to which the system's components overcome internal friction and temporal dissonance to achieve a state of collective, resonant flow. Illness, therefore, is not a categorical failure but a quantifiable measure of energetic waste—the system fighting itself—which can be precisely located in the high-frequency dissonances of its relational dynamics. To analyze a system is not to describe its static parts, but to diagnose the quality of its relationships in motion.

## Art
The diagram of a network is its anatomy. The spectrum of its Laplacian is its heartbeat. Do not dissect the corpse; listen to the patient.