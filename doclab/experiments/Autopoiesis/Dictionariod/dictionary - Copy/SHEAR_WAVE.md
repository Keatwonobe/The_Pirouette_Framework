---
term: "Shear Wave"
canonical_id: "SHEAR_WAVE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-QED-001_Time-Phase_Gauge_Principle"]
---

---
term: Shear Wave
canonical_id: SHEAR_WAVE
symbol: (excitation of `Aμ`)
aliases: [photon, Goldstone connection]
parents: [MATH-QED-001_Time-Phase_Gauge_Principle]
children: [MATH-QED-002, MATH-QED-003, MATH-QED-004]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-QED-001_Time-Phase_Gauge_Principle
      lines: "L10-L10"
      snippet: |
        ...photons are **shear waves of the temporal medium**.
  editors: [system]
  review_log: []
triad:
  art: |
    A ripple on the ocean of time, sent to ensure every local clock's tick remains honest with its neighbors. The Shear Wave is the messenger that enforces temporal coherence across spacetime.
  law: |
    A transverse wave whose dynamics are governed by the Maxwell action `L = -¼ FμνFμν`. It propagates without dispersion at the luminal speed `c` on the Coherence-Preserving Manifold, a property enforced by the high-gradient (`high-X`) limit of the temporal medium's kinetic term.
  philosophy: |
    The Shear Wave reframes the photon not as a fundamental force carrier but as a dynamic consequence of a deeper principle: local time-phase invariance. Its existence is mandated to preserve coherence in a substrate where every point in spacetime has the freedom to redefine its own "now".
pirouette_definition: |
  The physical manifestation of the photon as a propagating transverse disturbance in the temporal medium. The Shear Wave is the excitation of the Goldstone connection field (`Aμ`) required to maintain physical invariance under local relabeling of the clock-phase field (`θ(x)`). Its dynamics emerge from a "stiffness" penalty (`-¼ FμνFμν`) against gradients in the local clock calibration, ensuring luminal, nondispersive propagation.
operational_definition:
  units: The associated potential field `Aμ` has units of `Energy/Charge` (or `Mass` in natural units).
  symbol_table:
    - name: `Aμ`
      meaning: The connection field potential whose excitations are Shear Waves.
      dimensions: `M L T⁻¹ Q⁻¹`
      default_range: contextual
    - name: `Fμν`
      meaning: The field strength tensor, representing the curvature of the connection.
      dimensions: `M T⁻¹ Q⁻¹`
      default_range: contextual
    - name: `P(X,ρ)`
      meaning: Kinetic term of the temporal medium Lagrangian.
      dimensions: `M L⁻¹ T⁻²`
      default_range: contextual
  measurement:
    procedures:
      - name: Vacuum Dispersion Search
        outline: |
          Measure the arrival times of photons with different frequencies (e.g., from a gamma-ray burst or fast radio burst) originating from the same distant cosmological source. A frequency-dependent arrival time, after correcting for known plasma effects, would indicate a non-luminal dispersion relation.
        expected_signals: [Frequency-dependent speed of light `c(ω)`]
        pitfalls: [Astrophysical source modeling errors, Interstellar medium (ISM) dispersion mischaracterization]
      - name: Vacuum Birefringence Search
        outline: |
          Measure the polarization of light from distant sources like Active Galactic Nuclei (AGN) or the Cosmic Microwave Background (CMB). A systematic rotation of the polarization plane as a function of distance or frequency would indicate vacuum birefringence.
        expected_signals: [Polarization rotation `Δψ ≠ 0`]
        pitfalls: [Faraday rotation in galactic magnetic fields]
context_windows:
  # Short, trimmed context quotes harvested from modules (3–6 sentences each).
  - module: MATH-QED-001_Time-Phase_Gauge_Principle
    excerpt: |
      Show that **QED’s U(1) gauge symmetry** is not an axiomatic input but the **local relabeling freedom** of the temporal clock phase in Pirouette’s time-first substrate. The necessity of a compensating connection produces a Maxwell term; photons are **shear waves of the temporal medium**.
  - module: MATH-QED-001_Time-Phase_Gauge_Principle
    excerpt: |
      When spatial/temporal gradients of the local clock calibration are costly, the effective action acquires a curvature penalty for the connection: `L_EM = -¼ FμνFμν`. This arises either from integrating out short-scale fluctuations of `θ` or as the leading operator allowed by Lorentz and gauge invariance. On the Coherence-Preserving Manifold, the high-`X` form of `P` enforces nondispersive shear propagation, fixing the observed luminal speed `c`.
