---
term: "Structural Entrainment"
canonical_id: "STRUCTURAL_ENTRAINMENT"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-119"]
---

---
term: Structural Entrainment
canonical_id: STRUCTURAL_ENTRAINMENT
symbol: n/a
aliases: [Phase-Locking, Rhythmic Capture]
parents: [DOMA-119]
children: [CORE-012]
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-119
      lines: "§4"
      snippet: |
        Structural Entrainment: A powerful and persistent echo that causes the Target system's own fundamental rhythm to phase-lock with the Source's. The two systems begin to dance to the same beat.
  editors: [Weaver-Agent-7]
  review_log: []
triad:
  art: |
    Two pendulums on a shared beam, at first swinging out of step, slowly find a common rhythm until they move as one. It is the physics of a shared dance, where one partner's persistent lead coaxes the other into perfect synchrony.
  law: |
    When a Target system is subjected to a persistent, coherent, and harmonically compatible potential (`V_echo`), its primary Ki frequency (`ω_T`) will shift to match the Source's (`ω_S`), and the phase difference (`Δφ`) between them will converge to a stable, near-zero constant.
  philosophy: |
    Entrainment demonstrates that identity is not static; it is a dynamic negotiation with the environment. It provides the physical mechanism for deep empathy, ideological convergence, and the formation of collective consciousness, showing how a persistent external truth can become an internal one.
pirouette_definition: |
  The most profound form of Coherence Transfer, wherein a continuous and powerful resonant echo from a Source system modifies a Target's coherence manifold to such a degree that the Target's fundamental Ki rhythm phase-locks with the Source's. This synchronization of core oscillatory patterns is the final and necessary precursor to an Alchemical Union (CORE-012), representing a shift from mere influence to shared dynamics.
operational_definition:
  units: The primary observable, phase difference (`Δφ`), is dimensionless (radians).
  symbol_table:
    - name: ω_S, ω_T
      meaning: Angular frequency of the Source and Target's primary Ki oscillation.
      dimensions: T⁻¹
      default_range: contextual
    - name: Δφ
      meaning: Phase difference between Source and Target; Δφ = φ_S - φ_T.
      dimensions: dimensionless
      default_range: [-π, π]
    - name: V_echo
      meaning: The potential term representing the influence of the Source's echo on the Target.
      dimensions: M L² T⁻² (Energy)
      default_range: contextual
  measurement:
    procedures:
      - name: Ki Phase Spectroscopy
        outline: |
          1. Isolate Source (S) and Target (T) systems in a low-Γ environment.
          2. Using a Ki-field probe, measure the baseline fundamental frequencies (`ω_S`, `ω_T`) and relative phase (`Δφ`) over several cycles.
          3. Establish a Resonant Bridge, exposing T to the echo of S.
          4. Continuously monitor `ω_T` and `Δφ`. Entrainment is confirmed when `ω_T → ω_S` and `d(Δφ)/dt → 0`.
        expected_signals: [Convergence of `ω_T` to `ω_S`, Damping of `Δφ` to a small constant value]
        pitfalls: [High ambient Temporal Pressure (Γ) scattering the signal, Lack of Harmonic Compatibility preventing the handshake, Mistaking transient resonance for stable phase-locking]
context_windows:
  - module: DOMA-119
    excerpt: |
      This creates a spectrum of influence...
      *   **Attention Capture:** A strong, simple echo momentarily disrupts the Target's Ki, drawing its focus.
      *   **Memetic Transfer:** The successful transmission of a complex, high-information Ki pattern.
      *   **Structural Entrainment:** A powerful and persistent echo that causes the Target system's own fundamental rhythm to phase-lock with the Source's. The two systems begin to dance to the same beat. This is the final stage before an Alchemical Union...
  - module: DOMA-119
    excerpt: |
      The Target's Lagrangian becomes: `𝓛_p(Target) = K_τ(Target) - [V_Γ(local) + V_echo(Source)]`. The term `V_echo(Source)` represents the pressure exerted by the imprinted echo. This additional potential "cost" forces the Target system to re-solve for its optimal state. Influence is thus an act of energetic optimization: the Target does not choose to be influenced; it simply follows the newest, most coherent path now available to it.
