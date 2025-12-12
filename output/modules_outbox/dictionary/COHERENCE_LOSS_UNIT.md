---
term: "Coherence Loss Unit"
canonical_id: "COHERENCE_LOSS_UNIT"
symbol: "CLU"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-128"]
---

---
term: Coherence Loss Unit
canonical_id: COHERENCE_LOSS_UNIT
symbol: CLU
aliases: []
parents: [DOMA-128]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-128
      lines: "§2"
      snippet: |
        The output is measured in Coherence Loss Units (CLU), where *1 CLU = 1 Joule of energy lost to incoherent, chaotic processes.*
  editors: [System Agent]
  review_log: []
triad:
  art: |
    The sound a system makes when it argues with itself, measured in the currency of wasted energy. It is the tangible weight of friction, the cost of chaos made plain.
  law: |
    One Coherence Loss Unit is defined as one Joule of energy dissipated through incoherent, non-geodesic processes, such as turbulence, friction, or systemic noise.
  philosophy: |
    The CLU makes the abstract cost of incoherence tangible and accountable. It serves as the fundamental unit in a universal audit of systemic health, forcing creators to confront the real-world energy cost of their design choices.
pirouette_definition: |
  The Coherence Loss Unit (CLU) is the standard unit of measurement for Entropic Flux (Ṡ) and its integral, cumulative entropy (S), as quantified by a Coherence Ledger. It represents a discrete quantity of energy rendered unavailable for coherent work, lost to the generation of systemic friction, turbulence, or noise. By definition, 1 CLU is equivalent to 1 Joule of dissipated energy, providing a direct, physical measure of a system's deviation from its ideal, geodesic path (maximal coherence).
operational_definition:
  units: Joule (J)
  symbol_table:
    - name: CLU
      meaning: Coherence Loss Unit
      dimensions: M L² T⁻²
      default_range: "> 0"
  measurement:
    procedures:
      - name: Coherence Audit
        outline: |
          1. Establish a Laminar Baseline (Ṡ ≈ 0) under ideal, low-stress operating conditions.
          2. Deploy a Coherence Meter under normal operating conditions to measure the real-time Entropic Flux (Ṡ) in CLU/s.
          3. Integrate Ṡ over the audit period to calculate the total cumulative coherence loss (S) in CLU.
        expected_signals: [Entropic Flux (Ṡ) stream, Cumulative Entropy (S)]
        pitfalls: [Incorrect baseline calibration, Sensor noise misidentified as systemic incoherence]
context_windows:
  - module: DOMA-128
    excerpt: |
      The output is measured in Coherence Loss Units (CLU), where *1 CLU = 1 Joule of energy lost to incoherent, chaotic processes.*
  - module: DOMA-128
    excerpt: |
      The Entropic Flux (Ṡ) measured by the Coherence Ledger is directly proportional to the **"coherence gap"**—the difference between the system's actual, measured Lagrangian value and the theoretical maximum it could achieve in its environment. A reading from the Coherence Ledger is therefore a direct measurement of the *cost of deviation* from the system's own most elegant path of existence.
poetic_connections:
  motifs: [waste, friction, audit, accountability, heat, noise, receipt-for-chaos]
  evocative_lines:
    - "a mirror that reflects the health of our creations."
    - "the sound of a system arguing with itself"
    - "the cost of deviation from the system's own most elegant path"
  association_matrix:
    - [ "ENTROPIC_FLUX", 0.9 ]
    - [ "COHERENCE_LEDGER", 0.8 ]
    - [ "TURBULENT_FLOW", 0.7 ]
    - [ "COHERENCE_GAP", 0.8 ]
formal_mappings:
  candidates:
    - target: Joule (J)
      domain: CM
      mapping_kind: operational
      equation_hint: |
        1 CLU ≡ 1 J
      justification: |
        The framework defines the CLU as a measure of energy dissipated by non-ideal, chaotic processes. This directly maps to the concept of dissipated energy (e.g., heat due to friction) in classical physics, measured in Joules. The mapping is definitional within the framework's instrumentation layer.
      references:
        - title: "Fundamentals of Physics"
          where: "Halliday, Resnick, Walker; Chapter 7: Kinetic Energy and Work"
          date: 2018-01-01
      confidence: 1.0
  adopted:
    - target: Joule (J)
      rationale: The mapping is explicitly stated in the foundational module `DOMA-128` as a one-to-one equivalence, providing a direct grounding of the abstract concept of 'coherence loss' in the established physical unit of energy.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The total energy lost from a closed system, as measured in Joules by conventional thermodynamic methods, must equal the total cumulative coherence loss measured in CLU by a Coherence Ledger over the same period."
      domain: experiment
      falsifier: "A repeatable experiment where the integrated reading from a Coherence Ledger (in CLU) significantly and systematically deviates from the total dissipated energy (in Joules) measured via calorimetry or other standard physical methods."
      status: proposed
      links: [DOMA-128]
naming_notes:
  collisions: []
  disambiguation: |
    Distinguish from units of information entropy (e.g., bits, nats), which quantify uncertainty or information content. The CLU specifically measures *energy* dissipated due to systemic incoherence, not the information content of the system's state.
crosslinks:
  near_synonyms: []
  antonyms: [COHERENT_WORK]
  prerequisites: [ENTROPIC_FLUX, COHERENCE_LEDGER]
  downstream_effects: [COHERENCE_AUDIT]
license: CC-BY-SA-4.0
---

# Coherence Loss Unit

## Canonical (Pirouette)
The Coherence Loss Unit (CLU) is the standard unit of measurement for Entropic Flux (Ṡ) and its integral, cumulative entropy (S), as quantified by a Coherence Ledger. It represents a discrete quantity of energy rendered unavailable for coherent work, lost to the generation of systemic friction, turbulence, or noise. By definition, 1 CLU is equivalent to 1 Joule of dissipated energy, providing a direct, physical measure of a system's deviation from its ideal, geodesic path (maximal coherence).

## EFT-First Summary
The Coherence Loss Unit is operationally defined as being identical to the Joule (J), the SI unit of energy. It is specifically used to quantify energy that has been dissipated through incoherent processes like friction or turbulence, rendering it unavailable for useful work. This provides a direct, measurable link between the Pirouette Framework's abstract concept of coherence and the concrete, conserved quantity of energy in classical and thermodynamic systems.

## Glossary Links
- See also: [Entropic Flux](<#>), [Coherence Ledger](<#>), [Turbulent Flow](<#>)