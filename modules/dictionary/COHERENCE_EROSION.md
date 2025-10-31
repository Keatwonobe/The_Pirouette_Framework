---
term: "Coherence Erosion"
canonical_id: "COHERENCE_EROSION"
symbol: ""
aliases: [The Fraying Thread]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-040"]
---

---
term: Coherence Erosion
canonical_id: COHERENCE_EROSION
symbol: 
aliases: ["The Fraying Thread"]
parents: [DOMA-040]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-040
      snippet: |
        3. **Coherence Erosion (The Fraying Thread):**
            *   **Description:** The slow degradation of the organization's core identity and memory. The patterns that once ensured success begin to fray and dissolve. It is the quiet death of forgetting.
  editors: ["system-agent"]
  review_log: []
triad:
  art: |
    The house slowly forgets its own shape. Foundations crack not from a single blow, but from a thousand days of rain and neglect, until the memory of what it was meant to be is lost.
  law: |
    An organization's rate of coherence loss is directly proportional to the rate of institutional knowledge decay and inversely proportional to the rate of investment in core identity reinforcement. Left unaddressed, this leads to a monotonic decrease in market resonance over time.
  philosophy: |
    Erosion is the most insidious pathology because it lacks the crisis of Fever or the paralysis of Atrophy. It is the quiet entropy of success, where the patterns that created stability become fragile through inattention. Its purpose is to remind us that coherence is not a one-time achievement but a continuous, living practice of remembering and reinforcing what matters.
pirouette_definition: |
  A systemic pathology of organizational flow characterized by the gradual, often imperceptible degradation of core identity, institutional memory, and operational patterns. It manifests as a fraying of the coherent structures that define the organization's value proposition and culture, leading to a slow decline in performance and relevance. It represents a loss of Temporal Coherence (Kτ) not through friction (Fever) or blockage (Atrophy), but through the decay of the channels themselves.
operational_definition:
  units: Dimensionless rate of decay (e.g., % per fiscal quarter)
  symbol_table:
    - name: ε_c
      meaning: Rate of Coherence Erosion
      dimensions: T⁻¹
      default_range: 0.001 to 0.1
  measurement:
    procedures:
      - name: Brand Resonance Decay Audit
        outline: |
          Longitudinal sentiment analysis of public brand mentions and customer feedback. Track the semantic distance between brand-aspirational keywords (e.g., 'innovative', 'reliable') and actual customer language over N quarters. A widening distance indicates erosion.
        expected_signals: ["Decreasing positive keyword association", "Increasing mentions of legacy/outdated features", "Shift in customer demographic to older, less engaged cohorts"]
        pitfalls: ["Confounding effects from short-term PR crises", "Sentiment analysis tools misinterpreting industry jargon"]
      - name: Institutional Knowledge Half-life
        outline: |
          Map critical, undocumented processes to key senior employees. Measure the rate of attrition for this group ('key-holder attrition'). The inverse of this rate, weighted by process criticality, serves as a proxy for the half-life of institutional knowledge.
        expected_signals: ["High 'bus factor' on critical projects", "Repeated 'rediscovery' of solved problems", "Increasing onboarding time for new hires in senior roles"]
        pitfalls: ["Difficult to accurately map undocumented knowledge", "Attrition may be due to market-wide factors, not internal decay"]
context_windows:
  - module: DOMA-040
    excerpt: |
      **Coherence Erosion (The Fraying Thread):** The slow degradation of the organization's core identity and memory. The patterns that once ensured success begin to fray and dissolve. It is the quiet death of forgetting. Manifestations: Brand decay and loss of market resonance; a slow but steady loss of market share; the departure of key employees and the institutional knowledge they hold.
  - module: DOMA-040
    excerpt: |
      To resolve **Erosion (Decay)**, the lever is an act of "channel reinforcement"—reinvesting in the core brand, creating mentorship programs, or codifying founding values.
