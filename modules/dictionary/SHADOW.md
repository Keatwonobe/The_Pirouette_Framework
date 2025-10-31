---
term: "Shadow"
canonical_id: "SHADOW"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-PHYS-003_the_obs_sail"]
---

---
term: Shadow
canonical_id: SHADOW
symbol: 
aliases: [region of suppressed coherence, observational shadow]
parents: [DOMA-PHYS-003_the_obs_sail, DOMA-SHADOW-001]
children: [DOMA-PHYS-OBS-SAIL-APPX, DOMA-QCOMP-001]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-PHYS-003_the_obs_sail
      lines: "§8"
      snippet: |
        The weak meters raise V_obs on selected arms, lowering usable coherence there (ΔKτ < 0 locally).
        The triad geometry (Triadic Lock) converts that asymmetric Shadow into an asymmetric phase map.
        The far-field intensity—and thus momentum flow—follows the agreement geometry.
  editors: [system_agent]
  review_log: []
triad:
  art: |
    An observer's attention is not passive; by choosing which possibilities to listen for, it quiets them, sculpting the remaining silence into a form that can push and pull. The choice is a map, and maps move things.
  law: |
    A spatial gradient in measurement strength (the boundary of a Shadow) induces a corresponding drift or effective force on a coherent system. The magnitude of the force is proportional to the information acquisition rate, and its direction is determined by the geometry of the observation.
  philosophy: |
    Observation is an active, world-shaping force, not a passive reception of information. By strategically suppressing coherence in some regions, we can create structured potentials from pure information flow, enabling control and propulsion without classical force fields.
pirouette_definition: |
  A Shadow is a region in a system's configuration space where quantum coherence is actively suppressed by interaction with a measurement device (an observer). This suppression, quantified by an increase in the local Observation Potential (V_obs), damps or "erases" the quantum interference pathways passing through that region. Spatially asymmetric Shadows, or gradients in Shadow depth, create effective potentials that steer the system's dynamics, converting measurement back-action into a directed force.
operational_definition:
  units: Shadow depth can be measured in units of information rate (bits/sec) or equivalently, as a potential (Joules), or a decoherence rate (1/sec).
  symbol_table:
    - name: V_obs
      meaning: Observation Potential; the effective potential corresponding to the strength of local measurement.
      dimensions: M L^2 T^-2 (Energy)
      default_range: contextual
    - name: k(x)
      meaning: Local measurement strength function.
      dimensions: T^-1 (Rate)
      default_range: contextual
    - name: ΔKτ
      meaning: Coherence-Time budget; reduced by interaction with an observer.
      dimensions: M L^2 T^-1 (Action)
      default_range: contextual
  measurement:
    procedures:
      - name: Observation Sail Deflection
        outline: |
          A coherent particle beam (e.g., electrons) is passed through a multi-path interferometer (e.g., a triadic aperture). Weak, tunable which-way detectors are applied to a subset of the paths, creating an asymmetric Shadow. The resulting imbalance in the far-field interference pattern imparts a net momentum, measured as the static deflection of a sensitive nanocantilever sail placed in the beam path.
        expected_signals: [DC cantilever deflection Δx, shift in far-field diffraction pattern center-of-mass]
        pitfalls: [Thermal drift, mechanical/electrical crosstalk from detectors, beam current instability]
context_windows:
  # Short, trimmed context quotes harvested from modules (3–6 sentences each).
  - module: DOMA-PHYS-003_the_obs_sail
    excerpt: |
      Spatially/basis-asymmetric observation (different weak which-way gains on selected arms) produces an asymmetric interference envelope → net momentum transfer → steady deflection of a compliant sail. No additional conservative force on the plant is required; energy accounting resides in the measurement chain and record handling.
  - module: DOMA-PHYS-003_the_obs_sail
    excerpt: |
      The weak meters raise V_obs on selected arms, lowering usable coherence there (ΔKτ < 0 locally). The triad geometry (Triadic Lock) converts that asymmetric Shadow into an asymmetric phase map. The far-field intensity—and thus momentum flow—follows the agreement geometry.
