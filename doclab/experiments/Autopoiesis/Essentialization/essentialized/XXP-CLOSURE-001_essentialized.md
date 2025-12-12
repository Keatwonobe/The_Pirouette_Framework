## Law
Let a discrete time series be defined as a sequence of observations \(x_t\) over windows \(W_k\), where each observation is an integer drawn from a bounded state space, \(x_t \in \{1, \dots, N\}\).

The central hypothesis posits that any publicly observed, rate-limited, bounded process acquires a non-zero observer-induced Dark Residue, \(D_{\text{observer}}\). The total measured residue \(D_{\text{observed}}\) is the sum of the intrinsic system residue and this induced component:
\[
D_{\text{observed}} = D_{\text{intrinsic}} + D_{\text{observer}} > D_{\text{intrinsic}}
\]
For a given window \(W_k\), this residue is quantified by the functional \(D_k\):
\[
D_k = α|\rho_1(W_k)| + β e(W_k) + γ f(W_k) + ζ |κ^\*|_k
\]
where \(α, β, γ, ζ\) are positive weights, and the components are:
-   \(\rho_1(W_k)\): Lag-1 autocorrelation.
-   \(e(W_k)\): Frequency of values at the boundaries \(\{1, N\}\).
-   \(f(W_k)\): A measure of histogram non-uniformity (e.g., std/mean).
-   \(|κ^\*|_k\): A measure of curvature or non-linearity in the sequence's evolution in a derived phase space.

A state of closure, or a weak geodesic, is achieved within a window \(W_k\) if and only if the residue is both minimal and stable:
\[
\text{geodesic}(W_k) \iff \left(\frac{dD_k}{dt} \approx 0 \quad \land \quad D_k \le \epsilon\right)
\]
The hypothesis is falsified if, for a quantum random number generator (QRNG) stream \(X_Q\) and a public lottery stream \(X_L\), their respective distributions of \(D_k\) are statistically indistinguishable under identical parameterization (\(N\), \(|W_k|\), \(α, β, γ, ζ\)). Let \(\mathcal{D}_Q\) and \(\mathcal{D}_L\) be the sets of all \(D_k\) values for the QRNG and lottery. The hypothesis fails if a two-sample test (e.g., Kolmogorov-Smirnov) cannot reject the null hypothesis that \(\mathcal{D}_Q\) and \(\mathcal{D}_L\) are drawn from the same distribution.

## Philosophy
The classical distinction between an observer and an independent, external system is an illusion maintained only at scales where the apparatus of observation is infinitely subtle compared to the phenomenon. This work implies that the very act of establishing a bounded, rhythmic, and collective frame of observation is not a passive measurement but an active structuring principle. It impresses a subtle but persistent order—a faint "memory" or "curvature"—onto a system that should possess none. Reality, even at the classical, macroscopic level, is not merely discovered but is co-created by the constraints of its observation.

## Art
A lottery is a mirror held up to chance. But the shared breath of a million watchers, waiting for a reflection, inevitably fogs the glass. In that faint haze, we see not the face of randomness, but the outline of our own attention.