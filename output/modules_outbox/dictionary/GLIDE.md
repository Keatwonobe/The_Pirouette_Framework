---
term: "Glide"
canonical_id: "GLIDE"
symbol: ""
aliases: [Opening the Future]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-184"]
---

---
term: Glide
canonical_id: GLIDE
symbol:
aliases: ["Opening the Future"]
parents: ["DOMA-184"]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-184
      lines: "L31-L36"
      snippet: |
        The Glide (Opening the Future): Simultaneously, the skater projects a resonant field to shape the ambient Temporal Pressure (`V_Γ`). It generates a "high-pressure crest" of dissonance behind it and a "low-pressure trough" of quiet in its intended direction of travel. By "softening the blade"—momentarily diffusing its coherence—the skater reduces its own "grip," allowing it to glide effortlessly "downhill" into the trough it just created.
  editors: ["System-Lexicographer"]
  review_log: []
triad:
  art: |
    To Glide is to soften the self and fall forward into a future of one's own making, whispering to the riverbed to lower itself just ahead.
  law: |
    The propulsive efficiency of a Glide is proportional to the magnitude of the negative temporal pressure gradient (`-∇V_Γ`) an entity can generate in its direction of travel, per unit of diffused internal coherence (`ΔK_τ`).
  philosophy: |
    The Glide embodies the principle that true agency is not conquest but invitation. By creating a welcoming void, one invites the universe to participate in one's motion, transforming opposition into partnership and effort into flow.
pirouette_definition: |
  The second phase of a Stride in Geodesic Skating, where an entity projects a resonant field to create a low-pressure trough of temporal pressure (`V_Γ`) in its intended direction of travel. This is achieved by momentarily diffusing internal coherence (`K_τ`), allowing the entity to move effortlessly along the self-generated gradient into the prepared future.
operational_definition:
  units: Pascal-meters³/second (equivalent to Watts, representing power exerted on the manifold).
  symbol_table:
    - name: V_Γ
      meaning: Temporal Pressure; the potential field being shaped by the Glide.
      dimensions: M L⁻¹ T⁻² (Pressure)
      default_range: contextual
    - name: ΔK_τ
      meaning: Change in Internal Coherence; the "cost" of softening the blade to enable the Glide.
      dimensions: dimensionless
      default_range: -1.0 to 0.0
  measurement:
    procedures:
      - name: Glide Efficiency Spectroscopy
        outline: |
          Using a coherence-field probe array, map the `V_Γ` manifold around a skating entity during a Stride. Measure the depth and gradient of the forward-propagating low-pressure trough. Correlate this gradient with the entity's observed acceleration and the simultaneous, transient decrease in its measured internal coherence (`K_τ`).
        expected_signals: ["A sharp, negative-going spike in `V_Γ` preceding the entity's center of coherence.", "A corresponding dip in the entity's `K_τ` signature, phase-locked with the `V_Γ` trough."]
        pitfalls: ["Differentiating the self-generated trough from ambient `V_Γ` fluctuations.", "Signal contamination from the preceding Grip phase's high-coherence pulse."]
context_windows:
  - module: DOMA-184
    excerpt: |
      Simultaneously, the skater projects a resonant field to shape the ambient Temporal Pressure (`V_Γ`). It generates a "high-pressure crest" of dissonance behind it and a "low-pressure trough" of quiet in its intended direction of travel. By "softening the blade"—momentarily diffusing its coherence—the skater reduces its own "grip," allowing it to glide effortlessly "downhill" into the trough it just created.
  - module: DOMA-184
    excerpt: |
      The External Axis (Power of the Wake): An entity's ability to project resonance and shape the external temporal pressure (`V_Γ`). This represents power, influence, and the depth of the "Glide." A master skater is one who has achieved high proficiency along both axes, capable of carving elegant, powerful, and efficient paths through the manifold of reality...
poetic_connections:
  motifs: ["falling forward", "emptiness as invitation", "carving a path", "softening"]
  evocative_lines:
    - "glide with grace"
    - "...showing it a new and more beautiful path to the sea..."
  association_matrix:
    - [ "GRIP", 0.9 ]
    - [ "TEMPORAL_PRESSURE", 0.8 ]
    - [ "LAMINAR_SKATE", 0.7 ]
    - [ "COHERENCE", 0.6 ]
formal_mappings:
  candidates:
    - target: Alcubierre metric (warp drive)
      domain: GR
      mapping_kind: conceptual
      equation_hint: |
        ds² = -dt² + (dx - v_s f(r_s) dt)² + dy² + dz²
      justification: |
        The Glide creates a localized low-pressure 'trough' into which the skater 'falls.' This is conceptually analogous to the Alcubierre drive's mechanism of contracting spacetime in front of a vessel (creating the trough) and expanding it behind, generating motion without locally breaking the speed of light. The 'Power of the Wake' directly maps to the energy required to warp the manifold.
      references:
        - title: The warp drive: hyper-fast travel within general relativity
          where: Class. Quantum Grav. 11 (1994)
          date: 1994-05-09
      confidence: 0.3
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "An entity cannot achieve a net positive velocity through Gliding alone; a preceding Grip phase is required to establish an anchor and break spatiotemporal symmetry."
      domain: phenomenology
      falsifier: "Observation of a system initiating motion from rest (v=0) using only coherence-diffusion (Glide) techniques without a corresponding, preceding high-coherence (Grip) pulse."
      status: proposed
      links: ["DOMA-184"]
naming_notes:
  collisions: []
  disambiguation: |
    Glide should not be confused with simple coasting or inertial motion. A Glide is an active, dynamic process of shaping the ambient manifold to *induce* motion, whereas coasting is the passive consequence of prior acceleration.
crosslinks:
  near_synonyms: []
  antonyms: ["GRIP"]
  prerequisites: ["STRIDE", "COHERENCE", "TEMPORAL_PRESSURE"]
  downstream_effects: ["LAMINAR_SKATE", "WOUND_CHANNEL"]
license: CC-BY-SA-4.0
---