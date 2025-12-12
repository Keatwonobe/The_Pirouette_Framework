---
term: "Motion"
canonical_id: "MOTION"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-017"]
---

---
term: Motion
canonical_id: MOTION
symbol: p⃗ₖ
aliases: [Traversal, Propagation]
parents: [DOMA-017]
children: [DYNA-001, DYNA-002]
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-017
      snippet: |
        | Verb   | Geometry of Resonance | Description & Temporal Dynamics                                                                                                            |
        | :---   | :---                  | :---                                                                                                                                       |
        | Motion | Helical Wave          | The Ki pattern of a system tracing a geodesic. It is a resonance that propagates through the coherence manifold... Its action is to *traverse*. |
  editors: [aydao-v1]
  review_log: []
triad:
  art: |
    To move is not to displace, but to sing a traveling note through the fabric of coherence. It is the universe's oldest story: the journey from here to there, written as a spiral of existence.
  law: |
    A system in Motion follows a geodesic in the coherence manifold, a path of maximal coherence preservation (max ∫𝓛ₚ dt). Its velocity and direction are encoded in the pitch and orientation of its helical Ki resonance.
  philosophy: |
    Motion is not a property of an object but a state of resonance the object adopts. It redefines 'location' as a phase in a propagating wave, unifying the concepts of being and becoming into a single, dynamic geometry.
pirouette_definition: |
  Motion is one of the fundamental quantized coherence modes, defined as a stable, helical Ki resonance that propagates through the coherence manifold. This geometry represents the act of 'traversal' and is the state adopted by a system following a geodesic. The helix's pitch corresponds to the system's momentum, and its axis defines the direction of propagation, making it an informationally complete representation of a system's trajectory.
operational_definition:
  units: kg⋅m⋅s⁻¹ (Momentum)
  symbol_table:
    - name: p⃗ₖ
      meaning: Momentum vector of the helical Ki resonance.
      dimensions: MLT⁻¹
      default_range: contextual
  measurement:
    procedures:
      - name: Ki Phase-Shift Interferometry
        outline: |
          Couple the target system (in Motion) with a reference system in a known state (e.g., Rest). The interference pattern of their Ki resonances will exhibit a phase shift and beat frequency. The frequency shift (Doppler effect) is proportional to the momentum's magnitude, and the spatial asymmetry of the interference fringes reveals its vector direction.
        expected_signals: [Doppler-shifted Ki resonance frequency, Asymmetric interference fringe pattern]
        pitfalls: [Local manifold curvature can induce Aharonov-Bohm-like phase shifts, mistakable for momentum; High temporal pressure (Γ) can cause rapid decoherence of the interference pattern.]
context_windows:
  - module: DOMA-017
    excerpt: |
      **Motion** | Helical Wave | The Ki pattern of a system tracing a geodesic. It is a resonance that propagates through the coherence manifold, its helical nature encoding both its direction and momentum. Its action is to *traverse*.
  - module: DOMA-017
    excerpt: |
      A system in a **pure mode** like **Rest** or **Bind** has found a deep, local minimum in the potential landscape (V_Γ), maximizing its stability and temporal coherence (K_τ). A system in **Motion** is following a geodesic—a path of maximal coherence—through the manifold.
poetic_connections:
  motifs: [journey, spiral, wave, geodesic, unfolding, rhythm]
  evocative_lines:
    - "We sought a universe of nouns and found only verbs."
    - "Action is the universe's relentless search for the most elegant word."
  association_matrix:
    - [ "REST", -0.8 ]
    - [ "GEODESIC", 0.9 ]
    - [ "COHERENCE_MANIFOLD", 0.7 ]
    - [ "LAGRANGIAN", 0.5 ]
formal_mappings:
  candidates:
    - target: de Broglie wave (p = ħk)
      domain: QM
      mapping_kind: conceptual
      equation_hint: |
        |p⃗ₖ| ∝ (helical pitch)⁻¹
      justification: |
        Motion as a helical Ki resonance directly parallels the de Broglie hypothesis, where a particle's momentum is intrinsically linked to a wave property (wavelength/wavenumber). The helical pitch of the Ki resonance is the Pirouette analog of the de Broglie wavelength, recasting wave-particle duality as a geometric feature of coherence.
      references:
        - title: "Sur l'onde-particule"
          where: "Louis de Broglie, 1924 PhD thesis"
          date: 1924-11-25
      confidence: 0.9
    - target: Kinetic Energy Term (T)
      domain: CM
      mapping_kind: mathematical
      justification: |
        The propagation of the helical wave contributes to the system's kinetic coherence (K_τ) in the Pirouette Lagrangian (𝓛ₚ), analogous to how the kinetic energy term (T = ½mv²) contributes to the classical Lagrangian (L = T - V). A higher momentum (p⃗ₖ) corresponds to a larger K_τ.
      confidence: 0.8
  adopted:
    - target: de Broglie wave (p = ħk)
      rationale: This mapping provides the most direct bridge to established physics, recasting wave-particle duality as a geometric property of a system's state of being. It preserves the core relationship between momentum and wave characteristics.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "A system in a pure Motion state follows a geodesic of the local coherence manifold."
      domain: phenomenology
      falsifier: "The observation of a system in a stable, pure Motion state spontaneously deviating from a geodesic without any detectable interacting resonance would falsify this claim."
      status: proposed
      links: [DOMA-017]
naming_notes:
  collisions: [The symbol `p` for momentum is standard but can be confused with pressure; `k` for wavenumber is also standard. The composite `p⃗ₖ` is used to explicitly link the momentum to the wave-like Ki resonance.]
  disambiguation: |
    Distinguish from the generic concept of movement. In Pirouette, Motion is a specific, quantized coherence mode, not a continuous change of position. A system can be 'moving' in a colloquial sense while being in a complex superposition; the term 'Motion' refers only to the pure helical resonance state.
crosslinks:
  near_synonyms: []
  antonyms: [REST]
  prerequisites: [KI, COHERENCE_MANIFOLD, LAGRANGIAN]
  downstream_effects: [GEODESIC, OBSERVE]
license: CC-BY-SA-4.0
---

# Motion

## Canonical (Pirouette)
Motion is one of the fundamental quantized coherence modes, defined as a stable, helical Ki resonance that propagates through the coherence manifold. This geometry represents the act of 'traversal' and is the state adopted by a system following a geodesic. The helix's pitch corresponds to the system's momentum, and its axis defines the direction of propagation, making it an informationally complete representation of a system's trajectory.

## EFT-First Summary
In the language of quantum mechanics, Motion is the Pirouette Framework's description of the de Broglie wave. A system's momentum is not an extrinsic property but is encoded as the inverse pitch (wavenumber) of its intrinsic, helical Ki resonance. This state propagates as a wave-packet along a geodesic, with its dynamics governed by a Lagrangian analogous to that in classical mechanics. This recasts wave-particle duality as a fundamental geometric state of coherence.

## Glossary Links
- See also: REST, KI, COHERENCE_MANIFOLD, GEODESIC