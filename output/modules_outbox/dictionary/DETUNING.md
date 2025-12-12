---
term: "Detuning"
canonical_id: "DETUNING"
symbol: '\Delta f'

aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COG-RES-001"]
---

---
term: Detuning
canonical_id: DETUNING
symbol: \Delta f
aliases: [frequency deviation, resonance bandwidth, allowed detuning]
parents: [COG-RES-001]
children: [COG-RES-002, MATH-025]
status: draft
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COG-RES-001
      lines: "§5"
      snippet: |
        3. **Gamma-Load Detuning Function:**
           [\Delta f_{allowed} \propto \Gamma^{-1/2}]
           Predicts narrowing of viable frequency triads under high cognitive load.
  editors: [AI Assistant]
  review_log: []
triad:
  art: |
    A triad of notes can tolerate a slight dissonance, a gentle blurring at the edges. But as the world's demands sharpen this tolerance, only perfect harmony can hold the conscious moment.
  law: |
    The permissible frequency detuning (\Delta f) from a perfect Ki-addition triad is inversely proportional to the square root of the environmental load (\Gamma).
  philosophy: |
    Detuning quantifies the system's tolerance for imperfection. Its inverse relationship with environmental load suggests that conscious focus is not a metaphor, but a literal narrowing of resonance bandwidth—a process of tuning out noise to maintain a coherent state.
pirouette_definition: |
  The allowed frequency deviation from the strict Ki-addition rule (`f_3 = f_1 + f_2`) for a conscious triad. This deviation, symbolized as \Delta f, defines the resonance bandwidth necessary for maintaining triadic phase coupling. The Pirouette Framework hypothesizes that this bandwidth is not fixed but is dynamically constrained, narrowing as environmental load (\Gamma) increases according to the relation \Delta f \propto \Gamma^{-1/2}.
operational_definition:
  units: Hertz (Hz)
  symbol_table:
    - name: \Delta f
      meaning: Allowed frequency detuning from a perfect triad.
      dimensions: T^{-1}
      default_range: 0-10 Hz (in neural contexts)
    - name: \Gamma
      meaning: Environmental load or task complexity.
      dimensions: dimensionless or bits/s
      default_range: contextual
  measurement:
    procedures:
      - name: Gamma-Load Detuning Function Measurement
        outline: |
          1. Record neural activity (e.g., EEG) while a subject performs a task with variable cognitive load (\Gamma).
          2. Identify frequency triads (f_1, f_2, f_3) exhibiting significant Triadic Phase Coupling Index (TPCI).
          3. For each load level \Gamma, measure the frequency bandwidth (\Delta f) around the ideal `f_3 = f_1 + f_2` where TPCI remains above a defined threshold.
          4. Plot \Delta f as a function of \Gamma and fit to the model \Delta f = k \Gamma^{-1/2}.
        expected_signals: [TPCI, instantaneous frequency]
        pitfalls: [Low signal-to-noise ratio in neural data, inaccurate quantification of environmental load (\Gamma), non-task-related cognitive confounds]
context_windows:
  - module: COG-RES-001
    excerpt: |
      **Detuning Constraint Hypothesis:** The allowed detuning (\Delta f) narrows as (\Gamma) (task complexity / entropy load) increases.
  - module: COG-RES-001
    excerpt: |
      **Gamma-Load Detuning Function:** [\Delta f_{allowed} \propto \Gamma^{-1/2}] Predicts narrowing of viable frequency triads under high cognitive load.
poetic_connections:
  motifs: [tuning, focus, dissonance, harmony, signal vs noise]
  evocative_lines:
    - "The allowed detuning (\Delta f) narrows as (\Gamma) increases."
    - "Inverse square narrowing of detuning."
  association_matrix:
    - [ "ENVIRONMENTAL_LOAD", 0.9 ]
    - [ "TRIADIC_RESONANCE", 0.7 ]
    - [ "COHERENCE_AREA", 0.5 ]
formal_mappings:
  candidates:
    - target: Resonance width (\Delta\omega) of a driven harmonic oscillator
      domain: CM
      mapping_kind: conceptual
      equation_hint: |
        \Delta \omega \approx \omega_0 / Q
      justification: |
        Detuning (\Delta f) acts as the effective resonance bandwidth for a conscious triad. This is conceptually analogous to the resonance width of a damped, driven oscillator, which is inversely proportional to its Quality Factor (Q). In this mapping, increasing environmental load (\Gamma) corresponds to an effective increase in the system's Q-factor, sharpening the resonance and reducing tolerance for detuning.
      references:
        - title: Classical Mechanics
          where: J. R. Taylor, Chapter 5
          date: 2005-01-01
      confidence: 0.6
  adopted:
    []
constraints_and_falsifiers:
  claims:
    - statement: 'The allowed detuning (\Delta f) is inversely proportional to the square root of environmental load (\Gamma).'

      domain: experiment
      falsifier: 'Experimental measurement shows that \Delta f is constant, increases, or decreases with a different functional form (e.g., linear) as \Gamma increases.'

      status: proposed
      links: [COG-RES-001]
naming_notes:
  collisions: [The symbol \Delta is commonly used for change or difference in many fields. The module COG-RES-001 also uses \delta f.]
  disambiguation: |
    Distinguish from the general concept of frequency mismatch. Pirouette's Detuning is a *dynamic, load-dependent variable* that defines the boundary of a stable conscious state, not a static error term. The canonical symbol is \Delta f.
crosslinks:
  near_synonyms: []
  antonyms: [PERFECT_TRIAD]
  prerequisites: [TRIADIC_RESONANCE, KI_ADDITION_CONSTRAINT, ENVIRONMENTAL_LOAD]
  downstream_effects: [CONSCIOUSNESS_ACCESS, COHERENCE_AREA_CONSERVATION]
license: CC-BY-SA-4.0
---

# Detuning

## Canonical (Pirouette)
The allowed frequency deviation from the strict Ki-addition rule (`f_3 = f_1 + f_2`) for a conscious triad. This deviation, symbolized as \Delta f, defines the resonance bandwidth necessary for maintaining triadic phase coupling. The Pirouette Framework hypothesizes that this bandwidth is not fixed but is dynamically constrained, narrowing as environmental load (\Gamma) increases according to the relation \Delta f \propto \Gamma^{-1/2}.

## Physics-First Summary
Conceptually, Detuning maps to the resonance width of a driven oscillator in classical mechanics. As the system's effective Q-factor increases (driven by cognitive load), the resonance sharpens, decreasing the allowed detuning. This provides a physical intuition for 'focus' as a literal narrowing of the system's frequency response.

## Glossary Links
- See also: [Triadic Resonance](<#>), [Environmental Load](<#>), [Ki-Addition Constraint](<#>)