## Law
The universal two-loop coefficient, $C_2$, in the perturbative expansion of the lepton anomalous magnetic moment $a_\ell \equiv (g_\ell-2)/2$ is defined by:
\[
a_\ell(\alpha) = \sum_{n\ge1} C_n \left(\frac{\alpha}{\pi}\right)^n = \frac{1}{2}\left(\frac{\alpha}{\pi}\right) + C_2\left(\frac{\alpha}{\pi}\right)^2 + \mathcal{O}(\alpha^3)
\]
This coefficient is a finite physical constant derived from the Pauli form factor $F_2(q^2)$ in the limit $q^2 \to 0$, subject to the on-shell renormalization conditions for the electron self-energy $\Sigma(\slashed p)$:
\[
\Sigma(\slashed p=m)=0, \qquad \left.\frac{\partial\Sigma(\slashed p)}{\partial \slashed p}\right|_{\slashed p=m}=0
\]
The value of $C_2$ is obtained by summing the contributions from all gauge-invariant two-loop 1PI vertex topologies. Two equivalent formalisms yield the same result:

1.  **Background-Field Method (BFM):** The coefficient is the sum of finite parts of dimensionally regularized Feynman parameter integrals for three classes of diagrams: (T1) vacuum polarization, (T2) irreducible vertex, and (T3) self-energy/vertex counterterms.
    \[
    C_2 = \sum_{i=1}^3 F_2^{(Ti)}(0) = \frac{\alpha^2}{\pi^2} \int\!\!\int_{[0,1]^2} d\vec{x} \left( \mathcal{K}_{T1}(\vec{x}) + \mathcal{K}_{T2}(\vec{x}) + \mathcal{K}_{T3}(\vec{x}) \right)_{\text{fin}}
    \]
    where $\mathcal{K}$ are polylogarithmic kernels dependent on Feynman parameters $\vec{x}$, and the finite part is extracted after UV divergence cancellation via on-shell counterterms.

2.  **Worldline (Proper-Time) Formalism:** The coefficient is derived from the worldline representation of the spinor effective action with one internal photon exchange.
    \[
    C_2 = \int_0^\infty \frac{dT}{T} e^{-m^2 T} \int_0^1 du \int_0^1 dv \; \mathcal{K}_{\text{WL}}(T, u, v)
    \]
    where $\mathcal{K}_{\text{WL}}$ is the renormalized two-loop worldline kernel.

Both methods yield the positive numerical value:
\[
C_2 = +\frac{197}{144} + \frac{\pi^2}{12} - \frac{\pi^2}{2}\ln(2) + \frac{3}{4}\zeta(3) \approx +0.328478965\ldots
\]
**Falsifiable Criterion:** In any theory that reduces to QED in its low-energy limit, and using the on-shell renormalization scheme with metric signature $(+,-,-,-)$, the universal coefficient must be positive definite: $C_2 > 0$. A negative result would falsify the calculational framework or its underlying assumptions.

## Philosophy
The existence of multiple, independent, and formally disparate calculational paths—one based on the discrete, combinatorial accounting of virtual particle interactions (Feynman diagrams), the other on the continuous integration over all possible spacetime trajectories (worldline path integrals)—that converge to the identical, high-precision physical constant is not a mathematical coincidence. It reveals that physical law possesses an intrinsic duality of description. The granular, event-based language of quantum field theory is perfectly isomorphic to a holistic, geometric language of worldline evolution. An interaction is not merely analogous to a change in geometry; at the fundamental level of calculation and prediction, it *is* a change in geometry.

## Art
A particle’s path is a tapestry woven from the exchange of ghosts.