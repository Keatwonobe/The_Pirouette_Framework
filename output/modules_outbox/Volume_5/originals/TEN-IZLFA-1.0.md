---
id:           TEN-IZLFA-1.0
title:        Inverse Zipf/Power-Law Fitting Analysis
version:      1.0
parents:      []                            # Placeholder: To be filled manually
children:     []                            # Placeholder: To be filled manually
engrams:
  - analytic:pattern-analysis
keywords:     ['analysis', 'coverage', 'data', 'desired', 'determines', 'distribution']
uncertainty_tag: Medium # Placeholder
module_type:  applied-analytics-toolkit
---

## §1 · Purpose
Given observed frequency data or a desired statistical property (like tail coverage), this module determines the exponent α and other parameters of the underlying power-law (Zipfian) distribution.

---

## §2 · Conceptual Anchor
**Theoretical Insight**: Power-law distributions are ubiquitous in complex systems and describe phenomena where a small number of items have high frequency/rank and a 'long tail' of items has low frequency/rank. This module solves the inverse problem: inferring the law from the data. It is the core characterization engine for Pirouette's Reverse Pareto Analysis, which analyzes the stabilizing effects of such distributions. The exponent α is a critical measure of concentration and inequality in a system.

**Key Pirouette Parameters**:
* **Reverse Pareto Analysis**: This module provides the core fitting mechanism for Reverse Pareto Analysis (TEN-RPA-1.0). The exponent α is the key parameter that RPA interprets in the context of systemic stability.

---

## §3 · Input & Configuration
### 3·1 · Input Stream
* **Data Characteristics**: Empirical data suitable for rank-frequency analysis, or a set of desired statistical properties for the distribution.
* **And Structure**: A list of observed frequencies $\{x_i\}$, or target values for properties like tail coverage $\beta$ and cutoff rank $k$.
* **Viable Data Set**: A dataset with a sufficient number of points to establish a distribution, especially in the tail, for reliable fitting.
* **Steps**: Rank-ordering of data items by frequency. Optional log-transformation for visualization and preliminary regression fitting.

### 3·2 · Operational Parameters
| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| `α` | The power-law exponent, which can be fixed or estimated. | `real > 1` |
| `β` | Desired tail-coverage fraction. | `real in (0,1)` |
| `N` | Maximum rank in the support of the distribution. | `integer` |
| `k` | Cut-off rank for tail calculation, which can be fixed or solved for. | `integer` |
| `x_min` | Lower bound for data included in Maximum Likelihood Estimation. | `real` |

---

## §4 · Procedure & Outputs
### 4·1 · Procedural Guide
1. Exponent Estimation: Given observed data $\{x_i\}$, estimate the exponent $\hat{\alpha}$ using the Maximum Likelihood Estimation (MLE) formula.
2. Tail-Coverage Inversion: Given a target coverage $\beta$ and a known $\alpha$, find the smallest rank $k$ such that the cumulative probability from rank $k$ to $N$ is at least $\beta$.
3. Parameter-Coverage Mapping: Given a target coverage $\beta$ and a cutoff rank $k$, solve the equation $F(\alpha) = \sum_{r=k}^{N} r^{-\alpha} - \beta\sum_{i=1}^{N}i^{-\alpha} = 0$ for $\alpha$ using numerical root-finding methods.

### 4·2 · Output Interpretation
* **Data Structure**: The estimated power-law exponent $\hat{\alpha}$ and normalization constant C, or the parameters ($k$, $\alpha$) that satisfy the input constraints.
* **Insights And Derivations**: A quantitative measure of the 'heavy-tailedness' or concentration within a system. This helps in understanding risk, influence, and resource allocation patterns.
* **Guidelines**: The exponent $\alpha$ quantifies the steepness of the rank-frequency distribution. A value near 1 implies extreme concentration (a few items dominate), while a larger value indicates a more even distribution.

---

## §5 · Core Equations
### Power-Law (Zipfian) Distribution
$$ f(r) = \frac{C}{r^{\alpha}}, \quad C = \biggl(\sum_{r=1}^{N}r^{-\alpha}\biggr)^{-1} $$
The probability mass function for a discrete power-law distribution of rank 'r' with exponent α.

### Maximum Likelihood Estimator for α
$$ \hat\alpha = 1 + n\biggl[\sum_{i=1}^n\ln\frac{x_i}{x_{\min}}\biggr]^{-1} $$
The formula for estimating the power-law exponent from n data points $\{x_i\}$ with a lower bound $x_{min}$.

### Tail-Coverage Condition
$$ \sum_{r=k}^{N} \frac{r^{-\alpha}}{\sum_{i=1}^{N}i^{-\alpha}} \;\ge\;\beta $$
The condition to find the cutoff rank 'k' for a desired tail coverage fraction $\beta$.

---

## §6 · Assemblé
This module transforms data into insight by quantifying a core system property according to Pirouette Framework principles.

---

## §7 · Integration & Use Cases
### 7·1 · Integration Hooks
* **Dependencies**: Requires rank-frequency data.
* **Applications**: This module is the core computational engine for `TEN-RPA-1.0` (Reverse Pareto Analysis). Its outputs are used to characterize distributions in economics, linguistics, network science, and other domains of complex systems.
* **With Combined Workflows**: Integrates directly with TEN-RPA-1.0.

### 7·2 · Use Cases
* Modeling and analyzing word frequencies in a text corpus.
* Characterizing the distribution of city populations.
* Analyzing wealth and income distributions in economics.
* Modeling the degree distribution of nodes in scale-free networks.
* Quantifying hidden leverage and risk in long-tail phenomena.

---

### Version Notes
*1.0* — Initial conversion from JSON definition.
