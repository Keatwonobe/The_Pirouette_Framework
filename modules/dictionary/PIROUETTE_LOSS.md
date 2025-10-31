---
term: "Pirouette Loss"
canonical_id: "PIROUETTE_LOSS"
symbol: "L_pirouette"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["CORE-015_the_fractal_at_the_heart_of_time"]
---

---
term: Pirouette Loss
canonical_id: PIROUETTE_LOSS
symbol: $\mathcal{L}_{\text{pirouette}}$
aliases: [PRG-Supervised Coherence Loss, Coherence-Centric Objective]
parents: [CORE-015]
children: []
status: draft
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: CORE-015_the_fractal_at_the_heart_of_time
      lines: "Sec 4.1"
      snippet: |
        Given model predictions $(\hat x)$ over a horizon and multiscale features $(\mathcal F_L(\hat x))$, define
        [
        \mathcal L_{\text{pirouette}} = -\underbrace{\Delta K_\tau}_{\text{coherence gain}}
        + \lambda_\Gamma\underbrace{V_\Gamma}_{\text{pressure cost}}
        + \lambda_\tau\underbrace{\big(\partial_s\ln\tau_p - (\zeta_\Gamma V_\Gamma - \zeta_K K_\tau)\big)^2}_{\text{PRG beat consistency}}
        + \lambda_{\rm task}\mathcal L_{\rm task}.
        ]
  editors: [auto-populator]
  review_log: []
triad:
  art: |
    An objective that teaches a system to find the rhythm of its own unfolding. It learns to not just perform a task, but to do so with an elegance that maintains its structural integrity across all scales of time and space, keeping its story straight from the flicker to the epoch.
  law: |
    To optimize a system's trajectory, one must simultaneously maximize its gain in self-similar compressibility ($\Delta K_\tau$), minimize the environmental friction it generates ($V_\Gamma$), and minimize its deviation from the scale-invariant temporal scaling predicted by its own Pirouette Renormalization Group (PRG) flow.
  philosophy: |
    True generalization and robust intelligence emerge not from simply fitting data at a single, privileged scale, but from internalizing and satisfying the physical-like scaling laws that govern the relationships between scales. This objective function enforces a powerful inductive bias: that coherent, stable, and adaptive behavior is synonymous with respecting the fractal dynamics of the system itself.
pirouette_definition: |
  The Pirouette Loss is a composite objective function for training AI agents, designed to promote cross-scale coherence under the supervision of the Pirouette Renormalization Group (PRG). It is defined as a weighted sum of four components:

  $\mathcal{L}_{\text{pirouette}} = -\Delta K_\tau + \lambda_\Gamma V_\Gamma + \lambda_\tau \left( \frac{d \ln \tau_p}{ds} - \beta_\tau(K_\tau, V_\Gamma) \right)^2 + \lambda_{\text{task}}\mathcal{L}_{\text{task}}$

  1.  **Coherence Gain ($-\Delta K_\tau$):** The primary driver, which is maximized. It rewards the model for increasing the compressibility or self-similar structure ($K_\tau$) in its generated outputs or future states.
  2.  **Pressure Cost ($\lambda_\Gamma V_\Gamma$):** A regularizer that penalizes interaction with the environment that is costly or high-friction ($V_\Gamma$). This discourages brittle, environment-stressing solutions.
  3.  **PRG Beat Consistency ($\lambda_\tau (\dots)^2$):** A regularizer that penalizes deviations from the PRG-predicted scaling of the system's characteristic timescale or 'beat' ($\tau_p$). It enforces that the system's temporal dynamics evolve according to its own inferred scaling laws, damping oscillatory instabilities.
  4.  **Task Loss ($\lambda_{\text{task}}\mathcal{L}_{\text{task}}$):** A standard, domain-specific loss function (e.g., cross-entropy, mean squared error) that grounds the model in its primary task.

  The weights ($\lambda$) are schedulable hyperparameters, and the PRG parameters ($\zeta_K, \zeta_\Gamma$ in $\beta_\tau$) can be fixed a priori or learned from the model's own outputs in an iterative, EM-style loop.
operational_definition:
  units: Dimensionless (typically interpreted in nats or bits).
  symbol_table:
    - name: $\Delta K_\tau$
      meaning: Change in coherence ($K_\tau$) over a forward pass or time horizon.
      dimensions: dimensionless
      default_range: contextual
    - name: $V_\Gamma$
      meaning: Pressure, a measure of environmental drive or friction at a given scale.
      dimensions: contextual (depends on proxy)
      default_range: $[0, \infty)$
    - name: $\tau_p$
      meaning: Pulse, the dominant period or characteristic timescale of the system at a given scale.
      dimensions: T
      default_range: contextual
    - name: $s$
      meaning: Logarithmic scale parameter, $s \equiv \ln L$.
      dimensions: dimensionless
      default_range: contextual
    - name: $\beta_\tau$
      meaning: The PRG beta function for the pulse, $\beta_\tau = \zeta_\Gamma V_\Gamma - \zeta_K K_\tau$.
      dimensions: dimensionless
      default_range: contextual
    - name: $\lambda_i$
      meaning: Schedulable, non-negative weights for balancing the loss components.
      dimensions: dimensionless
      default_range: $[0, \infty)$
  measurement:
    procedures:
      - name: Loss Computation in a Training Step
        outline: |
          1.  Generate a model output trajectory (e.g., a sequence of tokens, a series of control actions).
          2.  Pass the trajectory through a multi-scale feature extractor (e.g., a wavelet bank, a PRG Layer) to compute observables $\{K_\tau(L_i), V_\Gamma(L_i), \tau_p(L_i)\}$ at a set of scales $\{L_i\}$.
          3.  Estimate derivatives with respect to log-scale $s=\ln L$ via finite differences (e.g., $\Delta K_\tau \approx K_\tau(L_{final}) - K_\tau(L_{initial})$).
          4.  Compute each of the four loss components using these observables and their derivatives.
          5.  Combine the components using the current weights ($\lambda$) to get the final $\mathcal{L}_{\text{pirouette}}$ scalar value for backpropagation.
        expected_signals: [Scalar loss value, gradients for each model parameter]
        pitfalls: [Numerical instability in derivative estimation, poorly conditioned PRG parameter fits, requirement for careful scheduling of $\lambda$ weights to avoid conflicting gradients early in training.]
