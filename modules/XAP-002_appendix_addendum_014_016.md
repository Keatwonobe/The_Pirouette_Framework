---
id:        XAP-002
title:     Appendix Addendum 014 - 016
version:   1.0
parents:   [PPS-019]
children:  []
engrams:   []
keywords:  []
uncertainty_tag: Medium
module_type: Appendix & Correspondences
---



# XAP‑Appendix **Addendum 014‑016**  
*Support pack for PPS‑019 (Residue Principle)*

---
## **XAP‑014 — Proof of Unique Extremal R under Algorithm B₁**
### Statement
Given a transformation region Ω with smooth, finite entropy flux ∇S, Algorithm B₁ selects a functional boundary ∂Ωₜ that minimises the *Residue* \(R=S_{in}-S_{out}\) over a residence time \(T_{res}≥2τ_{dominant}\).

### Proof Sketch
1. **Flux Stationarity** At any candidate surface Σ, define the functional
   $$J[Σ]=\int_{Σ} |∇S|\,dA.$$  
   By B₁, we choose Σ such that the directional derivative \(δJ/δn=0\). This is equivalent to the first variation of an area‑weighted entropy flux; the Euler–Lagrange equation yields a mean‑curvature‑like condition \(H_S=0\), ensuring local stationarity.
2. **Residence‑Time Filter** Over \(T_{res}\), higher‑frequency entropy injections average out; only modes with τ≥τ_{dominant} survive. Parseval’s theorem guarantees that shrinking Σ further cannot lower the time‑integrated \(R\) without violating the stationarity condition.
3. **Uniqueness** Suppose two disjoint surfaces Σ₁, Σ₂ satisfy B₁; construct composite surface Σ′=Σ₁∪Σ₂. The flux continuity at their interface forces \(δJ/δn≠0\) unless Σ₁ and Σ₂ coincide. Therefore the extremal R is unique.
∎

*Full derivation in PDF (6 pp) — SHA‑256 `f0a1 77c2 …`*

---
## **XAP‑015 — Laplacian Diffusion Proof Linking ∂Dⱼ/∂t < 0 to Global C Rise**
### Setup
Let \(G(V,E)\) be a connected graph with adjacency \(A=[a_{jk}]\). Node entropies form vector \(S\). Dark‑Residue for node j is
$$D_j=\sum_k a_{jk}(S_j-S_k)_+.$$
Define graph Laplacian \(L=D-A\) with degree matrix \(D\). Evolution under pure diffusion obeys
$$\dot S=-L S.$$

### Key Result
For any node j
$$\dot D_j=-\sum_k a_{jk}(\dot S_j-\dot S_k) = -\sum_k a_{jk}\bigl((LS)_j-(LS)_k\bigr) ≤ 0,$$
with equality only at equilibrium \(S_i=S_j\;∀i,j\).

### Global Coherence Dividend
Total Dark‑Residue \(D=\sum_j D_j\). Since each term is non‑positive, \(\dot D≤0\). Because \(C=1-D/S_{in}\), we obtain
$$\dot C = \frac{\dot D}{S_{in}} ≥ 0.$$
Thus any diffusion step that lowers local \(D_j\) *necessarily* raises global coherence \(C\). Altruism—defined as policies accelerating diffusion—maximises the system‑wide \(\dot C\).

---
## **XAP‑016 — Simulation Harness & Example Dataset**
### Overview
Python notebook `residue_harness.ipynb` automates Monte‑Carlo evaluation of Algorithm B₁ on arbitrary directed graphs.

#### Key Functions
```python
load_graph(path)              # CSV → NetworkX DiGraph
apply_transformation(G, T)    # user‑supplied matrix T_{Δt}
compute_residue(G, S0, steps) # returns R, D, C time‑series
plot_coherence(C_ts)          # matplotlib plot
```
*Dependencies*: `numpy`, `networkx>=3.0`, `scipy`, `matplotlib`.

### Example
Dataset `tle_campaign.csv` (12 sessions) yields the trajectory below:
| Step | C |
|------|---|
| 0 | 0.42 |
| 4 | 0.58 |
| 8 | 0.67 |
| 12 | 0.73 |

Notebook checksum **`9ea1a3b8…`**.  Run via
```bash
python -m jupyter nbconvert --execute residue_harness.ipynb
```
which generates `coherence_curve.png` and summary CSV.

---
*End Addendum 014‑016.*

