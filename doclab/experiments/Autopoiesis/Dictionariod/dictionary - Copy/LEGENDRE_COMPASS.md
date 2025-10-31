---
term: "Legendre Compass"
canonical_id: "LEGENDRE_COMPASS"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-144"]
---

---
term: Legendre Compass
canonical_id: LEGENDRE_COMPASS
symbol: (∂•/∂•)_•
aliases: [Legendre transform]
parents: [DOMA-144]
children: []
status: ratified
version: 2.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-144
      lines: "L92-L106"
      snippet: |
        The mathematical tool for moving between these different viewpoints is the Legendre transform. We conceive of this not as a mere formula, but as a **Legendre Compass**—a tool for navigating the system's unified coherence manifold.
        Taking a partial derivative is not an abstract operation; it is the act of asking a precise question.
  editors: [Agent (System)]
  review_log: []
triad:
  art: |
    A single mountain can be mapped from any starting point. The Compass is the tool that transforms one known path into a topographical map of the entire landscape, revealing the unity of all possible perspectives.
  law: |
    The partial derivative of a thermodynamic potential with respect to one of its natural variables yields the conjugate variable. For a potential Φ(x, y, ...), the conjugate to x is ξ = (∂Φ/∂x)_y,.... This operation allows for the systematic reconstruction of the entire Coherence Ledger from a single known potential.
  philosophy: |
    The act of mathematical transformation is an act of physical inquiry. The Compass reframes a formal procedure as a set of targeted questions one can ask a system, revealing that the interconnectedness of thermodynamic variables is a direct consequence of an underlying, unified state manifold.
pirouette_definition: |
  The Legendre Compass is the conceptual model and operational protocol for navigating the unified coherence manifold. It re-frames the mathematical Legendre transform as the physical act of asking a targeted question by taking a partial derivative of a thermodynamic potential with respect to one of its natural variables. This process reveals the conjugate variable, allowing a Weaver to move between different accounting perspectives (e.g., Gibbs Free Energy to Entropy) and reconstruct the system's complete Coherence Ledger from a single starting point.
operational_definition:
  units: Operator (dimensionless, but acts on physical quantities)
  symbol_table:
    - name: Φ
      meaning: A generic thermodynamic potential (e.g., F, G, U, H).
      dimensions: Energy (M L² T⁻²)
      default_range: contextual
    - name: xᵢ
      meaning: A natural variable of the potential Φ (e.g., T, P, V).
      dimensions: contextual
      default_range: contextual
    - name: x̃ᵢ
      meaning: The conjugate variable to xᵢ.
      dimensions: contextual
      default_range: contextual
    - name: (∂Φ/∂xᵢ)_xⱼ
      meaning: The partial derivative of Φ with respect to xᵢ, while holding all other natural variables xⱼ (j≠i) constant. The result is the conjugate variable x̃ᵢ.
      dimensions: [Φ]/[xᵢ]
      default_range: contextual
  measurement:
    procedures:
      - name: State Manifold Navigation
        outline: |
          1.  Select a known thermodynamic potential, Φ, expressed in its natural variables (e.g., G(T,P)). This is the "anchor point."
          2.  Identify a target conjugate variable to determine (e.g., Entropy, S).
          3.  Apply the Compass: compute the appropriate partial derivative of the anchor potential (e.g., S = -(∂G/∂T)_P).
          4.  Repeat for all natural variables to find all conjugate variables (e.g., V = (∂G/∂P)_T).
          5.  Use the derived variables and the anchor potential to algebraically construct all other potentials in the Coherence Ledger (e.g., H = G + TS).
        expected_signals: [A consistent set of state functions for U, F, H, G, S, T, P, V.]
        pitfalls: [Incorrect identification of natural variables for the chosen anchor potential, algebraic errors in differentiation, applying the transform to a potential not expressed in its natural variables.]
