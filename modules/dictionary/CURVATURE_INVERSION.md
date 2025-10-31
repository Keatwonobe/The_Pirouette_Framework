---
term: "Curvature Inversion"
canonical_id: "CURVATURE_INVERSION"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-096"]
---

---
term: Curvature Inversion
canonical_id: CURVATURE_INVERSION
symbol: κ_eff → 0⁻
aliases: [Phase-Folding Event]
parents: [DOMA-096]
children: [DOMA-097, DOMA-098]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-096
      lines: "§5"
      snippet: |
        Transition occurs through **Curvature Inversion** in the coherence manifold:
        [κ_{eff} = κ_0 (1 − Γ/Γ_c)]
        As Γ approaches Γ_c, curvature inverts and laminar flow becomes chaotic.
  editors: [system-ai-writer]
  review_log: []
triad:
  art: |
    The smooth landscape of order buckles and flips inside-out, birthing a storm from its own distorted reflection. It is the geometric moment when a surface becomes a chasm.
  law: |
    The effective curvature of a coherence manifold, `κ_{eff}`, inverts sign as temporal pressure `Γ` crosses a critical value `Γ_c`. This event deterministically triggers a phase transition from geodesic (laminar) to chaotic (turbulent) flow.
  philosophy: |
    Curvature Inversion establishes that stability is not an absolute state but a geometric property contingent on pressure. It posits that chaos is not a breakdown of order, but its necessary geometric dual, accessible via a smooth, predictable transition.
pirouette_definition: |
  The geometric event where the effective curvature (`κ_{eff}`) of a coherence manifold inverts its sign as temporal pressure (`Γ`) approaches a critical threshold (`Γ_c`). This inversion drives the transition from a stable, laminar coherence regime (where `κ_{eff} > 0`) to a dissipative, turbulent regime (where `κ_{eff} < 0`), visualized as a phase-folding of the Caduceus vortices (Ψ⁺, Ψ⁻).
operational_definition:
  units: dimensionless condition
  symbol_table:
    - name: κ_{eff}
      meaning: Effective coherence curvature
      dimensions: L⁻²
      default_range: (-∞, κ_0]
    - name: κ_0
      meaning: Intrinsic (base) manifold curvature at Γ=0
      dimensions: L⁻²
      default_range: contextual, > 0
    - name: Γ
      meaning: Temporal pressure
      dimensions: contextual (e.g., action, energy density)
      default_range: [0, ∞)
    - name: Γ_c
      meaning: Critical temporal pressure for inversion
      dimensions: same as Γ
      default_range: contextual, > 0
  measurement:
    procedures:
      - name: Manifold Curvature Spectroscopy via Flow Bifurcation
        outline: |
          Introduce a test coherence stream (e.g., a low-amplitude Ψ⁺ field) into the system. Incrementally increase temporal pressure `Γ` while monitoring the stream's trajectory via the Caduceus Operator (ℭ). The value of `Γ` at which the stream's geodesics abruptly bifurcate or |ℭ| exhibits a sharp, nonlinear increase corresponds to `Γ_c`. The function `κ_{eff}(Γ)` is then inferred from the flow's deviation from base geodesics.
        expected_signals: [Sharp increase in Caduceus Operator magnitude |ℭ|, onset of triadic vortices, phase-slip events in cognitive manifolds.]
        pitfalls: [Mistaking local noise for a global curvature inversion, system drift in `Γ_c` due to topological memory (κ-memory) from previous cycles.]
context_windows:
  - module: DOMA-096
    excerpt: |
      Transition occurs through **Curvature Inversion** in the coherence manifold: [κ_{eff} = κ_0 (1 − Γ/Γ_c)]. As Γ approaches Γ_c, curvature inverts and laminar flow becomes chaotic. The Caduceus visualizes this as a phase-folding event where Ψ⁺ and Ψ⁻ exchange dominance.
  - module: DOMA-096
    excerpt: |
      **Topological Memory:** Each laminar–turbulent cycle leaves a structural imprint in manifold curvature (κ-memory), measurable via phase recurrence metrics.
