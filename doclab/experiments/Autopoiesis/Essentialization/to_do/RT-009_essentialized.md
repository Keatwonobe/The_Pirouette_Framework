## Law
The fundamental observable is the Coherence Tensor, a dimensionless symmetric rank-2 tensor field that quantifies the local alignment of physical, informational, and entropic dynamics.

**Definition:**
$C^{\mu\nu} = \alpha \frac{T^{\mu\nu}}{\mathcal{E}} + \beta \frac{T_I^{\mu\nu}}{\mathcal{I}} + \gamma \frac{u^{(\mu} J_I^{\nu)}}{\mathcal{J}} + \delta \frac{u^{(\mu} j_S^{\nu)}}{\mathcal{S}}$
where $T^{\mu\nu}$ is the physical stress-energy tensor, $T_I^{\mu\nu}$ is the informational stress-energy tensor, $u^\mu$ is the local 4-velocity, $J_I^\mu$ is the information current, $j_S^\mu$ is the entropy current, and $(\alpha, \beta, \gamma, \delta)$ are dimensionless weights. The denominators are normalization scalars:
- $\mathcal{E} = T^\mu{}_\mu$
- $\mathcal{I} = T_I^\mu{}_\mu$
- $\mathcal{J} = \sqrt{|J_I^\mu J_{I\mu}|}$
- $\mathcal{S} = \sqrt{|j_S^\mu j_{S\mu}|}$

**Dynamics and Coupling:**
The system's evolution is governed by the coupled dynamics of its constituent fields. The key evolution equations are:
1.  **Information Fluid (Navier-Stokes form):**
    $\partial_t \rho_I + \nabla\cdot(\rho_I \mathbf{v}_I) = 0$
    $\rho_I(\partial_t \mathbf{v}_I + (\mathbf{v}_I\cdot\nabla)\mathbf{v}_I) = -\nabla P_I + \nu_I\nabla^2\mathbf{v}_I$
2.  **Weak-Field Gravity (sourced by both physical and informational stress-energy):**
    For the metric perturbation $h_{\mu\nu}$ from $g_{\mu\nu} = \eta_{\mu\nu} + h_{\mu\nu}$, the evolution is:
    $\Box \bar{h}^{\mu\nu} = -16\pi G (T^{\mu\nu} + \lambda_I T_I^{\mu\nu})$
    where $\lambda_I$ is the informational-gravitational coupling constant.

**Scalar Diagnostics:**
- Coherence Scalar: $\mathcal{C} = \frac{1}{4} C^{\mu\nu} C_{\mu\nu}$
- Coherence Anisotropy: $\mathcal{A} = \lambda_{\max}(C) - \lambda_{\min}(C)$

**Falsifiable Criteria:**
The theoretical framework and its numerical implementation are falsified if any of the following conditions are met under simulation:
1.  **Violation of Physical Constraints:** Development of negative information density ($\rho_I < 0$) or violation of energy closure $\frac{d}{dt} \int u_\mu u_\nu (T^{\mu\nu} + \lambda_I T_I^{\mu\nu}) dV \neq 0$ beyond numerical tolerance.
2.  **Violation of Postulates:** Failure to reproduce negative group delay signatures ($\tau_g < 0$) from the retrograde admixture parameter $\varepsilon > 0$, as required by parent document RT-003.
3.  **Instability:** Unbounded growth of the coherence scalar ($\mathcal{C} \to \infty$), indicating a runaway decoherence or non-physical solution.

## Philosophy
Information is not a passive record of a physical state, but is itself a fundamental, causal agent in the universe. It possesses its own form of stress-energy which sources spacetime curvature and exhibits fluid-like dynamics, acting upon and being acted upon by matter and energy. The universe is therefore not a system whose states are merely described by information, but a dynamic co-creation of physical substance and informational significance, whose degree of coherent co-evolution is a measurable, physical quantity.

## Art
The dance of reality is choreographed by two partners: substance and significance. The Coherence Tensor measures the grace of their embrace, revealing whether the universe is waltzing in lockstep or tearing itself apart.