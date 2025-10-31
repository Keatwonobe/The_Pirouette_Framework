---
term: "Globally Hyperbolic Spacetime"
canonical_id: "GLOBALLY_HYPERBOLIC_SPACETIME"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-011"]
---

---
term: Globally Hyperbolic Spacetime
canonical_id: GLOBALLY_HYPERBOLIC_SPACETIME
symbol: 
aliases: []
parents: [MATH-011]
children: []
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-011
      lines: "L36-L38"
      snippet: |
        Backgrounds assumed **globally hyperbolic** so canonical quantization is well-defined; for curved backgrounds we also present the covariant path-integral.
  editors: [GPT-4]
  review_log: []
triad:
  art: |
    A well-behaved stage for the quantum symphony, ensuring the story of cause and effect has a clear beginning, middle, and end. It is the cosmic loom upon which the threads of reality can be woven without paradoxical knots or loose ends.
  law: |
    A spacetime is globally hyperbolic if it possesses a Cauchy surface—a slice of 'now' that is crossed exactly once by every possible history. This guarantees that initial data specified on this surface uniquely determine the entire past and future evolution of the Coherence and Temporal Pressure fields.
  philosophy: |
    This is the foundational assumption of predictability in physics. By postulating a globally hyperbolic background, we assert that the universe is not capricious; its state at one moment is sufficient to determine its entire history. This makes the quantization program meaningful, transforming a potential cacophony of paradoxes into a calculable, coherent song.
pirouette_definition: |
  A property of the background spacetime manifold, `(M, g)`, assumed in the quantization of the Pirouette Framework. It is the minimal condition required to ensure the classical equations of motion for the Coherence (C) and Temporal Pressure (Γ) fields are well-posed as an initial value problem. This well-posedness is a prerequisite for a non-pathological canonical quantization, a uniquely defined Coherence Propagator, and the causal propagation of quantum information.
operational_definition:
  units: Dimensionless (mathematical property)
  symbol_table:
    - name: (M, g)
      meaning: A Lorentzian manifold M with metric g, representing spacetime.
      dimensions: N/A
      default_range: N/A
    - name: Σ
      meaning: A Cauchy surface; a spacelike hypersurface.
      dimensions: L³
      default_range: N/A
  measurement:
    procedures:
      - name: Test of Predictability
        outline: |
          Assume the universe's spacetime is globally hyperbolic. Use this to formulate a predictive Quantum Coherence Field Theory (QCFT). Calculate S-matrix elements, cosmological observables (e.g., CMB power spectrum from an initial slice), and other causal phenomena. Compare these high-precision predictions with experimental or observational data.
        expected_signals:
          - Conservation of probability (Unitarity) in scattering experiments.
          - The success of cosmological models that evolve a primordial state forward to the present day.
          - Absence of observed signals arriving from the future (i.e., no naked singularities or closed timelike curves).
        pitfalls:
          - Mistaking the mathematical assumption for a physical law that must hold at all scales; it may break down at the Planck scale or inside black hole singularities.
          - Falsification is difficult, as a discrepancy could be due to other model failures rather than a failure of global hyperbolicity itself.
context_windows:
  - module: MATH-011
    excerpt: |
      We promote the classical Pirouette matter sector [...] to a quantum field theory on a (possibly curved) **globally hyperbolic** spacetime. Quantization yields quanta of (C) ("coherons", complex scalar) and of (\Gamma) ("pressurons", real scalar).
  - module: MATH-011
    excerpt: |
      Backgrounds assumed **globally hyperbolic** so canonical quantization is well-defined; for curved backgrounds we also present the covariant path-integral.
poetic_connections:
  motifs: [causality, predictability, foundation, stage, well-posedness, determinism]
  evocative_lines:
    - "We quantize the beats (fields) that sculpt coherence and pressure—not the clock itself."
    - "The act of quantization transforms our deterministic machine into a living symphony of probabilities."
  association_matrix:
    - [ "CANONICAL_QUANTIZATION", 0.9 ]
    - [ "COHERENCE_PROPAGATOR", 0.7 ]
    - [ "CAUSALITY", 0.9 ]
    - [ "INITIAL_VALUE_PROBLEM", 1.0 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Global Hyperbolicity
      domain: GR|Math
      mapping_kind: mathematical
      equation_hint: |
        A spacetime (M, g) is globally hyperbolic iff there exists a smooth function f: M → ℝ such that its level sets are Cauchy surfaces.
      justification: |
        The Pirouette Framework directly adopts the standard definition from General Relativity and mathematical physics without modification. This property, established by Geroch (1970), is the canonical condition for ensuring that partial differential equations, like the Klein-Gordon equation for the C and Γ fields, have unique global solutions given initial data.
      references:
        - title: General Relativity
          where: Chapter 8, R. M. Wald (1984)
          date: 1984-01-01
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The large-scale spacetime of our universe is well-approximated by a globally hyperbolic manifold."
      domain: phenomenology
      falsifier: "The confirmed observation of a naked singularity or a closed timelike curve, which would invalidate the existence of a global Cauchy surface and render prediction from initial data impossible."
      status: supported
      links: []
naming_notes:
  collisions: []
  disambiguation: |
    Global hyperbolicity is a strong causality condition. It is often confused with weaker conditions like chronology (no closed timelike curves) or causality (no closed causal curves). Global hyperbolicity implies these weaker conditions but adds the crucial requirement of a well-posed initial value problem, which is essential for quantization.
crosslinks:
  near_synonyms: []
  antonyms: [NAKED_SINGULARITY, CLOSED_TIMELIKE_CURVE]
  prerequisites: [LORENTZIAN_MANIFOLD, CAUSALITY_CONDITIONS]
  downstream_effects: [CANONICAL_QUANTIZATION, COHERENCE_PROPAGATOR, FEYNMAN_RULES]
license: CC-BY-SA-4.0
---

# Globally Hyperbolic Spacetime

## Canonical (Pirouette)
A property of the background spacetime manifold, `(M, g)`, assumed in the quantization of the Pirouette Framework. It is the minimal condition required to ensure the classical equations of motion for the Coherence (C) and Temporal Pressure (Γ) fields are well-posed as an initial value problem. This well-posedness is a prerequisite for a non-pathological canonical quantization, a uniquely defined Coherence Propagator, and the causal propagation of quantum information.

## EFT-First Summary
The Pirouette Framework adopts the standard definition of global hyperbolicity from General Relativity and Quantum Field Theory in Curved Spacetime. It is the essential assumption that guarantees the existence of a global time function and ensures that field equations (like the Klein-Gordon equation) have a well-posed initial value formulation. This allows for a consistent and predictive quantum theory by preventing pathologies such as naked singularities or closed timelike curves, thereby securing a stable causal structure on which to define quantum states and their evolution.

## Glossary Links
- See also: Canonical Quantization, Coherence Propagator, Causality