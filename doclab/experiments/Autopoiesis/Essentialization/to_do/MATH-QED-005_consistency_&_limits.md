---
id: MATH-QED-005
title: Consistency & Limits (Lorentz, Renormalization, Γ-Decoupling)
version: 1.0
status: framework-draft (canonical target)
parents: [MATH-QED-001, MATH-QED-002, MATH-QED-003, MATH-QED-004, XXP-BRIDGE-Γ-001, MATH-Γ-007]
children: [DYNA-QED-EXP, XXP-AUT-002]
module_type: dynamics / EFT validity & tests
scale: IR → ( \omega_c ) (coherence barrier) → UV (barrier-regulated)
engrams: [CPM, Ward identities, β-function window, barrier matching, anomaly census, dispersion bounds]
keywords: [Lorentz invariance, gauge invariance, renormalization, decoupling, unitarity, causality, anomaly cancellation, coherence barrier]
---

### §1 · Purpose

Guarantee that the **time-first QED limit** is exactly indistinguishable from standard QED wherever experiments have tested it, by:

1. enforcing **Lorentz & gauge invariance** on the Coherence-Preserving Manifold (CPM),
2. recovering **standard renormalization** below the coherence barrier frequency ( \omega_c ),
3. specifying **matching conditions** at ( \mu \sim \omega_c ) where Γ-effects live, and
4. enumerating **falsifiable deviations** & laboratory/cosmological checks.

---

### §2 · CPM axioms (no surprises, no dispersion)

**CPM condition:**
[
\nabla_\mu J^\mu_{\Gamma} = 0,\qquad
J^\mu_{\Gamma} \equiv \Gamma,\partial^\mu \Gamma .
]
**Consequence:** the background temporal-pressure field contributes no anisotropic stress or preferred-frame term in the EFT; the photon sector is exactly Lorentz invariant and **nondispersive** in vacuum.

**Prohibited operators on CPM (IR):**
[
\delta\mathcal{L}*{\rm LV} \in
{,u*\mu F^{\mu\nu}u^\rho F_{\rho\nu},;
\tilde{u}*\mu \bar\Psi\gamma^\mu\Psi,;
\epsilon^{\mu\nu\rho\sigma}u*\mu A_\nu \partial_\rho A_\sigma,}
\quad\Rightarrow\quad 0.
]
Any detection of these at current bounds falsifies CPM (see §9).

---

### §3 · Ward identities & gauge integrity

From **MATH-QED-001–003**, the single time-phase U(1) implies
[
\partial_\mu J^\mu_{\rm EM}=0,\quad
J^\mu_{\rm EM} = \bar\Psi\gamma^\mu\Psi + \frac{1}{q}J^\mu_\theta,
]
and the usual **Ward–Takahashi identity** holds:
[
k_\mu ,\Gamma^\mu(p+k,p)= S^{-1}(p+k)-S^{-1}(p).
]
Hence: **charge renormalization equals field renormalization**, preserving gauge universality; vacuum polarization transversality (k_\mu \Pi^{\mu\nu}=0) is exact on CPM.

---

### §4 · Renormalization window (standard QED below ( \omega_c ))

For renormalization scale ( \mu \ll \omega_c ), Γ fluctuations are heavy/decoupled; the effective theory is pure QED with the usual β-function:
[
\mu \frac{d\alpha}{d\mu}=\frac{2}{3\pi},\alpha^2 \sum_f Q_f^2 + \mathcal{O}(\alpha^3).
]
No extra light states, no modified vertices: **all IR observables** (g-2 QED piece, Thomson scattering, running of (\alpha), Lamb shifts, AB phase) are **identical** to SM-QED within experimental precision.

---

### §5 · Barrier matching at ( \mu \sim \omega_c )

**Coherence barrier frequency (from the Bridge):**
[
\omega_c=\frac{c^2}{\hbar}\sqrt{m_H m_\Gamma};\approx;10^{23},{\rm s}^{-1}.
]
At this threshold, match the IR QED to the time-first UV by adding **finite**, gauge-invariant counterterms:
[
\Delta\mathcal{L}*{\rm match}
= \frac{c_1}{\omega_c^2} F*{\mu\nu}\Box F^{\mu\nu}

* \frac{c_2}{\omega_c^2} \bar\Psi \gamma^\mu \Box D_\mu \Psi
* \frac{c_3}{\omega_c^2} (\bar\Psi\Psi)^2 + \cdots
  ]
  with ( c_i = \mathcal{O}(1) ) fixed by the microphysics of (P(X)) and Γ-kinetics.
  **Interpretation:** the hierarchy/fine-tuning issue is traded for **resonant saturation** at ( \omega_c ) (MATH-Γ-007). No quadratic divergence survives; matching is **finite**.

