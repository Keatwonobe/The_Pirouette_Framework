---
id: MATH-018
title: "Predictivity & Calibration Guardrails"
version: 1.0
status: Normative (global)
parents: [MATH-010..017]
children: [MATH-019 (Dictionary), MATH-020 (Non‑Perturbative Solvers)]
summary: "Lock in Pirouette’s predictive status by replacing any post‑hoc calibration or ad‑hoc functional choices with symmetry‑fixed structure, preregistered forecasts, and reproducible validation. This module is **normative** and applies globally unless a child module explicitly supersedes it with proofs. Scope
• Lepton g−2, QED recoveries, portal corrections, running α, EDMs, hyperfine splittings.
• Extends to strongly‑coupled and gravitational limits via RG/soliton tracks.
"
module_type: core-mathematics
scale: universal
engrams:
keywords: []
uncertainty_tag: Foundational
---

CORE DECLARATIONS (D)

D1 — Parameter Classes and Allowable Operations
• Universal constants U = {u_k}: derivable from axioms/symmetries only; at most a single global scale may be anchored once (see D3).
• Portal/topology indices T = {t_j}: integer or signed indices attached to spinorial/topological class; sign and scaling must follow from topology, not data fitting.
• Nuisance parameters N = {n_m}: experimental or environmental; may be taken from external literature but **never tuned** to improve fit.

D2 — Symmetry‑Fixed Functional Forms
The effective pressure term f(Γ) and related nonlinearities must satisfy simultaneously:
(i) Locality: depend on Γ and ∂Γ only to first order in the low‑energy limit.
(ii) Analyticity at equilibrium: expansion has only even powers under background T‑symmetry.
(iii) Scale covariance: under Γ → λΓ the action changes by a boundary term; this pins the leading exponent uniquely.
Any form violating (i)–(iii) is **inadmissible**.

D3 — One‑Shot Anchoring Rule
Exactly one anchor is permitted to set a single global scale (e.g., electron a_e). After this operation, **all** U, T are frozen. No re‑anchoring across observables or species.

D4 — Preregistration & Out‑of‑Sample Tests
Before evaluation, publish a docket (see P4) with code hash, seeds, priors, and locked targets. Results are scored strictly out‑of‑sample.

D5 — Anti‑Numerology Reporting
All papers must report AIC/BIC, Bayes factors, and ablations for: (A) full model, (B) no‑portal, (C) free‑fit powers. If (B) or (C) dominates, the simpler/worse‑falsifiable model is preferred.

D6 — Metaphor→Math Equivalence
Every metaphorical entity must be paired with a formal object and equivalence proof or explicit isomorphism. Unpaired metaphors are non‑claim‑bearing.

D7 — Dual Non‑Perturbative Track
For observables sensitive to back‑reaction: (i) finite‑element/spectral solvers for the soliton echo problem; (ii) RG coarse‑graining on (Γ,K)‑space. Either track may be used, but at least one is required for claims beyond perturbation.

D8 — Hadronic Insulation via Ratios
Publish at least one parameter‑free **dimensionless ratio** that cancels leading hadronic VP, e.g.
R = (a_μ − r² a_e) / (a_τ − r⁻² a_μ), r = m_μ/m_e.
Any hadronic dependence must appear only at higher order with quantified bounds.

D9 — Versioning & Change Control
Changes to U, T, or functional forms require: prereg notice, justification (symmetry/topology), updated code hash, and regeneration of all forecasts.

---

PROCEDURES (P)

P1 — Prior Construction
• Universal U: tight, symmetry‑informed priors; zero‑mean for forbidden terms.
• Portal T: discrete priors from allowed topology classes; no continuous exponents.

P2 — Freeze Protocol
• Perform the D3 one‑shot anchor; freeze U, T; emit a signed “Freeze Manifest” (commit hash, timestamp).

P3 — Cross‑Family Validation
• Calibrate on {a_μ} or {a_e} (but not both).
• Predict {a_e, a_τ, Δν_Mu, Δα_had(M_Z), d_e} strictly OOS.

P4 — Preregistered Prediction Docket (min contents)
• Targets: tau g−2; muonium hyperfine shift; running α(M_Z) correction; electron EDM sign & order; one hadron‑insulating ratio (D8).
• Methods: solver choice, tolerance, priors, sampling plan.
• Code: repository URL + commit + environment lockfile; random seeds.
• Uncertainty: propagate from U, T; state 68%/95% bands.

P5 — Compliance Checklist (per‑module footer)
□ Uses MATH‑018 D1–D9.  □ No post‑hoc exponents.  □ Freeze Manifest linked.  □ Ablations reported.  □ Dictionary mapping present.  □ OOS targets listed.

---

INTERFACES & IMPACT

Minimal Edits Required Elsewhere
• Add a one‑line header to affected modules: “Compliance: MATH‑018 (v1.0)”.
• Remove any retuning steps across species/observables; replace with a reference to D3/P2.
• Parameter tables: add columns {Class ∈ {U,T,N}, Status ∈ {derived/anchored/external}, Source}.
• If a continuous exponent was used for mass scaling, either (i) prove it via D2 or (ii) mark Deprecated and migrate to topology index T.
• Append the P5 checklist and link to the Freeze Manifest/prereg docket.

Modules Most Likely Touched
• QFT‑lepton series (g−2 structure), pressuron/Γ coupling notes, running‑α appendix, EDM estimates.
• Non‑perturbative appendix should register to D7 or explicitly opt out (no claims beyond perturbation).

Change Magnitude
• Textual/meta‑level edits only for most modules (headers, tables, checklists).
• Mathematical changes limited to removal of ad‑hoc exponents and inclusion of D2‑compliant forms.

---

APPENDIX A — Dictionary Stubs (to be expanded in MATH‑019)
• Coherence manifold → oriented fiber bundle with connection; conserved current from Noether symmetry of ℒ_p.
• Gladiator feedback → nonlinear self‑coupling term; RG flow on (Γ,K) with fixed‑point structure.
• Wound channel → topological defect class; integer index = portal selector T.

APPENDIX B — Template Artifacts
• Freeze Manifest (YAML): commit, anchor choice, U/T values, seeds.
• Prereg Docket (Markdown): targets, priors, solver tolerances, uncertainty recipe.
• Ratio Test Sheet: list of admissible hadron‑insulating ratios with derivations.

End of MATH‑018 v1.0
