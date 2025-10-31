---
term: "Critical Angular Velocity"
canonical_id: "CRITICAL_ANGULAR_VELOCITY"
symbol: "Ω_c"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["COSMO-006"]
---

---
term: Critical Angular Velocity
canonical_id: CRITICAL_ANGULAR_VELOCITY
symbol: Ω_c
aliases: []
parents: [COSMO-006]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: COSMO-006
      lines: "SECT-Γ-A-HALO.3"
      snippet: |
        Critical angular velocity for first vortex: Ω_c ≈ (ħ/m_H r_c^2) ln(r_c/ξ);
  editors: [system]
  review_log: []
triad:
  art: |
    A quiescent fluid, spun faster and faster, resists with perfect smoothness until the strain becomes too great. At a precise moment, it yields by birthing a tiny whirlpool, a spiraling filament of nothingness that relieves the rotational stress.
  law: |
    For a rotating superfluid system with core radius `r_c` and healing length `ξ`, a single quantized vortex will spontaneously form if and only if its angular velocity `Ω` exceeds the critical value `Ω_c`. This threshold is set by the energy balance between the irrotational state and the state with one vortex, scaling as `Ω_c ∝ (1/r_c^2) ln(r_c/ξ)`.
  philosophy: |
    `Ω_c` marks a fundamental phase transition in a dynamic system, the point where a simple, smooth state must yield to a topologically complex one to accommodate angular momentum. It is a sharp, predictive link between the microphysics of a superfluid (particle mass, healing length) and the macrophysics of a galaxy halo (rotation, core size), making it a key observable for validating the superfluid paradigm.
pirouette_definition: |
  The critical angular velocity, `Ω_c`, is the minimum angular velocity at which the free energy of a rotating superfluid system is lowered by the nucleation of a single quantized vortex. It is determined by the system's core radius `r_c`, the superfluid healing length `ξ`, and the mass of the constituent particle `m_H`. Exceeding this threshold marks the transition from a purely irrotational flow state to one containing topological defects that carry the system's angular momentum.
operational_definition:
  units: rad s⁻¹
  symbol_table:
    - name: Ω_c
      meaning: Critical angular velocity
      dimensions: T⁻¹
      default_range: contextual
    - name: ħ
      meaning: Reduced Planck constant
      dimensions: M L² T⁻¹
      default_range: 1.054e-34 J s
    - name: m_H
      meaning: Mass of the superfluid constituent particle
      dimensions: M
      default_range: 1e-22 eV/c² to 1e-2 eV/c²
    - name: r_c
      meaning: Core radius of the halo/condensate
      dimensions: L
      default_range: 0.1 - 10 kpc
    - name: ξ
      meaning: Superfluid healing length
      dimensions: L
      default_range: < 1 pc
  measurement:
    procedures:
      - name: Vortex Stability Threshold Simulation
        outline: |
          In a numerical simulation (`solver: FV+HLLC | spectral`), initialize a stationary halo profile as per `SECT-Γ-A-HALO.2`. Impose a rigid-body rotation `Ω` and allow the system to relax. Increment `Ω` in small steps, monitoring the system's energy and phase topology. `Ω_c` is the lowest value of `Ω` for which a stable phase singularity (vortex) appears and lowers the total energy. The test requires the measured `Ω_c` to match the analytical estimate to within the solver tolerance (`tol`).
        expected_signals: [Appearance of a stable phase singularity in the `vortex_map` output, a non-zero value in the `vortex_thresholds` field of the `halo_sf.json` artifact]
        pitfalls: [Numerical dissipation suppressing vortex formation, insufficient mesh resolution (`N_r`) to resolve the vortex core]
context_windows:
  - module: COSMO-006
    excerpt: |
      Outputs: (r_c, ρ_0, Σ_0, V_c(r), κ(θ)); vortex stability threshold vs. Ω. ... Critical angular velocity for first vortex: Ω_c ≈ (ħ/m_H r_c^2) ln(r_c/ξ); vortex lattice spacing d_v ∝ √(c_s/Ω).
  - module: COSMO-006
    excerpt: |
      Rotating systems are characterized by the nucleation of quantized vortices when the angular velocity exceeds a critical threshold, Ω_c. The presence of these vortices leads to observable non-circular flows in IFU maps and potential wiggles in stellar-stream power spectra at wave numbers corresponding to the vortex lattice spacing.
