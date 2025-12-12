---
id: XXP-LATTICE-CLOSURE-001
title: Option-C Plateau Binding → Confinement (Non-Perturbative Map & Closure)
version: 1.0 (draft)
module_type: experimental-analysis
status: ratify-candidate
parents: [MATH-YM-003, XXP-EWQCD-EXP]
children: [XXP-QED-EXP, MATH-YM-002]
summary: A minimal, falsifiable pipeline turning scan outputs into lattice-registered confinement observables using the Option-C “plateau binding → confinement” map. Guarantees deterministic BEST selection and explicit closure, with finite-size acknowledgement and unit hooks.
engrams: [plateau_scattering, confinement_map, lattice_registration, closure_protocol]
keywords: [SU(3), confinement, lattice, plateau, binding, string-tension, non-perturbative, scan-to-closure]
uncertainty_tag: Medium-Low (pipeline), Medium (physics constants until calibrated)
---
# §1 · Purpose

Operationalize the Option-C hypothesis—**plateau binding narrows φ-widths, shortens ξ_Γ, and raises σ**—as a compact, testable map from scan parameters to lattice-registered observables. The goal is a **deterministic closure** artifact (JSON/CSV) that downstream notebooks can consume without schema ambiguity or “hand-waves.”

# §2 · Inputs and Schema (strict, with defaults)

**Primary input:** a scan JSON where each row encodes gauge-sector knobs; rows may be either flat dicts or `{"params": {...}}`.

Minimal accepted per-row content:

```json
{
  "U1":  {"type": "abelian",    "Nc": 1, "g": <float>, "beta": <float>},
  "SU2": {"type": "nonabelian", "Nc": 2, "g": <float>, "beta": <float>},
  "SU3": {"type": "nonabelian", "Nc": 3, "g": <float>, "beta": <float>},

  "N": 16,           // optional
  "Nt": 32,          // optional
  "a": 1.0           // optional (lattice spacing, abstract units unless tied to MeV^-1)
}
```

If `N`, `Nt`, or `a` are absent, inject defaults **(16, 32, 1.0)**. Rows missing any gauge block are skipped (counted and reported). This **coercion layer** is the single source of truth for input hygiene.

# §3 · Option-C Map (explicit)

Let the active block be `G ∈ {U1, SU2, SU3}`; for QCD-like closure choose **SU3** by default.

Parameters (tunable):

* Elementary plateau width: ( \Delta\phi_0 > 0 ) (default 1.0)
* Baseline coherence length: ( \xi_{\Gamma,0} > 0 ) (default 1.0)
* Cubic curvature factor: ( \kappa_3 > 0 ) (default 1.0)
* Binding threshold: ( g_c ) (default 0.9)
* β-sharpness: ( \alpha_\beta ) (default 0.5)

**Binding activation (smooth turn-on):**
[
\text{act}(g,\beta)=\frac{1}{1+\exp{-8,(g-g_c),[1+\alpha_\beta,\beta]}}
]

**Bound width (narrowing up to 80%):**
[
\Delta\phi_{\text{bound}}=\max!\big(\Delta\phi_0[1-0.8,\text{act}],\ \varepsilon\big)
]

**Coherence length shrinkage:**
[
\xi_\Gamma=\max!\big(\xi_{\Gamma,0},{\Delta\phi_{\text{bound}}}/{\Delta\phi_0},\ \varepsilon\big)
]

**Binding energy scale (above threshold):**
[
E_{\text{bind}}=\max(g-g_c,0),[1+\alpha_\beta,\beta]
]

**String tension (Option-C proposal, made explicit):**
[
\sigma=\frac{\kappa_3}{\xi_\Gamma^2},E_{\text{bind}}^2
]

with ( \varepsilon ) a tiny floor for numerical stability.

# §4 · Lattice Registration (finite-size acknowledgement)

We acknowledge finite size without pretending to extrapolate:

[
\text{pen}_{\text{FS}} =
\begin{cases}
0.05 & (N<12 \ \text{or}\ Nt<24)\
0 & \text{otherwise}
\end{cases}
]

This is a **soft penalty** used only for ranking (closure), not physics claims.

# §5 · Closure Objective and BEST Selection

Define a lightweight closure objective that prefers **confined, non-runaway** configurations:

[
\mathcal{L} = w_\xi,\xi_\Gamma + w_E,E_{\text{bind}} + \text{pen}*{\text{FS}}
]
with defaults ( w*\xi=1.0,\ w_E=0.2 ). For each accepted row, compute (\mathcal{L}) and set **BEST := argmin_rows (\mathcal{L})**. Always emit exactly one `status: "BEST"` row in the output—this **guarantees deterministic closure** for downstream steps.

