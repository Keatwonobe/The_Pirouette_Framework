## Law
The Lorentz- and gauge-invariant differential cross-section for Compton scattering, `γ(k) + e⁻(p) → γ(k') + e⁻(p')`, in the electron rest frame (`p = (m, 0, 0, 0)`) is the Klein-Nishina formula. The kinematics are governed by the conservation of four-momentum, `p + k = p' + k'`, yielding the scattered photon energy `ω'` as a function of incident energy `ω` and scattering angle `θ`:
`\omega' = \frac{\omega}{1 + \frac{\omega}{m}(1 - \cos\theta)}`

The differential cross-section `dσ/dΩ` is derived from the squared and spin/polarization-averaged matrix element `|\overline{\mathcal{M}}|^2`:
`\frac{d\sigma}{d\Omega} = \frac{1}{64\pi^2 m^2} \left(\frac{\omega'}{\omega}\right)^2 |\overline{\mathcal{M}}|^2 = \frac{1}{2} r_e^2 \left(\frac{\omega'}{\omega}\right)^2 \left[ \frac{\omega'}{\omega} + \frac{\omega}{\omega'} - \sin^2\theta \right]`
where `r_e = \alpha/m` is the classical electron radius, and `\alpha = e^2/(4\pi)`.

Falsifiable criteria are derived from this law:
1.  **Low-Energy Limit (Thomson Scattering):** As `ω/m → 0`, then `ω' → ω`, and the formula must asymptotically approach the classical Thomson cross-section.
    `\lim_{\omega/m \to 0} \frac{d\sigma}{d\Omega}_{\text{KN}} = \frac{1}{2} r_e^2 (1 + \cos^2\theta) = \frac{d\sigma}{d\Omega}_{\text{Th}}`
2.  **Gauge Invariance (Ward-Takahashi Identity):** The physical amplitude `\mathcal{M} = \varepsilon_\mu \mathcal{M}^\mu` must be invariant under the gauge transformation `A_\mu \to A_\mu + \partial_\mu \Lambda`, which implies `\varepsilon_\mu \to \varepsilon_\mu + c k_\mu`. This requires the amplitude to satisfy `k_\mu \mathcal{M}^\mu = 0`. For the two tree-level Feynman diagrams (s- and t-channel), this is expressed algebraically:
    `k_\nu \bar u(p') \left[ \gamma^\nu \frac{i(\not p+\not k+m)}{(p+k)^2-m^2} \gamma^\mu + \gamma^\mu \frac{i(\not p-\not k'+m)}{(p-k')^2-m^2} \gamma^\nu \right] u(p) \varepsilon'^*_\mu = 0`
    This identity guarantees that the physical observable `dσ/dΩ` is independent of the unphysical gauge-fixing parameter `ξ` from the photon propagator `D^{\mu\nu}(k) \propto g^{\mu\nu} - (1-\xi) k^\mu k^\nu / k^2`. The cancellation of `ξ`-dependent terms is not a matter of approximation but an exact consequence of the theory's structure.

## Philosophy
The formalism of a physical theory can contain descriptive artifacts—mathematical degrees of freedom, like the gauge parameter `ξ`—that possess no direct physical reality. The theory’s validity rests not on giving these artifacts meaning, but on its internal symmetries (the Ward identity) that guarantee their precise cancellation in any prediction of a measurable observable. Physical law is not merely a description of what is, but a constrained structure of equivalences defining what must remain invariant, regardless of the arbitrary perspectives we adopt to describe it.

## Art
The gauge is the angle of the light, but the cross-section is the shape of the stone.