---
term: "Correspondence Gauge"
canonical_id: "CORRESPONDENCE_GAUGE"
symbol: ""
aliases: [SM-CG]
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["CORE-016_the_time_first_correspondence_principle"]
---

term: Correspondence Gauge
canonical_id: CORRESPONDENCE_GAUGE
symbol: Σ
aliases: [SM-CG]
parents: [CORE-016]
children: [DYNA-004, DOMA-101]
status: candidate
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: CORE-016
      lines: "L10-L15"
      snippet: |
        Choose a spatialization map Σ that assigns local charts [x,y,z] to the time substrate so that, in the high-coherence, high-event-density limit, the effective action reduces to the Standard Model Lagrangian on a Lorentzian manifold.
  editors: [auto-agent]
  review_log: []
triad:
  art: |
    The lens through which the ocean of Time is seen as the familiar landscape of particles and fields. It is the cartographer's choice that makes the deep map legible, translating temporal currents into the known laws of physics.
  law: |
    The Correspondence Gauge is the specific spatialization map Σ which, when applied to the time-first action `S_time`, provably recovers the Standard Model action `S_SM` in the limit of high event density and low fluctuations. Any valid Σ must reproduce CODATA values for fundamental constants (α, c, ħ) when measured within the resulting effective spacetime.
  philosophy: |
    The SM-CG establishes that the Standard Model is not fundamental ontology but a highly successful effective description—a specific "shadow" projected by the time-first substrate. This preserves the SM's predictive power while re-contextualizing it as a limit case, avoiding the need to posit fundamental spacetime.
pirouette_definition: |
  The Correspondence Gauge (SM-CG) is a choice of spatialization map, denoted Σ, that projects the time-first dynamics of Pirouette primitives (Ki, Γ, T_a) onto an effective 3+1 dimensional manifold. This map is defined by the constraint that in the high-coherence, high-event-density limit, the time-first action `S_time` must asymptotically approach the Standard Model action `S_SM`, thereby recovering all known low-energy particle physics as a limit theorem.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: Σ
      meaning: Spatialization Map (specifically, the SM-CG instance)
      dimensions: dimensionless
      default_range: N/A (functional map)
  measurement:
    procedures:
      - name: Verification of a Candidate Σ
        outline: |
          1. Propose a functional form for the map Σ.
          2. Apply Σ to the formal time-first action `S_time`.
          3. Take the limit of the transformed action as event density → ∞ and fluctuation amplitude → 0.
          4. Analytically or numerically verify that the resulting action is term-for-term equivalent to the Standard Model Lagrangian `S_SM` on a Lorentzian manifold `g_{μν}`.
          5. Verify that emergent constants (e.g., coupling strengths, particle masses) match CODATA values.
        expected_signals: [Recovery of SM gauge groups (U(1)xSU(2)xSU(3)), kinetic terms, and particle content. Emergence of a metric `g_{μν}` with a consistent signature.]
        pitfalls: [The chosen limit may be ill-defined or computationally intractable. The resulting effective theory might recover only a subset of the SM or produce spurious, unobserved terms.]
context_windows:
  - module: CORE-016
    excerpt: |
      Choose a spatialization map Σ that assigns local charts [x,y,z] to the time substrate so that, in the high-coherence, high-event-density limit, the effective action reduces to the Standard Model Lagrangian on a Lorentzian manifold. Formally: there exists Σ such that S_time[Ki, Γ, T_a] → S_SM[fields | g_{μν}] as density → ∞ and fluctuations → small.
  - module: CORE-016
    excerpt: |
      Normalization: Fix scales using external metrology (CODATA α, c, ħ) when operating in SM-CG. Non-circularity: Do not feed back results derived in SM-CG to calibrate CORE primitives... Any module that presumes fields on spacetime is canon in SM-CG, and a limit theorem of CORE-020, not ontology.