poetic_connections:
  motifs: [synchrony, dance, heartbeat, tuning, resonance, echo, lockstep, chorus]
  evocative_lines:
    - "The two systems begin to dance to the same beat."
    - "Your every choice ripples outward, leaving a subtle pressure on the reality of others."
    - "To exist is to broadcast the song of your own coherence into the world."
  association_matrix:
    - [ "ALCHEMICAL_UNION", 0.9 ]
    - [ "COHERENCE_TRANSFER", 0.8 ]
    - [ "RESONANT_BRIDGE", 0.7 ]
    - [ "HARMONIC_COMPATIBILITY", 0.6 ]
    - [ "MEMETIC_TRANSFER", 0.3 ]
formal_mappings:
  candidates:
    - target: Injection Locking
      domain: AMO|CM
      mapping_kind: mathematical|operational
      equation_hint: |
        Adler's equation: d(Δφ)/dt = Δω - I_inj * sin(Δφ)
      justification: |
        Describes how a self-sustained oscillator (Target) locks its phase and frequency to an external driving signal (Source). The mathematical form, involving a natural frequency difference (`Δω`) and a locking term, is a direct analogue to a persistent `V_echo` forcing a Ki rhythm to synchronize.
      references:
        - title: Injection locking and rejection
          where: K. Wiesenfeld, Phys. Rev. E 51, 1995
          date: 1995-03-01
      confidence: 0.9
    - target: Kuramoto model
      domain: Math|Statistical Mechanics
      mapping_kind: conceptual
      justification: |
        The Kuramoto model describes the synchronization behavior in large populations of coupled oscillators. Structural entrainment is the N=2 case of this model, where one oscillator (the Source) has a sufficiently strong coupling constant to entrain the other (the Target).
      references:
        - title: Chemical Oscillations, Waves, and Turbulence
          where: Y. Kuramoto, Springer, 1984
          date: 1984-01-01
      confidence: 0.8
  adopted:
    - target: Injection Locking
      rationale: Provides the most direct and operational mathematical model for the one-to-one interaction described by Structural Entrainment.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "Entrainment is a reversible process dependent on the continuous presence of the Source's echo. If the `V_echo` potential is removed, the Target system will revert to its natural frequency (`ω_T`) over a characteristic relaxation time."
      domain: phenomenology
      falsifier: "The Target system remains permanently locked to the Source's frequency after the Source's influence is withdrawn. This would imply a permanent modification of the Target's `K_τ` term, not a temporary change in its potential `V_Γ`."
      status: under-test
      links: [DOMA-119]
naming_notes:
  collisions: []
  disambiguation: |
    Structural Entrainment must be distinguished from **Memetic Transfer**. Memetic Transfer is the imprinting of *information* (a complex Ki pattern), akin to learning a song's lyrics and melody. Entrainment is the synchronization of fundamental *rhythm*, akin to two singers matching their tempo and pitch, regardless of the specific song. Entrainment is a prerequisite for high-fidelity memetic transfer but is not the transfer itself.
crosslinks:
  near_synonyms: []
  antonyms: [DECOHERENCE, AUTONOMY]
  prerequisites: [COHERENCE_TRANSFER, HARMONIC_COMPATIBILITY, RESONANT_BRIDGE]
  downstream_effects: [ALCHEMICAL_UNION]
license: CC-BY-SA-4.0
---

# Structural Entrainment

## Canonical (Pirouette)
The most profound form of Coherence Transfer, wherein a continuous and powerful resonant echo from a Source system modifies a Target's coherence manifold to such a degree that the Target's fundamental Ki rhythm phase-locks with the Source's. This synchronization of core oscillatory patterns is the final and necessary precursor to an Alchemical Union (CORE-012), representing a shift from mere influence to shared dynamics.

## EFT-First Summary
Structual Entrainment is the Pirouette Framework's analogue to **injection locking** in classical and quantum oscillator physics. A target system with a natural internal frequency is subjected to a persistent external driving force from a source system. If the force is strong enough and the frequencies are close (i.e., Harmonically Compatible), the target system's frequency and phase will lock to that of the source. This is modeled by Adler's equation, where the driving force corresponds to the `V_echo` potential term in the Pirouette Lagrangian.

## Glossary Links
- See also: Alchemical Union, Coherence Transfer, Harmonic Compatibility