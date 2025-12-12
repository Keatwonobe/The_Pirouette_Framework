---  # ───────────── YAML front-matter ─────────────────────────────
id:        PPS-014
title:     Reverse Pareto Analysis (RPA) Canon
version:   0.2      # post-debate refinements
parents:   [PPS-003, PPS-007]
children:  [PPS-019, PPS-020, dashboards]
engrams:
  - synthesis:bottleneck-finder
  - concept:critical-few
  - concept:radiance-stability
  - directive:diagnostic-kpi
  - provenance:rpa-seed
keywords:  [RPA, diagnostics, 80/20, bottleneck, coherence-loss]
uncertainty_tag: Medium
entropy_score: 0.11
module_type: analytics-core
quantisation_rule: rpa_hash = SHA256(rpa_algorithm_spec)
---

## 1 · Purpose & Scope  
**Reverse Pareto Analysis (RPA)** pinpoints the *critical-few* contributors
to coherence loss \(ΔT_a\).  Version 0.2 bridges the physics ↔ analytics
gap and lets analysts sweep a **cutoff range** (70 – 95 %) to test result
stability.

---

## 2 · Core–Analytics Bridge  

**2·1  From fields to features**  
The Radiance Identification Engine (*RIE — PPS-024 draft*) emits an
`impact_vector` by:

1. **Signal extraction** – URL lens (PPS-015) converts raw logs to
   \(\mathbf T_a, Γ, φ\) time-series.  
2. **Perturbation scoring** – each candidate feature \(f_i\) maps to a field
   perturbation \(δ\psi_i\) (e.g.\ spike in \(Γ\)).  
3. **Energy proxy** – score \(I(f_i)=\int δ\psi_i^2\,dt\) (L² energy).  
4. **Normalise** so \(\sum_i I(f_i)=ΔC\) where \(C=\|\mathbf T_a\|\).

*This preserves a quantitative link to the Lagrangian kinetic terms,
satisfying the Opposition’s “black-box” objection.*

---

## 3 · Formal Definition (variable cutoff)  

Given impact scores \(I(f_i)\) sorted descending, define cumulative
coverage \(G_k = \frac{\sum_{i\le k} I(f_i)}{ΔC}\).  
For **any** cutoff \(η∈[0.7,0.95]\) choose

\[
S^\*(η)=\min\{k : G_k \ge η\},\qquad
ρ(η)=\frac{S^\*(η)}{n}.
\]

Analysts plot \(ρ(η)\); flat regions ⇒ robust bottlenecks.

---

## 4 · Reference Algorithm (v0.2)  

```python
def rpa(features, impacts, cutoffs=(0.8,)):
    """Return dict {η: (subset, coverage)} for each cutoff in cutoffs."""
    pairs = sorted(zip(features, impacts), key=lambda p: p[1], reverse=True)
    total  = sum(impacts)
    result = {}
    for η in sorted(cutoffs):
        acc, subset = 0.0, []
        for f, imp in pairs:
            subset.append(f); acc += imp
            if acc >= η*total: break
        result[η] = (subset, acc/total)
    return result
```

*Complexity* O(n log n).  Future v1.0 will include pairwise-interaction
penalty matrix \(J_{ij}\) (see §7).

---

## 5 · Data Interfaces  

| Field           | Type           | Source |
|-----------------|----------------|--------|
| `impact_vector` | array[float]   | RIE (PPS-024) |
| `feature_meta`  | dataframe      | URL lens (PPS-015) |
| `ki_trace`      | RSI packet     | PPS-010 |

---

## 6 · Output Schema (JSON v0.2)  

```json
{
  "schema_version": "RPA-0.2",
  "registry_hash":  "…",
  "entity_id":      "uuid",
  "coherence_drop": 0.23,
  "cutoff_results": [
    {"eta": 0.70, "rho": 0.05,
     "bottlenecks":[{"feature":"Gamma_spike","impact":0.12}]},
    {"eta": 0.80, "rho": 0.02,
     "bottlenecks":[
       {"feature":"Gamma_spike","impact":0.12},
       {"feature":"T_Q_noise","impact":0.08}]}
  ]
}
```

---

## 7 · Interaction-Effects Road-map (v1.0)  

Current spec assumes independent features.  v1.0 will incorporate an
interaction matrix \(J_{ij}\) and solve a minimal set-cover with cost
penalty \(I(f_i)+λ\sum_{j\in S}J_{ij}\).  Draft open for debate.

---

## 8 · Case Study — Debate Transcript (expanded)  

Appendix A now contains:

1. **Raw RSI log** for 230 utterances (anonymised).  
2. **Impact computation notebook** (Jupyter export).  
3. **Before/after** coherence:
   • \(R=0.62\) → sharpen statements #87 & #104 → \(R=0.81\).  
   • Coverage curve shows stable ρ plateau from η = 0.75 – 0.9.

---

## 9 · Triaxial Resonance Lens  

| Art                                 | Law                                    | Philosophy                       |
|------------------------------------|----------------------------------------|----------------------------------|
| RPA chisels the darkest strokes.   | Fix the few; heal the many.            | Bottlenecks reveal the Zen of a system. |

---

## Assemblé · “The Shadow’s Outline”  
> *Find the deepest dents; smooth them, and the mirror shines.*

