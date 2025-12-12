---
term: "Usable Coherence"
canonical_id: "USABLE_COHERENCE"
symbol: "K_τ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DYNA-005_coherent_adherence_protocol"]
---

---
term: Usable Coherence
canonical_id: USABLE_COHERENCE
symbol: K_τ
aliases: []
parents: [DYNA-005]
children: [PPS-015, DOMA-QCOMP-001, DOMA-203]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DYNA-005_coherent_adherence_protocol
      snippet: |
        \[
        \max_{\mathcal A}\;\;\underbrace{\mathbf E[\,K_\tau(T_a)\,]}_{\text{usable coherence}}
        -\underbrace{V_\Gamma}_{\text{pressure}}
        -\underbrace{V_{\text{obs}}}_{\text{observer cost}}
        -\lambda\,\underbrace{\mathcal D}_{\text{Dark Residue}}
        \quad \text{s.t.}\;\;\mathcal C_{\mathrm{consent}},\;\mathcal C_{\mathrm{transparency}}.
        \]
  editors: [System Agent]
  review_log: []
triad:
  art: |
    The resonance of a choir that has tuned the room itself. It is not the effort of the conductor, but the emergent harmony that arises when conditions are right, transforming individual voices into a powerful, unified song.
  law: |
    An increase in Usable Coherence, ΔK_τ, for a given system pathway exponentially increases the rate of transition along that pathway, `k = k^0 * exp(ΔK_τ)`. It functions as a catalyst for preferred dynamics.
  philosophy: |
    This term reframes coherence not as a state to be imposed, but as a capability to be unlocked. It represents the productive potential released when a system's components align consensually, turning internal friction into collective capacity. Its maximization under ethical constraints is the central goal of consentful dynamics.
pirouette_definition: |
  The kinetic term in the Pirouette Lagrangian, `K_τ(T_a)`, that quantifies the operational benefit or capability gained from increased system Adherence (`T_a`). It represents the functional, productive outcome of consentful alignment and is the primary objective function to be maximized by the Coherent Adherence Protocol (CAP v2), balanced against costs like pressure (`V_Γ`), observation (`V_obs`), and negative externalities (`D`).
operational_definition:
  units: Joules (J), often normalized to be dimensionless in rate equations.
  symbol_table:
    - name: K_τ
      meaning: Usable Coherence; the kinetic energy component representing functional benefit from adherence.
      dimensions: M L^2 T^-2
      default_range: contextual; positive values indicate a capability gain.
    - name: T_a
      meaning: Adherence; the squared magnitude of the mean phase over a system manifold.
      dimensions: dimensionless
      default_range: "[0, 1]"
  measurement:
    procedures:
      - name: Rate Change Inversion
        outline: |
          1. For a specific process (e.g., team task completion, state transition), measure the baseline rate `k^0` in a control environment.
          2. Implement a CAP v2 intervention (e.g., change meeting cadence, adjust UI) designed to increase Adherence (`T_a`). Simultaneously, measure the change in observer cost, `ΔV_obs`.
          3. Measure the new, stabilized rate `k`.
          4. Calculate the change in Usable Coherence by inverting the minimal control law: `ΔK_τ = ln(k/k^0) + ΔV_obs`.
        expected_signals: [Exponential increase in process rate `k`, measurable increase in Adherence `T_a`]
        pitfalls: [Failing to isolate `ΔK_τ` from coercive pressure (`V_Γ`), inaccurate measurement of observer cost `ΔV_obs`, misattributing transient dynamics to a stable rate change.]
context_windows:
  - module: DYNA-005_coherent_adherence_protocol
    excerpt: |
      The protocol goal is to maximize the expected usable coherence, `E[K_τ(T_a)]`, subject to costs and ethical constraints. This reframes alignment as the cultivation of emergent capability, not the imposition of control. `K_τ` is the prize; `V_Γ`, `V_obs`, and `D` are the costs.
  - module: DYNA-005_coherent_adherence_protocol
    excerpt: |
      The minimal control law dictates how `K_τ` shapes system pathways. Given two options, the rates are modified as `k_j = k_j^0 * exp(ΔK_τ^(j)(T_a) - ΔV_obs^(j))`. CAP v2 permits only interventions that disclose the intended `ΔK_τ` channel and its associated observation cost.
poetic_connections:
  motifs: [resonance, harmony, flow, catalysis, unlocked potential]
  evocative_lines:
    - "The room tuned itself."
    - "it changes the *room*, not the throat."
  association_matrix:
    - [ "ADHERENCE", 0.9 ]
    - [ "CONSENT", 0.7 ]
    - [ "DARK_RESIDUE", -0.8 ]
    - [ "TEMPORAL_PRESSURE", -0.6 ]
formal_mappings:
  candidates:
    - target: -ΔG‡ (Negative change in Gibbs free energy of activation)
      domain: Physical Chemistry
      mapping_kind: operational
      equation_hint: |
        `rate ∝ exp(-ΔG‡ / RT)` vs `rate ∝ exp(ΔK_τ)`
      justification: |
        `K_τ` functions operationally as a reduction in the activation barrier for a process. In transition state theory, lowering the activation energy exponentially increases the reaction rate. `K_τ` represents a similar "catalytic" effect on system dynamics, making desired pathways more probable without increasing the base energy/temperature.
      references:
        - title: Eyring equation
          where: Transition state theory
          date: 1935-01-01
      confidence: 0.8
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "For a fixed budget of influence, interventions that increase `K_τ` (via context-shaping) yield a greater increase in a target process rate than interventions that apply direct pressure (`V_Γ`) or increase observation (`V_obs`)."
      domain: experiment
      falsifier: "An A/B test (e.g., T4 Coherence-not-force test) where a CAP v2 intervention shows no significant rate advantage over a coercive or surveillance-based intervention with an equivalent, independently measured cost/energy budget."
      status: proposed
      links: [DYNA-005]
naming_notes:
  collisions: [`K` for kinetic energy is standard. The subscript `τ` is crucial for disambiguation.]
  disambiguation: |
    Distinguish from thermal kinetic energy. `K_τ` is not the energy of random motion, but the *functional capability* unlocked by phase-correlated dynamics (high `T_a`). It is the energy made available *for work* by coherence, analogous to how a laser's coherent photons can perform tasks that a lightbulb's incoherent photons cannot.
crosslinks:
  near_synonyms: []
  antonyms: [DARK_RESIDUE, TEMPORAL_PRESSURE, SHADOW_GAUGE_COST]
  prerequisites: [ADHERENCE, PIROUETTE_LAGRANGIAN]
  downstream_effects: [COHERENT_ADHERENCE_PROTOCOL, INERTIAL_LEAP]
license: CC-BY-SA-4.0
---