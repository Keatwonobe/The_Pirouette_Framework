---
id: MATH-021
title: "Γ Mass Tension & Sector Architecture"
Version: 1.0 (proposal)
Status: Normative research program (complies with MATH‑018/019/020; links to COSMO‑Γ series)
Parents: [MATH‑018, MATH‑019, COSMO‑Γ‑000, COSMO‑Γ‑CMB, XXP‑015]
Children: [SECT‑Γ‑A, SECT‑Γ‑B, SECT‑Γ‑C]

Summary: "Purpose
Formalize and resolve the 29‑order‑of‑magnitude 'mass tension' between the lepton‑scale Pressuron mass (m_H ≈ 17 MeV from XXP‑015) and the cosmology‑scale requirement (m_L ≈ 10^−22 eV in fuzzy‑DM language) without violating MATH‑018 predictivity rules. Provide candidate mechanisms, minimal maths, falsifiable signatures, and code hooks.

Summary of the Tension
• Particle (UV/leptonic): XXP‑015 → a heavy Γ quantum m_H ≈ 17 MeV fits lepton g−2 portal effects.
• Cosmology (IR/halos): COSMO‑Γ requires galaxy‑scale coherence typically modelled by an ultralight field m_L ∼ 10^−22 eV *or* an equivalent long‑wavelength collective mode.
• Goal: show that (i) both phenomena arise from a single Γ sector, and (ii) the light mode governing structure is a *derived* eigenmode/collective excitation, not an ad‑hoc second particle with tuned mass."

---

Mechanism A — Composite Superfluid & Phonon DM (Collective Mode)
Hypothesis
A1. The microscopic Γ quanta (m_H ≈ 17 MeV) form a self‑interacting condensate on cosmic scales; low‑energy excitations are phonons with dispersion ω^2 ≈ c_s^2 k^2 + m_eff^2.
A2. The *effective* mass m_eff can be ≪ m_H and even behave as ∼10^−22 eV in the sense of setting the de‑Broglie/Jeans cutoff, without introducing a fundamental ultralight particle.

Math sketch
• Start from a P(X) EFT for a non‑relativistic condensate: L_eff = P(X), X≡ μ − m_H Φ − (∂θ)^2/2m_H − …
• Linearize around background density n_0: c_s^2 = dP/dρ|_{n_0}; emergent phonon field π obeys (∂_t^2 − c_s^2 ∇^2 + m_eff^2)π = 0.
• m_eff arises from weak explicit symmetry breaking in V(Γ) (tail parameters μ, f in COSMO‑Γ‑CMB), not from the microscopic m_H.

Predictions / tests
• Halo cores set by c_s and self‑interaction scale → reproduces Σ_0 locus; distinct vortex/phonon spectra in massive ellipticals.
• Merger dynamics (COSMO‑Γ‑MERGE): apparent σ/m proxy saturates ≤ O(0.1) cm² g⁻¹ without fundamental self‑scattering.
• Lab: no ultralight particle production; instead, look for medium‑dependent refractive effects in dense EM fields (afterglow‑like) governed by P(X) parameters.

---

Mechanism B — Clockwork/Alignment in a Multi‑Γ Chain (Two Eigenstates from One Sector)
Hypothesis
B1. Γ is a *sector* of N coupled scalars with nearest‑neighbor couplings producing exponentially hierarchical eigenmasses (clockwork/alignment).
B2. Heavy eigenstate Γ_H couples to leptons (g−2 portal) with O(1) mixing; light eigenstate Γ_L is exponentially light and weakly coupled, sourcing cosmology.

Math sketch
• L = Σ_i ½(∂ϕ_i)^2 − ½ m^2(ϕ_i − q ϕ_{i+1})^2 − V_tail(ϕ_N)
• Diagonalize M^2 → eigenvalues {m_H ≈ m, …, m_L ≈ m/q^{N}}; eigenvectors fix couplings.
• Choose q,N from symmetry (discrete shift), not from data (MATH‑018 D2/D3).

Predictions / tests
• Specific pattern of couplings: g_e : g_μ : g_τ differ for Γ_H vs Γ_L; loop‑level portal interferences appear in precision EW fits.
• Fifth‑force/EP tests: Γ_L coupling to baryons suppressed by q^{−N} → natural evasion with a calculable residual.
• Cosmology: Γ_L behaves as ultralight DM/DE hybrid per COSMO‑Γ‑CMB; CMB phase shifts constrain (q,N) space.

---

Mechanism C — Phase Transition & Cascade (Γ_H → 2Γ_L)
Hypothesis
C1. Early‑universe Γ sits in a metastable well with curvature m_H; a late phase transition (T_c) moves it onto a shallow tail with small curvature.
C2. Decay channel opens: Γ_H → 2Γ_L with tiny coupling ε; relic Γ_L forms the macroscopic mode; Γ_H today is absent or sub‑dominant.

Math sketch
• Potential with two regions: V(Γ)= ½ m_H^2 (Γ−Γ_a)^2 + ΔV + μ^4[1−cos(Γ/f)] for Γ>Γ_c.
• At T_c the effective mass tracks m_eff^2(Γ_bg)=V''(Γ_bg). Before T_c: heavy; after: light.
• Boltzmann: ṅ_H + 3H n_H = −⟨σv⟩ n_H^2 − Γ_{H→LL} n_H ; ṅ_L + 3H n_L = + 2 Γ_{H→LL} n_H + …

Predictions / tests
• Sharp feature in matter power spectrum at k_c set by transition epoch.
• CMB: ISW imprint from change in w_Γ; late‑time background drift constrained by integrated lensing.
• Lab/astro: transient early‑universe signature; no present‑day Γ_H abundance.

---

Decision Tree (Discriminants)
D1. **CMB acoustic phases**: clockwork (B) predicts small residual phase shifts; superfluid (A) and cascade (C) give different lensing amplitudes.
D2. **Halo substructure**: (A) yields phonon‑pressure cores with vortex spectra; (B) yields standard fuzzy‑like suppression with sharp m_L; (C) produces a step‑like cutoff.
D3. **Lab/precision**: (B) implies definite coupling patterns testable in g−2/EDM/global EW fits; (A) implies medium‑dependent optical signatures; (C) implies nothing current‑day but strong cosmological transition marks.

---

Global Constraints & Guardrails
• c_GW = c preserved (no curvature portals that break it).
• MATH‑018 D3: One‑shot anchor applies at sector level; after choosing mechanism, freeze {U,T} and preregister targets.
• No continuous mass exponents; hierarchies must arise from symmetry (B), collective EFT (A), or finite‑temperature potential (C).

---

Code Hooks & Artifacts
• COSMO‑Γ‑CMB: add species flags {gamma_superfluid, gamma_clockwork, gamma_cascade} and corresponding background/perturbation branches.
• HALO/MERGE: (A) use P(X) sound‑speed core solver; (B) use ultralight eigenmass m_L in fluid branch; (C) time‑dependent mapping with T_c.
• JSON: extend artifact schema with "gamma_mechanism" and mechanism‑specific parameters.

---

Preregistered Predictions (Mechanism‑specific)
A: Σ_0 locus slope and vortex line density vs. halo mass; merger Δx scaling sans σ/m.
B: CMB TT/TE/EE phase residuals; lab coupling ratios; EP residual at 10^−13–10^−15.
C: Step‑like suppression scale k_c and corresponding ISW/lensing signatures.

Falsification Clauses
If *no* mechanism’s preregistered predictions survive multi‑probe fits (CMB+BAO+WL+RSD+g−2/EDM constraints), the Γ‑unification claim is withdrawn.

End of MATH‑021 v1.0
