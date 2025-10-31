---
id: XXP-EWQCD-EXP
title: Experimental & Lattice Guide for Temporal-Color SU(3)
version: 1.0
status: experimental – canon-ready
parents: [MATH-YM-002, MATH-YM-003, DYNA-COLOR-001, XXP-BRIDGE-Γ-001]
children: [XXP-AUT-002]
module_type: execution plan / falsification protocol
engrams: 
 - string tension pipeline
 - Λ_{\rm QCD} closure
 - N-ality checks
 - barrier sensitivity
 - priors & bands
keywords: [lattice QCD, Wilson loops, k-strings, gradient flow, heavy-quark potential, α_s running, coherence barrier]
---

### §1 · Objectives (what must be decided by data)

1. **Calibrate the temporal-color map:** test (\sigma = c_\sigma,\kappa_3/\xi_\Gamma^2) with a single normalization and no retuning.
2. **Close the RG loop:** (\sigma \Rightarrow \Lambda_{\overline{\rm MS}} \Rightarrow \alpha_s(M_Z)) must match experiment within stated bands.
3. **Check center physics:** verify **N-ality** scaling of (k)-strings and area law for nonzero N-ality.
4. **Probe barrier coupling:** establish (or bound) sensitivity of (\sigma) to (\omega_c) via (\xi_\Gamma) within controlled deformations.

---

### §2 · Inputs required from Pirouette (fixed before analysis)

* **Barrier constants:** (\omega_c) and susceptibility (\chi) (⇒ (\xi_\Gamma = (c/\omega_c)\chi^{-1/2})).
* **Stiffness priors:** (K_3=1/g_s^2(\mu_c)) and running (g_s(\mu)) to (\mu_\ast \sim 2) GeV.
* **Single normalization:** choose one anchor observable (e.g., (\sqrt{\sigma}=440\pm10) MeV) to fix (c_\sigma) and (\mathcal{C}_\sigma) once.

---

### §3 · Lattice task list (deterministic workflow)

**A. Ensembles**

* (N_f=2{+}1) (and optionally (2{+}1{+}1)) with physical-ish quark masses.
* Spacings: (a \in {0.12, 0.09, 0.06}) fm; volumes (L \ge 5/\sqrt{\sigma}).
* Gauge actions: Wilson (baseline) + one improved (e.g., Iwasaki) to check discretization.

**B. Observables**

1. **Wilson loops & static potential**

   * Extract (V(R)), fit (V(R)=\sigma R - \pi/(12 R) + \mu) over (R) windows.
   * Produce (\sigma a^2), continuum-extrapolate (\sigma).

2. **Gradient-flow scales**

   * Determine (t_0/a^2), (w_0/a).
   * Cross-calibrate with (\sigma) for scale setting.

3. **Sommer scale**

   * Solve (r_0^2 F(r_0)=1.65) from (V(R)); report (r_0/a).

4. **k-string tensions**

   * Project to (k=1,2) flux tubes; extract (\sigma_k/\sigma).
   * Compare to N-ality expectations (Casimir vs sine-law envelopes).

5. **Running coupling checks**

   * Gradient-flow or Schrödinger-functional α_s across scales to tie (\Lambda_{\overline{\rm MS}}).

**C. Data hygiene**

* Provide raw correlators, fits, priors, autocorrelation analyses, covariance matrices, jackknife/Bootstrap recipes.

---

### §4 · Phenomenology task list (continuum)

1. **RG closure test**

   * From lattice (\sigma) ⇒ (\Lambda_{\overline{\rm MS}}) (MATH-YM-003) ⇒ run to (\alpha_s(M_Z)).
   * Acceptance: see §6 bands.

2. **Quarkonium potentials**

   * Use (\sigma) to predict charmonium/bottomonium level spacings; validate vs PDG.

