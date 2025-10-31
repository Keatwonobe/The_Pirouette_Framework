---
term: "Pirouette Neutrino Mass Law"
canonical_id: "PIROUETTE_NEUTRINO_MASS_LAW"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-PHYS-002_the_neutrino_knot"]
---

---
term: Pirouette Neutrino Mass Law
canonical_id: PIROUETTE_NEUTRINO_MASS_LAW
symbol: $$ m_i = \mu_\nu \left(\frac{\mathrm{PR}_i}{3}\right)^{p} \left(\mathrm{Purity}_i\right)^{q} $$
aliases: [PPS-ν-001]
parents: [DOMA-PHYS-002]
children: []
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-PHYS-002
      snippet: |
        Law. For each mass eigenstate νᵢ,
        $$ m_i = \mu_\nu;\Big(\tfrac{\mathrm{PR}i}{3}\Big)^{p};\big(\mathrm{Purity}i\big)^{q}, \qquad
        \mathrm{Purity}i = \max\alpha |U{\alpha i}|^2, \quad \mathrm{PR}i = \frac{1}{\sum\alpha |U{\alpha i}|^4}. $$
  editors: [Pirouette System]
  review_log: []
triad:
  art: |
    A neutrino's mass is not an intrinsic weight, but the geometric signature of its entangled flavors. It is a knot of pure possibility, tied perfectly on a surface of universal resonance.
  law: |
    The mass of a neutrino eigenstate (mᵢ) is the product of a base mass scale (μ_ν) and two geometric factors derived from the mixing matrix: the Participation Ratio (PRᵢ) and Purityᵢ, each raised to a constant power (p, q respectively).
  philosophy: |
    The law reframes fundamental constants as parameters defining a continuous manifold of valid physical realities. This suggests the universe's laws possess a geometric suppleness rather than being a set of rigid, singular values.
pirouette_definition: |
  The Pirouette Neutrino Mass Law is a formula that derives the absolute mass of a neutrino mass eigenstate, mᵢ, from its geometric properties within the PMNS mixing matrix. It states that mᵢ is equal to a fundamental base mass scale for the neutrino sector, μ_ν, scaled by the eigenstate's Participation Ratio (PRᵢ) and Purityᵢ, raised to the exponents p and q, respectively. The law posits that a neutrino's mass is an emergent, not intrinsic, property governed by its flavor composition.
operational_definition:
  units: Mass terms (mᵢ, μ_ν) are in electron-volts (eV). All other parameters are dimensionless.
  symbol_table:
    - name: mᵢ
      meaning: Mass of the i-th neutrino mass eigenstate (i=1,2,3).
      dimensions: M
      default_range: 0.007–0.012 eV
    - name: μ_ν
      meaning: The base mass scale for the neutrino sector.
      dimensions: M
      default_range: 0.017–0.019 eV
    - name: p
      meaning: The Participation Exponent, scaling the effect of flavor mixedness.
      dimensions: dimensionless
      default_range: ~1.54
    - name: q
      meaning: The Purity Exponent, scaling the effect of flavor alignment.
      dimensions: dimensionless
      default_range: ~0.45
    - name: PRᵢ
      meaning: Participation Ratio of state i; a measure of flavor mixedness.
      dimensions: dimensionless
      default_range: "[1, 3]"
    - name: Purityᵢ
      meaning: Purity of state i; measures alignment with a single flavor.
      dimensions: dimensionless
      default_range: "[1/3, 1]"
  measurement:
    procedures:
      - name: Global Fit Inference
        outline: |
          The parameters (μ_ν, p, q) are not directly measured but are inferred by fitting the law's predictions to experimental data from neutrino oscillation experiments.
          1. Construct the PMNS mixing matrix U from experimentally measured oscillation angles (θ₁₂, θ₁₃, θ₂₃) and the CP-violating phase (δ).
          2. Calculate the geometric properties Purityᵢ and PRᵢ for each mass state i=1,2,3 from the elements of U.
          3. Perform a numerical optimization to find the values of (μ_ν, p, q) that best reproduce the experimentally measured mass-squared differences (Δm²₂₁ and Δm²₃₁).
        expected_signals: [A self-consistent set of (μ_ν, p, q) that fits oscillation data for both Normal and Inverted orderings, A continuous 2D manifold of such solution sets.]
        pitfalls: [Assuming a unique point-like solution instead of a manifold, Neglecting environmental production effects (modeled by the Γ-toggle) which can subtly alter the input geometry.]