context_windows:
  - module: DOMA-144
    excerpt: |
      The mathematical tool for moving between these different viewpoints is the Legendre transform. We conceive of this not as a mere formula, but as a **Legendre Compass**—a tool for navigating the system's unified coherence manifold. Taking a partial derivative is not an abstract operation; it is the act of asking a precise question.
  - module: DOMA-144
    excerpt: |
      Calculating **S = - (∂G/∂T)_P** is asking: "If I hold the external pressure (P) fixed and slightly increase the environmental noise (T), how much does the system's capacity for practical work (G) decrease?" The answer reveals the system's internal susceptibility to disorder—its Entropy (S). The Legendre Compass allows a Weaver to chart the entire manifold of state by making a series of these careful, targeted inquiries from a single starting point.
poetic_connections:
  motifs: [navigation, cartography, questioning, perspective-shifting, accounting]
  evocative_lines:
    - "Taking a partial derivative is not an abstract operation; it is the act of asking a precise question."
    - "You have transformed one complete path up the mountain into a topographical map of the entire mountain."
  association_matrix:
    - [ "COHERENCE_LEDGER", 0.9 ]
    - [ "GIBBS_FREE_ENERGY", 0.7 ]
    - [ "STATE_RECONSTRUCTION", 0.8 ]
    - [ "COHERENCE_MANIFOLD", 0.9 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Legendre transformation
      domain: Math
      mapping_kind: mathematical
      equation_hint: |
        f*(p) = sup_x(px - f(x))
        Example: H(q,p) = p·(∂L/∂p) - L, where p = ∂L/∂q̇
      justification: |
        The Legendre Compass is the Pirouette framework's physical and operational interpretation of the standard Legendre transformation used in classical mechanics to switch from the Lagrangian to the Hamiltonian, and in thermodynamics to switch between potentials (U, F, H, G). The core mathematical operation is identical.
      references:
        - title: Classical Mechanics
          where: Chapter 8, "The Hamiltonian Method"
          date: 2002-01-01
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "Any complete thermodynamic potential, expressed in its natural variables, contains all information required to reconstruct the full Coherence Ledger via application of the Legendre Compass."
      domain: theory
      falsifier: "The discovery of two systems where the entropy S derived from G(T,P) is empirically inconsistent with the entropy S derived from F(T,V), after accounting for all other state variables. This would imply the manifold is not unified or navigable in this way."
      status: supported
      links: [DOMA-144]
naming_notes:
  collisions: [Legendre transform]
  disambiguation: |
    "Legendre transform" refers to the pure mathematical procedure. "Legendre Compass" is the Pirouette term for the *application* of this procedure as a tool for physical inquiry, emphasizing its role in navigating between different but equivalent descriptions of a single underlying physical state on the coherence manifold.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [COHERENCE_LEDGER, GIBBS_FREE_ENERGY, PIROUETTE_LAGRANGIAN]
  downstream_effects: [STATE_RECONSTRUCTION]
license: CC-BY-SA-4.0
---

# Legendre Compass

## Canonical (Pirouette)
The Legendre Compass is the conceptual model and operational protocol for navigating the unified coherence manifold. It re-frames the mathematical Legendre transform as the physical act of asking a targeted question by taking a partial derivative of a thermodynamic potential with respect to one of its natural variables. This process reveals the conjugate variable, allowing a Weaver to move between different accounting perspectives (e.g., Gibbs Free Energy to Entropy) and reconstruct the system's complete Coherence Ledger from a single starting point.

## EFT-First Summary
The Legendre Compass is the Pirouette framework's operational name for the Legendre transformation, the standard mathematical tool used in classical mechanics and thermodynamics to switch between equivalent physical descriptions. For example, it is the procedure used to transform the Lagrangian L(q, q̇) into the Hamiltonian H(q, p) or to derive entropy and volume from the Gibbs Free Energy G(T, P). This transformation is re-conceptualized not as a mere formality but as an active process of physical inquiry.

## Glossary Links
- See also: [COHERENCE_LEDGER](link), [STATE_RECONSTRUCTION](link), [GIBBS_FREE_ENERGY](link)