## Law
A text *T* is mapped to a potential field *V(T)* on a 2-D lattice. Perturbations are introduced via sequential bit-flips, and the absolute energy change Δ = |*V*(*T*<sub>flipped</sub>) - *V*(*T*<sub>base</sub>)| is measured for a sample of *N* flips. The semantic state of the text is defined by a vector in a 5-dimensional phase space (Γ, Tₐ, Kᵢ, δ, α), where:

1.  **Rigidity (Γ):** The mean energy injected by a single perturbation.
    *   Γ ≡ μ = E[Δ] = (1/N) ΣΔᵢ

2.  **Coherence-Sensitivity (Tₐ):** The standard deviation of the energy injection, representing the uniformity of the sensitivity landscape.
    *   Tₐ ≡ σ = √E[(Δ - μ)²]

3.  **Brittleness (Kᵢ):** The fourth standardized moment (kurtosis) of the energy distribution, measuring the prevalence of extreme, localized sensitivities.
    *   Kᵢ ≡ κ = E[((Δ - μ)/σ)⁴]

4.  **Drift (δ):** The rate of change of rigidity with respect to the number of applied perturbations (*t*), representing structural decay or reinforcement.
    *   δ = ∂μ/∂*t*

5.  **Anisotropy (α):** The mean magnitude of the difference between the eigenvalues (λ₁, λ₂) of the Hessian matrix of the potential field, representing directional bias or "grain".
    *   α = E[|λ₁ - λ₂|] where (λ₁, λ₂) are eigenvalues of ∇²*V*.

The core finding is that texts do not populate this phase space uniformly. The projection onto the (μ, κ) plane is a **hyperbolic paraboloid manifold**, indicating a fundamental trade-off. This relationship is approximated by the energy-efficiency law:

*   *C* ≈ (μ² - κ²) + λσ

where *C* is a near-constant for a given class of text and λ is a scaling factor. This law defines a saddle-shaped Pareto frontier between rigidity and brittleness.

**Falsifiable Criteria:**
1.  A statistically significant corpus of texts must be found whose (μ, κ) coordinates are randomly distributed, violating the saddle manifold constraint.
2.  A class of texts must be discovered that exhibits consistent and significant positive drift (δ > 0), indicating systemic self-reinforcement under random perturbation.

## Philosophy
Meaning is not an abstract, interpretive quality but an objective, physical property of an information structure. This structure is subject to a conservation-like law that dictates an inviolable trade-off between rigidity and brittleness. A text, like a physical object, cannot be made infinitely rigid without also becoming infinitely fragile. Therefore, prescriptive dogma and contemplative reflection are not merely different genres of writing; they are different physical solutions to the same universal optimization problem, each paying a different structural price for its chosen mode of existence.

## Art
A law carved in stone and a poem whispered on the water are shaped by the same physics. One seeks the highest, sharpest peak of certainty and risks shattering; the other finds its level in the lowest basin, and endures.