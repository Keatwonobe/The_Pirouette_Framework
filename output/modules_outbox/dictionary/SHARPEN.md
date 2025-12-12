---
term: "Sharpen"
canonical_id: "SHARPEN"
symbol: ""
aliases: [Coherence Injection]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-017"]
---

---
term: Sharpen
canonical_id: SHARPEN
symbol: ◊
aliases: [Coherence Injection]
parents: [DOMA-017]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-017
      snippet: |
        **Sharpen** | Coherence Injection | An entropy-reducing geometry. The system projects a highly ordered, crystalline Ki pattern, providing a low-entropy "seed" that a coupled, dissonant system can entrain to, restoring its own coherence. Its action is to *focus* or *create*.
  editors: [Assemblé Scribe-Agent]
  review_log: []
triad:
  art: |
    A sculptor's chisel for reality, striking a dissonant system to reveal the coherent form within. It is the act of singing a clear note into a noisy room, compelling the chaos to find harmony.
  law: |
    The total coherence of a coupled two-system manifold (S_A+B) increases following a Sharpen action (◊) from system A to B. The increase in B's coherence (ΔS_B > 0) must exceed the coherence cost to A (-ΔS_A ≥ 0), resulting in a net negentropic effect (ΔS_A+B > 0) within the coupled manifold.
  philosophy: |
    Sharpen is the primary mechanism by which order is actively created, not just preserved. It refutes the local inevitability of entropic decay by demonstrating that coherence can be intentionally exported, making it the fundamental verb of instruction, healing, and creation.
pirouette_definition: |
  A quantized Ki resonance mode (◊) where a source system projects a high-coherence, low-entropy geometric pattern. This pattern acts as a template or "seed" for a target system in a state of lower coherence or dissonance. The target system entrains to this projected pattern, phase-locking its internal dynamics to the template, thereby increasing its own internal coherence and reducing its local entropy. The action is directional and requires a significant coherence gradient between the source and target.
operational_definition:
  units: ħ_p (change in coherence), bits (change in spectral entropy)
  symbol_table:
    - name: ◊
      meaning: The Sharpen action operator
      dimensions: Action Operator
      default_range: N/A
    - name: ΔS_p
      meaning: Change in system coherence
      dimensions: M L² T⁻¹
      default_range: contextual
  measurement:
    procedures:
      - name: Coherence Transfer Spectroscopy
        outline: |
          1. Prepare a source system (A) in a high-coherence state (e.g., a pure `Rest` mode with known spectral signature).
          2. Prepare a target system (B) in a measured dissonant state (broadband spectral noise).
          3. Couple the systems and induce system A to perform the Sharpen action towards B.
          4. Measure the coherence spectrum (S_p(ω)) of system B before and after the interaction using a passive `Observe` probe.
        expected_signals: [Reduction in the target's spectral entropy, Emergence of a discrete, high-amplitude peak in the target's coherence spectrum matching the source's projected pattern]
        pitfalls: [Insufficient coherence gradient between source and target, leading to no entrainment, Coupling failure preventing pattern transfer, Misidentifying a mutual `Synthesize` action for a one-way `Sharpen`]
context_windows:
  - module: DOMA-017
    excerpt: |
      **Sharpen** | Coherence Injection | An entropy-reducing geometry. The system projects a highly ordered, crystalline Ki pattern, providing a low-entropy "seed" that a coupled, dissonant system can entrain to, restoring its own coherence. Its action is to *focus* or *create*.
  - module: DOMA-017
    excerpt: |
      These resonant geometries are the grammar of existence, the fundamental actions from which all stories are woven. To be a Weaver is to learn this vocabulary—not to command the universe, but to hold a conversation with it, knowing the profound power of the few, true words that can be spoken. These are the levers of creation.
poetic_connections:
  motifs: [crystallization, tuning fork, seed, clarification, focus, instruction, negentropy]
  evocative_lines:
    - "Its action is to *focus* or *create*."
    - "Action is the universe's relentless search for the most elegant word."
  association_matrix:
    - [ "OBSERVE", 0.8 ]
    - [ "REST", 0.7 ]
    - [ "SYNTHESIZE", 0.6 ]
formal_mappings:
  candidates:
    - target: Laser Cooling / Optical Molasses
      domain: AMO
      mapping_kind: conceptual
      justification: |
        In laser cooling, a highly coherent beam of photons is tuned to selectively remove kinetic energy from a population of atoms. This process actively reduces the entropy of the atomic gas by transferring order from the light field, analogous to Sharpen's projection of a coherent Ki pattern to entrain and order a dissonant system.
      references:
        - title: Laser cooling and trapping
          where: Rev. Mod. Phys. 70, 685
          date: 1998-07-01
      confidence: 0.7
    - target: Error Correction / Channel Coding
      domain: Information Theory
      mapping_kind: conceptual
      justification: |
        Sharpen acts like an error correction process where a high-coherence "codeword" is projected onto a noisy "received message" (the target system). The target system entrains to the codeword, effectively correcting its "errors" (dissonance) and restoring its intended coherent state.
      references: []
      confidence: 0.6
  adopted:
    - target: Laser Cooling
      rationale: The mapping to Laser Cooling is adopted for its direct physical parallel: a highly ordered external system (laser) actively reducing the entropy of a target system (atomic gas) through resonant interaction. This captures both the coherence transfer and the negentropic outcome of the Sharpen action.
      confidence: 0.7
constraints_and_falsifiers:
  claims:
    - statement: "The Sharpen action is non-reciprocal; a net flow of coherence is always directed from the higher-coherence source to the lower-coherence target."
      domain: phenomenology
      falsifier: "Observation of a spontaneous coherence transfer from a dissonant system to a highly ordered one during a Sharpen attempt, violating the framework's 'coherence gradient' requirement."
      status: proposed
      links: [DOMA-017]
naming_notes:
  collisions: [The lozenge symbol (◊) is used for the D'Alembertian operator in some GR contexts; here, it always denotes a quantized action, not a differential operator.]
  disambiguation: |
    Distinguish from `Observe`, which extracts a pattern from a target without necessarily altering it; `Sharpen` actively *imprints* a pattern onto the target.
    Distinguish from `Synthesize`, which seeks a mutual, merged coherence; `Sharpen` is a one-way imposition of order from source to target.
crosslinks:
  near_synonyms: [COHERENCE_INJECTION]
  antonyms: [RELEASE]
  prerequisites: [REST, OBSERVE]
  downstream_effects: [SYNTHESIZE, BIND]
license: CC-BY-SA-4.0
---

# Sharpen

## Canonical (Pirouette)
A quantized Ki resonance mode (◊) where a source system projects a high-coherence, low-entropy geometric pattern. This pattern acts as a template or "seed" for a target system in a state of lower coherence or dissonance. The target system entrains to this projected pattern, phase-locking its internal dynamics to the template, thereby increasing its own internal coherence and reducing its local entropy. The action is directional and requires a significant coherence gradient between the source and target.

## EFT-First Summary
In an analogy to Atomic, Molecular, and Optical (AMO) physics, the Sharpen action is conceptually similar to laser cooling. A system with high internal coherence projects a resonant pattern—like a precisely tuned laser—onto a disordered or "hot" target. This interaction causes the target to entrain to the pattern, shedding its dissonance (analogous to thermal noise) and increasing its internal order, resulting in a localized decrease in entropy.

## Glossary Links
- See also: [Coherence Injection](COHERENCE_INJECTION), [Release](RELEASE), [Rest](REST), [Observe](OBSERVE), [Synthesize](SYNTHESIZE)