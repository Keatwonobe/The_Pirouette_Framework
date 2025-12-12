---
term: "Mass-dependent coupling"
canonical_id: "MASS_DEPENDENT_COUPLING"
symbol: "g_ℓ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-013"]
---

---
term: Mass-dependent coupling
canonical_id: MASS_DEPENDENT_COUPLING
symbol: g_ℓ
aliases: []
parents: [MATH-013]
children: []
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-013
      lines: "L25-L28"
      snippet: |
        **Scaling hypothesis:** heavier leptons couple more strongly to temporal pressure,
        [
        g_\ell=\kappa\left(\frac{m_\ell}{m_e}\right)^p,\qquad p\ge 0,
        ]
        with base strength (\kappa\equiv g_e). Default working choice: **(p=1)** (linear mass scaling), but keep (p) symbolic.
  editors: [GPT-4-Pirouette]
  review_log: []
triad:
  art: |
    A particle's mass is its antenna. Heavier leptons resonate more strongly with the background hum of the Temporal Forge, feeling its pressure as a more significant force.
  law: |
    The interaction strength `g_ℓ` between a lepton `ℓ` and the Pressuron field is a dimensionless Yukawa coupling that scales as a power `p` of the lepton's mass `m_ℓ` relative to the electron mass `m_e`. This scaling law, `g_ℓ = κ(m_ℓ/m_e)^p`, is testable via precision measurements of lepton properties.
  philosophy: |
    This coupling realizes the principle that mass is not a passive property but an active measure of a particle's engagement with the universe's temporal substrate. It provides a direct, falsifiable mechanism linking a particle's intrinsic scale (mass) to the framework's unique background field, making phenomenology a direct probe of fundamental ontology.
pirouette_definition: |
  The mass-dependent coupling, `g_ℓ`, is the dimensionless Yukawa coupling constant governing the interaction strength between a lepton of type `ℓ` (field `ψ_ℓ`) and the Pressuron scalar field `Γ`. The coupling is defined by the interaction Lagrangian term `g_ℓ Γ ψ̄_ℓ ψ_ℓ`. It is hypothesized to scale with lepton mass according to the power law `g_ℓ = κ(m_ℓ/m_e)^p`, where `κ` is the base coupling strength (for the electron) and `p` is the scaling exponent.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: g_ℓ
      meaning: Coupling strength for a given lepton ℓ.
      dimensions: dimensionless
      default_range: contextual, constrained by experiment
    - name: κ
      meaning: Base coupling strength, defined as g_e.
      dimensions: dimensionless
      default_range: "< 10⁻⁴ (from a_e constraints)"
    - name: m_ℓ
      meaning: Mass of lepton ℓ.
      dimensions: M
      default_range: contextual (e.g., 0.511 MeV/c² for electron)
    - name: p
      meaning: Mass-scaling exponent.
      dimensions: dimensionless
      default_range: "p ≥ 0, with p=1 as the default working hypothesis."
  measurement:
    procedures:
      - name: Lepton Anomalous Magnetic Moment Inference
        outline: |
          1. Measure the anomalous magnetic moment `a_ℓ` for a specific lepton `ℓ` (e.g., the muon).
          2. Calculate the Standard Model prediction for `a_ℓ`.
          3. Attribute the measured discrepancy, `Δa_ℓ = a_ℓ(exp) - a_ℓ(SM)`, to the one-loop Pressuron contribution.
          4. Use the formula `Δa_ℓ = (α / 12π²) κ² (m_ℓ/m_e)^(2p) * f(m_Γ/m_ℓ)` to solve for the parameters `(κ, p)` given a value for the Pressuron mass `m_Γ`.
          5. Repeat for at least two different leptons (e.g., electron and muon) to constrain both `κ` and `p` simultaneously.
        expected_signals: [A non-zero `Δa_ℓ` for heavy leptons (muon, tau), A ratio `Δa_μ / Δa_e` that significantly deviates from 1]
        pitfalls: [Other new physics contributing to `a_ℓ`, Insufficient experimental precision to distinguish `p=1` from `p=2`, Strong dependence on the unknown Pressuron mass `m_Γ`]
