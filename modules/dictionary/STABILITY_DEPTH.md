---
term: "Stability Depth"
canonical_id: "STABILITY_DEPTH"
symbol: "Δ𝓛_p"
aliases: [Inter-Modal Barrier Height]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-185"]
---

---
term: Stability Depth
canonical_id: STABILITY_DEPTH
symbol: Δ𝓛_p
aliases: [Inter-Modal Barrier Height]
parents: [DOMA-185]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-185
      lines: "§3"
      snippet: |
        **Stability Depth (Δ𝓛_p)** | The height of the mode's peak relative to the lowest surrounding transition saddle. It is a direct measure of the mode's resistance to perturbation. A deeper basin requires more disruption to exit. | `Inter-Modal Barrier Height`, `Γ Confinement`
  editors: [GPT-4]
  review_log: []
triad:
  art: |
    A state's stability is the depth of its gravity well. It is the height of the walls one must climb to escape a familiar valley and see a new landscape. The deeper the well, the stronger the habit.
  law: |
    The minimum perturbation required to induce a transition from a stable mode is proportional to its Stability Depth. A system will not spontaneously cross a transition saddle; it must be pushed over the edge with a dissonant injection exceeding Δ𝓛_p.
  philosophy: |
    Stability Depth measures resilience, not quality. It quantifies a system's commitment to a specific mode of being, separating transient preferences from deeply ingrained, robust behaviors. It reveals how much a system must be challenged before it is forced to change.
pirouette_definition: |
  The difference in the Pirouette Lagrangian (𝓛_p) between the peak of a modal basin (𝓛_p,m) and the lowest adjacent transition saddle (𝓛_p,s) on the Coherence Manifold. It is a direct, quantitative measure of a mode's resistance to decohering perturbations, representing the coherence "cost" of initiating a state transition. A large Δ𝓛_p signifies a robustly stable state.
operational_definition:
  units: Units of 𝓛_p (dimensionless coherence units or context-scaled).
  symbol_table:
    - name: Δ𝓛_p
      meaning: Stability Depth.
      dimensions: Same as 𝓛_p.
      default_range: "> 0"
    - name: 𝓛_p,m
      meaning: Pirouette Lagrangian at the mode's peak (local maximum).
      dimensions: Same as 𝓛_p.
      default_range: contextual
    - name: 𝓛_p,s
      meaning: Pirouette Lagrangian at the lowest-lying transition saddle adjacent to the mode.
      dimensions: Same as 𝓛_p.
      default_range: contextual
  measurement:
    procedures:
      - name: Transition Induction Titration
        outline: |
          1.  Establish the system in a target stable mode (resonant pattern Ki_m).
          2.  Measure the baseline Coherence Height (𝓛_p,m).
          3.  Apply a calibrated Dissonant Injection (a perturbation of known magnitude and form).
          4.  Incrementally increase the perturbation's magnitude until a state transition is reliably induced.
          5.  The minimal perturbation magnitude that triggers the leap is a direct proxy for Δ𝓛_p. Alternatively, if the Coherence Manifold can be mapped, Δ𝓛_p is calculated directly as 𝓛_p,m - 𝓛_p,s.
        expected_signals: [Time series of system state variables, perturbation signal, computed 𝓛_p]
        pitfalls: [Stochastic noise can cause premature transitions, underestimating Δ𝓛_p. The system may possess multiple exit pathways (saddles) of varying heights; this procedure might only find the lowest one.]
context_windows:
  - module: DOMA-185
    excerpt: |
      **Stability Depth (Δ𝓛_p)** | The height of the mode's peak relative to the lowest surrounding transition saddle. It is a direct measure of the mode's resistance to perturbation. A deeper basin requires more disruption to exit.
  - module: DOMA-185
    excerpt: |
      Persistence in a mode carves a **Wound Channel** (CORE-011) into the manifold, geometrically deepening its basin over time. This increases the `Stability Depth`, making the state a "habit" that is gravitationally harder to leave. It is the memory of the state.
poetic_connections:
  motifs: [well, valley, barrier, habit, inertia, resilience, escape, threshold]
  evocative_lines:
    - "A deeper basin requires more disruption to exit."
    - "It is the memory of the state."
    - "To transition from one mode to another, a system must traverse one of these regions of lower coherence..."
  association_matrix:
    - [ "COHERENCE_MANIFOLD", 0.9 ]
    - [ "STATE_TRANSITION", 0.9 ]
    - [ "WOUND_CHANNEL", 0.8 ]
    - [ "COHERENCE_HEIGHT", 0.5 ]
formal_mappings:
  candidates:
    - target: Activation Energy (E_a) / Potential Energy Barrier (ΔE)
      domain: Chemistry|CM
      mapping_kind: operational
      equation_hint: |
        Transition Rate ∝ exp(-Δ𝓛_p / T_eff)
      justification: |
        Stability Depth plays the identical functional role as the activation energy barrier in chemical kinetics (e.g., Arrhenius equation) or the potential barrier in Kramers' escape rate problem. It is the energetic or coherence-based "cost" that must be paid by a perturbation or fluctuation to overcome the stability of the current state and induce a transition.
      references:
        - title: 'Theory of the Rate of Chemical Reactions'
          where: 'Eyring, H. J. Chem. Phys. 3, 107 (1935)'
          date: 1935-02-01
      confidence: 0.9
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The probability of a noise-induced state transition is exponentially suppressed by the Stability Depth."
      domain: phenomenology
      falsifier: "If systems with high Δ𝓛_p are observed to transition as frequently as systems with low Δ𝓛_p under similar noise conditions, the claim that Δ𝓛_p governs resilience is false."
      status: proposed
      links: [DOMA-185]
naming_notes:
  collisions: [ΔE, ΔU in physics]
  disambiguation: |
    Stability Depth (Δ𝓛_p) must not be confused with Coherence Height (𝓛_p,m). Coherence Height is an *absolute* measure of a mode's internal efficiency and quality. Stability Depth is a *relative* measure of a mode's resilience against its surroundings on the manifold. A mode can have a very high Coherence Height but a low Stability Depth, making it a high-quality but fragile state.
crosslinks:
  near_synonyms: [INTER_MODAL_BARRIER_HEIGHT]
  antonyms: []
  prerequisites: [COHERENCE_MANIFOLD, PIROUETTE_LAGRANGIAN, MODAL_BASIN, TRANSITION_SADDLE]
  downstream_effects: [STATE_TRANSITION, WOUND_CHANNEL]
license: CC-BY-SA-4.0