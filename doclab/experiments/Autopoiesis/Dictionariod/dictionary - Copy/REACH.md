---
term: "Reach"
canonical_id: "REACH"
symbol: "ρ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-019"]
---

---
term: Reach
canonical_id: REACH
symbol: ρ
aliases: [Scope (S)]
parents: [DOMA-019]
children: [INST-GOV-001_placeholder]
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-019
      snippet: |
        | Old Term | New Pirouette Term | Mapping Question |
        | :--- | :--- | :--- |
        | Scope (S) | **Reach (ρ)** | How many nested systems will the resulting turbulence propagate to? |
  editors: [system]
  review_log: []
triad:
  art: |
    An action is a stone dropped into a nested series of ponds. Reach measures not the size of the stone, but how many distinct ponds its ripples will cross before they fade.
  law: |
    Reach (ρ) is a normalized (0–1) measure of the count of distinct, nested systems whose core dynamics are predicted to be perturbed above a baseline coherence threshold by the turbulence originating from a single action.
  philosophy: |
    Reach operationalizes the ethical principle of radical interconnectedness. It asserts that an action's moral weight is not confined to its immediate target but extends to the entire web of systems it perturbs, obliging the actor to consider the full "blast radius" of their choice.
pirouette_definition: |
  Reach (ρ) is a core component of Coherence Risk (R_κ) that quantifies the propagation of an action's turbulence. It measures the number of distinct, nested systems whose core dynamics will be consequentially affected by the action, thereby assessing the breadth of its impact across the coherence manifold. It is the geometric parameter for systemic scope.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: ρ
      meaning: Reach
      dimensions: dimensionless
      default_range: "[0, 1]"
  measurement:
    procedures:
      - name: Systemic Propagation Simulation
        outline: |
          1. Model the action as a localized perturbation (e.g., energy/information injection) within a graph of interconnected systems.
          2. Propagate the perturbation's effects through the system graph according to the governing dynamics and coupling strengths.
          3. Count the number of systems (N_affected) where the perturbation exceeds a pre-defined coherence degradation threshold (e.g., ΔKi > ε).
          4. Normalize this count against a contextual maximum (e.g., the total number of accessible systems, N_total) to yield ρ.
        expected_signals: [Cross-system coherence degradation, Dissonance cascades, Resonance chain-reactions]
        pitfalls: [Underestimation of weak or long-range couplings, Misidentification of system boundaries, Failure to account for non-linear amplification]
context_windows:
  - module: DOMA-019
    excerpt: |
      To map this geometry, we translate the old risk parameters into their true, dynamic forms:

      | Old Term | New Pirouette Term | Mapping Question |
      | :--- | :--- | :--- |
      | Scope (S) | **Reach (ρ)** | How many nested systems will the resulting turbulence propagate to? |
      | Magnitude (M) | **Dissonance (δ)** | How severely will the action disrupt a target system's core resonant pattern (Ki)? |
      | Irreversibility (I) | **Wound Channel Depth (ω)** | How deeply and permanently will the action scar a system's memory and identity...? |
  - module: DOMA-019
    excerpt: |
      Coherence Risk is a predictive metric (0–1 scale) that estimates the potential degradation of a system's health... It is a weighted function of the three core geometric factors:

      $$ R_κ = w_ρ ρ + w_δ δ + w_ω ω $$

      Where **ρ**, **δ**, and **ω** are normalized scores (0-1) and **w** are the currently calibrated weights for Reach, Dissonance, and Wound Channel Depth.
poetic_connections:
  motifs: [ripple, echo, contagion, blast radius, propagation, network]
  evocative_lines:
    - "How many nested systems will the resulting turbulence propagate to?"
    - "Every choice we make becomes a permanent feature of the landscape upon which others must walk."
  association_matrix:
    - [ "DISSONANCE", 0.8 ]
    - [ "WOUND_CHANNEL_DEPTH", 0.8 ]
    - [ "COHERENCE_RISK", 0.9 ]
formal_mappings:
  candidates:
    - target: Influence Domain / Propagation Radius
      domain: Network Science
      mapping_kind: operational
      justification: |
        Reach measures the number of nodes (systems) in a complex network whose state is significantly perturbed by an initial change at a source node. This is directly analogous to measuring the size of the "influence domain" or the propagation radius of a signal or shock within network science and contagion models. It quantifies the extent of a perturbation's spread.
      confidence: 0.9
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The Reach (ρ) of an action is primarily determined by the topological connectivity and resonance properties of the affected systems, not the initial energy of the action itself."
      domain: phenomenology
      falsifier: "Demonstrate that two actions with identical turbulence profiles injected into systems with identical topology result in vastly different ρ values. This would imply that a property of the action other than its turbulence geometry is the dominant factor."
      status: proposed
      links: [DOMA-019]
naming_notes:
  collisions: [The symbol ρ is standard for mass/charge density in physics.]
  disambiguation: |
    In Pirouette, ρ refers to the topological breadth of an action's impact across a count of discrete systems. It is a dimensionless, normalized count, not a physical density (mass/volume). Context is usually Coherence Risk (R_κ) calculation.
crosslinks:
  near_synonyms: [SCOPE]
  antonyms: [LOCALITY, CONTAINMENT]
  prerequisites: [SYSTEM, COHERENCE_MANIFOLD]
  downstream_effects: [COHERENCE_RISK, THE_CRUCIBLE]
license: CC-BY-SA-4.0
---

# Reach

## Canonical (Pirouette)
Reach (ρ) is a core component of Coherence Risk (R_κ) that quantifies the propagation of an action's turbulence. It measures the number of distinct, nested systems whose core dynamics will be consequentially affected by the action, thereby assessing the breadth of its impact across the coherence manifold. It is the geometric parameter for systemic scope.

## EFT-First Summary
In network science terms, an action's Reach (ρ) is its influence domain. It quantifies the number of distinct systems (nodes) whose dynamics are perturbed by the propagation of the action's initial turbulence. It measures the breadth of consequence, distinct from its severity (Dissonance) or permanence (Wound Channel Depth).

## Glossary Links
- See also: [Coherence Risk](<COHERENCE_RISK>), [Dissonance](<DISSONANCE>), [Wound Channel Depth](<WOUND_CHANNEL_DEPTH>)