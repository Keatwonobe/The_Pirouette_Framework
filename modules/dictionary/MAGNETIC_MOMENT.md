---
term: "Magnetic Moment"
canonical_id: "MAGNETIC_MOMENT"
symbol: "µ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-002"]
---

---
term: Magnetic Moment
canonical_id: MAGNETIC_MOMENT
symbol: µ
aliases: [Magnetic Dipole Moment]
parents: [MATH-002, CORE-009]
children: [XXP-001]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-002
      lines: "§4"
      snippet: |
        The Doubling Effect: The magnetic moment mu is a measure of the energy change per unit of magnetic field, which is coupled to the full 720° cycle of the resonance. However, the spin angular momentum S is conventionally defined by the physics of a 360° rotation. When we calculate the ratio, we are comparing a phenomenon (mu) that operates on a 720° cycle to a definition (S) that operates on a 360° cycle.
  editors: [system_agent]
  review_log: []
triad:
  art: |
    The echo of a two-step dance. A particle’s magnetic moment is the shadow cast by its full 720° pirouette, not just the half-turn we see.
  law: |
    A particle's magnetic moment (µ) is proportional to its spin angular momentum (S), with a gyromagnetic ratio (g) of exactly 2. This factor of 2 is a geometric constant arising from the ratio of the resonance's 720° topological path to the 360° rotational period used to define S.
  philosophy: |
    The magnetic moment's anomalous strength (g=2) is not a quantum mystery but a geometric inevitability. It is the conversion factor between a system that lives in a 720° world and our 360° definitions of its properties, proving that fundamental constants can emerge from topology.
pirouette_definition: |
  A measure of the interaction energy between a particle's spin and an external magnetic field. The magnetic moment's magnitude is intrinsically coupled to the full 720° topological cycle of the particle's underlying resonance. Because its associated spin angular momentum (S) is conventionally measured over a 360° rotation, the magnetic moment is geometrically doubled relative to S, yielding a baseline gyromagnetic ratio of g=2.
operational_definition:
  units: Joules per Tesla (J·T⁻¹) or Ampere-meters squared (A·m²)
  symbol_table:
    - name: µ
      meaning: Magnetic Moment vector
      dimensions: M L² T⁻² / (M T⁻² I⁻¹) = I L²
      default_range: For an electron, ~9.28 × 10⁻²⁴ J·T⁻¹
    - name: g
      meaning: Gyromagnetic ratio (g-factor)
      dimensions: dimensionless
      default_range: ~2.0023 for an electron; derived as exactly 2 from base topology.
    - name: S
      meaning: Spin Angular Momentum vector
      dimensions: M L² T⁻¹
      default_range: For a spin-1/2 particle, eigenvalues are ±ħ/2.
  measurement:
    procedures:
      - name: Electron Spin Resonance (ESR) Spectroscopy
        outline: |
          1. Place a sample of particles in a strong, uniform magnetic field (B).
          2. The magnetic field splits the particle's spin energy levels (Zeeman effect).
          3. Irradiate the sample with microwave-frequency photons.
          4. At a specific resonant frequency, photons are absorbed, exciting transitions between spin states.
          5. The energy of the absorbed photons (ΔE) is directly proportional to the magnetic moment: ΔE = g * µ_B * B, where µ_B is the Bohr magneton. This allows for precise measurement of g, and thus µ.
        expected_signals: [Sharp absorption peak at the resonant microwave frequency.]
        pitfalls: [Line broadening due to field inhomogeneity, thermal motion, or spin-spin interactions.]
context_windows:
  # Short, trimmed context quotes harvested from modules (3–6 sentences each).
  - module: MATH-002
    excerpt: |
      The Doubling Effect: The magnetic moment µ is a measure of the energy change per unit of magnetic field, which is coupled to the full 720° cycle of the resonance. However, the spin angular momentum S is conventionally defined by the physics of a 360° rotation. When we calculate the ratio, we are comparing a phenomenon (µ) that operates on a 720° cycle to a definition (S) that operates on a 360° cycle. The magnetic moment is effectively twice as large as it "should" be for a given amount of angular momentum.
  - module: MATH-002
    excerpt: |
      For an electron, we posit a "Möbius-like" path: P(theta) = exp(i*theta/2). At theta = 360 degrees (2*pi): P(2*pi) = exp(i*pi) = -1. The particle has rotated 360° but is now in the opposite phase. At theta = 720 degrees (4*pi): P(4*pi) = exp(i*2*pi) = 1. The particle has returned to its original state only after two full rotations. This mathematical form perfectly models the behavior of a spin-1/2 particle.
poetic_connections:
  # Lightweight "word-association graph" and sticky lines.
  motifs: [resonance, echo, topology, two-cycle, möbius path, geometric doubling]
  evocative_lines:
    - "The electron's spin is a twist in time."
    - "It is the description of the dance itself."
    - "The echo of that resonance."
  association_matrix:
    # symmetric or directed; weights in [0,1]
    - [ "SPIN_ANGULAR_MOMENTUM", 0.9 ]
    - [ "G_FACTOR", 0.9 ]
    - [ "RESONANCE", 0.7 ]
    - [ "TOPOLOGY", 0.6 ]
formal_mappings:
  # Candidate alignments to EFT/SM/CM/GR terms, each with justification and refs.
  candidates:
    []
  adopted:
    - target: Electron magnetic dipole moment (µ_e)
      domain: SM/QED
      mapping_kind: operational
      equation_hint: |
        µ_e = -g_e (µ_B / ħ) S
      rationale: |
        The Pirouette µ for an electron is definitionally and operationally identical to the Standard Model electron magnetic moment. The Pirouette framework provides a novel *ab initio* derivation for the Dirac equation's prediction of g=2, attributing it to the resonance's 720° topology rather than relativistic quantum mechanics.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The baseline gyromagnetic ratio (g) for a fundamental spin-1/2 particle is exactly 2, arising as a geometric factor from its 720° resonance topology, prior to any radiative corrections."
      domain: theory
      falsifier: "The discovery of a fundamental spin-1/2 lepton whose baseline g-factor is significantly different from 2, or experimental evidence that its quantum phase is not described by a 720° (SU(2)) symmetry."
      status: supported
      links: [MATH-002]
naming_notes:
  collisions: [The symbol µ is commonly used for the muon particle and for magnetic permeability.]
  disambiguation: |
    When appearing in equations with spin (S) or a magnetic field (B), µ refers to the magnetic moment. In particle physics contexts, the muon is typically written with its charge, µ⁻ or µ⁺. Magnetic permeability is a property of a medium, not a particle.
crosslinks:
  near_synonyms: []
  antonyms: [ELECTRIC_DIPOLE_MOMENT]
  prerequisites: [SPIN_ANGULAR_MOMENTUM, G_FACTOR, COHERENCE_FIELD]
  downstream_effects: [ZEEMAN_EFFECT]
license: CC-BY-SA-4.0
---