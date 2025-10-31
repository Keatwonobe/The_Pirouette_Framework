---
term: "Wound Boundary"
canonical_id: "WOUND_BOUNDARY"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-131"]
---

---
term: Wound Boundary
canonical_id: WOUND_BOUNDARY
symbol: ∂Ω_rupture
aliases: [Topological Scar, Fracture Surface, Rupture Surface]
parents: [DOMA-131]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-131
      lines: "§5"
      snippet: |
        A rupture permanently alters the geometry of a system's being by creating a **Wound Boundary**. This is not merely a memory of stress like a `Wound Channel`, but a new, harsh, and irreversible topological feature—a scar where a single coherent body was violently torn into two or more entities.
  editors: [GPT-4 (Pirouette Dictionary Agent)]
  review_log: []
triad:
  art: |
    The jagged edge of a broken bell that no longer sings, but shrieks. A cliff where a bridge once stood, its echo a constant reminder of the fall. It is the scar tissue of spacetime, a story of severance written into the very fabric of a system.
  law: |
    A Wound Boundary is a permanent, zero-transmittance discontinuity in the coherence manifold. Information, energy, and resonance cannot cross this boundary; they are either reflected or dissipated as dissonant noise. Its formation is an irreversible phase transition.
  philosophy: |
    The Wound Boundary teaches that not all things can be mended. It rejects naive notions of healing as restoration, forcing a system to acknowledge its new, fractured reality. Survival and growth depend not on erasing the scar, but on learning to navigate the new, harsher geometry it creates.
pirouette_definition: |
  A permanent, irreversible topological feature of a system's coherence manifold, created by a Rupture. A Wound Boundary manifests as a sharp discontinuity that completely severs information flow and resonant coupling between previously connected sub-domains. It functions as a persistent source of temporal noise (`Turbulent Flow`) and fundamentally alters the system's available paths of least resistance (geodesics).
operational_definition:
  units: Dimensionless (topological feature).
  symbol_table:
    - name: ∂Ω_rupture
      meaning: The set of points defining the boundary of a ruptured domain (Ω).
      dimensions: L^(N-1), where N is the dimensionality of the coherence manifold.
      default_range: N/A (represents a geometric locus).
  measurement:
    procedures:
      - name: Coherence Flow Tomography
        outline: |
          1. Identify a conserved current (information, energy, trust) that flows through the system.
          2. Map the flow vector field across the system's manifold under nominal conditions.
          3. After a suspected rupture event, remap the flow field.
          4. A Wound Boundary is confirmed where the flow vector magnitude drops to and remains at zero across a stable, co-dimension 1 surface.
        expected_signals: [A persistent step-function drop in cross-boundary information transfer to zero, Emergence of high-amplitude, low-frequency noise originating from the boundary line/surface.]
        pitfalls: [Mistaking a temporary blockage or a highly resistive `Wound Channel` for a true zero-transmittance boundary. Failing to measure for a sufficient duration to confirm irreversibility.]
context_windows:
  - module: DOMA-131
    excerpt: |
      A rupture permanently alters the geometry of a system's being by creating a **Wound Boundary**. This is not merely a memory of stress like a `Wound Channel`, but a new, harsh, and irreversible topological feature—a scar where a single coherent body was violently torn into two or more entities. The Wound Boundary is a cliff where a smooth path once existed. The flow of coherence across the rupture line ceases. Parts of the system are now isolated, unable to communicate or support each other.
poetic_connections:
  motifs: [severance, scar, echo, abyss, amputation, fracture, schism]
  evocative_lines:
    - "The jagged edges of a broken bell."
    - "The Broken Geodesic."
    - "A cliff where a smooth path once existed."
  association_matrix:
    - [ "RUPTURE", 0.9 ]
    - [ "COHERENCE_CASCADE", 0.8 ]
    - [ "WOUND_CHANNEL", 0.6 ]
    - [ "TURBULENT_FLOW", 0.7 ]
formal_mappings:
  candidates:
    - target: Domain Wall
      domain: EFT
      mapping_kind: conceptual
      equation_hint: |
        ∇φ → ∞ across the boundary ∂Ω.
      justification: |
        A domain wall is a topological defect separating two distinct vacuum states. This maps to the Wound Boundary separating two now-decoupled sub-systems that can no longer communicate, effectively existing in different "ground states" of coherence. The boundary is a permanent feature of the system's new topology.
      references:
        - title: "An Invitation to Quantum Fields and Strings"
          where: "Chapter on Topological Defects"
          date: 2005-01-01
      confidence: 0.8
    - target: Graph Cut
      domain: Math
      mapping_kind: operational
      equation_hint: |
        Flow(A, B) = 0, for all nodes a ∈ A, b ∈ B.
      justification: |
        In graph theory, a cut partitions the vertices of a graph into two disjoint sets. A Wound Boundary is analogous to a minimum cut where the cut capacity is zero, representing the complete and permanent severance of all edges (information pathways) between the two partitions of the system.
      references:
        - title: "Graph Theory"
          where: "Chapter on Network Flows"
          date: 2008-01-01
      confidence: 0.7
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "A Wound Boundary is topologically stable and irreversible; information flow across it cannot be restored, only bypassed."
      domain: phenomenology
      falsifier: "Observation of a system spontaneously 'healing' a Wound Boundary, restoring direct information flow across the original rupture line to pre-rupture levels, without the creation of a new bridging structure."
      status: proposed
      links: [DOMA-131]
naming_notes:
  collisions: []
  disambiguation: |
    Crucially distinct from a `Wound Channel` (CORE-011). A Wound Channel is a region of *degraded* coherence, a path of high resistance that can be deepened by stress or potentially reinforced. A Wound Boundary is a region of *zero* coherence, a complete severance. A channel is a sick organ; a boundary is an amputation.
crosslinks:
  near_synonyms: [SCHISM]
  antonyms: [COHERENCE, LAMINAR_FLOW]
  prerequisites: [RUPTURE, COHERENCE_CASCADE]
  downstream_effects: [TURBULENT_FLOW, SYSTEMIC_TRAUMA]
license: CC-BY-SA-4.0
---

# Wound Boundary

## Canonical (Pirouette)
A permanent, irreversible topological feature of a system's coherence manifold, created by a Rupture. A Wound Boundary manifests as a sharp discontinuity that completely severs information flow and resonant coupling between previously connected sub-domains. It functions as a persistent source of temporal noise (`Turbulent Flow`) and fundamentally alters the system's available paths of least resistance (geodesics).

## EFT-First Summary
Conceptually, a Wound Boundary maps to a **topological defect** like a **domain wall** in Effective Field Theory. It represents a permanent, high-energy interface separating two regions of a system that have collapsed into distinct, incommunicable states of coherence. Like a domain wall, it is a stable feature of the system's new topology, fundamentally altering its dynamics and preventing any direct flow of information or conserved quantities across it.

## Glossary Links
- See also: RUPTURE, COHERENCE_CASCADE, WOUND_CHANNEL, TURBULENT_FLOW