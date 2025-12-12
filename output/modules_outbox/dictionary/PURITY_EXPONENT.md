---
term: "Purity Exponent"
canonical_id: "PURITY_EXPONENT"
symbol: "q"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-PHYS-002_the_neutrino_knot"]
---

---
term: Purity Exponent
canonical_id: PURITY_EXPONENT
symbol: q
aliases: []
parents: [DOMA-PHYS-002]
children: []
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-PHYS-002
      lines: "§2"
      snippet: |
        q (Purity Exponent): A dimensionless exponent governing how a state's mass is scaled by its "Purity."
  editors: [system]
  review_log: []
triad:
  art: |
    The Purity Exponent `q` measures a neutrino's inertial fealty to a single flavor. It is the exponent of allegiance, quantifying how much a state's mass is amplified by its geometric focus and resistance to mixing.
  law: |
    The absolute mass of a neutrino eigenstate `m_i` scales with its Purity (`max_α |U_{αi}|^2`) raised to the power of the Purity Exponent `q`. This scaling is a component of the Pirouette Neutrino Mass Law. A value of `q ≈ 0.45` is empirically derived from global fits to neutrino oscillation data.
  philosophy: |
    The exponent `q` is not merely a fitting parameter but a fundamental coordinate on the Prime Resonance Manifold. It represents a degree of freedom in how the universe translates geometric structure (Purity) into physical reality (mass). Its existence implies that physical laws possess a "suppleness," allowing for different self-consistent realities ("knots") to exist.
pirouette_definition: |
  The Purity Exponent `q` is a dimensionless exponent within the Pirouette Neutrino Mass Law that quantifies the scaling relationship between a neutrino mass eigenstate's Purity and its absolute mass. Along with the Participation Exponent `p` and the base mass scale `μ_ν`, `q` defines a specific "knot" configuration on the Prime Resonance Manifold of valid physical solutions.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: q
      meaning: Purity Exponent
      dimensions: dimensionless
      default_range: ≈ 0.45
  measurement:
    procedures:
      - name: Global Fit to Oscillation Data
        outline: |
          The value of `q` is not measured directly but is inferred as a free parameter in the Pirouette Neutrino Mass Law, `m_i ∝ (Purity_i)^q`. A numerical optimization routine fits the parameters `(p, q, μ_ν)` by requiring the law to reproduce experimentally measured mass-squared differences (Δm²₂₁, Δm²₃₁) using measured mixing angles as inputs. The procedure is performed for a given mass ordering (e.g., Normal Ordering).
        expected_signals:
          - A stable, best-fit value for `q` that minimizes the residuals between predicted and measured Δm² values across different experimental datasets.
          - The value of `q` is expected to be constant across different "knots" (i.e., different choices of `μ_ν` and `p` that lie on the manifold).
        pitfalls:
          - Strong correlation with the Participation Exponent `p`, potentially leading to fitting degeneracies.
          - High sensitivity to precision and uncertainties in the input mixing angle measurements (e.g., θ₁₃, δ_CP).
context_windows:
  - module: DOMA-PHYS-002
    excerpt: |
      The Law:
      $$ m_i = \mu_\nu; \left(\frac{\mathrm{PR}_i}{3}\right)^{p}; \left(\mathrm{Purity}_i\right)^{q} $$
      Where:
      ...
      q (Purity Exponent): A dimensionless exponent governing how a state's mass is scaled by its "Purity."
  - module: DOMA-PHYS-002
    excerpt: |
      The fundamental parameters (μ_ν,p,q) are not universal constants. Instead, they define a continuous, two-dimensional surface within their three-dimensional parameter space. Any point on this surface represents a valid, self-consistent physical reality. A neutrino is not defined by a single set of parameters, but by a "knot" configuration that lies somewhere on this prime resonance manifold.
poetic_connections:
  motifs: [allegiance, focus, geometry, knot, resonance, scaling]
  evocative_lines:
    - "...a knot of pure geometry, tied perfectly on a surface of possibility."
    - "...physical law from a rigid decree to a geometric relationship."
  association_matrix:
    - [ "PARTICIPATION_EXPONENT", 0.9 ]
    - [ "PURITY", 0.8 ]
    - [ "PRIME_RESONANCE_MANIFOLD", 0.7 ]
formal_mappings:
  candidates:
    - target: Anomalous dimension (γ)
      domain: QFT
      mapping_kind: conceptual
      equation_hint: |
        O(x) → Z O_R(x), where mass ~ <O>. `m ∝ Purity^q` resembles a scaling law where `q` is an anomalous dimension.
      justification: |
        The Purity Exponent `q` modifies a naive scaling relationship, behaving like an anomalous dimension in a scaling law derived from a renormalization group flow. It quantifies how the emergent property (mass) scales with a geometric system property (Purity) in a non-trivial way, deviating from a simpler integer or classical exponent.
      references: []
      confidence: 0.4
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The Purity Exponent `q` is independent of the neutrino mass ordering (NO vs. IO)."
      domain: phenomenology
      falsifier: "If future, high-precision global fits of oscillation data require statistically distinct values of `q` to correctly predict the mass-squared differences for Normal Ordering versus Inverted Ordering, the claim is falsified."
      status: supported
      links: [DOMA-PHYS-002]
    - statement: "The value of `q`, in conjunction with `p` and `μ_ν`, defines a coordinate on the two-dimensional Prime Resonance Manifold."
      domain: theory
      falsifier: "Future measurements of oscillation parameters may yield a best-fit point in `(p, q, μ_ν)` space that lies significantly off the predicted manifold surface, falsifying the manifold hypothesis."
      status: proposed
      links: [DOMA-PHYS-002]
naming_notes:
  collisions: ["The symbol `q` is commonly used for electric charge or momentum transfer in particle physics."]
  disambiguation: |
    Within the Pirouette Framework, `q` in the context of the neutrino mass law exclusively refers to the Purity Exponent. In contrast, the Participation Exponent is denoted `p`.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [PURITY, PIROUETTE_NEUTRINO_MASS_LAW]
  downstream_effects: [PRIME_RESONANCE_MANIFOLD, NEUTRINO_KNOT]
license: CC-BY-SA-4.0