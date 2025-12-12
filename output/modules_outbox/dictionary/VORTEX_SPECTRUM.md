---
term: "Vortex spectrum"
canonical_id: "VORTEX_SPECTRUM"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["SECT-001"]
---

---
term: Vortex spectrum
canonical_id: VORTEX_SPECTRUM
symbol: κ_v
aliases: [Quantized Circulation]
parents: [SECT-001, SECT-Γ-A-HALO]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: SECT-001
      lines: "Section 3"
      snippet: |
        **Vortex spectrum** in rotating systems: quantized circulation κ_v = 2π/m_H; predicts a minimal vortex spacing ∝ √(c_s/Ω) (Ω rotation rate).
  editors: [pirouette-gpt4-alpha]
  review_log: []
triad:
  art: |
    Cosmic whirlpools etched into the dark, where the flow of the universe is not smooth but steps in discrete, spinning quanta. Each vortex is a silent storm, a knot in the superfluid aether whose existence is dictated by phase coherence.
  law: |
    In a rotating superfluid halo described by the P(X) EFT, fluid circulation Γ is quantized in integer multiples of the fundamental quantum κ_v = 2π/m_H. The spatial density and arrangement of these vortices are determined by the halo's angular velocity Ω and the superfluid sound speed c_s.
  philosophy: |
    The Vortex Spectrum transforms the abstract U(1) phase symmetry of the superfluid into a concrete, observable kinematic pattern within galactic halos. It provides a "smoking gun" signature, distinguishing this model from scalar field or particle-based dark matter candidates by predicting discrete, rather than continuous, rotational states.
pirouette_definition: |
  The set of allowed, discrete circulation values {nκ_v | n ∈ ℤ} that can manifest as stable vortices in a rotating superfluid dark matter halo. The fundamental quantum of circulation, κ_v = 2π/m_H, is set by the mass of the constituent pressuron, m_H. The density and arrangement of these vortices provide a falsifiable kinematic prediction tied to the halo's rotation rate and the superfluid's equation of state.
operational_definition:
  units: m²/s (for circulation quantum)
  symbol_table:
    - name: κ_v
      meaning: Quantum of circulation
      dimensions: L² T⁻¹
      default_range: "2π/m_H ≈ 2.18 × 10⁻³ m²/s for m_H=17 MeV"
    - name: m_H
      meaning: Mass of the microscopic pressuron quantum
      dimensions: M
      default_range: "17 MeV/c²"
    - name: Ω
      meaning: Angular velocity of the rotating halo
      dimensions: T⁻¹
      default_range: contextual
    - name: n
      meaning: Integer quantum number of a vortex line
      dimensions: dimensionless
      default_range: ℤ
  measurement:
    procedures:
      - name: Kinematic Mapping of Rotating Halos
        outline: |
          Use Integral Field Unit (IFU) spectroscopy or stellar stream dynamics to map the velocity field of gas or stars within a rapidly rotating, dark-matter-dominated galaxy. Search for discrete jumps, shear layers, or localized non-Keplerian features in the velocity map consistent with the presence of vortices. A power spectrum analysis of stream perturbations can also reveal characteristic scales set by vortex spacing.
        expected_signals: [Sharp, localized velocity gradients in rotation curves, Statistical excess of specific velocity shears corresponding to nκ_v, Characteristic modes in stellar stream power spectra]
        pitfalls: [Baryonic feedback and turbulence can create complex velocity structures that mimic vortices, Insufficient spatial/velocity resolution can smear the discrete signal, Projection effects obscure vortex cores]
