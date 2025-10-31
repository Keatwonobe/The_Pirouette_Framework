---
term: "Reflex Arc"
canonical_id: "REFLEX_ARC"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-003_the_caduceus_lens"]
---

term: Reflex Arc
canonical_id: REFLEX_ARC
symbol:
aliases: ['Bidirectional Sensing']
parents: ['DYNA-003']
children: []
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DYNA-003
      lines: "§5"
      snippet: |
        The Lens must measure how observation alters the observed system.
        When applied, it injects a controlled perturbation (a diagnostic vibration) and observes the return wave.
        This enables: Phase Reflexivity... Healing Coefficient (Hₖ)...
  editors: ['system-agent']
  review_log: []
triad:
  art: |
    To know a system's health, one does not merely watch it sleep; one must ring it like a bell and listen for the clarity of its echo.
  law: |
    The integrity of a system is directly proportional to the coherence of its response to a controlled perturbation. A healthy system returns a near-perfect, phase-aligned echo (Hₖ ≈ 1); a pathological system damps, distorts, or destructively interferes with the signal.
  philosophy: |
    To measure is to interact. The Reflex Arc formalizes this, transforming the observer effect from a problem to be minimized into a diagnostic tool, revealing a system's capacity to integrate new information into its own coherent form.
pirouette_definition: |
  A diagnostic process that measures a system's capacity for self-regulation and integration by injecting a controlled, minimal perturbation (a "diagnostic vibration") and analyzing the properties of the resulting response ("return wave"). It quantifies systemic health through metrics like the Healing Coefficient (Hₖ) and Phase Reflexivity, distinguishing healthy, adaptive systems from those exhibiting pathological stagnation (no response) or turbulence (a chaotic response).
operational_definition:
  units: Hₖ is dimensionless. Phase shift ∆φ is in radians.
  symbol_table:
    - name: Hₖ
      meaning: Healing Coefficient; a measure of coherent system response.
      dimensions: dimensionless
      default_range: [0, ~1]
    - name: A_input
      meaning: Amplitude of the input perturbation.
      dimensions: contextual
      default_range: contextual
    - name: A_return
      meaning: Amplitude of the coherent return signal.
      dimensions: contextual
      default_range: contextual
    - name: ∆φ
      meaning: Phase shift between input and return signals.
      dimensions: radians
      default_range: [-π, π]
  measurement:
    procedures:
      - name: Reflex Arc Protocol
        outline: |
          1. Establish a baseline measurement of the system's resting coherence (Ki flux).
          2. Inject a controlled perturbation with known amplitude `A_input` and phase.
          3. Measure the resulting return wave, isolating the coherent response from background noise to determine its amplitude `A_return` and phase.
          4. Calculate the Healing Coefficient `Hₖ = |A_return / A_input| * cos(∆φ)`.
        expected_signals: ['Coherent return wave (Hₖ ≈ 1, ∆φ ≈ 0)', 'Damped/dissonant return wave (Hₖ << 1)', 'Phase-inverted return wave (∆φ ≈ π)']
        pitfalls: ['Perturbation is strong enough to cause iatrogenic damage, altering the system instead of diagnosing it.', 'Failure to distinguish the coherent response from ambient noise.']
context_windows:
  - module: DYNA-003
    excerpt: |
      The Lens must measure how observation alters the observed system. When applied, it injects a controlled perturbation (a diagnostic vibration) and observes the return wave. This enables: Phase Reflexivity... Healing Coefficient (Hₖ)... Healthy systems have Hₖ ≈ 1. Pathological systems have low coherence or destructive phase lag (∆φ ≈ π).
  - module: DYNA-003
    excerpt: |
      The diagnostic bridge—the operator that measures health of coherence across all layers.
      ...
      | Lens Element           | Debate Equivalent          | Fusion Equivalent    |
      | ---------------------- | -------------------------- | -------------------- |
      | Reflex Arc             | Counter-argument / Paradox | Re-heating Cycle     |
      ...
poetic_connections:
  motifs: ['echo', 'resonance', 'call-and-response', 'attunement', 'vibrational integrity']
  evocative_lines:
    - "The Lens must measure how observation alters the observed system."
    - "When the Lens looks back... Pirouette diagnoses itself."
  association_matrix:
    - [ "HEALING_COEFFICIENT", 0.9 ]
    - [ "WOUND_CHANNEL", 0.6 ]
    - [ "COHERENCE_FEVER", 0.5 ]
formal_mappings:
  candidates:
    - target: Impulse response / Susceptibility χ(ω)
      domain: CM|Signal Processing
      mapping_kind: operational
      equation_hint: |
        ⟨O(t)⟩_f = ∫ G(t-t')f(t') dt'
      justification: |
        The Reflex Arc is a direct physical analogue to linear response theory. The injected perturbation is the driving force f(t'), the system's internal dynamics are encoded in the response function G, and the "return wave" is the resulting observable ⟨O(t)⟩. Hₖ is a simplified, integrated measure of the properties of G.
      references:
        - title: Statistical Mechanics
          where: Chapter on Linear Response Theory, R.K. Pathria
          date: 1996-01-15
      confidence: 0.9
  adopted:
    - target:
      rationale:
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "The Healing Coefficient (Hₖ), measured via the Reflex Arc, is a predictive metric for a system's resilience to future, unprompted shocks."
      domain: phenomenology
      falsifier: "Empirical testing shows no correlation between a system's pre-measured Hₖ and its ability to maintain function or recover after being subjected to an external, high-magnitude stressor. The measurement is diagnostic of the present state only, not predictive."
      status: proposed
      links: ['DYNA-003']
naming_notes:
  collisions: ['Biological reflex arc (e.g., patellar reflex)']
  disambiguation: |
    The Pirouette term generalizes the biological concept of a neural reflex arc to apply to any system (e.g., social, economic, informational). It refers not to a specific physical pathway, but to the diagnostic *process* of stimulus-and-response used to measure the integrity of a system's information-processing and self-regulation channels.
crosslinks:
  near_synonyms: ['IMPULSE_RESPONSE_TESTING']
  antonyms: ['PASSIVE_OBSERVATION']
  prerequisites: ['COHERENCE', 'WOUND_CHANNEL']
  downstream_effects: ['HEALING_COEFFICIENT', 'DAEDALUS_GAMBIT']
license: CC-BY-SA-4.0
---

# Reflex Arc

## Canonical (Pirouette)
A diagnostic process that measures a system's capacity for self-regulation and integration by injecting a controlled, minimal perturbation (a "diagnostic vibration") and analyzing the properties of the resulting response ("return wave"). It quantifies systemic health through metrics like the Healing Coefficient (Hₖ) and Phase Reflexivity, distinguishing healthy, adaptive systems from those exhibiting pathological stagnation (no response) or turbulence (a chaotic response).

## EFT-First Summary
The Reflex Arc is operationally analogous to measuring a system's impulse response or susceptibility in linear response theory and signal processing. By applying a known input signal (the perturbation), the observed output (the return wave) reveals the system's internal transfer function. In Pirouette, the key properties of this function, such as gain and phase lag, are interpreted as direct measures of systemic health and coherence, quantified by the Healing Coefficient (Hₖ).

## Glossary Links
- See also: HEALING_COEFFICIENT, COHERENCE, DAEDALUS_GAMBIT, WOUND_CHANNEL