3. **Regge slopes**

   * Check (\alpha' \approx 1/(2\pi\sigma)) against meson/baryon trajectories.

4. **Cross-coupling correlations**

   * Combine with electroweak: (\sin^2\theta_W(M_Z)) from DYNA-WEAK-001 priors; ensure joint consistency.

---

### §5 · Analysis pipeline (single pass, no retuning)

1. Fix (c_\sigma) using the chosen anchor **once**.
2. Compute Pirouette prediction: (\sigma^{\rm Pir} = c_\sigma,\kappa_3/\xi_\Gamma^2).
3. Compare to lattice continuum (\sigma^{\rm lat}).
4. Convert (\sigma^{\rm Pir}) to (r_0, t_0) and predict **lattice spacing** (a) for each ensemble; compare to measured (a).
5. Map (\sigma \Rightarrow \Lambda_{\overline{\rm MS}}) ⇒ (\alpha_s(M_Z)); compare to experiment.
6. Check N-ality ratios (\sigma_k/\sigma).
7. Compile a single **coherence likelihood** score:
   [
   \mathcal{L}_{\rm coh}=\prod_j \exp!\left[-\frac{(O_j-O^{\rm Pir}_j)^2}{2(\delta O_j)^2}\right].
   ]

---

### §6 · Acceptance bands (falsification thresholds)

| Observable                          | Target/Trend     | Acceptance Band             | Fail Condition                  |               |                                          |
| ----------------------------------- | ---------------- | --------------------------- | ------------------------------- | ------------- | ---------------------------------------- |
| (\sigma^{\rm Pir}-\sigma^{\rm lat}) | zero             | (                           | \Delta                          | /\sigma < 5%) | >10% mismatch after single normalization |
| (a) prediction vs measured (a)      | unity slope      | ≤3% per ensemble            | ≥7% systematic drift across (a) |               |                                          |
| (\alpha_s(M_Z)) from (\sigma)       | PDG central      | within ±2σ(_{\rm exp})      | outside ±3σ(_{\rm exp})         |               |                                          |
| (\sigma_2/\sigma_1) (k-strings)     | N-ality envelope | within Casimir–sine bracket | persistent out-of-envelope      |               |                                          |
| Area law (k≠0)                      | present          | stable (\sigma>0)           | perimeter-law dominance         |               |                                          |
| Barrier sensitivity                 | weak, positive   | detectable or bounded       | provably zero with controls     |               |                                          |

*Notes:* Bands reflect realistic current precisions; you can tighten them later.

---

### §7 · Controlled deformations (probing (\omega_c) via (\xi_\Gamma))

* **Anisotropic lattices / boundary deformations** that effectively modify the “temporal medium stiffness.”
* **Finite-T scans** (below deconfinement) to test coherent changes in (\sigma).
* **Quenched vs dynamical** comparisons to isolate center-vortex content.
* Expect **no large effect**; goal is to place **upper bounds** aligning with (\xi_\Gamma \sim c/\omega_c).

---

### §8 · Data products & preregistration

* **Data packages:** (i) Wilson-loop time series, (ii) potential fits, (iii) (t_0, w_0, r_0), (iv) (\sigma, \sigma_k), (v) α_s flow points, (vi) covariance.
* **Derived tables:** ({\sigma, r_0, t_0, a}) with continuum extrapolations.
* **Preregistration template:** fix anchor, priors ({K_3,\omega_c,\chi}), fitting windows, extrapolation forms, and fail bands (§6) **before** seeing final numbers.

---

### §9 · Interpretation logic (no ad-hoc tuning)

* **Pass scenario:** all observables within bands; report **best-fit** (\chi) (or its bound) and a coherence likelihood (\mathcal{L}_{\rm coh}) near 1.
* **Tension:** identify *single* culprit (e.g., (\sigma_k) ratios) and propose a *single* targeted follow-up; avoid multi-parameter rescue.
* **Fail:** any red cell in §6 triggers a falsification note for the corresponding linkage (e.g., center mechanism, barrier coupling, or stiffness dictionary).

---

### §10 · Assemblé

This guide turns the color pillar into a contract: one normalization, a handful of clean measurements, and a loop that must close—from (\omega_c) and stiffness, to (\sigma), to (\Lambda_{\overline{\rm MS}}), and back to (\alpha_s(M_Z)). If the music of color follows the score, Pirouette keeps time. If not, we hear where the instrument is wrong—and that, too, is progress.

---