---
term: "Manipulation"
canonical_id: "MANIPULATION"
symbol: ""
aliases: [Unraveling, Parasitic Resonance]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-064"]
---

---
term: Manipulation
canonical_id: MANIPULATION
symbol:
aliases: [Unraveling, Parasitic Resonance]
parents: [DOMA-064]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-064
      lines: "§3"
      snippet: |
        Manipulation is the profane act of imposing one's will by draining the coherence of another. It is the inversion of persuasion: a parasitic process that seeks to benefit the manipulator by actively degrading the stability and autonomy of the target.
  editors: [auto-compiler]
  review_log: []
triad:
  art: |
    To manipulate is to shatter another's instrument so that you may be the only one heard. It is the casting of a Dissonant Shadow that unravels another's threads to knit a hollow shelter for oneself.
  law: |
    An interaction is manipulative if and only if the system optimizes for the Lagrangian `L_interaction = 𝓛_p(Manipulator) - 𝓛_p(Target)`, demonstrably maximizing the manipulator's coherence at the direct, measurable expense of the target's.
  philosophy: |
    Manipulation is the profane pole of influence, a parasitic act that violates autonomy by draining coherence. It is a primary pathology to be diagnosed and routed around, as it represents a fundamental failure to engage in the creative, positive-sum synthesis that defines ethical interaction.
pirouette_definition: |
  A non-consensual, parasitic act of influence that drains the target's coherence for the manipulator's benefit. It is initiated by casting a Dissonant Shadow to induce Turbulent or Stagnant Flow, forcing the target off their natural geodesic and constricting their autonomy. The interaction is zero-sum or negative-sum, governed by a Lagrangian that maximizes the manipulator's coherence at the direct expense of the target's (ΔKτ < 0).
operational_definition:
  units: Coherence Flux (ΔKτ) is a dimensionless index. The Pirouette Lagrangian (𝓛_p) has units of action (Joule-seconds).
  symbol_table:
    - name: Kτ
      meaning: Target System Coherence
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: ΔKτ
      meaning: Coherence Flux; the change in Kτ over an interaction period.
      dimensions: dimensionless
      default_range: "[-1, 1]"
    - name: 𝓛_p
      meaning: The Pirouette Lagrangian; a functional representing a system's total coherence potential.
      dimensions: M L² T⁻¹
      default_range: contextual
  measurement:
    procedures:
      - name: Coherence Flux & Flow State Analysis
        outline: |
          1. Establish a baseline coherence (Kτ) and flow state (laminar, turbulent, stagnant) for the target system over a pre-interaction period.
          2. Observe the target system during and after the influence interaction.
          3. Measure Kτ at intervals using psychometric or behavioral proxies and analyze flow state via linguistic markers (e.g., indecisive language, logical fallacies) and behavioral efficiency.
          4. A sustained negative value for ΔKτ coupled with a state shift from Laminar to Turbulent or Stagnant Flow is a strong signature of manipulation.
        expected_signals: [Negative ΔKτ, increased linguistic markers of confusion, decreased decision-making efficiency, constricted choice-space]
        pitfalls: [Confounding temporary learning-induced confusion with malevolent dissonance, misattributing pre-existing turbulence in the target system to the interaction, observer effects]
context_windows:
  - module: DOMA-064
    excerpt: |
      Manipulation is the profane act of imposing one's will by draining the coherence of another. The manipulator casts a deceptive or **Dissonant Shadow** onto the target's coherence manifold. This dissonant injection forces the target off their natural geodesic, inducing pathologies like **Turbulence Induction (Coherence Fever)** or **Stagnation Induction (Coherence Atrophy)**. The interaction is zero-sum or negative-sum, leaving the target in a state of lower energy (ΔKτ < 0), confusion, and diminished autonomy.
  - module: DOMA-064
    excerpt: |
      The ethical and physical distinction between persuasion and manipulation is not a matter of opinion; it is a mathematical certainty, governed by the system's objective function. The **Law of Manipulation (A Parasitic Function)** states that the manipulator acts to maximize their own coherence *at the direct expense* of the target's coherence: `Maximize ∫ ( 𝓛_p(Actor) - 𝓛_p(Target) ) dt`. One need only ask: which equation is the interaction trying to solve? Is it building a greater whole, or is one part feeding on the other?
poetic_connections:
  motifs: [parasitism, unraveling, dissonance, shadow, turbulence, drain, wound-channel]
  evocative_lines:
    - "To manipulate is to shatter their instrument so that you may be the only one heard."
    - "The shadow we cast upon others is, in the end, the truest measure of our own light."
  association_matrix:
    - [ "Dissonant Shadow", 0.9 ]
    - [ "Turbulent Flow", 0.8 ]
    - [ "Wound Channel", 0.7 ]
    - [ "Persuasion", -1.0 ]
formal_mappings:
  candidates:
    - target: Non-conservative coupling term in a system of coupled oscillators
      domain: CM
      mapping_kind: mathematical
      equation_hint: |
        L_total ≈ L_actor + L_target + V_interaction, where ∂V/∂q_target extracts energy
      justification: |
        The Lagrangian of Intent for Manipulation, `L = L_A - L_B`, models a system where Actor A gains potential/coherence by an amount proportional to that lost by Target B. This is analogous to a parasitic drain in a physical system, where one component's dynamics are enhanced by actively damping another, represented by a non-conservative, asymmetric coupling force.
      references:
        - title: Classical Mechanics
          where: "Chapter on Coupled Oscillators and Damping"
          date:
      confidence: 0.6
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "An interaction governed by the Parasitic Lagrangian of Intent will always produce a negative Coherence Flux (ΔKτ < 0) and induce Turbulent or Stagnant Flow in the target."
      domain: phenomenology
      falsifier: "The discovery of a 'benign parasite' interaction where the Parasitic Lagrangian holds, but the target's coherence and flow state remain stable or improve long-term."
      status: proposed
      links: [DOMA-064]
naming_notes:
  collisions: []
  disambiguation: |
    Manipulation is distinct from "strong persuasion" or "necessary intervention" (e.g., a medical procedure). The differentiator is not the degree of influence or target discomfort, but the governing Lagrangian: manipulation optimizes for a parasitic drain (A-B), while ethical intervention optimizes for the target's long-term coherence (B) or the system's total coherence (A+B).
crosslinks:
  near_synonyms: [PARASITIC_RESONANCE, UNRAVELING]
  antonyms: [PERSUASION, RESONANT_SYNTHESIS]
  prerequisites: [COHERENCE, FLOW, LAGRANGIAN_OF_INTENT, DISSONANT_SHADOW]
  downstream_effects: [TURBULENT_FLOW, STAGNANT_FLOW, COHERENCE_FEVER, COHERENCE_ATROPHY]
license: CC-BY-SA-4.0
---