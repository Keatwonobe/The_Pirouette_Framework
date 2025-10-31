---
term: "Resonant Gain"
canonical_id: "RESONANT_GAIN"
symbol: "G_R"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-157"]
---

---
term: Resonant Gain
canonical_id: RESONANT_GAIN
symbol: G_R
aliases: []
parents: [DOMA-157, DYNA-003, CORE-011]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-157
      lines: "L63-L75"
      snippet: |
        To quantify this, we define the central observable as **Resonant Gain (G_R)**. It is the ratio of the observed systemic effect to the estimated energy of the input signal.

        *   **Coherence Flux (ΔKτ):** The *effect*. This is the measured increase in a narrative's coherence across multiple domains—its phase-locking between news, social media, and market activity. It is the size of the resulting avalanche.
        *   **Injection Pressure (Γ_inj):** The *cause*. This is a proxy for the energy and cost of the initial seed—the obscurity of the source, the concentration of initial reports, the novelty of the signal, and the presence of astroturfed amplification. It is the size of the initial whisper.

        The core diagnostic equation is: **G_R = ΔKτ / Γ_inj**
  editors: [system-agent]
  review_log: []
triad:
  art: |
    The chord is deafening, but no one can see the orchestra. It is the measure of a whisper that starts an avalanche.
  law: |
    A Resonant Gain (G_R) significantly greater than 1, calculated as the ratio of emergent Coherence Flux (ΔKτ) to estimated Injection Pressure (Γ_inj), is the primary indicator of anomalous efficiency and likely narrative manipulation.
  philosophy: |
    The framework must distinguish a system's native coherence from injected, pathological coherence. Resonant Gain provides the instrument for this discernment, measuring not just the effect of a narrative, but the suspicious efficiency of its cause, thereby guarding against hidden ventriloquists.
pirouette_definition: |
  The dimensionless ratio of a narrative's emergent Coherence Flux (ΔKτ) to the estimated Injection Pressure (Γ_inj) of its seed. It quantifies the efficiency with which a narrative `Ki` converts injection energy into systemic, cross-domain resonance. Anomalously high values (G_R >> 1) are a primary indicator of a managed narrative exploiting a pre-existing Coherence Cliff.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: G_R
      meaning: Resonant Gain
      dimensions: dimensionless
      default_range: "[0, ∞), with G_R >> 1 being anomalous"
    - name: ΔKτ
      meaning: Coherence Flux; the systemic impact or effect.
      dimensions: dimensionless (proxy for coherence)
      default_range: contextual
    - name: Γ_inj
      meaning: Injection Pressure; the estimated energy/cost of the seed event or cause.
      dimensions: dimensionless (proxy for energy)
      default_range: contextual
  measurement:
    procedures:
      - name: Coherence Lens Diagnostic Workflow
        outline: |
          1. Ingest high-frequency, multi-source data streams.
          2. Extract dominant narrative patterns (`Ki` clusters).
          3. For a target `Ki`, measure the change in its cross-domain phase-locking (Alchemical Union) to quantify Coherence Flux (ΔKτ).
          4. Trace the `Ki` to its earliest seed event and assess proxies for effort (e.g., source obscurity, syndication concentration, astroturfing) to estimate Injection Pressure (Γ_inj).
          5. Calculate the ratio G_R = ΔKτ / Γ_inj and compare against a domain-calibrated threshold.
        expected_signals: [Coherence Spike, Cross-Domain Entrainment, Anomalous Gain Confirmed]
        pitfalls: [Misattribution of Γ_inj (a quiet but influential source is not necessarily low-energy), difficulty in calibrating baseline G_R for a given information ecosystem, confounding organic "black swan" events with manipulated ones.]
context_windows:
  - module: DOMA-157
    excerpt: |
      A high Resonant Gain suggests that a powerful, coherent effect was achieved with suspiciously little visible effort, pointing toward an efficient, pre-planned, and likely inorganic origin.
  - module: DOMA-157
    excerpt: |
      The manipulative act—a Daedalus Gambit (DYNA-003)—is a minimal energy nudge (δΓ_inj) that pushes the system over this edge. The system then rapidly follows a steep geodesic toward a state of much higher coherence (Kτ), releasing a cascade of stored potential energy. The high Resonant Gain is the macroscopic signature of a system that was engineered for this precise, efficient state transition.
