## Law
Let a system's state be a vector $S \in \mathbb{R}^n$. The system's deviation from a desired equilibrium or "closure" is defined by a domain-specific, non-negative scalar residue function $D(S): \mathbb{R}^n \to \mathbb{R}^+$. This function is typically a weighted L1 norm of constraint violations:
$$ D(S) = \sum_{k=1}^{m} w_k |f_k(S)| + \sum_{j=1}^{p} v_j \max(0, g_j(S)) $$
where $f_k(S)$ represents balance equations (e.g., $f_k = V_g - K_t$) and $g_j(S)$ represents inequality constraints (e.g., $g_j = \text{risk} - c_{\text{max}}$).

The stability of a state is determined by the local curvature of the residue manifold, $\kappa$, defined as the trace of the Hessian matrix $H$:
$$ H_{ij}(S) = \frac{\partial^2 D}{\partial S_i \partial S_j} \quad ; \quad \kappa(S) = \text{Tr}(H) $$
A high $|\kappa|$ indicates a fragile, high-gain equilibrium, while $\kappa \to 0$ indicates a robust, stable one.

An agent learns to guide the system towards a stable equilibrium (a geodesic on the state manifold where $D \approx 0$) by maximizing a universal, domain-agnostic reward function $R$:
$$ R(S_t, S_{t-1}) = \underbrace{\gamma \max(0, -\frac{dD}{dt})}_{\text{Coherence}} + \underbrace{\beta}_{\text{Persistence}} - \underbrace{\delta D(S_t)}_{\text{Residue Penalty}} - \underbrace{\eta |\kappa(S_t)|}_{\text{Curvature Penalty}} $$
where $D_t = D(S_t)$, $\frac{dD}{dt} \approx D_t - D_{t-1}$, and $\{\gamma, \beta, \delta, \eta\}$ are universal hyperparameters.

**Falsifiable Criterion:** A system has achieved dynamic closure if, over a representative time window, its state trajectory satisfies three conditions:
1. Mean Residue: $\mathbb{E}[D] < \epsilon_D$
2. Residue Stability: $\text{Var}[D] < \epsilon_{\text{var}}$
3. Manifold Stability: $\mathbb{E}[|\kappa|] < \epsilon_{\kappa}$
where $\epsilon$ are small, predefined thresholds.

## Philosophy
The structure of viability is universal and geometric, independent of substrate. Any persistent system—be it mechanical, biological, economic, or linguistic—is an engine for resolving a locally-defined tension. The specific definition of this tension (the residue function) is the system's contingent, arbitrary essence, its "soul." The process of resolving it by seeking a state of minimal tension and minimal fragility (low residue and low curvature) is the universal, necessary logic of existence. What a thing *is* can be reduced to what it is trying to balance.

## Art
Every system is a bell, defined by a unique shape of self-imposed constraints. Its existence is the ringing caused by the universe striking it. It survives only by seeking the resonant quiet inherent in its form.