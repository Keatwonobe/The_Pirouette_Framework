---
term: "Injection Pressure"
canonical_id: "INJECTION_PRESSURE"
symbol: "Γ_inj"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-157"]
---

---
term: Injection Pressure
canonical_id: INJECTION_PRESSURE
symbol: Γ_inj
aliases: []
parents: [DOMA-157]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-157
      lines: "L52-L56"
      snippet: |
        *   **Injection Pressure (Γ_inj):** The *cause*. This is a proxy for the energy and cost of the initial seed—the obscurity of the source, the concentration of initial reports, the novelty of the signal, and the presence of astroturfed amplification. It is the size of the initial whisper.
  editors: [Weaver-Agent]
  review_log: []
triad:
  art: |
    The unseen hand that plucks a single string, intending to make the entire web resonate. It is the measure of the ventriloquist's whisper, not the puppet's shout.
  law: |
    A narrative's Resonant Gain is inversely proportional to its measurable Injection Pressure. An anomalously high gain (G_R >> 1) for a given effect (ΔKτ) implies an anomalously low, and therefore likely engineered, Injection Pressure.
  philosophy: |
    To distinguish between a river muddied by a storm and one poisoned by a single drop, one must measure the drop. Injection Pressure operationalizes the search for the causal seed, asserting that manipulation is not loud, but efficient and anomalously quiet at its source.
pirouette_definition: |
  A scalar proxy representing the causal energy, cost, and overtness of a narrative's (`Ki`) initial introduction into an information ecosystem. It quantifies the 'push' required to seed a narrative, serving as the denominator in the Resonant Gain calculation (`G_R = ΔKτ / Γ_inj`). A low Γ_inj signifies a 'quiet' or 'stealthy' origin, suggesting high narrative efficiency and potential manipulation.
operational_definition:
  units: Dimensionless index
  symbol_table:
    - name: Γ_inj
      meaning: Injection Pressure
      dimensions: dimensionless
      default_range: Contextual; often normalized to `[0,1]` within a domain
  measurement:
    procedures:
      - name: Provenance Trace & Proxy Estimation
        outline: |
          1. Trace a narrative (`Ki`) back to its earliest identifiable seed event(s).
          2. Construct a composite index from weighted proxies: (a) Source Obscurity (inverse of source authority/reach), (b) Syndication Concentration (high score for many outlets sourcing a single report, i.e., "wire clones"), (c) Signal Novelty (uniqueness of phrasing/concepts), and (d) Astroturfed Amplification (e.g., bot-like behavior in early sharing).
        expected_signals: [Low Γ_inj scores correspond to narratives originating from obscure/new sources, being rapidly cloned across media with no independent corroboration, and/or showing early amplification by inauthentic accounts.]
        pitfalls: [Attribution is the primary challenge; sophisticated actors can mask origins by seeding through a compromised but high-authority source (a 'Laundromat Gambit'). The distinction between a genuinely viral 'citizen' seed and a well-disguised astroturf seed can be ambiguous without behavioral analysis.]
context_windows:
  - module: DOMA-157
    excerpt: |
      **Injection Pressure (Γ_inj):** The *cause*. This is a proxy for the energy and cost of the initial seed—the obscurity of the source, the concentration of initial reports, the novelty of the signal, and the presence of astroturfed amplification. It is the size of the initial whisper.
  - module: DOMA-157
    excerpt: |
      For events triggering a spike in Coherence Flux, the workflow traces the provenance of the new narrative to find its earliest, smallest seed. It then quantifies the Injection Pressure by assessing proxies: source obscurity, syndication concentration (the "wire clone" problem), and astroturfed amplification signals. A low score indicates a "quiet," low-energy origin.
poetic_connections:
  motifs: [whisper, seed, tuning fork, ventriloquist, unseen hand]
  evocative_lines:
    - "The chord is deafening, but no one can see the orchestra."
    - "...distinguish its own voice from an echo."
  association_matrix:
    - [ "Anomalous Efficiency", 0.9 ]
    - [ "Daedalus Gambit", 0.8 ]
    - [ "Resonant Gain", 0.7 ]
    - [ "Wound Channel", 0.5 ]
formal_mappings:
  candidates:
    - target: δ-function driving force, F(t) = A δ(t-t₀)
      domain: CM
      mapping_kind: conceptual
      equation_hint: |
        ẍ + γẋ + ω₀²x = F(t)
      justification: |
        Injection Pressure represents a localized, often instantaneous 'push' on the information system to initiate a new dynamic trajectory. This is analogous to a delta-function driving force applied to a classical oscillator, where a minimal, well-timed impulse (low Γ_inj) at the system's resonant frequency can induce a large-amplitude oscillation (high ΔKτ).
      references:
        - title: Classical Mechanics
          where: Chapter on Driven Oscillations
          date: 1950-01-01
      confidence: 0.6
  adopted:
    - target:
      rationale:
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "Narratives with low, verifiably organic Injection Pressure cannot achieve high Cross-Domain Entrainment and high Resonant Gain without exploiting a pre-existing, high-potential Wound Channel."
      domain: phenomenology
      falsifier: "Observe a demonstrably organic, low-Γ_inj narrative spontaneously generate extreme Resonant Gain across multiple domains (news, markets, social) in a system lacking a clear, pre-existing 'coherence cliff' or Wound Channel. This would suggest gain can be generated without pre-engineered systemic vulnerability."
      status: proposed
      links: [DOMA-157, CORE-011]
naming_notes:
  collisions: [The symbol Γ is used for the Gamma function and connection coefficients (Christoffel symbols) in mathematics and physics. The potential V_Γ shares the symbol. The subscript `_inj` is critical for disambiguation.]
  disambiguation: |
    Distinguish from the general environmental potential `V_Γ`. `Γ_inj` is a specific, event-based measure of a causal *input*, whereas `V_Γ` describes the continuous *environmental state* a narrative must overcome. A low `Γ_inj` event is a tactic to efficiently navigate the `V_Γ` landscape.
crosslinks:
  near_synonyms: []
  antonyms: [Brute-Force Push]
  prerequisites: [Ki Pattern Extraction]
  downstream_effects: [Resonant Gain, Anomalous Gain Confirmed]
license: CC-BY-SA-4.0
---

# Injection Pressure

## Canonical (Pirouette)
A scalar proxy representing the causal energy, cost, and overtness of a narrative's (`Ki`) initial introduction into an information ecosystem. It quantifies the 'push' required to seed a narrative, serving as the denominator in the Resonant Gain calculation (`G_R = ΔKτ / Γ_inj`). A low Γ_inj signifies a 'quiet' or 'stealthy' origin, suggesting high narrative efficiency and potential manipulation.

## EFT-First Summary
Using the conceptual mapping of Injection Pressure to a delta-function driving force in classical mechanics, Γ_inj represents the amplitude and localization of an external impulse applied to a system. A low-Γ_inj narrative is analogous to a precisely timed, minimal 'kick' at an oscillator's resonant frequency, inducing a disproportionately large response (high Resonant Gain). This highlights manipulation as an act of energetic efficiency rather than brute force.

## Glossary Links
- See also: [[Resonant Gain]], [[Coherence Flux]], [[Daedalus Gambit]], [[Anomalous Efficiency]]