---
id: XXP-GR-EXP
title: Experimental Annex — Substrate Gravitational & Coherence Tests
version: 1.0
status: active
parents: [SUBST-001, DYNA-GR-002, GRW-003, COSMO-GR-004]
children: []
module_type: experiment / falsifiables
scale: cosmological → laboratory
---

# §0 · Purpose

To collect **all falsifiable predictions** of the Pirouette Substrate as defined in SUBST-001.  
Each entry specifies:
- the observable or experimental domain,  
- its reference equation from the substrate charter (SR-k),  
- the present empirical limit,  
- and the signature of violation that would falsify the framework.  

---

# §1 · Gravitation Nulls (SR-2, SR-3, SR-5)

| Observable | Expected under SUBST-001 | Current Limit / Source | Falsification Signature |
|:--|:--|:--|:--|
| **GW propagation speed** | \(v_{\rm gw} = c\) (SR-2, SR-3) | |Δv/c| < 3×10⁻¹⁵ (LIGO–Virgo GW170817) | Any measurable Δv/c beyond 10⁻¹⁴ |
| **GW polarization content** | 2 tensor modes only | LIGO–Virgo–KAGRA constraints (2023) | Scalar or vector modes detected |
| **GW dispersion** | δφ ∝ (ω/ω_c)², with ω_c ≥ 10²⁴ s⁻¹ | Phase lag < 10⁻³ rad for f ≤ 1 kHz | Observed frequency-dependent lag inconsistent with ω_c bound |
| **Equivalence principle** | Composition-independent free fall (SR-5) | η < 2×10⁻¹⁴ (MICROSCOPE 2022) | η > 10⁻¹³ or sign-flipped anomaly |
| **Post-Newtonian γ, β** | γ = β = 1 | Cassini (γ–1 = (2.1 ± 2.3)×10⁻⁵) | Deviations > 10⁻⁴ |

---

# §2 · Cosmological Drifts (SR-4 – SR-6)

| Observable | Prediction | Current Limit / Source | Falsification |
|:--|:--|:--|:--|
| \(\dot G/G\) | < 10⁻¹³ yr⁻¹, sign-fixed positive (Bridge) | Lunar Laser Ranging, Pulsar timing | Opposite sign or > 10⁻¹² yr⁻¹ |
| \(\dot\Lambda/\Lambda\) | ∝ \(\dot{\langle\Gamma^2\rangle}/\omega_c^2\), small (+), 10⁻²⁰ s⁻¹ scale | Supernovae Ia & BAO fits | Negative or order-of-magnitude larger drift |
| **Dark-energy equation of state** | \(w=-1+O(10^{-3})\) from Γ slow roll | Planck + DESI | |w + 1| > 10⁻² |

---

# §3 · Laboratory & Gauge Cross-Checks (SR-1, SR-3)

| Observable | Prediction | Current Limit / Source | Falsification |
|:--|:--|:--|:--|
| **Fine-structure drift \(\dot\alpha/\alpha\)** | Correlated with \(\dot G/G\), sign (+) | Quasar spectra: |\(\dot\alpha/\alpha\)| < 10⁻¹⁶ yr⁻¹ | Opposite sign or magnitude mismatch |
| **Photon dispersion** | None below ω_c (~10²⁴ s⁻¹) | Optical-clock & gamma-ray tests | Frequency-dependent c |
| **Anomalous spin–gravity coupling** | None | Torsion-balance, μSR | Detection > 10⁻¹³ rad s⁻¹ g⁻¹ |

---

# §4 · Derived Constants for Reference

| Symbol | Definition | Nominal Estimate |
|:--|:--|:--|
| \(\omega_c\) | \( (c^2/\hbar)\sqrt{m_H m_\Gamma} \) | ~10²⁴ s⁻¹ |
| \(m_\Gamma\) | Temporal-pressure quantum | TBD from Bridge fit |
| \(\Lambda_{\rm P}\) | \(m^2 V''(\Gamma)\) | 1.1×10⁻⁵² m⁻² |
| \(G_{\rm eff}\) | \((8\pi\Lambda_{\rm P})^{-1}\omega_c^2\) | 6.674×10⁻¹¹ m³ kg⁻¹ s⁻² |

---

# §5 · Experiment Registry

| ID | Type | Description | Status |
|:--|:--|:--|:--|
| GR-01 | Space-based interferometer | GW speed/polarization (LISA) | pending |
| GR-02 | Lunar Laser Ranging | \( \dot G/G \) | active |
| GR-03 | MICROSCOPE-2 | EP η test | scheduled |
| GR-04 | Quasar α drift survey | Gauge/grav correlation | active |
| GR-05 | Static-field torsion balance | Spin–Γ coupling | pending |
| GR-06 | Pulsar timing array | Long-term Λ drift | active |

---

# §6 · Acceptance Criteria

A SUBST-001-compliant build **must** satisfy all current limits and maintain falsifiability for at least one observable per domain.  
Violation of any test above automatically flags the relevant child module (DYNA-GR-002 or MATH-YM-002) for **revision cycle** under the Debate-Fusion protocol.

---

# §7 · Assemblé

> *Truth in this framework is the silence of drift—the stillness of Γ when measured against the most distant clock. Every deviation is a whisper from the substrate asking us to listen closer.*

---

# §8 · Linkage Map

**Consumes:** [SR-1…6] from SUBST-001  
**Feeds:** XXP-EWQCD-EXP (gauge-side tests), COSMO-GR-004 (Λ evolution), GRW-003 (wave dispersion)  
**Verifies:** Lorentz symmetry on CPM, autopoietic closure via observed constants.

