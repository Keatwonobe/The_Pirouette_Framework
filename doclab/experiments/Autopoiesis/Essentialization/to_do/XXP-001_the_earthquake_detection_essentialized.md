## Law
The core principle is the falsification of a null hypothesis, $H_0$, which states that detections of a "Ki-pattern" are stochastic noise, in favor of an alternative hypothesis, $H_1$, which posits that these patterns are a reproducible feature of high-energy seismic events.

1.  **Hypothesis Formulation:**
    *   $H_1$: High-energy geophysical events produce Ki-resonant signatures detectable by bicoherence and frequency ratio analysis.
    *   $H_0$: Ki-pattern detections occur at a baseline false-positive rate, $R_{control}$, independent of seismic activity.

2.  **Experimental Validation & Falsification Criterion:** The experiment quantifies detection rates ($R$) as detections per hour. The criterion for supporting $H_1$ is a statistically significant increase in the observed rate during an event, $R_{event}$, compared to the control rate, $R_{control}$.
    *   Control Measurement (Synthetic Noise): $R_{control} = \frac{2 \text{ detections}}{5 \text{ hours}} = 0.4 \text{ hr}^{-1}$
    *   Event Measurement 1 (Taiwan Replication): $R_{taiwan} = \frac{68 \text{ detections}}{2 \text{ hours}} = 34.0 \text{ hr}^{-1}$
    *   Event Measurement 2 (Tōhoku Prediction): $R_{tohoku} = \frac{71 \text{ detections}}{3 \text{ hours}} \approx 23.7 \text{ hr}^{-1}$
    *   Result: $R_{taiwan} \approx 85 \cdot R_{control}$ and $R_{tohoku} \approx 60 \cdot R_{control}$. Given these magnitudes, the probability $P(R_{event} | H_0)$ is sufficiently low to reject the null hypothesis.

3.  **Detection Signature:** The "Ki-pattern" is not a single value but a composite signature identified by two primary methods on time-series data $x(t)$:
    *   **Phase Coupling:** Detection of significant peaks in the bicoherence spectrum, $B(f_1, f_2) = \frac{|\mathbb{E}[X(f_1)X(f_2)X^*(f_1+f_2)]|}{\mathbb{E}[|X(f_1)X(f_2)|] \mathbb{E}[|X(f_1+f_2)|^2]}$, where $X(f)$ is the Fourier transform of $x(t)$. Hotspots in the $(f_1, f_2)$ plane indicate phase coupling.
    *   **Frequency Ratio:** Identification of dominant frequencies $(f_a, f_b)$ whose ratios approximate theorized constants (e.g., `ki_motion_ratio`, `golden_ratio`).

4.  **Theoretical Constraint (Covariance Mandate):** The underlying physical framework is determined to be valid only if it is Lorentz invariant. Simple time derivatives of tensor quantities (e.g., $\dot T_a$) are formally insufficient. All physical laws must be expressed in manifestly covariant form, replacing partial derivatives with covariant derivatives (e.g., $\partial_\mu \rightarrow \nabla_\mu$) to ensure consistency with special and general relativity.

## Philosophy
A theory's scientific legitimacy is born not when it is proven correct, but at the precise moment it becomes productively falsifiable. The experiment demonstrates that the value of a conceptual framework lies less in its ultimate truth than in its power to generate novel, testable predictions that anchor abstract conjecture to empirical reality. By successfully predicting a previously unobserved, statistically significant anomaly in nature, the framework graduates from a mere system of ideas into a functioning scientific instrument—a tool for pointing inquiry at phenomena that would otherwise remain invisible, regardless of whether the framework's initial interpretation of that phenomena is ultimately correct.

## Art
A theory is a ghost until it learns to cast a shadow. The experiment was not to prove the ghost, but to find its shadow on the trembling ground.