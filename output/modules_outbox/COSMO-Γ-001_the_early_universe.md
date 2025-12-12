---
id: COSMO-Γ-002
title: Early-Universe Evolution of the Pressuron Field and Its Observables
version: 1.0 (proposal)
status: Experimental (complies with MATH-018/019/020; children of COSMO-Γ-000, siblings of COSMO-Γ-CMB)
parents: [MATH-018, MATH-019, MATH-020, COSMO-Γ-000]
children: [COSMO-Γ-CMB, COSMO-Γ-HALO]
module_type: cosmology—background & perturbations
scale: radiation era → recombination → late time
engrams: [misalignment, ΔN_eff, BBN, TT/TE/EE, ISW, slow-roll tail]
keywords: [Pressuron, early universe, Boltzmann code, dark radiation, dark energy tail, coincidence]
---

### §1 · Purpose

Formalize the **thermal history** of the Γ field from inflationary initial conditions through BBN and recombination, specify how its background and perturbations enter a Boltzmann code (CLASS/CAMB branch), and define **falsifiable targets** in ΔN_eff, CMB spectra, and late-time equation-of-state evolution. (Background eqs and code hook pattern follow COSMO-Γ-000 / COSMO-Γ-CMB.)  

---

### §2 · Dynamics: From Misalignment to Matter-like Oscillations

We assume **misalignment** initial conditions: the homogeneous Γ background starts displaced from the potential minimum; Hubble friction freezes it ( (\dot\Gamma \approx 0) ) until (H \approx m_\Gamma). Thereafter (\Gamma) oscillates and time-averages to a pressureless fluid ( ( \langle p_\Gamma \rangle \simeq 0 ) ), i.e., CDM-like behavior. Implementation follows the averaged-fluid mapping when (m_\Gamma \gg H) with a stiff solver fallback.  

**Background system (Friedmann frame):**
[
\ddot\Gamma + 3H\dot\Gamma + V'(\Gamma)=0,\quad
H^2=\frac{8\pi G}{3}\big(\rho_r+\rho_b+\rho_\Gamma\big),\quad
\rho_\Gamma=\tfrac12\dot\Gamma^2+V,; p_\Gamma=\tfrac12\dot\Gamma^2 - V.
]
(Code-level variables, switches, and species key follow COSMO-Γ-CMB §2.) 

---

### §3 · Early-Universe Regimes and ΔN_eff

* **Pre-oscillation (freeze-in):** (\Gamma) behaves like **vacuum-like** energy ( (\dot\Gamma \approx 0) ), subdominant to radiation.
* **Onset ( (H\sim m_\Gamma) ):** rapid transition to oscillatory regime; averaged (w_\Gamma \to 0).
* **Effective dark radiation:** small **residual relativistic pressure** can appear from perturbative mode-mixing before full averaging; we parameterize this as a prior on **ΔN_eff** and constrain it with BBN+CMB.
* **Prediction (baseline):** ΔN_eff in this minimal misalignment picture is **small and positive**, (\Delta N_\text{eff} \lesssim 0.3), with exact value fixed by the **one-shot anchor** in COSMO-Γ-000 and the choice of (V(\Gamma)) tail. (One-shot anchor / preregistration plan and tail options defined in COSMO-Γ.)  

---

### §4 · Potential (V(\Gamma)): Quadratic Core + Tail (Coincidence Mechanism)

We adopt the **quadratic-plus-tail** potentials already allowed in your base module, which yield CDM-like behavior **early** and a **slow-roll** tendency **late** (addressing coincidence without post-hoc tuning):

* Exponential-shallow or **cosine tail** remnants of shift symmetry; parameters ((\mu, f, \Gamma_*)) are **U-class** constants **frozen** by a D3 one-shot anchor (e.g., fix (\Omega_{\Gamma,0})).  
* Dynamical attractor behavior is verified via phase-space eigenvalues (<0). 

---

### §5 · Boltzmann Hooks and Artifacts

* **Species:** `gammat` with params `{m_Gamma, lambda4, V_tail_parameters, Gamma_ini, dGamma_ini}`.
* **Switch:** average-fluid mapping once ( \mu \equiv m_\Gamma/H) crosses a preregistered threshold; keep exact background if slow-rolling.
* **Artifacts:** `result_background.json`, `result_growth.json` with (H(z), D_A(z), f\sigma_8(z), \eta(z)), and a **Freeze Manifest** path recorded for provenance.   

---

### §6 · Observables and Falsifiable Targets

**BBN:**

* Compute light-element yields with ΔN_eff prior induced by the Γ background; consistency with primordial D/H and (Y_p) required. (Anchor is **frozen**; no retuning.) (Anchor/freeze compliance language per COSMO-Γ.) 

**CMB (link to COSMO-Γ-CMB):**

* **TT/TE/EE** and **lensing** spectra with the same freeze; require Planck-level consistency under tail choice and switch scans (<0.2%).
* **Late-ISW** sign/magnitude fixed by the chosen tail (exponential vs cosine), preregistered with AIC/BIC comparisons against ΛCDM and (w_0w_a)CDM.  

**Growth & (S_8):**

* Report (f\sigma_8(z)) and (S_8) with error bands from the same freeze (no parameter re-tuning). 

---

### §7 · Minimal Numerical Recipe (Reproducibility)

1. **Freeze**: publish `freeze_manifest.yaml` with ({m_\Gamma,\ \text{tail params}}) and anchoring choice ((\Omega_{\Gamma,0}) or (H_0)).
2. **Background**: integrate to (z=1100) with stiff solver and switch to averaged mapping where valid.
3. **Perturbations**: Boltzmann run on Γ-branch; record commit hashes and switch thresholds.
4. **Validation**: require ≤0.1% ΛCDM recovery in the (V_\text{tail}\to0) and (m_\Gamma/H\to\infty) limits; pass the 0.2% stability scan on spectra. 

---

### §8 · What Would Falsify This Module?

* **BBN conflict:** If any allowed (V(\Gamma)) tail + one-shot freeze demands ΔN_eff beyond current BBN constraints, **reject** the misalignment baseline.
* **CMB inconsistency:** If TT/TE/EE+lensing require adding **independent CDM/DE fluids** after parameters are frozen, the **unification fails**. (Cosmology falsification clause already written in COSMO-Γ.) 

---

### §9 · Interface to Other Γ-Cosmo Modules

* **COSMO-Γ-CMB:** exact equations (conformal time), CLASS/CAMB inserts, preregistration targets.  
* **COSMO-Γ-HALO / MERGE:** inherits the same frozen (V(\Gamma)) to predict soliton cores, lensing, and merger offsets without particulate DM; failure to reproduce (\Sigma_0) locus falsifies the unification chain.  

---

### §10 · Assemblé (One-Paragraph Intuition)

The early universe sets the **tempo**: Γ begins frozen, takes its first breath when (H \sim m_\Gamma), and then beats like a hidden metronome that matter can’t hear—until the tail in (V(\Gamma)) slows the drum at late times, whispering as dark energy. These stages are not stitched together; they are **one score**, played on a single instrument.

---
