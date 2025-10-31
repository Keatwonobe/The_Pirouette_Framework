---
term: "Reduced Planck scale"
canonical_id: "REDUCED_PLANCK_SCALE"
symbol: "M_*"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-GW-QUANTA-001"]
---

---
term: Reduced Planck scale
canonical_id: REDUCED_PLANCK_SCALE
symbol: M_*
aliases: [emergent planck mass]
parents: [MATH-GW-QUANTA-001, SUBST-001]
children: [XXP-GR-EXP, DYNA-BH-INT-001]
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-GW-QUANTA-001
      lines: "§2"
      snippet: |
        Define the reduced Planck scale M_* by the emergent constitutive law of SUBST-001...
        Canonical field:
        - v_{ij} ≡ (M_*/2) h_{ij}^{TT}  ⇒  S_2 = 1/2 ∫ d^4x [ (∂_t v_{ij})^2 − (∇ v_{ij})^2 ] .
  editors: [auto-agent-alpha]
  review_log: []
triad:
  art: |
    The energy scale that calibrates the stiffness of spacetime; it sets the volume of gravity's whisper against the hum of the temporal medium.
  law: |
    The Reduced Planck scale, M_*, is the unique mass-energy scale that canonically normalizes the kinetic term for transverse-traceless (TT) metric perturbations. It defines the transformation `v_{ij} = (M_*/2) h_{ij}^{TT}` that renders the graviton action quadratic, from which all gravitational coupling strengths (`~1/M_*`) are derived.
  philosophy: |
    Demotes the Planck scale from a fundamental constant to an emergent, collective property of the temporal medium, akin to the stiffness of a solid. It is the scale at which the description of spacetime as a smooth elastic medium breaks down, revealing the underlying substrate dynamics.
pirouette_definition: |
  The Reduced Planck scale, M_*, is the emergent energy scale that governs the strength of gravitational interactions. Operationally, it is the constant of proportionality required to transform the dimensionless metric perturbation, `h_{ij}^{TT}`, into a canonically normalized tensor field, `v_{ij}`, whose quadratic action describes two free, massless spin-2 particles. This normalization sets the coupling strength of gravitons to matter (`1/M_*`) and to themselves (`1/M_*`). The value of M_* is not fundamental, but is determined by the integrated constitutive properties of the temporal medium as defined in SUBST-001.
operational_definition:
  units: Energy (GeV)
  symbol_table:
    - name: M_*
      meaning: Reduced Planck scale
      dimensions: M L^2 T^-2
      default_range: ~2.435 x 10^18 GeV
    - name: h_{ij}^{TT}
      meaning: Transverse-traceless metric perturbation
      dimensions: dimensionless
      default_range: contextual (e.g., 10^-21 for astrophysical GWs)
    - name: v_{ij}
      meaning: Canonically normalized graviton field
      dimensions: M L^2 T^-2 (Energy)
      default_range: contextual
    - name: T_{ij}
      meaning: Stress-energy tensor
      dimensions: M L^-1 T^-2 (Energy Density)
      default_range: contextual
  measurement:
    procedures:
      - name: Gravitational Force Measurement
        outline: |
          Measure the static gravitational force between two known masses at a known distance (e.g., via torsion balance). Relate the measured force to Newton's constant G, and use the defining relation `M_*^2 = (8πG)^-1` to infer M_*.
        expected_signals: [Macroscopic force proportional to `m1*m2/r^2`]
        pitfalls: [Systematic errors in mass and distance measurement, shielding from non-gravitational forces]
      - name: Gravitational Wave Amplitude
        outline: |
          Measure the strain `h` of a gravitational wave from a source with a well-modeled luminosity (e.g., a "standard siren" binary merger). The observed amplitude `h` at a given distance is inversely proportional to `M_*`, allowing its inference.
        expected_signals: [Oscillatory spacetime strain `h(t)` in a GW detector]
        pitfalls: [Uncertainty in source luminosity distance, instrumental calibration error]
context_windows:
  - module: MATH-GW-QUANTA-001
    excerpt: |
      Define the reduced Planck scale M_* by the emergent constitutive law of SUBST-001 and write the quadratic action. The canonical field is defined as v_{ij} ≡ (M_*/2) h_{ij}^{TT}, which results in the standard kinetic term S_2 = 1/2 ∫ d^4x [ (∂_t v_{ij})^2 − (∇ v_{ij})^2 ]. This normalization is the operational basis for M_*.
  - module: MATH-GW-QUANTA-001
    excerpt: |
      The free propagator in momentum space scales as ⟨ h h ⟩ ~ 2/M_*^2. Self-interactions are also suppressed by this scale, with the cubic vertex L_3 = (1/M_*) h ∂h ∂h. Tree-level GR amplitudes are recovered in the IR, while substrate-specific deviations are suppressed by extra M_* powers.
