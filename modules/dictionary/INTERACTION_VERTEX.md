---
term: "Interaction Vertex"
canonical_id: "INTERACTION_VERTEX"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-011"]
---

---
term: Interaction Vertex
canonical_id: INTERACTION_VERTEX
symbol: —●— (graphical), g, λ (coupling constants)
aliases: [Feynman Vertex, Coupling]
parents: [MATH-011]
children: [XXP-013]
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-011
      snippet: |
        Vertices follow from derivatives of (V). Example: the cubic (g|C|^2\Gamma) gives a vertex with two coheron legs and one pressuron leg of strength (-ig).
  editors: [GPT-4]
  review_log: []
triad:
  art: |
    At a vertex, the silent score of the universe becomes audible. It is the point where world-lines meet, a chord is struck, and particles are transformed in the ongoing quantum symphony.
  law: |
    An interaction vertex is a graphical rule derived from a non-quadratic term in the interaction potential V. The number and type of lines meeting at the vertex, and its associated coupling constant, dictate the fundamental probability amplitude for that local interaction.
  philosophy: |
    The vertex is the atomic unit of causal influence in a quantum field theory. It embodies locality, ensuring interactions are point-like events from which all complex phenomena of scattering, decay, and transformation are built.
pirouette_definition: |
  A fundamental rule for constructing Feynman diagrams, derived from a specific interaction term in the Pirouette potential `V(|C|^2, Γ)`. An interaction vertex represents a local, point-like event where a specific number of Coheron and/or Pressuron world-lines meet. The structure of the vertex (which particles participate) is fixed by the fields in the interaction term, and its strength is determined by the associated coupling constant (e.g., `g`, `λ`). Every vertex conserves four-momentum.
operational_definition:
  units: The units of the associated coupling constant depend on the vertex. For a `g|C|^2Γ` term in 4D spacetime, `g` has units of mass (energy). For `λ|C|^4`, `λ` is dimensionless.
  symbol_table:
    - name: V
      meaning: Interaction Potential
      dimensions: M L⁻¹ T⁻² (Energy Density)
      default_range: contextual
    - name: g, λ
      meaning: Coupling constants; strength of a specific interaction vertex
      dimensions: contextual (e.g., M or dimensionless)
      default_range: must be measured; perturbative control requires small values
    - name: C, Γ
      meaning: Coheron and Pressuron fields
      dimensions: M¹ᐟ² L⁻¹ᐟ² T⁰ (scalar field)
      default_range: N/A (fields)
  measurement:
    procedures:
      - name: Particle Decay Width Measurement
        outline: |
          If the kinematics allow (e.g., `m_Γ > 2m_C`), the `g|C|^2Γ` vertex permits the decay `Γ → C + anti-C`. Prepare or isolate a sample of Pressurons and measure the lifetime or decay width of the ensemble. The measured width can be compared directly to the theoretical prediction, which is proportional to `g^2`.
        expected_signals: [A resonance peak at `m_Γ` in the `C-anti-C` invariant mass spectrum, An exponential decay curve for a `Γ` population]
        pitfalls: [Failing to account for other decay channels, Incorrect final-state particle identification, Poor statistics leading to large uncertainty in the measured width]
      - name: Scattering Cross-Section Measurement
        outline: |
          Collide beams of particles (e.g., Coherons on Coherons) at various center-of-mass energies. The interaction vertex (e.g., `λ|C|^4`) determines the probability and angular distribution of the scattering. Measure the differential cross-section `dσ/dΩ` and total cross-section `σ` and fit to theoretical predictions, which are a function of the coupling constants.
        expected_signals: [Specific angular distribution of scattered particles, Energy-dependent total cross-section `σ(E)`]
        pitfalls: [Ignoring contributions from other vertices (t-channel, u-channel), Poor beam energy resolution, Inefficient detector coverage]