context_windows:
  - module: CORE-015
    excerpt: |
      Interpretation: maximize compressive structure while minimizing environmental friction and enforcing PRG-consistent beat scaling. $(\lambda)$ are schedulable weights; $(\zeta)$ can be learned or fixed from PRG fits.
  - module: CORE-015
    excerpt: |
      PRG turns “maximize coherence” into a *predictive*, scale-aware control law; baking it into AI objectives yields models that keep their story straight across scales — and that’s where generalization lives.
poetic_connections:
  motifs: [self-consistency, rhythmic stability, fractal dynamics, scale-invariance, controlled unfolding]
  evocative_lines:
    - "keep their story straight across scales"
    - "the fractal at the heart of time"
  association_matrix:
    - [ "COHERENCE_KT", 0.8 ]
    - [ "PIROUETTE_RENORMALIZATION_GROUP", 0.7 ]
    - [ "PRESSURE_VG", 0.6 ]
    - [ "BEAT_DILATION_TAU", 0.6 ]
formal_mappings:
  candidates:
    - target: Variational Free Energy / ELBO
      domain: Math
      mapping_kind: conceptual
      equation_hint: |
        $F = \mathbb{E}_q[\ln q(z|\phi) - \ln p(x,z|\theta)] = D_{KL}(q||p) - \mathbb{E}_q[\ln p(x|z)]$
      justification: |
        The Pirouette Loss can be framed as a generalized free energy functional. The task loss ($\mathcal{L}_{\text{task}}$) is analogous to a reconstruction error (negative log-likelihood). The coherence gain term ($-\Delta K_\tau$) acts like maximizing model evidence by minimizing description length. The pressure and beat consistency terms act as a complex, dynamics-aware prior on the latent trajectory of the system, penalizing "surprising" or incoherent state transitions.
      references:
        - title: "Neural Variational Inference and Learning in Belief Networks"
          where: "ICML 2014"
          date: 2014-06-01
      confidence: 0.7
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: 'For sequential modeling tasks, minimizing $\mathcal{L}_{\text{pirouette}}$ produces models with lower long-horizon perplexity compared to optimizing $\mathcal{L}_{\text{task}}$ alone.'

      domain: phenomenology
      falsifier: 'An ablation study shows that models trained with only the coherence term ($\lambda_\Gamma=\lambda_\tau=0$) or only the task loss perform equally well or better on long-horizon benchmarks, indicating the PRG consistency constraints do not improve generalization.'

      status: proposed
      links: [CORE-015]
    - statement: 'The pressure regularizer term ($\lambda_\Gamma V_\Gamma$) reduces reward-hacking behavior in complex reinforcement learning environments.'

      domain: experiment
      falsifier: "In benchmark RL environments known for reward-hacking, agents trained with the pressure term enabled find qualitatively similar exploits to baseline agents, showing no significant improvement in strategic alignment."
      status: proposed
      links: [CORE-015]
naming_notes:
  collisions: [The symbol $\mathcal{L}$ is standard for both Loss functions in machine learning and Lagrangians in physics. This is intentional, as the objective function plays the role of a Lagrangian in an action-minimization principle.]
  disambiguation: |
    Distinguish from a pure "Coherence Loss", which would only contain the $\Delta K_\tau$ term. The Pirouette Loss is a composite objective that includes pressure and temporal scaling constraints derived from the Pirouette Renormalization Group (PRG), not just coherence.
crosslinks:
  near_synonyms: []
  antonyms: [TASK_LOSS_ONLY]
  prerequisites: [COHERENCE_KT, PRESSURE_VG, BEAT_PULSE_TAU, PIROUETTE_RENORMALIZATION_GROUP]
  downstream_effects: [PIROUETTE_AGENT]
license: CC-BY-SA-4.0
---

# Pirouette Loss

## Canonical (Pirouette)
The Pirouette Loss is a composite objective function, $\mathcal{L}_{\text{pirouette}}$, used to train AI systems by rewarding behaviors that are not only effective at a specific task but also demonstrate self-consistent, stable dynamics across multiple scales. It achieves this by combining a standard task loss with three terms derived from the Pirouette Renormalization Group (PRG): a reward for increasing coherence (compressibility), a penalty for high-friction environmental interaction (pressure), and a penalty for deviating from the system's own predicted scaling laws for its characteristic tempo (beat consistency).

## EFT-First Summary
The Pirouette Loss can be interpreted as a variational free energy functional. The task-specific loss acts as a data-fitting or reconstruction term, while the remaining PRG-derived components collectively form a complex, structured prior over the system's dynamics. Maximizing coherence gain is analogous to maximizing model evidence by minimizing descriptive complexity (an MDL principle). The pressure and beat consistency terms constrain the latent trajectory to low-energy, dynamically stable paths, effectively regularizing against chaotic or inefficient solutions.

## Glossary Links
- See also: [Coherence (K_τ)](COHERENCE_KT), [Pressure (V_Γ)](PRESSURE_VG), [Pirouette Renormalization Group](PIROUETTE_RENORMALIZATION_GROUP), [Pirouette Agent](PIROUETTE_AGENT)