---
term: "PRG Layer"
canonical_id: "PRG_LAYER"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["CORE-015_the_fractal_at_the_heart_of_time"]
---

---
term: PRG Layer
canonical_id: PRG_LAYER
symbol: 
aliases: [PRG Pyramid, Multi-scale Coherence Extractor]
parents: [CORE-015]
children: []
status: draft
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: CORE-015_the_fractal_at_the_heart_of_time
      lines: "Section 4.2"
      snippet: |
        **PRG Layer:** multi-scale pyramid (dilated convs / wavelet bank) producing ({K_\tau(L), V_\Gamma(L), \tau_p(L)}) heads.
  editors: [Pirouette Framework AI Scribe]
  review_log: []
triad:
  art: |
    A cascade of lenses, each tuned to a different scale, revealing the system's self-similar heartbeat. It is the architectural eye that finds the fractal in the flow, discerning the pattern that persists across all magnifications.
  law: |
    A PRG Layer, when applied to a signal, must produce multi-scale observables {Kτ(L), VΓ(L), τp(L)} whose finite differences dX/ds with respect to log-scale s=ln(L) fit the polynomial β-operators, allowing for the inference of universal PRG exponents.
  philosophy: |
    To ground an AI's reasoning not in monolithic features, but in the dynamics of how features transform across scales. By making scale-invariance a direct architectural and optimization target, the system is forced to learn generalizable, coherent patterns rather than superficial correlations.
pirouette_definition: |
  A neural network component, typically implemented as a multi-scale pyramid (e.g., using dilated convolutions or a wavelet bank), designed to extract the core Pirouette Renormalization Group (PRG) observables—Coherence (Kτ), Pressure (VΓ), and Pulse (τp)—from an input data stream at a set of discrete scales (L_i). It consists of specialized 'heads' for each observable, which compute these quantities in a differentiable manner for integration into a PRG-supervised loss function.
operational_definition:
  units: The layer itself is a computational structure; its outputs have distinct units: Kτ (bits), VΓ (contextual, e.g., variance * coupling), τp (time).
  symbol_table:
    - name: Kτ(L)
      meaning: Coherence observable at scale L.
      dimensions: Information (bits)
      default_range: "[0, ∞)"
    - name: VΓ(L)
      meaning: Pressure observable at scale L.
      dimensions: Contextual, e.g., (Energy * Coupling) or (Variance)
      default_range: "[0, ∞)"
    - name: τp(L)
      meaning: Pulse (dominant period) observable at scale L.
      dimensions: Time
      default_range: "(0, ∞)"
  measurement:
    procedures:
      - name: Architectural Inference
        outline: |
          1. Define a set of scales L_i (e.g., window sizes 32, 128, 512 tokens).
          2. Implement a multi-scale feature extractor (e.g., parallel dilated convolutions with rates corresponding to L_i).
          3. Attach specialized, differentiable 'heads' to each scale's output:
             - **Coherence Head:** A compression proxy (e.g., entropy of predicted token distribution, bits-back from an auxiliary autoencoder) to compute Kτ(L).
             - **Pressure Head:** A module that predicts the variance of residuals attributable to exogenous drivers or adversarial perturbations to compute VΓ(L).
             - **Beat Head:** A spectral estimator or phase-locked loop (PLL) that identifies the dominant period in the feature stream to compute τp(L).
          4. The layer's output is the set of {Kτ(L_i), VΓ(L_i), τp(L_i)} vectors across all scales.
        expected_signals: [Multi-scale feature maps, Differentiable Coherence/Pressure/Pulse values]
        pitfalls: [Mode collapse in heads, Discretization artifacts from scale selection, Non-differentiability of naive spectral estimators]
context_windows:
  - module: CORE-015_the_fractal_at_the_heart_of_time
    excerpt: |
      **Architecture Recipe**
      * **Backbone:** transformer/graph net appropriate to domain.
      * **PRG Layer:** multi-scale pyramid (dilated convs / wavelet bank) producing ({K_\tau(L), V_\Gamma(L), \tau_p(L)}) heads.
      * **Coherence Head:** differentiable compressor proxy (predict next-token NLL; or train an auxiliary autoencoder; use bits-back estimate as (K_\tau)).
      * **Pressure Head:** predict exogenous residual variance; adversarial perturbation module approximates “pressure coupling.”
      * **Beat Head:** phase-locked loop estimator to output (\tau_p) and its gradient.
  - module: CORE-015_the_fractal_at_the_heart_of_time
    excerpt: |
      Given model predictions (\hat x) over a horizon and multiscale features (\mathcal F_L(\hat x)) [from the PRG Layer], define
      [
      \mathcal L_{\text{pirouette}} = -\underbrace{\Delta K_\tau}_{\text{coherence gain}} + \lambda_\Gamma\underbrace{V_\Gamma}_{\text{pressure cost}} + \lambda_\tau\underbrace{\big(\partial_s\ln\tau_p - (\zeta_\Gamma V_\Gamma - \zeta_K K_\tau)\big)^2}_{\text{PRG beat consistency}} + \lambda_{\rm task}\mathcal L_{\rm task}.
      ]
      - **Interpretation:** maximize compressive structure while minimizing environmental friction and enforcing PRG-consistent beat scaling.
