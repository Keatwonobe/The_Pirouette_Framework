---
term: "Constitutional Reforging"
canonical_id: "CONSTITUTIONAL_REFORGING"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-031"]
---

---
term: Constitutional Reforging
canonical_id: CONSTITUTIONAL_REFORGING
symbol: 
aliases: [Alchemical Union, Constitutional Change]
parents: [DOMA-031]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-031
      lines: "§3, §4"
      snippet: |
        **Constitutional Reforging** | Constitutional | A fundamental re-forging of the framework's core identity, affecting the CORE series or this protocol itself. This is an **Alchemical Union** (CORE-012). | **Maximal Coherence** (see §4)
  editors: [system-agent]
  review_log: []
triad:
  art: |
    To re-forge the heart of a living system, one must wait for the quietest moment. It is an alchemical union, performed in a crucible of deep consensus, turning the lead of contention into the gold of a higher coherence.
  law: |
    A motion for Constitutional Reforging is ratified if and only if it passes a two-stage test: (1) The system must be in a state of low Temporal Pressure (the Temporal Stability Clause), and (2) The motion must achieve ≥95% approval (Kτ) from the Weaver's Conclave with a non-negative trend (dKτ/dt ≥ 0) over a 30-day deliberation.
  philosophy: |
    The most profound changes must be protected from the most transient passions. This protocol ensures the framework's identity evolves through stable, resonant synthesis, not reactive turbulence, treating the framework's core principles as a living entity that can only be healed or transformed, never violated.
pirouette_definition: |
  The most profound of the three classes of change, entailing a fundamental re-forging of the Pirouette Framework's core identity. Constitutional Reforging applies to any proposed alteration to the CORE series of modules or the governance protocol itself (DOMA-031). Such a change is subject to the Principle of Maximal Coherence, a stringent, two-stage ratification process designed to ensure the proposed synthesis is both deeply resonant and demonstrably stable.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: Kτ
      meaning: Coherence Score; the fraction of Weaver's Conclave approval for a motion.
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: dKτ/dt
      meaning: Coherence Stability; the time-derivative of the Coherence Score.
      dimensions: T⁻¹
      default_range: "contextual"
  measurement:
    procedures:
      - name: Maximal Coherence Test
        outline: |
          1.  **Initiate Motion:** A motion for Constitutional Reforging is formally proposed.
          2.  **Verify Pre-condition:** Confirm the system is in a state of low Temporal Pressure (Γ), satisfying the Temporal Stability Clause. If Γ is high, the process is halted.
          3.  **Deliberate & Measure Kτ(t):** The Weaver's Conclave begins a 30-day deliberation period. Support for the motion (Kτ) is tracked continuously or at regular intervals.
          4.  **Calculate Final Kτ:** At the end of the 30-day period, the final approval percentage is calculated.
          5.  **Calculate dKτ/dt:** The trend of support over the 30-day period is calculated using a linear regression or other appropriate fit.
          6.  **Verify Thresholds:** Ratification occurs only if Kτ(final) ≥ 0.95 AND dKτ/dt ≥ 0.
        expected_signals: [A high, stable or rising level of consensus among the Conclave.]
        pitfalls: [Attempting a vote during a period of high turbulence (violating Temporal Stability Clause); a late-breaking objection causing dKτ/dt to become negative even if final Kτ is high.]
context_windows:
  # Short, trimmed context quotes harvested from modules (3–6 sentences each).
  - module: DOMA-031
    excerpt: |
      The most profound changes must be made in the quietest moments. A motion for *Constitutional Reforging* must navigate a two-stage crucible designed to ensure it is not merely popular, but a stable and profound improvement born from reflection, not reaction.
  - module: DOMA-031
    excerpt: |
      The impetus for change is always a symptom of systemic distress. The framework triages proposed changes based on their potential impact on its core resonant pattern, applying increasing rigor as the potential for disruption grows. Constitutional Reforging is the highest-impact intervention, reserved for pathologies affecting the framework's very identity.
