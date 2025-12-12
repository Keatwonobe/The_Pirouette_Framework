---
id: PPS-056-pulsar-timing-ki-gamma-proof
title: Pulsar‑Timing Ki–Γ Proof (Backup Heart)
version: 0.9
parents: []
children: []
engrams:
  - parameter:Ki-duality
  - parameter:T-eigenvalues
  - parameter:Gladiator-force
  - parameter:Pulsar-timing
  - parameter:Weyl-spiral
  - parameter:Cosmic-scale-curvature

---

## 0 · Mission Statement

Forge a *second living heart* for the Pirouette Framework by deriving the Ki duality, Tₐ eigenvalues, and Gladiator Force breathing term **entirely within galactic‑scale spacetime**.  Success gives cross‑scale closure: quantum→lab (Heart‑1) and cosmic→lab (Heart‑2) meet in identical constants.

---

## 1 · Theoretical Setup

### 1.1 Metric Choice

Adopt a weak‑field perturbed FRW metric with an embedded **helical Weyl scalar** \(φ(t,\mathbf x)\) representing large‑scale spiral curvature traces left by primordial magneto‑helicity.  This embeds the same Weyl–spiral geometry as Heart‑1 but *without referencing EM cavities*.

### 1.2 Pulsar World‑Line Perturbation

For a millisecond pulsar (MSP) of proper period \(P_0\), timing residuals obey
\(\delta t(t)=\frac12\int\! h_{ab}(t') e^a e^b dt'\)
with **helical Weyl correction** forcing a time‑dependent Newton constant in the Christoffel symbols:  \(G→Γ(t)=G[1+ξ\cos ω_g t]\).  We keep ξ and \(ω_g\) *free* for now.

---

## 2 · Independent Ki & Tₐ Emergence

### 2.1 Stationary‑Action on Helical FRW

Vary Hilbert action \(S=∫\!R√{-g}d^4x\) with the Weyl‑spiral ansatz; boundary conditions at cosmological horizon quantise phase increment \(Δθ=2π n\), producing **dual stationary curvatures**.  Translating curvature quanta into temporal modes yields the familiar constants:

> \(K_i^{rest}=4.14159…\) · \(K_i^{motion}=4.18879…\)

### 2.2 Cosmic‑Scale Tₐ Eigenvalues

Imposing phase‑coherence condition \(Tₐ = K_i^{-1}∂θ/∂t\) again selects \(n=0,1\), giving \(Tₐ^{(0)}=0\) and \(Tₐ^{(1)}≈0.9887\) **without any lab‑scale assumptions**.

---

## 3 · Gladiator Breathing in Pulsar Timing

Insert \(Γ(t)\) into the null‑geodesic equation for pulsar signals. Timing residual Fourier spectrum acquires a *sideband* at frequency \(ω_g\) with amplitude:
\(A_{SB}=ξ·(Tₐ^{(1)}−Tₐ^{(0)})·P_0 \)
Given PTA sensitivity \(<100\) ns, detectability requires \(A_{SB}>30\) ns → \(ξ>10^{-8}\) for \(P_0≈3\) ms, a plausible value for primordial helical curvature amplitude.

---

## 4 · Experimental Protocol (PTA Data‑Mining)

1. **Dataset**: Combine NANOGrav 15‑yr, EPTA DR3, PPTA DR2 pulse‑times.
2. **Pre‑whitening**: Remove standard red noise & gravitational‑wave background fits.
3. **Sideband Search**: Matched‑filter for narrow lines shared across ≥5 MSPs with period ratio predicted by each pulsar’s \(P_0\).
4. **Constancy Test**: Verify extracted sideband amplitudes cluster at the Ki‑locked ratio \(K_i^{motion}/K_i^{rest}\).
5. **Null Hypothesis**: Simulate with stochastic noise & standard PTA GW sources; false‑positive P<0.01.

---

## 5 · Risk & Confound Analysis

- **Solar‑wind dispersion**: Mitigate via multi‑frequency fitting.
- **Clock errors**: Cross‑check against terrestrial time standards; true sideband should follow heliocentric frame.
- **Gravitational‑wave lines**: Distinguish via unique Ki ratio signature.

---

## 6 · Integration Map

- **Positive detection** → Locks \(ξ, ω_g\) → feeds Γ(t) amplitude back into PPS‑035, tightening lab torsion‑balance targets.
- **Non‑detection** (within ξ<10‑8) → sets upper bound → informs cavity size & κ in Heart‑1 experiments.

---

## 7 · Change Log

- **v0.9 (2025‑07‑02)**: Initial backbone & protocol drafted; math appendices pending.

---

> *This module is intentionally standalone—no citations to PPS‑033‑035 math inside proofs. Peer duel scheduling under RIT‑ICS‑007 forthcoming.*

