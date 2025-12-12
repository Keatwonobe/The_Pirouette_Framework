---
term: "Ki-Lock Test"
canonical_id: "KI_LOCK_TEST"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-073"]
---

---
term: Ki-Lock Test
canonical_id: KI_LOCK_TEST
symbol: 
aliases: []
parents: [DOMA-073]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-073
      snippet: |
        The definitive confirmation is not just finding a signal, but verifying its identity. A true detection of the cosmic heartbeat must exhibit amplitude ratios and harmonic content that are geometrically locked to the framework's fundamental Ki constants. This unique signature—the framework's mathematical fingerprint—would distinguish it from any other known astrophysical phenomenon.
  editors: [system]
  review_log: []
triad:
  art: |
    To hear the cosmos sing its own name, verifying the notes we first learned from a single electron. This test is the act of listening for that specific, scale-invariant melody.
  law: |
    A candidate cosmological signal is confirmed as the Primordial Resonance if and only if its harmonic power spectrum exhibits amplitude ratios precisely matching the geometric progression of a fundamental Ki constant (e.g., Aₙ₊₁/Aₙ = κᵢ).
  philosophy: |
    This test is the ultimate arbiter of universality for the framework's constants. It asks whether the principles derived in the lab are mere local parameters or the genuine, scale-invariant grammar of reality.
pirouette_definition: |
  A definitive validation protocol applied to a candidate signal, such as the Primordial Gamma Oscillation detected in Pulsar Timing Array data, to confirm its origin as a Pirouette-framework phenomenon. The test requires that the signal's harmonic content, specifically the amplitude ratios between its frequency sidebands, must conform to the geometric series defined by one of the framework's fundamental Ki constants. A positive result (a "Ki-Lock") provides unambiguous identification and distinguishes the signal from all other known astrophysical or instrumental sources.
operational_definition:
  units: Dimensionless (significance, e.g., σ)
  symbol_table:
    - name: Aₙ
      meaning: Amplitude of the nth harmonic of the candidate signal
      dimensions: Context-dependent (e.g., seconds for timing residuals)
      default_range: contextual
    - name: κᵢ
      meaning: A fundamental Ki constant from the Pirouette Lagrangian (CORE-006)
      dimensions: dimensionless
      default_range: [0, 1]
    - name: ω_c
      meaning: Fundamental frequency of the candidate signal
      dimensions: T⁻¹
      default_range: contextual
  measurement:
    procedures:
      - name: Harmonic Amplitude Ratio Analysis
        outline: |
          1. Acquire a high-S/N time-series dataset of a candidate signal (e.g., cleaned PTA timing residuals).
          2. Perform a Fourier transform to generate a power spectrum of the signal.
          3. Identify the fundamental frequency (ω_c) and measure the amplitude (Aₙ) of it and its integer harmonics (nω_c).
          4. Calculate the amplitude ratios Rₙ = Aₙ₊₁/Aₙ for all detected harmonics.
          5. Test the null hypothesis that the set of ratios {Rₙ} is not statistically consistent with a constant value equal to a known Ki constant (κᵢ). A rejection of the null hypothesis at >5σ constitutes a Ki-Lock.
        expected_signals: [A set of narrow-band spectral lines at frequencies nω_c with amplitudes Aₙ ∝ (κᵢ)ⁿ for some fundamental constant κᵢ.]
        pitfalls: [Contamination from astrophysical red noise processes mimicking harmonic structure; aliasing effects from irregular observation cadence; misidentification of instrumental or solar system ephemeris artifacts as a cosmological signal.]
context_windows:
  - module: DOMA-073
    excerpt: |
      The Fingerprint: The Ki-Lock Test. The definitive confirmation is not just finding a signal, but verifying its identity. A true detection of the cosmic heartbeat must exhibit amplitude ratios and harmonic content that are geometrically locked to the framework's fundamental Ki constants. This unique signature—the framework's mathematical fingerprint—would distinguish it from any other known astrophysical phenomenon.
  - module: DOMA-073
    excerpt: |
      The quantum and the cosmic are not two different realms; they are two verses of the same song, written with the same notes. To hear this cosmic heartbeat in the steady ticking of the pulsars is to receive the ultimate confirmation: the framework is not a map we have drawn, but a song the universe has been singing all along.
poetic_connections:
  motifs: [fingerprint, cosmic heartbeat, resonance, universal song, scale-invariance]
  evocative_lines:
    - "We sought to test our laws against the heavens and found ourselves taking the pulse of the universe."
    - "The framework is not a map we have drawn, but a song the universe has been singing all along."
  association_matrix:
    - [ "KI_CONSTANTS", 0.9 ]
    - [ "PRIMORDIAL_GAMMA_OSCILLATION", 0.8 ]
    - [ "COSMOLOGICAL_VALIDATION", 0.7 ]
    - [ "SCALE_INVARIANCE", 0.6 ]
formal_mappings:
  candidates:
    - target: Branching Ratio Confirmation
      domain: SM
      mapping_kind: conceptual
      equation_hint: |
        Γ(H→γγ) / Γ(H→ZZ*) vs. A₂/A₁
      justification: |
        In particle physics, the ratios of decay rates (branching ratios) of a particle like the Higgs boson into different final states are a key fingerprint that confirms its identity within the Standard Model. Similarly, the Ki-Lock Test uses the amplitude ratios of a signal's harmonics as a definitive, model-specific fingerprint to confirm its identity.
      references: []
      confidence: 0.7
    - target: Spectroscopic Overtone Analysis
      domain: AMO
      mapping_kind: operational
      justification: |
        The procedure is analogous to identifying a molecule by its unique absorption or emission spectrum. The fundamental frequency is the base tone, and the Ki-locked harmonics are the specific set of overtones whose relative strengths are a unique chemical signature.
      references: []
      confidence: 0.6
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "Any genuine signal from the Primordial Gamma Oscillation must exhibit a Ki-Lock signature in its power spectrum."
      domain: phenomenology
      falsifier: "The detection of a statistically significant, common-spectrum periodic signal in Pulsar Timing Arrays that otherwise matches the predictions for the Primordial Gamma Oscillation but whose harmonic amplitude ratios are statistically inconsistent with any of the framework's Ki constants."
      status: proposed
      links: [DOMA-073]
naming_notes:
  collisions: []
  disambiguation: |
    The term "Lock" is metaphorical, referring to the mathematical relationship between the signal's harmonics and the Ki constants. It does not imply a physical locking mechanism or a phase-locked loop in the signal processing sense.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [KI_CONSTANTS]
  downstream_effects: [COSMOLOGICAL_VALIDATION]
license: CC-BY-SA-4.0