context_windows:
  - module: SECT-001
    excerpt: |
      Core predictions:
      **Constant surface‑density locus** Σ_0 ≡ ρ_0 r_c emerges from ξ and σ: Σ_0 ≈ C(α,β,σ,m_H) nearly mass‑independent (matches COSMO‑Γ‑HALO P1).
      **Vortex spectrum** in rotating systems: quantized circulation κ_v = 2π/m_H; predicts a minimal vortex spacing ∝ √(c_s/Ω) (Ω rotation rate).
  - module: SECT-001
    excerpt: |
      Section 6 — Distinctive, Falsifiable Signatures
      A) **Halo cores with universal Σ_0** and **vortex spectra** in fast rotators (IFU kinematics; stellar streams).
      B) **Merger offset scaling** without invoking particulate self‑interaction; predicts specific v_rel dependence through interface work.
poetic_connections:
  motifs: [cosmic whirlpool, quantized spin, superfluidity, dark flow, phase coherence]
  evocative_lines:
    - "**Vortex spectrum** in rotating systems: quantized circulation..."
    - "vacuum as fuzzy baseline that creeps like the CMB"
  association_matrix:
    - [ "HALO_CORE", 0.8 ]
    - [ "SUPERFLUID_PRESSURON", 0.9 ]
    - [ "U1_PHASE_SYMMETRY", 1.0 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Quantized vortex (in a BEC or superfluid)
      domain: AMO|CM
      mapping_kind: mathematical
      equation_hint: |
        ∮ v · dl = n (2πħ / m)
      justification: |
        Circulation quantization is a generic feature of superfluids described by a complex field ψ = √n e^{iθ}. The requirement that the phase θ be single-valued (modulo 2π) upon traversing a closed loop necessitates that the circulation, derived from the velocity field v ∝ ∇θ, be an integer multiple of 2π/m (with ħ=1). This is a direct analogue to vortices in laboratory superfluids.
      references:
        - title: Bose-Einstein Condensation in Dilute Gases
          where: "Pethick, C. J., & Smith, H. (2008), Chapter 9"
          date: 2008-04-17
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The circulation in rotating dark matter halos is quantized in units of κ_v = 2π/m_H."
      domain: phenomenology
      falsifier: "The definitive observation of a continuum of circulation values, or the systematic absence of any vortex-induced kinematic signatures in a population of rapidly rotating, dark matter-dominated galaxies where they are predicted to be observable."
      status: proposed
      links: [SECT-001]
naming_notes:
  collisions: [Vorticity power spectrum (fluid dynamics)]
  disambiguation: |
    Distinguish from the continuous vorticity power spectrum used in classical turbulence analysis. The Pirouette Vortex Spectrum refers to the discrete, allowed *values* of circulation, a macroscopic quantum mechanical effect arising from the U(1) phase symmetry of the underlying field.
crosslinks:
  near_synonyms: [QUANTIZED_CIRCULATION]
  antonyms: [LAMINAR_FLOW, CONTINUOUS_VORTICITY]
  prerequisites: [SUPERFLUID_PRESSURON, P_OF_X_LAGRANGIAN]
  downstream_effects: [HALO_KINEMATICS, STELLAR_STREAM_PERTURBATIONS]
license: CC-BY-SA-4.0
---

# Vortex spectrum

## Canonical (Pirouette)
The set of allowed, discrete circulation values {nκ_v | n ∈ ℤ} that can manifest as stable vortices in a rotating superfluid dark matter halo. The fundamental quantum of circulation, κ_v = 2π/m_H, is set by the mass of the constituent pressuron, m_H. The density and arrangement of these vortices provide a falsifiable kinematic prediction tied to the halo's rotation rate and the superfluid's equation of state.

## EFT-First Summary
In the P(X) effective field theory for the Superfluid Pressuron model, the U(1) phase symmetry of the complex field `ψ` leads directly to the quantization of circulation. This phenomenon is a direct cosmological analogue to quantized vortices in laboratory superfluids like Bose-Einstein Condensates (cf. Pethick & Smith, 2008). The predicted spectrum of circulation `Γ = n(2π/m_H)` provides a direct, measurable link between the microscopic pressuron mass (`m_H` ≈ 17 MeV) and macroscopic, observable kinematics in rotating galactic halos.

## Glossary Links
- See also: [[HALO_CORE]], [[SUPERFLUID_PRESSURON]]