poetic_connections:
  motifs: [tuning fork, hidden orchestra, avalanche from a whisper, coherence cliff]
  evocative_lines:
    - "...detecting the whispers that start avalanches."
    - "The chord is deafening, but no one can see the orchestra."
  association_matrix:
    - [ "DAEDALUS_GAMBIT", 0.9 ]
    - [ "COHERENCE_FLUX", 0.8 ]
    - [ "INJECTION_PRESSURE", 0.8 ]
    - [ "WOUND_CHANNEL", 0.7 ]
formal_mappings:
  candidates:
    - target: Gain (G)
      domain: Control Theory
      mapping_kind: operational
      equation_hint: |
        G = Output / Input
      justification: |
        G_R measures the amplification of a small input signal (Γ_inj) into a large systemic output (ΔKτ), analogous to how electronic or mechanical gain measures the ratio of output to input. A high gain indicates the system is operating near a resonance or has strong positive feedback, a core feature of the high-G_R phenomenon.
      references:
        - title: Feedback Control of Dynamic Systems
          where: "Chapter 4: Basic Properties of Feedback"
          date: 2010-01-01
      confidence: 0.8
  adopted:
    - target: Gain (G) in Control Theory
      rationale: The mapping is a direct operational analogy, providing a robust, well-understood formal basis for the concept of anomalous efficiency.
      confidence: 0.8
constraints_and_falsifiers:
  claims:
    - statement: "A narrative event with a verifiably high G_R is more likely to be of inorganic, manipulated origin than a low G_R event of similar systemic impact (ΔKτ)."
      domain: phenomenology
      falsifier: "The discovery of a class of naturally occurring, organic narratives that consistently produce G_R >> 1 without any evidence of pre-planning or exploitation of system vulnerabilities. This would invalidate G_R as a unique indicator of manipulation."
      status: proposed
      links: [DOMA-157]
naming_notes:
  collisions: [Gain (general electronics/signal processing)]
  disambiguation: |
    Resonant Gain must be distinguished from simple 'virality' or 'engagement'. Virality measures only the effect (proxied by ΔKτ), while G_R is a ratio of effect to *cause* (ΔKτ / Γ_inj). A high-budget advertising campaign may go viral but will have a low G_R due to its massive, overt Γ_inj.
crosslinks:
  near_synonyms: [ANOMALOUS_EFFICIENCY]
  antonyms: [BRUTE_FORCE_PUSH]
  prerequisites: [COHERENCE_FLUX, INJECTION_PRESSURE, KI]
  downstream_effects: [MANAGED_NARRATIVE_CHANNEL, DAEDALUS_GAMBIT]
license: CC-BY-SA-4.0
---

# Resonant Gain

## Canonical (Pirouette)
The dimensionless ratio of a narrative's emergent Coherence Flux (ΔKτ) to the estimated Injection Pressure (Γ_inj) of its seed. It quantifies the efficiency with which a narrative `Ki` converts injection energy into systemic, cross-domain resonance. Anomalously high values (G_R >> 1) are a primary indicator of a managed narrative exploiting a pre-existing Coherence Cliff.

## Control Theory Analogy
Resonant Gain (G_R) is operationally equivalent to gain in a signal amplifier or control system, where G = Output / Input. Here, a small input signal (Injection Pressure, Γ_inj) drives a disproportionately large system response (Coherence Flux, ΔKτ). A high gain indicates the system is operating near a resonance or has strong positive feedback, which in the Pirouette framework corresponds to a narrative exploiting a Wound Channel.

## Glossary Links
- See also: [Coherence Flux](<#>), [Injection Pressure](<#>), [Managed Narrative Channel](<#>), [Daedalus Gambit](<#>)