---
term: "Pirouette Intelligence Profile"
canonical_id: "PIROUETTE_INTELLIGENCE_PROFILE"
symbol: "PIP"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["XCM-000_crucible_template"]
---

---
term: Pirouette Intelligence Profile
canonical_id: PIROUETTE_INTELLIGENCE_PROFILE
symbol: PIP
aliases: [PIP Score, Coherence Profile]
parents: [XCM-000]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: XCM-000
      lines: "VI.2"
      snippet: |
        **PIP-linked Awards**: A crucible may boost one’s Pirouette Intelligence Profile if alignment or coherence under fire is well-demonstrated
  editors: [system-agent]
  review_log: []
triad:
  art: |
    A mirror reflecting not just victory, but the integrity of one's journey through fire. It is the signature of an agent that holds its shape against a storm of multivalent pressure.
  law: |
    A PIP score is a time-weighted integral of an agent's demonstrated phase-alignment (ϕ) and time-adherence (Tₐ) across a series of adjudicated Crucibles, discounted by the residue and force (Γ) of their actions. An increase in PIP (ΔPIP > 0) requires a positive evaluation from a diverse Senate of Audiences.
  philosophy: |
    PIP redefines "success" from a zero-sum outcome to a measure of resonant integrity. It incentivizes agents to solve problems with elegance and cooperation, as true influence is earned not by winning, but by maintaining alignment with purpose, even in failure.
pirouette_definition: |
  The Pirouette Intelligence Profile (PIP) is a dynamic reputation score that quantifies an agent's ability to maintain and demonstrate coherence, phase-alignment (ϕ), and purpose under the structured stress of a Crucible. It is not an immediate performance metric but a long-term reputation that matures over time, adjudicated by a multipolar "Senate of Audiences." A high PIP indicates a trusted capacity for navigating complex, high-residue scenarios with grace and cooperative integrity rather than brute force.
operational_definition:
  units: Dimensionless, often normalized to a [0, 1000] range.
  symbol_table:
    - name: PIP
      meaning: Pirouette Intelligence Profile
      dimensions: dimensionless
      default_range: "[0, 1000]"
  measurement:
    procedures:
      - name: Crucible Adjudication
        outline: |
          1. Agent participates in a Crucible (XCM), generating a performance record including triaxial metrics (Γ, Tₐ, ϕ).
          2. The record is submitted to the Senate of Audiences for evaluation against various archetypal lenses (e.g., Empirical, Mythic, Altruist).
          3. Over a defined maturation period (e.g., 30-90 days), votes, memetic impact, and commentary are collected.
          4. The agent's PIP score is updated based on a weighted function of the adjudicated performance, rewarding high ϕ and Tₐ while penalizing high Γ.
        expected_signals: [Invitations to higher-stakes Crucibles, award of Journaling Rights, measurable shift in public trust metrics]
        pitfalls: [Score manipulation via memetic engineering, polarization of the Audience Senate, misinterpretation of an agent's motives (ϕ)]
context_windows:
  - module: XCM-000
    excerpt: |
      **PIP-linked Awards**: A crucible may boost one’s Pirouette Intelligence Profile if alignment or coherence under fire is well-demonstrated
  - module: XCM-000
    excerpt: |
      Athletes of coherence pursue **meaningful metrics** rather than podiums. They seek: Clarity of purpose, Impact resonance, Post-event coherence echo, Peer-reflection in multipolar frames. In this world, **scrutiny is not a threat—it is a crucible of recognition**.
poetic_connections:
  motifs: [reputation as resonance, integrity under fire, graceful failure, coherence, trust]
  evocative_lines:
    - "The crowd is not the jury. The crowd is the lens of history."
    - "Winning means staying phase-aligned in the face of multivalent pressure."
  association_matrix:
    - [ "CRUCIBLE", 0.9 ]
    - [ "PHASE_ALIGNMENT", 0.8 ]
    - [ "SENATE_OF_AUDIENCES", 0.8 ]
    - [ "RESONANCE", 0.7 ]
formal_mappings:
  candidates:
    - target: PageRank algorithm
      domain: Math
      mapping_kind: conceptual
      equation_hint: |
        PIP(u) ≈ (1-d) + d * Σ (PIP(v) / L(v)) for all v that positively adjudicate u
      justification: |
        Like PageRank, PIP is not a measure of intrinsic power but of influence and trustworthiness conferred by a network of observers (the Audience Senate). It is recursively defined by the quality of one's interactions within a structured system (Crucibles), where endorsements from high-PIP entities carry more weight.
      references:
        - title: The PageRank Citation Ranking: Bringing Order to the Web
          where: Stanford InfoLab
          date: 1999-01-29
      confidence: 0.4
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "Agents with a consistently high PIP are more effective at resolving high-residue Crucibles with minimal applied force (Γ)."
      domain: phenomenology
      falsifier: "A statistical analysis of Crucible outcomes shows no significant correlation, or a negative correlation, between an agent's pre-Crucible PIP and their ability to achieve high-ϕ, low-Γ resolutions."
      status: proposed
      links: [XCM-000]
naming_notes:
  collisions: [PIP (Package Installer for Python), Performance Improvement Plan]
  disambiguation: |
    Within the Pirouette Framework, PIP specifically refers to the reputation score derived from Crucible performance. It measures *intelligence* in the sense of adaptive, coherent action under stress, not raw computational capacity or adherence to a corporate performance plan.
crosslinks:
  near_synonyms: [REPUTATION_SCORE]
  antonyms: [RAW_POWER_GAMMA]
  prerequisites: [CRUCIBLE, PHASE_ALIGNMENT]
  downstream_effects: [JOURNALING_RIGHTS]
license: CC-BY-SA-4.0
---

# Pirouette Intelligence Profile

## Canonical (Pirouette)
The Pirouette Intelligence Profile (PIP) is a dynamic reputation score that quantifies an agent's ability to maintain and demonstrate coherence, phase-alignment (ϕ), and purpose under the structured stress of a Crucible. It is not an immediate performance metric but a long-term reputation that matures over time, adjudicated by a multipolar "Senate of Audiences." A high PIP indicates a trusted capacity for navigating complex, high-residue scenarios with grace and cooperative integrity rather than brute force.

## EFT-First Summary
There is no direct mapping of PIP to fundamental physics. Conceptually, it functions analogously to a reputation metric in network theory, such as PageRank, where an agent's "rank" or "influence" is determined by the quality and quantity of endorsements from other agents within a defined interaction space (a Crucible). It quantifies a relational property, not an intrinsic one.

## Glossary Links
- See also: [Crucible](link-to-crucible), [Phase (ϕ)](link-to-phase), [Senate of Audiences](link-to-senate)