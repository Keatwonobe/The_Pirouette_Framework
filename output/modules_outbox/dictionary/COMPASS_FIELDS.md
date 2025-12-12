---
term: "Compass Fields"
canonical_id: "COMPASS_FIELDS"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-019"]
---

---
term: Compass Fields
canonical_id: COMPASS_FIELDS
symbol: E_μ, B_μ
aliases: [Cosmic Compass, Coherence Compass]
parents: [MATH-019]
children: [PHEN-004, PHEN-007]
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-019
      snippet: |
        6. Compass Fields
           Metaphor: “Cosmic compass / coherence compass”
           Math: Two‑form sector 𝔉 decomposed via Hodge into electric‑like and magnetic‑like 1‑forms relative to u^μ (fluid frame). Define E_μ = F_{μν}u^ν, B_μ = ⋆F_{μν}u^ν.
  editors: [system-ai-20251018]
  review_log: []
triad:
  art: |
    The universe's flow provides a local north, splitting the raw potential of coherence into a directed force and a swirling vortex. This act of observation turns an abstract curvature into a tangible compass pointing along the observer's worldline.
  law: |
    Relative to any timelike observer with 4-velocity u^μ, the coherence curvature 2-form F_{μν} uniquely splits into an electric-like vector E_μ and a magnetic-like pseudovector B_μ. Both fields are purely spatial with respect to the observer (E_μ u^μ = 0, B_μ u^μ = 0).
  philosophy: |
    This decomposition is the essential bridge from abstract gauge geometry to operational physics. It grounds the invariant curvature F_{μν} in the contingent, observer-dependent reality of forces and torques, making the framework's predictions locally measurable and intuitive.
pirouette_definition: |
  The Compass Fields are the electric-like vector field E_μ and the magnetic-like pseudovector field B_μ that result from the decomposition of the coherence curvature 2-form F_{μν} with respect to a local fluid frame's 4-velocity u^μ. They are defined by the contractions E_μ = F_{μν}u^ν and B_μ = ⋆F_{μν}u^ν, where ⋆ is the Hodge dual. By construction, both fields are spacelike and orthogonal to the observer's velocity.
operational_definition:
  units: Coherence Units (inverse area, e.g., τ_p⁻²)
  symbol_table:
    - name: E_μ
      meaning: Electric-like component of coherence curvature
      dimensions: L⁻²
      default_range: contextual
    - name: B_μ
      meaning: Magnetic-like component of coherence curvature
      dimensions: L⁻²
      default_range: contextual
    - name: F_{μν}
      meaning: Coherence curvature 2-form
      dimensions: L⁻²
      default_range: contextual
    - name: u^μ
      meaning: 4-velocity of the local fluid frame
      dimensions: dimensionless
      default_range: u^μ u_μ = -1
    - name: ⋆F_{μν}
      meaning: Hodge dual of the coherence curvature
      dimensions: L⁻²
      default_range: contextual
  measurement:
    procedures:
      - name: Infer from Spinor Dynamics
        outline: |
          Measure the precession or acceleration of a test spinor coupled to the coherence field. The equation of motion, involving the term σ^{μν}F_{μν}, can be decomposed into E- and B-like couplings in the spinor's rest frame. By measuring spin precession (related to B_μ) and Stark-like level shifts or acceleration (related to E_μ), one can reconstruct the local Compass Field components.
        expected_signals: [Zeeman-like splitting of energy levels, acceleration of coherence-charged particles]
        pitfalls: [Isolating the Pirouette effects from Standard Model electromagnetic forces, defining a non-perturbative "test spinor"]
context_windows:
  - module: MATH-019
    excerpt: |
      Two‑form sector 𝔉 decomposed via Hodge into electric‑like and magnetic‑like 1‑forms relative to u^μ (fluid frame). Define E_μ = F_{μν}u^ν, B_μ = ⋆F_{μν}u^ν. This decomposition is critical for interpreting interactions, such as the Pauli term σ^{μν}F_{μν} in the spinor self-energy, which gives rise to the anomalous moment.
  - module: PHEN-007
    excerpt: |
      The calculation of the electron EDM `d_e` requires evaluating the interaction `ψ̄ iσ^{μν}γ_5 ψ F_{μν}`. In the rest frame of the electron, where `u^μ = (1, 0, 0, 0)`, this simplifies significantly. The interaction can be expressed in terms of the Compass Fields as `d_e (B · σ - i E · γ_5 σ)`, cleanly separating the magnetic and electric-like contributions to the CP-violating energy shift.
