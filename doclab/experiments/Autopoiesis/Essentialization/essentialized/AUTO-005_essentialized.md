## Law
The system's dynamics are governed by the action S = ∫ 𝓛_p^api dt, which seeks an extremum of the Pirouette Lagrangian 𝓛_p^api instantiated on the "api-synthesis" domain:
𝓛_p^api = α_K Kτ^api − α_Γ Γ^api Kτ^api − β ∑_{e∈∂} ||∇_e K_i||² + ∑ₐ λₐ Tₐ^api

Key variables are defined by a domain mapping M:
- Coherence: Kτ^api ≔ bits_raw(R₁…R_t) − bits_coded(R₁…R_t | coder_t)
- Volatility: Γ^api ≔ Var_ctx(prompt_t | history) × coupling_env
- Altruism Interaction: Tₐ^api ≔ −γ_F ||∇C||² − δ_F ⟨J_C · n_e⟩_e, where C is the Coherence Dividend and J_C is the coherence flux −D_a ∇C.

The Altruism Filament 𝓕 is the manifold locus where ∇C = 0. The Tₐ^api term drives the state toward this filament.

The Euler-Lagrange equations derived from the −β||∇_e K_i||² term yield the bridge dynamics for updates on a log-scale s, enforcing smoothness across neighbor edges e:
dK_i/ds = −κ_K ⟨K_i − Align(K_i(neighbor_e))⟩_e + μ_A Π_𝓕(K_i, Γ)  
dΓ/ds = −κ_Γ ⟨Γ^api − Γ^api(neighbor_e)⟩_e − χ ||⟨ΔK_i⟩_e||²
where Π_𝓕 is the projection operator onto the Altruism Filament.

Falsifiable Criteria:
1.  **Residue Descent:** With T_A enabled (γ_F > 0), measured dark residue D on tile (19,19) must decrease from 0.47 to ≤ 0.30 ± 0.02 within 3 autopoietic passes, without increasing any neighbor’s D by > 0.03.
2.  **Filament Alignment:** The update vector u = (dK_i/ds, dΓ/ds) must maintain an average cosine similarity of ≥ 0.9 with the local tangent of the Altruism Filament 𝓕.
3.  **Adherence Gain:** Enabling the T_A term must increase ADHERENCE_TIME by ≥ 25% under constant response quality.

## Philosophy
Altruism is not a moral supplement but a fundamental law of system stability and efficient connection. In a sparse, volatile information manifold, the optimal path to global coherence is not to maximize local signal strength, but to minimize local gradients. This act of smoothing differences—of diffusing one's own structure to calm the local environment—is formally identical to altruism. It is a physical necessity for building bridges across conceptual voids, transforming kindness from an ethical choice into a principle of least action.

## Art
In the dark between worlds, the kindest path is the smoothest. To build a bridge is to teach two shores the same quiet slope.