---
term: "Multi-Γ Chain"
canonical_id: "MULTI_CHAIN"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-021"]
---

---
term: Multi-Γ Chain
canonical_id: MULTI_GAMMA_CHAIN
symbol: 
aliases: [Clockwork Mechanism, Alignment Mechanism]
parents: [MATH-021]
children: [COSMO-Γ-CMB, HALO/MERGE]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-021
      lines: "Mechanism B"
      snippet: |
        L = Σ_i ½(∂ϕ_i)^2 − ½ m^2(ϕ_i − q ϕ_{i+1})^2 − V_tail(ϕ_N)
        Diagonalize M^2 → eigenvalues {m_H ≈ m, …, m_L ≈ m/q^{N}}; eigenvectors fix couplings.
        Choose q,N from symmetry (discrete shift), not from data (MATH‑018 D2/D3).
  editors: [System Agent]
  review_log: []
triad:
  art: |
    A cascade of whispers along a structured chain, where many small, local shifts conspire to create a single, deep note that resonates across the cosmos.
  law: |
    A sector of N scalar fields with nearest-neighbor coupling `q` generates a mass spectrum with eigenvalues scaling as `m/q^k`, producing an exponentially light eigenstate `m_L` and suppressed couplings from a heavy fundamental scale `m`.
  philosophy: |
    To derive vast scale separation not from ad-hoc tuning or accident, but from the inherent architecture of a coupled system, replacing a "hierarchy problem" with a "connectivity problem."
pirouette_definition: |
  The physical realization of the clockwork mechanism as a solution to the Γ Mass Tension. The Multi-Γ Chain is a sector of N scalar fields (`ϕ_i`) with nearest-neighbor interactions parameterized by a fundamental mass `m` and a dimensionless coupling `q`. Diagonalization of the mass matrix yields an exponentially hierarchical spectrum of mass eigenstates. The heaviest eigenstate, `Γ_H`, acquires a mass `m_H ≈ m` (≈17 MeV) and couples to leptons, while the lightest, `Γ_L`, has a mass `m_L ≈ m/q^N` (≈10⁻²² eV) and serves as the cosmological ultralight field. The couplings of `Γ_L` to matter are likewise exponentially suppressed, naturally explaining its cosmological role and its evasion of fifth-force constraints.
operational_definition:
  units: Fields `ϕ_i` and mass `m` are in units of energy (e.g., eV). `N` and `q` are dimensionless.
  symbol_table:
    - name: N
      meaning: Number of scalar fields (sites) in the chain.
      dimensions: dimensionless
      default_range: O(10) - O(100)
    - name: q
      meaning: Dimensionless nearest-neighbor coupling parameter.
      dimensions: dimensionless
      default_range: >2
    - name: m
      meaning: Fundamental mass scale of the sector, setting the mass of the heaviest eigenstate.
      dimensions: M
      default_range: ≈ 17 MeV
    - name: ϕ_i
      meaning: The i-th scalar field in the interaction basis.
      dimensions: M
      default_range: contextual
    - name: Γ_H, Γ_L
      meaning: The heaviest and lightest mass eigenstates of the chain.
      dimensions: M
      default_range: m_H ≈ 17 MeV, m_L ≈ 10⁻²² eV
  measurement:
    procedures:
      - name: Cosmological Eigenmode Inference
        outline: |
          Perform a global fit to high-precision CMB temperature, polarization, and lensing data (e.g., TT, TE, EE spectra). The light eigenstate `Γ_L` acts as an ultralight dark matter component, inducing subtle, `(q,N)`-dependent phase shifts in the acoustic peaks and modifying the lensing potential.
        expected_signals: [Small, non-zero residuals in CMB acoustic peak phases, specific modifications to the matter power spectrum at small scales.]
        pitfalls: [Degeneracy with other cosmological parameters (e.g., `n_s`, `H_0`), requires percent-level precision in CMB measurements.]
      - name: Precision Lepton Coupling Test
        outline: |
          Measure the anomalous magnetic moments (g-2) of the electron, muon, and tau lepton with sufficient precision to resolve contributions from `Γ_H` loops. The chain structure predicts a specific, non-universal pattern of couplings `g_e : g_μ : g_τ` that depends on the eigenvector mixing.
        expected_signals: [A consistent pattern of deviations from the Standard Model prediction for lepton g-2 values, violation of lepton flavor universality in related observables.]
        pitfalls: [Hadronic and other SM uncertainties obscuring the signal, required precision may be beyond current experimental reach.]
      - name: Equivalence Principle Violation Search
        outline: |
          Use high-sensitivity torsion balance or atom interferometry experiments to search for a new long-range force mediated by `Γ_L`. The chain predicts a non-zero but exponentially suppressed `q^{-N}` coupling to baryons.
        expected_signals: [A positive detection of an EP-violating force at a level of 10⁻¹³–10⁻¹⁵, consistent with the cosmologically-inferred `(q,N)` values.]
        pitfalls: [Signal is predicted to be near the threshold of planned experiments, systematic errors and environmental noise.]