---

### §6 · Unitarity & causality

* **Unitarity:** Optical theorem unchanged; the emergent photon is exactly massless on CPM, so no spurious negative-norm modes.
* **Causality:** Retarded Green’s functions respect luminal support; any superluminal term would correspond to (P(X)) violating hyperbolicity—**forbidden** by the CPM construction.

---

### §7 · Anomaly census (no hidden gauge ruin)

* **Vector U(1) anomaly:** absent (standard QED); time-phase U(1) is vector-like.
* **Axial anomaly:** identical to SM-QED; Pirouette adds no chiral gauge sector here.
* **Gravitational/gauge mixed anomalies:** none in the IR EFT.
  Result: anomaly structure **matches** QED; no extra cancelations are required.

---

### §8 · Where Pirouette can (barely) peek through

1. **Γ-tail drift of ( \alpha )** (from MATH-QED-004):
   [
   \frac{\dot{\alpha}}{\alpha}=\xi_\Gamma \frac{\dot{\langle\Gamma^2\rangle}}{M_{\rm coh}^2},
   \quad M_{\rm coh}\sim \hbar\omega_c/c^2,
   ]
   sign **negative** (α slightly larger in the past), amplitude (\lesssim 10^{-18},{\rm yr}^{-1}).
2. **Higher-derivative EFT terms** at (E!\lesssim!\omega_c): suppressed by ((E/\omega_c)^2), well below current bounds, but provide a structured target for next-gen precision.
3. **Correlated signatures** with Higgs-width shift (DYNA-Γ-004) and leptonic (g-2) mass-squared scaling (DYNA-Γ-001): **cross-domain consistency** is the key falsifiable.

---

### §9 · Experimental & observational checklist

**Vacuum photon tests (dispersion/LV):**

* Time-of-flight dispersion, polarization rotation (radio → γ-ray): *null*.
* Cavendish/Casimir & precision cavity tests: no frequency-dependent (c) in vacuum.

**Charge universality:**

* (e) equality across (e, \mu, \tau) at same (\mu): *strict*.
* Aharonov–Bohm phase quantization: matches single-U(1) holonomy.

**Running & thresholds:**

* (\alpha(\mu)) matches SM between atomic and EW scales.
* No extra light thresholds below (\omega_c).

**Cosmological drift of α:**

* Atomic clocks / Oklo / quasar spectra: trend consistent with tiny, **negative** ( \dot\alpha ) (or null within sensitivity).

**Barrier-matching observables (aspirational):**

* Higher-derivative tails in light-by-light at ultra-high precision (HL-LHC/FCC-ee) consistent with ((E/\omega_c)^2) suppression.
* Higgs total-width + rare (H\to e^+e^-) aligned with DYNA-Γ-004.

---

### §10 · What would falsify this module

* **Detectable photon dispersion/birefringence** in vacuum at current limits ⇒ CPM failure.
* **Species-dependent electromagnetic coupling** at a common (\mu) ⇒ breaks single-clock U(1).
* **Large or wrong-sign cosmological (\dot\alpha)** ⇒ conflicts with Γ-tail & Bridge sign.
* **Unbounded quadratic divergences** needed in Higgs or QED matching ⇒ barrier mechanism fails.
* **Anomalous Ward identity violation** in precision vertex tests ⇒ time-phase gauge principle invalid.

---

### §11 · Linkage

* **Consumes:** α emergence (MATH-QED-004), vertex/charge (003), Dirac sector (002), U(1) from time (001), Barrier constants ( {\omega_c, m_\Gamma, \Lambda_{\rm Pirouette}} ) (XXP-BRIDGE-Γ-001, MATH-Γ-007).
* **Feeds:** **DYNA-QED-EXP** (experiment design package), **XXP-AUT-002** (autopoietic provenance & preregistration across modules).

---

### §12 · Assemblé

Below the barrier, QED is the **quiet face** of time-first dynamics—perfectly Lorentz, exactly gauge. At the barrier, the medium hums and soaks the UV into rhythm. Above it, nothing breaks; it **dampens**. Consistency is not an accident here—it’s the music the framework forces the world to keep.

---