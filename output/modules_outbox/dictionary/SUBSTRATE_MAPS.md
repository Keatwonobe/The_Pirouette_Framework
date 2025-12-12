---
term: "Substrate Maps"
canonical_id: "SUBSTRATE_MAPS"
symbol: "χ_S"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-026"]
---

---
term: Substrate Maps
canonical_id: SUBSTRATE_MAPS
symbol: χ_S
aliases: [Bare Coupling Functions]
parents: [MATH-026]
children: [DOMA-096, COG-RES-002, SOCIO-FIELD-003]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-026
      lines: "§9"
      snippet: |
        Substrate parameters (conductance, latency, noise spectra) renormalize into effective (a,b,c,λ,g). Practical rule: • Increase in latency → raises a (harder to cohere) • Increased noise at resonant bands → raises effective b (stronger nonlinear damping)... Mapping χ_S must be calibrated per domain, but flow topology (fixed points, eigenvalues) remains substrate-invariant.
  editors: [AI Assistant (gpt-4-turbo)]
  review_log: []
triad:
  art: |
    The grain of the wood, the hum of the wire, the friction of the crowd—all are whispered into the constants that chart the course of coherence. A substrate map is the ear that hears this whisper, translating the world's texture into the fates of form.
  law: |
    A substrate map χ_S is a set of functions {a(S), b(S), c(S), ...} that predicts the LPF couplings from a vector of measurable substrate properties S. The map is validated if the RG flow generated from these couplings correctly predicts the critical exponents (ν, β_P, etc.) and crossover behavior observed in the system.
  philosophy: |
    Substrate maps embody the principle that while every system is unique in its material composition, its collective behavior near a critical point is not. They are the instruments of universality, revealing the common dynamical laws that transcend the specific details of physical, cognitive, or social matter.
pirouette_definition: |
  Substrate Maps (χ_S) are a set of calibrated, domain-specific functions that translate a vector of measurable, microscopic physical properties of a system (the substrate, S) into the effective parameters {a, b, c, λ, g, ...} of the Landau–Pirouette Functional (LPF). These maps serve as the crucial input for the Renormalization Flow of Coherence, connecting substrate-level physics to universal, macroscopic phase behavior and critical exponents.
operational_definition:
  units: Transformation from physical units of substrate properties (e.g., seconds, watts) to the effective units of LPF parameters.
  symbol_table:
    - name: χ_S
      meaning: Substrate Map; a functional S → {a, b, c, ...}
      dimensions: Varies (functional map)
      default_range: N/A
    - name: S
      meaning: Vector of measurable substrate properties
      dimensions: Varies per component (e.g., T for latency, M L^2 T^-3 for noise power)
      default_range: contextual
    - name: a, b, c
      meaning: LPF effective couplings
      dimensions: Defined by the LPF action being dimensionless.
      default_range: contextual
  measurement:
    procedures:
      - name: Substrate Parameter Sweep Calibration
        outline: |
          1. Identify key substrate properties (S_i) hypothesized to control coherence (e.g., neural latency, social network density, material conductivity).
          2. Systematically vary one S_i while holding others constant.
          3. At each S_i value, measure system-level observables (e.g., susceptibility χ_P, correlation length ξ).
          4. Fit the LPF to these observables to extract the effective parameters (a, b, c,...).
          5. The resulting function, e.g., a(S_i), is a component of the substrate map χ_S.
        expected_signals: [Smooth, monotonic dependence of LPF parameters on swept substrate parameters]
        pitfalls: [Confounding variables where multiple substrate properties co-vary, Non-equilibrium effects if the system does not fully relax between parameter sweeps]
context_windows:
  - module: MATH-026
    excerpt: |
      Substrate parameters (conductance, latency, noise spectra) renormalize into effective (a,b,c,λ,g). Practical rule: • Increase in latency → raises a (harder to cohere) • Increased noise at resonant bands → raises effective b (stronger nonlinear damping) • Bandwidth constraints → renormalize c (stiffer gradients). Mapping χ_S must be calibrated per domain, but flow topology (fixed points, eigenvalues) remains substrate-invariant.
  - module: MATH-026
    excerpt: |
      The LPF's control fields include substrate constants, S, which enter through the potential term U(Γ,S) and implicitly define the bare values of a, b, and c before renormalization. A substrate map χ_S makes this dependence explicit, providing the initial conditions for the RG flow from the microscopic scale.
