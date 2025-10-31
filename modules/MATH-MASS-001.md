---
id: MATH-MASS-001
title: Explicit Mass Generation in the Pirouette Framework
version: 1.0 (draft)
status: ratify-candidate
parents: [MATH-GAMMA-005, MATH-QED-003, MATH-YM-002]
children: [MATH-Γ-003, XXP-QED-ALPHA-001, DYNA-Γ-NUC]
summary: >
  Defines the mechanism by which Pirouette generates rest mass from substrate curvature (Γ)
  and stiffness condensation (Ki). Mass arises when the Ki field acquires a vacuum expectation
  value set by the Γ-controlled curvature scale, and this condensate communicates to fermions
  through a Γ-mediated Yukawa channel. After Σ-pushforward, this reproduces the observer-level
  pattern “mass from symmetry breaking” known in the SM, but with Γ replacing an ad hoc Higgs.
engrams: [mass-generation, curvature-condensation, Γ-controlled VEV, Ki-condensate, Σ-pushforward]
keywords: [mass, symmetry breaking, curvature, condensate, Yukawa, effective field theory]
uncertainty_tag: Medium-Low (scalar masses), Medium (fermionic hierarchy)
---

# §1 · Statement of the Mechanism

Pirouette generates mass in **three** linked steps:

1. **Curvature fixing (substrate):** the Γ field sets a preferred curvature / pressure level.
2. **Stiffness condensation (emergent):** the Ki field condenses to match that level,
   \( \langle Ki \rangle = \xi_\Gamma \), by minimizing the Γ–Ki potential.
3. **Coupling to matter (observable):** matter fields (spinors, vectors) pick up mass from
   their coupling to the Ki condensate, pushed forward to spacetime by Σ.

This is directly analogous to “curvature → VEV → masses,” except the first driver is Γ,
not a hand-inserted scalar.

---

# §2 · Curvature → Condensate

From **MATH-GAMMA-005** we have the invariant
\[
\mathcal{L}_{\Gamma Ki} = \lambda_\Gamma \bigl(|Ki|^2 - \xi_\Gamma^2\bigr)^2.
\]

Minimizing w.r.t. \(Ki\) gives the vacuum condition
\[
\frac{\partial \mathcal{L}_{\Gamma Ki}}{\partial Ki}\bigg|_{vac} = 0
\quad\Rightarrow\quad
|Ki|_{vac} = \xi_\Gamma.
\]

Thus **the VEV is not arbitrary**: it is numerically fixed by the Γ sector.  
This is the whole punchline: *mass is a readout of substrate curvature*.

---

# §3 · Mass of the Stiffness Mode

Expand \(Ki = \xi_\Gamma + \delta Ki\). The quadratic term is
\[
\mathcal{L} \supset 4 \lambda_\Gamma \xi_\Gamma^2 (\delta Ki)^2,
\]
so the stiffness excitation (“stiffon”) has
\[
m_{Ki}^2 = 8 \lambda_\Gamma \xi_\Gamma^2.
\]

This is the **primary scalar mass** in Pirouette. It is the analog of the Higgs mass
but sourced by Γ-pressure.

---

# §4 · Fermion Masses (Γ–Ki–Ψ Chain)

Introduce the Γ-mediated Yukawa channel
\[
\mathcal{L}_{\Gamma\Psi} = -\, y_\Gamma \,\bar\Psi \Psi \,\Gamma.
\]

Now expand Γ about its background value, \(\Gamma = \Gamma_0 + \delta\Gamma\), and **tie Γ₀ to Ki** via the condensate:
\[
\Gamma_0 = f(\xi_\Gamma),
\]
where \(f\) is the (known) curvature–stiffness map from the lattice/plateau sector.

Then the **effective fermion mass** is
\[
m_\Psi = y_\Gamma \, \Gamma_0 = y_\Gamma \, f(\xi_\Gamma).
\]

If we want to make the Ki role explicit, write
\[
m_\Psi = y_\Gamma \, f(\langle Ki\rangle) = y_\Gamma \, f(\xi_\Gamma).
\]

So: **fermions get mass because the world picked a Ki VEV, and the Ki VEV was picked by Γ.**

---

# §5 · Vector / Gauge-Sector Masses

