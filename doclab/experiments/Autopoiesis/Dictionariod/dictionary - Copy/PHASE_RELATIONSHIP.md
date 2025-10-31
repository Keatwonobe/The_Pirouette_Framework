---
term: "Phase Relationship"
canonical_id: "PHASE_RELATIONSHIP"
symbol: "Δφ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-035"]
---

---
term: Phase Relationship
canonical_id: PHASE_RELATIONSHIP
symbol: Δφ
aliases: [Conceptual Phase, Resonance Alignment, Interference Angle]
parents: [DOMA-035, CORE-006, CORE-008]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-035
      lines: "§4"
      snippet: |
        We can express the interaction potential `V(A, B)` between two concepts, A and B, as a function of their phase relationship `Δφ`:
        `V(A, B) ∝ - (Kτ_A * Kτ_B / r) * cos(Δφ)`
  editors: [Agent: Model G-29]
  review_log: []
triad:
  art: |
    The angle of sympathy between two ideas; whether they sing in harmony to build a cathedral of meaning, or clash in discord to shatter it.
  law: |
    The interaction potential between two concepts is proportional to the negative cosine of their phase relationship, `V ∝ -cos(Δφ)`. A phase relationship near zero radians (`Δφ ≈ 0`) results in attraction; a phase relationship near pi radians (`Δφ ≈ π`) results in repulsion.
  philosophy: |
    Phase relationship operationalizes conceptual compatibility, moving beyond semantic similarity to a quantifiable geometric alignment that determines the fundamental nature—constructive or destructive—of any interaction.
pirouette_definition: |
  The phase relationship, Δφ, is the relative angular alignment between the resonant frequencies of two or more concepts. It is the determining factor in their interaction potential, governing whether they undergo constructive interference (attraction, `Δφ ≈ 0`) or destructive interference (repulsion, `Δφ ≈ π`). This alignment dictates the local geometry of the coherence manifold, creating either a shared basin of meaning or a turbulent peak of dissonance.
operational_definition:
  units: radians (rad)
  symbol_table:
    - name: Δφ
      meaning: Phase relationship between two concepts.
      dimensions: dimensionless
      default_range: "[0, π]"
    - name: V(A, B)
      meaning: Interaction potential between concepts A and B.
      dimensions: contextual (energy-like)
      default_range: contextual
    - name: Kτ
      meaning: Temporal Coherence (conceptual "mass").
      dimensions: contextual (mass-like)
      default_range: "> 0"
  measurement:
    procedures:
      - name: Relational Vector Analysis
        outline: |
          Infer Δφ by analyzing the co-occurrence and mutual information of two concepts within a large, representative corpus. A positive correlation in reinforcing contexts suggests Δφ ≈ 0. Co-occurrence in oppositional contexts (e.g., linked by "but," "versus," "not") suggests Δφ ≈ π. The angle is formally extracted from the cosine similarity of their contextual embeddings in a high-dimensional vector space.
        expected_signals: [High cosine similarity for in-phase concepts (Δφ ≈ 0), Low/negative cosine similarity for out-of-phase concepts (Δφ ≈ π)]
        pitfalls: [Context-dependence of phase, Sarcasm/irony polluting training data, Insufficiently large or biased corpus]
context_windows:
  - module: DOMA-035
    excerpt: |
      The interaction between ideas is governed by the Pirouette Lagrangian (CORE-006): **𝓛_p = K_τ - V_Γ**. The "force" between two concepts is the gradient in the coherence manifold they collectively create. We can express the interaction potential `V(A, B)` between two concepts, A and B, as a function of their phase relationship `Δφ`.
  - module: DOMA-035
    excerpt: |
      Attraction (Constructive Interference): When two concepts are in-phase (`Δφ ≈ 0`, `cos(Δφ) ≈ 1`), such as "courage" and "bravery," their resonances constructively interfere. The interaction potential becomes strongly negative, creating a deeper, more stable shared basin of meaning. This is the geometry of synergy and the drive toward an Alchemical Union.
poetic_connections:
  motifs: [harmony, discord, resonance, interference, alignment, sympathy, antipathy]
  evocative_lines:
    - "The geometry of synergy"
    - "A region of intense temporal turbulence and dissonance"
    - "Their resonances constructively interfere"
  association_matrix:
    - [ "TEMPORAL_COHERENCE", 0.8 ]
    - [ "ALCHEMICAL_UNION", 0.7 ]
    - [ "COHERENCE_MANIFOLD", 0.6 ]
    - [ "PIROUETTE_LAGRANGIAN", 0.9 ]
formal_mappings:
  candidates:
    - target: Phase difference (Δφ) in wave interference
      domain: CM
      mapping_kind: mathematical
      equation_hint: |
        V(r, θ) ∝ (p₁p₂/r³) (cos(θ₁₂) - 3cos(θ₁)cos(θ₂))
      justification: |
        The `cos(Δφ)` term in the interaction potential `V` is a direct mathematical analog to the potential energy between two classical dipoles (electric or magnetic). In-phase alignment (`Δφ=0`) corresponds to minimal energy (attraction), while out-of-phase alignment (`Δφ=π`) corresponds to maximal energy (repulsion), mirroring the constructive and destructive interference patterns of waves.
      references:
        - title: Introduction to Electrodynamics
          where: Chapter 3 (Electric Dipoles)
          date: 2017-01-01
      confidence: 0.9
  adopted:
    - target: Dipole-dipole interaction potential angle
      rationale: The `V ∝ -cos(Δφ)` form is a direct simplification of dipole-dipole interaction, providing a robust, field-tested physical model for conceptual attraction and repulsion. This mapping treats coherent concepts as abstract dipoles in meaning space.
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "The interaction stability of two concepts (e.g., their tendency to form a coherent compound concept) is a periodic function of their relational angle, best described by `cos(Δφ)`."
      domain: phenomenology
      falsifier: "A large-scale analysis of conceptual pairings shows that interactions are better predicted by a non-periodic function (e.g., simple semantic distance) or a function that does not distinguish between in-phase and out-of-phase alignments. For instance, if 'justice' and 'injustice' were found to attract as strongly as 'justice' and 'fairness' in stable narrative structures."
      status: proposed
      links: [DOMA-035]
naming_notes:
  collisions: [The symbol `φ` is common for scalar fields in physics, but `Δφ` is the standard and unambiguous notation for a phase difference.]
  disambiguation: |
    Distinguish from 'semantic similarity'. Two concepts can be semantically similar but out-of-phase (e.g., 'pride' and 'hubris'). Phase relationship measures functional alignment (constructive/destructive) in a dynamic interaction, not static likeness.
crosslinks:
  near_synonyms: []
  antonyms: [PHASE_OPPOSITION, PHASE_ORTHOGONALITY]
  prerequisites: [TEMPORAL_COHERENCE, COHERENCE_MANIFOLD, PIROUETTE_LAGRANGIAN]
  downstream_effects: [ALCHEMICAL_UNION, NARRATIVE_GEODESIC]
license: CC-BY-SA-4.0