poetic_connections:
  motifs: [translation, distillation, texture, materiality, universality]
  evocative_lines:
    - "...flow topology (fixed points, eigenvalues) remains substrate-invariant."
    - "Caduceus Lens as RG flow on laminar ↔ turbulent manifolds."
  association_matrix:
    - [ "UNIVERSALITY_CLASS", 0.9 ]
    - [ "LANDAU_PIROUETTE_FUNCTIONAL", 0.8 ]
    - [ "COHERENCE", 0.6 ]
    - [ "TEMPORAL_PRESSURE", 0.5 ]
formal_mappings:
  candidates:
    - target: Bare couplings in a Landau-Ginzburg-Wilson effective field theory
      domain: EFT
      mapping_kind: conceptual
      equation_hint: |
        L_EFT = (∂ϕ)² + r₀ ϕ² + u₀ ϕ⁴ + ... , where χ_S: {T, P, J_ij, ...} → {r₀, u₀}
      justification: |
        Substrate maps are analogous to the process in condensed matter physics where microscopic model parameters (e.g., from an Ising or Hubbard model) are mapped onto the parameters of a coarse-grained Landau-Ginzburg effective field theory. This 'integrating out' of high-energy modes to define a low-energy theory is the conceptual basis for χ_S.
      references:
        - title: Lectures on Phase Transitions and the Renormalization Group
          where: N. Goldenfeld, Westview Press
          date: 1992-01-01
      confidence: 0.95
  adopted:
    - target: Bare couplings in a Landau-Ginzburg-Wilson effective field theory
      rationale: The Pirouette Framework explicitly models its Renormalization Flow of Coherence (RFC) on Wilson's RG approach to critical phenomena. The Substrate Map is the direct analog of determining the initial ('bare') parameters of the LGW functional from the underlying microscopic physics of a specific material or system.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The topology of the RG flow (i.e., the existence and stability of the Pirouette Wilson-Fisher fixed point) is independent of the specific substrate, even though the starting point of the flow, determined by χ_S, is substrate-dependent."
      domain: phenomenology
      falsifier: "Discovering a system described by the LPF that exhibits a phase transition belonging to a different universality class (i.e., with different critical exponents) than predicted by the Pirouette Wilson-Fisher fixed point."
      status: proposed
      links: [MATH-026]
    - statement: "The practical rules provided in MATH-026 (§9), such as 'increased latency → raises a', are directionally correct for all substrates within the Pirouette domain of applicability."
      domain: experiment
      falsifier: "An experimental calibration on a new substrate shows that increased signal latency systematically lowers the effective 'a' parameter, promoting coherence, which would invalidate the proposed general mapping rule."
      status: proposed
      links: [MATH-026]
naming_notes:
  collisions: [The symbol χ is standard for susceptibility. In Pirouette, coherence susceptibility is χ_P, while the substrate map is χ_S. The subscript is non-optional to avoid ambiguity.]
  disambiguation: |
    A Substrate Map (χ_S) is not a physical map or chart of a system. It is a *functional mapping* from a system's physical properties to the abstract parameter space of the LPF. It is the 'lookup table' that connects reality to the theory.
crosslinks:
  near_synonyms: [BARE_COUPLING_FUNCTIONS]
  antonyms: [UNIVERSAL_QUANTITIES]
  prerequisites: [LANDAU_PIROUETTE_FUNCTIONAL, SUBSTRATE]
  downstream_effects: [RENORMALIZATION_FLOW_OF_COHERENCE, PIRIOUETTE_WILSON_FISHER_POINT]
license: CC-BY-SA-4.0
---

# Substrate Maps

## Canonical (Pirouette)
Substrate Maps (χ_S) are a set of calibrated, domain-specific functions that translate a vector of measurable, microscopic physical properties of a system (the substrate, S) into the effective parameters {a, b, c, λ, g, ...} of the Landau–Pirouette Functional (LPF). These maps serve as the crucial input for the Renormalization Flow of Coherence, connecting substrate-level physics to universal, macroscopic phase behavior and critical exponents.

## EFT-First Summary
In the language of effective field theory, a Substrate Map χ_S is the procedure for determining the "bare" couplings (e.g., r₀, u₀) of a Landau-Ginzburg-Wilson action by starting from the microscopic physics of a specific material. It provides the initial conditions for the renormalization group flow, connecting a system's unique physical properties (like lattice spacing or interaction strength) to its universal critical behavior.

## Glossary Links
- See also: Renormalization Flow of Coherence (RFC), Landau–Pirouette Functional (LPF), Universality Class