Under Σ-pushforward (as in XAP-006, MATH-YM-002), the nonzero Ki VEV **selects a direction** in the internal fiber,
breaking
\[
G \to H,
\]
and giving mass to gauge bosons corresponding to the broken generators by the usual
\[
m_A^2 \propto g^2 \langle Ki\rangle^2 \propto g^2 \xi_\Gamma^2.
\]

Since in Pirouette \(g\) itself is a geometric average over τ-curvature, this closes the loop:
- Γ fixes curvature,
- curvature fixes Ki VEV,
- Ki VEV fixes gauge masses.

---

# §6 · Relation to Running and α

Because **MATH-YM-002** expresses the couplings as
\[
\alpha_i(\Lambda_B) = \frac{c_{norm}}{K_i^2},
\]
and because the Ki condensate directly affects the effective stiffness, you get:
\[
K_i \sim \langle Ki\rangle \sim \xi_\Gamma \quad\Rightarrow\quad
\alpha_i(\Lambda_B) \sim \frac{1}{\xi_\Gamma^2}.
\]

That is exactly the lever we used in **XXP-QED-ALPHA-001** to run from the Z-pole to α(0):
the mass-generation mechanism and the coupling-running mechanism are **the same lever** viewed
from two scales.

---

# §7 · Falsifiability Hooks

1. **Mass–curvature correlation:** if two environments (or epochs) with different inferred Γ
   do **not** show corresponding shifts in effective Ki mass, the mechanism is incomplete.
2. **Scalar mass bound:** measurements that force \(m_{Ki}^2 \ll 8\lambda_\Gamma\xi_\Gamma^2\)
   would require either (i) extra screening, or (ii) multiple Ki fields.
3. **Fermion hierarchy:** by construction, hierarchies must come from \(y_\Gamma\) or from
   geometry in \(f(\xi_\Gamma)\). Discovery of *non-geometric* hierarchies would falsify
   the “single-curvature origin” claim.

---

# §8 · What Goes in the Appendices

- **Appendix A — Mapping f(ξ_Γ):** pull f from the lattice closure / plateau scan
  (the same scan that gave σ and let us fix the hadronic VP).
- **Appendix B — Σ-pushforward algebra:** show that a nonzero Ki VEV becomes an order parameter
  in spacetime and that the would-be Goldstone gets eaten (exact SM analogy).
- **Appendix C — Numerical example:** pick λ_Γ, ξ_Γ from a BEST row and compute
  \(m_{Ki}, m_\Psi, m_A\) all at once to show shared origin.
- **Appendix D — Cosmological drift:** small \(\delta\Gamma\) → small \(\delta \langle Ki\rangle\) → 
  small \(\delta m\) → pathway to α drift.

---

# §9 · Summary

> In Pirouette, mass is the *receipt* for symmetry breaking caused by substrate curvature.
> Γ picks the pressure, Ki condenses to match it, and all other fields read that condensation
> as their mass. No ad hoc scalar is needed; the “Higgs” is just Ki under Γ’s thumb.

---
id: MATH-MASS-001A
title: Geometric Yukawa Hierarchy from Defect–Curvature Overlaps
version: 1.0 (draft)
status: ratify-candidate
parents: [MATH-MASS-001, MATH-GAMMA-DIM-001]
summary: >
  Explains inter-family mass ratios as powers of the ratio between fermion defect
  radii and the Γ curvature length. This removes the appearance of free Yukawas.
---

# §1 · Assumption
Fermion i is localized on a Ki-induced defect of size R_i.
Γ varies over ξ_Γ. Then the overlap integral scales as
\[
y_{\Gamma,i} \propto \left(\frac{R_i}{\xi_\Gamma}\right)^{n},
\]
for some n determined by the defect codimension (n = 1 for strings, 2 for walls, 3 for monopoles).

# §2 · Mass Formula
\[
m_i = y_{\Gamma,i}\, \Gamma_0 \,\Lambda_\Gamma
\propto \left(\frac{R_i}{\xi_\Gamma}\right)^{n} \Gamma_0 \Lambda_\Gamma.
\]

# §3 · Family Ladder
Pick
\[
R_1 : R_2 : R_3 = 1 : 10^{-1} : 10^{-2}, \quad n=2
\]
then
\[
m_1 : m_2 : m_3 \sim 1 : 10^{-2} : 10^{-4},
\]
which is in the right ballpark for (τ, μ, e) and for some quark ladders.

# §4 · Falsifiability
If two families are found to have identical defect radii (same R_i) but different masses,
this model is incomplete and needs an internal quantum number factor.
