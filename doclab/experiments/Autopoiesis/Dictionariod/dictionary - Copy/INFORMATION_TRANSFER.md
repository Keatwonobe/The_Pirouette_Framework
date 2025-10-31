---
term: "Information Transfer"
canonical_id: "INFORMATION_TRANSFER"
symbol: "Φ_Kτ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-159"]
---

---
term: Information Transfer
canonical_id: INFORMATION_TRANSFER
symbol: Φ_Kτ
aliases: ["Echo Fidelity", "Coherence Flow", "I_gain"]
parents: ["DOMA-159"]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-159
      lines: "§5 · The Shadow Gauge Protocol"
      snippet: |
        **Information Transfer (Φ_Kτ):** Measures the net flow of coherence between the observer and the system, quantifying the fidelity of the Measurement Echo. A positive flow indicates the observer successfully imprinted its pattern onto the system (high `I_gain`). A negative flow indicates the system's resonance was so powerful it altered the observer's state (an act of "learning" by the observer, but potentially a failed measurement).
  editors: ["system-compiler"]
  review_log: []
triad:
  art: |
    A measure of the shared song in an echo. It tracks whether the observer's question or the system's answer sang louder in their brief duet, revealing the balance of influence in the act of knowing.
  law: |
    Information Transfer is a signed quantity representing the net gain in structured coherence by the observer attributable to the system. A positive value (Φ_Kτ > 0) correlates with a successful measurement, while a negative value (Φ_Kτ < 0) indicates the measurement apparatus was coherently altered by the system in a way that corrupted the intended data channel.
  philosophy: |
    This metric reframes measurement from passive data extraction to an active, bidirectional exchange. It quantifies not just *what* was learned, but *who* was transformed by the interaction, forcing the observer to account for their own change as part of the result. It is the formal acknowledgement that no question is asked without risk to the asker.
pirouette_definition: |
  A core metric of the Shadow Gauge Protocol that quantifies the net directional flow of temporal coherence (Kτ) between an observer and a system during a measurement interaction. It measures the fidelity of the resulting Measurement Echo in the observer's manifold. A positive value (Φ_Kτ > 0) indicates a high-fidelity echo was formed and information was gained, while a negative value indicates the system's resonance actively disrupted the observer's coherence, corrupting the measurement.
operational_definition:
  units: Joules (J)
  symbol_table:
    - name: Φ_Kτ
      meaning: Information Transfer
      dimensions: M L^2 T^-2 (Energy)
      default_range: contextual, can be < 0, = 0, or > 0
    - name: ΔKτ_obs
      meaning: Change in observer's temporal coherence
      dimensions: M L^2 T^-2 (Energy)
      default_range: contextual
    - name: ΔKτ_sys
      meaning: Change in system's temporal coherence (Coherence Cost)
      dimensions: M L^2 T^-2 (Energy)
      default_range: contextual
  measurement:
    procedures:
      - name: Shadow Gauge Audit
        outline: |
          1. Establish baseline temporal coherence Kτ_sys and Kτ_obs for the uncoupled system and observer.
          2. Model the measurement interaction by introducing the observer's potential, V_obs, into the system's Lagrangian.
          3. Evolve the coupled system-observer state through the measurement period.
          4. Measure the final coherence states, Kτ'_sys and Kτ'_obs.
          5. Calculate Φ_Kτ as the component of ΔKτ_obs = (Kτ'_obs - Kτ_obs) that is isomorphically structured as an echo of the system, minus dissonant changes.
        expected_signals: [A coherent change in the observer's state vector, A corresponding change in the system's state vector]
        pitfalls: [Observer state is contaminated by environmental noise (VΓ_env), System's resonant response overwhelms and decoheres the observer state (resulting in Φ_Kτ < 0)]
context_windows:
  - module: DOMA-159
    excerpt: |
      **Information Transfer (Φ_Kτ):** Measures the net flow of coherence between the observer and the system, quantifying the fidelity of the Measurement Echo. A positive flow indicates the observer successfully imprinted its pattern onto the system (high `I_gain`). A negative flow indicates the system's resonance was so powerful it altered the observer's state (an act of "learning" by the observer, but potentially a failed measurement).
  - module: DOMA-159
    excerpt: |
      **Psychology:** Assesses interviewer bias by measuring the `Information Transfer (Φ_Kτ)` between therapist and client, revealing the subtle ways one's own patterns shape another's narrative.
poetic_connections:
  motifs: [echo, fidelity, resonance, flow, duet, imprint, gaze]
  evocative_lines:
    - "The data we receive is the memory of that shared step."
    - "To measure the world is to take responsibility for the echo you leave behind."
  association_matrix:
    - [ "MEASUREMENT_ECHO", 0.9 ]
    - [ "OBSERVERS_SHADOW", 0.6 ]
    - [ "COHERENCE_COST", 0.5 ]
    - [ "SHADOW_GAUGE", 0.8 ]
formal_mappings:
  candidates:
    - target: Mutual Information I(X;Y)
      domain: Math
      mapping_kind: conceptual
      equation_hint: |
        Φ_Kτ ∝ I(Observer_final; System_initial)
      justification: |
        Mutual information quantifies the reduction of uncertainty about one variable from knowing another. This strongly aligns with Φ_Kτ's role in measuring the fidelity of an echo—how much information about the system is successfully encoded in the observer's state after interaction. Unlike I(X;Y), however, Φ_Kτ is a signed, energetic quantity.
      references:
        - title: Elements of Information Theory
          where: "Cover, T. M.; Thomas, J. A. (2006), Chapter 2"
          date: 2006-07-18
      confidence: 0.7
  adopted:
    - target: null
      rationale: null
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "A measurement interaction can result in a negative Information Transfer (Φ_Kτ < 0), where the system's state actively imprints a dissonant pattern on the observer, corrupting the measurement channel."
      domain: experiment
      falsifier: "A comprehensive experimental survey finds no reproducible instances of Φ_Kτ < 0. All interactions that alter the observer's state either produce a positive information transfer or zero, indicating information cannot be 'negatively' transferred."
      status: proposed
      links: ["DOMA-159"]
naming_notes:
  collisions: ["The symbol Φ is commonly used for magnetic flux, electric flux, and the golden ratio. The Kτ subscript is essential for disambiguation."]
  disambiguation: |
    Information Transfer is distinct from Shannon or classical information. Φ_Kτ is a physical quantity with units of energy (Joules), not a dimensionless statistical measure (bits). It can be negative, representing a corruption of the measurement channel, a concept with no direct analogue in classical information theory.
crosslinks:
  near_synonyms: [ECHO_FIDELITY]
  antonyms: [COHERENCE_COST]
  prerequisites: [MEASUREMENT_ECHO, OBSERVERS_SHADOW]
  downstream_effects: [SHADOW_PROFILE]
license: CC-BY-SA-4.0
---