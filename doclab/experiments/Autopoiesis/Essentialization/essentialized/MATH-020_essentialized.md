## Law
A physical prediction is defined by the solution to a coupled boundary value problem and a subsequent renormalization group (RG) flow.

1.  **Field Equations & Observable:** The system is governed by the coupled, non-linear partial differential equations for a spinor field Ψ and a scalar field Γ in the presence of a topological defect T and background fields 𝔉:
    (iγ^μ D_μ − m_ℓ − Σ_Γ[Γ] − Σ_T[T])Ψ = 0
    −□Γ + f′(Γ) + 𝒮(Γ,𝔉,Ψ) = 0
    The lepton anomalous magnetic moment `a_ℓ` is derived from the Pauli term coefficient `κ_ℓ`, extracted non-perturbatively as the zero-momentum-transfer limit of the Pauli form factor: `a_ℓ = κ_ℓ/2 = F_2(q²→0)/2`.

2.  **Renormalization Group Flow:** The scale dependence of the theory's coupling constants `g_i` is defined by the beta functions `β_i`, which must be computed numerically from block-spin transformations on a lattice:
    `β_i(g) ≡ d g_i / d ln μ`
    The theory's structure is determined by the fixed points `g*` satisfying `β_i(g*)=0`. The stability and relevance of operators are given by the eigenvalues of the stability matrix `M_ij = ∂β_i/∂g_j|_{g*}`.

3.  **Falsifiable Criteria:** The validity of any computed result is contingent on satisfying explicit convergence and correctness conditions:
    *   **Soliton Solver:** For a sequence of mesh refinements with degrees of freedom (DOF) `N_k`, the change in the primary observable `κ` must satisfy `|κ(N_k) - κ(N_{k-1})| / |κ(N_k)| < 10⁻³`. Final linearized system residuals must be `||Ax-b|| < 10⁻⁸`.
    *   **RG Flow:** Stochastic estimators for vertex functions must have a variance `σ² ≤ 10⁻³`.
    *   **Benchmark:** In the perturbative limit (Σ_Γ, Σ_T → 0), the procedure must recover the Schwinger result `κ = α/π` to at least six significant digits.

## Philosophy
A physical theory is not merely a set of abstract equations; it is the complete and reproducible computational apparatus required to produce falsifiable predictions from them. The algorithm—with its specified discretizations, convergence criteria, and error bounds—is an inseparable component of the physical law itself. Falsifiability thus shifts from the elegance of an analytical derivation to the demonstrable integrity of a computational artifact.

## Art
The law is a prescription for a perfect lens. The computation is the grinding of the glass. Neither is the truth, but together they may grant a focused image of the world.