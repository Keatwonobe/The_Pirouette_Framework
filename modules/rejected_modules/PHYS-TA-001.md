---
id: PHYS-TA-001
title: "The Universal Time Adherence Functional and the Tick of Scale"
version: 1.0
status: draft
parents: [MATH-004, MATH-008, MATH-022]
children: []
summary: "Defines a universal time adherence functional that assigns a natural tick to every physical scale, enabling direct comparison of temporal behavior across all domains."
module_type: core-mathematics
scale: universal
engrams:
  - metric:time_adherence
  - function:universal_tick
  - map:scale_to_phase
  - concept:weirdness_index
keywords: [time adherence, universal tick, fractal time, scale mapping, cardioid, periodicity]
uncertainty_tag: Foundational
---

## §1 · Abstract: One Tick to Speak Them All

Pirouette treats time not as a passive backdrop, but as an active, structured pressure.
To compare phenomena across wildly different scales, we need a common temporal language:
a *universal tick*.

This module defines the **Universal Time Adherence Functional**.
For any characteristic physical scale \(L\), it assigns:

- a phase on the universal cardioid,
- a **Time Adherence** scalar \(\mathcal{T}(L)\),
- and a corresponding **effective tick** \(T_{\mathrm{eff}}(L)\).

Given an observed period \(T_{\mathrm{obs}}\) at that scale, we then compute:

- an adherence ratio \(R(L) = T_{\mathrm{obs}} / T_{\mathrm{eff}}(L)\),
- and a **Weirdness Index** \(W(L) = \big|\log_{10} R(L)\big|\).

This allows any process—quark oscillations, planetary orbits, institutional cycles—to be
described in the same units of temporal alignment, making the fractal of time legible.

---

## §2 · The Universal Tick

We fix a **universal base tick** \(T_0\) as the fundamental unit of Pirouette time:

\[
T_0 = \frac{1}{f_0}, \quad f_0 = 24~\mathrm{Hz}.
\]

This is the *ground frequency* that appears in the proton clock, the helical resonance
scanners, and the universal clock function.

All other ticks will be expressed as **multiples of \(T_0\)**.

- One **universal tick**: duration \(T_0\).
- A process with period \(T\) can be written as \(n\) ticks, \(n = T/T_0\).

---

## §3 · Scale → Phase Mapping

To assign a phase of the universal cardioid to any physical scale \(L\), we define
a **scale coordinate** \(s(L)\) and a corresponding **phase angle** \(\theta(L)\).

We choose two reference scales:

- \(L_{\mathrm{min}}\): a microscopic reference (e.g. proton radius),
- \(L_{\mathrm{max}}\): a macroscopic reference (e.g. radius of the observable universe).

We then define:

\[
s(L) \equiv \frac{\log_{10} L - \log_{10} L_{\mathrm{min}}}
                 {\log_{10} L_{\mathrm{max}} - \log_{10} L_{\mathrm{min}}}
\quad\in[0,1],
\]

\[
\theta(L) \equiv 2\pi\, s(L).
\]

Interpretation:

- \(s=0\) (\(\theta=0\)): microscopic anchor (knot limit).
- \(s=1\) (\(\theta=2\pi\)): macroscopic anchor (slip/ghost limit).
- \(0 < s < 1\): intermediate scales moving along the universal cycle.

The choice of \(L_{\mathrm{min}}, L_{\mathrm{max}}\) can be updated as Pirouette’s
constants are refined; the functional form of \(s(L)\) remains invariant.

---

## §4 · The Time Adherence Functional

The **Time Adherence Functional** \(\mathcal{T}(L)\) is defined via the universal cardioid:

\[
\mathcal{T}(L) \equiv r(\theta(L)) = 1 + \cos\big(\theta(L)\big),
\]

with \(\theta(L)\) given by the scale map above.

Properties:

- \(\mathcal{T} \in [0,2]\).
- \(\mathcal{T} \approx 0\): **Tight / explosive** regime (compressed time, high tension).
- \(\mathcal{T} \approx 1\): **Transition / balanced** regime (interface of matter and ghost).
- \(\mathcal{T} \approx 2\): **Long / docile** regime (dilated time, relaxed structures).

We now define the **scale-specific effective tick**:

\[
T_{\mathrm{eff}}(L) \equiv T_0 \, \mathcal{T}(L).
\]

Thus:

