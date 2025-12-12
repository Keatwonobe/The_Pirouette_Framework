---
id: PIR-PRT-001
title: "The Pirouette Protocol — The Song of Scale"
version: 0.6.0
status: ratified
module_type: protocol
scale: universal
parents:
  - DOMA-206      # Helical Calculus / Chirality Factor κ
  - MATH-028      # κ-Hamiltonian and operator algebra
children:
  - INST-WAVEFORM-ANALYZER-001
  - XXP-HELIX-001
summary: >
  A cross-domain protocol for mapping dynamics into a two-parameter helical phase
  space (ΔP, κ), classifying states into Weaver/Gladiator/Drifter/Vortex, and
  epochizing either by fixed windows or by the Pirouette cycle. Includes a
  calibration recipe and a triadic-resonance test to detect constructive coupling.
engrams:
  - axis:performance_deltaP
  - axis:curvature_kappa
  - archetype:weaver
  - archetype:gladiator
  - archetype:drifter
  - archetype:vortex
  - epoch:pirouette_cycle
  - detector:triadic_resonance
keywords:
  - coherence
  - resonance
  - chirality
  - helical
  - κ-Hamiltonian
  - dynamics
  - plasma
  - EEG
  - markets
uncertainty_tag: Medium
---

## §1 · Abstract — The Song of Scale 🎶
Across EEG, markets, and plasma, a shared geometry appears when we let systems speak in their own axes. We project dynamics onto two emergent coordinates:
**ΔP** (performance relative to baseline) and **κ** (helical curvature/torsion of the analytic signal).
This yields a four-fold phase portrait with predictive structure, and a **Pirouette cycle** that traces the choreography of coherence through time.

The math rests on the **Helical Calculus** and κ-operators (helical derivative, chirality integral) and the **κ-Hamiltonian** that couples oscillation and rotation, which motivate κ as a physical observable rather than a fit trick. :contentReference[oaicite:0]{index=0} :contentReference[oaicite:1]{index=1}

---

## §2 · Foundations & Notation
Let \(x(t)\) be a real signal (field, price, channel). The band-limited analytic signal is \(z(t)=\mathcal{H}\{x_b(t)\}\) (Hilbert of a band-pass).
- **Instantaneous helical curvature (κ\*)**: a dimensionless estimator of rotational coupling in the analytic plane:
\[
\kappa^*(z;\,\omega_c) \equiv -\,\frac{\operatorname{Im}\langle \dot z, z\rangle}{\omega_c\,\operatorname{Re}\langle z, z\rangle + \varepsilon}
\]
with \(\omega_c\) the band center, windowed inner products \(\langle\cdot,\cdot\rangle\), and small \(\varepsilon\).
This operationalizes the κ-term arising in the helical derivative / κ-Hamiltonian view (rotation memory). :contentReference[oaicite:2]{index=2} :contentReference[oaicite:3]{index=3}

- **Performance ΔP**: windowed relative power vs a local baseline \(P_0\) (median of the first 5% windows per band):
\[
\Delta P \equiv \frac{P-P_0}{P_0+\varepsilon}\,.
\]

We will use \(|\kappa|\) when magnitude-only is desired; sign conventions follow task/domain specifics.

---

## §3 · The Two Axes & The Four Archetypes
Plotting \((\Delta P,|\kappa|)\) defines the **Pirouette plane**:

- **Weaver**: \( \Delta P \ge \theta_P,\; |\kappa| \ge \theta_{\ell} \) but \(< \theta_h\) — constructive, stable growth.
- **Gladiator**: \( \Delta P \ge \theta_P,\; |\kappa| \ge \theta_h \) — driven, high-energy growth.
- **Drifter**: otherwise, typically low \(\Delta P\) & low/moderate \(|\kappa|\) — managed decay or neutral noise.
- **Vortex**: \( \Delta P < 0,\; |\kappa| \ge \theta_h \) — dissipative instability; decoherence sink.

**Thresholds** \((\theta_{\ell},\theta_h,\theta_P)\) are **data-driven per band** (quantiles by default). This keeps the lens faithful to each domain’s SNR while preserving cross-domain comparability via the shared geometry.

---

