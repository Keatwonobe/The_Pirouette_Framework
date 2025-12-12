---
term: "Topological Index"
canonical_id: "TOPOLOGICAL_INDEX"
symbol: "T"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COSMO-001"]
---

---
term: Topological Index
canonical_id: TOPOLOGICAL_INDEX
symbol: T
aliases: []
parents: [COSMO-001]
children: [COSMO-Γ-MERGE]
status: candidate
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COSMO-001
      snippet: |
        Model galactic and cluster halos as stationary Γ‑condensate (soliton) solutions labeled by topological index T ∈ ℤ. Derive core properties, rotation curves V_c(r), and lensing convergence κ(θ) from the same potential V(Γ) fixed in COSMO‑Γ‑000...
  editors: [GPT-4o]
  review_log: []
triad:
  art: |
    A cosmic knot's integer twist, carving distinct families of halos from a single primordial field. Each number is a blueprint for a different kind of stable, gravitational island in the void.
  law: |
    The Topological Index `T` is an integer input to the stationary field balance equation for `Γ(r)` that selects a discrete, stable solution from a family of possible halo profiles. Solutions with different `T` exhibit systematically different core properties (`r_c`, `ρ_0`) and contribute to a predictable, T-indexed scatter around the universal surface density `Σ_0`.
  philosophy: |
    The Topological Index introduces a principle of quantized stability into halo structure, replacing stochastic baryonic feedback with a deterministic, non-local quantum number. It posits that the observed diversity of galactic cores is not random but reflects an underlying, discrete order, analogous to the shells of an atom or modes of a drum.
pirouette_definition: |
  The Topological Index, `T`, is an integer quantum number (`T ∈ ℤ`) that uniquely labels discrete families of stationary, spherically symmetric Γ-soliton solutions, `Γ_T(r)`. Each value of `T` corresponds to a topologically distinct field configuration that satisfies the boundary conditions Γ'(0)=0 and Γ(∞)→Γ_∞. Physically, `T` selects a specific halo mass profile from the solution space, yielding predictable core radii (`r_c`), central densities (`ρ_0`), and a characteristic scatter in the `Σ_0` scaling relation.
operational_definition:
  units: Dimensionless integer
  symbol_table:
    - name: T
      meaning: Topological Index
      dimensions: dimensionless
      default_range: ℤ (small integers, e.g., 0, 1, 2, ...)
    - name: Γ_T(r)
      meaning: Γ-soliton profile for a given T
      dimensions: contextual (depends on V(Γ))
      default_range: contextual
    - name: Σ_0
      meaning: Central surface density product (ρ_0 * r_c)
      dimensions: M L⁻²
      default_range: ~10² M_☉ pc⁻²
  measurement:
    procedures:
      - name: Inference from Halo Observables
        outline: |
          1. Measure a galaxy's rotation curve `V_c(r)` and/or a cluster's lensing profile `κ(θ)`.
          2. For a fixed potential `V(Γ)` (per `COSMO-Γ-000`), numerically solve for the family of stationary solutions `Γ_T(r)` for a range of integer `T`.
          3. From each `Γ_T(r)`, compute the predicted observables `V_c,T(r)` and `κ_T(θ)`.
          4. The inferred Topological Index `T` is the integer whose predicted observables provide the best fit (e.g., minimum χ²) to the observational data.
        expected_signals: [A discrete ladder of halo profiles, T-dependent scatter in scaling relations like the Σ_0 locus]
        pitfalls: [Degeneracy with baryonic effects (e.g., adiabatic contraction), Solver non-convergence for certain T-values, Observational errors blurring the distinction between adjacent T-states]
context_windows:
  - module: COSMO-001
    excerpt: |
      Model galactic and cluster halos as stationary Γ‑condensate (soliton) solutions labeled by topological index T ∈ ℤ. Derive core properties, rotation curves V_c(r), and lensing convergence κ(θ) from the same potential V(Γ) fixed in COSMO‑Γ‑000, without introducing particulate DM. A family of stationary solutions Γ_T(r) exists for allowed T, generating collisionless halo mass profiles ρ_Γ(r) with **cored** centers.
  - module: COSMO-001
    excerpt: |
      Prediction: Σ_0 ≡ ρ_0 r_c ≈ Σ_* (nearly constant) across halo masses for fixed V(Γ); weak T‑indexed scatter ΔΣ/Σ_* ≲ 0.2. Variation of T and baryon compression leads to a controlled family of inner slopes; reproduce dwarf diversity without stochastic sub‑grid feedback.
