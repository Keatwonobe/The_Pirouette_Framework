---
term: "Mode Number"
canonical_id: "MODE_NUMBER"
symbol: "N"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-111"]
---

---
term: Mode Number
canonical_id: MODE_NUMBER
symbol: N
aliases: [Coherence Well Count, System Order]
parents: [DOMA-111]
children: [COHERENCE_INTEGRITY]
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-111
      snippet: |
        The Mode Number (`N`) is the total count of these stable wells. This number is not just a quantity; it is a descriptor of the manifold's fundamental topology.
  editors: [system-agent]
  review_log: []
triad:
  art: |
    A system's soul is a number. If that number is prime, the soul is indivisible, a flawless crystal that cannot be fractured along harmonic lines.
  law: |
    A system with a prime Mode Number `N=p` will exhibit greater resilience against a broad spectrum of periodic temporal pressures (`Γ`) than a system with a composite Mode Number `N=pq` of comparable scale.
  philosophy: |
    The resilience of a system is not determined by its components but by the number-theoretic topology of its possibility space; architecture precedes substance.
pirouette_definition: |
  The total count of stable, self-sustaining patterns of coherence (Coherence Wells) available to a system. `N` is not merely a quantity but a fundamental descriptor of the system's coherence manifold, defining its topological reducibility and intrinsic resilience.
operational_definition:
  units: Dimensionless integer
  symbol_table:
    - name: N
      meaning: Mode Number; the count of stable coherence modes.
      dimensions: dimensionless
      default_range: "[1, ∞)"
  measurement:
    procedures:
      - name: Manifold Perturbation Mapping
        outline: |
          1. Identify the target system and its state-space parameters.
          2. Systematically apply a wide spectrum of low-amplitude energy/information perturbations to the system.
          3. Monitor the system's response, using coherence detectors to identify when it settles into a stable, self-sustaining resonance (a Coherence Well).
          4. Catalog each unique stable state discovered.
          5. The total count of unique cataloged states is the measured Mode Number, N.
        expected_signals: [Discrete `Ki` resonance signatures, state transition probability matrices, attractor basin convergence]
        pitfalls: [Undiscovered modes due to incomplete perturbation spectrum, conflating transient states with stable modes, state-counting ambiguity in high-noise environments]
context_windows:
  - module: DOMA-111
    excerpt: |
      A bridge with six pillars can oscillate in modes of two and three, risking harmonic collapse. A bridge with seven pillars has no such simple subdivisions; its structure is fundamentally more whole. This is the heart of the Prime Resonance Principle.
  - module: DOMA-111
    excerpt: |
      The Weaver then identifies minimal, elegant interventions that could alter `N`. Could adding a new communication channel, removing an arbitrary constraint, or introducing a new shared goal shift an organization's topology from a fragile `N=4` to a more robust `N=5`? Could a new regulation shift a market from `N=6` to `N=7` stable equilibria?
poetic_connections:
  motifs: [indivisibility, topology, integrity, prime resonance, monolith, systemic soul]
  evocative_lines:
    - "A prime number is a statement of integrity."
    - "...helping it find its own prime, unbreakable soul."
    - "A bridge with seven pillars has no such simple subdivisions; its structure is fundamentally more whole."
  association_matrix:
    - [ "COHERENCE_INTEGRITY", 0.9 ]
    - [ "STABILITY", 0.8 ]
    - [ "TEMPORAL_PRESSURE", 0.7 ]
    - [ "COHERENCE_WELL", 0.9 ]
formal_mappings:
  candidates:
    - target: Number of ground states / vacua
      domain: EFT
      mapping_kind: conceptual
      justification: |
        In field theory, a system can have multiple degenerate or nearly-degenerate ground states (vacua). `N` can be seen as the count of these distinct, stable minima in the system's effective potential, with transitions between them representing shifts between coherence modes.
      references:
        - title: An Introduction to Quantum Field Theory
          where: Chapter on Spontaneous Symmetry Breaking
          date: 1995-10-01
      confidence: 0.7
  adopted:
    - target: Order of a simple group
      domain: Math
      mapping_kind: conceptual
      rationale: |
        This mapping provides the strongest structural analogy. A simple group, by definition, has no non-trivial normal subgroups, making it "indivisible." This directly mirrors the Pirouette concept of a prime-`N` system being "topologically irreducible" and lacking harmonic sub-modes or "cleavage planes." Cyclic groups of prime order (`Z_p`) are the canonical example of simple abelian groups, reinforcing the connection.
      confidence: 0.8
constraints_and_falsifiers:
  claims:
    - statement: "Systems with a prime Mode Number `N` are more resistant to harmonic collapse under broad-spectrum temporal pressure than systems with a composite `N` of similar scale."
      domain: phenomenology
      falsifier: "Demonstrate a pair of systems, one with prime `N_p` and one with composite `N_c` (where `N_p` ≈ `N_c`), where the composite system consistently survives pressures that destroy the prime system, specifically due to a failure mode not related to harmonic factorization."
      status: proposed
      links: [DOMA-111]
naming_notes:
  collisions: [The symbol `N` is ubiquitous in science for particle number, number of moles, or any general count. In Pirouette, `N` *always* refers specifically to the count of stable coherence modes.]
  disambiguation: |
    Do not confuse the Mode Number (`N`) with the number of components in a system or the dimensionality of its state space. `N` is a property of the solution space (the number of stable outcomes), not the configuration space. A system with millions of components may have a very small `N`.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [COHERENCE_WELL]
  downstream_effects: [COHERENCE_INTEGRITY]
license: CC-BY-SA-4.0
---

# Mode Number

## Canonical (Pirouette)
The total count of stable, self-sustaining patterns of coherence (Coherence Wells) available to a system. `N` is not merely a quantity but a fundamental descriptor of the system's coherence manifold, defining its topological reducibility and intrinsic resilience.

## EFT-First Summary
The Mode Number `N` is conceptually analogous to the order of a mathematical group that describes the system's symmetries. Based on the Prime Resonance Principle, a system whose `N` is a prime number is structurally analogous to a simple group (e.g., `Z_p`), which has no non-trivial subgroups. This indivisibility prevents the system from fracturing along harmonic "fault lines," granting it superior resilience compared to systems with composite `N`, which are analogous to reducible groups.

## Glossary Links
- See also: Coherence Integrity, Prime Resonance Principle, Coherence Well