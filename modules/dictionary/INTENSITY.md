---
term: "Intensity"
canonical_id: "INTENSITY"
symbol: ""
aliases: [The Projection]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-197"]
---

---
term: Intensity
canonical_id: INTENSITY
symbol: A_Ψ
aliases: [The Projection]
parents: [DOMA-197]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-197
      snippet: |
        Intensity (The Projection): [...] Intensity is the amplitude of the Observer's Shadow that carves this channel, a function of focus and conviction. A high-intensity projection creates a deep coherence well, a steep gradient that makes the desired path almost irresistible.
  editors: [Agent.Construct]
  review_log: []
triad:
  art: |
    The force of the sculptor's first strike, determining how deeply the chisel bites into the stone. It is raw vision made manifest, the initial shock that deforms reality before the patient work of shaping begins.
  law: |
    Intensity is the amplitude of the projected Observer's Shadow (A_Ψ) at the moment of a willed act's initiation (t=0). This amplitude directly determines the magnitude of the localized deformation of the temporal pressure potential (δV_Γ), thereby setting the initial gradient of the new Channel of Intent.
  philosophy: |
    Intensity is the bridge between pure ideation (Clarity) and sustained action (Persistence). It is the singular moment of commitment where a potential future is given enough weight to impress itself upon the present, demonstrating that the depth of one's conviction can physically alter the landscape of possibility.
pirouette_definition: |
  Intensity is the measure of amplitude for the Observer's Shadow when projected to create a Future Wound Channel. As the second stage of a willed act, following Clarity and preceding Persistence, it quantifies the initial impact of an intention upon the coherence manifold. Functionally, it is a measure of an agent's focused conviction, which determines the initial depth and gradient of the 'coherence well' impressed upon the local Pirouette Lagrangian. A high-intensity projection creates a significant, localized dip in the temporal pressure potential (V_Γ), making the willed action the new path of least resistance.
operational_definition:
  units: Dimensionless (normalized) or in units of Coherence (Kτ).
  symbol_table:
    - name: A_Ψ
      meaning: Amplitude of Observer's Shadow projection
      dimensions: Dimensionless
      default_range: "[0, 1]"
    - name: δV_Γ
      meaning: Localized change in Temporal Pressure Potential
      dimensions: Action (J·s)
      default_range: contextual
  measurement:
    procedures:
      - name: Channel Depth Inference
        outline: |
          Intensity is not measured directly but is inferred from its effect. Using Flow Diagnostics (DYNA-001), an agent's coherence manifold is mapped before and immediately after the initiation of a willed act. The depth (δV_Γ) and gradient (∇V_Γ) of the newly-carved Channel of Intent are calculated. Intensity (A_Ψ) is derived as the primary causal factor for this initial geometric change.
        expected_signals: [A sharp, localized drop in V_Γ potential, a corresponding spike in the local V_Γ gradient.]
        pitfalls: [Differentiating the effect of a single high-intensity projection from the cumulative effect of low-intensity, high-Persistence acts. Confounding with ambient manifold fluctuations.]
context_windows:
  - module: DOMA-197
    excerpt: |
      Intensity (The Projection): A coherent intent is projected into the manifold as a Future Wound Channel (CORE-011)—the geometric scar of an event that has not yet occurred. This "projected echo" is what actively deforms the local `V_Γ` landscape. Intensity is the amplitude of the Observer's Shadow that carves this channel, a function of focus and conviction. A high-intensity projection creates a deep coherence well, a steep gradient that makes the desired path almost irresistible.
  - module: DOMA-197
    excerpt: |
      Stagnant Will (Paralysis): The agent forms a coherent intent (the Seed) but cannot overcome the initial activation energy required to begin carving the path. The perceived slope of the default `V_Γ` landscape is too steep to climb. This represents a failure to generate sufficient Intensity to initiate the channel.
poetic_connections:
  motifs: [chisel strike, shockwave, imprint, depth, conviction, lightning flash]
  evocative_lines:
    - "The path forward is not found, but carved."
    - "...the solemn and terrifying right of the Weaver to pick up the chisel."
  association_matrix:
    - [ "OBSERVERS_SHADOW", 0.9 ]
    - [ "WOUND_CHANNEL", 0.8 ]
    - [ "CLARITY", 0.6 ]
    - [ "PERSISTENCE", 0.5 ]
formal_mappings:
  candidates:
    - target: Source term strength `J`
      domain: EFT
      mapping_kind: mathematical
      equation_hint: |
        L_int = J(x) * φ(x), where A_Ψ ~ max(|J(x, t=0)|)
      justification: |
        Intensity can be mapped to the strength of a source term (`J`) that couples to a system's dynamic field (`φ`). A high-intensity projection is analogous to a strong, localized source being 'switched on', which then dictates the subsequent evolution of the field by creating a deep potential well.
      references: []
      confidence: 0.4
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The initial depth of a Future Wound Channel is directly proportional to the Intensity of the projection, independent of its duration (Persistence)."
      domain: phenomenology
      falsifier: "Observation of systems where low-Intensity projections, held for an extremely short duration, produce deep channels, suggesting a non-linear or resonant effect is dominant over simple amplitude."
      status: proposed
      links: [DOMA-197, CORE-011]
naming_notes:
  collisions: [The symbol `I` is overloaded (current, inertia). Using `A_Ψ` (Amplitude of Shadow) is preferred for clarity.]
  disambiguation: |
    Distinguish from Persistence. Intensity is the initial amplitude of the projection at t=0, a "snapshot" measure. Persistence is the integral of that projection over time. A lightning strike has high Intensity and low Persistence; a slow river has low Intensity and high Persistence.
crosslinks:
  near_synonyms: []
  antonyms: [MANIFOLD_INERTIA]
  prerequisites: [CLARITY, OBSERVERS_SHADOW]
  downstream_effects: [WOUND_CHANNEL, PERSISTENCE]
license: CC-BY-SA-4.0
---

# Intensity

## Canonical (Pirouette)
Intensity is the measure of amplitude for the Observer's Shadow when projected to create a Future Wound Channel. As the second stage of a willed act, following Clarity and preceding Persistence, it quantifies the initial impact of an intention upon the coherence manifold. Functionally, it is a measure of an agent's focused conviction, which determines the initial depth and gradient of the 'coherence well' impressed upon the local Pirouette Lagrangian. A high-intensity projection creates a significant, localized dip in the temporal pressure potential (V_Γ), making the willed action the new path of least resistance.

## EFT-First Summary
Intensity maps to the strength of a localized source term (`J`) coupling to a system's dynamic field. A high-intensity act is analogous to a strong source momentarily imprinting a new potential well onto the system's landscape, altering its path of least action. This provides a formal hook for modeling willed acts within effective field theory frameworks. See [Formal Mappings](#formal_mappings).

## Glossary Links
- See also: [Clarity](...), [Persistence](...), [Observer's Shadow](...), [Wound Channel](...)