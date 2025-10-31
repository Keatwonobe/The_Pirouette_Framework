---
term: "Coheron"
canonical_id: "COHERON"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-011"]
---

---
term: Coheron
canonical_id: COHERON
symbol: C
aliases: [C-quantum, Coherence quantum]
parents: [MATH-011]
children: [XXP-013]
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-011
      snippet: |
        The quanta created by (a^\dagger) (coheron), (b^\dagger) (anti-coheron), and (c^\dagger) (pressuron) furnish one-particle states.
  editors: [auto-fill agent]
  review_log: []
triad:
  art: |
    The discrete echo in the symphony of phase; a single, resonant note plucked from the continuous hum of the Coherence field. It is the carrier of the universe's capacity for mutual understanding.
  law: |
    A complex scalar particle (spin-0) with mass `m_C` and a conserved U(1) charge, arising as the fundamental excitation of the Coherence field `C`. It interacts via vertices derived from the potential `V(|C|^2, Γ)`.
  philosophy: |
    The Coheron embodies the principle that coherence itself is not just a background property but a physical, quantized substance. It acts as the fundamental messenger of phase information and resonant coupling between systems, transforming abstract relationships into tangible interactions.
pirouette_definition: |
  The Coheron is the quantum of the complex scalar Coherence field, `C`. It is a spin-0 particle with mass `m_C` and an associated anti-particle (the anti-coheron), distinguished by a conserved charge arising from the global U(1) phase symmetry of the Pirouette Lagrangian. Coherons are created and annihilated by operators satisfying canonical commutation relations, and their interactions are governed by the potential `V(|C|^2, Γ)`.
operational_definition:
  units: Joules (J) or electron-volts (eV) for mass.
  symbol_table:
    - name: C
      meaning: Coherence field operator
      dimensions: M^(1/2) L^(-1/2) (in natural units)
      default_range: contextual
    - name: m_C
      meaning: Mass of the Coheron
      dimensions: M
      default_range: > 0 (experimentally unconstrained)
    - name: a†, b†
      meaning: Creation operators for coheron and anti-coheron
      dimensions: dimensionless
      default_range: N/A
  measurement:
    procedures:
      - name: Resonance Decay Search
        outline: |
          If a heavier particle (e.g., the Pressuron `Γ`) can decay into a coheron/anti-coheron pair (`Γ → C C̄`), search for this decay channel. As coherons are likely invisible to Standard Model detectors, this appears as a parent particle decaying into missing energy. The decay width is a direct function of the coupling `g` and masses `m_Γ, m_C`, as in `Γ ∝ g² f(m_C/m_Γ)`.
        expected_signals:
          - A new decay mode for a known or new particle with a specific branching ratio.
          - A peak in a missing mass spectrum corresponding to `m_Γ` in experiments producing `C C̄` pairs.
        pitfalls:
          - Differentiating the signal from decays into neutrinos, which also produce missing energy.
          - The decay may be kinematically forbidden (`m_Γ < 2m_C`) or have a suppressed branching ratio.
context_windows:
  - module: MATH-011
    excerpt: |
      **Coheron ((C)-quantum):** scalar excitation of the coherence field. Unless you extend the field content, coherons are *not* SM fermions; they can mix/mediate with SM via portals specified in (V) or via gauge couplings.
  - module: MATH-011
    excerpt: |
      With (V⊃ m_C^2|C|^2 + ⋯), the free solutions decompose as
      [ \hat C(x) = \int_\mathbf p \frac{1}{\sqrt{2E_{\mathbf p}^C}}\left( a_{\mathbf p} e^{-ip\cdot x} + b^\dagger_{\mathbf p} e^{ip\cdot x}\right), \quad \cdots ]
      with (E_{\mathbf p}^{C}=\sqrt{\mathbf p^2+m_{C}^2}). The quanta created by (a^\dagger) (coheron), (b^\dagger) (anti-coheron)... furnish one-particle states.
poetic_connections:
  motifs: [resonance, phase, quantum, echo, carrier, messenger]
  evocative_lines:
    - "Giving a Voice to the Hum"
    - "The act of quantization transforms our deterministic machine into a living symphony of probabilities."
  association_matrix:
    - [ "COHERENCE_FIELD", 0.9 ]
    - [ "PRESSURON", 0.7 ]
    - [ "INTERACTION_VERTEX", 0.6 ]
    - [ "CANONICAL_QUANTIZATION", 0.5 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Complex Scalar Field
      domain: QFT
      mapping_kind: mathematical
      equation_hint: |
        L = (∂µ C)* (∂µ C) - m² |C|² - λ |C|⁴
      justification: |
        The Coheron is defined as the quantum of a complex scalar field `C` with a U(1) global symmetry. This is a textbook example in quantum field theory, and its dynamics (Klein-Gordon equation), quantization (canonical commutation relations), and conserved charge (Noether's theorem) are standard constructions.
      references:
        - title: An Introduction to Quantum Field Theory
          where: Peskin & Schroeder, Chapter 2
          date: 1995-10-01
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The Coheron is a fundamental scalar particle (spin-0)."
      domain: experiment
      falsifier: "Observation of a Coheron candidate with measured non-zero spin, determined, for example, from the angular distribution of its decay products."
      status: proposed
      links: [MATH-011]
    - statement: "The Coheron possesses a conserved charge, implying coheron number is conserved in interactions (coherons and anti-coherons are created/destroyed in pairs)."
      domain: theory
      falsifier: "A well-motivated and observed process that violates this U(1) symmetry, such as Coheron-oscillations or charge-violating decays."
      status: proposed
      links: [MATH-011]
naming_notes:
  collisions: [The symbol `C` is overloaded, commonly representing capacitance, the set of complex numbers, or the speed of light (c).]
  disambiguation: |
    Distinguish the Coheron (the particle) from the Coherence field `C` (the field it quantizes). Context usually clarifies whether `C` refers to the field operator or the particle state. The Coheron is fundamentally distinct from all Standard Model particles, most critically by its spin-0 nature, which prevents it from being a fermion like an electron.
crosslinks:
  near_synonyms: [COHERENCE_FIELD_QUANTUM]
  antonyms: []
  prerequisites: [COHERENCE_FIELD, CANONICAL_QUANTIZATION]
  downstream_effects: [PRESSURON_DECAY, INTERACTION_VERTEX]
license: CC-BY-SA-4.0
---

# Coheron

## Canonical (Pirouette)
The Coheron is the quantum of the complex scalar Coherence field, `C`. It is a spin-0 particle with mass `m_C` and an associated anti-particle (the anti-coheron), distinguished by a conserved charge arising from the global U(1) phase symmetry of the Pirouette Lagrangian. Coherons are created and annihilated by operators satisfying canonical commutation relations, and their interactions are governed by the potential `V(|C|^2, Γ)`.

## EFT-First Summary
In the language of effective field theory, the Coheron is the quantum of a standard complex scalar field `C` with a global U(1) symmetry. Its mass `m_C` and coupling constants (e.g., `g` to the Pressuron field, or the self-coupling `λ`) are treated as free parameters of the EFT, to be constrained by experiment. Its dynamics are described by the Klein-Gordon equation, and its interactions are determined by the symmetry-allowed terms in the potential V(|C|², Γ). See: *Peskin & Schroeder, An Introduction to Quantum Field Theory*.

## Glossary Links
- See also: Pressuron, Coherence Field, Interaction Vertex