## Law
The governing principle is the maximization of the Pirouette Action, $S_p$, for a system path $x(t)$.
$$S_p[x(t)] = \int_{t_1}^{t_2} \mathcal{L}_p(x, \dot{x}, t) \, dt$$
where the Pirouette Lagrangian is defined as the differential between Temporal Coherence ($K_\tau$) and Temporal Pressure ($V_\Gamma$):
$$\mathcal{L}_p = K_\tau - V_\Gamma$$
The Surveyor's Problem is the inverse: given a sparse set of observations $\{\vec{x}_j\}_{j=1..N}$ on a geodesic of $S_p$, infer the qualitative magnitudes of the functional terms $K_\tau$ and $V_\Gamma$. This is achieved by mapping heuristic estimators to a state diagnosis.

Define estimators $\hat{K}_\tau$ and $\hat{V}_\Gamma$:
1.  **Coherence Estimator ($\hat{K}_\tau$):** Measures path regularity and internal rhythm.
    *   Phase Coherence: $\hat{K}_\tau \propto P_c = \left| \frac{1}{N} \sum_{j=1}^{N} e^{i\theta_j} \right|^2$
    *   Normalized Variance Proxy: $\hat{K}_\tau \propto (1 - \sigma^2(\{\vec{x}_j\}) / \sigma^2_{max})$
2.  **Pressure Estimator ($\hat{V}_\Gamma$):** Measures path dispersion and environmental volatility.
    *   Dispersion Metric: $\hat{V}_\Gamma \propto \text{Var}(\{\vec{x}_j\})$
    *   Jump Frequency: $\hat{V}_\Gamma \propto \frac{1}{T} \sum_{j} H(\Vert\vec{x}_{j+1} - \vec{x}_j\Vert - \theta_{thr})$ where $H$ is the Heaviside step function.

The system state is diagnosed via the mapping $D: (\hat{K}_\tau, \hat{V}_\Gamma) \to \{\text{Laminar, Turbulent, Resilient, Erosional}\}$. Let $H$ denote high magnitude and $L$ denote low magnitude.
*   $D(K_H, V_L) \implies$ **Laminar Flow**: System follows a low-resistance geodesic.
*   $D(K_L, V_H) \implies$ **Turbulent Flow**: System coherence is overwhelmed by environmental pressure.
*   $D(K_H, V_H) \implies$ **Resilient Struggle**: System maintains internal coherence against high environmental pressure.
*   $D(K_L, V_L) \implies$ **Coherence Erosion**: System decays due to internal failure, not external pressure.

This model is falsified if a system diagnosed in a specific state consistently fails to exhibit the predicted aggregate behaviors under dense sampling. For example, a system diagnosed as "Resilient Struggle" from sparse data must, under full observation, exhibit both high internal periodicity and high-amplitude external perturbation.

## Philosophy
The most profound implication is the reframing of inference under uncertainty: when data is sparse, the most rational and scientifically rigorous act is not to pursue a precise, quantitative estimate that is likely false, but to construct a qualitative, narrative diagnosis that is likely true. It replaces the epistemology of statistical estimation with an epistemology of hermeneutic interpretation. We do not calculate a parameter from a fragment of evidence; we intuit the character of the drama from a single line of dialogue. This suggests that for complex systems, the ultimate goal of science may not be prediction in figures, but understanding in stories.

## Art
To know the shape of the wind, do not count the fallen leaves; watch the dance of the one still on the branch.