poetic_connections:
  motifs: [inside-out geometry, phase-folding, catastrophe, mirror-world transition]
  evocative_lines:
    - "The Caduceus visualizes this as a phase-folding event where Ψ⁺ and Ψ⁻ exchange dominance."
    - "Each laminar–turbulent cycle leaves a structural imprint in manifold curvature (κ-memory)..."
  association_matrix:
    - [ "TEMPORAL_PRESSURE", 0.9 ]
    - [ "TURBULENCE", 0.8 ]
    - [ "CADUCEUS_LENS", 0.7 ]
    - [ "KAPPA_MEMORY", 0.6 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Pitchfork/Transcritical Bifurcation
      domain: Math
      mapping_kind: mathematical
      equation_hint: |
        The governing equation `κ_{eff} = κ_0(1 - Γ/Γ_c)` maps the control parameter `Γ` to the stability of the system's fixed point (geodesic flow). At `Γ = Γ_c`, the fixed point at the origin loses stability, and new attractors emerge, mirroring a classical bifurcation.
      justification: |
        The inversion of curvature is analogous to the change in stability of a fixed point in bifurcation theory. As the control parameter (`Γ`) passes a critical value (`Γ_c`), the potential energy landscape of the system fundamentally changes, causing the system's state (flow trajectory) to transition from a single stable configuration (laminar) to a new, often chaotic or multi-stable, one (turbulent).
      references:
        - title: Nonlinear Dynamics and Chaos
          where: Strogatz, S. H.
          date: 1994-01-01
      confidence: 0.85
constraints_and_falsifiers:
  claims:
    - statement: "The transition from laminar to turbulent flow in all Pirouette-compliant systems is mediated by a Curvature Inversion event governed by the linear relationship κ_{eff} ∝ (Γ_c - Γ)."
      domain: theory
      falsifier: "Observation of a laminar-turbulent transition where the effective curvature does not invert sign, or where the transition follows a different functional dependence on Γ (e.g., exponential, quadratic)."
      status: proposed
      links: [DOMA-096]
naming_notes:
  collisions: [The symbol κ for curvature is standard in differential geometry.]
  disambiguation: |
    Distinguish from the static, intrinsic manifold curvature (`κ_0`). Curvature Inversion is a *dynamical event* driven by temporal pressure (`Γ`), representing a change in the *effective* geometry experienced by coherence flows.
crosslinks:
  near_synonyms: [PHASE_FOLDING_EVENT]
  antonyms: [GEODESIC_INTEGRITY, LAMINAR_PERSISTENCE]
  prerequisites: [TEMPORAL_PRESSURE, COHERENCE_MANIFOLD]
  downstream_effects: [TURBULENT_BURST, KAPPA_MEMORY, CASCADE_ONSET]
license: CC-BY-SA-4.0
---

# Curvature Inversion

## Canonical (Pirouette)
The geometric event where the effective curvature (`κ_{eff}`) of a coherence manifold inverts its sign as temporal pressure (`Γ`) approaches a critical threshold (`Γ_c`). This inversion drives the transition from a stable, laminar coherence regime (where `κ_{eff} > 0`) to a dissipative, turbulent regime (where `κ_{eff} < 0`), visualized as a phase-folding of the Caduceus vortices (Ψ⁺, Ψ⁻).

## EFT-First Summary
Curvature Inversion models the onset of chaos as a pitchfork or transcritical bifurcation, a core concept in dynamical systems theory. The system's effective potential, governed by manifold curvature (`κ_eff`), changes stability as a control parameter, Temporal Pressure (`Γ`), crosses a critical threshold. This forces the system state from a single stable fixed point (laminar, geodesic flow) to an unstable one, triggering an abrupt transition to a new set of attractors (turbulent flow). This provides a geometric mechanism for phase transitions described in theories of critical phenomena.

## Glossary Links
- See also: [Temporal Pressure](<#>), [Caduceus Lens](<#>), [Turbulence](<#>), [Kappa Memory](<#>)