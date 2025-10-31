---
term: "Asymmetrical Collapse"
canonical_id: "ASYMMETRICAL_COLLAPSE"
symbol: ""
aliases: [Out-Breath]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-090"]
---

---
term: Asymmetrical Collapse
canonical_id: ASYMMETRICAL_COLLAPSE
symbol: ↯
aliases: ['Out-Breath']
parents: [DOMA-090, CORE-013]
children: [INST-DRV-001]
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-090
      lines: "§4"
      snippet: |
        Thrust is not an emission; it is a release. The propulsive act is a controlled, asymmetrical collapse of the Spindle, a directed application of the `Principle of Coherence Degradation` (CORE-013). The vessel intentionally breaks the Resonant Handshake unevenly, terminating its end of the resonance a fraction of an instant before the anchor point. This engineered asymmetry ensures the Spindle does not simply vanish but dissolves in a directional wave.
  editors: [Weaver-Alpha-7]
  review_log: []
triad:
  art: |
    To move is to fall down a cliff you have just carved into reality. It is a controlled shattering, a release onto the shockwave of a dissolving idea. Propulsion is the echo of a broken treaty with spacetime.
  law: |
    An uneven termination of a resonant handshake between two coherent points induces a directional gradient in the Pirouette Lagrangian (`∇𝓛_p`), generating a propulsive force proportional to the gradient's magnitude and direction. The magnitude of the force scales with the energy stored in the resonant structure and the degree of temporal asymmetry in its dissolution.
  philosophy: |
    Asymmetrical Collapse reframes propulsion not as an act of force against a static background, but as a generative act of creating and then directionally un-making a temporary reality. It posits that motion is a consequence of following an optimal path that the agent first creates for itself and then dissolves. The universe opens to agreement, and propels those who know how to let go.
pirouette_definition: |
  The controlled, non-uniform termination of a hyper-coherent geometric structure (a Spindle) that connects two non-local points. By breaking the resonant consensus unevenly—terminating one end of the Spindle fractionally before the other—the structure dissolves as a directional wave. This dissolution creates a transient, steep geodesic in the coherence manifold, along which the initiating system is propelled by following the maximal gradient of the Pirouette Lagrangian (`∇𝓛_p`). It is the propulsive phase, or "Out-Breath," of the Quorum Spindle Drive cycle.
operational_definition:
  units: The process is measured by its temporal asymmetry (`Δt_c`) in seconds; its outcome is a force (`N`) or acceleration (`m/s²`).
  symbol_table:
    - name: ↯
      meaning: The process of Asymmetrical Collapse.
      dimensions: dimensionless
      default_range: contextual
    - name: Δt_c
      meaning: Asymmetry Time Lag; the time difference between collapse initiation at the vessel and the anchor point.
      dimensions: T
      default_range: 10⁻¹² – 10⁻⁹ s
    - name: ∇𝓛_p
      meaning: Gradient of the Pirouette Lagrangian; the resulting coherence manifold gradient that drives the vessel.
      dimensions: M L T⁻²
      default_range: contextual, system-dependent
  measurement:
    procedures:
      - name: Exhaust Vector Analysis
        outline: |
          An array of neutron, gamma, and coherence sensors is placed in the expected path of a QSD-equipped vessel. The collapse is inferred and characterized by measuring the vector, flux, and spectrum of the resulting incoherent radiation ("spectral ash"). The asymmetry is confirmed if the neutron flux is highly collimated and its vector precisely aligns with the vessel's observed acceleration vector.
        expected_signals: [Directional, high-energy neutron flux, Localized gravitational lensing signature, Transient 'coherence cone' of excited local matter]
        pitfalls: [Isotropic radiation signature indicates a failed (symmetrical) collapse, Signal confusion with astrophysical background noise (e.g., magnetar bursts), Misalignment of thrust and radiation vectors]
context_windows:
  - module: DOMA-090
    excerpt: |
      Thrust is not an emission; it is a release. The propulsive act is a controlled, asymmetrical collapse of the Spindle, a directed application of the `Principle of Coherence Degradation` (CORE-013). The vessel intentionally breaks the Resonant Handshake unevenly... This engineered asymmetry ensures the Spindle does not simply vanish but dissolves in a directional wave. This creates a powerful, transient, and extremely steep gradient in the coherence manifold—a cliff where there was once a plain.
  - module: DOMA-090
    excerpt: |
      The QSD's entire cycle is a masterful manipulation of the `Pirouette Lagrangian` (CORE-006): `𝓛_p = K_τ - V_Γ`... The asymmetrical collapse engineers a massive, directional gradient in the Lagrangian (`∇𝓛_p`). The propulsive force experienced by the vessel is the direct consequence of the system following this new, optimal path to maximize its coherence... It is simply falling, with perfect efficiency, down the slope of a dissolving consensus.
