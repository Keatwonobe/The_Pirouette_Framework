---
term: "Purity"
canonical_id: "PURITY"
symbol: "Purity_i"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-PHYS-002_the_neutrino_knot"]
---

---
term: Purity
canonical_id: PURITY
symbol: Purityᵢ
aliases: []
parents: [DOMA-PHYS-002_the_neutrino_knot]
children: []
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-PHYS-002_the_neutrino_knot
      lines: "§2"
      snippet: |
        Purity_i = max_α |U_{αi}|^2: Measures how strongly a mass state i is aligned with a single flavor state α. A "pure" state is dominated by one flavor.
  editors: [system-agent]
  review_log: []
triad:
  art: |
    The degree to which a state sings in a single, clear note rather than a complex chord. It is the measure of a neutrino's focus, its unwavering identity within the dance of flavors.
  law: |
    For a given neutrino mass eigenstate νᵢ, Purity is the squared L-infinity norm of the i-th column vector of the PMNS matrix. Within the Pirouette Neutrino Mass Law, the absolute mass mᵢ scales with (Purityᵢ) raised to the power of a universal Purity Exponent, q.
  philosophy: |
    Purity quantifies the geometric alignment between the mass and flavor bases. It posits that a state's intrinsic mass is not fundamental but is instead an emergent property reflecting its structural simplicity and relationship to the interaction basis. A less-mixed state has a different mass signature.
pirouette_definition: |
  For a given neutrino mass eigenstate νᵢ, Purity is a dimensionless quantity representing the maximum squared magnitude of any single element in the corresponding column of the Pontecorvo–Maki–Nakagawa–Sakata (PMNS) mixing matrix U. It quantifies the degree to which the mass state is dominated by a single flavor eigenstate (α = e, μ, τ). A value of 1 indicates a perfect alignment (no mixing), while a value of 1/3 would indicate maximal mixing (equal participation from all three flavors).
operational_definition:
  units: dimensionless
  symbol_table:
    - name: Purityᵢ
      meaning: Purity of the i-th mass eigenstate.
      dimensions: dimensionless
      default_range: [1/3, 1]
    - name: U_{αi}
      meaning: Element of the PMNS mixing matrix connecting flavor state α to mass state i.
      dimensions: dimensionless
      default_range: Complex number with magnitude in [0, 1]
    - name: α
      meaning: Flavor eigenstate index {e, μ, τ}.
      dimensions: dimensionless
      default_range: N/A
    - name: i
      meaning: Mass eigenstate index {1, 2, 3}.
      dimensions: dimensionless
      default_range: N/A
  measurement:
    procedures:
      - name: Inference from Global Oscillation Data
        outline: |
          1. Perform a global fit of experimental neutrino oscillation data (from solar, atmospheric, reactor, and accelerator sources) to determine the best-fit values and uncertainties for the PMNS mixing angles (θ₁₂, θ₁₃, θ₂₃) and CP-violating phase (δ).
          2. Construct the PMNS matrix U from these parameters.
          3. For each column `i` of the matrix U, calculate the squared magnitudes of its elements: |U_{ei}|², |U_{μi}|², |U_{τi}|².
          4. Purityᵢ is the maximum value among the three squared magnitudes for that column.
        expected_signals: [Determined values for PMNS matrix elements from global fits.]
        pitfalls: [Uncertainties in mixing parameters, particularly the octant of θ₂₃ and the value of δ, propagate directly to Purity calculations. The procedure assumes the 3x3 PMNS matrix is unitary.]
context_windows:
  - module: DOMA-PHYS-002_the_neutrino_knot
    excerpt: |
      The Law:
      $$ m_i = \mu_\nu; \left(\frac{\mathrm{PR}_i}{3}\right)^{p}; \left(\mathrm{Purity}_i\right)^{q} $$
      ...
      Purity_i = max_α |U_{αi}|^2: Measures how strongly a mass state i is aligned with a single flavor state α. A "pure" state is dominated by one flavor.
      ...
      This law proposes that a neutrino's mass is a direct consequence of its internal geometry, as described by the mixing matrix U.
  - module: DOMA-PHYS-002_the_neutrino_knot
    excerpt: |
      Fitting protocol.
      1. Build PMNS from (θ₁₂,θ₁₃,θ₂₃,δ) using PDG-like input; compute (PRᵢ, Purityᵢ).
      2. Normal ordering (NO): fit (p,q,μ_ν) to (Δm²₂₁, Δm²₃₁).
      3. Inverted ordering (IO): freeze (p,q) from NO; refit μ_ν only to (Δm²₂₁, Δm²₃₁|_{IO}).
poetic_connections:
  motifs: [alignment, focus, identity, simplicity, clarity]
  evocative_lines:
    - "A neutrino, in this view, is not a static object, but a dynamic equilibrium—a knot of pure geometry, tied perfectly on a surface of possibility."
    - "We began by seeking a single point of light in the darkness... Instead, we found a constellation."
  association_matrix:
    - [ "PARTICIPATION_RATIO", 0.9 ]
    - [ "PRIME_RESONANCE_MANIFOLD", 0.7 ]
    - [ "NEUTRINO_KNOT", 0.6 ]
formal_mappings:
  candidates: []
  adopted:
    - target: max_α |U_{αi}|²
      domain: SM
      mapping_kind: mathematical
      equation_hint: |
        Purityᵢ = max( |U_{ei}|², |U_{μi}|², |U_{τi}|² )
      justification: |
        Purity is not an independent physical parameter but a derived geometric quantity. It is defined as the maximum squared magnitude of the elements in a given column of the PMNS mixing matrix, U. Each element |U_{αi}|² represents the probability of observing flavor α when measuring a state of mass i, a standard concept in neutrino physics. Purity is thus the L-infinity norm (squared) of a column vector in the flavor basis.
      references:
        - title: Review of Particle Physics
          where: Particle Data Group, "Neutrino Mass, Mixing, and Oscillations" section
          date: 2024-08-01
      confidence: 1.0
      rationale: The mapping is a direct mathematical definition, not an analogy. Purity is a specific statistic of a column vector in the PMNS matrix.
constraints_and_falsifiers:
  claims:
    - statement: "The absolute mass of a neutrino eigenstate (mᵢ) scales as a power-law function of its Purity, (Purityᵢ)^q, where q is an order-independent constant."
      domain: phenomenology
      falsifier: "If future global fits of oscillation data, combined with absolute mass measurements from cosmology or beta-decay experiments, require significantly different values for the exponent q to fit the mass-squared differences in Normal vs. Inverted orderings, this simple form of the law would be falsified."
      status: proposed
      links: [DOMA-PHYS-002_the_neutrino_knot]
naming_notes:
  collisions: ["Chemical Purity"]
  disambiguation: |
    Purity in the Pirouette Framework is a specific, dimensionless geometric measure derived from the PMNS matrix column vectors. It must not be confused with the common-language or chemical concept of purity as the absence of contaminants.
crosslinks:
  near_synonyms: []
  antonyms: [PARTICIPATION_RATIO]
  prerequisites: []
  downstream_effects: [NEUTRINO_MASS, PRIME_RESONANCE_MANIFOLD, NEUTRINO_KNOT]
license: CC-BY-SA-4.0
---