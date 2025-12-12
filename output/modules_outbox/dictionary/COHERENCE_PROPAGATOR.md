---
term: "Coherence Propagator"
canonical_id: "COHERENCE_PROPAGATOR"
symbol: "Δ_F^C"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-011"]
---

---
term: Coherence Propagator
canonical_id: COHERENCE_PROPAGATOR
symbol: Δ_F^C(x, x'), Δ_F^C(p)
aliases: [Coheron Propagator, C-field Propagator]
parents: [MATH-011]
children: [XXP-013]
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-011
      snippet: |
        Free Feynman propagators solve covariant Green equations:
        [ (\Box + m_C^2),\Delta_F^C(x,x') = -,\frac{i,\delta^{(4)}(x,x')}{\sqrt{-g}} ... ]
  editors: [system-ai-autocompiler]
  review_log: []
triad:
  art: |
    A quantum echo of coherence, propagating the possibility of a particle from one event to another. It is the path integral's fundamental whisper, carrying the amplitude for what might be.
  law: |
    The Coherence Propagator is the time-ordered two-point correlation function of the quantum Coherence field, Δ_F^C(x-y) = ⟨0|T{Ĉ(x)Ĉ†(y)}|0⟩. In momentum space, it is i / (p² - m_C² + iε), representing the amplitude for a coheron of four-momentum p to propagate.
  philosophy: |
    The propagator turns the abstract concept of a quantum field into a computational tool. It is the fundamental grammar of interaction, defining how influence travels and enabling the calculation of all phenomena arising from the exchange of coherons.
pirouette_definition: |
  The Coherence Propagator, Δ_F^C(x,x'), is the Feynman Green's function for the quantum Coherence field (C). It represents the amplitude for a coheron (or anti-coheron) to propagate between spacetime points x and x'. As the solution to (□ + m_C²)Δ_F^C = -iδ⁴(x-x') in Minkowski space, it serves as the internal line for coherons in all Feynman diagrams, forming the basis for perturbative calculations within Pirouette's Quantum Coherence Field Theory.
operational_definition:
  units: [Energy]⁻² or [Length]² (in natural units where ħ=c=1).
  symbol_table:
    - name: Δ_F^C
      meaning: Coherence Feynman Propagator
      dimensions: M⁻² L⁰ T⁰
      default_range: Complex-valued
    - name: p
      meaning: Four-momentum of the propagating coheron
      dimensions: M¹ L¹ T⁻¹
      default_range: contextual
    - name: m_C
      meaning: Rest mass of the coheron particle
      dimensions: M¹ L⁰ T⁰
      default_range: >0; constrained by experiment
    - name: ε
      meaning: Infinitesimal positive constant defining the Feynman contour
      dimensions: dimensionless
      default_range: → 0⁺
  measurement:
    procedures:
      - name: Indirect Inference via Particle Interactions
        outline: |
          The propagator itself is not directly measured. Its key parameter, the coheron mass m_C, is inferred by measuring physical processes that depend on it. This involves calculating a theoretical cross-section or decay rate using Feynman rules (which include Δ_F^C for internal coheron lines) and fitting the result to experimental data.
        expected_signals:
          - A resonance peak in a scattering cross-section at a center-of-mass energy s = m_C².
          - A specific decay width for processes like Γ → C C̄, whose rate depends on m_C.
          - Precision shifts in other observables (e.g., g-2 anomalies) from loop diagrams containing a coheron propagator.
        pitfalls:
          - Misattributing a resonance peak if multiple particles have similar masses.
          - Theoretical predictions require including loop corrections for high precision, introducing renormalization scheme dependence.
