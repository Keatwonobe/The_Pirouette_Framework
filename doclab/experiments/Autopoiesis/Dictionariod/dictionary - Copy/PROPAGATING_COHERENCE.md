---
term: "Propagating Coherence"
canonical_id: "PROPAGATING_COHERENCE"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-146"]
---

---
term: Propagating Coherence
canonical_id: PROPAGATING_COHERENCE
symbol: κ_p
aliases: ["Ki_motion", "Song of Interaction"]
parents: [DOMA-146, CORE-007]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-146
      snippet: |
        Propagating Coherence (The Song of Interaction): This component represents the frequencies that govern the system's interaction with the wider coherence manifold. It is the signature of The Current and the Compass (CORE-007). These are the rhythms of communication, motion, and response—the means by which the system projects itself and perceives others.
  editors: [auto-scribe]
  review_log: []
triad:
  art: |
    The song a system sings to its world. It is the voice, the hand outstretched, the signal broadcast across the void seeking a reply.
  law: |
    A system's propagating coherence is quantified by the amplitude, bandwidth, and persistence of transient, high-frequency, or broad-bandwidth resonances identified via spectral analysis, which collectively determine its capacity for environmental interaction.
  philosophy: |
    To exist is to be distinct; to live is to interact. Propagating Coherence is the principle that no system is an island, defining the necessary outward-facing aspect of being that enables communication, adaptation, and evolution within an environment.
pirouette_definition: |
  Propagating Coherence is the component of a system's total resonant signature (`Ki`) that mediates its interaction, communication, and response to the external environment. Distinguished from Structural Coherence, it manifests as rhythms that project the system's influence and process incoming signals, expressing the dynamics of The Current and the Compass (CORE-007). In Resonant Spectrum Analysis, it is identified by coherent patterns that are typically higher-frequency, broader-bandwidth, or more transient than their structural counterparts.
operational_definition:
  units: Dimensionless (relative amplitude) or units of the input signal.
  symbol_table:
    - name: κ_p
      meaning: Propagating Coherence component of a system's resonant signature.
      dimensions: Dimensionless
      default_range: contextual
  measurement:
    procedures:
      - name: Resonant Spectrum Analysis
        outline: |
          1. Ingest a time-series signature of the system's behavior.
          2. Apply a Continuous Wavelet Transform (CWT) or similar time-frequency analysis to generate a spectrogram.
          3. Identify persistent high-energy ridges (coherent `Ki` patterns).
          4. Classify ridges as Propagating based on diagnostic metrics: typically higher-frequency (ω_k), broader-bandwidth (Δω), and/or more transient (lower persistence Δt) compared to Structural modes.
        expected_signals: ["High-energy ridges in a spectrogram, often appearing as transient bursts, frequency-modulated chirps, or broad-band features."]
        pitfalls: ["Misclassifying a noisy structural mode as propagating; aliasing from improper signal sampling; confusing environmental signals (Γ) with the system's own propagation."]
context_windows:
  - module: DOMA-146
    excerpt: |
      Propagating Coherence (The Song of Interaction): This component represents the frequencies that govern the system's interaction with the wider coherence manifold. It is the signature of The Current and the Compass (CORE-007). These are the rhythms of communication, motion, and response—the means by which the system projects itself and perceives others. A rich, adaptive propagating spectrum indicates a system that is actively engaged with its environment.
  - module: DOMA-146
    excerpt: |
      Structural coherences tend to be low-frequency, narrow-bandwidth, and high-persistence, while Propagating coherences are often higher-frequency, broader-bandwidth, or more transient.
  - module: DOMA-146
    excerpt: |
      To truly know a cello, you must listen. You must learn to distinguish the deep, resonant voice of the wood itself from the clear, soaring notes that fly from its strings. One is the sound of its being; the other is the sound of its song. They are not two different things, but two expressions of a single, vibrant whole.