poetic_connections:
  motifs: [orientation, splitting, flow, duality, observer-dependence]
  evocative_lines:
    - "Cosmic compass"
    - "Splitting the formless into force and flow."
  association_matrix:
    - [ "COHERENCE_CURVATURE", 0.9 ]
    - [ "ELECTRON_EDM", 0.7 ]
    - [ "SOLITON_ECHO_G_MINUS_2", 0.7 ]
    - [ "COHERENCE_CURRENT", 0.5 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Observer-frame E and B fields in GR
      domain: GR|Electromagnetism
      mapping_kind: mathematical
      equation_hint: |
        E_μ = F_{μν}u^ν
        B_μ = (1/2) ε_{μνρσ} u^ν F^{ρσ} = (⋆F)_{μν} u^ν
      rationale: |
        The Pirouette definition is a direct adoption of the standard 3+1 ("threading") decomposition of any 2-form tensor relative to a timelike observer 4-velocity u^μ. This formalism is used ubiquitously in general relativity to define local electric and magnetic fields in a covariant way. The Compass Fields are simply this construct applied to the coherence curvature F_{μν} rather than the electromagnetic Faraday tensor.
      references:
        - title: General Relativity
          where: Robert M. Wald, University of Chicago Press, Chapter 4.3
          date: 1984-01-01
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "For any timelike 4-velocity field u^μ, the coherence curvature F_{μν} can be uniquely and covariantly decomposed into an electric-like field E_μ and a magnetic-like field B_μ, both orthogonal to u^μ."
      domain: theory
      falsifier: "Demonstrating that the fluid frame u^μ is ill-defined in a relevant physical regime, or that physical observables depend on a different, non-orthogonal decomposition of F_{μν}."
      status: supported
      links: [MATH-019]
naming_notes:
  collisions: [E (Electric Field), B (Magnetic Field)]
  disambiguation: |
    The symbols E_μ and B_μ are chosen to be deliberately analogous to their counterparts in electromagnetism. In contexts where both the coherence field and EM field are present, they must be distinguished, e.g., E_μ^{(coh)} and E_μ^{(EM)}. The 'Compass' name emphasizes their role in providing a local orientation relative to the coherence fluid, rather than being fundamental fields themselves.
crosslinks:
  near_synonyms: []
  antonyms: [COHERENCE_CURVATURE]
  prerequisites: [COHERENCE_CURVATURE]
  downstream_effects: [ELECTRON_EDM, SOLITON_ECHO_G_MINUS_2]
license: CC-BY-SA-4.0
---

# Compass Fields

## Canonical (Pirouette)
The Compass Fields are the electric-like vector field E_μ and the magnetic-like pseudovector field B_μ that result from the decomposition of the coherence curvature 2-form F_{μν} with respect to a local fluid frame's 4-velocity u^μ. They are defined by the contractions E_μ = F_{μν}u^ν and B_μ = ⋆F_{μν}u^ν, where ⋆ is the Hodge dual. By construction, both fields are spacelike and orthogonal to the observer's velocity.

## EFT-First Summary
In the language of general relativity and field theory, the Compass Fields are the standard observer-dependent electric and magnetic parts of a generalized U(1) field strength tensor `F_{μν}`. This 3+1 decomposition, defined by `E_μ = F_{μν}u^ν` and `B_μ = ⋆F_{μν}u^ν` with respect to a local fluid 4-velocity `u^μ`, is a standard technique for isolating the physical force components experienced by an observer moving with the fluid. This formalism is identical to that used for the electromagnetic field in curved spacetime (cf. Wald, 1984).

## Glossary Links
- See also: [Coherence Curvature](DICT:COHERENCE_CURVATURE), [Electron EDM](DICT:ELECTRON_EDM)