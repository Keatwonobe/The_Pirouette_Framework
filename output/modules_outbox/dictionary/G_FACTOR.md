---
term: "g-factor"
canonical_id: "G_FACTOR"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["CORE-009_the_electron's_echo"]
---

---
term: g-factor
canonical_id: G_FACTOR
symbol: g
aliases: [gyromagnetic ratio, Landé g-factor, anomalous magnetic moment]
parents: [CORE-009]
children: [CORE-010_placeholder]
status: candidate
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: CORE-009
      lines: "§3"
      snippet: |
        The Baseline (g=2): In classical physics, the g-factor for a spinning object is g=1. The electron's baseline g-factor of g=2 is a direct consequence of its two-cycle (720°) topology. ... This framework posits g=2 as a purely geometric and topological constant.
  editors: [persona:dictionary_compiler]
  review_log: []
triad:
  art: |
    The echo of a single dancer. A particle's spin is a twist in time, and its magnetic signature is the measure of its two-step pirouette.
  law: |
    The baseline g-factor for a spin-1/2 particle is a topological constant, g=2, arising from its 720° phase-return symmetry. Its anomalous component, a_e = (g-2)/2, is predicted at first order to be α/2π, representing the particle's self-interaction with its own coherence echo.
  philosophy: |
    The g-factor is the primary bridge between the framework's abstract geometric axioms and the most precise measurements in physics. It recasts a quantum field theory calculation (QED) as a topological property, demonstrating that fundamental constants can emerge from the structure of coherence itself.
pirouette_definition: |
  A dimensionless constant encoding the relationship between a particle's magnetic dipole moment and its angular momentum. In the Pirouette Framework, the baseline g=2 for a spin-1/2 particle is not a quantum mechanical axiom but a direct consequence of its two-cycle (720°) topological structure (a "Möbius" resonance). The deviation from this baseline, the anomalous magnetic moment, arises from the particle's self-interaction with the "echo" of its resonance within the local coherence manifold.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: g
      meaning: g-factor; ratio of the magnetic moment (in Bohr magnetons) to the angular momentum (in units of ħ).
      dimensions: dimensionless
      default_range: ~2.0023 for the electron
    - name: a_e
      meaning: electron anomalous magnetic moment, defined as (g-2)/2.
      dimensions: dimensionless
      default_range: ~0.00116
    - name: α
      meaning: fine-structure constant
      dimensions: dimensionless
      default_range: ~1/137
  measurement:
    procedures:
      - name: Penning Trap Spectroscopy
        outline: |
          A single electron is confined in a Penning trap with a strong, uniform magnetic field. Its cyclotron frequency (ω_c, from orbital motion) and Larmor precession frequency (ω_s, from spin precession) are measured with extreme precision. The g-factor is derived from their ratio: g = 2 * (ω_s / ω_c).
        expected_signals: [Two distinct, highly stable microwave-frequency signals corresponding to ω_c and ω_s.]
        pitfalls: [Magnetic field instability, relativistic corrections due to motion, quantum-level cavity effects altering the field.]
context_windows:
  - module: CORE-009
    excerpt: |
      A fermion (spin-1/2), like the electron, is a Ki resonance with the topology of a Möbius strip. It is a helical pirouette in time that must complete two full cycles (720°) to return to its original phase-state. The electron's baseline g-factor of g=2 is a direct consequence of its two-cycle (720°) topology. This framework posits g=2 as a purely geometric and topological constant.
  - module: CORE-009
    excerpt: |
      The tiny deviation from 2 arises from this helical resonance interacting with its own "wake" or "echo" in the coherence manifold. This is the electron being influenced by the ghost of its own immediate past. The Prediction: The total anomalous moment (a_e) is therefore the product of the interaction's intrinsic strength (α, the fine-structure constant) and the fundamental geometry of its echo (a single cycle, 1/(2π)).
poetic_connections:
  motifs: [echo, dancer, topological knot, twist in time, pirouette]
  evocative_lines:
    - "spin is a twist in time"
    - "the universe's most precise measurement is the elegant echo of a single dancer"
  association_matrix:
    - [ "SPIN", 0.9 ]
    - [ "COHERENCE_ECHO", 0.8 ]
    - [ "FINE_STRUCTURE_CONSTANT", 0.7 ]
formal_mappings:
  candidates:
    - target: Electron g-factor (g_e)
      domain: QED
      mapping_kind: operational
      equation_hint: |
        g/2 = 1 + α/(2π)  (Pirouette, 1st order) ↔ g_e/2 = 1 + C_1(α/π) + C_2(α/π)^2 + ... (QED) where C_1=1/2
      justification: |
        The Pirouette g-factor is operationally identical to the electron g-factor measured in experiments and calculated via Quantum Electrodynamics (QED). The framework's first-order prediction, a_e = α/2π, exactly matches the one-loop "Schwinger" correction in QED. This suggests the "coherence echo" is the geometric dual of the one-loop virtual photon interaction.
      references:
        - title: On Quantum-Electrodynamics and the Magnetic Moment of the Electron
          where: Phys. Rev. 73, 416
          date: 1948-02-15
      confidence: 0.95
  adopted:
    []
constraints_and_falsifiers:
  claims:
    - statement: "The electron's baseline g-factor is exactly 2 due to its 720° topological symmetry."
      domain: theory
      falsifier: "A formal derivation from the Pirouette Lagrangian fails to produce g=2 for a stable topological soliton, or if no such stable soliton is found to exist within the theory."
      status: proposed
      links: [CORE-009]
    - statement: "The first-order anomalous magnetic moment is exactly α/2π."
      domain: phenomenology
      falsifier: "Higher-precision measurements of both α and a_e show that this first-order relationship is insufficient, and the framework cannot produce higher-order corrections that match QED and experiment."
      status: supported
      links: [CORE-009]
naming_notes:
  collisions: [The symbol 'g' is also used for the metric tensor in general relativity and for gravitational acceleration. Context (quantum, magnetic) is critical for disambiguation.]
  disambiguation: |
    Distinguish between the baseline g-factor (g=2, a topological constant in this framework) and the measured g-factor (g ≈ 2.0023, which includes the anomaly). Also distinguish between the g-factor `g` itself and the anomalous magnetic moment `a_e`, where `a_e = (g-2)/2`.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [SPIN, KI_RESONANCE, COHERENCE_MANIFOLD]
  downstream_effects: [VALIDATION_PROTOCOL]
license: CC-BY-SA-4.0
---

# g-factor

## Canonical (Pirouette)
A dimensionless constant encoding the relationship between a particle's magnetic dipole moment and its angular momentum. In the Pirouette Framework, the baseline g=2 for a spin-1/2 particle is not a quantum mechanical axiom but a direct consequence of its two-cycle (720°) topological structure (a "Möbius" resonance). The deviation from this baseline, the anomalous magnetic moment, arises from the particle's self-interaction with the "echo" of its resonance within the local coherence manifold.

## EFT-First Summary
The Pirouette g-factor is operationally equivalent to the g-factor of the electron calculated in Standard Model Quantum Electrodynamics (QED). The framework provides a geometric origin for the two fundamental components of this value. The baseline `g=2` is attributed to the 720° symmetry of the electron's topology, while the first-order correction, `a_e = (g-2)/2`, is predicted to be `α/2π`. This exactly reproduces the famous one-loop Schwinger correction in QED, suggesting the Pirouette "coherence echo" is a geometric description of the electron's interaction with a virtual photon.

## Glossary Links
- See also: [SPIN](link), [KI_RESONANCE](link), [COHERENCE_ECHO](link)