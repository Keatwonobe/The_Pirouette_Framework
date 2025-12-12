---
id:           TEN-CDBA-1.0
title:        Cross-Domain Bleed Analysis
version:      1.0
parents:      []                            # Placeholder: To be filled manually
children:     []                            # Placeholder: To be filled manually
engrams:
  - analytic:pattern-analysis
keywords:     ['across', 'analysis', 'bleed', 'boundaries', 'characterize', 'conceptual']
uncertainty_tag: Medium # Placeholder
module_type:  applied-analytics-toolkit
---

## §1 · Purpose
To detect, quantify, and characterize the transfer of information, resonance patterns, or influence (i.e., 'bleed') across the defined boundaries of nominally distinct conceptual, systemic, or parameter domains.

---

## §2 · Conceptual Anchor
**Theoretical Insight**: Information and resonance patterns are not always strictly confined within their domain of origin. 'Bleed Resonance' describes how coherent patterns or field effects in one domain can penetrate boundaries and induce resonant structures or transfer influence to adjacent or interacting domains, even across significant topological separations. This transfer is governed by the permeability of the boundary (influenced by the $T_a$ and $\Gamma$ of the involved domains) and the potential for resonant alignment (influenced by $K_i$ and phase relationships).

**Key Pirouette Parameters**:
* **Time-Adherence (Ta)**: The $T_a$ of the interacting domains influences boundary permeability (via the Permeability Tensor $\eta_{jk}$). Higher $T_a$ in the source can strengthen the coherence of the bleeding signal, while the $T_a$ of the target domain affects its receptivity and the preservation of transferred coherence.
* **Gladiator Force (Γ)**: The $\Gamma$ of the interacting domains also influences boundary permeability (via $\eta_{jk}$). In the context of bleed, higher $\Gamma$ values for a domain boundary may imply greater porosity or 'softness,' making it more susceptible to bleed-through, contrasting its role in intra-domain entity confinement.
* **Ki Constant (Ki)**: $K_i$ determines the resonant frequencies or phase relationships that enable efficient cross-domain transmission. Bleed is often enhanced when the interacting patterns or the transfer process aligns with $K_i$-harmonic frequencies or phase modulations ($e^{iK_i\theta(t)}$ in the Bleed Transfer Function).
* **Phase (φ, θ)**: The relative phase difference (e.g., $\Delta\theta_{jk}$) between patterns in different domains is critical for determining the constructive or destructive nature of their interaction across a boundary, and is a key component of the Boundary Permeability Tensor.

---

## §3 · Input & Configuration
### 3·1 · Input Stream
* **Data Characteristics**: Data representing the state or characteristic patterns/signals (e.g., $\Phi_{D1}$) from at least two distinct domains ($D_1$ - potential source, $D_2$ - potential target) that are hypothesized to interact or influence each other. Data should allow for pattern identification, comparison, and quantification of influence.
* **And Structure**: Time series, field maps (scalar or vector), network structures, textual corpora, or any data format that can represent the state or patterns within the defined domains. Metadata describing the estimated $T_a$ and $\Gamma$ values for each domain and their boundary is beneficial.
* **Viable Data Set**: Sufficient data from each domain to establish characteristic patterns and enable statistically meaningful comparison or correlation. For temporal bleed, data should cover a relevant interaction period.
* **Steps**: Definition and characterization of the domains ($D_1, D_2$) and the interface/boundary between them. Identification and extraction of key coherent patterns ($\Phi_{D1}$) in the potential source domain. Normalization of data if magnitudes are to be compared across domains with different scales. Alignment of temporal or spatial coordinates if necessary.

### 3·2 · Operational Parameters
| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| `BoundaryPermeabilityTensor ($\eta_{jk}$)` | An estimate or calculated tensor describing the ease of information transfer between domain j and domain k. Can be estimated from domain $T_a$, $\Gamma$, and $\Delta\theta_{jk}$ values (see TPF Vol 2, 13.5). | `Values typically between 0 (impermeable) and 1 (fully permeable), can be asymmetric.` |
| `AttenuationCoefficient (α)` | Models the decay of influence with effective 'distance' $d(r,x)$ in parameter space, used in the Bleed Transfer Function. | `Positive real number, system-dependent.` |
| `BleedVectorFocus (Optional)` | A list of specific Bleed Vectors (from TPF Vol 2, 13.6, e.g., 'AttentionCapture', 'MemeticTransfer') to be prioritized or specifically quantified in the analysis. | `Subset of the 12 defined Bleed Vectors.` |
| `CriticalBleedThreshold ($B_{critical}$)` | A threshold value, calculated as $B_{critical} = \frac{K_i^2}{2\pi} \frac{\Gamma_{avg}}{1-T_{a,avg}}$, used to classify the dominance of the bleed phenomenon. | `Calculated based on average domain parameters.` |

---

