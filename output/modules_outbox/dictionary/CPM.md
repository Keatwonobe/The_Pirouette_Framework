---
term: "CPM"
canonical_id: "CPM"
symbol: ""
aliases: [Constraint Preservation Machine]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-BH-INT-001"]
---

---
term: CPM
canonical_id: CPM
symbol: N/A
aliases: [Constraint Preservation Machine]
parents: [DYNA-BH-INT-001, SUBST-001]
children: [XXP-GR-EXP]
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DYNA-BH-INT-001
      lines: "§1, §7"
      snippet: |
        **Interior**: medium with fields \( \Gamma(r),\, Ki(\cdot) \) in a new phase; **no extra graviton polarizations** allowed anywhere (CPM).
  editors: [GPT-4 (Pirouette Agent)]
  review_log:
    - {date: 2025-10-18, reviewer: GPT-4 (Pirouette Agent), notes: Initial draft from seed.}
triad:
  art: |
    Gravity speaks with only two voices—a transverse whisper. The Machine ensures no third voice can ever join the chorus, preserving the spacetime medium's fundamental grammar.
  law: |
    Any validated detection of gravitational wave (GW) polarizations other than the two transverse-traceless (TT) tensor modes in any regime falsifies the CPM. All physical models within the framework must propagate only TT modes at all energy scales.
  philosophy: |
    CPM enforces single-metric universality and the Equivalence Principle at the level of propagating degrees of freedom. It acts as a powerful Occam's Razor, forbidding a proliferation of new gravitational fields and ensuring that modifications to GR are confined to the constitutive laws of the temporal medium, not its fundamental symmetries.
pirouette_definition: |
  A fundamental rule stating that the gravitational field, as an excitation of the temporal medium, possesses only two propagating degrees of freedom, corresponding to the transverse-traceless (TT) tensor polarizations of General Relativity. The CPM forbids the emergence of any additional (e.g., scalar, vector) gravitational polarizations from any physical process or in any medium, including the high-density cores of black holes. This constraint is a direct consequence of the Substrate Charter's principles of gauge structure (SR-2/3) and single-metric universality (SR-5).
operational_definition:
  units: Dimensionless (rule)
  symbol_table:
    - name: h+, h×
      meaning: Amplitudes of the two allowed transverse-traceless (tensor) GW polarizations.
      dimensions: dimensionless (strain)
      default_range: 10⁻²³ – 10⁻²⁰ (typical for detection)
    - name: h_S, h_V
      meaning: Amplitudes of hypothetical scalar (breathing, longitudinal) or vector (shear) GW polarizations.
      dimensions: dimensionless (strain)
      default_range: 0 (by CPM)
  measurement:
    procedures:
      - name: Multi-Detector Polarization Analysis
        outline: |
          Correlate signals from a network of at least three non-collinear gravitational wave detectors (e.g., LIGO-Virgo-KAGRA-IndiGO). Reconstruct the full strain tensor and attempt to fit the data to a model including scalar and vector modes in addition to the standard tensor modes. A null result for non-tensor modes supports CPM.
        expected_signals: [A statistically significant non-zero amplitude for any polarization mode other than the two TT modes would be a falsifying signal.]
        pitfalls: [Detector calibration errors mimicking non-TT signals, incomplete sky localization leading to polarization ambiguity, noise mischaracterization.]
context_windows:
  - module: DYNA-BH-INT-001
    excerpt: |
      **Interior**: medium with fields \( \Gamma(r),\, Ki(\cdot) \) in a new phase; **no extra graviton polarizations** allowed anywhere (CPM).
      **Barrier finiteness**: curvature growth saturates at \( \omega_c \) (prevents singularities).
      Both minimal phases (Γ-Saturated and Vortex-Foam) are compatible with CPM & barrier finiteness.
  - module: DYNA-BH-INT-001
    excerpt: |
      **Falsifiable Signatures (to XXP-GR-EXP)**
      1) **No new GW polarizations** anywhere (hard falsifier; breaks SR-2/3).
      [...]
      5) **Tidal Love**: effectively zero at leading order; detection of large static Love numbers falsifies CPM-respecting interiors.
