---
term: "Brittleness"
canonical_id: "BRITTLENESS"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-047"]
---

---
term: Brittleness
canonical_id: BRITTLENESS
symbol: 
aliases: [Rigid Coherence]
parents: [DOMA-047]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-047
      snippet: |
        **Brittleness** characterizes systems with rigid, inflexible coherence. They resist stress with high fidelity up to a sharp limit, but possess little to no capacity for plastic deformation. When Coherence Stress exceeds their critical threshold, they do not bend; they shatter instantly.
  editors: [autodict_compiler]
  review_log: []
triad:
  art: |
    A crystal that holds its perfect form against all pressure, until a final tap turns it to dust. Its story has no middle act between integrity and ruin. It is a song that cannot learn a new note and so chooses silence.
  law: |
    A system is brittle if its yield threshold is greater than or equal to its fracture threshold. Under increasing Coherence Stress, it will transition directly from elastic deformation to catastrophic decoherence, with a negligible or non-existent phase of plastic deformation (yielding).
  philosophy: |
    Brittleness is the pathology of perfectionism. It prioritizes the preservation of an original, rigid identity over adaptation and survival. It reveals that unyielding integrity, when faced with overwhelming change, is indistinguishable from suicide.
pirouette_definition: |
  The character of a system defined by a rigid, inflexible Temporal Coherence ($K_\tau$) that prevents plastic deformation. When Coherence Stress exceeds the system's elastic limit, it is unable to adapt by re-carving its Wound Channel. Instead, it undergoes an immediate, catastrophic phase transition to decoherence, known as fracture.
operational_definition:
  units: Dimensionless (often expressed as a ratio of energies or stresses)
  symbol_table:
    - name: $\mathcal{E}_{yield}$
      meaning: Energy threshold for plastic deformation (Wound Channel re-carving)
      dimensions: $M L^2 T^{-2}$
      default_range: contextual
    - name: $\mathcal{E}_{fracture}$
      meaning: Energy threshold for catastrophic decoherence (fracture)
      dimensions: $M L^2 T^{-2}$
      default_range: contextual
  measurement:
    procedures:
      - name: Coherence Stress Test
        outline: |
          1.  Establish a baseline measurement of the system's Temporal Coherence ($K_\tau$) in a low-stress state.
          2.  Apply a controlled, incrementally increasing Coherence Stress (e.g., increasing Temporal Pressure, Γ, or directly disrupting coherence).
          3.  Simultaneously monitor the system's coherence signature and its structural integrity for two key transitions:
              a.  **Yield Point**: A permanent change in the baseline coherence signature after stress is removed.
              b.  **Fracture Point**: A sudden, cascading collapse of coherence ($K_\tau \to 0$).
          4.  Brittleness is confirmed if the Fracture Point is reached without a preceding, measurable Yield Point. The system's response curve will show a sharp, terminal drop-off from the elastic region.
        expected_signals: [A stress-response curve lacking a plastic deformation plateau; a sharp discontinuity in the power spectrum of the system's "song".]
        pitfalls: [Failure to apply stress faster than the system's potential adaptation time, misclassifying rapid ductile failure as brittle; Insufficient sensor resolution to detect a very brief yield phase.]
context_windows:
  - module: DOMA-047
    excerpt: |
      **Brittleness** characterizes systems with rigid, inflexible coherence. They resist stress with high fidelity up to a sharp limit, but possess little to no capacity for plastic deformation. When Coherence Stress exceeds their critical threshold, they do not bend; they shatter instantly. Their story has no middle act between perfect form and total failure.
  - module: DOMA-047
    excerpt: |
      In material science, brittle fracture (glass) is an example of a system where a rigid $K_\tau$ cannot adapt. A sharp increase in $V_\Gamma$ (impact) causes an immediate coherence collapse ($K_\tau \to 0$). Similarly, in economics, a market crash is a brittle failure where coherence ($K_\tau$, trust) is rigid and a shock ($V_\Gamma$) triggers a feedback loop where $K_\tau$ evaporates instantly.
poetic_connections:
  motifs: [shattering, silence, ice, glass, perfection, rigidity, suddenness, unyielding]
  evocative_lines:
    - "Their story has no middle act between perfect form and total failure."
    - "The shatter is the final, sudden end of a song that could not learn a new note."
  association_matrix:
    # symmetric or directed; weights in [0,1]
    - [ "DUCTILITY", -1.0 ]
    - [ "FRACTURE", 0.9 ]
    - [ "COHERENCE_STRESS", 0.7 ]
    - [ "WOUND_CHANNEL", -0.5 ]
formal_mappings:
  candidates:
    - target: Brittleness
      domain: CM
      mapping_kind: operational
      equation_hint: |
        In a stress-strain curve ($\sigma$ vs $\epsilon$), brittle materials show $\epsilon_{plastic} \approx 0$ before fracture.
      justification: |
        The Pirouette definition is a direct conceptual and operational mapping of brittleness from continuum mechanics and material science. The absence of a "yield transition" before "fracture" in Pirouette corresponds to the lack of a plastic deformation region before the fracture point on a classical stress-strain curve.
      references:
        - title: Mechanical Behavior of Materials
          where: Chapter on Fracture
          date: 2003-01-01
      confidence: 0.95
  adopted:
    - target: Brittleness (Material Science)
      rationale: The mapping is a 1:1 analogy and serves as the primary physical intuition for the abstract Pirouette concept.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "A system's brittleness is inversely correlated with the complexity and adaptability of its Wound Channel."
      domain: theory
      falsifier: "Discovering a system with a highly complex, adaptive Wound Channel that consistently fails in a brittle manner, suggesting that brittleness is governed by a factor other than coherence flexibility."
      status: proposed
      links: [DOMA-047, CORE-011]
naming_notes:
  collisions: []
  disambiguation: |
    Brittleness is not synonymous with weakness. A brittle system can be exceptionally strong (i.e., possess a high fracture threshold) but will fail catastrophically once that threshold is crossed. Contrast with a weak but ductile system, which deforms easily but fails gradually.
crosslinks:
  near_synonyms: []
  antonyms: [DUCTILITY]
  prerequisites: [COHERENCE_STRESS, TEMPORAL_COHERENCE, FRACTURE, YIELD_TRANSITION]
  downstream_effects: [FRACTURE]
license: CC-BY-SA-4.0