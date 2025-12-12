---
term: "Information"
canonical_id: "INFORMATION"
symbol: "I"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["CORE-013_the_river_of_information"]
---

---
term: Information
canonical_id: INFORMATION
symbol: I
aliases: []
parents: [CORE-013]
children: []
status: draft
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: CORE-013_the_river_of_information
      lines: "21-25"
      snippet: |
        Information (I): The information content of a system is a direct measure of its coherence (Kτ). A system with a stable, sharply defined Ki pattern is a low-entropy, high-information state. It is a clear signal, a distinct note in the cosmic song.
  editors: [System]
  review_log: []
triad:
  art: |
    A river of coherence flowing through a landscape of noise; a clear note sung against the static of the cosmos. It is the signature of a thing that holds itself together against the current.
  law: |
    The information content (I) of a system is directly proportional to its measured coherence (Kτ). It quantifies the degree to which a system's energy is bound in a stable, predictable, and thus work-capable, pattern. I ∝ Kτ.
  philosophy: |
    Information is not static data but the active persistence of form. It re-frames existence not as an inevitable decline into disorder (entropy), but as a constant struggle to create and maintain islands of coherence against a universal tide of noise.
pirouette_definition: |
  The degree of a system's coherence (Kτ), representing a stable, low-entropy pattern. High information states possess a sharply defined internal resonance (Ki pattern), making their energy structured and available to perform work. Information is the measure of a system's successful, temporary defiance of ambient temporal noise (Γ).
operational_definition:
  units: Dimensionless (or bits)
  symbol_table:
    - name: I
      meaning: Information; degree of coherence
      dimensions: dimensionless
      default_range: "[0, ∞)"
    - name: Kτ
      meaning: Temporal Coherence
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: S
      meaning: Entropy; degree of temporal dissonance
      dimensions: J/K (joules per kelvin)
      default_range: "[0, ∞)"
  measurement:
    procedures:
      - name: Coherence Spectroscopy
        outline: |
          A system's information content is inferred by measuring its coherence. This is done by analyzing the system's response to external probes or its own emissions over time. The stability, predictability, and bandwidth of the system's characteristic resonant frequency (its Ki pattern) are quantified.
        expected_signals: [Sharp, narrow-bandwidth spectral peaks, Low phase noise, High signal-to-noise ratio]
        pitfalls: [Measurement intrusion introducing decoherence, Environmental noise (Γ) masking the signal]
context_windows:
  - module: CORE-013_the_river_of_information
    excerpt: |
      Information (I): The information content of a system is a direct measure of its coherence (Kτ). A system with a stable, sharply defined Ki pattern is a low-entropy, high-information state. It is a clear signal, a distinct note in the cosmic song. Its pattern is predictable, and because it is stable, it has the capacity to couple with other systems and perform work. It has energy that is available.
  - module: CORE-013_the_river_of_information
    excerpt: |
      A coherent system is a river of information flowing through the landscape of entropic noise... This constant interaction inevitably introduces noise into its Ki pattern, "eroding" its coherence over time... The river of information slows, widens, and ultimately merges with the chaotic sea of the background Γ, its unique signal lost in the noise.
  - module: CORE-013_the_river_of_information
    excerpt: |
      A living organism is a masterpiece of coherence. It maintains its incredible low-entropy state... by exploiting it. It is an "entropy pump." It actively consumes low-entropy, high-information energy from its environment... and uses it to maintain and repair its own coherence, while expelling high-entropy, low-information waste.
poetic_connections:
  motifs: [river, island, signal, noise, song, pattern, order]
  evocative_lines:
    - "A river of information flowing through the landscape of entropic noise."
    - "A clear signal, a distinct note in the cosmic song."
    - "Information is not static data; it is the active, willful persistence of a pattern."
  association_matrix:
    - [ "COHERENCE", 0.9 ]
    - [ "ENTROPY", 0.8 ]
    - [ "NOISE", 0.8 ]
    - [ "LIFE", 0.7 ]
formal_mappings:
  candidates:
    - target: Shannon Entropy (H)
      domain: CM|Information Theory
      mapping_kind: conceptual
      equation_hint: |
        I_pirouette ∝ -H(X) = Σ p(x) log p(x)
      justification: |
        Shannon Entropy (H) quantifies the uncertainty or unpredictability of a system's state. Pirouette's Information (I) is defined as the opposite: the degree of order, stability, and predictability. Therefore, I is inversely proportional to H.
      references:
        - title: A Mathematical Theory of Communication
          where: Bell System Technical Journal
          date: 1948-07-01
      confidence: 0.9
  adopted:
    - target: Negentropy (N)
      rationale: |
        Negentropy (N = S_max - S_actual) directly quantifies a system's distance from a state of maximum entropy (disorder). This aligns perfectly with Pirouette's definition of Information as a measure of coherence and structured, work-capable energy. It is the most direct and operational mapping.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "A system's capacity to perform work is a monotonically increasing function of its Information (I)."
      domain: theory|experiment
      falsifier: "Demonstration of two systems where the one with lower measured coherence (Kτ) and thus lower Information (I) can consistently perform more thermodynamic work than the higher-coherence system, under identical energy conditions."
      status: proposed
      links: [CORE-013]
naming_notes:
  collisions: [Electric Current (I), Moment of Inertia (I), Luminous Intensity (I)]
  disambiguation: |
    Unlike the standard information-theoretic usage where "information" is often synonymous with entropy/uncertainty (H), Pirouette's Information (I) is an inverse concept. It measures order, predictability, and coherence. It is operationally equivalent to *negentropy*, not entropy.
crosslinks:
  near_synonyms: [COHERENCE, ORDER, NEGENTROPY]
  antonyms: [ENTROPY, NOISE, DISSONANCE]
  prerequisites: [COHERENCE, TEMPORAL_PRESSURE]
  downstream_effects: [LIFE, ALCHEMICAL_UNION, WOUND_CHANNEL]
license: CC-BY-SA-4.0
---

# Information

## Canonical (Pirouette)
The degree of a system's coherence (Kτ), representing a stable, low-entropy pattern. High information states possess a sharply defined internal resonance (Ki pattern), making their energy structured and available to perform work. Information is the measure of a system's successful, temporary defiance of ambient temporal noise (Γ).

## EFT-First Summary
In the language of statistical mechanics, Pirouette's Information (I) is operationally equivalent to negentropy (`N = S_max - S`). It quantifies a system's distance from thermodynamic equilibrium (maximum entropy), representing the structured, available energy (free energy) that can be extracted to perform work. A state of high Information is one of low statistical entropy, high order, and high predictability.

## Glossary Links
- See also: [Coherence](<#>), [Entropy](<#>), [Temporal Pressure](<#>)