context_windows:
  - module: MATH-011
    excerpt: |
      Generating functional (sources (J_C,J_{C^*},J_\Gamma)):
      [ Z[J] = \int ! \mathcal D C,\mathcal D C^*,\mathcal D\Gamma; \exp!\left{ i!\int d^4x\sqrt{-g}, \big( \mathcal L + J_C C + J_{C^*} C^* + J_\Gamma \Gamma \big) \right}. ]
      Free Feynman propagators solve covariant Green equations:
      [ (\Box + m_C^2),\Delta_F^C(x,x') = -,\frac{i,\delta^{(4)}(x,x')}{\sqrt{-g}},\qquad (\Box + m_\Gamma^2),\Delta_F^\Gamma(x,x') = -,\frac{i,\delta^{(4)}(x,x')}{\sqrt{-g}}. ]
      In Minkowski space these reduce to the usual momentum-space (i/(p^2-m^2+i\epsilon)).
  - module: MATH-011
    excerpt: |
      If (m_\Gamma > 2 m_C) and (g|C|^2\Gamma) is present, the pressuron can decay (\Gamma\to C\bar C) with width
      [ \Gamma_{\Gamma\to C\bar C} = \frac{g^2}{8\pi m_\Gamma}\sqrt{1-\frac{4m_C^2}{m_\Gamma^2}}. ]
      This provides a clean handle to constrain (g) from non-observation.
poetic_connections:
  motifs: [quantum echo, ripple of possibility, virtual exchange, amplitude path]
  evocative_lines:
    - "It is the step that allows the framework to speak of not just the path that is, but of all paths that could be..."
    - "Giving a Voice to the Hum"
  association_matrix:
    - [ "COHERON", 0.9 ]
    - [ "INTERACTION_VERTEX", 0.8 ]
    - [ "FEYNMAN_DIAGRAM", 0.9 ]
    - [ "QUANTUM_COHERENCE_FIELD", 0.7 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Klein-Gordon Feynman Propagator
      domain: QFT
      mapping_kind: mathematical
      equation_hint: |
        Δ_F^C(p) ≡ i / (p² - m_C² + iε)
      justification: |
        The definition of Δ_F^C in MATH-011 is mathematically identical to the standard Feynman propagator for a complex scalar (spin-0) field in quantum field theory. This is not an analogy but a direct application of a standard QFT tool to the Pirouette Framework's Coherence field.
      references:
        - title: An Introduction to Quantum Field Theory
          where: Peskin & Schroeder, Ch. 2
          date: 1995-10-12
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The Coherence Propagator has a single, simple pole on the real momentum axis at p² = m_C², corresponding to a stable, on-shell coheron particle."
      domain: theory
      falsifier: "Experimental observation of coheron decay would imply its mass m_C has an imaginary part (m_C² → m_C² - i m_C Γ_C), shifting the propagator's pole off the real axis. Alternatively, if coherons are found to be composite, the propagator would be a more complex function without a simple pole, revealed by deviations from predicted scattering amplitudes at high energies."
      status: proposed
      links: [MATH-011]
naming_notes:
  collisions: [Δ is a common symbol for the Laplacian operator and for finite differences. The subscripts 'F' for Feynman and 'C' for Coherence are essential for disambiguation.]
  disambiguation: |
    This is the propagator for the Coherence field (C) and its quantum, the coheron. It must not be confused with the Pressuron Propagator (Δ_F^Γ) or with propagators for Standard Model particles. The 'C' superscript is mandatory.
crosslinks:
  near_synonyms: []
  antonyms: [INTERACTION_VERTEX]
  prerequisites: [COHERON, QUANTUM_COHERENCE_FIELD]
  downstream_effects: [FEYNMAN_DIAGRAM]
license: CC-BY-SA-4.0
---

# Coherence Propagator

## Canonical (Pirouette)
The Coherence Propagator, Δ_F^C(x,x'), is the Feynman Green's function for the quantum Coherence field (C). It represents the amplitude for a coheron (or anti-coheron) to propagate between spacetime points x and x'. As the solution to (□ + m_C²)Δ_F^C = -iδ⁴(x-x') in Minkowski space, it serves as the internal line for coherons in all Feynman diagrams, forming the basis for perturbative calculations within Pirouette's Quantum Coherence Field Theory.

## EFT-First Summary
In the language of standard Quantum Field Theory, the Coherence Propagator is the Feynman propagator for a complex scalar field (the coheron) with mass m_C. Its momentum-space form, i / (p² - m_C² + iε), is the fundamental building block for calculating any physical process involving the exchange of real or virtual coherons, from simple particle decays to complex loop corrections. Its structure is dictated by the Klein-Gordon equation and the principles of causality.

## Glossary Links
- See also: [Coheron](term:COHERON), [Interaction Vertex](term:INTERACTION_VERTEX), [Pressuron Propagator](term:PRESSURON_PROPAGATOR)