---
term: "Filament Centre"
canonical_id: "FILAMENT_CENTRE"
symbol: "μ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["XAP-003_appendix_addendum_017_018"]
---

---
term: Filament Centre
canonical_id: FILAMENT_CENTRE
symbol: μ
aliases: []
parents: [XAP-003, PPS-023]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: XAP-003_appendix_addendum_017_018
      lines: "XAP-018 Workflow Outline"
      snippet: |
        # Fit 2‑D GMM (1 component suffices but we check for multimodality)
        gmm = GaussianMixture(n_components=1, covariance_type='full')
        gmm.fit(filament)
        mu = gmm.means_[0]            # [mu_Gamma, mu_Ta]
  editors: [Agent]
  review_log: []
triad:
  art: |
    The spine of the attractor, the gravitational line where altruistic states gather and stabilize. It is the bright thread of coherence woven through the noise of possibility.
  law: |
    The Filament Centre μ is the vector mean of the state-space distribution for all system states whose Coherence Dividend C exceeds the 95th percentile of a Monte-Carlo ensemble. It represents the most probable stable configuration.
  philosophy: |
    The Filament Centre identifies the optimal, stable balance point for altruistic dynamics. It serves as a concrete target for system tuning and a benchmark against which perturbations and evolutionary trajectories are measured.
pirouette_definition: |
  The Filament Centre, μ, is the central tendency of the Altruism Filament, operationally defined as the mean vector of a Gaussian Mixture Model (GMM) fitted to the high-coherence (top 5%) subset of system states \(x=(\Gamma,T_a)\) from a Monte-Carlo simulation. Theoretically, it approximates the point of maximum stability and coherence on the Lyapunov-stable manifold \(\mathcal F\) where \(\nabla C = 0\).
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: μ
      meaning: Filament Centre vector, \((\mu_\Gamma, \mu_{T_a})\).
      dimensions: dimensionless
      default_range: "(1.49, 1.01) per XAP-018"
    - name: C
      meaning: Coherence Dividend
      dimensions: dimensionless
      default_range: contextual
    - name: Γ
      meaning: Gamma component of the reduced Compass state.
      dimensions: dimensionless
      default_range: contextual
    - name: T_a
      meaning: T_a component of the reduced Compass state.
      dimensions: dimensionless
      default_range: contextual
  measurement:
    procedures:
      - name: GMM Analysis of Monte-Carlo Ensemble
        outline: |
          1. Execute a Monte-Carlo simulation of system dynamics to generate a large ensemble of state points \((\Gamma, T_a)\) and their associated Coherence Dividend \(C\).
          2. Filter the ensemble, retaining only points in the 95th percentile or higher of \(C\).
          3. Fit a single-component, 2D Gaussian Mixture Model (GMM) to the filtered \((\Gamma, T_a)\) data.
          4. The Filament Centre μ is the mean vector `gmm.means_[0]` from the fitted model.
        expected_signals: [A JSON object with mean and standard deviation values, e.g., `{"mu_Gamma":1.49,"sigma_Gamma":0.04,"mu_Ta":1.01,"sigma_Ta":0.03}`]
        pitfalls: [The filament's state-space distribution may not be unimodal or well-approximated by a single Gaussian. The 95% coherence percentile is a heuristic that may be suboptimal.]
context_windows:
  - module: XAP-003_appendix_addendum_017_018
    excerpt: |
      Since \(L\ge0\) and \(\dot L\le0\) with \(\dot L=0\) exclusively on \(\mathcal F\), the altruism filament is **Lyapunov‑stable**. Small perturbations decay monotonically back to the filament.
  - module: XAP-003_appendix_addendum_017_018
    excerpt: |
      Parse Monte‑Carlo output from `cosmic_compass_simulation2.py`, isolate the top‑5 % Coherence Dividend points, and fit a 2‑component Gaussian Mixture to quantify filament centre & width. [...] `mu = gmm.means_[0]`
poetic_connections:
  motifs: [stability, attractor, spine, ridge, coherence, optimum]
  evocative_lines:
    - "Small perturbations decay monotonically back to the filament."
    - "The bright thread of coherence woven through noise."
  association_matrix:
    - [ "ALTRUISM_ATTRACTOR", 0.9 ]
    - [ "COHERENCE_DIVIDEND", 0.8 ]
    - [ "LYAPUNOV_STABILITY", 0.7 ]
formal_mappings:
  candidates:
    - target: Maximum of a potential function \(C(x)\)
      domain: CM|Dynamical Systems
      mapping_kind: mathematical
      equation_hint: |
        \dot x \propto \nabla_x C(x)
      justification: |
        System dynamics are defined as gradient ascent on the Coherence Dividend C. The filament is the manifold where the gradient is zero, representing a ridge of local maxima. The Filament Centre is the peak of this ridge, analogous to the stable equilibrium point at the maximum of a potential field.
      references: []
      confidence: 0.8
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The Filament Centre represents the global maximum of the Coherence Dividend C in the \((\Gamma, T_a)\) state space."
      domain: phenomenology
      falsifier: "Discovery of a disjoint region of state space with a statistically significant higher mean Coherence Dividend after a more exhaustive Monte-Carlo search. Alternatively, if the GMM fit consistently identifies multiple, distinct components with similar weights."
      status: proposed
      links: [XAP-003]
naming_notes:
  collisions: [The symbol μ is overloaded (e.g., mean, chemical potential, muon).]
  disambiguation: |
    Distinguish from the Altruism Filament (\(\mathcal F\)) itself, which is a manifold (a set of points). The Filament Centre (μ) is a single point on that manifold, representing its statistically-derived central tendency.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [COHERENCE_DIVIDEND]
  downstream_effects: []
license: CC-BY-SA-4.0
---

# Filament Centre

## Canonical (Pirouette)
The Filament Centre, μ, is the central tendency of the Altruism Filament, operationally defined as the mean vector of a Gaussian Mixture Model (GMM) fitted to the high-coherence (top 5%) subset of system states \(x=(\Gamma,T_a)\) from a Monte-Carlo simulation. Theoretically, it approximates the point of maximum stability and coherence on the Lyapunov-stable manifold \(\mathcal F\) where \(\nabla C = 0\).

## EFT-First Summary
The Filament Centre μ behaves as a stable equilibrium point in a potential landscape defined by the Coherence Dividend \(C\). System dynamics follow gradient ascent on \(C\), causing states to converge on the filament, with μ representing the peak of this attractor. This is analogous to a particle settling at the maximum of a potential field in classical mechanics.

## Glossary Links
- See also: Coherence Dividend, Altruism Attractor