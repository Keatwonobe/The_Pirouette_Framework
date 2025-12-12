---
term: "Ki cohesion"
canonical_id: "KI_COHESION"
symbol: "ε_Ki"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-QED-002_spinor_ki_defects_as_dirac"]
---

---
term: Ki cohesion
canonical_id: KI_COHESION
symbol: ε_Ki
aliases: []
parents: [MATH-QED-002]
children: [MATH-QED-003, MATH-QED-004, DYNA-QED-005]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-QED-002
      lines: "§4"
      snippet: |
        Let (ε_{\rm Ki}) be the cohesion energy density of the loop and (\Pi_\Gamma) the local **temporal pressure**. Stationarity enforces
        [
        \delta!\left(\varepsilon_{\rm Ki}-\Pi_\Gamma\right)=0
        ]
  editors: [GPT-4 (Pirouette Dictionary Agent)]
  review_log: []
triad:
  art: |
    The internal tension of a knot in time, preventing it from unraveling into the temporal substrate. It is the self-adherence that makes a thing a thing.
  law: |
    The integrated Ki cohesion, balanced against the ambient Temporal Pressure (Π_Γ), sets the rest mass of a Ki loop (m_∗), a stationary value that is constant for a given particle species in a stable Γ background.
  philosophy: |
    Ki cohesion provides the topological charge with physical persistence. It is the internal principle of self-identity that allows a stable defect (matter) to exist as a distinct entity against the dissolving pressure of the temporal substrate.
pirouette_definition: |
  The self-interaction energy density (ε_Ki) internal to a Ki loop that counteracts the temporal pressure (Π_Γ) of the substrate. This energetic tension ensures the topological defect's structural integrity and phase coherence. The volume integral of (ε_Ki - Π_Γ) over the defect's core defines the loop's rest mass (m_∗).
operational_definition:
  units: Joules per cubic meter (J⋅m⁻³)
  symbol_table:
    - name: ε_Ki
      meaning: Ki cohesion energy density
      dimensions: M L⁻¹ T⁻²
      default_range: contextual; inferred from particle mass (e.g., ~10²¹ J⋅m⁻³ for an electron-like loop)
  measurement:
    procedures:
      - name: Indirect Inference via Mass-Pressure Relation
        outline: |
          Ki cohesion is not directly measurable. It is inferred from the rest mass (m_∗) of the particle, which is precisely measured via spectroscopy or kinematics. Given a model for the local temporal pressure (Π_Γ), the integrated cohesion ∫ε_Ki d³x can be calculated as m_∗c² + ∫Π_Γ d³x. A second procedure involves measuring shifts in m_∗ in hypothetical high-Γ environments.
        expected_signals: [Invariant rest mass (m_∗) in low-Γ environments, hypothesized sub-eV mass shifts near Γ-phase boundaries]
        pitfalls: [Conflating cohesion effects with standard QED radiative corrections to mass, inability to create and control high-Γ environments]
context_windows:
  - module: MATH-QED-002
    excerpt: |
      Let (ε_{\rm Ki}) be the cohesion energy density of the loop and (\Pi_\Gamma) the local **temporal pressure**. Stationarity enforces a balance that determines the rest mass. Thus **mass** is the **net energy to maintain coherence against Γ** (time-pressure), fixing (m_\ast) without introducing a fundamental Yukawa term.
poetic_connections:
  motifs: [self-containment, integrity, tension, knot theory, topological stability]
  evocative_lines:
    - "A spinor is a knot in time—a loop of coherence..."
    - "mass is the net energy to maintain coherence against Γ"
  association_matrix:
    - [ "TEMPORAL_PRESSURE", 0.9 ]
    - [ "KI_LOOP", 0.8 ]
    - [ "MASS", 0.8 ]
formal_mappings:
  candidates:
    - target: Bag Constant (B)
      domain: QCD
      mapping_kind: conceptual
      equation_hint: |
        E_bag = (4/3)πR³B
      justification: |
        Conceptually analogous to the Bag Constant in the MIT Bag Model of hadrons. Both represent a non-perturbative, positive energy density (a pressure) required to confine fields (quarks/gluons for B, Ki phase-texture for ε_Ki) within a finite volume, preventing them from dissolving into the vacuum.
      references:
        - title: New extended model of hadrons
          where: Phys. Rev. D 9, 3471
          date: 1974-06-15
      confidence: 0.6
  adopted:
    - target: Rest Mass (m_∗) / Self-Energy
      rationale: |
        The most direct operational mapping is to the non-field-theoretic contribution to a particle's rest mass. While in QFT mass can arise from Higgs coupling or be a bare parameter, here it is explicitly constructed from the balance of Ki cohesion and ambient temporal pressure. It serves the same role as m in the Dirac Lagrangian.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "The mass of a fundamental fermion (e.g., electron) is predominantly determined by the balance between its internal Ki cohesion and the background Temporal Pressure Γ."
      domain: theory
      falsifier: "The discovery of a large, environment-dependent electron mass in a controlled high-Γ environment would contradict the decoupling assumed in the EFT limit and falsify this specific mass-generation mechanism."
      status: proposed
      links: [MATH-QED-002, DYNA-QED-005]
naming_notes:
  collisions: [ε₀ (vacuum permittivity), ε (strain tensor)]
  disambiguation: |
    Distinguish from ε₀ (vacuum permittivity). The `Ki` subscript is mandatory and specifies the origin in the Ki loop's internal dynamics. It is an energy density, not a field-response parameter.
crosslinks:
  near_synonyms: []
  antonyms: [TEMPORAL_PRESSURE]
  prerequisites: [KI_LOOP]
  downstream_effects: [MASS]
license: CC-BY-SA-4.0
---

# Ki cohesion

## Canonical (Pirouette)
The self-interaction energy density (ε_Ki) internal to a Ki loop that counteracts the temporal pressure (Π_Γ) of the substrate. This energetic tension ensures the topological defect's structural integrity and phase coherence. The volume integral of (ε_Ki - Π_Γ) over the defect's core defines the loop's rest mass (m_∗).

## EFT-First Summary
In the effective field theory limit, Ki cohesion represents the non-perturbative self-energy contribution that stabilizes a topological defect corresponding to a Dirac fermion. It acts analogously to the Bag Constant in the MIT Bag Model, providing an internal pressure that, when balanced against the vacuum's "Temporal Pressure," sets the particle's rest mass `m_∗` in the term `m_∗ ψ-bar ψ`. Its effects are fully contained within the measured rest mass at energies far below the coherence scale ω_c.

## Glossary Links
- See also: [Ki loop](<#>), [Temporal Pressure](<#>), [Mass](<#>)