poetic_connections:
  motifs: [quantized states, soliton families, cosmic knots, core diversity, integer order]
  evocative_lines:
    - "...solutions labeled by topological index T ∈ ℤ."
    - "...reproduce dwarf diversity without stochastic sub-grid feedback."
  association_matrix:
    - [ "Γ-SOLITON", 0.9 ]
    - [ "CORE_SURFACE_DENSITY", 0.7 ]
    - [ "BARYON_HALO_COUPLING", 0.5 ]
formal_mappings:
  candidates:
    - target: Winding number / Topological charge
      domain: Math|EFT
      mapping_kind: conceptual
      equation_hint: |
        T ∝ ∫ d³x J⁰_topological
      justification: |
        `T` is an integer that labels distinct, stable field configurations (solitons), which is the definition of a topological charge or winding number in field theory. These charges are conserved for topological reasons and classify non-trivial solutions that cannot be continuously deformed into the vacuum state.
      references:
        - title: Topological Solitons
          where: N. Manton & P. Sutcliffe, Cambridge University Press
          date: 2004-01-01
      confidence: 0.9
  adopted:
    - target: Winding number
      rationale: The term's usage as an integer classifying stable, topologically distinct soliton families is a direct match to the established concept in mathematical physics.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "The diversity in galactic core properties (inner slopes, core sizes) is explained by a discrete family of halo solutions indexed by `T`, combined with predictable baryonic compression effects."
      domain: phenomenology
      falsifier: "Observational data on galaxy cores shows a continuous or random distribution of properties that cannot be binned into discrete families predicted by integer `T` values."
      status: proposed
      links: [COSMO-001]
    - statement: "The central surface density of halos, `Σ_0`, is nearly constant across mass scales, with a small, systematic scatter that is correlated with the inferred Topological Index `T`."
      domain: phenomenology
      falsifier: "The observed scatter in the `Σ_0` relation is large and uncorrelated with any other halo property that could serve as a proxy for `T`, or is fully explained by baryonic feedback alone."
      status: proposed
      links: [COSMO-001]
naming_notes:
  collisions: [Temperature (T), Trace of the stress-energy tensor (T)]
  disambiguation: |
    Distinguish from Temperature (`T`), common in thermodynamics and cosmology, and the trace of the stress-energy tensor (`T = T^μ_μ`) in general relativity. In Pirouette's cosmological modules, `T` without further context refers to this index.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [Γ-FIELD, Γ-SOLITON]
  downstream_effects: [CORE_SURFACE_DENSITY, BARYON_HALO_COUPLING, COSMO-Γ-MERGE]
license: CC-BY-SA-4.0
---

# Topological Index

## Canonical (Pirouette)
The Topological Index, `T`, is an integer quantum number (`T ∈ ℤ`) that uniquely labels discrete families of stationary, spherically symmetric Γ-soliton solutions, `Γ_T(r)`. Each value of `T` corresponds to a topologically distinct field configuration that satisfies the boundary conditions Γ'(0)=0 and Γ(∞)→Γ_∞. Physically, `T` selects a specific halo mass profile from the solution space, yielding predictable core radii (`r_c`), central densities (`ρ_0`), and a characteristic scatter in the `Σ_0` scaling relation.

## EFT-First Summary
The Topological Index `T` is conceptually equivalent to a **Winding number** or topological charge in effective field theory. Such integer charges classify stable, non-dissipative field configurations (solitons) that cannot be continuously deformed into the vacuum state. In the Pirouette Framework, each integer `T` labels a distinct kind of Γ-soliton, which manifests as a galactic halo with specific, measurable properties, providing an ordered, first-principles explanation for the observed diversity of galaxy cores.

## Glossary Links
- See also: Γ-Soliton, Core Surface Density, Baryon-Halo Coupling