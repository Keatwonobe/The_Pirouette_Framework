---
term: "Rest"
canonical_id: "REST"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-017"]
---

---
term: Rest
canonical_id: REST
symbol: Ki₀
aliases: ["Baseline State", "Ground State Resonance", "n=0 Mode"]
parents: ["DOMA-017"]
children: ["DYNA-001", "DYNA-002"]
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-017
      snippet: |
        | **Rest** | Spherical Standing Wave | The baseline state of self-preservation (`n=0`). A simple, self-referential Ki pattern that maintains identity against the erosive pressure of Γ. Its action is the pure act of *being*. |
  editors: ["System Agent"]
  review_log: []
triad:
  art: |
    A still point in a turning world. The silent hum of a held note, perfectly sustained against the winds of time. The simple, profound act of continuing to be oneself.
  law: |
    A system is in a state of Rest when its coherence pattern (Ki) is a spherical standing wave satisfying the Pirouette Cycle condition for topological winding number `n=0`. This configuration minimizes its interaction potential (`V_Γ`) and maximizes its temporal self-coherence (`K_τ`), making it the most stable, non-propagating state of being.
  philosophy: |
    Rest is not the absence of action, but the fundamental action of self-preservation. It is the geometric proof that existence is not a given, but a continuous, resonant achievement against the universe's dissipative tendency. All other, more complex actions are built upon this primary verb of identity.
pirouette_definition: |
  Rest is the baseline, quantized coherence mode (Ki₀) corresponding to the `n=0` solution of the Pirouette Cycle integral. Geometrically, it manifests as a self-referential, spherical standing wave. This state represents the most efficient method for a system to maintain its topological identity against the erosive pressure of the Temporal Forge (Γ) by minimizing its environmental potential (`V_Γ`) and maximizing its internal temporal coherence (`K_τ`).
operational_definition:
  units: Dimensionless (state classification)
  symbol_table:
    - name: Ki₀
      meaning: The specific Ki resonance pattern for the Rest state.
      dimensions: Contextual (pattern-dependent)
      default_range: N/A
    - name: n
      meaning: Topological winding number of the resonant pattern.
      dimensions: dimensionless
      default_range: 0 (for Rest)
  measurement:
    procedures:
      - name: Resonant Mode Spectroscopy via Observer's Shadow
        outline: |
          Project a low-intensity, variable-frequency Observer probe (CORE-010) at the target system. Scan the probe's frequency spectrum. A system in a pure state of Rest will exhibit a single, sharp absorption/entrainment peak at a characteristic base frequency (ω₀) with zero harmonic complexity, corresponding to the `n=0` mode. The signal's amplitude is proportional to the system's coherence (`K_τ`), and its narrowness indicates stability against Γ.
        expected_signals: ["A single, narrow, high-amplitude resonance peak at the system's fundamental frequency.", "Absence of Doppler shift (indicating no propagation/Motion)."]
        pitfalls: ["Mistaking a long-lived, complex superposition for a pure Rest state.", "Environmental noise (high Γ) broadening the resonance peak, making it difficult to distinguish from a dissonant state."]
context_windows:
  - module: DOMA-017
    excerpt: |
      **Rest**: The baseline state of self-preservation (`n=0`). A simple, self-referential Ki pattern that maintains identity against the erosive pressure of Γ. Its action is the pure act of *being*.
  - module: DOMA-017
    excerpt: |
      A system in a pure mode like **Rest** or **Bind** has found a deep, local minimum in the potential landscape (`V_Γ`), maximizing its stability and temporal coherence (`K_τ`). The "choice" of an action is not a metaphysical event, but the system settling into the most energetically favorable geometric configuration available to it. Action is the universe's relentless search for the most elegant word.
poetic_connections:
  motifs: ["Stillness", "Identity", "Ground State", "Being", "Hum", "Silence"]
  evocative_lines:
    - "We sought a universe of nouns and found only verbs."
    - "Its action is the pure act of being."
  association_matrix:
    - [ "TEMPORAL_FORGE", 0.9 ]
    - [ "COHERENCE", 0.9 ]
    - [ "MOTION", 0.7 ]
    - [ "IDENTITY", 1.0 ]
formal_mappings:
  candidates:
    - target: Ground state energy / Vacuum state
      domain: QM|QFT
      mapping_kind: conceptual
      equation_hint: |
        H|ψ₀⟩ = E₀|ψ₀⟩
      justification: |
        Rest represents the lowest, most stable energy/action state a system can occupy while maintaining its identity, analogous to the ground state in QM. The `n=0` winding number corresponds to the simplest topological configuration, similar to a vacuum state from which excitations (other 'verbs') emerge.
      references: []
      confidence: 0.7
    - target: Rest Mass (m₀)
      domain: SR
      mapping_kind: conceptual
      equation_hint: |
        E = m₀c²
      justification: |
        The state of Rest corresponds to a system's intrinsic, non-propagating identity, which is conceptually similar to rest mass—the energy a particle has when it is not in motion. In this framework, this 'mass' would be a measure of the system's coherence (`K_τ`) in its `n=0` state.
      references: []
      confidence: 0.6
  adopted:
    - target: Ground State (|ψ₀⟩)
      rationale: The 'Ground State' mapping from QM/QFT best captures the dual nature of Rest as both a state of minimal excitation (`n=0`) and a stable baseline from which all other dynamic states (verbs) are generated. It aligns with the principle of quantization and topological stability.
      confidence: 0.75
constraints_and_falsifiers:
  claims:
    - statement: "The `n=0` spherical standing wave is the unique, most stable, non-propagating coherence mode for any isolated system."
      domain: theory
      falsifier: "Discovery of a different, more stable non-propagating geometry, or evidence that the `n=0` state is not perfectly spherical but has some intrinsic, stable asymmetry. This would imply the 'alphabet' of being starts with a more complex letter."
      status: proposed
      links: ["DOMA-017"]
naming_notes:
  collisions: ["Rest frame (Special Relativity)"]
  disambiguation: |
    In Pirouette, Rest is not merely the absence of motion (a kinematic property), but an active, resonant process of self-maintenance. A system in Motion is also coherent; Rest is the specific `n=0` coherence mode, distinct from the helical `n>0` mode of Motion.
crosslinks:
  near_synonyms: []
  antonyms: ["RELEASE", "MOTION"]
  prerequisites: ["KI_RESONANCE", "TEMPORAL_FORGE", "PIROUETTE_LAGRANGIAN"]
  downstream_effects: ["MOTION", "OBSERVE", "SHARPEN", "SYNTHESIZE", "FORK"]
license: CC-BY-SA-4.0
---

# Rest

## Canonical (Pirouette)
Rest is the baseline, quantized coherence mode (Ki₀) corresponding to the `n=0` solution of the Pirouette Cycle integral. Geometrically, it manifests as a self-referential, spherical standing wave. This state represents the most efficient method for a system to maintain its topological identity against the erosive pressure of the Temporal Forge (Γ) by minimizing its environmental potential (`V_Γ`) and maximizing its internal temporal coherence (`K_τ`).

## EFT-First Summary
Operationally, Rest is analogous to the quantum mechanical **ground state** (`|ψ₀⟩`). It represents the minimum energy configuration required for a system to exist as a coherent entity, characterized by a topological index `n=0`. All other actions or states are treated as excitations from this baseline, with their properties determined by their specific resonant geometry and higher topological numbers.

## Glossary Links
- See also: [[MOTION]], [[KI_RESONANCE]], [[TEMPORAL_FORGE]]