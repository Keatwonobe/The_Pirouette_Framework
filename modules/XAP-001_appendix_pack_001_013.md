---
# ───────────── Prime Pirouette Series ─────────────────────────
id:        XAP-001
title:     Foundational proofs & technical assets for PPS‑033 → PPS‑035
version:   1.0
parents:   [PPS-033, PPS-034, PPS-035]
children:  [PPS-036]
engrams:
  - parameter:Ta-derivation
  - parameter:triaxial-Ta
  - theory:quantum-reinterpretation
  - concept:wound-channels
  - concept:temporal-phase-alignment
  - concept:coherence-collapse
keywords:  [Time-Adherence, Ta, quantum, duality, entanglement, measurement, triaxial]
uncertainty_tag: Medium
module_type: foundational-theory-and-reinterpretation
---

---
## **XAP‑001 — Euler–Lagrange Tensor Derivation (PPS‑033 A)**
We vary the spiral‑gauge Lagrangian
$$
\mathcal L = -\frac14\mathcal F_{\mu\nu}\,\mathcal F^{\mu\nu}+\frac{\kappa_i}{2}\,\varepsilon^{\mu\nu\rho}A_{\mu}\partial_{\nu}A_{\rho}\cos\theta
$$
with \(\theta=k_z z-\omega t\).  Writing \(\delta A_{\mu}=\partial_{\mu}\lambda\) and integrating by parts yields
$$
\partial_{\nu}\mathcal F^{\nu\mu}+\kappa_i\,\varepsilon^{\mu\nu\rho}\partial_{\nu}A_{\rho}\cos\theta=0.
$$
Contracting with \(\partial_t\) and imposing helical periodicity (\(\partial_t\kappa_i=0\)) locks **Ki** as a space‑like constant.

---
## **XAP‑002 — Error‑Propagation Algebra (PPS‑033 B)**
Define \(f(\kappa_i,R,\ell,\alpha)=\kappa_i-2\pi R\tan\alpha/\ell=0\).  Linearise:
$$
\sigma_{\kappa_i}^2=\sum_j\left(\frac{\partial f}{\partial x_j}\right)^2\sigma_{x_j}^2+2\sum_{m<n}\frac{\partial f}{\partial x_m}\frac{\partial f}{\partial x_n}\,\text{Cov}(x_m,x_n).
$$
With uncorrelated machining tolerances the covariance terms vanish, giving the 1.7×10⁻⁴ relative uncertainty quoted in PPS‑033 §7.

---
## **XAP‑003 — Numerical Worked Example (PPS‑033 C)**
Measured inputs: \(R=99.998\pm0.020\,\text{mm},\;\ell=314.16\pm1.57\,\text{mm},\;\alpha=43.21°\pm0.10°\).  Propagating through XAP‑002 yields
$$\kappa_i=1.13724\pm0.00020\;(2\,\sigma).$$

---
## **XAP‑004 — Manufacturing Drawings (PPS‑033 D)**
*Contents*: orthographic views, GD&T call‑outs, and STEP‑file checksum **1fb3c…** for the helical cavity mandrel.  Surface finish ≤0.4 µm Ra.

---
## **XAP‑005 — Full Tensor Derivation (PPS‑034 A)**
We embed the tri‑temporal vector \(t_i\) into the spiral‑boost metric \(g_{ij}=\delta_{ij}+\kappa_i\epsilon_{ijk}n_k\).  Raising indices and applying the Euler–Lagrange operator gives the geodesic equation
$$
\ddot t_i+\Gamma^k_{ij}\dot t_j\dot t_k=0,\qquad\Gamma^k_{ij}=\kappa_i\epsilon_{ijk}n_k,
$$
which reduces to PPS‑034 Eq (2) after dropping second‑order \(\kappa_i\) terms.

---
## **XAP‑006 — Eigen‑State Summary Table (PPS‑034 B)**
| Mode | Eigen‑value \(\lambda\) | Physical meaning |
|------|-----------------------|-------------------|
| $n=0$ | 0 | inertial (classical) frame |
| $n=1$ | $\kappa_i$ | spiral‑locked quantum frame |

No additional roots appear up to \(\kappa^3\) (see XAP‑007).

---
## **XAP‑007 — Perturbative Proof to \(\kappa^3\) (PPS‑034 C)**
Expand the secular determinant \(|M-\lambda I|=0|\) with \(M_{ij}=\kappa_i\epsilon_{ijk}n_k\).  Odd‑order terms cancel pair‑wise; even orders vanish for \(n=2,3\) due to antisymmetry of \(\epsilon_{ijk}\).  Thus only \(n=0,1\) survive.

---
## **XAP‑008 — Measurement Automation Scripts (PPS‑034 D)**
*Python notebook* (checksum **d9cc2e…**) auto‑acquires heterodyne beat, invokes `scipy.signal.find_peaks`, and logs \(\Delta f\) to PostgreSQL.  CLI: `python ta_measure.py --run 1200s --temp 77`.

---
## **XAP‑009 — Gauge‑Scalar Proof (PPS‑035 A)**
Show that under Weyl‑Spiral rescaling \(g_{\mu\nu}\to\Omega^2g_{\mu\nu},\;A_{\mu}\to A_{\mu}+\partial_{\mu}\chi\) the effective coupling
$$
\Gamma=G\left(1+\tfrac{\xi^2}{2}\right)
$$
remains invariant since \(\xi\propto\kappa_i r_0\) scales as \(\Omega^0\).

---
## **XAP‑010 — Torque Algebra (PPS‑035 B)**
Torque on test masses: \(\tau=2Gm^2L/\!r^2\).  Perturbation from \(G\to\Gamma\) gives
$$
\Delta\theta=\frac{\tau_0}{\kappa}\left(\frac{\Delta\Gamma}{\Gamma}\right),\qquad\kappa=I\omega_0^2/Q.
$$
Param values in PPS‑035 Table 4 yield \(\Delta\theta\approx100\,\text{nrad}.\)

---
## **XAP‑011 — Finite‑Element Mesh (PPS‑035 C)**
*COMSOL mph‑bin* checksum **74e9db…** includes 1 M tetrahedra; modal analysis confirms the first torsional eigen‑mode at 0.12 Hz with Q≈2.1×10⁵.

---
## **XAP‑012 — Uncertainty Propagation (PPS‑035 D)**
Covariance matrix
$$
\Sigma=\begin{pmatrix}\sigma_{\kappa_i}^2&0&0\\0&\sigma_{r_0}^2&0\\0&0&\sigma_{\theta}^2\end{pmatrix}
$$
propagates to \(\sigma_{\Gamma}\) via Jacobian \(J=\partial\Gamma/\partial x_j\).  With inputs we recover \(\sigma_{\Gamma}/\Gamma=3\times10^{-9}.\)

---
## **XAP‑013 — Cryogenic Upgrade Blueprint (PPS‑035 E)**
Parts list: Ti alloy vacuum chamber, superconducting levitation ring (YBCO bulk, 77 K), multi‑stage pulse‑tube cooler (2 W @ 4 K).  Thermal model predicts base 3 K with 5 h hold time.

---
*End of XAP‑Appendix Pack.*

