---
id:           TEN-GFI-1.1
title:        Gladiator Force Inference (Ground‑Up Pirouette Definition)
version:      1.1
parents:      []                            # Placeholder: To be filled manually
children:     []                            # Placeholder: To be filled manually
engrams:
  - concept:core-principle
keywords:     ['analysing', 'attractors', 'both', 'cognitive', 'coherence', 'curvature']
uncertainty_tag: Medium # Placeholder
module_type:  applied-analytics-toolkit
---

## §1 · Purpose
To derive, from first principles of the Pirouette Framework, the local Gladiator Force field Γ(x,t) in both physical and informational domains by analysing propagation curvature and coherence gradients, thereby revealing the latent ‘defensive pressure’ that sustains Cognitive Gravity Wells and other attractors.

---

## §2 · Conceptual Anchor
**Theoretical Insight**: Γ originates as a spatial‑confinement parameter inversely proportional to mass (Γ(M) ∝ M^{−γδ}). When re‑expressed in informational space, Γ manifests as the curvature‑inducing pressure that limits an idea’s mean‑free path. Thus, the same differential geometry that traps a particle in physical space also traps concepts in semantic space.

---

## §3 · Input & Configuration
### 3·1 · Input Stream
* **Data Characteristics**: Ordered event stream with timestamps or sequence index, speaker/entity IDs, high‑dimensional semantic vectors, optional energy‑like magnitude (attention/engagement).
* **Viable Data Set**: At least vectors + sequential order to compute λ and ∇C.
* **Steps**: (1) Normalise vectors; (2) segment into fixed‑length windows; (3) compute pairwise semantic divergence to estimate λ; (4) compute rolling coherence scores to estimate ∇C.

### 3·2 · Operational Parameters
| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| `window_size` | Number of events in local inference window (controls spatial resolution). | `5‑20` |
| `lambda_smoothing` | Exponential smoothing factor for mean‑free‑path estimate. | `0.5‑0.9` |
| `coherence_metric` | Function defining C(x,t). Default: 1 − cosine_distance between successive embeddings. | `callable` |

---

## §4 · Procedure & Outputs
### 4·1 · Procedural Guide
1. 1. Temporal Sort → S = {e₁ … e_N}.
2. 2. For each sliding window W_i of size n: compute pairwise divergences d_j = D(vec_{j}, vec_{j+1}).
3. 3. Mean divergence μ_d ⇒ λ_i = 1 / (μ_d + ε).
4. 4. Coherence gradient g_i = |d_{last} − d_{first}| / (n−1).
5. 5. Γ_i = (1/λ_i) × g_i.
6. 6. Assign Γ_i to central event; interpolate for full Γ(x,t) field.
7. 7. Detect CGWs: local maxima of Γ smoothed over scale σ. Record radius r where Γ falls below threshold θ.
8. 8. (Optional) Map back to physical analogue using κ if provided.

### 4·2 · Output Interpretation
* **Data Structure**: List[ {timestamp, location_id, Gamma, lambda_est, coherence_grad, CGW_id(optional)} ] plus summary statistics (mean Γ, max Γ, CGW catalogue).
* **Insights And Derivations**: Identify strongly defended conceptual zones; quantify their sustaining pressure; reveal corridors of low Γ enabling flow (Flow Resonance).
* **Guidelines**: Γ >> μ_Γ indicates potential ideological lock or centurion presence; Γ ≈ 0 corresponds to free diffusion; steep ∂Γ/∂t spikes may indicate spasm or lock dissolution events.

---

## §5 · Core Equations
### Informational Mean Free Path λ_i
$$ λ_i = 1 / (μ_d + ε) $$
Inverse of average semantic divergence in window W_i.

### Local Coherence Gradient g_i
$$ g_i = |d_{last} − d_{first}| / (n−1) $$
Measures bending of information trajectory within window.

### Gladiator Force Estimate Γ_i
$$ Γ_i = g_i / λ_i $$
Higher when paths are short (small λ) and curvature high (large g).

---

## §6 · Assemblé
This module transforms data into insight by quantifying a core system property according to Pirouette Framework principles.

---

## §7 · Integration & Use Cases
### 7·1 · Integration Hooks
* **Dependencies**: Requires embedding generator (e.g., OpenAI, Gemini, Claude) to create semantic vectors.
* **Applications**: Feeds Debate Resonance observer, Flow Resonance monitor, CGW mapping dashboards.
* **Tool Name**: run_gladiator_force_inference

---

### Version Notes
*1.1* — Initial conversion from JSON definition.