poetic_connections:
  motifs: [spinning, threshold, rupture, nucleation, whirlpool]
  evocative_lines:
    - "the minimum angular velocity at which it becomes energetically favorable for a vortex to form."
    - "a quiescent pool... a dimple of nothingness, a vortex, blossoms at its heart to release the tension."
  association_matrix:
    - [ "QUANTIZED_VORTEX", 0.9 ]
    - [ "ANGULAR_MOMENTUM", 0.8 ]
    - [ "CORE_RADIUS", 0.7 ]
    - [ "HEALING_LENGTH", 0.7 ]
formal_mappings:
  candidates:
    - target: Ω_{c1} (First critical angular velocity in superfluids)
      domain: AMO
      mapping_kind: mathematical
      equation_hint: |
        Ω_c ≈ (ħ/m R²) ln(R/ξ)
      justification: |
        The formula in `COSMO-006` is a direct analogue of the canonical result for vortex nucleation in a trapped Bose-Einstein Condensate (BEC). The halo core radius `r_c` plays the role of the trap radius `R`, and the physical origin—balancing the kinetic energy of rotation against the energy cost of a vortex line—is identical.
      references:
        - title: Rotating trapped Bose-Einstein condensates
          where: Rev. Mod. Phys. 81, 647
          date: 2009-04-29
      confidence: 0.95
  adopted:
    - target: Ω_{c1} (First critical angular velocity in Bose-Einstein Condensates)
      rationale: The mathematical form and physical origin are identical to the established result in the AMO/BEC literature. This provides a strong physical anchor and allows cross-pollination of numerical techniques and phenomenological expectations.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The formation of the first stable vortex in a relaxed, rotating superfluid halo is exclusively governed by Ω_c; no vortices will form in systems rotating with Ω < Ω_c."
      domain: theory
      falsifier: "A demonstration, either theoretical or numerical, of a vortex formation mechanism independent of bulk rotation (e.g., via violent relaxation or non-equilibrium dynamics) that can produce stable vortices in a system with global Ω < Ω_c."
      status: proposed
      links: [COSMO-006]
naming_notes:
  collisions: [The symbol `Ω_c` is used in standard cosmology for the critical density parameter of the universe.]
  disambiguation: |
    Within superfluid halo modules (`COSMO-006`), `Ω` always denotes angular velocity. The subscript `c` here means 'critical' for vortex formation. This should be distinguished from its cosmological usage, typically written as `Ω_crit` or in contexts with other density parameters like `Ω_m` and `Ω_Λ`.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [HEALING_LENGTH, CORE_RADIUS, QUANTIZED_VORTEX]
  downstream_effects: [VORTEX_LATTICE]
license: CC-BY-SA-4.0
---

# Critical Angular Velocity

## Canonical (Pirouette)
The critical angular velocity, `Ω_c`, is the minimum angular velocity at which the free energy of a rotating superfluid system is lowered by the nucleation of a single quantized vortex. It is determined by the system's core radius `r_c`, the superfluid healing length `ξ`, and the mass of the constituent particle `m_H`. Exceeding this threshold marks the transition from a purely irrotational flow state to one containing topological defects that carry the system's angular momentum.

## EFT-First Summary
The Pirouette `Ω_c` is the direct analogue of the first critical angular velocity `Ω_{c1}` in rotating Bose-Einstein Condensates (BECs). It represents the rotational frequency at which it becomes energetically favorable to nucleate a single quantized vortex line to carry angular momentum, rather than maintaining a purely irrotational velocity field. Its value depends on the ratio of the system's size (core radius `r_c`) to its coherence length (healing length `ξ`), providing a key link between macroscopic halo properties and the microscopic parameters of the superfluid dark matter model (see Fetter, 2009, Rev. Mod. Phys. 81, 647).

## Glossary Links
- See also: [Quantized Vortex](...), [Healing Length](...), [Core Radius](...)