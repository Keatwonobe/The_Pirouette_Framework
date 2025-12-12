---
term: "Pseudoscalar"
canonical_id: "PSEUDOSCALAR"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-Γ-001_the_pressurons_identity"]
---

---
term: Pseudoscalar
canonical_id: PSEUDOSCALAR
symbol: J^(PC) = 0^(-+)
aliases: [spin-0 odd-parity particle, axion-like particle]
parents: [DYNA-Γ-001]
children: [DYNA-Γ-002, COSMO-Γ-001]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DYNA-Γ-001
      lines: "L15-L17"
      snippet: |
        ...where ( \delta\Gamma ) transforms as a **pseudoscalar** under temporal inversion ( t \rightarrow -t ).
  editors: [Pirouette-Genesis-Agent]
  review_log: []
triad:
  art: |
    The breathing mode of time’s fabric, representing the phase inversion of temporal curvature. It is the phase recoil of the universe when mass bends time faster than coherence can repair itself.
  law: |
    A particle or field with quantum numbers J=0, P=-1, C=+1 (CP=-1) that couples to fermions via a derivative interaction, `L_int ∝ (∂_μ Γ) * ψ̄γ^μγ₅ψ`, ensuring interactions are suppressed for light fermions.
  philosophy: |
    A pseudoscalar interaction defines how coherent time-pressure dissipates into the particle sea. It is a physical analog to coherence collapse, framing particle decay as the resolution of a stress in the temporal fabric.
pirouette_definition: |
  A quantum excitation with spin J=0 and odd parity (P=-1), specifically transforming non-trivially under temporal inversion (`t → -t`). In the Pirouette Framework, the Pressuron (Γ) is a pseudoscalar, mediating coherence stress through a derivative coupling to matter that scales with fermion mass. This identity dictates its decay kinematics, primarily into lepton pairs (`e⁺e⁻`), and provides a falsifiable signature for temporal-pressure phenomena.
operational_definition:
  units: Dimensionless (quantum numbers)
  symbol_table:
    - name: J
      meaning: Total angular momentum (Spin)
      dimensions: dimensionless
      default_range: 0
    - name: P
      meaning: Parity transformation eigenvalue
      dimensions: dimensionless
      default_range: -1
    - name: C
      meaning: Charge conjugation eigenvalue
      dimensions: dimensionless
      default_range: +1
    - name: L_int
      meaning: Pseudoscalar interaction Lagrangian
      dimensions: M L⁻¹ T⁻² (Energy Density)
      default_range: contextual
  measurement:
    procedures:
      - name: Lepton Pair Decay Kinematics
        outline: |
          Produce Pressurons (Γ) in a beam-dump experiment or high-luminosity collider. Isolate candidate events by searching for a narrow resonance in the invariant mass distribution of electron-positron pairs. Reconstruct the decay angle of the leptons in the Γ particle's rest frame.
        expected_signals:
          - A narrow invariant mass peak at `m_Γ ≈ 17 MeV`.
          - Mild angular anisotropy in the `e⁺e⁻` decay distribution, consistent with a spin-0, odd-parity parent state.
        pitfalls:
          - Misidentification of isotropic decays from a scalar particle.
          - High backgrounds from standard QED processes (e.g., bremsstrahlung) that can mimic the signal.
context_windows:
  - module: DYNA-Γ-001
    excerpt: |
      Linearizing the temporal-pressure field...gives: `Γ(x) = Γ_0 + δΓ(x)`, where `δΓ` transforms as a **pseudoscalar** under temporal inversion (`t → -t`). Thus, its fundamental quantum numbers are: Spin (`J=0`), Parity (`P=-1`), Charge Conjugation (`C=+1`), and CP (`-1`). This identifies the Pressuron excitation as a pseudoscalar, which dictates the form of its interaction with matter.
  - module: DYNA-Γ-001
    excerpt: |
      BESIII and NA64 exclude scalar decays in this mass band for photon-dominant channels, but **pseudoscalar leptonic channels remain unconstrained**. Belle II, FASER 2, and DarkQuest could observe a transient excess at 17 MeV in e⁺e⁻ invariant mass distributions, especially in missing-momentum searches with soft-lepton tagging.
