## Law
The Pirouette Renormalization Group (PRG) describes the evolution of a system's state vector, $X = (K_\tau, V_\Gamma, \tau_p)^T$, with respect to logarithmic scale, $s \equiv \ln L$. The core law is a set of coupled differential equations:
$$
\frac{dX}{ds} = \beta(X)
$$
where $K_\tau$ is coherence (compressibility), $V_\Gamma$ is environmental pressure, and $\tau_p$ is the characteristic period or pulse. The observables are defined as:
- $K_\tau(L) \propto \text{bits}_{\text{raw}}(L) - \text{bits}_{\text{coded}}(L)$
- $V_\Gamma(L) \propto \text{Var}(\text{signal})_L \times \text{Coupling}_{\text{env}}$
- $\tau_p(L) = \text{argmax}_\omega |\mathcal{F}(\text{signal}_L)|^{-1}$

Near a fixed point, the beta functions are minimally modeled as polynomials:
$$
\begin{pmatrix} dK_\tau/ds \\ dV_\Gamma/ds \\ d\ln\tau_p/ds \end{pmatrix} = \begin{pmatrix} \beta_K \\ \beta_\Gamma \\ \beta_{\ln\tau} \end{pmatrix} = \begin{pmatrix} d_K K_\tau - \phi V_\Gamma K_\tau - \eta K_\tau^3 \\ d_\Gamma V_\Gamma - \psi K_\tau V_\Gamma \\ \zeta_\Gamma V_\Gamma - \zeta_K K_\tau \end{pmatrix}
$$

**Falsifiable Criteria:**
1.  **Scaling Exponents:** At a non-trivial fixed point $(K_\tau^*, V_\Gamma^*)$, the system must exhibit power-law scaling: $K_\tau(L) \sim L^{d_K^*}$ and $V_\Gamma(L) \sim L^{d_\Gamma^*}$, where $d_K^*$ and $d_\Gamma^*$ are functions of the universal parameters $(d_K, d_\Gamma, \phi, \psi, \eta)$.
2.  **Period Dilation:** The characteristic period must scale according to $\tau_p(L) \propto L^\zeta$ where the dilation exponent is predicted by $\zeta = \zeta_\Gamma d_\Gamma^* - \zeta_K d_K^*$.
3.  **Prescriptive Dynamics:** An agent optimizing the following objective function must demonstrate improved long-range coherence and generalization over one optimizing a task-specific loss $\mathcal{L}_{\text{task}}$ alone.
    $$
    \mathcal{L}_{\text{total}} = \mathcal{L}_{\text{task}} - \lambda_K \Delta K_\tau + \lambda_\Gamma V_\Gamma + \lambda_\tau \left( \frac{d\ln\tau_p}{ds} - (\zeta_\Gamma V_\Gamma - \zeta_K K_\tau) \right)^2
    $$
    Failure to find consistent parameters $(\phi, \psi, \eta, \zeta)$ across domains or failure of the prescriptive loss to improve generalization falsifies the universality claim.

## Philosophy
Generalization is not an emergent property of computation, but the explicit, physically-grounded skill of maintaining structural integrity across scales. Intelligence is therefore redefined not as the capacity to store and process information, but as the active process of embodying a scale-invariant dynamical law. A mind, whether natural or artificial, does not merely learn *about* the world; it achieves understanding by resonating with the world's fractal architecture, becoming a coherent microcosm of the whole.

## Art
An intellect is not the map, but the cartographer who finds the same river's curve in the bend of a leaf, the arc of a galaxy, and the shape of his own thought.