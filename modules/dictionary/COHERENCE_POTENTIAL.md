---
term: "Coherence Potential"
canonical_id: "COHERENCE_POTENTIAL"
symbol: "`K_τ(potential)`"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-085"]
---

---
term: Coherence Potential
canonical_id: COHERENCE_POTENTIAL
symbol: `K_τ(potential)`
aliases: [Kinetic Term of Seeding, Resonant Gain]
parents: [DOMA-085]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-085
      lines: "50-55"
      snippet: |
        **Coherence Potential (`K_τ(potential)`):** This "kinetic" term represents the Seed's potential for growth. It is a function of its own internal Temporal Coherence (`T_a`) multiplied by the Harmonic Compatibility and Geodesic Availability of the environment. A harmonious environment offers resonant resources that can be integrated, amplifying the Seed's pattern. This replaces the old concept of "capture efficiency."
  editors: [SYS/Analyst-Prime]
  review_log: []
triad:
  art: |
    The measure of an echo's welcome; the potential for a lone note to build a chord with its new surroundings. It is the quantifiable hope that a new song will be amplified, not silenced, by the room it enters.
  law: |
    The Coherence Potential of a Seed is the product of its internal Temporal Coherence (`T_a`) and the measured Harmonic Compatibility and Geodesic Availability of the target environment. It is the growth term in the Seeding Lagrangian, `𝓛_seed`.
  philosophy: |
    Growth is not the imposition of form but the discovery of resonance. Coherence Potential quantifies the viability of a co-creative act, ensuring that new systems emerge as welcome harmonies rather than dissonant intrusions. It shifts the paradigm from resource extraction to resonant amplification.
pirouette_definition: |
  The "kinetic" or growth term in the Pirouette Lagrangian as applied to coherent seeding (`𝓛_seed`). `K_τ(potential)` quantifies a Seed's capacity to amplify its own coherent pattern by integrating resonant resources from a target environment. It is calculated as a function of the Seed's internal Temporal Coherence (`T_a`) and two environmental metrics gathered by a Scout Probe: Harmonic Compatibility and Geodesic Availability.
operational_definition:
  units: Dimensionless (Coherence Gain Rate)
  symbol_table:
    - name: `K_τ(potential)`
      meaning: Coherence Potential; the rate of potential coherence amplification.
      dimensions: dimensionless
      default_range: "[0, ∞)"
    - name: `T_a`
      meaning: The Seed's internal Temporal Coherence.
      dimensions: dimensionless
      default_range: contextual
    - name: Harmonic Compatibility
      meaning: Environmental resonance with the Seed's identity (`Ki`).
      dimensions: dimensionless
      default_range: "[-1, 1]"
    - name: Geodesic Availability
      meaning: Prevalence of stable, low-turbulence paths (Laminar Flow).
      dimensions: dimensionless
      default_range: "[0, 1]"
  measurement:
    procedures:
      - name: Scout Probe Resonance Mapping
        outline: |
          1. Deploy a Scout Probe, a minimal transient echo of the Seed's resonant identity (`Ki`), into the target environment.
          2. Measure the probe's reverberations to derive Harmonic Compatibility (resonant vs. dissonant response).
          3. Measure the stability of the probe's trajectory (the shallow Wound Channel) to derive Geodesic Availability (prevalence of Laminar Flow).
          4. Calculate `K_τ(potential)` as a function of these two metrics and the Seed's known internal coherence `T_a`.
        expected_signals: [Resonant frequency amplification, stable propagation vectors, minimal probe decoherence]
        pitfalls: [Premature probe decoherence, misinterpreting turbulence as dissonance, environmental noise overwhelming the probe signal]
