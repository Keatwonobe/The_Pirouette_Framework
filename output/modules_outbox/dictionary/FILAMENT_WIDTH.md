---
term: "Filament Width"
canonical_id: "FILAMENT_WIDTH"
symbol: "σ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["XAP-003_appendix_addendum_017_018"]
---

---
term: Filament Width
canonical_id: FILAMENT_WIDTH
symbol: σ
aliases: []
parents: [XAP-003_appendix_addendum_017_018]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: XAP-003_appendix_addendum_017_018
      lines: "XAP-018 — Notebook"
      snippet: |
        # Fit 2‑D GMM (1 component suffices but we check for multimodality)
        gmm = GaussianMixture(n_components=1, covariance_type='full')
        gmm.fit(filament)
        cov = gmm.covariances_[0]
        print('Std‑dev', np.sqrt(np.diag(cov)))
  editors: [autocompleter_agent]
  review_log: []
triad:
  art: |
    A stable filament is a glowing thread of emergent order in state space. Its width is the soft blur at the edges, the hum of tolerable fluctuations around a central truth.
  law: |
    Filament Width (σ) is the standard deviation of state-space points populating a stable attractor, quantified as the square root of the diagonal elements of the covariance matrix from a fitted Gaussian Mixture Model. A smaller σ implies a tighter, more stable filament.
  philosophy: |
    Width quantifies the tolerance or robustness of an attractor. A thin filament represents a highly constrained, precise emergent behavior, while a wider filament indicates a more permissive or fuzzy region of stability. It measures the practical boundary of an ideal form.
pirouette_definition: |
  Filament Width (σ) is a parameter quantifying the thickness or dispersion of a stable attractor (filament) in a system's state space. It is operationally defined by fitting a one-component Gaussian Mixture Model (GMM) to a population of high-value state points (e.g., the top 5% by Coherence Dividend). The width along a given state-space axis is the standard deviation, calculated as the square root of the corresponding diagonal element of the GMM's covariance matrix.
operational_definition:
  units: Same as the associated state-space coordinate (dimensionless for Γ and Tₐ).
  symbol_table:
    - name: σᵢ
      meaning: Filament Width along state-space axis 'i'.
      dimensions: Same as the coordinate of axis 'i'.
      default_range: "> 0, typically << 1"
    - name: cov
      meaning: Covariance matrix of the fitted Gaussian distribution.
      dimensions: (dim_axis_i) × (dim_axis_j)
      default_range: contextual
  measurement:
    procedures:
      - name: GMM Covariance Fitting
        outline: |
          1. From Monte Carlo simulation data, select the population of state-space points corresponding to the highest values of a target metric (e.g., top 5% of Coherence Dividend).
          2. Fit a single-component Gaussian Mixture Model (GMM) to this selected data cloud.
          3. Extract the covariance matrix, `cov`, from the fitted model.
          4. For each state-space axis `i`, calculate the filament width as σᵢ = √cov[i,i].
        expected_signals: [A positive-definite covariance matrix, a unimodal distribution of high-performance points.]
        pitfalls: [Insufficient data leading to a poorly conditioned covariance matrix, non-Gaussian or multi-modal filament structures confounding the single-component GMM assumption.]
context_windows:
  - module: XAP-003_appendix_addendum_017_018
    excerpt: |
      Parse Monte‑Carlo output from `cosmic_compass_simulation2.py`, isolate the top‑5 % Coherence Dividend points, and fit a 2‑component Gaussian Mixture to quantify filament centre & width. [...] `cov = gmm.covariances_[0]` [...] The output `filament_stats.json` contains `{"mu_Gamma":1.49,"sigma_Gamma":0.04,"mu_Ta":1.01,"sigma_Ta":0.03}`.
  - module: XAP-003_appendix_addendum_017_018
    excerpt: |
      Since \(L\ge0\) and \(\dot L\le0\) with \(\dot L=0\) exclusively on \(\mathcal F\), the altruism filament is **Lyapunov‑stable**. Small perturbations decay monotonically back to the filament.
poetic_connections:
  motifs: [stability, dispersion, tolerance, attractor, ridge]
  evocative_lines:
    - "Small perturbations decay monotonically back to the filament."
    - "the altruism filament is Lyapunov‑stable."
  association_matrix:
    - [ "COHERENCE_DIVIDEND", 0.8 ]
    - [ "LYAPUNOV_STABILITY", 0.7 ]
    - [ "ALTRUISM_FILAMENT", 0.9 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Standard Deviation (σ)
      domain: Math
      mapping_kind: mathematical
      equation_hint: |
        σᵢ = √⟨(xᵢ - μᵢ)²⟩ = √cov[i,i]
      rationale: The Pirouette definition is a direct, specific application of the mathematical concept of standard deviation to characterize the dispersion of a cloud of state-space points that constitute a stable system configuration. The mapping is definitional.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The distribution of high-coherence states forming the Altruism Filament is well-approximated by a single multivariate Gaussian distribution."
      domain: phenomenology
      falsifier: "A goodness-of-fit test rejects the single-Gaussian hypothesis, or model selection criteria (e.g., BIC/AIC) strongly favor a multi-component GMM, indicating filament substructure or non-Gaussian shape."
      status: supported
      links: [XAP-003_appendix_addendum_017_018]
naming_notes:
  collisions: [The symbol σ is standard for standard deviation, but is also used for conductivity, stress tensors, and scattering cross-sections in other fields.]
  disambiguation: |
    Filament Width (σ) refers specifically to the standard deviation of state-space coordinates *within* a stable filament, not a generic statistical standard deviation of the entire state space. It is an intrinsic geometric property of the attractor itself.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [ALTRUISM_FILAMENT, COHERENCE_DIVIDEND]
  downstream_effects: []
license: CC-BY-SA-4.0