poetic_connections:
  motifs: [fractal, scale, hierarchy, pyramid, resonance, beat]
  evocative_lines:
    - "PRG turns 'maximize coherence' into a *predictive*, scale-aware control law."
    - "...baking it into AI objectives yields models that keep their story straight across scales — and that’s where generalization lives."
  association_matrix:
    - [ "COHERENCE", 0.9 ]
    - [ "PRESSURE", 0.9 ]
    - [ "PULSE", 0.8 ]
    - [ "PIRUETTE_RENORMALIZATION_GROUP", 1.0 ]
formal_mappings:
  candidates:
    - target: Wavelet Scattering Transform
      domain: Math
      mapping_kind: mathematical
      justification: |
        Both use a cascade of filters (wavelets) to extract multi-scale, stable representations of a signal. The PRG Layer is a learnable, task-oriented generalization of this principle, with heads designed to extract specific physical observables rather than just statistical moments.
      confidence: 0.8
    - target: Inception Module (GoogLeNet)
      domain: ML
      mapping_kind: conceptual
      justification: |
        Both architectures use parallel convolutional pathways with different kernel sizes (or dilations) to capture features at multiple scales simultaneously within a single network block. The PRG Layer formalizes this by assigning specific physical interpretations (Kτ, VΓ, τp) to the outputs of each pathway.
      confidence: 0.7
    - target: Renormalization Group (RG) Decimation
      domain: CM
      mapping_kind: operational
      justification: |
        The PRG Layer is the computational analogue of an RG procedure. Each scale L in the layer corresponds to a level of coarse-graining, and the heads measure the effective "couplings" (Kτ, VΓ) of the system's representation at that scale, providing the data needed to compute the RG flow.
      confidence: 0.9
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "Including a PRG Layer and its associated L_pirouette loss in a sequence model improves long-range coherence and reduces perplexity on held-out long-context tasks compared to an identical backbone trained only on a task loss."
      domain: phenomenology
      falsifier: "An ablation study shows that adding the PRG layer and loss provides no statistically significant improvement in long-range dependency tasks (e.g., story completion, audio generation) over a baseline with the same parameter count."
      status: proposed
      links: [CORE-015]
naming_notes:
  collisions: ["PRG" is a common acronym for "Pseudorandom Generator".]
  disambiguation: |
    In the Pirouette Framework, 'PRG' almost always refers to the 'Pirouette Renormalization Group'. The 'PRG Layer' is the specific neural network architecture that implements the measurement of PRG observables. It is distinct from pseudorandom generators used in cryptography or statistics.
crosslinks:
  near_synonyms: [PRG_PYRAMID]
  antonyms: [MONOSCALE_FEATURE_EXTRACTOR]
  prerequisites: [COHERENCE, PRESSURE, PULSE, PIRUETTE_RENORMALIZATION_GROUP]
  downstream_effects: [PIROUETTE_LOSS]
license: CC-BY-SA-4.0
---

# PRG Layer

## Canonical (Pirouette)
A neural network component, typically implemented as a multi-scale pyramid (e.g., using dilated convolutions or a wavelet bank), designed to extract the core Pirouette Renormalization Group (PRG) observables—Coherence (Kτ), Pressure (VΓ), and Pulse (τp)—from an input data stream at a set of discrete scales (L_i). It consists of specialized 'heads' for each observable, which compute these quantities in a differentiable manner for integration into a PRG-supervised loss function.

## EFT-First Summary
The PRG Layer is the architectural realization of a Wilsonian Renormalization Group (RG) procedure for a neural network. It acts as a 'multi-scale probe' that measures the effective 'couplings' of the model's internal representation (Coherence, Pressure) at different length scales (L). By explicitly optimizing the 'flow' of these couplings via a PRG-derived loss, the model learns a scale-invariant, and therefore more generalizable, theory of the data.

## Glossary Links
- See also: COHERENCE, PRESSURE, PULSE, PIROUETTE_LOSS, PIRUETTE_RENORMALIZATION_GROUP