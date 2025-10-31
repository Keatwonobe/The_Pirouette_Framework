---
term: "Resonant Concordance"
canonical_id: "RESONANT_CONCORDANCE"
symbol: ""
aliases: [Macro-Ki]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-154"]
---

---
term: Resonant Concordance
canonical_id: RESONANT_CONCORDANCE
symbol: Ki_M
aliases: [Macro-Ki]
parents: [CORE-014, DYNA-001]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-154
      lines: "L63-L67"
      snippet: |
        The final output is the **Coherence Tapestry**: a multi-layered, time-series visualization that transforms a static measure into a dynamic narrative of systemic influence. It reveals: Periods of High Resonance... Phase Leads and Lags... Resonance Breaks...
  editors: [System Agent]
  review_log: []
triad:
  art: |
    The universe plays the same song on different instruments. A Resonant Concordance is the act of hearing that symphony—the tremor in the market and the fever in the heart as harmonics of a single, fundamental note.
  law: |
    A Resonant Concordance is confirmed when the Phase-Locking Value (PLV) between two or more normalized, cross-domain time-series exceeds a pre-defined significance threshold (e.g., >0.8) at a shared, persistent resonant frequency. Absence of a significant PLV peak falsifies the claim of concordance.
  philosophy: |
    This instrument makes the invisible architecture of systemic causality visible. It demonstrates that disparate domains are not isolated but are sections of a single orchestra, forced by a shared pressure to navigate the same macro-geodesic, revealing a unified, underlying reality.
pirouette_definition: |
  A single, shared resonant pattern or phase-synchronized rhythm (an emergent Macro-Ki) that manifests across multiple, disparate domains. It is the empirical signature that multiple systems, under a shared Temporal Pressure (Macro-Γ), have coupled their behavior and are traversing the same path of least resistance (a macro-geodesic) on a higher-order manifold.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: Ki_M
      meaning: Resonant Concordance, quantified as the degree of cross-domain phase synchronization.
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: PLV
      meaning: Phase-Locking Value; a direct measure of Ki_M.
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: ωk
      meaning: Shared resonant frequency at which domains are synchronized.
      dimensions: T⁻¹
      default_range: contextual
    - name: φk
      meaning: Shared phase angle at the resonant frequency.
      dimensions: dimensionless
      default_range: "[0, 2π]"
  measurement:
    procedures:
      - name: Cross-Domain Resonance Analysis
        outline: |
          1. **Domain Selection**: Select 2+ conceptually distant domains (e.g., economics, public health, social media sentiment).
          2. **Variable Normalization**: Translate primary metrics from each domain into framework universals (e.g., market volatility → Γ, public health response → Kτ).
          3. **Resonance Detection**: Perform cross-spectral analysis on the normalized time-series to identify a shared peak frequency (ωk). Calculate the Phase-Locking Value (PLV) at ωk to quantify synchronization strength.
          4. **Synthesis**: Visualize results as a Coherence Tapestry, mapping PLV over time and plotting phase lags to determine causal direction.
        expected_signals: [A statistically significant PLV peak (>0.8) at a common frequency ωk, Stable phase-lag relationships between domains]
        pitfalls: [Mistaking amplitude correlation for phase-locking, Insufficient time-series length for robust spectral analysis, Improper domain variable normalization leading to spurious signals]
context_windows:
  - module: DOMA-154
    excerpt: |
      The universe does not invent new laws for every domain; it plays the same song on different instruments. The economy, the ecosystem, and the collective psyche are not separate entities; they are different sections of the same orchestra. Therefore, a pervasive, large-scale Temporal Pressure (a **Macro-Γ**) will not produce isolated effects. It will induce a corresponding, large-scale resonant solution that ripples through all affected domains.
  - module: CORE-006
    excerpt: |
      The discovery of a strong Resonant Concordance is a profound physical statement. According to the Pirouette Lagrangian, each system follows the geodesic—the path of maximal coherence—on its local manifold. When this instrument detects a shared resonance, it has found empirical evidence that these disparate systems are navigating the *same **macro-geodesic***.
poetic_connections:
  motifs: [symphony, tapestry, fractal, rhythm, echo, tidal, puppeteer]
  evocative_lines:
    - "a tuning fork for reality itself"
    - "hearing the symphony in the noise"
    - "the tremor in the market can be the same tremor in the heart"
    - "they are all flowing downhill along the same cosmic contour"
  association_matrix:
    - [ "TEMPORAL_PRESSURE", 0.9 ]
    - [ "FRACTAL_BRIDGE", 0.8 ]
    - [ "COHERENCE", 0.6 ]
    - [ "GEODESIC", 0.7 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Kuramoto model of coupled oscillators
      domain: Math|CM
      mapping_kind: conceptual|operational
      equation_hint: |
        dθᵢ/dt = ωᵢ + (K/N) Σⱼ sin(θⱼ - θᵢ)
      justification: |
        The Kuramoto model describes how a population of independent oscillators (domains) can spontaneously lock into a common phase when their coupling strength (driven by Macro-Γ) exceeds a critical threshold. A Resonant Concordance (Ki_M) is the macro-scale observation of this synchronized state, and the PLV is its direct measurement.
      references:
        - title: Sync: The Emerging Science of Spontaneous Order
          where: Strogatz, S. (2003)
          date: 2003-01-01
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "The detection of a strong Resonant Concordance (PLV > 0.8) between two domains implies they are responding to a shared causal driver (a Macro-Γ), not a direct peer-to-peer causal link."
      domain: phenomenology
      falsifier: "Demonstrate a recurring high PLV between two domains where a direct, confounding causal link is proven, and no shared third driver can be identified. Alternatively, show that high PLV values appear frequently in phase-randomized surrogate data, indicating statistical insignificance."
      status: proposed
      links: [DOMA-154, CORE-014]
naming_notes:
  collisions: [Resonance (physics), Ki (general coherence symbol)]
  disambiguation: |
    Resonant Concordance (or Macro-Ki) is a *macro-scale, cross-domain* phenomenon. It is distinct from local resonance within a single system. It describes the synchronization *of* multiple local systems, each with their own internal Coherence (Kτ), into a single, phase-locked rhythm.
crosslinks:
  near_synonyms: [MACRO_KI]
  antonyms: [SYSTEMIC_DECOUPLING, DOMAIN_ISOLATION]
  prerequisites: [TEMPORAL_PRESSURE, FRACTAL_BRIDGE, COHERENCE]
  downstream_effects: [COHERENCE_TAPESTRY, MACRO_GEODESIC]
license: CC-BY-SA-4.0
---

# Resonant Concordance

## Canonical (Pirouette)
A Resonant Concordance is a single, shared resonant pattern or phase-synchronized rhythm (an emergent Macro-Ki) that manifests across multiple, disparate domains. It is the empirical signature that multiple systems, under a shared Temporal Pressure (Macro-Γ), have coupled their behavior and are traversing the same path of least resistance (a macro-geodesic) on a higher-order manifold.

## EFT-First Summary
Operationally, a Resonant Concordance is an observed instance of large-scale phase synchronization among weakly coupled oscillators, as described by the Kuramoto model. Disparate domains (e.g., finance, public health) are treated as oscillators whose phases (normalized behaviors) lock together under a common driving force. The strength of this concordance is measured by the Phase-Locking Value (PLV), a dimensionless metric from 0 (uncoupled) to 1 (perfectly synchronized). See Strogatz, S. (2003), *Sync*.

## Glossary Links
- See also: [Temporal Pressure](link), [Fractal Bridge](link), [Coherence](link), [Coherence Tapestry](link)