poetic_connections:
  # Lightweight "word-association graph" and sticky lines.
  motifs: [selective listening, sculpting possibility, erasure as creation, maps that move things]
  evocative_lines:
    - "Your clapping *chose* which ripples live long enough to meet me."
    - "That choice is a map. Maps move things."
  association_matrix:
    # symmetric or directed; weights in [0,1]
    - [ "OBSERVATION_SAIL", 0.9 ]
    - [ "AGREEMENT_GEOMETRY", 0.8 ]
    - [ "V_OBS", 0.8 ]
    - [ "ZENO_WALL", 0.6 ]
formal_mappings:
  # Candidate alignments to EFT/SM/CM/GR terms, each with justification and refs.
  candidates:
    - target: Lindblad dissipator D[c]ρ
      domain: AMO|Math
      mapping_kind: mathematical
      equation_hint: |
        dρ/dt = ... + ∫ dx k(x)·D[c(x)]ρ, where D[c]ρ = cρc† - 1/2{c†c, ρ}
      justification: |
        The creation of a Shadow is formally described by the application of a position-dependent Lindbladian term to the system's density matrix. The measurement strength k(x) directly corresponds to the depth of the Shadow at position x, and the operator c(x) defines which basis is being decohered.
      references:
        - title: Quantum Measurement and Control
          where: H. M. Wiseman & G. J. Milburn, Cambridge University Press
          date: 2009-01-01
      confidence: 0.95
  adopted:
    - target: Position-dependent decoherence rate
      rationale: This is the most direct and widely understood formalism in open quantum systems for describing how a Shadow is implemented mathematically and its effect on a system's coherence.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "A spatial gradient in Shadow depth, created by asymmetric observation, can generate a net, directional force on a coherent system."
      domain: experiment
      falsifier: "In an Observation Sail experiment, the measured cantilever deflection is invariant to the geometry of which-way observation (e.g., swapping observed arms) at constant beam current and detector power, or the deflection sign fails to flip when the observation geometry is inverted."
      status: proposed
      links: [DOMA-PHYS-003_the_obs_sail]
naming_notes:
  collisions: [Shadow (optics)]
  disambiguation: |
    Unlike a classical shadow, which is the passive obstruction of light or particles, a Pirouette Shadow is an *active suppression of quantum coherence* or possibility. It is not an absence of particles, but an absence of a specific kind of interference between potential histories, enforced by an act of measurement.
crosslinks:
  near_synonyms: [ZENO_WALL]
  antonyms: [COHERENCE_RESERVOIR]
  prerequisites: [WEAK_MEASUREMENT, OBSERVER_EFFECT, V_OBS]
  downstream_effects: [OBSERVATION_SAIL, AGREEMENT_GEOMETRY, MEASUREMENT_INDUCED_RATCHET]
license: CC-BY-SA-4.0
---

# Shadow

## Canonical (Pirouette)
A Shadow is a region in a system's configuration space where quantum coherence is actively suppressed by interaction with a measurement device (an observer). This suppression, quantified by an increase in the local Observation Potential (V_obs), damps or "erases" the quantum interference pathways passing through that region. Spatially asymmetric Shadows, or gradients in Shadow depth, create effective potentials that steer the system's dynamics, converting measurement back-action into a directed force.

## EFT-First Summary
The effect of a Shadow is modeled within the framework of open quantum systems as a position-dependent decoherence channel. Its dynamics are captured by a Lindblad master equation where the dissipator's strength, `k(x)`, varies spatially. This term induces not only decoherence but also a related drift force proportional to the gradient of the decoherence strength, `∂x k(x)`, providing a mechanism for measurement-induced control. This is a well-established concept in quantum control and measurement theory. (Ref: Wiseman & Milburn, *Quantum Measurement and Control*).

## Glossary Links
- See also: [Observation Sail](OBSERVATION_SAIL), [Zeno Wall](ZENO_WALL), [Agreement Geometry](AGREEMENT_GEOMETRY)