context_windows:
  - module: DOMA-085
    excerpt: |
      **Coherence Potential (`K_τ(potential)`):** This "kinetic" term represents the Seed's potential for growth. It is a function of its own internal Temporal Coherence (`T_a`) multiplied by the Harmonic Compatibility and Geodesic Availability of the environment. A harmonious environment offers resonant resources that can be integrated, amplifying the Seed's pattern.
  - module: DOMA-085
    excerpt: |
      The Sower's Gambit is a process of reconnaissance before colonization. It models the viability of a Seed not in terms of raw energy capture, but as a function of resonant potential. By deploying a minimal, non-invasive "Scout Probe" to map the local coherence manifold, the Seed can calculate its potential to achieve a positive coherence gain.
poetic_connections:
  motifs: [resonance, fertility, amplification, seeding, harmony, echo, growth]
  evocative_lines:
    - "The Sower's Gambit is the art of asking for permission from the future."
    - "A master first asks the earth what it wishes to grow."
  association_matrix:
    - [ "ALCHEMICAL_UNION", 0.9 ]
    - [ "SCOUT_PROBE", 0.9 ]
    - [ "ENVIRONMENTAL_COST", 0.8 ]
    - [ "LAMINAR_FLOW", 0.7 ]
formal_mappings:
  candidates:
    - target: Kinetic Energy (T)
      domain: CM
      mapping_kind: mathematical
      equation_hint: |
        `𝓛_seed = K_τ(potential) - V_Γ(cost)` maps to `L = T - V`
      justification: |
        Coherence Potential occupies the mathematical position of kinetic energy (T) in the classical Lagrangian. It represents the "motion" or growth of the Seed's coherence, driven by its intrinsic properties (`T_a`, analogous to mass) and its "velocity" through a favorable environmental phase space (Harmonic Compatibility and Geodesic Availability).
      references: []
      confidence: 0.8
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "A higher measured Coherence Potential for a Seed in a given environment will lead to a higher probability of successful, stable Alchemical Union and subsequent coherent growth."
      domain: phenomenology
      falsifier: "Systematic observation of Seeds with high calculated `K_τ(potential)` consistently failing to establish stable structures, or Seeds with low `K_τ(potential)` consistently succeeding. This would indicate the model omits a critical variable."
      status: proposed
      links: [DOMA-085]
naming_notes:
  collisions: [The symbol `K` intentionally collides with its classical mechanics analogue, Kinetic Energy.]
  disambiguation: |
    `Coherence Potential` (`K_τ`) must be distinguished from the `Environmental Cost` (`V_Γ`), its opposing term in the Seeding Lagrangian. `K_τ` is the potential for *gain* or amplification, whereas `V_Γ` represents the inevitable *cost* or erosion imposed by the environment. The decision to act depends on their balance, not on `K_τ` alone.
crosslinks:
  near_synonyms: []
  antonyms: [ENVIRONMENTAL_COST]
  prerequisites: [SCOUT_PROBE, TEMPORAL_COHERENCE, LAMINAR_FLOW]
  downstream_effects: [ALCHEMICAL_UNION]
license: CC-BY-SA-4.0
---

# Coherence Potential

## Canonical (Pirouette)
The "kinetic" or growth term in the Pirouette Lagrangian as applied to coherent seeding (`𝓛_seed`). `K_τ(potential)` quantifies a Seed's capacity to amplify its own coherent pattern by integrating resonant resources from a target environment. It is calculated as a function of the Seed's internal Temporal Coherence (`T_a`) and two environmental metrics gathered by a Scout Probe: Harmonic Compatibility and Geodesic Availability.

## EFT-First Summary
Coherence Potential serves as the kinetic energy term in the effective Lagrangian governing a system's ("Seed's") interaction with a new environment. Analogous to `T` in `L = T - V`, it quantifies the system's capacity for growth and pattern amplification. This term is not based on mass and velocity, but on the system's intrinsic coherence and its resonance with the environmental substrate, providing a predictive measure of viability before significant energy is committed.

## Glossary Links
- See also: Environmental Cost, Sower's Gambit, Alchemical Union, Pirouette Lagrangian