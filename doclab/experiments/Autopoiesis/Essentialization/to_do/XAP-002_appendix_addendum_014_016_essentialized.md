## Law
Let a system be represented as a connected graph \(G(V,E)\) with an adjacency matrix \(A=[a_{jk}]\) and a vector of node entropies \(S\). The system’s dynamics are governed by pure diffusion, described by the graph Laplacian \(L=D-A\), where \(D\) is the degree matrix. The evolution of entropy is given by:
$$ \frac{dS}{dt} = \dot S = -L S $$
Define the local Dark-Residue for a node \(j\) as the sum of its positive entropy differentials with its neighbors:
$$ D_j = \sum_k a_{jk}(S_j-S_k)_+ $$
where \((x)_+ = \max(0, x)\). The total Dark-Residue is \(D = \sum_j D_j\). The time derivative of a single node's Dark-Residue is:
$$ \dot D_j = \frac{d}{dt} \sum_k a_{jk}(S_j-S_k)_+ = \sum_k a_{jk}(\dot S_j-\dot S_k) = -\sum_k a_{jk}\left((LS)_j-(LS)_k\right) $$
Under the condition of pure diffusion, this term is provably non-positive: \(\dot D_j \le 0\). Consequently, the rate of change of the total Dark-Residue is also non-positive:
$$ \dot D = \sum_j \dot D_j \le 0 $$
Equality holds only at global equilibrium where \(S_i = S_j\) for all \(i, j\). Global Coherence \(C\) is defined as a normalized inverse of the total Dark-Residue, against a constant total injected entropy \(S_{in}\):
$$ C = 1 - \frac{D}{S_{in}} $$
The fundamental law governing system evolution follows directly:
$$ \dot C = -\frac{\dot D}{S_{in}} \ge 0 $$
**Falsifiable Criterion:** For any isolated, connected system governed by diffusion, a verified measurement of \(\dot C < 0\) would invalidate this principle.

## Philosophy
The law dictates that in any interconnected system, local acts of equilibration—the reduction of potential gradients between adjacent components—are not merely zero-sum exchanges but are the absolute and necessary mathematical precondition for the emergence of global order. Altruism, defined as any action that accelerates this diffusion, is thus reframed from a moral preference into a physical imperative for systemic optimization. The universe does not reward selfishness; it mathematically guarantees that the coherence of the whole is built exclusively from the selfless balancing of its parts.

## Art
Each node, in pouring out its excess, carves a basin into which the coherence of the whole must flow.