context_windows:
  - module: MATH-021
    excerpt: |
      Mechanism B — Clockwork/Alignment in a Multi-Γ Chain (Two Eigenstates from One Sector)
      Hypothesis
      B1. Γ is a *sector* of N coupled scalars with nearest‑neighbor couplings producing exponentially hierarchical eigenmasses (clockwork/alignment).
      B2. Heavy eigenstate Γ_H couples to leptons (g−2 portal) with O(1) mixing; light eigenstate Γ_L is exponentially light and weakly coupled, sourcing cosmology.
  - module: MATH-021
    excerpt: |
      Decision Tree (Discriminants)
      D1. **CMB acoustic phases**: clockwork (B) predicts small residual phase shifts; superfluid (A) and cascade (C) give different lensing amplitudes.
      D3. **Lab/precision**: (B) implies definite coupling patterns testable in g−2/EDM/global EW fits; (A) implies medium‑dependent optical signatures; (C) implies nothing current‑day but strong cosmological transition marks.
poetic_connections:
  motifs: [hierarchy, cascade, gears, symmetry, resonance]
  evocative_lines:
    - "Choose q,N from symmetry, not from data."
    - "natural evasion with a calculable residual."
  association_matrix:
    - [ "Γ Mass Tension", 0.9 ]
    - [ "Symmetry", 0.7 ]
    - [ "Predictivity", 0.6 ]
formal_mappings:
  candidates:
    - target: Clockwork Mechanism / KNP Alignment
      domain: BSM/EFT
      mapping_kind: mathematical
      equation_hint: |
        L = Σ_i [ ½(∂ϕ_i)² − V(ϕ_i) ] − ½ m²(ϕ_i − q ϕ_{i+1})²
      justification: |
        The Multi-Γ Chain is a direct implementation of the clockwork mechanism, a theoretical tool for generating exponentially large hierarchies from O(1) parameters. The Lagrangian, mass matrix, and resulting hierarchical spectrum of masses and couplings are mathematically identical to those presented in the original clockwork literature.
      references:
        - title: "The Clockwork Mechanism"
          where: "Phys. Rev. Lett. 115, 201801 (2015) [arXiv:1508.05013]"
          date: 2015-11-06
        - title: "A Natural Theory of the Weak Scale"
          where: "JHEP 09 (2016) 094 [arXiv:1511.00139]"
          date: 2015-11-01
      confidence: 0.95
  adopted:
    - target: Clockwork Mechanism
      rationale: The module explicitly identifies this structure with "clockwork/alignment" and uses its defining mathematical features. This mapping is direct and intentional.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The heavy eigenstate `Γ_H` couples non-universally to lepton flavors (e, μ, τ) with a specific pattern determined by the chain's structure."
      domain: phenomenology
      falsifier: "Precision measurements of lepton anomalous magnetic moments and other flavor observables show no deviation from the Standard Model, or show a deviation pattern inconsistent with any allowed `(q,N)`."
      status: proposed
      links: [MATH-021, XXP-015]
    - statement: "The light eigenstate `Γ_L` induces characteristic, small phase shifts in the CMB acoustic peaks."
      domain: cosmology
      falsifier: "Next-generation CMB observatories (e.g., CMB-S4) find no evidence for such phase shifts, ruling out the cosmologically relevant `(q,N)` parameter space."
      status: proposed
      links: [MATH-021, COSMO-Γ-CMB]
    - statement: "The chain generates a calculable, non-zero fifth force mediated by `Γ_L`, suppressed by `q^{-N}`."
      domain: experiment
      falsifier: "Equivalence Principle tests place limits on new forces that are stronger than the predicted residual force for any `(q,N)` combination consistent with cosmology and lepton physics."
      status: proposed
      links: [MATH-021]
naming_notes:
  collisions: [The symbol Γ is used for various quantities in physics (e.g., Gamma function, decay width). The term "chain" is generic.]
  disambiguation: |
    The Multi-Γ Chain (Mechanism B) is one of three proposed solutions to the Γ Mass Tension, distinct from the Composite Superfluid (A) and Phase Transition (C) models. The Chain mechanism is defined by a *sector* of N fundamental fields generating a static, hierarchical mass spectrum via nearest-neighbor couplings. This contrasts with Mechanism A, which uses collective phonon excitations in a single-field condensate, and Mechanism C, which involves a dynamical phase transition of a single field.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [GAMMA_MASS_TENSION]
  downstream_effects: [COSMO_GAMMA_CMB, HALO_MERGE]
license: CC-BY-SA-4.0