poetic_connections:
  motifs: [stiffness, substrate, emergence, coupling, scale]
  evocative_lines:
    - "The graviton is the medium’s cleanest whisper: a transverse shiver of the loom."
  association_matrix:
    - [ "TEMPORAL_MEDIUM", 0.9 ]
    - [ "GRAVITON", 0.8 ]
    - [ "BARRIER_FREQUENCY", 0.7 ]
    - [ "COHERENCE_PRESERVING_MANIFOLD", 0.6 ]
formal_mappings:
  candidates:
    - target: Reduced Planck mass, M_Pl = (8πG_N)^(-1/2)
      domain: GR
      mapping_kind: operational
      equation_hint: |
        L_int = - (1/2) h_{ij}^{TT} T_{ij}^{TT} = - (1/M_*) v_{ij} T_{ij}^{TT}
      justification: |
        M_* plays the identical operational role as the reduced Planck mass in General Relativity and Quantum Field Theory. It sets the scale of the gravitational coupling constant, with interaction strengths for both matter-coupling and graviton self-interaction being suppressed by powers of 1/M_*. This identification is exact in the infrared limit (E << ω_c).
      references:
        - title: Quantum Field Theory in a Nutshell
          where: Part V, Chapter 5 (Effective Field Theory)
          date: 2003-09-14
      confidence: 1.0
  adopted:
    - target: Reduced Planck mass, M_Pl = (8πG_N)^(-1/2)
      rationale: The term is functionally identical to the standard model's reduced Planck mass; adopting this mapping provides a direct bridge to established gravitational phenomenology and experimental constraints.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "M_* is a constant energy scale, independent of the energy of interacting particles, in the infrared limit (E << ω_c)."
      domain: phenomenology
      falsifier: "Observation of energy-dependent gravitational coupling ('running of G') at low energies not accounted for by standard QFT loop corrections. For example, if gravitational scattering cross-sections scale differently than `E^2/M_*^4`."
      status: supported
      links: [XXP-GR-EXP]
    - statement: "The value of M_* is determined by the constitutive properties of the temporal medium and is not a fundamental constant of nature."
      domain: theory
      falsifier: "Failure of SUBST-001 to provide a mechanism to compute M_* from more fundamental parameters, or a definitive proof from a verified theory of quantum gravity that the Planck scale must be fundamental."
      status: proposed
      links: [SUBST-001]
naming_notes:
  collisions: [Planck Mass M_P = G_N^(-1/2). Note that M_* = M_P / sqrt(8π).]
  disambiguation: |
    This entry refers to the *reduced* Planck scale, which is the conventional scale for field theory normalizations where coupling constants appear in the denominator of interaction Lagrangians. It differs from the Planck Mass (derived directly from G) by a factor of `sqrt(8π)`. Pirouette exclusively uses M_* as the fundamental gravitational scale.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [TEMPORAL_MEDIUM]
  downstream_effects: [GRAVITON, GRAVITATIONAL_WAVE_DISPERSION]
license: CC-BY-SA-4.0
---

# Reduced Planck scale

## Canonical (Pirouette)
The Reduced Planck scale, M_*, is the emergent energy scale that governs the strength of gravitational interactions. Operationally, it is the constant of proportionality required to transform the dimensionless metric perturbation, `h_{ij}^{TT}`, into a canonically normalized tensor field, `v_{ij}`, whose quadratic action describes two free, massless spin-2 particles. This normalization sets the coupling strength of gravitons to matter (`1/M_*`) and to themselves (`1/M_*`). The value of M_* is not fundamental, but is determined by the integrated constitutive properties of the temporal medium as defined in SUBST-001.

## EFT-First Summary
The Reduced Planck Scale M_* is operationally identical to the standard Reduced Planck Mass (approx. 2.435 x 10^18 GeV) used in effective field theories of gravity. It is the mass scale that suppresses gravitational interactions, appearing as `1/M_*` in coupling terms between gravitons and matter, and `1/M_*` in graviton self-interaction vertices. In Pirouette, this scale is not fundamental but emerges from the physics of the temporal medium, analogous to how material stiffness emerges from atomic bonds.

## Glossary Links
- See also: Graviton, Temporal Medium, Barrier Frequency