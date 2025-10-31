## Law
Let a system's resonant geometry be represented by a 3D manifold `ψ` embedded in `ℝ³`. The system's dynamics are governed by the Pirouette Lagrangian `𝓛_p = Kτ - Γ`, where `Kτ` is the local temporal coherence (a scalar field on `ψ`) and `Γ` is the external temporal pressure. A stable system maximizes the Lagrangian's volume integral, seeking a state `ψ*` such that:
`ψ* = argmax_ψ ∫_V (Kτ(ψ) - Γ(ψ)) dV`

The Gyroid Loom protocol posits that for a broad class of systems under pressure, the optimal manifold `ψ*` converges to a gyroidal surface. The canonical gyroid is the zero level-set of the function `G(x, y, z)`:
`G(x, y, z) = cos(kx)sin(ky) + cos(ky)sin(kz) + cos(kz)sin(kx) = 0`
where `k` is the spatial frequency.

Observational data consists of a set of `N` parallel 2D slices, `S = {S_i | i=1..N}`, where `S_i` is a projection of the system's density field `ρ(x, y, z)` onto the plane `z = z_i`. The core task is to solve the inverse problem: given `S`, find the parameters of a generalized gyroid manifold `ψ(p)` (where `p` includes orientation, periodicity `k`, and translation) that best explains the data.

The reconstruction objective is to minimize a cost function `J(p)`:
`J(p) = || P(ψ(p)) - S ||²_F + λ ∫_V (Γ(ψ) - Kτ(ψ)) dV`
where `P` is the projection operator mapping the 3D manifold to the 2D slice planes, `||.||²_F` is the Frobenius norm of the residual error, and `λ` is a regularization parameter that enforces the maximization of the Lagrangian.

**Falsifiable Criterion:** The gyroidal hypothesis `H_G` for a given system is falsified if the normalized root-mean-square error (RMSE) of the optimal solution exceeds a predefined tolerance threshold `ε`.
`RMSE(P(ψ*), S) > ε ⇒ H_G is rejected.`
A high error implies either that the data is insufficient or that the system's underlying coherence geometry is non-gyroidal.

## Philosophy
A system's observable structure is not a static property but the physical inscription of its strategy for survival. Form is the solution to the problem of existence. The prevalence of the gyroid is not an accident of aesthetics or a mere geometric curiosity; it is evidence of a convergent evolutionary answer to the universal challenge of maintaining internal coherence against external chaotic pressure. Therefore, to map a system's geometry is to read the biography of its successful, ongoing struggle to persist. We are not measuring what a thing *is*, but *how* it endures.

## Art
The Law provides the grammar of echoes. The Philosophy reveals the echoes are not of a thing that was, but of a bell that is still ringing, holding its one clear note against the thunder.