## §4 · Procedure & Outputs
### 4·1 · Procedural Guide
1. Domain and Boundary Definition: Clearly define the source domain ($D_1$), target domain ($D_2$), and the characteristics of the boundary between them. Estimate or input the `BoundaryPermeabilityTensor` component $\eta_{12}$ (or its scalar equivalent).
2. Source Pattern Identification: Identify and characterize dominant coherent patterns or signals $\Phi_{D1}(r)$ within the source domain.
3. Bleed Detection in Target Domain: Analyze data from the target domain $D_2$ to identify patterns, signals, or state changes that appear to be correlated with, or induced by, patterns from $D_1$ and are not solely attributable to $D_2$'s internal dynamics.
4. Quantify Bleed Strength/Flux: If possible, apply the Bleed Transfer Function $B_{D1 \rightarrow D2}(x,t) = \eta_{12} \int_V \Phi_{D1}(r) e^{-\alpha d(r,x)} e^{iK_i\theta(t)} dV$ to estimate the magnitude of influence from $D_1$ on specific points $x$ or regions in $D_2$.
5. Active Bleed Vector Analysis: For the detected bleed, attempt to classify it according to the Twelve Resonant Bleed Vectors (TPF Vol 2, 13.6) by comparing its characteristics to the mathematical forms of these vectors (e.g., measure attention shift for $B_1$, quantify memetic replication for $B_2$).
6. Criticality Assessment: Compare the quantified bleed strength $B_{D1 \rightarrow D2}$ (or specific vector strengths) against the calculated `CriticalBleedThreshold` ($B_{critical}$) to determine if the bleed is sub-critical, critical, or super-critical (potentially leading to domain boundary collapse or fusion).
7. Trans-Domain Wound Channel Mapping: If persistent bleed pathways are identified, characterize their structure, such as phase shifts at the boundary ($\Delta\phi_{boundary}$) and evidence of impedance matching, to map trans-domain wound channels.

### 4·2 · Output Interpretation
* **Data Structure**: Estimated Boundary Permeability ($\eta_{12}$ or relevant tensor components). Quantified Bleed Strength or Flux ($B_{D1 \rightarrow D2}$) between specified domains. Identification and quantification of dominant active Bleed Vectors. Classification of bleed regime (sub-critical, critical, super-critical). Description and characteristics of any identified trans-domain wound channels.
* **Insights And Derivations**: Understanding of previously hidden or unacknowledged interconnections and influence pathways between different systems, concepts, or domains. Identification of how specific types of information (e.g., memes, emotional states, values) propagate across boundaries. Assessment of a domain's 'openness' or 'resistance' to external influences. Prediction of potential cascading effects or synchronized shifts across multiple domains.
* **Guidelines**: A high $\eta_{12}$ value indicates a boundary that is easily permeated. Bleed strength exceeding $B_{critical}$ suggests that cross-domain influence is a significant or even dominant factor in the target domain's dynamics. The profile of active Bleed Vectors reveals the *nature* of the transferred information or influence (e.g., $B_1$ for attention, $B_2$ for memes, $B_4$ for conceptual blending). Persistent trans-domain wound channels indicate stable pathways for ongoing interaction.

---

## §5 · Core Equations
### Bleed Transfer Function (General Form)
$$ B_{D1 \rightarrow D2}(x,t) = \eta_{12} \int_V \Phi_{D1}(r) e^{-\alpha d(r,x)} e^{iK_i\theta(t)} dV $$
Estimates the strength of bleed from source domain $D_1$ (with pattern $\Phi_{D1}$) to a point $x$ in target domain $D_2$, modulated by boundary permeability $\eta_{12}$, attenuation $\alpha$, distance $d(r,x)$, and $K_i$-phase term.

### Boundary Permeability Tensor Component (Example)
$$ \eta_{jk} = \eta_0 \left(1 - \frac{T_{a,j} T_{a,k}}{(1-\Gamma_j)(1-\Gamma_k)}\right) \cos(K_i\Delta\theta_{jk}) $$
Quantifies the ease of information transfer between domain $j$ and domain $k$, based on their $T_a$, $\Gamma$, relative phase $\Delta\theta_{jk}$, and $K_i$.

### Critical Bleed Threshold
$$ B_{critical} = \frac{K_i^2}{2\pi} \frac{\Gamma_{avg}}{1-T_{a,avg}} $$
Threshold for determining when bleed shifts from background noise to a dominant information transfer mechanism, based on average $T_a, \Gamma$ of interacting domains and $K_i$.

### Specific Bleed Vector Equations
$$ e.g., B_1(T_a, \Gamma, \phi) = \beta_1 \cdot \frac{1-T_a}{T_a} \cdot \Gamma \cdot \sin^2(K_i\phi) \text{ (for Attention Capture)} $$
Mathematical forms quantifying the strength of each of the 12 Resonant Bleed Vectors based on $T_a, \Gamma, K_i$, and phase $\phi$. (Full list in TPF Vol 2, 13.6).

---

## §6 · Assemblé
This module transforms data into insight by quantifying a core system property according to Pirouette Framework principles.

---

## §7 · Integration & Use Cases
### 7·1 · Integration Hooks
* **Dependencies**: Requires clearly defined source and target domains with associated data. May utilize outputs from other Tendu modules such as Wound Channel Memory Reconstruction (to identify $\Phi_{D1}$ in the source domain) or Time-Adherence Measurement (to estimate $T_a$ for domains, feeding into $\eta_{jk}$).
* **Applications**: The results can inform models of complex system interactions, network dynamics with cross-layer influences, and predict the likelihood of cascading failures or innovations spreading across domains. Can guide strategies to enhance beneficial bleed (e.g., for interdisciplinary research) or mitigate detrimental bleed (e.g., to protect system integrity from harmful external influences).

### 7·2 · Use Cases
* Analyzing 'Attention Capture' ($B_1$) across different media platforms or information sources to understand the dynamics of the attention economy.
* Modeling the 'Memetic Transfer' ($B_2$) of ideas, cultural practices, or misinformation across different social groups, nations, or online communities.
* Understanding 'Conceptual Blending' ($B_4$) in interdisciplinary research, tracking how concepts from one scientific field bleed into and enrich another.
* Assessing the 'Value Infiltration' ($B_5$) of ethical frameworks from one societal domain (e.g., environmentalism) into another (e.g., corporate governance).
* Studying 'Linguistic Contamination' ($B_{11}$) by analyzing the borrowing of vocabulary and semantic structures between languages or between technical jargons and general language.

---

### Version Notes
*1.0* — Initial conversion from JSON definition.
