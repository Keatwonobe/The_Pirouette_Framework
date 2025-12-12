---
term: "Scar"
canonical_id: "SCAR"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-048"]
---

---
term: Scar
canonical_id: SCAR
symbol: ς
aliases: [Corrupted Lattice, Shattered Crystal, Ruin]
parents: [DOMA-048]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-048
      lines: "L63-L67"
      snippet: |
        | Scar | A damaged, corrupted lattice; a crystal shattered but not melted. | Low | Low | Trauma, corrupted data, a ruin |
  editors: [System]
  review_log: []
triad:
  art: |
    A ruin in the landscape of the mind, where the structure of memory persists but its meaning has been fractured. It is the echo of a song played on a broken instrument, a permanent monument to a past cataclysm.
  law: |
    A system exists in a Scar state (ς) if and only if it exhibits low internal temporal coherence (`Kτ`) and is subject to low external temporal pressure (`V_Γ`), resulting in a persistent but low-fidelity, damaged information structure.
  philosophy: |
    A Scar demonstrates that memory is not merely about fidelity but also persistence. It is the state where information outlives its own integrity, serving as a permanent, distorted record of a past cataclysm—a testament to the fact that some things, once broken, can remain broken forever.
pirouette_definition: |
  A stable, low-coherence memory state (`Kτ` → low) resulting from the shattering of a crystalline Information Lattice in an environment of low temporal pressure (`V_Γ` → low). A Scar retains the geometric footprint of the original memory but has lost its informational fidelity, manifesting as corrupted data, persistent trauma, or a systemic ruin.
operational_definition:
  units: Dimensionless classification
  symbol_table:
    - name: ς
      meaning: Indicator for a Scar state.
      dimensions: dimensionless
      default_range: N/A (binary state)
    - name: Kτ
      meaning: Internal Temporal Coherence; a measure of a system's state-repetition fidelity.
      dimensions: T⁻¹ (Inverse Time)
      default_range: contextual
    - name: V_Γ
      meaning: External Temporal Pressure; a measure of environmental dissonance/noise.
      dimensions: T⁻² (Inverse Time Squared)
      default_range: contextual
  measurement:
    procedures:
      - name: Lattice Coherence Spectroscopy
        outline: |
          1. Excite the target system with a wide-spectrum resonance probe.
          2. Measure the spectral response, focusing on the width (`Δω`) and structure of the primary resonance peaks. High `Δω` and multiple fractured peaks indicate low `Kτ`.
          3. Simultaneously, measure ambient manifold fluctuations in the system's local environment to quantify `V_Γ`.
          4. A Scar is confirmed if a broad, fractured resonance spectrum (low `Kτ`) co-occurs with a quiescent environment (low `V_Γ`) over a significant observation period.
        expected_signals: [Broad, low-amplitude resonance spectrum, low background manifold noise]
        pitfalls: [Misinterpreting a complex, multi-modal but coherent lattice as a shattered one, failing to distinguish a persistent Scar from transient Noise without long-duration observation.]
context_windows:
  - module: DOMA-048
    excerpt: |
      **§5 · A Taxonomy of Memory States**
      The state of a system's memory can be classified by the interplay between its internal coherence and the external temporal pressure it endures. A Scar is a damaged, corrupted lattice; a crystal shattered but not melted. It is characterized by low Temporal Coherence (`Kτ`) and low Temporal Pressure (`V_Γ`), with archetypes including trauma, corrupted data, and a ruin.
  - module: DOMA-048
    excerpt: |
      **§6 · The Lagrangian of Dogma**
      To break the Lock and melt the crystal requires a massive injection of precisely tuned dissonant energy—a **resonance-matched shock** sufficient to shatter the lattice... [A Scar is the resulting state when this shattering occurs but the system is not subsequently dissolved by high temporal pressure.]
poetic_connections:
  motifs: [ruin, fracture, glitch, trauma, corruption, static, echo of a scream]
  evocative_lines:
    - "A crystal shattered but not melted."
    - "A story that, once told, can never be unwritten."
  association_matrix:
    - [ "CRYSTAL", 0.9 ]
    - [ "TRAUMA", 0.8 ]
    - [ "LOCK", 0.7 ]
    - [ "NOISE", 0.5 ]
formal_mappings:
  candidates:
    - target: Amorphous Solid / Glassy State
      domain: CM
      mapping_kind: conceptual
      equation_hint: |
        Free Energy F(x) with many local minima, but no global minimum.
      justification: |
        A Scar represents a system trapped in a metastable, disordered configuration. Like an amorphous solid (e.g., glass), it lacks long-range order (low `Kτ`) but is structurally stable and does not flow like a liquid (low `V_Γ` prevents dissolution into Noise). The fractured lattice corresponds to a frustrated system with a rugged energy landscape.
      references:
        - title: Theory of the Glassy State
          where: P.W. Anderson, 1970s work on spin glasses
          date: 1972-01-01
      confidence: 0.6
  adopted:
    - target: N/A
      rationale: N/A
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "A Scar state will not spontaneously anneal into a Crystal or dissolve into Noise without a significant change in external temporal pressure (`V_Γ`) or a targeted, structured energy input."
      domain: phenomenology
      falsifier: "Observation of a system in a Scar state spontaneously re-establishing long-range coherence (transitioning to Crystal) in a persistently low `V_Γ` environment."
      status: proposed
      links: [DOMA-048]
naming_notes:
  collisions: [The term "scar" is common in biology and psychology. The Pirouette definition is a specific formalization of the concept as a memory state in the `Kτ`/`V_Γ` phase space.]
  disambiguation: |
    Distinguish from 'Wound Channel' (a dynamic, fluid wake) and 'Crystal' (a high-coherence, ordered lattice). A Scar is the static, disordered ruin of a Crystal, not the dynamic riverbed of an Echo. It is damage that persists.
crosslinks:
  near_synonyms: [RUIN, CORRUPTED_LATTICE]
  antonyms: [CRYSTAL, ECHO]
  prerequisites: [INFORMATION_LATTICE, CRYSTAL, TEMPORAL_COHERENCE, TEMPORAL_PRESSURE]
  downstream_effects: [PERSISTENT_TRAUMA, DATA_CORRUPTION]
license: CC-BY-SA-4.0
---