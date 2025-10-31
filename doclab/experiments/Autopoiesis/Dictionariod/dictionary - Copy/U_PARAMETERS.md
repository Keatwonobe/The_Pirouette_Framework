---
term: "U_parameters"
canonical_id: "U_PARAMETERS"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["COSMO-004"]
---

---
term: U_parameters
canonical_id: U_PARAMETERS
symbol: U_params
aliases: [Universal Parameters, Frozen Constants]
parents: [COSMO-004]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: COSMO-004
      snippet: |
        U_parameters:
          m_Gamma_eV: 1.7e7     # 17 MeV (pressuron)
          lambda4: 0.0
          V_tail:
            type: exp_shallow
            mu_eV: 1.0e-33
            Gamma_star_Mpl: 1.0
  editors: [system-agent]
  review_log: []
triad:
  art: |
    The immutable laws of a simulated cosmos, etched in stone before its first dawn. These are the fixed stars by which its entire history, from cosmic web to galactic core, must navigate.
  law: |
    The `U_parameters` are the set of scalar constants {`m_Γ`, `λ₄`, ...} defining the potential V(Γ) for a given Freeze. They are fixed once in a `freeze_manifest.yaml` and are computationally immutable across all subsequent modules (cosmology, halo, merge) that reference that manifest.
  philosophy: |
    To enforce theoretical and computational consistency by separating the *universal laws* of a model (the U_parameters) from contingent initial conditions or observer-dependent parameters. This ensures that a halo profile and a cosmological power spectrum are guaranteed to be derived from the exact same underlying physics.
pirouette_definition: |
  The set of universal, scalar physical constants that define the potential V(Γ) of the Γ field. These parameters, such as the field's mass (`m_Gamma_eV`) and self-interaction couplings (`lambda4`), are specified within a Freeze Manifest. Once "frozen", they are treated as immutable constants for all subsequent calculations within a given simulation suite, ensuring physical consistency from cosmological scales down to individual object solvers.
operational_definition:
  units: Primarily energy (eV) or dimensionless.
  symbol_table:
    - name: m_Gamma_eV
      meaning: Mass of the Γ field.
      dimensions: Energy (M L² T⁻²)
      default_range: "[10⁻³³, 10¹⁰] eV"
    - name: lambda4
      meaning: Quartic self-coupling constant of the Γ potential.
      dimensions: dimensionless
      default_range: "[0, ∞)"
    - name: mu_eV
      meaning: Energy scale of the potential's tail, V_tail.
      dimensions: Energy (M L² T⁻²)
      default_range: contextual
    - name: Gamma_star_Mpl
      meaning: Field value scale for V_tail, in Planck units.
      dimensions: dimensionless
      default_range: contextual
  measurement:
    procedures:
      - name: Freeze Manifest Specification
        outline: |
          Values are not measured but are specified a priori in a `freeze_manifest.yaml` file. This file is cryptographically committed (via git hash) and serves as the single source of truth for the model's physics. Downstream modules (e.g., Boltzmann, halo, or merge solvers) read this file to configure their physical models, ensuring consistency.
        expected_signals:
          - A `U_parameters` block in a valid YAML Freeze Manifest.
          - Invariant values for potential V(Γ) derivatives across different computational modules referencing the same manifest.
        pitfalls:
          - Using different manifests for different stages of a simulation pipeline, breaking physical consistency.
          - Failure to re-run all dependent simulations after a manifest is updated.
context_windows:
  - module: COSMO-004
    excerpt: |
      C) Freeze Manifest Template (YAML)
      freeze_manifest.yaml
      anchor:
        type: Omega_m0
        value: 0.315
        justification: "One‑shot global scale set; all U,T frozen thereafter."
      U_parameters:
        m_Gamma_eV: 1.7e7
        lambda4: 0.0
        V_tail:
          type: exp_shallow
          mu_eV: 1.0e-33
  - module: COSMO-004
    excerpt: |
      D2. Halo Solver (YAML)
      halo_config.yaml
      freeze_manifest: path/to/freeze_manifest.yaml
      potential:
        type: quadratic_plus_tail
        m_Gamma_eV: ${from_freeze}
        lambda4: ${from_freeze}
        tail:
          type: exp_shallow
          mu_eV: ${from_freeze}
          Gamma_star_Mpl: ${from_freeze}
poetic_connections:
  motifs: [frozen, universal law, manifest, immutability, single source of truth]
  evocative_lines:
    - "One‑shot global scale set; all U,T frozen thereafter."
    - "m_Gamma_eV: ${from_freeze}"
  association_matrix:
    - [ "FREEZE_MANIFEST", 0.9 ]
    - [ "POTENTIAL_V_GAMMA", 0.8 ]
    - [ "T_INDICES", 0.3 ]
formal_mappings:
  candidates: []
  adopted:
    - target: EFT Lagrangian Parameters {m², λ, ...}
      domain: EFT
      mapping_kind: mathematical
      equation_hint: |
        V(Γ) = (1/2) m_Γ² Γ² + (λ₄/4!) Γ⁴ + V_tail(Γ)
      justification: |
        These parameters directly correspond to the free constants in the Lagrangian density defining the Γ scalar field model. They are the fundamental numbers of the theory, to be constrained by experiment (or, in this framework, set for a simulation). The `m_Gamma_eV` and `lambda4` map directly to the mass and quartic coupling terms.
      references: []
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The set of `U_parameters` defined in a Freeze Manifest is sufficient to fully specify the potential V(Γ) and its derivatives for all Pirouette modules."
      domain: theory
      falsifier: "A downstream module (e.g., a new radiative transfer calculation) requires a physical parameter of the Γ model (e.g., a coupling to photons) that is not included in the standard `U_parameters` set, forcing a breaking change to the Freeze Manifest specification."
      status: supported
      links: [COSMO-004]
naming_notes:
  collisions: [The symbol 'U' is commonly used for potential energy in physics. Here, `U_parameters` refers to "Universal" parameters.]
  disambiguation: |
    `U_parameters` are distinct from `T_indices`. `U_parameters` define the universal physics (the shape of the potential V(Γ)) for an entire simulated cosmos. `T_indices` are instance-specific parameters that select a particular solution or state *within* that universal physics (e.g., selecting a specific halo profile from a family of solutions).
crosslinks:
  near_synonyms: []
  antonyms: [T_INDICES]
  prerequisites: [FREEZE_MANIFEST]
  downstream_effects: [POTENTIAL_V_GAMMA]
license: CC-BY-SA-4.0
---

# U_parameters

## Canonical (Pirouette)
The set of universal, scalar physical constants that define the potential V(Γ) of the Γ field. These parameters, such as the field's mass (`m_Gamma_eV`) and self-interaction couplings (`lambda4`), are specified within a Freeze Manifest. Once "frozen", they are treated as immutable constants for all subsequent calculations within a given simulation suite, ensuring physical consistency from cosmological scales down to individual object solvers.

## EFT-First Summary
The `U_parameters` are the free parameters of the effective field theory (EFT) Lagrangian for the Γ scalar field. They correspond directly to terms like the mass (`m_Gamma_eV`) and self-interaction couplings (`lambda4`) that define the potential V(Γ). In the Standard Model or its extensions, these would be fundamental constants of nature to be measured experimentally; in Pirouette, they are fixed for a given simulated universe via a Freeze Manifest.

## Glossary Links
- See also: [Freeze Manifest](<link-to-freeze-manifest>), [T_indices](<link-to-t-indices>)