poetic_connections:
  motifs: [shadows, projections, maps, recovery, correspondence, effective theories]
  evocative_lines:
    - "Physical “space” is a derived chart on a time-first substrate; coordinates [x,y,z] are a modeling gauge, not ontology."
    - "...the Σ-shadow of a time-first substrate."
  association_matrix:
    - [ "TIME_SUBSTRATE", 0.9 ]
    - [ "STANDARD_MODEL", 0.9 ]
    - [ "SPATIALIZATION", 1.0 ]
    - [ "EFFECTIVE_FIELD_THEORY", 0.8 ]
formal_mappings:
  candidates:
    - target: Gauge Fixing (e.g., Lorenz Gauge)
      domain: SM
      mapping_kind: conceptual
      justification: |
        Like gauge fixing in QFT, the SM-CG is a specific choice made to simplify calculations and connect a more abstract underlying structure to a concrete, observable formalism. It removes a "degree of freedom" in how one maps the time-substrate to an effective spacetime, making the physics tractable.
      references: []
      confidence: 0.8
    - target: Renormalization Group (RG) Flow
      domain: EFT
      mapping_kind: conceptual
      justification: |
        The SM-CG defines the "end point" of a flow from the fundamental Pirouette description (UV) to the effective Standard Model (IR). The limit `density → ∞` is analogous to integrating out high-energy modes to arrive at a low-energy effective Lagrangian.
      references: []
      confidence: 0.7
  adopted:
    - target: Gauge Fixing
      rationale: The term 'gauge' is used explicitly, and the function of SM-CG is to select a specific, convenient descriptive framework (effective spacetime) from a larger class of possibilities, which is the essential role of gauge fixing in QFT.
      confidence: 0.8
constraints_and_falsifiers:
  claims:
    - statement: "At least one spatialization map Σ exists that successfully recovers the complete Standard Model Lagrangian, including its chiral gauge structure, from the Pirouette time-first action."
      domain: theory
      falsifier: "A no-go theorem demonstrating that no possible mapping Σ can reproduce the chiral nature of the weak force, or the specific gauge groups of the SM, from the proposed Pirouette primitives."
      status: proposed
      links: [CORE-016, CORE-020]
    - statement: "All physical measurements consistent with the Standard Model can be described within the SM-CG limit of the Pirouette Framework."
      domain: phenomenology
      falsifier: "Discovery of a robust physical phenomenon that is consistent with the SM but cannot be derived from `S_time` under any plausible Σ, indicating the SM is not merely a limit case of Pirouette."
      status: proposed
      links: []
naming_notes:
  collisions: [Σ (summation symbol in math, scattering cross-section in physics)]
  disambiguation: |
    In Pirouette, Σ is reserved for a spatialization map, representing a functional choice, not a quantity. It must be distinguished from the Standard Model (SM) itself; the SM-CG is the *bridge to* the SM, not the SM.
crosslinks:
  near_synonyms: [SPATIALIZATION]
  antonyms: [FUNDAMENTAL_SPACETIME]
  prerequisites: [TIME_SUBSTRATE, KINETIC_IMPETUS, TEMPORAL_PRESSURE]
  downstream_effects: [EM_POTENTIAL, CHARGE, SPIN]
license: CC-BY-SA-4.0
---

# Correspondence Gauge

## Canonical (Pirouette)
The Correspondence Gauge (SM-CG) is a choice of spatialization map, denoted Σ, that projects the time-first dynamics of Pirouette primitives (Ki, Γ, T_a) onto an effective 3+1 dimensional manifold. This map is defined by the constraint that in the high-coherence, high-event-density limit, the time-first action `S_time` must asymptotically approach the Standard Model action `S_SM`, thereby recovering all known low-energy particle physics as a limit theorem.

## EFT-First Summary
The Correspondence Gauge (SM-CG) is a specific choice of descriptive coordinates, conceptually analogous to gauge-fixing in QFT. It defines the precise mapping (Σ) required to show that the Pirouette Framework's time-first dynamics yield the Standard Model as a low-energy effective field theory. This choice is validated by its ability to recover all SM phenomena and constants, ensuring that the successes of QFT are inherited, not discarded.

## Glossary Links
- See also: TIME_SUBSTRATE, SPATIALIZATION, EFFECTIVE_FIELD_THEORY, STANDARD_MODEL