poetic_connections:
  # Lightweight "word-association graph" and sticky lines.
  motifs: [temporal ocean, connection stiffness, coherence, local clock]
  evocative_lines:
    - "a shear wave that carries the memo from one tick of time to the next."
    - "photons are shear waves of the temporal medium."
  association_matrix:
    # symmetric or directed; weights in [0,1]
    - [ "U(1)_GAUGE_SYMMETRY", 0.9 ]
    - [ "TEMPORAL_MEDIUM", 0.8 ]
    - [ "COHERENCE_PRESERVING_MANIFOLD", 0.7 ]
    - [ "MINIMAL_COUPLING", 0.5 ]
formal_mappings:
  # Candidate alignments to EFT/SM/CM/GR terms, each with justification and refs.
  candidates: []
  adopted:
    - target: Photon (U(1) gauge boson of QED/Standard Model)
      rationale: |
        The Shear Wave is a massless, spin-1 vector excitation whose dynamics are described by the Maxwell Lagrangian, which is derived from the principle of local time-phase invariance. It couples to a conserved Noether current associated with this U(1) symmetry. This is a one-to-one emergent reconstruction of the QED photon.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "Shear waves (photons) propagate in a vacuum without dispersion or birefringence."
      domain: experiment
      falsifier: "Observation of a frequency-dependent vacuum speed of light or vacuum polarization rotation beyond current experimental bounds (e.g., from CTA, Fermi-LAT, or CMB polarization studies)."
      status: supported
      links: [MATH-QED-001_Time-Phase_Gauge_Principle]
    - statement: "The Maxwell action `-¼ FμνFμν` is the complete low-energy description of Shear Wave dynamics."
      domain: phenomenology
      falsifier: "Discovery of anomalous long-range forces or photon self-interactions not accounted for by QED loops, implying additional massless modes or operators beyond the F² term."
      status: supported
      links: []
naming_notes:
  collisions: [shear wave (condensed matter)]
  disambiguation: |
    In condensed matter physics, a "shear wave" is a transverse mechanical wave propagating through an elastic solid medium. Pirouette's use is a direct analogy: it is a transverse wave, but it propagates through the temporal medium, not a spatial, elastic one. The "shear" refers to the disturbance of the clock-phase gradient field.
crosslinks:
  near_synonyms: [PHOTON]
  antonyms: [TEMPORAL_PRESSURE]
  prerequisites: [TEMPORAL_MEDIUM, TIME_PHASE_GAUGE_PRINCIPLE]
  downstream_effects: [MINIMAL_COUPLING, FINE_STRUCTURE_CONSTANT, DIRAC_OPERATOR]
license: CC-BY-SA-4.0
---

# Shear Wave

## Canonical (Pirouette)
The physical manifestation of the photon as a propagating transverse disturbance in the temporal medium. The Shear Wave is the excitation of the Goldstone connection field (`Aμ`) required to maintain physical invariance under local relabeling of the clock-phase field (`θ(x)`). Its dynamics emerge from a "stiffness" penalty (`-¼ FμνFμν`) against gradients in the local clock calibration, ensuring luminal, nondispersive propagation.

## EFT-First Summary
The Shear Wave is the Pirouette framework's emergent realization of the **QED photon**. It is identified as the massless U(1) gauge boson whose dynamics are governed by the Maxwell Lagrangian. This structure is not postulated but derived from the requirement of local phase invariance for a scalar "clock" field that constitutes the temporal substrate. The theory predicts that any observed deviation from the Maxwell action, such as vacuum dispersion, would falsify the model's low-energy limit.

## Glossary Links
- See also: [Temporal Medium](<link>), [Time-Phase Gauge Principle](<link>), [Minimal Coupling](<link>)