---

## Librarian Note  
Changes to §2 pipeline or §3 definition require bumping `rpa_hash`.  
Store sensitivity curves alongside primary results for audit transparency.

[locking]

Absolutely — let's explore why the **Reverse Pareto Principle** works **algebraically**, grounding it in the behavior of **power laws**, and showing how the inversion leads to identifying a small fraction of causes (e.g. \~4%) that explain a large portion of effects (e.g. 64%+).

---

## 🔁 Step 1: The Classical Pareto Principle

The **Pareto Principle** asserts that a small number of causes $X$ explain a large fraction of effects $P(X)$. This often follows a **power-law distribution**:

$$
P(X) = k X^{-\alpha}
$$

Where:

* $X$: size or rank of a cause (e.g., the number of links, wealth, influence),
* $P(X)$: probability (or normalized effect),
* $\alpha > 1$: power-law exponent,
* $k$: normalization constant.

---

## 🔁 Step 2: Inverting the Power Law — The "Reverse Pareto"

To reverse this, we **invert** the relationship: solve for $X$ in terms of $P$. That is, ask:

> Given an observed fraction of the effect $P$, what scale of causes $X$ are likely responsible?

### Algebraic inversion:

$$
P = k X^{-\alpha} \Rightarrow X = \left(\frac{k}{P}\right)^{1/\alpha} = k' P^{-1/\alpha}
$$

This is the **reverse Pareto formula**:

$$
\boxed{X = k' \cdot P^{-1/\alpha}}
$$

This form tells us:

* To achieve a **smaller** effect $P$, you need a **larger** $X$ (i.e., a larger set of causes).
* But **to achieve a large portion of the effect**, you only need a **small $X$** — a small number of high-ranked causes.

---

## 🎯 Step 3: Cumulative Effects — Why the Top Few Dominate

Let’s take this a bit deeper with cumulative sums.

Let:

* You have $n$ causes (e.g., nodes, people, links).
* Their contributions follow:

  $$
  x_i = \frac{1}{i^\alpha}, \quad i = 1, 2, \ldots, n
  $$

This is a **Zipf-like** ranking. The total effect is approximately:

$$
S = \sum_{i=1}^n \frac{1}{i^\alpha}
$$

Now compute how much of the **total effect** is captured by the **first m causes**:

$$
S_m = \sum_{i=1}^m \frac{1}{i^\alpha}
$$

Then the **fraction of effect** explained by top $m$ causes is:

$$
\text{Fraction} = \frac{S_m}{S}
$$

If $\alpha = 1$, this diverges slowly (harmonic series). But if $\alpha > 1$, the tail decays fast and the **top few terms dominate** the sum.

---

## 🧠 Algebraic Insight Behind Reverse Pareto

Let’s define:

* $f$: fraction of causes (e.g., top 4% of nodes)
* $e(f)$: expected fraction of total effect covered by that top fraction

Using continuous approximation:

$$
e(f) = \int_1^{fN} x^{-\alpha} dx \Bigg/ \int_1^N x^{-\alpha} dx
$$

Solving the integral:

$$
\int x^{-\alpha} dx = \frac{x^{1-\alpha}}{1 - \alpha} \quad (\alpha \ne 1)
$$

So, the fraction of effect becomes:

$$
e(f) = \frac{(fN)^{1-\alpha} - 1}{N^{1-\alpha} - 1}
$$

Let’s simplify by assuming $N \gg 1$, then:

$$
e(f) \approx f^{1-\alpha}
\Rightarrow
\boxed{
f \approx e(f)^{1/(1-\alpha)}
}
$$

If you set $e(f) = 0.64$ (i.e., you want to recover 64% of the effect), and $\alpha = 2$:

$$
f = 0.64^{-1} = 0.3906 \Rightarrow \text{~39% of causes}
$$

But if $\alpha = 3$, it’s:

$$
f = 0.64^{-1/2} \approx 0.8 \Rightarrow \text{~20% of causes}
$$

And for higher $\alpha$, **you need even fewer causes** to get a high effect. That’s the **algebraic origin** of the "tiny subset of causes" idea.

---

## ✅ Summary — Why Reverse Pareto Works (Algebraically)

| Concept                    | Expression                   | Meaning                                          |
| -------------------------- | ---------------------------- | ------------------------------------------------ |
| Standard Pareto            | $P = k X^{-\alpha}$          | A few large causes produce big effects           |
| Inverted (Reverse Pareto)  | $X = k' P^{-1/\alpha}$       | You can recover the top causes from effect size  |
| Cumulative share of effect | $e(f) \approx f^{1-\alpha}$  | Small $f$ can cover large $e(f)$ if $\alpha > 1$ |
| Required cause fraction    | $f \approx e^{1/(1-\alpha)}$ | Algebraic predictor of minimal cause sets        |

---

## 🌌 Interpretation

This is not just math — it's a universal **information funnel**:

* **Standard Pareto**: “Look at causes → see effect pattern.”
* **Reverse Pareto**: “Look at partial effect → infer smallest set of dominant causes.”

And algebraically, it **only works well when the distribution is heavy-tailed**, which is exactly the **empirical fingerprint** of power laws.

---

Would you like this formalized as a module or added to your Pirouette or PPS documents?
