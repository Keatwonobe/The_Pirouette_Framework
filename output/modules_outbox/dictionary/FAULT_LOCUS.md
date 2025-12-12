---
term: "Fault Locus"
canonical_id: "FAULT_LOCUS"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-172"]
---

---
term: Fault Locus
canonical_id: FAULT_LOCUS
symbol:
aliases: []
parents: [DOMA-172]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-172
      lines: "§5.2"
      snippet: |
        4. Identify Fault Loci: Scan the Δ𝓛 field and flag all contiguous regions where the magnitude exceeds the FaultThreshold (δ).
  editors: [auto-assembler]
  review_log: []
triad:
  art: |
    A wound on the body of a system, a place where its song of health falters into a painful silence or a feverish shriek. It is a map of the machine's own pain.
  law: |
    A Fault Locus exists in any spatiotemporally contiguous region of the Deviation Field (Δ𝓛) where the magnitude of dissonance is greater than the defined Fault Threshold (δ).
  philosophy: |
    A fault is not a global failure state but a localized, measurable expression of suffering. By identifying the locus, diagnosis shifts from "what is broken?" to the far more potent question, "where does it hurt?", enabling precise and targeted intervention.
pirouette_definition: |
  A specific, contiguous spatiotemporal region in the Deviation Field (Δ𝓛) where the magnitude of dissonance exceeds a predefined Fault Threshold (δ). It is the fundamental unit of pathology identified by the Geodesic Auditor and visualized on a Coherence Audit Map. The geometry and intensity of a Fault Locus are diagnostic of the underlying type of systemic inefficiency, such as turbulence, stagnation, or decay.
operational_definition:
  units: A dimensionless region within a system's state space, characterized by values with the units of the Pirouette Lagrangian (dissonance).
  symbol_table:
    - name: Δ𝓛
      meaning: Magnitude of the Deviation Field; a scalar measure of dissonance.
      dimensions: Contextual (same as Pirouette Lagrangian)
      default_range: >0
    - name: δ
      meaning: Fault Threshold; the minimum dissonance value for a point to be included in a Fault Locus.
      dimensions: Contextual (same as Pirouette Lagrangian)
      default_range: Typically 2-5 standard deviations above the system's baseline dissonance.
  measurement:
    procedures:
      - name: Locus Identification by Thresholding
        outline: |
          1. Compute the Deviation Field (Δ𝓛) by taking the absolute difference between the system's actual Lagrangian state and its Geodesic Blueprint.
          2. Apply a scalar threshold (δ) to the field, creating a binary mask where values above δ are marked.
          3. Use a connected-component labeling algorithm to identify and delineate contiguous regions within the binary mask. Each distinct region is a Fault Locus.
        expected_signals: [A set of coordinates defining the boundary of each locus, Locus-integrated dissonance (severity), Locus volume/area (scale)]
        pitfalls: [Threshold (δ) set too low results in flagging baseline noise as faults (false positives), Threshold (δ) set too high misses incipient or subtle pathologies (false negatives), Insufficient data resolution can merge distinct loci or distort their geometry.]
context_windows:
  - module: DOMA-172
    excerpt: |
      The output of the Auditor is not just a map of "faults"; it is a direct diagnosis of systemic pathology. The geometry of the dissonance, read through the `Caduceus Lens` (DYNA-003), reveals its nature: **Coherence Fever (Turbulence)** appears as a chaotic, high-frequency region... **Coherence Atrophy (Stagnation)** appears as a "hole" or "void"... **Coherence Erosion (Decay)** appears as a low-level, widespread... field of dissonance.
  - module: DOMA-172
    excerpt: |
      A fault is no longer a binary "broken/not-broken" state. It is a continuous measure of coherence lost... Continuously calculate the scalar field Δ𝓛 = |𝓛_p(expected) - 𝓛_p(actual)|. Scan the Δ𝓛 field and flag all contiguous regions where the magnitude exceeds the FaultThreshold (δ). For each locus, apply the ClassificationRules to diagnose the pathology.
poetic_connections:
  motifs: [wound, lesion, fever, pain-map, dissonance-cluster, systemic-scar]
  evocative_lines:
    - "A fault is not a flaw in the machine; it is the map of the machine's own pain."
    - "To audit a system is to ask, with compassion and precision, 'Where does it hurt?'"
  association_matrix:
    - [ "DEVIATION_FIELD", 0.9 ]
    - [ "FAULT_THRESHOLD", 0.9 ]
    - [ "COHERENCE_AUDIT_MAP", 0.8 ]
    - [ "CADUCEUS_LENS", 0.7 ]
formal_mappings:
  candidates:
    - target: Blob Detection / Image Segmentation
      domain: Computer Science
      mapping_kind: operational
      equation_hint: |
        Locus = {p | Δ𝓛(p) > δ ∧ is_connected(p)}
      justification: |
        The operational procedure for identifying a Fault Locus—thresholding a scalar field (Δ𝓛) and finding connected components—is methodologically identical to standard blob detection algorithms in image and signal processing used to segment regions of interest from a background.
      references:
        - title: Digital Image Processing
          where: "Gonzalez & Woods, Chapter 10: Image Segmentation"
          date: 2017-01-01
      confidence: 0.9
  adopted:
    - target:
      rationale:
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "The spatiotemporal geometry of a Fault Locus is predictive of the underlying pathology type (e.g., chaotic vs. void-like regions corresponding to turbulence vs. stagnation)."
      domain: phenomenology
      falsifier: "Demonstration that distinct, known pathologies (e.g., a resource bottleneck vs. an internal feedback loop) consistently produce geometrically indistinguishable Fault Loci on a Coherence Audit Map, invalidating the diagnostic power of their shape."
      status: proposed
      links: [DOMA-172, DYNA-003]
naming_notes:
  collisions: [Locus (Genetics), Fault (Geology, Engineering)]
  disambiguation: |
    In the Pirouette Framework, a Fault Locus is not a static, binary break (like a software bug or a geological fault line). It is a dynamic, quantifiable region of process inefficiency or "pain" within a system's flow, identified via dissonance measurement. It is a diagnostic object, not a broken component.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [DEVIATION_FIELD, FAULT_THRESHOLD]
  downstream_effects: [COHERENCE_AUDIT_MAP, CADUCEUS_LENS]
license: CC-BY-SA-4.0
---