context_windows:
  - module: DOMA-PHYS-002
    excerpt: |
      The foundation of this discovery is the Pirouette Neutrino Mass Law, which posits that the absolute mass of each neutrino mass eigenstate (m_i) is not an intrinsic property, but an emergent one, governed by a geometric relationship between a base mass scale and the state's structural properties.
  - module: DOMA-PHYS-002
    excerpt: |
      The primary prediction is the existence and specific shape of the manifold itself. The relationship between the three parameters is not arbitrary and should be describable by a predictive mathematical function. Future, more precise measurements of the oscillation parameters will either further constrain the shape of this manifold or, if they are inconsistent with any point on its surface, falsify the law.
poetic_connections:
  motifs: [geometric mass, resonant manifold, physical law as relationship, knot hypothesis]
  evocative_lines:
    - "Instead, we found a constellation."
    - "A knot of pure geometry, tied perfectly on a surface of possibility."
  association_matrix:
    - [ "PRIME_RESONANCE_MANIFOLD", 0.9 ]
    - [ "NEUTRINO_KNOT", 0.8 ]
    - [ "GEOMETRY_OF_RESONANCE", 0.7 ]
formal_mappings:
  candidates:
    - target: Phenomenological neutrino mass models (e.g., seesaw mechanism)
      domain: BSM
      mapping_kind: conceptual
      justification: |
        The Pirouette Neutrino Mass Law provides a phenomenological formula for neutrino masses, similar to how BSM models like the seesaw mechanism generate them. However, instead of introducing new heavy particles, this law derives masses from the geometry of the existing PMNS mixing matrix. It serves as an alternative, geometrically-motivated organizational principle for the observed mass pattern, rooted in resonance dynamics.
      references: []
      confidence: 0.2
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The law, with a single pair of exponents (p,q), can accurately reproduce the measured mass-squared differences for both Normal and Inverted mass orderings."
      domain: phenomenology
      falsifier: "Future global fits of oscillation data require statistically distinct (p,q) values for Normal and Inverted orderings to match experimental results, invalidating the claim of order-independence."
      status: supported
      links: [DOMA-PHYS-002]
    - statement: "The set of valid parameters (μ_ν, p, q) that fit experimental data forms a continuous, two-dimensional manifold."
      domain: theory
      falsifier: "Higher precision measurements of oscillation parameters constrain the valid parameter space to a single point, a discrete set of points, or a space with dimensionality other than two."
      status: proposed
      links: [DOMA-PHYS-002]
naming_notes:
  collisions: [The term "mass law" is generic in physics.]
  disambiguation: |
    This is not a fundamental Lagrangian term but a phenomenological relationship derived from the Pirouette Framework's core principles. It describes the emergent *result* of underlying resonance dynamics, not the dynamics themselves.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [GEOMETRY_OF_RESONANCE]
  downstream_effects: [PRIME_RESONANCE_MANIFOLD, NEUTRINO_KNOT]
license: CC-BY-SA-4.0
---

# Pirouette Neutrino Mass Law

## Canonical (Pirouette)
The Pirouette Neutrino Mass Law is a formula that derives the absolute mass of a neutrino mass eigenstate, mᵢ, from its geometric properties within the PMNS mixing matrix. It states that mᵢ is equal to a fundamental base mass scale for the neutrino sector, μ_ν, scaled by the eigenstate's Participation Ratio (PRᵢ) and Purityᵢ, raised to the exponents p and q, respectively. The law posits that a neutrino's mass is an emergent, not intrinsic, property governed by its flavor composition.

## EFT-First Summary
Currently, there is no direct mapping of this law to a specific Standard Model Effective Field Theory (SMEFT) operator. It functions as a novel organizational principle for neutrino mass terms, deriving them from the geometry of the lepton mixing matrix rather than from higher-dimension operators involving new fields (e.g., as in the seesaw mechanism). The law's parameters (μ_ν, p, q) would be emergent properties of a more fundamental theory.

## Glossary Links
- See also: Prime Resonance Manifold, Neutrino Knot Hypothesis