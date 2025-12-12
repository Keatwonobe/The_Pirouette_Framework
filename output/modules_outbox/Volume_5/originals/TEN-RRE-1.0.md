---
id:           TEN-RRE-1.0
title:        Recursive Residue Evaluation
version:      1.0
parents:      []                            # Placeholder: To be filled manually
children:     []                            # Placeholder: To be filled manually
engrams:
  - analytic:pattern-analysis
keywords:     ['after', 'analytical', 'analyze', 'application', 'characterizing', 'coherence']
uncertainty_tag: Medium # Placeholder
module_type:  applied-analytics-toolkit
---

## §1 · Purpose
To iteratively analyze the residual components (leftover coherence, patterns, or 'noise') of a dataset after the application of primary analytical transformations, with the goal of uncovering hidden or nested structures, subtle signals, or characterizing the true nature of unexplained variance.

---

## §2 · Conceptual Anchor
**Theoretical Insight**: After a primary analytical mode extracts dominant signals or structures from a dataset, the remaining 'residue' is not necessarily random or uninformative. This residue can contain secondary coherent patterns, echoes of unmodeled processes, structured noise, or information requiring a different analytical lens. By recursively applying analytical modes to these residues, deeper layers of information, complexity, and the true nature of the system's coherence (or lack thereof) can be unveiled. This aligns with the Pirouette principle that information is conserved and transforms rather than being simply lost as 'noise'.

**Key Pirouette Parameters**:
* **Time-Adherence (Ta)**: The $T_a$ of the original dataset and of each subsequent residue is a critical metric. A residue exhibiting unexpectedly high $T_a$ suggests it contains further coherent information rather than being pure noise. The analysis might continue until the residue's $T_a$ falls below a defined threshold.
* **Gladiator Force (Γ)**: The $\Gamma$ parameter of the system from which the data originates can influence the nature of residues. For example, a high $\Gamma$ system (loosely confined) might produce more complex, diffuse residues. The analysis of residues might also reveal different confinement scales for nested phenomena.
* **Ki Constant (Ki)**: Recursive evaluation of residues might uncover $K_i$-harmonic patterns or symmetries at deeper layers, indicating nested resonant structures that were not apparent in the initial analysis. The $K_i$ constant may also inform the optimal 'rhythm' or depth of recursive steps.

---

## §3 · Input & Configuration
### 3·1 · Input Stream
* **Data Characteristics**: An initial dataset $D_0$ of any type (e.g., time series, field data, parameter map). A defined sequence of one or more Tendu Analytical Modes (or other transformation functions) to be applied iteratively.
* **And Structure**: The initial dataset should be in a format compatible with the first analytical mode in the chosen sequence. Subsequent residues will typically be numerical arrays or data structures of the same type as the output of the preceding analytical mode minus its identified signal.
* **Viable Data Set**: The dataset must be rich enough to potentially contain multiple layers of structure or information beyond what a single analytical pass can capture.
* **Steps**: Standard preprocessing suitable for the *first* analytical mode in the sequence should be applied to the initial dataset $D_0$.

### 3·2 · Operational Parameters
| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| `SequenceOfAnalyticalModes ($M_k$)` | An ordered list or a function that determines which Tendu Analytical Mode (or other transformation) is applied at each recursion level 'k'. This is the core 'lens' used at each step. | `A list of Tendu Module IDs or callable functions.` |
| `ResidueCalculationMethod` | Defines how the residue is calculated after a signal/structure is extracted. Common methods include subtractive ($R_k = D_{k-1} - S_k$) or divisive ($R_k = D_{k-1} / S_k$). | `['Subtractive', 'Divisive', custom function]` |
| `RecursionDepthLimit ($k_{max}$)` | The maximum number of recursive steps to perform. | `Integer, e.g., 3-10, system-dependent.` |
| `ResidueSignificanceThreshold` | A criterion to determine if a residue warrants further analysis or should be considered terminal noise. This could be based on metrics like its $T_a$, energy, variance, entropy, or specific pattern detection. | `E.g., $T_a(R_k) < 0.1$, Variance$(R_k) < 0.01 \cdot$ Variance$(D_0)$.` |

---

