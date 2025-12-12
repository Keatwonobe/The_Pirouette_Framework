---
term: "Vortex Lattice"
canonical_id: "VORTEX_LATTICE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["COSMO-006"]
---

---
term: Vortex Lattice
canonical_id: VORTEX_LATTICE
symbol: d_v
aliases: [Abrikosov lattice, vortex array]
parents: [COSMO-006]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: COSMO-006
      lines: "Section 3"
      snippet: |
        Critical angular velocity for first vortex: Ω_c ≈ (ħ/m_H r_c^2) ln(r_c/ξ); vortex lattice spacing d_v ∝ √(c_s/Ω).
        Observables: non‑circular flows in IFU maps; wiggles in stellar‑stream power spectra at k~1/d_v.
  editors: [Pirouette Framework AI]
  review_log: []
triad:
  art: |
    A crystal of motion, where countless quantum whirlpools arrange themselves into a silent, spinning grid. It is the superfluid's ordered response to being stirred, a hidden structure that betrays the cosmos's quantum heartbeat.
  law: |
    A superfluid rotating with an angular velocity Ω greater than a critical value Ω_c will form a regular array of quantized vortices with an inter-vortex spacing d_v that scales as 1/√Ω. On macroscopic scales, this array mimics solid-body rotation.
  philosophy: |
    The Vortex Lattice transforms a smooth, classical rotation into a discrete, quantum phenomenon on astrophysical scales. Its existence provides a falsifiable signature for the superfluid nature of dark matter, linking the largest structures in the universe to the granular rules of quantum mechanics.
pirouette_definition: |
  A regular, two-dimensional array of quantized vortices that forms in a rotating superfluid halo when the angular velocity Ω exceeds a critical threshold Ω_c. Each vortex carries a quantized circulation Γ = 2πħ/m_H. The lattice spacing d_v is determined by Ω and the fluid's sound speed c_s, and the entire array co-rotates with the bulk fluid, mimicking solid-body rotation on average.
