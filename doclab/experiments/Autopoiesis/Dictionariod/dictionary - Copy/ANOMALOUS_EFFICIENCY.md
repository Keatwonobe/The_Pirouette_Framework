---
term: "Anomalous Efficiency"
canonical_id: "ANOMALOUS_EFFICIENCY"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-157"]
---

---
term: Anomalous Efficiency
canonical_id: ANOMALOUS_EFFICIENCY
symbol: 
aliases: ["Injected Coherence", "Resonant Injection"]
parents: ['DOMA-157']
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-157
      lines: "L22-L24"
      snippet: |
        The Coherence Lens is an instrument designed to detect a specific pathology: **injected coherence**. It operates on the core principle that manipulation reveals itself through *anomalous efficiency*.
  editors: ['[auto-agent]']
  review_log: []
triad:
  art: |
    A whisper that starts an avalanche. A single, poisoned drop that muddies a river. A perfectly formed, synchronized wave with no visible splash.
  law: |
    The ratio of a narrative's systemic effect (Coherence Flux, ΔKτ) to the observable energy of its origin (Injection Pressure, Γ_inj) is anomalously high (`G_R >> 1`) for manipulated narratives compared to organic ones.
  philosophy: |
    Manipulation is not brute force; it is parasitic efficiency. It exploits pre-existing systemic vulnerabilities (Wound Channels) to achieve maximum effect with minimum effort, revealing its artifice not through its noise, but through its unnatural quietness.
pirouette_definition: |
  Anomalous Efficiency is the core diagnostic principle of the Coherence Lens, stating that inorganic, manipulated narratives are distinguished by a disproportionately large systemic impact (measured as Coherence Flux, ΔKτ) relative to the observable energy of their injection (Injection Pressure, Γ_inj). This high Resonant Gain (`G_R`) is the macroscopic signature of a narrative `Ki` engineered to exploit a system's pre-existing vulnerabilities (a Wound Channel), allowing it to follow a steep, low-cost geodesic to a new state of high coherence.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: G_R
      meaning: Resonant Gain; the primary measure of Anomalous Efficiency.
      dimensions: dimensionless
      default_range: "Organic < 1; Manipulated >> 1"
    - name: ΔKτ
      meaning: Coherence Flux; the measured increase in a narrative's phase-locking across multiple domains (the effect).
      dimensions: dimensionless
      default_range: contextual
    - name: Γ_inj
      meaning: Injection Pressure; a proxy for the energy, cost, and obscurity of a narrative's initial seed (the cause).
      dimensions: dimensionless
      default_range: contextual
  measurement:
    procedures:
      - name: Resonant Gain Analysis
        outline: |
          1. **Temporal Ingestion:** Ingest multi-source, high-frequency data streams.
          2. **Ki Pattern Extraction:** Identify dominant narrative patterns (`Ki`).
          3. **Coherence Flux Measurement (ΔKτ):** For each `Ki`, measure its degree of phase-locking across domains, triggered by a sudden Alchemical Union.
          4. **Injection Pressure Estimation (Γ_inj):** Trace the triggering narrative's provenance to its earliest seed and quantify its source obscurity, syndication, and amplification signals.
          5. **Gain Calculation:** Calculate `G_R = ΔKτ / Γ_inj` and flag if it exceeds a calibrated threshold.
        expected_signals: ["G_R >> 1", "Red Flag: Anomalous Gain Confirmed"]
        pitfalls: ["Mis-attributing the origin (underestimating Γ_inj)", "Confusing high organic virality with manipulation", "Poor calibration of the G_R threshold for a given domain"]
context_windows:
  - module: DOMA-157
    excerpt: |
      The Coherence Lens is an instrument designed to detect a specific pathology: **injected coherence**. It operates on the core principle that manipulation reveals itself through *anomalous efficiency*. A natural, organic story creates a turbulent splash proportional to its cause. A manipulated narrative often appears as a perfectly formed, unnaturally synchronized wave with no visible splash.
  - module: DOMA-157
    excerpt: |
      A managed narrative is a `Ki` pattern that has been deliberately shaped to align with a deep **Wound Channel (CORE-011)**... Such a system exists in a state of high potential, poised on a "coherence cliff edge." The manipulative act—a **Daedalus Gambit (DYNA-003)**—is a minimal energy nudge (`δΓ_inj`) that pushes the system over this edge. The high Resonant Gain is the macroscopic signature of a system that was engineered for this precise, efficient state transition.
poetic_connections:
  motifs: ["whisper vs. shout", "avalanche from a pebble", "ventriloquist's echo", "poisoned well"]
  evocative_lines:
    - "The chord is deafening, but no one can see the orchestra."
    - "A perfectly formed, unnaturally synchronized wave with no visible splash."
    - "...the difference between a song that arises organically from the crowd and one that is played by a hidden ventriloquist."
  association_matrix:
    - [ "RESONANT_GAIN", 0.9 ]
    - [ "WOUND_CHANNEL", 0.8 ]
    - [ "DAEDALUS_GAMBIT", 0.7 ]
    - [ "BRUTE_FORCE_PUSH", -0.9 ]
formal_mappings:
  candidates:
    - target: System transition from a metastable state
      domain: CM|Math
      mapping_kind: conceptual
      equation_hint: |
        ΔE_released >> E_activation
      justification: |
        A system with a Wound Channel is analogous to a system in a metastable state (e.g., a ball atop a hill). The manipulative injection is the small activation energy (a nudge) required to overcome the potential barrier, causing a transition to a more stable state and releasing a large amount of stored potential energy. The Anomalous Efficiency is the large ratio of released energy (the narrative's impact) to the small activation energy (the injection).
      references:
        - title: Classical Mechanics
          where: "Chapter on Potential Energy and Stability"
          date: 
      confidence: 0.6
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "Narratives flagged with `Red Flag: Anomalous Gain Confirmed` will consistently trace back to a coordinated, non-organic origin point upon forensic investigation."
      domain: phenomenology
      falsifier: "A significant population of red-flagged narratives are found to have genuinely organic, distributed origins, indicating that G_R is a poor discriminator that mistakes natural virality for manipulation."
      status: proposed
      links: ['DOMA-157']
naming_notes:
  collisions: ["η (Thermodynamic efficiency)"]
  disambiguation: |
    Anomalous Efficiency should not be confused with high organic virality. Virality implies rapid, broad propagation but does not inherently mean a disproportionate effect-to-origin energy ratio; a genuinely popular idea can be a 'loud' origin. Anomalous Efficiency specifically describes events that are 'loud' in effect but suspiciously 'quiet' at their source.
crosslinks:
  near_synonyms: [RESONANT_GAIN]
  antonyms: [BRUTE_FORCE_PUSH]
  prerequisites: [COHERENCE_LENS, WOUND_CHANNEL]
  downstream_effects: [DAEDALUS_GAMBIT, MANAGED_NARRATIVE_CHANNEL]
license: CC-BY-SA-4.0
---