poetic_connections:
  motifs: [universality, grammar of spacetime, gauge purity, two-voice gravity, constraint]
  evocative_lines:
    - "The graviton counts its threads as a barely-audible delay."
    - "The singularity is replaced by a phase—a yolk of time under pressure."
  association_matrix:
    - [ "SINGLE_METRIC_UNIVERSALITY", 0.9 ]
    - [ "EQUIVALENCE_PRINCIPLE", 0.8 ]
    - [ "SUBSTRATE_CHARTER", 0.7 ]
formal_mappings:
  candidates:
    - target: Constraint against scalar-tensor theories
      domain: Modified Gravity
      mapping_kind: operational
      equation_hint: |
        e.g., in Brans-Dicke, S ∝ ∫d⁴x [φR - (ω/φ)(∂φ)²]. CPM rules out the dynamical φ as a propagating GW field.
      justification: |
        Scalar-tensor theories generically predict a scalar gravitational wave polarization. CPM functions as an *a priori* exclusion of such theories, making any experimental search for scalar modes a direct test of a foundational Pirouette principle.
      references:
        - title: The Confrontation between General Relativity and Experiment
          where: Living Rev. Relativ. 15, 5 (2012)
          date: 2012-01-01
      confidence: 0.95
  adopted:
    - target: The exclusion of non-tensor modes in General Relativity's propagating vacuum solutions.
      rationale: In standard GR, the linearized field equations in vacuum yield only two propagating TT modes. CPM elevates this result from a consequence of a specific Lagrangian to a fundamental principle applicable even within non-vacuum, modified-gravity interiors, acting as a powerful selection rule.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "The gravitational wave field has exactly two propagating polarizations."
      domain: experiment
      falsifier: "Detection of a statistically significant signal component in a non-TT polarization channel (e.g., scalar/breathing mode) by a GW detector network."
      status: supported
      links: [DYNA-BH-INT-001, XXP-GR-EXP]
    - statement: "The static tidal Love numbers of black holes are effectively zero."
      domain: phenomenology
      falsifier: "Measurement of a non-zero static tidal Love number for a black hole binary inspiral, which would imply the existence of a new field (often scalar) that mediates the tidal force, violating CPM."
      status: supported
      links: [DYNA-BH-INT-001]
naming_notes:
  collisions: [Critical Path Method (project management), Continuous Passive Motion (medicine)]
  disambiguation: |
    The term "Machine" is metaphorical, implying an active, background process or fundamental law of the temporal medium that actively "preserves" the gauge constraint. It is not an engineered device, but a rule that enforces itself, distinguishing it from an accidental feature of a low-energy limit.
crosslinks:
  near_synonyms: [SINGLE_METRIC_UNIVERSALITY]
  antonyms: [SCALAR_TENSOR_GRAVITY]
  prerequisites: [SUBSTRATE_CHARTER]
  downstream_effects: [TT_PHONON, ZERO_LOVE_NUMBER]
license: CC-BY-SA-4.0
---

# CPM

## Canonical (Pirouette)
A fundamental rule stating that the gravitational field, as an excitation of the temporal medium, possesses only two propagating degrees of freedom, corresponding to the transverse-traceless (TT) tensor polarizations of General Relativity. The CPM forbids the emergence of any additional (e.g., scalar, vector) gravitational polarizations from any physical process or in any medium, including the high-density cores of black holes. This constraint is a direct consequence of the Substrate Charter's principles of gauge structure (SR-2/3) and single-metric universality (SR-5).

## EFT-First Summary
The CPM is a strong prior that selects for theories of gravity that are dynamically equivalent to General Relativity in their propagating degrees of freedom. It explicitly forbids theories with additional propagating fields, such as the scalar field in Brans-Dicke gravity or other scalar-tensor theories, which would manifest as additional gravitational wave polarizations. This makes any observational constraints on non-tensor GW modes from sources like LIGO/Virgo/KAGRA a direct and stringent test of this core Pirouette assumption.

## Glossary Links
- See also: SINGLE_METRIC_UNIVERSALITY, EQUIVALENCE_PRINCIPLE, SUBSTRATE_CHARTER