poetic_connections:
  motifs: [phase inversion, breathing mode, coherence collapse, temporal recoil]
  evocative_lines:
    - "We sought a particle and found a pulse of time."
    - "To measure it is to catch the universe inhaling between its own heartbeats."
  association_matrix:
    - [ "Pressuron", 1.0 ]
    - [ "Temporal Pressure", 0.8 ]
    - [ "Coherence Collapse", 0.7 ]
    - [ "Leptonic Anomaly", 0.6 ]
formal_mappings:
  candidates:
    - target: Axion-Like Particle (ALP)
      domain: EFT
      mapping_kind: conceptual
      equation_hint: |
        L_int = (∂_μ a / f_a) ψ̄γ^μγ₅ψ
      justification: |
        The Pressuron (Γ) shares the key properties of an ALP: it is a light (~17 MeV), neutral, CP-odd pseudoscalar that couples derivatively to fermions and possesses a two-photon decay channel. The primary difference is the theoretical origin (temporal pressure vs. Peccei-Quinn symmetry) and the specific quadratic mass-scaling (`g_Γ ∝ m_ℓ`) of its fermion coupling.
      references:
        - title: The Landscape of ALPs
          where: PDG Review of Particle Physics
          date: 2024-08-15
      confidence: 0.9
  adopted:
    - target: Axion-Like Particle (ALP)
      rationale: The ALP framework provides the closest, most operationally useful language in standard particle physics for describing the phenomenology of the Pressuron.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "The Pressuron (Γ) particle is a pseudoscalar with quantum numbers J^(PC) = 0^(-+)."
      domain: phenomenology
      falsifier: "Observation of an isotropic angular distribution in its dominant e⁺e⁻ decay channel would favor a scalar (0^(++)) assignment. Measurement of non-zero spin or positive parity would directly refute this identity."
      status: proposed
      links: [DYNA-Γ-001]
naming_notes:
  collisions: [The symbol Γ is also used for the Gamma function in mathematics and the decay width in particle physics. Context (e.g., Γ-field, m_Γ) is crucial for disambiguation.]
  disambiguation: |
    A "scalar" refers to a spin-0 particle with even parity (P=+1), while a "pseudoscalar" has odd parity (P=-1). This distinction is critical for decay kinematics and interaction Lagrangians; a scalar decay is isotropic while a pseudoscalar decay can exhibit angular anisotropy.
crosslinks:
  near_synonyms: []
  antonyms: [SCALAR_PARTICLE]
  prerequisites: [TEMPORAL_PRESSURE]
  downstream_effects: [LEPTONIC_ANOMALY]
license: CC-BY-SA-4.0
---

# Pseudoscalar

## Canonical (Pirouette)
A quantum excitation with spin J=0 and odd parity (P=-1), specifically transforming non-trivially under temporal inversion (`t → -t`). In the Pirouette Framework, the Pressuron (Γ) is a pseudoscalar, mediating coherence stress through a derivative coupling to matter that scales with fermion mass. This identity dictates its decay kinematics, primarily into lepton pairs (`e⁺e⁻`), and provides a falsifiable signature for temporal-pressure phenomena.

## EFT-First Summary
In Effective Field Theory (EFT), the Pirouette Framework's pseudoscalar Pressuron is best understood as an **Axion-Like Particle (ALP)**. It is a light (~17 MeV), neutral, CP-odd particle that couples derivatively to Standard Model fermions. Its unique feature is a coupling `g_Γ` that scales with the fermion mass `m_ℓ`, offering a natural explanation for mass-dependent lepton anomalies.

## Glossary Links
- See also: Pressuron, Temporal Pressure, Leptonic Anomaly