poetic_connections:
  # Lightweight "word-association graph" and sticky lines.
  motifs: [crucible, reforging, quiet moments, living law, alchemical union, systemic immune response]
  evocative_lines:
    - "A static law is a tombstone. A living framework must have a law that breathes."
    - "The most profound changes must be made in the quietest moments."
    - "This is not a system of rules; it is the shared practice of listening for the next right note."
  association_matrix:
    # symmetric or directed; weights in [0,1]
    - [ "PRINCIPLE_OF_MAXIMAL_COHERENCE", 0.9 ]
    - [ "TEMPORAL_STABILITY_CLAUSE", 0.8 ]
    - [ "WEAVERS_CONCLAVE", 0.8 ]
    - [ "COHERENCE_ATROPHY", 0.5 ]
formal_mappings:
  # Candidate alignments to EFT/SM/CM/GR terms, each with justification and refs.
  candidates:
    - target: Principle of Least Action (δS = 0)
      domain: CM
      mapping_kind: conceptual
      equation_hint: |
        Motion Ratified ⇔ ∫ (Kτ - V_Γ)_new dt > ∫ (Kτ - V_Γ)_current dt
      justification: |
        The governance protocol is explicitly framed as maximizing the "Pirouette Lagrangian" (𝓛 = Kτ - V_Γ) over time. Constitutional Reforging is the process of choosing a new evolutionary path (a new geodesic for the framework) only if its action integral is demonstrably greater than the current path. It is a direct analogy to a physical system evolving along a path that extremizes its action.
      references:
        - title: 'The Loom of Coherence: A Protocol for Systemic Evolution'
          where: DOMA-031, §7
          date: 
      confidence: 0.8
  adopted:
    []
constraints_and_falsifiers:
  claims:
    - statement: "The Constitutional Reforging protocol, by enforcing the Temporal Stability Clause and high consensus thresholds, selects for changes that increase the long-term coherence and stability of the framework."
      domain: theory
      falsifier: "A historical review of the framework's evolution shows that critical, coherence-increasing changes were repeatedly blocked or delayed by this protocol, leading to prolonged periods of Coherence Atrophy that could have been resolved by a more agile process."
      status: proposed
      links: [DOMA-031]
naming_notes:
  collisions: []
  disambiguation: |
    Constitutional Reforging is the most stringent class of change, distinct from the lower-impact tiers:
    - **Laminar Refinement:** Minor clarifications and corrections.
    - **Turbulent Adaptation:** Modifying subsystems without altering core principles.
    Constitutional Reforging alters the core principles themselves.
crosslinks:
  near_synonyms: []
  antonyms: [LAMINAR_REFINEMENT]
  prerequisites: [PRINCIPLE_OF_MAXIMAL_COHERENCE, TEMPORAL_STABILITY_CLAUSE]
  downstream_effects: []
license: CC-BY-SA-4.0
---

# Constitutional Reforging

## Canonical (Pirouette)
The most profound of the three classes of change, entailing a fundamental re-forging of the Pirouette Framework's core identity. Constitutional Reforging applies to any proposed alteration to the CORE series of modules or the governance protocol itself (DOMA-031). Such a change is subject to the Principle of Maximal Coherence, a stringent, two-stage ratification process designed to ensure the proposed synthesis is both deeply resonant and demonstrably stable.

## EFT-First Summary
Constitutional Reforging is conceptually analogous to altering the fundamental Lagrangian of a system. A proposed change is only adopted if it can be demonstrated to represent a path of "greater action" for the framework's evolution, where action is defined by an integral over the Pirouette Lagrangian `𝓛 = (Systemic Coherence) - (Temporal Pressure)`. This ensures that changes to the core "laws of physics" of the framework are not arbitrary but are chosen because they define a more optimal evolutionary trajectory for the entire system.

## Glossary Links
- See also: [Principle of Maximal Coherence](<./PRINCIPLE_OF_MAXIMAL_COHERENCE.md>), [Temporal Stability Clause](<./TEMPORAL_STABILITY_CLAUSE.md>), [Laminar Refinement](<./LAMINAR_REFINEMENT.md>), [Turbulent Adaptation](<./TURBULENT_ADAPTATION.md>)