context_windows:
  - module: MATH-011
    excerpt: |
      Expand the potential around a vacuum ((C_0,\Gamma_0)):
      [ V = V_0 + m_C^2|\delta C|^2 + \tfrac12 m_\Gamma^2 (\delta\Gamma)^2 + \lambda_1 |\delta C|^4 + \lambda_2 (\delta\Gamma)^4 + g, |\delta C|^2,\delta\Gamma + \cdots. ]
      Vertices follow from derivatives of (V). Example: the cubic (g|C|^2\Gamma) gives a vertex with two coheron legs and one pressuron leg of strength (-ig). **Do not pre-identify (g) with the fine-structure constant**; treat it as a parameter to be fixed by data (or matched to a UV theory).
  - module: MATH-011
    excerpt: |
      If (m_\Gamma > 2 m_C) and (g|C|^2\Gamma) is present, the pressuron can decay (\Gamma\to C\bar C) with width
      [ \Gamma_{\Gamma\to C\bar C} = \frac{g^2}{8\pi m_\Gamma}\sqrt{1-\frac{4m_C^2}{m_\Gamma^2}}. ]
      This provides a clean handle to constrain (g) from non-observation.
poetic_connections:
  motifs: [crossroads, confluence, symphony, transformation, coupling, event]
  evocative_lines:
    - "giving a voice to the hum"
    - "a living, breathing symphony of probabilities"
    - "the rules of their interaction"
  association_matrix:
    - [ "FEYNMAN_DIAGRAM", 0.9 ]
    - [ "COHERON", 0.7 ]
    - [ "PRESSURON", 0.7 ]
    - [ "COUPLING_CONSTANT", 1.0 ]
    - [ "SCATTERING_AMPLITUDE", 0.8 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Feynman Vertex
      domain: QFT
      mapping_kind: mathematical
      equation_hint: |
        V_{int} = g \phi_1 \phi_2 \phi_3  →  Vertex Rule = -ig
      rationale: |
        The Interaction Vertex in the Pirouette Framework is derived by taking functional derivatives of the interaction terms in the action, exactly analogous to the standard procedure for deriving Feynman rules in quantum field theory. It is the momentum-space representation of a local interaction term in the Lagrangian.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The `g|C|^2Γ` vertex mediates the decay of a Pressuron into a Coheron-anti-Coheron pair if `m_Γ > 2m_C`."
      domain: phenomenology
      falsifier: "Experimental observation of a Pressuron with `m_Γ > 2m_C` that does not decay into `C-anti-C` pairs, or does so with a rate orders of magnitude different from the tree-level prediction, would refute the existence or assumed strength of this vertex."
      status: proposed
      links: [MATH-011, XXP-013]
    - statement: "All valid interaction vertices must correspond to terms in the interaction potential `V` that are allowed by the theory's symmetries."
      domain: theory
      falsifier: "Observation of a particle process (e.g., a decay or scattering event) that is forbidden by all specified vertices would falsify the completeness of the interaction potential `V`."
      status: supported
      links: [MATH-011]
naming_notes:
  collisions: [Vertex (graph theory), Vertex (geometry)]
  disambiguation: |
    An Interaction Vertex is not a physical point in space, but a node in an abstract Feynman diagram representing the spacetime point of a quantum interaction. Its "strength" is not a geometric property but the value of the associated coupling constant.
crosslinks:
  near_synonyms: [COUPLING_CONSTANT]
  antonyms: [FREE_PROPAGATOR]
  prerequisites: [PIROUETTE_LAGRANGIAN, COHERON, PRESSURON, FEYNMAN_DIAGRAM]
  downstream_effects: [SCATTERING_AMPLITUDE, DECAY_WIDTH, LOOP_CORRECTION]
license: CC-BY-SA-4.0
---

# Interaction Vertex

## Canonical (Pirouette)
A fundamental rule for constructing Feynman diagrams, derived from a specific interaction term in the Pirouette potential `V(|C|^2, Γ)`. An interaction vertex represents a local, point-like event where a specific number of Coheron and/or Pressuron world-lines meet. The structure of the vertex (which particles participate) is fixed by the fields in the interaction term, and its strength is determined by the associated coupling constant (e.g., `g`, `λ`). Every vertex conserves four-momentum.

## EFT-First Summary
The Interaction Vertex is the Pirouette Framework's direct analog of the standard **Feynman Vertex** in Quantum Field Theory (QFT). It is a mathematical rule, represented graphically as a node where particle lines meet, that is derived directly from interaction terms (e.g., `g|C|^2Γ`) in the theory's Lagrangian. The value associated with the vertex, the coupling constant, is a fundamental parameter of the effective field theory that must be determined by experiment, for example by measuring particle decay rates or scattering cross-sections.

## Glossary Links
- See also: [Coheron](<./COHERON.md>), [Pressuron](<./PRESSURON.md>), [Feynman Diagram](<./FEYNMAN_DIAGRAM.md>), [Coupling Constant](<./COUPLING_CONSTANT.md>)