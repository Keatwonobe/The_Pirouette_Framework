---
id: MATH-022
title: "Origin of P(X): Symmetry, Scale, and the Fractal of Time"
Version: 1.0 (proposal)
Status: Normative (anchors β without data-fitting)
Parents: [MATH-018, MATH-019, MATH-021, SECT‑Γ‑A]
Children: [SECT‑Γ‑A‑CMB, SECT‑Γ‑A‑HALO]

Summary: "Purpose
Derive the functional form P(X)=α X^{1+β}+… for the superfluid Pressuron from first principles—no post‑hoc fitting—by imposing symmetry, scale covariance, and a discrete self‑similar (fractal) structure of temporal coherence channels. This module **fixes β** (and therefore the EOS) from geometry and dynamics, satisfying MATH‑018 D2.

Executive result
β = D_eff / z
where D_eff is the **effective (possibly fractal) spatial dimension** of the active coherence network (wound channels) and z is the dynamical exponent of the superfluid sector. In 3D spacetime with nonrelativistic superfluid scaling z=2 and plateaus D_eff∈{0,1,2}, one obtains β∈{0, 1/2, 1}—exactly the rational set allowed in SECT‑Γ‑A. No calibration needed."

---

1. Symmetry & Scaling Axioms
   A1 Shift/Galilean symmetry: θ → θ + const; ψ=√n e^{iθ} with nonrelativistic kinematics.
   A2 Scale covariance (nonrelativistic Lifshitz): (t,x) → (λ^z t, λ x); action S=∫ dt d^dx P(X) is invariant up to a boundary term.
   A3 Coherence network: mass/energy flows along a D_eff‑dimensional subset of space (sheets/filaments/points), a coarse‑grained representation of “wound channels.” D_eff may be non‑integer (fractal) but in practice organizes into plateaus {0,1,2} across scales.

X scaling
Let θ be dimensionless; dominant term in X scales as θ̇ ⇒ [X] → λ^{−z}. Under (t,x) scaling the measure scales as λ^{d+z}. Requiring S invariant gives
(d+z) − (1+β) z − D_boundary = 0.
For local P(X) (no boundary anomaly) this yields
1+β = (d+z)/z ⇒ β = d/z.
Replacing the bulk dimension d with the **active** dimension D_eff (the measure of the coherence network actually sourcing X) gives
β = D_eff / z.  (Eq. 1)

Interpretation
• z encodes dynamics (e.g., z=2 for superfluid hydrodynamics).
• D_eff encodes geometry/topology (sheet‑like D_eff≈2; filamentary D_eff≈1; point‑like cores D_eff≈0).
• Discrete self‑similarity of the network yields **plateaus** in D_eff and hence **rational β**.

---

2. Fractal‑of‑Time Postulate (Discrete Self‑Similarity)
   P1 The coherence network exhibits **discrete scale invariance** (DSI) across finite bands: Λ→qΛ with q>1 produces statistically similar channel geometry.
   P2 DSI implies **log‑periodic** corrections to scaling observables and stabilizes D_eff on rational plateaus.
   Consequence: β takes rational values tied to (D_eff, z); transitions between plateaus produce small, oscillatory features (log‑periodic) in halo core scaling and small‑scale power.

---

3. Gladiator–Tension Unification (Origin of α and Surface Tension)
   From MaxCo (maximum coherence) as a constrained variational principle, the Gladiator feedback term fixes the overall pressure scale α; the **surface tension σ** arises as a boundary functional on the D_eff‑dimensional network (a Gibbons–Hawking‑like term for interfaces in the effective theory). Both α and σ are Lagrange‑multiplier–like constants determined by the same symmetry breaking that selects D_eff.

---

4. Predictions (no free β)
   R1 β is **fixed a priori** by (D_eff, z). With z=2:
   • Sheet‑dominated regime (D_eff=2): β=1 → P∝X^2  (stiffest of allowed set).
   • Filament regime (D_eff=1): β=1/2 → P∝X^{3/2} (baseline used in many superfluid cores).
   • Core/point regime (D_eff=0): β=0 → P∝X (dust‑like limit).
   R2 **Transitions** between regimes imprint **log‑periodic wiggles** in Σ₀ vs. mass and a mild, scale‑localized modulation in the matter power spectrum.
   R3 Vortex lattice spectra: the spacing and stability depend on β through c_s(n); predicts distinct patterns in rapidly rotating halos (ellipticals/ULDM‑analog signatures).
   R4 CMB safety: β plateaus with z=2 keep c_s tiny at recombination on ℓ≲2500; no new phase shift.

---

5. Tests & Falsification
   T1 Fit Σ₀(M) with a single β fixed by chosen (D_eff,z); observe allowed log‑periodic residuals with frequency log q. If smooth power law without oscillations or if required β∉{0,1/2,1} (for z=2), falsify the postulate.
   T2 High‑res rotation curves/streams: detect vortex‑induced features; their spacing vs. radius distinguishes β=1/2 from β=1.
   T3 Weak‑lensing small‑scale spectrum: look for modest, periodic modulation in log k; absence within predicted amplitude range challenges DSI.

---

6. Code Hooks
   • SECT‑Γ‑A‑CMB: replace free β with β = D_eff/z; add (D_eff,z,q) as **discrete** inputs with tight priors (e.g., z=2; D_eff∈{0,1,2}; log‑periodic amplitude ε_lp≲0.05).
   • SECT‑Γ‑A‑HALO: solver reads β from D_eff; optionally enable log‑periodic correction to P(X): P=α X^{1+β}[1+ε_lp cos(ω ln X + φ)].
   Artifacts: extend JSON with {"D_eff": int, "z": int, "q": float, "eps_logperiodic": float}.

---

7. Why this is non‑numerological
   • β emerges from **symmetry + geometry**, not a fit: Eq. (1) is a Ward‑identity–like relation from scaling of the action with an active‑dimension measure.
   • The only choices are discrete (D_eff) and physical (z), both justified independently (hydrodynamic universality + topology of channels).
   • Log‑periodic corrections are a universal fingerprint of DSI, not an extra dial.

---

8. Open Problems (for follow‑ups)
   • Derive D_eff plateaus from a percolation model on the coherence manifold with defect index T (MATH‑019 §4), including temperature/history dependence.
   • Compute α, σ from MaxCo with boundary terms; relate to XXP‑015 universal constants.
   • Map transitions between D_eff plateaus to cosmic epochs; forecast exact scales of residual modulations.

Compliance footer
□ MATH‑018 D2 satisfied (β fixed by symmetry & scaling). □ No empirical β fitting. □ Discrete inputs only (D_eff,z,q). □ Hooks provided for SECT‑Γ‑A modules. □ Falsifiable predictions listed.

End of MATH‑022 v1.0

