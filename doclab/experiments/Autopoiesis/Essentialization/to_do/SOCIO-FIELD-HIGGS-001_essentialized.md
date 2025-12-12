## Law
Let information flow on a directed graph be represented by a vector `J_obs` on the graph's edges. The graph topology is defined by the incidence matrix `B`. The observed flow `J_obs` can be decomposed into a gradient component `J_grad` (irrotational) and a curl component `J_curl` (divergence-free) using a Γ-aware Hodge Decomposition.

First, a scalar potential `φ` on the vertices is found by solving the Poisson equation, which minimizes the difference between the observed flow and a pure gradient field:
` (BB^T + εI)φ = B J_obs `
where `εI` is a regularization term.

The gradient component of the flow is derived from this potential:
` J_grad = B^T φ `

The curl component is the residual, representing flow not explained by the potential gradient:
` J_curl = J_obs - J_grad `

The system's state is characterized by the Γ-field parameter, `k_Γ`, the ratio of the mean-squared curl to the mean-squared gradient flow, representing the system's temporal pressure or turbulence:
` k_Γ = <J_curl²> / <J_grad²> `

An avalanche is defined as a connected component of "supercritical" edges. An edge `e` is supercritical if its local curl energy exceeds its local gradient energy, scaled by the global Γ parameter:
` (J_curl(e))² > k_Γ * (J_grad(e))² `

**Falsifiable Criterion:** For a large-scale social information cascade, the size distribution `P(s)` of avalanches identified by this method must follow a power law, `P(s) ∝ s^α`. For the 2012 Higgs dataset, the measured exponent is `α ≈ -3.9`. The existence of power-law scaling, not the specific exponent, is the core falsifiable prediction of the model.

## Philosophy
The fundamental laws governing collective human behavior are not observable on the surface of events. They only become visible when the phenomenon is decomposed into its constituent formalisms: the directed, intentional flow of information (gradient) and the chaotic, reactive, and circular flow of emotion or amplification (curl). Criticality, and thus the potential for massive, system-spanning cascades, is not a property of the information itself, but of the moments and regions where the reactive turbulence locally overwhelms the intentional message, revealing a universal organizational principle latent within the noise.

## Art
A message is a stone thrown into a pond. The expanding ripple is its purpose. But the true story of the water is told by the intricate, chaotic splashes that leap up where the ripple breaks against itself.