context_windows:
  - module: MATH-013
    excerpt: |
      We model the lepton as a Dirac field (ψ_ℓ) and take a **Yukawa-type** portal to the pressuron (Γ). **Mass dimensions (4D):** ([\psi]=3/2), ([\Gamma]=1) (⇒) ([g_ℓ]=0) (dimensionless Yukawa). This keeps (Δa_ℓ∼α,g_ℓ²) and makes power counting transparent. **Scaling hypothesis:** heavier leptons couple more strongly to temporal pressure, `g_ℓ = κ(m_ℓ/m_e)^p`.
  - module: MATH-013
    excerpt: |
      Using `g_ℓ = κ(m_ℓ/m_e)^p`, the contribution to the anomalous magnetic moment takes the numerical form: `Δa_ℓ = (α / 12π²) κ² (m_ℓ/m_e)^(2p) f(m_Γ/m_ℓ)`, where `f(0)=1`. For the muon target `Δa_μ ≈ 2.5×10⁻⁹`, this formula fixes `κ` as a function of `p` and the Pressuron mass, providing a direct link between theory and experiment.
poetic_connections:
  motifs: [mass as antenna, gravitational weight, temporal storm, particle resonance]
  evocative_lines:
    - "heavier leptons couple more strongly to temporal pressure"
    - "The anomalous song of the muon is...the sound of a heavy particle being buffeted by the ceaseless storm of the Temporal Forge."
  association_matrix:
    - [ "TEMPORAL_PRESSURE", 0.9 ]
    - [ "LEPTON_MASS", 0.9 ]
    - [ "PRESSURON", 0.8 ]
formal_mappings:
  candidates:
    - target: Yukawa coupling
      domain: QFT
      mapping_kind: mathematical
      equation_hint: |
        L_int = g_Y ϕ ψ̄ ψ
      justification: |
        The module explicitly models the Pressuron-lepton interaction as a `g_ℓ Γ ψ̄_ℓ ψ_ℓ` term in the Lagrangian. This is the canonical form of a Yukawa interaction between a scalar field (Γ) and a Dirac fermion field (ψ_ℓ), where `g_ℓ` is the Yukawa coupling constant.
      references:
        - title: An Introduction to Quantum Field Theory
          where: Chapter 4
          date: 1995-10-11
      confidence: 1.0
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The coupling strength g_ℓ scales with lepton mass according to g_ℓ ∝ (m_ℓ)^p for a universal, non-zero exponent p."
      domain: phenomenology
      falsifier: "Experimental measurements of `Δa_e`, `Δa_μ`, and `Δa_τ` are inconsistent with a single power-law scaling. For example, if `Δa_μ` is confirmed to be large while future measurements show `Δa_τ` is negligible."
      status: under-test
      links: [MATH-013]
    - statement: "For any valid p > 0, the base coupling κ must be small enough that the predicted contribution to the electron's g-2 (`Δa_e`) does not exceed experimental bounds."
      domain: experiment
      falsifier: "The parameters `(κ, p)` required to explain the muon g-2 anomaly predict a value for `Δa_e` that is conclusively larger than the experimentally measured value."
      status: proposed
      links: [MATH-013]
naming_notes:
  collisions: [The symbol 'g' is commonly used for gauge couplings (e.g., `g_s` for the strong force) or the metric tensor. The subscript `g_ℓ` provides necessary specificity.]
  disambiguation: |
    `g_ℓ` is the coupling to the scalar Pressuron field, not the electromagnetic coupling `e` (charge) which governs the lepton's interaction with photons. Both contribute to the lepton's total magnetic moment, but `g_ℓ` is responsible for the *anomalous* contribution within the Pirouette Framework.
crosslinks:
  near_synonyms: []
  antonyms: [UNIVERSAL_COUPLING]
  prerequisites: [PRESSURON, LEPTON]
  downstream_effects: [ANOMALOUS_MAGNETIC_MOMENT_CONTRIBUTION]
license: CC-BY-SA-4.0
---