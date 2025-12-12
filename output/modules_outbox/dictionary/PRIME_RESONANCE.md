---
term: "Prime Resonance"
canonical_id: "PRIME_RESONANCE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-124"]
---

---
term: Prime Resonance
canonical_id: PRIME_RESONANCE
symbol: (none)
aliases: ['Resonant Archetype', 'Fundamental Pattern']
parents: ['CORE-006', 'CORE-012']
children: []
status: ratified
version: 2.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-124
      lines: "§2"
      snippet: |
        A Prime Resonance is an irreducible, stable Ki pattern—a fundamental "verb" of existence. While countless composite patterns exist, they are all synthesized from these core archetypes.
  editors: [Pirouette Agent]
  review_log: []
triad:
  art: |
    These are the fundamental notes a system can play, the universe's most elegant geometric solutions to the problem of maintaining coherence against decay. Reality is not a machine to be analyzed, but a song to be played.
  law: |
    A system falls into the Prime Resonant pattern that offers the path of maximal coherence for the lowest energetic cost. These patterns are not chosen; they are the deepest, most stable valleys on the coherence manifold.
  philosophy: |
    Understanding that all complex behaviors are compositions of a few simple, dynamic archetypes shifts the focus from analyzing static parts to diagnosing and composing dynamic harmonies.
pirouette_definition: |
  An irreducible, stable, recurring Ki pattern of dynamic behavior. Prime Resonances are the fundamental archetypes from which all complex system behavior is composed, representing the most energetically efficient, high-coherence solutions (stable orbits or "valleys") on the manifold defined by the Pirouette Lagrangian. The ratified set includes the Vector, Orbit, Helix, and Braid.
operational_definition:
  units: Dimensionless classification
  symbol_table: []
  measurement:
    procedures:
      - name: Resonant Analysis
        outline: |
          1. **Capture:** Record the system's key dynamics over a significant time window to generate a temporal signal.
          2. **Decompose:** Apply harmonic analysis (e.g., Fourier Transform) to the signal to break it into its constituent frequencies and phases.
          3. **Map:** Identify the dominant, stable frequencies and their relationships, mapping them to the corresponding Prime Resonances (e.g., a single strong frequency suggests an Orbit; two phase-locked frequencies suggest a Braid).
          4. **Assess:** Evaluate the clarity and signal-to-noise ratio of the resulting Resonant Signature to measure the system's Harmony.
        expected_signals: ['Dominant spectral peaks', 'Phase-locked frequency pairs', 'Slowly drifting frequencies (chirps)']
        pitfalls: ['Insufficient observation time leading to aliasing', 'Mistaking transient noise for a stable resonance', 'Over-fitting complex composites instead of identifying the constituent primes']
context_windows:
  - module: DOMA-124
    excerpt: |
      A Prime Resonance is an irreducible, stable Ki pattern—a fundamental "verb" of existence. While countless composite patterns exist, they are all synthesized from these core archetypes. They are the natural "valleys" and stable orbits on the coherence manifold defined by the Pirouette Lagrangian.
  - module: DOMA-124
    excerpt: |
      Complex systems are rarely a single, pure note; they are chords. Their Ki pattern is an Alchemical Union (CORE-012) of multiple Prime Resonances. A system's nature is defined by its Resonant Signature—the set of its constituent prime patterns. The stability of such a composite system depends on the Harmony between its constituent resonances.
poetic_connections:
  motifs: ['music', 'harmony', 'archetype', 'geometry', 'flow', 'song']
  evocative_lines:
    - "We sought a catalog of parts and found a musical scale."
    - "The universe does not build with bricks; it composes with notes."
  association_matrix:
    - [ "KI", 0.9 ]
    - [ "HARMONY", 0.8 ]
    - [ "ALCHEMICAL_UNION", 0.7 ]
    - [ "TEMPORAL_FORGE", 0.6 ]
formal_mappings:
  candidates:
    - target: Attractor
      domain: Math
      mapping_kind: conceptual
      equation_hint: |
        ẋ = f(x)
      justification: |
        Prime Resonances are described as stable, recurring patterns that a system "falls into," which is the definition of an attractor in the phase space of a dynamical system. The discrete "Periodic Table" (Vector, Orbit, Helix) is a classification of fundamental attractor types (e.g., fixed point, limit cycle).
      references:
        - title: Nonlinear Dynamics and Chaos
          where: Strogatz, S. H.
          date: 1994-01-01
      confidence: 0.9
    - target: Normal Modes of Oscillation
      domain: CM
      mapping_kind: operational
      equation_hint: |
        x(t) = Σ A_n cos(ω_n t + φ_n)
      justification: |
        The diagnostic protocol of "Harmonic Decomposition" directly maps to modal analysis, where a complex system's vibration is broken down into its fundamental, independent patterns of motion (normal modes). Prime Resonances are the conceptual equivalent of these modes for any dynamic system.
      references:
        - title: Classical Mechanics
          where: Goldstein, H.
          date: 1980-01-01
      confidence: 0.8
  adopted:
    - target: Attractors / Normal Modes
      rationale: The term blends the conceptual role of an Attractor (a stable destination for system dynamics) with the operational measurement technique of Modal Analysis (decomposing behavior into fundamental frequencies).
      confidence: 0.85
constraints_and_falsifiers:
  claims:
    - statement: "All complex, stable system behaviors can be decomposed into a finite, small set of Prime Resonances (Vector, Orbit, Helix, Braid) or their harmonious composites."
      domain: phenomenology
      falsifier: "The discovery of a stable, irreducible Ki pattern that cannot be classified as one of the established primes or a composite thereof. For example, a fundamentally chaotic but globally stable pattern (analogous to a strange attractor) that is not a dissonant composite but a prime form in its own right."
      status: supported
      links: ['DOMA-124']
naming_notes:
  collisions: ["prime number"]
  disambiguation: |
    "Prime" in this context means "fundamental," "irreducible," or "archetypal," not the mathematical concept of a number divisible only by 1 and itself. A Prime Resonance is a dynamic pattern that cannot be factored into simpler, stable dynamic patterns.
crosslinks:
  near_synonyms: ['ARCHETYPE']
  antonyms: ['DISSONANCE', 'TURBULENCE', 'CHAOS']
  prerequisites: ['KI', 'PIRQUETTE_LAGRANGIAN', 'PRINCIPLE_OF_MAXIMAL_COHERENCE']
  downstream_effects: ['RESONANT_SIGNATURE', 'HARMONY', 'FORK']
license: CC-BY-SA-4.0
---

# Prime Resonance

## Canonical (Pirouette)
An irreducible, stable, recurring Ki pattern of dynamic behavior. Prime Resonances are the fundamental archetypes from which all complex system behavior is composed, representing the most energetically efficient, high-coherence solutions (stable orbits or "valleys") on the manifold defined by the Pirouette Lagrangian. The ratified set includes the Vector, Orbit, Helix, and Braid.

## EFT-First Summary
In the language of dynamical systems, a Prime Resonance is an **attractor** in the system's phase space, corresponding to a stable, low-entropy configuration. The Pirouette framework posits a finite, universal set of these attractors (Vector, Orbit, Helix, Braid) as the fundamental building blocks of all emergent behavior. The 'Resonant Analysis' protocol is a form of **modal analysis**, using spectral decomposition (e.g., Fourier Transform) on time-series data to identify the dominant **normal modes** (the Prime Resonances) that constitute the system's overall dynamics.

## Glossary Links
- See also: [Resonant Signature](<#>), [Harmony](<#>), [Ki](<#>)