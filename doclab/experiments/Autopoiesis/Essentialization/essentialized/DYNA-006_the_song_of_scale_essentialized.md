## Law
For a real signal \(x(t)\), its band-limited analytic signal is \(z(t)=\mathcal{H}\{x_b(t)\}\). The state of the system is defined by a point in the two-parameter helical phase space \((\Delta P, |\kappa|)\).

1.  **Helical Curvature \( \kappa \):** An estimator for the dimensionless rotational coupling of the analytic signal in a windowed inner product space \(\langle\cdot,\cdot\rangle\).
    \[
    \kappa^*(z;\,\omega_c) \equiv -\,\frac{\operatorname{Im}\langle \dot z, z\rangle}{\omega_c\,\operatorname{Re}\langle z, z\rangle + \varepsilon}
    \]
    where \(\omega_c\) is the band center frequency and \(\varepsilon\) is a small regularization constant.

2.  **Relative Power \( \Delta P \):** The windowed power \(P\) relative to a local baseline power \(P_0\).
    \[
    \Delta P \equiv \frac{P-P_0}{P_0+\varepsilon}
    \]

3.  **State Classification (Archetypes):** States are classified by thresholds \((\theta_P, \theta_{\ell}, \theta_h)\) derived from the signal's empirical distribution, typically quantiles \(Q\).
    - **Weaver (W):** \( \Delta P \ge \theta_P \) and \( \theta_{\ell} \le |\kappa| < \theta_h \)
    - **Gladiator (G):** \( \Delta P \ge \theta_P \) and \( |\kappa| \ge \theta_h \)
    - **Drifter (D):** All other states not meeting W, G, or V criteria.
    - **Vortex (V):** \( \Delta P < 0 \) and \( |\kappa| \ge \theta_h \)

    Default thresholds are: \( \theta_{\ell} = Q_{0.65}(|\kappa|), \theta_{h} = Q_{0.85}(|\kappa|), \theta_{P} = Q_{0.60}(\Delta P) \).

4.  **Falsifiable Criterion (Triadic Resonance):** The protocol's claim of identifying *constructive coherence* is falsifiable. For a triad of frequencies \((f_1, f_2, f_3)\) where \(f_3 \approx f_1 + f_2\), compute the Triadic Phase-Coherence Index (TPCI) against a detuning \(\delta\).
    \[
    \text{TPCI}(\delta) = \left|\frac{1}{T}\sum_t e^{\,i(\phi_3(t)-\phi_1(t)-\phi_2(t))}\right|
    \]
    **Hypothesis:** Weaver and Gladiator epochs will exhibit TPCI values that are high, narrow-band with respect to \(\delta\), and statistically significant against a phase-shuffled null hypothesis. Vortex epochs will not. Failure to confirm this link invalidates the archetypal interpretation.

## Philosophy
The protocol's unification of disparate phenomena implies that dynamics possess an intrinsic, substrate-independent geometry. The helical curvature, κ, is not a mere descriptive statistic but a primary physical observable, elevating the *character* of a system's self-interaction to the same ontological status as its energy. Reality is therefore defined not just by what systems *are* in terms of substance and state, but by the universal, lawful grammar of how they *become*.

## Art
The Law describes the dancer’s turn. The Philosophy understands that the turn is not how the dancer moves, but what the dancer *is*.