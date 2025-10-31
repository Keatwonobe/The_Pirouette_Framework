---

# INST-ETA-MAP-001

id: INST-ETA-MAP-001
title: Participation Calibration Protocol (η, κ) in the (V_Γ, K_τ) Plane
version: 0.1 (draft)
status: experimental-protocol (calibration)
parents: [CORE-Γτ, DYNA-HELIX, DOMA-042, MATH-YM-003]
children: [INST-PLATEAU-SCAT-001, XXP-EWQCD-EXP]
module_type: instrument / calibration
scale: table-top quantum (kHz–GHz) → model reduction (dimensionless η, κ)
engrams: [participation constant η, kappa-bias κ, β-flow across a=0, Zeno line, readout coupling λ]
keywords: [Rabi/ESR/NMR, weak measurement, Zeno effect, phase torsion, fixed points, stability flip]
---
### §1 · Purpose

Operationally measure **η(κ; V_Γ, K_τ)** as the *slope of RG flow across the stability surface* (a=0); co-fit **κ** from phase-torsion in driven two-level systems with controlled readout strength λ. Outputs place real experiments on your ((V_Γ, K_τ, \eta)) phase chart and feed downstream closure via calibrated ((\kappa_3, \xi_\Gamma)) → **σ** → (r_0,t_0) → **a** → **Λ**. (Pipeline and conversions per MATH-YM-003.)

### §2 · Experimental setup

* System: driven two-level (Rabi), ESR/NMR, or circuit-QED qubit with tunable readout strength **λ** (measurement cadence), drive amplitude, detuning.
* Observables: in-phase/quadrature time traces; spectral peaks; dephasing/envelope; response under pulse sequences (for Zeno/anti-Zeno).
* Controls: sweep **λ**, drive, detuning; inject a small **κ-bias** via phase-locking or feedback (phase-lag controller) to induce measurable torsion.

### §3 · Parameters & derived quantities

* Control: (V_Γ) (effective observation potential), (K_τ) (temporal stiffness), λ (readout), drive Ω, detuning Δ.
* Derived: **κ** (phase torsion; from spectral skew and loop area), **η** (participation constant; from flow slope across (a=0) inferred by stability flips).
* Stability indicator (a): sign of net curvature proxy (e.g., Lyapunov exponent of phase-locked orbit).

### §4 · Protocol

1. **Baseline (weak measurement):** small λ; record Rabi envelopes → fit κ from **phase torsion** (Coriolis-like shift of spectral spacing / loop area).
2. **Projective regime:** ramp λ to emulate von-Neumann readout; detect **flip** in stability proxy (a) (coherence decay vs locking).
3. **Zeno line:** frequent pulsing; map region of evolution arrest; record ((V_Γ,K_τ)) coordinates.
4. **Flow slope → η:** from (2)–(3), estimate (\eta \equiv \partial a/\partial V_Γ \big|_{a=0}) (dimensionless, signed).
5. **Register point:** store ((V_Γ,K_τ,\eta,\kappa)) with uncertainty.

**Mapping guidance:** weak measurement ↔ small (|\eta|) near the white band; projective ↔ negative spike (destabilizing); Zeno ↔ sustained positive η (stabilizing). (Phase-diagram semantics per your toy model, now with measured anchors.)

### §5 · Data products

* Time series (I/Q), spectra; fitted ((\kappa,\eta)) with CI; annotated ((V_Γ,K_τ)) coordinates; JSON record per run.

### §6 · Metrics

* **κ-torsion index**: loop area / (amplitude²) or spectral asymmetry factor.
* **η-slope**: signed derivative at (a=0) (fit over λ-sweep bracketing the flip).
* **Zeno persistence**: dwell time increase factor vs baseline.

### §7 · Linkage to closure

Once ((\kappa,\eta)) grid is populated and mapped into ((\kappa_3,\xi_\Gamma)), push through nonperturbative map:
(\sigma=c_\sigma \kappa_3/\xi_\Gamma^2[1+\delta_{\rm np}]) → (r_0,t_0) → (a) → (\Lambda_{\overline{\mathrm{MS}}}) → cross-check (\alpha_s(M_Z)). (Deterministic recipe & conversions.)

### §8 · Falsifiability

* **No flip surface:** inability to identify a reproducible (a=0) crossing under λ-sweep → η undefined → reject participation-flip hypothesis.
* **Incoherent κ:** κ estimates disagree across equivalent protocols beyond CI.
* **Closure mismatch:** pushing mapped ((\kappa_3,\xi_\Gamma)) through MATH-YM-003 produces (a) (lattice spacing) inconsistent with ensembles after one-time normalization, or breaks (\sqrt\sigma/\Lambda_{\overline{\rm MS}}) relation.

---