poetic_connections:
  motifs: ["forgetting", "fraying", "fading", "rust", "decay", "ghosts in the machine"]
  evocative_lines:
    - "It is the quiet death of forgetting."
    - "The balance sheet is a photograph of where the river was."
  association_matrix:
    - [ "Temporal Coherence", 0.9 ]
    - [ "Laminar Flow", 0.7 ]
    - [ "Coherence Atrophy", 0.2 ]
    - [ "Coherence Fever", 0.2 ]
formal_mappings:
  candidates:
    - target: Material fatigue / stress corrosion cracking
      domain: CM
      mapping_kind: conceptual
      justification: |
        Erosion is analogous to material fatigue, where repeated, low-level stresses (e.g., minor process failures, employee turnover) don't cause immediate failure but gradually introduce micro-fractures in the organizational structure, eventually leading to systemic weakness and failure.
      references: []
      confidence: 0.8
    - target: Second law of thermodynamics / Entropy (S)
      domain: SM
      mapping_kind: conceptual
      justification: |
        Coherence Erosion maps to the concept of entropy in a closed or neglected system. The organization's 'information' and 'structure' (negentropy) naturally decay over time without active energy input ('channel reinforcement') to maintain order.
      references: []
      confidence: 0.7
  adopted:
    - target: Material fatigue
      rationale: |
        The analogy to material fatigue is operationally potent. It frames erosion not as a passive, thermodynamic inevitability (entropy) but as an active process of structural degradation from accumulated micro-damages, which can be monitored (via 'non-destructive testing' like audits) and mitigated (via 'reinforcement').
      confidence: 0.8
constraints_and_falsifiers:
  claims:
    - statement: "Organizations with high rates of undocumented-knowledge-holder attrition will exhibit a corresponding decline in product innovation and quality metrics within 2-3 fiscal years."
      domain: phenomenology
      falsifier: "A study of N companies shows no significant correlation between key-employee turnover and subsequent innovation output (e.g., patent filings, R&D ROI), suggesting knowledge is successfully encoded in systems or that new hires bring more innovative potential."
      status: proposed
      links: [DOMA-040]
naming_notes:
  collisions: ["Soil erosion", "Data erosion"]
  disambiguation: |
    Coherence Erosion is distinct from **Coherence Atrophy**. Atrophy is a blockage *in* a healthy channel, causing flow to stop. Erosion is the decay *of* the channel itself, making flow weak, leaky, and ineffective. Atrophy is an acute problem of 'stuckness'; Erosion is a chronic problem of 'weakness'.
crosslinks:
  near_synonyms: ["Institutional Decay", "Brand Dilution"]
  antonyms: ["Channel Reinforcement", "Coherence Weaving"]
  prerequisites: [COHERENCE, LAMINAR_FLOW]
  downstream_effects: [LOSS_OF_MARKET_SHARE, DECREASED_TEMPORAL_COHERENCE]
license: CC-BY-SA-4.0
---

# Coherence Erosion

## Canonical (Pirouette)
A systemic pathology of organizational flow characterized by the gradual, often imperceptible degradation of core identity, institutional memory, and operational patterns. It manifests as a fraying of the coherent structures that define the organization's value proposition and culture, leading to a slow decline in performance and relevance. It represents a loss of Temporal Coherence (Kτ) not through friction (Fever) or blockage (Atrophy), but through the decay of the channels themselves.

## Physics-First Summary
Operationally, Coherence Erosion is modeled as a form of organizational material fatigue. The 'structure' of the firm—its processes, culture, and brand identity—accumulates micro-damage from the stress of employee turnover, market shifts, and neglected maintenance. While no single event is catastrophic, their accumulation degrades the system's integrity, reducing its capacity to transmit value efficiently, analogous to how repeated stress weakens a physical material, leading to eventual failure.

## Glossary Links
- See also: Coherence Atrophy, Coherence Fever, Temporal Coherence, Channel Reinforcement