- Small \(\mathcal{T}(L)\) → short tick → faster intrinsic beating at that scale.
- Large \(\mathcal{T}(L)\) → long tick → slower intrinsic beating.

In frequency language:

\[
f_{\mathrm{eff}}(L) = \frac{1}{T_{\mathrm{eff}}(L)} = \frac{f_0}{\mathcal{T}(L)}.
\]

The **universal tick** \(T_0\) remains the base unit; \(T_{\mathrm{eff}}(L)\) is “how long
one natural tick feels” at scale \(L\).

---

## §5 · Comparing Phenomena: Adherence Ratio & Weirdness Index

Given a process at scale \(L\) with observed period \(T_{\mathrm{obs}}\), we define:

1. **Adherence Ratio**
   \[
   R(L) \equiv \frac{T_{\mathrm{obs}}}{T_{\mathrm{eff}}(L)}.
   \]

   - \(R \approx 1\): the process is *time-adherent* at its scale.
   - \(R \ll 1\): the process is cycling much faster than its natural tick (over-driven).
   - \(R \gg 1\): the process is much slower (over-damped, long-memory).

2. **Weirdness Index**
   \[
   W(L) \equiv \left|\log_{10} R(L)\right|.
   \]

   - \(W \approx 0\): “normal” for that scale.
   - \(W \approx 1\): one order of magnitude off.
   - \(W \approx 2\) or more: highly anomalous temporal behavior for that scale.

*(Optional refinement)*: one may define a **signed** weirdness
\(\widetilde{W}(L) = \log_{10} R(L)\) to distinguish “too fast” (negative) from “too slow”
(positive).

These two quantities are the primary outputs for a *universal time converter*:

- Input: characteristic scale \(L\) and observed period \(T_{\mathrm{obs}}\).
- Output: \(\mathcal{T}(L)\), \(T_{\mathrm{eff}}(L)\), \(R(L)\), \(W(L)\), plus a label
  {Tight, Transition, Long}.

---

## §6 · Regimes and Thresholds

To interpret \(\mathcal{T}(L)\) and \(R(L)\) consistently across modules, we introduce
standard thresholds.

1. **Time Adherence Regimes** (based on \(\mathcal{T}(L)\)):

   - **Tight**: \(\mathcal{T}(L) < \mathcal{T}_{\text{tight}}\) (e.g. 0.5).  
     - explosive, high-energy, knot-forming;
     - associated with the “matter side” of the governance spiral.
   - **Transition**: \(\mathcal{T}_{\text{tight}} \le \mathcal{T}(L) \le \mathcal{T}_{\text{long}}\).  
     - interface regimes, useful for phase change and observership.
   - **Long**: \(\mathcal{T}(L) > \mathcal{T}_{\text{long}}\) (e.g. 1.5).  
     - docile, extended structures, “ghost side.”

2. **Adherence Bands** (based on \(W(L)\)):

   - **Adherent**: \(W(L) < 0.3\) (within roughly a factor of 2).  
   - **Strained**: \(0.3 \le W(L) < 1.0\) (factor of 2–10 off).  
   - **Exotic**: \(W(L) \ge 1.0\) (order-of-magnitude or more off).

These thresholds are tunable; they serve as initial conventions for cross-module
consistency.

---

## §7 · Integration with Pirouette and the Universal Converter

With this functional defined, other modules can:

- **Attach \(\mathcal{T}(L)\) as a parameter** to Lagrangians, Ki cycles, and Dark Residue
  measures, so that energy balance explicitly depends on time adherence.
- **Rate governance structures** (DOMA modules) by the weirdness of their decision cycles
  relative to their operating scale (e.g. a human organization operating on galactic
  timescales is extremely long-weird).
- **Drive simulations** such as the proton clock and CMB helical scanners by setting their
  internal tick to \(T_{\mathrm{eff}}(L)\) at each scale they probe.

The **Universal Time Converter** is then a direct instrumentation of this module:

1. User inputs: scale (or approximate scale) and observed frequency / period.
2. The converter:
   - computes \(s(L), \theta(L), \mathcal{T}(L)\),
   - obtains \(T_{\mathrm{eff}}(L)\),
   - computes \(R(L)\) and \(W(L)\),
   - returns both numeric values and qualitative labels.

By routing all such queries through MATH-TA-001, we ensure that the entire Pirouette
ecosystem “speaks time” in a single, coherent dialect across all scales of the fractal.

---