operational_definition:
  units: d_v is in meters (m) or parsecs (pc).
  symbol_table:
    - name: d_v
      meaning: Inter-vortex spacing in the lattice
      dimensions: L
      default_range: 0.1–10 kpc
    - name: Ω
      meaning: Angular velocity of the superfluid halo
      dimensions: T⁻¹
      default_range: 10⁻¹⁶–10⁻¹⁵ rad/s
    - name: Ω_c
      meaning: Critical angular velocity for first vortex nucleation
      dimensions: T⁻¹
      default_range: contextual
    - name: c_s
      meaning: Superfluid sound speed
      dimensions: L T⁻¹
      default_range: 10–300 km/s
    - name: m_H
      meaning: Mass of the superfluid constituent particle
      dimensions: M
      default_range: 1–100 MeV/c²
  measurement:
    procedures:
      - name: Stellar Stream Power Spectrum Analysis
        outline: |
          Identify a cold stellar stream passing through a candidate superfluid halo. Measure density and/or line-of-sight velocity fluctuations along the stream. Compute the one-dimensional power spectrum of these fluctuations and search for a peak at a characteristic wavenumber k ≈ 2π/d_v.
        expected_signals: [A statistically significant peak in the power spectrum at a wavenumber consistent with the predicted d_v for the host halo's rotation.]
        pitfalls: [Confounding peaks from stream epicyclic motions or interactions with baryonic substructures, insufficient stream density leading to high shot noise.]
      - name: IFU Kinematic Mapping
        outline: |
          Use an Integral Field Unit (IFU) to map the velocity field of a tracer population (gas or stars) within a rotating halo. Subtract a smooth, axisymmetric rotation model from the observed velocity map. Analyze the residual velocity field for a regular, grid-like pattern of perturbations.
        expected_signals: [A coherent, periodic pattern of non-circular velocity residuals with a characteristic length scale matching the predicted d_v.]
        pitfalls: [Observational resolution insufficient to resolve d_v, turbulent motions or stellar feedback masking the faint vortex-induced signal.]
context_windows:
  - module: COSMO-006
    excerpt: |
      Critical angular velocity for first vortex: Ω_c ≈ (ħ/m_H r_c^2) ln(r_c/ξ); vortex lattice spacing d_v ∝ √(c_s/Ω). Observables: non‑circular flows in IFU maps; wiggles in stellar‑stream power spectra at k~1/d_v.
  - module: COSMO-006
    excerpt: |
      The solver configuration allows for direct output of the vortex configuration via the `vortex_map` key. This map can be used to generate mock observations for testing measurement procedures. Each point in the map corresponds to the quantized circulation `ℓ`.
poetic_connections:
  motifs: [crystal, lattice, whirlpool, quantum fluid, rigid rotation]
  evocative_lines:
    - "wiggles in stellar-stream power spectra"
    - "non-circular flows in IFU maps"
    - "vortex stability threshold vs. Ω"
  association_matrix:
    - [ "HALO_ANGULAR_VELOCITY", 0.9 ]
    - [ "SUPERFLUID_SOUND_SPEED", 0.7 ]
    - [ "HALO_CORE_RADIUS", 0.5 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Abrikosov lattice
      domain: AMO
      mapping_kind: conceptual
      equation_hint: |
        n_v = 2Ω / (2πħ/m)  (Vortex density vs. rotation)
      justification: |
        The concept of a vortex lattice in a rotating superfluid is a direct analogue of the lattice formed in a rotating Bose-Einstein Condensate (BEC). In both cases, a continuous external rotation is accommodated by the nucleation of a regular array of quantized topological defects (vortices) whose area density is proportional to the rotation frequency. This is the energetically favored state over smooth, viscous rotation.
      references:
        - title: Application of Quantum Mechanics to Liquid Helium
          where: Prog. Low Temp. Phys. 1, 17–53
          date: 1955-01-01
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "Rotating superfluid dark matter halos with Ω > Ω_c must contain a vortex lattice with spacing d_v ∝ 1/√Ω."
      domain: phenomenology
      falsifier: "The detection of a rotating galactic halo exhibiting other signs of superfluidity (e.g., a cored profile from quantum pressure) but a complete absence of the predicted non-circular flows or stellar stream power spectrum features, despite sufficient observational precision to rule out d_v in the predicted range."
      status: proposed
      links: [COSMO-006]
naming_notes:
  collisions: [Crystal lattice, Lattice QCD]
  disambiguation: |
    The term 'lattice' here refers to a regular spatial arrangement of dynamical defects (vortices) in a fluid, not a static grid of particles (crystal lattice) or a discretized spacetime grid for computation (Lattice QCD).
crosslinks:
  near_synonyms: []
  antonyms: [LAMINAR_FLOW]
  prerequisites: [QUANTIZED_CIRCULATION, SUPERFLUID, HALO_ANGULAR_VELOCITY]
  downstream_effects: [STELLAR_STREAM_DYNAMICS, HALO_KINEMATICS]
license: CC-BY-SA-4.0
---

# Vortex Lattice

## Canonical (Pirouette)
A regular, two-dimensional array of quantized vortices that forms in a rotating superfluid halo when the angular velocity Ω exceeds a critical threshold Ω_c. Each vortex carries a quantized circulation Γ = 2πħ/m_H. The lattice spacing d_v is determined by Ω and the fluid's sound speed c_s, and the entire array co-rotates with the bulk fluid, mimicking solid-body rotation on average.

## EFT-First Summary
In the effective field theory of a superfluid, the vortex lattice is a stable, low-energy, non-perturbative configuration of the Goldstone boson (the phase of the condensate) in a rotating frame. It represents the macroscopic state in which the system minimizes its free energy by nucleating an array of topological defects, each with a quantized winding number, whose density is proportional to the external angular velocity. This configuration is a direct analogue of the Abrikosov lattice in Ginzburg-Landau theory and rotating Bose-Einstein Condensates.

## Glossary Links
- See also: [Quantized Circulation](link-to-quantized-circulation), [Superfluid](link-to-superfluid)