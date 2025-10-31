---
term: "Cross-Domain Entrainment"
canonical_id: "CROSS_DOMAIN_ENTRAINMENT"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-157"]
---

---
term: Cross-Domain Entrainment
canonical_id: CROSS_DOMAIN_ENTRAINMENT
symbol: "ΔKτ > θ_entrain"
aliases: [phase-locking, narrative synchronization]
parents: [DOMA-157]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-157
      lines: "L102-L104"
      snippet: |
        Orange Flag: Cross-Domain Entrainment. The pattern's resonance has jumped to a second or third domain, creating a powerful Laminar Flow. *The note has become a chord, and the whole room is vibrating with it.*
  editors: [System Weaver]
  review_log: []
triad:
  art: |
    A single note becomes a chord, and the whole room begins to vibrate with it. A story escapes its original medium and becomes the ambient music of the world, shaping the silence between other sounds.
  law: |
    A narrative pattern (`Ki`) achieves entrainment when its coherence signature (`Kτ`) exhibits a statistically significant phase-locking across two or more distinct information domains (e.g., social, financial, political) within a defined temporal window.
  philosophy: |
    Entrainment marks the moment a story transcends being *information* and becomes *environment*. It is the threshold where a narrative gains the power to shape reality not just by being told, but by becoming the silent context for all other actions.
pirouette_definition: |
  The process by which a coherent narrative pattern (`Ki`), having achieved resonance in a primary domain, precipitates a phase-locking of information flow in one or more separate domains. This synchronization creates a powerful, unified Laminar Flow, representing a significant increase in the narrative's systemic Coherence Flux (`ΔKτ`). It is the key observable transition between a localized Coherence Spike and a potential system-wide state change, and a necessary condition for calculating Resonant Gain.
operational_definition:
  units: Dimensionless (a state transition identified via correlation metrics).
  symbol_table:
    - name: Ki
      meaning: A recurring, coherent narrative pattern or cluster.
      dimensions: dimensionless
      default_range: contextual
    - name: Kτ
      meaning: Coherence; the degree of internal resonance of a Ki.
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: ΔKτ
      meaning: Coherence Flux; the change in a Ki's coherence over time and across domains.
      dimensions: dimensionless
      default_range: contextual
  measurement:
    procedures:
      - name: Cross-Correlation Phase-Locking
        outline: |
          1. Ingest time-series data from multiple domains (e.g., social media mentions, news headline frequency, market volatility).
          2. Identify a dominant narrative pattern (`Ki`) and its temporal signature in a primary domain.
          3. Compute the rolling cross-correlation or phase coherence between the primary domain's signal and the signals from secondary domains.
          4. Entrainment is confirmed when the coherence metric surpasses a dynamically calibrated threshold (`θ_entrain`) and remains stable.
        expected_signals: [A sharp, sustained increase in the cross-correlation function between domain time series, A synchronized spike in spectral density at a characteristic frequency across domains.]
        pitfalls: [Spurious correlations caused by a confounding, exogenous global event, Domain definitions are too broad or overlapping, leading to false positives.]
context_windows:
  - module: DOMA-157
    excerpt: |
      For each identified `Ki`, the protocol measures its degree of phase-locking across different domains. A sudden, qualitative phase shift where disparate streams lock into a single, unified Laminar Flow—an **Alchemical Union (CORE-012)**—is the primary trigger, representing a significant `ΔKτ`.
  - module: DOMA-157
    excerpt: |
      The workflow translates into a simple set of diagnostic flags... **Yellow Flag: Coherence Spike.** A single narrative pattern (`Ki`) has suddenly achieved high internal resonance within one domain. ... **Orange Flag: Cross-Domain Entrainment.** The pattern's resonance has jumped to a second or third domain, creating a powerful Laminar Flow.
poetic_connections:
  motifs: [resonance, harmonics, synchronization, contagion, river-flow, chord]
  evocative_lines:
    - "The note has become a chord, and the whole room is vibrating with it."
    - "disparate streams lock into a single, unified Laminar Flow"
    - "the whispers that start avalanches"
  association_matrix:
    - [ "COHERENCE_FLUX", 0.9 ]
    - [ "LAMINAR_FLOW", 0.8 ]
    - [ "ALCHEMICAL_UNION", 0.6 ]
    - [ "ANOMALOUS_GAIN", 0.5 ]
formal_mappings:
  candidates:
    - target: Mode-locking / Phase-locking of coupled oscillators
      domain: CM
      mapping_kind: conceptual
      equation_hint: |
        dθ_i/dt = ω_i + Σ K_ij * sin(θ_j - θ_i)
      justification: |
        Information domains can be modeled as weakly coupled oscillators, each with a natural rhythm. A high-coherence narrative (`Ki`) acts as a powerful forcing function or coupling agent that drives disparate domains to synchronize to a common phase and frequency. Entrainment is the onset of this collective, mode-locked state.
      references:
        - title: Sync: The Emerging Science of Spontaneous Order
          where: Strogatz, S. (2003)
          date: 2003-01-01
      confidence: 0.85
  adopted:
    - target: Phase-locking of coupled oscillators
      rationale: The mapping is conceptually direct, operationally useful for modeling, and draws on a well-understood physical phenomenon that captures both the synchronization and resonance aspects of the term.
      confidence: 0.85
constraints_and_falsifiers:
  claims:
    - statement: "A high Resonant Gain (`G_R >> 1`) event requires Cross-Domain Entrainment as a necessary precondition."
      domain: phenomenology
      falsifier: "The discovery of a confirmed high-gain manipulation (Red Flag) that achieved its effect entirely within a single, isolated domain without measurable spillover or phase-locking. This would imply an alternative mechanism for anomalous efficiency not dependent on systemic resonance."
      status: proposed
      links: [DOMA-157]
naming_notes:
  collisions: [The term "entrainment" is widely used in chronobiology (synchronization of circadian rhythms to external cues) and neuroscience (neural entrainment to sensory stimuli).]
  disambiguation: |
    In Pirouette, 'entrainment' specifically refers to the synchronization of *narrative patterns* across distinct *information domains* (e.g., social, financial), not the synchronization of biological rhythms or neural oscillators, though the underlying dynamical principle of coupled systems is analogous.
crosslinks:
  near_synonyms: [PHASE_LOCKING, LAMINAR_FLOW]
  antonyms: [DECOHERENCE, TURBULENT_FLOW]
  prerequisites: [COHERENCE_SPIKE]
  downstream_effects: [ANOMALOUS_GAIN, MANAGED_NARRATIVE_CHANNEL]
license: CC-BY-SA-4.0
---

# Cross-Domain Entrainment

## Canonical (Pirouette)
The process by which a coherent narrative pattern (`Ki`), having achieved resonance in a primary domain, precipitates a phase-locking of information flow in one or more separate domains. This synchronization creates a powerful, unified Laminar Flow, representing a significant increase in the narrative's systemic Coherence Flux (`ΔKτ`). It is the key observable transition between a localized Coherence Spike and a potential system-wide state change, and a necessary condition for calculating Resonant Gain.

## EFT-First Summary
Cross-Domain Entrainment maps to the well-understood physical phenomenon of **phase-locking in coupled oscillators**. Just as separate pendulums on a shared surface will eventually synchronize their swings, distinct information domains (e.g., markets, social media) can be modeled as oscillators that lock onto the phase of a powerful, resonant narrative. This event marks a transition to a collective, coherent state, making the system highly susceptible to efficient, low-energy manipulation.

## Glossary Links
- See also: [COHERENCE_FLUX](<#>), [LAMINAR_FLOW](<#>), [ANOMALOUS_GAIN](<#>)