poetic_connections:
  motifs: ["song", "voice", "signal", "broadcast", "echo", "interaction"]
  evocative_lines:
    - "The song of interaction."
    - "...the clear, soaring notes that fly from its strings."
  association_matrix:
    - [ "STRUCTURAL_COHERENCE", -0.8 ]
    - [ "CURRENT_AND_COMPASS", 0.9 ]
    - [ "TEMPORAL_PRESSURE", 0.3 ]
    - [ "RESONANCE", 0.7 ]
formal_mappings:
  candidates:
    - target: Propagator / Green's function
      domain: QFT
      mapping_kind: conceptual
      justification: |
        The propagator in QFT describes the amplitude for a particle to travel between points, mediating interactions. Propagating Coherence similarly describes the system's capacity to project its influence and interact with its environment, effectively defining the 'field' of its influence.
      references: []
      confidence: 0.5
    - target: Phonons or other collective excitations
      domain: CM
      mapping_kind: operational
      justification: |
        In a crystal, phonons are quantized modes of vibration that propagate and carry energy/information. Propagating coherences are measured as specific vibrational modes (resonances) in a system that are responsible for its external interactions, analogous to the role of phonons versus the static lattice (cf. Structural Coherence).
      references: []
      confidence: 0.7
  adopted:
    - target: Phonons / collective interaction modes
      rationale: |
        The mapping to phonons is operationally robust. Both are identified as specific modes in a spectral analysis of a complex system's dynamics, and both are fundamentally responsible for mediating interaction and energy/information transfer with an environment, distinct from the static structure of the system itself.
      confidence: 0.7
constraints_and_falsifiers:
  claims:
    - statement: "Systems with higher measured propagating coherence amplitudes will exhibit faster and more accurate responses to external stimuli."
      domain: experiment
      falsifier: "An experiment where two systems with identical structural coherence but different propagating coherence show no statistically significant difference in reaction time or fidelity when subjected to a controlled external signal."
      status: proposed
      links: [DOMA-146]
    - statement: "The total interactive cross-section of a system is proportional to the integrated power of its propagating coherence spectrum."
      domain: theory
      falsifier: "A formal derivation or simulation shows that interactive cross-section depends non-linearly on a combination of both structural and propagating modes, or is dominated by a different factor entirely."
      status: proposed
      links: [CORE-007, DOMA-146]
naming_notes:
  collisions: ["The term 'coherence' is used broadly in physics (e.g., quantum coherence, optical coherence). Pirouette's use is specific to the persistence and purity of temporal patterns (resonances)."]
  disambiguation: |
    Distinguish from `Structural Coherence`, which governs internal stability, not external interaction. While both are components of a system's total `Ki`, Propagating Coherence is about *doing* in the world, while Structural Coherence is about *being* in the world.
crosslinks:
  near_synonyms: []
  antonyms: [STRUCTURAL_COHERENCE]
  prerequisites: [RESONANT_SPECTRUM, KI]
  downstream_effects: [PIRQUETTE_LAGRANGIAN]
license: CC-BY-SA-4.0
---

# Propagating Coherence

## Canonical (Pirouette)
Propagating Coherence is the component of a system's total resonant signature (`Ki`) that mediates its interaction, communication, and response to the external environment. Distinguished from Structural Coherence, it manifests as rhythms that project the system's influence and process incoming signals, expressing the dynamics of The Current and the Compass (CORE-007). In Resonant Spectrum Analysis, it is identified by coherent patterns that are typically higher-frequency, broader-bandwidth, or more transient than their structural counterparts.

## EFT-First Summary
In an analogy to condensed matter physics, a system's Propagating Coherence can be understood as its spectrum of collective interaction modes, akin to phonons in a crystal lattice. These modes are the 'quanta' of the system's interaction with its environment, carrying information and mediating influence. This is distinct from the static properties of the 'lattice' itself (see `Structural Coherence`). The richness and amplitude of this phonon-like spectrum determine the system's ability to communicate and adapt.

## Glossary Links
- See also: `Structural Coherence`, `Resonant Spectrum`, `Ki`, `The Current and the Compass (CORE-007)`