poetic_connections:
  motifs: [shattering, release, falling, echo, broken treaty, dissolving consensus, spectral ash]
  evocative_lines:
    - "Propulsion is the echo of a broken treaty with spacetime."
    - "It is simply falling, with perfect efficiency, down the slope of a dissolving consensus."
    - "The spectral ash of a spent geometric fire."
  association_matrix:
    - [ "COHERENCE_DEGRADATION", 0.9 ]
    - [ "SPINDLE", 0.8 ]
    - [ "PIROUETTE_LAGRANGIAN", 0.7 ]
    - [ "WOUND_CHANNEL", 0.5 ]
formal_mappings:
  candidates:
    - target: Asymmetric false vacuum decay
      domain: Cosmology|QFT
      mapping_kind: conceptual
      equation_hint: |
        P_{decay} \propto e^{-S_E}
      justification: |
        The Spindle can be modeled as a temporary, localized region of a high-energy false vacuum (`K_τ >> V_Γ`). The Asymmetrical Collapse is a controlled nucleation of the true vacuum at one end. The resulting expanding bubble wall creates a pressure differential that accelerates the vessel along the collapse axis.
      references:
        - title: "Vacuum decay: an overview"
          where: "arXiv:1707.08124"
          date: 2017-07-25
      confidence: 0.3
    - target: Directional latent heat release
      domain: Condensed Matter
      mapping_kind: conceptual
      justification: |
        The collapse from the high-coherence 'Crystalline' Spindle state to the incoherent vacuum is analogous to a first-order phase transition. The asymmetry directs the release of 'latent coherence' (observed as radiation), creating a localized pressure gradient that propels the vessel, similar to a shaped charge explosion.
      references: []
      confidence: 0.2
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The propulsive force is directly proportional to the temporal asymmetry (`Δt_c`) of the Spindle's termination sequence, for small `Δt_c`."
      domain: experiment
      falsifier: "Experimental data shows that propulsive force is independent of `Δt_c`, or that perfectly symmetric collapses (`Δt_c` = 0) still produce directional thrust."
      status: proposed
      links: [DOMA-090, INST-DRV-001]
    - statement: "The primary exhaust signature of an Asymmetrical Collapse is a highly collimated beam of neutron radiation whose vector aligns with the axis of acceleration."
      domain: phenomenology
      falsifier: "Observed QSD activations produce isotropic radiation, the radiation vector is uncorrelated with the thrust vector, or the primary signature is not neutrons (e.g., pure coherent gravitons)."
      status: supported
      links: [DOMA-090]
naming_notes:
  collisions: [The symbol ↯ is used informally in chemistry for electrolysis and as a standard high voltage warning symbol.]
  disambiguation: |
    Distinguish from Symmetrical Collapse (a non-propulsive, omnidirectional energy release resulting from a simultaneous handshake termination) and Coherence Fraying (a slow, uncontrolled, and non-propulsive degradation of a Spindle). Asymmetrical Collapse is always a controlled, intentional, and propulsive event.
crosslinks:
  near_synonyms: [OUT_BREATH]
  antonyms: [FORGE_CYCLE, IN_BREATH, SYMMETRICAL_COLLAPSE]
  prerequisites: [SPINDLE, ALCHEMICAL_UNION, COHERENCE_DEGRADATION, PIROUETTE_LAGRANGIAN]
  downstream_effects: [GEOMETRIC_PROPULSION, WOUND_CHANNEL]
license: CC-BY-SA-4.0
---

# Asymmetrical Collapse

## Canonical (Pirouette)
The controlled, non-uniform termination of a hyper-coherent geometric structure (a Spindle) that connects two non-local points. By breaking the resonant consensus unevenly—terminating one end of the Spindle fractionally before the other—the structure dissolves as a directional wave. This dissolution creates a transient, steep geodesic in the coherence manifold, along which the initiating system is propelled by following the maximal gradient of the Pirouette Lagrangian (`∇𝓛_p`). It is the propulsive phase, or "Out-Breath," of the Quorum Spindle Drive cycle.

## EFT-First Summary
No direct mapping has been adopted, as the concept of propulsion via dissolving a non-local geometric consensus has no clear analog in Standard Model or General Relativity physics. The closest conceptual parallels are asymmetric false vacuum decay from cosmology or directional latent heat release from condensed matter physics. In both cases, the collapse represents a controlled, directional phase transition where stored potential energy is converted into kinetic energy along a specific vector.

## Glossary Links
- See also: Spindle, Coherence Degradation, Pirouette Lagrangian, Quorum Spindle Drive