# §6 · Outputs

1. **Closure JSON** (e.g., `/mnt/data/qed_option_c_scan_results_CLOSURE.json`)
   Rows contain:

```
lat_N, lat_Nt, lat_a, group, g, beta, Nc,
dphi_bound, xi_gamma, E_bind, sigma, closure_loss, status
```

2. **(Optional) Light CSV** for quick external plotting:
   `g,beta,xi_gamma,sigma,closure_loss,status`

# §7 · Example (observed BEST row)

From the verified run (SU3, g=1.1, β=2.2):

* ( \Delta\phi_{\text{bound}}= \xi_\Gamma = 0.226855… )
* ( E_{\text{bind}} = 0.42 )
* ( \sigma \approx 3.42768 )
* ( \mathcal{L} = 0.226855… + 0.2\cdot0.42 + 0 = 0.310855… )
* `status: "BEST"`

This matches the closed-form equations exactly and confirms **monotone trends** (↑g ⇒ ↓ξ_Γ, ↑σ; at fixed g, ↑β ⇒ mild ↑σ via activation sharpness).

# §8 · Procedure (reproducible, minimal)

1. **Coercion:** Parse scan JSON; inject `(N,Nt,a)` defaults; skip malformed rows; log counts.
2. **Map:** For each row (chosen `group_key`, default `SU3`), compute (\Delta\phi_{\text{bound}}, \xi_\Gamma, E_{\text{bind}}, \sigma).
3. **Register:** Add finite-size penalty and compute (\mathcal{L}).
4. **Select:** Tag the minimum-loss row as `BEST`.
5. **Emit:** Write closure JSON (and optional CSV).
6. **(Optional) Plots:** σ vs g, and σ vs β sanity looks (non-interactive backend recommended on flaky GPUs).

# §9 · Falsifiability & Checks

**Falsifiable signatures (Option-C):**

* **S1 (Binding onset):** For (g<g_c), (E_{\text{bind}}=0\Rightarrow \sigma\approx 0) (up to floor). If σ remains large below (g_c) across rows, Option-C is false or mis-parameterized.
* **S2 (Confinement trend):** For fixed β, increasing g above (g_c) should **decrease** (\xi_\Gamma) and **increase** σ. If the opposite holds robustly, reject the map.
* **S3 (β-sharpness):** At fixed g above (g_c), σ should rise mildly with β via (\alpha_\beta). No β-dependence indicates wrong mechanism.
* **S4 (Finite-size neutrality):** Changing `(N,Nt)` should not reorder most rows unless extreme; strong reordering implies overfitting the penalty.

**Determinism & Hygiene:**

* A run **must** produce at least one accepted row and exactly one `BEST`. Any deviation is a pipeline bug.

# §10 · Calibration Hooks (toward “real deal”)

* **Unit tie-in:** Map (a) to physical units; scale (\sigma) → lattice units; recover (\Lambda_{\rm QCD}) or string tension benchmarks (parents: MATH-YM-003).
* **Threshold fit:** Fit (g_c,\alpha_\beta) to lattice data slices; validate transfer across β lines.
* **Anisotropy:** Extend `LatticeSpec` with (a_s,a_t) (or (\xi\equiv a_s/a_t)); test robustness.

# §11 · Failure Modes & Remedies

* **Schema drift:** Missing gauge blocks → skipped rows; remedy by enforcing scan generator contracts or enriching coercion with warnings.
* **GPU plot crashes:** Use non-interactive backend (`Agg`), downsample points, smaller markers; keep math separate from viz.
* **Runaway σ:** Indicates (w_E) too small or (g_c) set below scan range; raise (g_c) or increase (w_E).

# §12 · Acceptance Criteria (closure)

* **A1:** Closure JSON written; ≥1 accepted row; exactly one `BEST`.
* **A2:** Monotone behavior observed for σ and ξ_Γ in at least one (g, β) line consistent with §9.
* **A3:** Re-runs with the same seed are bit-identical in outputs (deterministic RNG seeding).

# §13 · Implementation Notes (minimal spine)

* The entire map is implemented in pure, side-effect-free functions; parameters live in a single dataclass (`OptionCParams`), and lattice extents in `LatticeSpec`.
* Only the **loader/coercion** touches input JSON. Everything else is typed transforms.
* One place to compute `closure_loss`; one place to emit artifacts.

# §14 · Linkage to V6 (where this sits)

This module concretizes the **non-perturbative bridge** proposed under your YM mapping and experimental annexes (parents above) and supplies the **closure artifact** expected by your QED/QCD experimental modules (children). It is a narrow but high-leverage “spine” that upgrades earlier, more narrative steps to numeric registration and falsifiability inside the existing Volume-6 tree. 

---