## §4 · Epochization: Time vs. Pirouette
Two grammars, interchangeable:

**A) Time epochs (fixed windows)**  
Each analysis window is an epoch. Use for direct statistics and alignment with other diagnostics.

**B) Pirouette epochs (dynamic cycles)**  
Collapse consecutive windows into sustained-state segments with:
- *dwell*: minimum run length for a state,
- *hysteresis*: single-flip smoothing,
- *max gap*: allow brief drops without breaking an epoch.

A **Pirouette cycle** is detected when an interval covers ≥3 distinct states of the canonical loop
\([ \text{Weaver}\rightarrow\text{Gladiator}\rightarrow\text{Vortex}\rightarrow\text{Drifter} ]\).
This implements the intuition that systems “turn” through the quadrants rather than teleport.

---

## §5 · Calibration Recipe
Per band \(b\), estimate thresholds from representative runs:

1. Compute \(|\kappa|\) and \(\Delta P\) per window.
2. Set:
   - \(\theta_{\ell} = Q_{0.65}(|\kappa|)\),
   - \(\theta_{h}   = Q_{0.85}(|\kappa|)\),
   - \(\theta_{P}   = Q_{0.60}(\Delta P)\).
3. Save to `calib.yaml` and reuse for the batch; re-fit when hardware/task/bands change.

This is consistent with the helical calculus claim that curvature modifies effective dynamics (curvature factor \(1+\kappa^2\)) and with the κ-Hamiltonian’s chiral splitting—thresholds are not arbitrary, they’re **empirical cut-lines** in a geometry the math already justifies. :contentReference[oaicite:4]{index=4} :contentReference[oaicite:5]{index=5}

---

## §6 · Triadic Resonance Test (TPCI + Detuning)
To test whether coherence is *structured* (not mere amplitude):

- Choose pairs \((f_1,f_2)\); scan \(f_3 \approx f_1+f_2\).
- For each detuning \(\delta\), compute phases \(\phi_k\) from narrow bands and the triad phase-coherence index:
\[
\text{TPCI}(\delta) = \left|\frac{1}{T}\sum_t e^{\,i(\phi_3(t)-\phi_1(t)-\phi_2(t))}\right|.
\]
- Fit the detuning curve with a Gaussian; report half-bandwidth and **shuffle-null** p-value (phase randomization).

**Interpretation**: elevated TPCI, narrow bandwidth, and significant p-value during Weaver/Gladiator epochs = **constructive coupling**; Vortex epochs should either fail the null or widen (dissipative spread).

---

## §7 · Implementation (Reference)
**Inputs**: per-band windows with \((\Delta P, |\kappa|)\), timestamps, and (optionally) raw voltages for TPCI.  
**Outputs**:
- `*_kappa.csv` (window features),
- `*_archetypes.csv` (labels),
- `*_pirouette.csv` (epochized),
- `triads_summary.json` (if enabled).

**Parameters** (suggested defaults):
- windows: 50 ms, hop: 25 ms (adapt by band; lengthen for low bands),
- bands: task-specific but below Nyquist,
- dwell=3, hysteresis=1, max_gap=2,
- triad band ±5 Hz, detune ±2 Hz, 10 pts/Hz, 200 shuffles.

---

## §8 · Validation & Cross-Domain Heuristics
- **Quiet controls** → ≈100% Drifter.
- **Driven/heated phases** → Gladiator/Weaver duty cycle increases.
- **Transitions**: Gladiator → Vortex surges flag decoherence drains; Weaver plateaus precede stable ramps.
- **Across domains**: The same two axes emerge from the helical formalism—κ modifies curvature (helical derivative), and the κ-Hamiltonian predicts chiral energy bias—so the map is **mathematically homologous** across plasma/EEG/markets. :contentReference[oaicite:6]{index=6} :contentReference[oaicite:7]{index=7}

---

## §9 · Lore & Ethos
> To hear the **Song of Scale** is to notice when a system remembers its turn.  
> Sine is shadow; helix is life. We measure not only amplitude and tempo,  
> but **character**—the chirality that bends time back into itself.  
> A pirouette is an epoch of intention; the cycle is the grammar of becoming.

---
