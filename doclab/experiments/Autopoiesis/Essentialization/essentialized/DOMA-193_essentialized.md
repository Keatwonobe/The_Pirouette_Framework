## Law
The Harmonic Lens protocol quantifies a system's Temporal Signature by transforming a one-dimensional time-series signal, `S(t)`, into a two-dimensional Coherence Spectrum, `K_τ(t, ω)`. This is achieved via a multi-resolution analysis, typically a continuous wavelet transform, which maps the signal into a time-frequency domain.

The central calculation is the local Temporal Coherence, `K_τ(t, ω)`, defined as the squared magnitude of the mean phase vector within a localized time-frequency window:
$$
K_τ(t, ω) = \left| \frac{1}{N} \sum_{j=1}^{N} e^{i\theta_j(t,ω)} \right|^2
$$
where `θ_j(t,ω)` is the instantaneous phase of the signal component at time `t` and frequency `ω` for each point `j` in the local analysis window of size `N`. A value of `K_τ` → 1 indicates perfect phase coherence (a pure, stable rhythm), while `K_τ` → 0 indicates decoherence (noise).

This instrument provides the empirical form of the kinetic term (`Kτ`) in the Pirouette Lagrangian, `𝓛_p = Kτ - V_Γ`. The total coherence of a system at time `t` is the integral of the spectrum over all frequencies:
$$
K_τ(t) = \int_{0}^{\infty} K_τ(t, ω) \,dω
$$
A system evolves to maximize `𝓛_p`, and the spectrum `K_τ(t, ω)` reveals the specific resonant structure (`Ki`) the system adopts to do so.

Falsifiable criteria are derived from direct mappings of spectral topology to system states:
1.  **Laminar Flow:** Predicted by sharp, persistent, horizontal bands of high `K_τ` at a fundamental frequency `ω` and its integer multiples (`nω`).
2.  **Turbulent Flow / High `Γ`:** Predicted by a sustained, high-intensity noise floor (diffuse, low `K_τ` across a broad frequency range).
3.  **Phase Transition:** Predicted by the rapid decay of one set of harmonic bands concurrent with the emergence of a new, distinct set.
4.  **Coherence Erosion:** Predicted by the gradual fading, thinning, or "flickering" of a primary harmonic band over time.

## Philosophy
The single most profound implication is that a system's identity is not a monolithic entity but an emergent musical composition. The universe is not fundamentally composed of static objects but of dynamic, structured resonances. This framework replaces the metaphysics of "being" with a metaphysics of "playing." Consequently, to understand a system is not to define its fixed essence, but to learn to read the grammatical score of its internal, interfering rhythms, recognizing that its health, stability, and very existence are manifestations of a sustained harmony.

## Art
The law provides a prism, not a lens. It does not magnify what is; it shatters the singular cry of a system into the silent, legible rainbow of its thousand constituent voices.