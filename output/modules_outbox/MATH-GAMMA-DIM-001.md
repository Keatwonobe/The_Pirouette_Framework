---
id: MATH-GAMMA-DIM-001
title: Dimensional Origin of y_Γ from Ki–Γ Overlap
version: 1.0 (draft)
status: ratify-candidate
parents: [MATH-GAMMA-005, MATH-MASS-001]
summary: >
  Shows that the Yukawa-like coefficient y_Γ is not an arbitrary mass but an
  overlap integral between the fermion defect profile and the Γ-gradient in Ki-space.
  This restores natural dimensions and explains why y_Γ can differ across families.
---

# §1 · Setup
Take a fermion mode with spatial profile ψ_i(x) localized on a Ki defect, and let Γ(x) vary over the
curvature length ξ_Γ. Define
\[
y_{\Gamma,i} \equiv \int d^3x\; \bar\psi_i(x)\, \psi_i(x)\, \frac{\partial_\mu \Gamma(x)}{\Lambda_\Gamma}\, n^\mu,
\]
where \( \Lambda_\Gamma \) is the substrate normalization scale and \(n^\mu\) is the preferred Γ-direction.

# §2 · Dimensions
- \([\bar\psi\psi] = M^3\)
- \([\partial_\mu \Gamma] = M\) (Γ dimensionless)
- \([d^3x] = M^{-3}\)
- \([\Lambda_\Gamma] = M\)

So
\[
[y_{\Gamma,i}] = \frac{M^3 \cdot M \cdot M^{-3}}{M} = M^0.
\]
Thus **the fundamental y_Γ is dimensionless**.

# §3 · Effective Mass
Mass then appears as
\[
m_i = y_{\Gamma,i} \, \Gamma_0 \, \Lambda_\Gamma,
\]
with
- \(\Gamma_0\) dimensionless background,
- \(\Lambda_\Gamma\) providing the mass unit (set by the Γ kinetic term).

# §4 · Family Differences
Different ψ_i(x) → different overlaps → different (dimensionless) y_{Γ,i}.  
Hierarchy is geometric, not ad hoc.