## §4 · Procedure & Outputs
### 4·1 · Procedural Guide
1. Initialization: Define $D_{current} = D_0$ (the initial dataset). Set recursion level $k = 0$. Initialize an empty list $S_{extracted}$ to store identified signals/structures and their parameters.
2. Recursive Loop: Iterate while $k < k_{max}$ AND the significance of $D_{current}$ (calculated using `ResidueSignificanceThreshold` criteria) is above the threshold:
3.   a. Increment recursion level: $k = k + 1$.
4.   b. Mode Selection: Select the analytical mode $M_k$ for the current level from `SequenceOfAnalyticalModes` (this could be a fixed sequence or dynamically chosen based on $D_{current}$'s properties).
5.   c. Apply Mode: Apply mode $M_k$ to $D_{current}$. Let this produce an identified signal/structure component $S_k$ and any associated parameters $P_k$.
6.   d. Store Component: Add $\{S_k, P_k, \text{ModeUsed: } M_k\}$ to $S_{extracted}$.
7.   e. Calculate New Residue: Compute $D_{next\_residue}$ using the chosen `ResidueCalculationMethod`, e.g., $D_{next\_residue} = D_{current} - S_k$.
8.   f. Update Current Data: Set $D_{current} = D_{next\_residue}$.
9. Termination: Once the loop terminates, the final $D_{current}$ is the terminal residue, $D_{terminal\_residue}$.
10. Output Compilation: The complete output consists of the list $S_{extracted}$ and the $D_{terminal\_residue}$ with its characteristics.

### 4·2 · Output Interpretation
* **Data Structure**: A structured list of extracted signal/structure components $\{S_k, P_k, M_k\}$ for each recursion level $k$. The final terminal residue $D_{terminal\_residue}$ and its characterization (e.g., noise profile, entropy, $T_a$).
* **Insights And Derivations**: Uncovering signals or patterns that were masked by more dominant components. Characterizing the nature of what is typically considered 'noise' – determining if it's truly random or contains unmodeled structures. Identifying hierarchical or nested patterns within the data. Assessing the completeness of primary analytical models (a model is more complete if its residue is closer to true noise). Revealing subtle influences or secondary causal factors.
* **Guidelines**: Each $S_k$ represents a layer of structure found in the data. The sequence of $M_k$ used indicates the types of structures present at different layers. A $D_{terminal\_residue}$ with very low $T_a$ and high entropy suggests that most discernible coherence has been extracted. If $D_{terminal\_residue}$ still shows structure, the `RecursionDepthLimit` or `ResidueSignificanceThreshold` might need adjustment, or a different analytical mode might be required.

---

## §5 · Core Equations
### Residue Calculation (Subtractive Example)
$$ R_k = D_{k-1} - S_k(D_{k-1}) $$
Calculates the $k^{th}$ residue $R_k$ by subtracting the signal/structure $S_k$ (identified by applying an analytical mode to the previous residue $D_{k-1}$) from $D_{k-1}$.

### Residue Significance Metric (Example using Ta)
$$ \text{Significance}(R_k) = T_a(R_k) $$
A metric to evaluate if a residue $R_k$ contains further coherence. Recursion stops if $T_a(R_k) < \text{Threshold}_{Ta}$.

### Iterative Application of Analytical Mode $M_k$
$$ S_k, P_k = M_k(D_{k-1}) $$
Symbolic representation of applying the $k^{th}$ analytical mode $M_k$ to the $(k-1)^{th}$ residue (or initial data for $k=1$) to extract signal $S_k$ and parameters $P_k$.

---

## §6 · Assemblé
This module transforms data into insight by quantifying a core system property according to Pirouette Framework principles.

---

## §7 · Integration & Use Cases
### 7·1 · Integration Hooks
* **Dependencies**: An initial dataset $D_0$. A defined (or dynamically definable) sequence of Tendu Analytical Modes or other transformation functions.
* **Applications**: The extracted components $S_k$ can be analyzed individually or used to build a more comprehensive multi-layer model of the original system. The $D_{terminal\_residue}$ can be subjected to statistical tests for randomness or further characterized as a specific type of structured noise.

### 7·2 · Use Cases
* Advanced signal processing: Separating multiple layered or interfering signals (e.g., geophysical data, complex audio signals).
* Deep data analysis: Finding subtle trends or anomalies after removing primary seasonal or cyclical components.
* Cognitive science: Modeling hierarchical processing in perception or language, where each stage processes the residue of the previous.
* System diagnostics: Identifying secondary or cascading faults after primary faults are accounted for.
* Creative content analysis: Deconstructing complex artistic works (e.g., music, literature) into layers of structural, thematic, or influential components.
* Financial market analysis: Identifying higher-order dependencies or subtle arbitrage opportunities after primary market models are applied.

---

### Version Notes
*1.0* — Initial conversion from JSON definition.
