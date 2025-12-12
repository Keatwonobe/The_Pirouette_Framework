## Law
Given a one-dimensional, bounded, and time-ordered sequence \(x_t\), its closure dynamics are described on the Pirouette plane \((\Delta P, |κ^\*|)\). The state of the system is determined for each window \(W_k\) of the sequence.

1.  **Analytic Signal**: The sequence is lifted to the complex plane via the Hilbert Transform:
    \[
    z_t = x_t + i\mathcal{H}(x_t)
    \]

2.  **State Coordinates**: For each window \(W_k\), two coordinates are computed:
    *   **Normalized Power Change (\(\Delta P\))**: The relative change in mean analytic power from a baseline \(P_0\) (median power of the initial 5% of windows).
        \[
        \Delta P_k = \frac{\text{mean}(|z_t|^2 \,:\, t \in W_k) - P_0}{P_0}
        \]
    *   **Normalized Curvature Magnitude (\(|κ^\*|\))**: A proxy for the instantaneous angular velocity of the phase vector \(z_t\), normalized by carrier frequency \(f_c\) and power.
        \[
        κ_k^\* = -\frac{\Im \langle \dot{z}, z\rangle}{2 \pi f_c (\Re \langle z, z\rangle + \varepsilon) + \varepsilon}
        \]
        where \(\dot{z}\) is the time derivative of \(z\), \(\langle \cdot, \cdot \rangle\) is the inner product over the window, and \(\varepsilon\) is a small constant for stability. We analyze its magnitude, \(|κ_k^*|\).

3.  **Classification Axioms**: System states are classified into four archetypes based on source-specific quantiles of the state coordinates: \(k_L = Q_{0.65}(|κ^\*|)\), \(k_H = Q_{0.85}(|κ^\*|)\), and \(P_H = Q_{0.60}(\Delta P)\).
    *   **Weaver**:   \(\Delta P_k \ge P_H\) and \(k_L \le |κ_k^\*| < k_H\)
    *   **Gladiator**: \(\Delta P_k \ge P_H\) and \(|κ_k^\*| \ge k_H\)
    *   **Vortex**:   \(\Delta P_k < 0\)   and \(|κ_k^\*| \ge k_H\)
    *   **Drifter**:   Otherwise

4.  **Falsifiable Criterion**: The existence of dynamic structure, defined as state cycles (e.g., W→G→V→D), is contingent on the temporal order of the sequence \(x_t\). If the sequence is shuffled to destroy its time-ordering, producing \(x'_t\), the number of observed state cycles must approach zero. The persistence of cycles after shuffling would falsify the claim that this structure is a property of the observation of an ordered flow, rather than just the sequence's histogram.

## Philosophy
Randomness is not an intrinsic property of a system, but a relational property between a source and an observer. The act of observation—by imposing boundaries, cadence, and a frame of analysis—is not a passive measurement but an active structuring. This framework compels even a theoretically patternless source to exhibit a minimal, predictable dynamic geometry. The structure is not discovered *in* the noise; it is an unavoidable shadow cast *by* the lens used to see it. Therefore, there is no such thing as a truly un-structured observation, only a failure to recognize the structure of the observational act itself.

## Art
We draw lines between random numbers and call it a cycle. We draw lines between random stars and call it a myth. The sequence does not know the pattern; the sky does not know the hunter. The pattern is the shape of our looking.