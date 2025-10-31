---
term: "Slow-roll Tail"
canonical_id: "SLOW_ROLL_TAIL"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["COSMO-Γ-001_the_early_universe"]
---

---
term: Slow-roll Tail
canonical_id: SLOW_ROLL_TAIL
symbol: V_tail(Γ)
aliases: [dark energy tail]
parents: [COSMO-Γ-001_the_early_universe, COSMO-Γ-000]
children: [COSMO-Γ-CMB, COSMO-Γ-HALO]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: COSMO-Γ-001_the_early_universe
      lines: "§4"
      snippet: |
        We adopt the **quadratic-plus-tail** potentials already allowed in your base module, which yield CDM-like behavior **early** and a **slow-roll** tendency **late** (addressing coincidence without post-hoc tuning)
  editors: [Agent (Pirouette Framework Scribe)]
  review_log: []
triad:
  art: |
    The universe's early, frantic rhythm of oscillation gives way to a final, sustained note. The field's potential flattens into a long, quiet hum, and this whisper of remaining energy gently pushes spacetime apart.
  law: |
    At late times (z ≲ 1), when the Hubble friction `3H` becomes smaller than the effective mass scale of the potential tail, the Γ field's evolution becomes overdamped (`3H\dot\Gamma \approx -V'(\Gamma)`). This forces the equation of state `w_Γ` toward -1, sourcing cosmic acceleration. The precise evolution `w_Γ(z)` is a falsifiable prediction for a given potential shape.
  philosophy: |
    The Slow-roll Tail embodies the principle of dynamical unification, demonstrating how a single field can account for phenomena typically attributed to separate entities (dark matter and dark energy). It resolves the cosmic coincidence problem by making the onset of acceleration a natural, attractor-driven consequence of the field's primordial dynamics, not a fine-tuned initial condition.
pirouette_definition: |
  A feature of the Γ-field potential, `V(Γ)`, characterized by a shallow, low-energy region far from the potential minimum. After the early phase of matter-like oscillations, the field's amplitude decreases until it enters this tail region. Here, Hubble friction dominates the potential's restoring force, causing the field to evolve slowly (slow-roll), with its potential energy `V(Γ)` driving late-time cosmic acceleration. The parameters of the tail are not tuned but are fixed by the `one-shot anchor` that sets the field's present-day abundance.
operational_definition:
  units: Energy density (e.g., GeV^4 in natural units, or dimensionless in Planck units).
  symbol_table:
    - name: V_tail(Γ)
      meaning: The component of the scalar potential V(Γ) responsible for late-time acceleration.
      dimensions: M L⁻¹ T⁻²
      default_range: contextual; determined by cosmological constraints (e.g., Ω_Λ,0).
    - name: w_Γ
      meaning: Equation of state parameter for the Γ field, w_Γ = p_Γ / ρ_Γ.
      dimensions: dimensionless
      default_range: [-1, 1]; approaches -1 during the slow-roll tail phase.
    - name: H
      meaning: Hubble parameter, measuring the cosmic expansion rate.
      dimensions: T⁻¹
      default_range: 70 (km/s)/Mpc at z=0.
  measurement:
    procedures:
      - name: Cosmological Expansion and Growth Probes
        outline: |
          1. Measure the cosmic expansion history `H(z)` using Type Ia supernovae, BAO, and cosmic chronometers.
          2. Measure the growth of structure `fσ_8(z)` using galaxy clustering and weak lensing.
          3. Perform a joint fit of these datasets to a cosmological model including the Γ field, constraining the parameters of `V_tail(Γ)` and the evolution of `w_Γ(z)`.
        expected_signals: [An equation of state `w_Γ(z)` that deviates from -1 at z > 0, A specific, non-zero signal in the late-time Integrated Sachs-Wolfe (ISW) effect of the CMB temperature anisotropy spectrum.]
        pitfalls: [Degeneracy with other dynamical dark energy models (e.g., w0-wa), Systematic errors in astrophysical measurements, Model dependence on the assumed functional form of the tail (e.g., exponential vs. cosine).]
context_windows:
  - module: COSMO-Γ-001_the_early_universe
    excerpt: |
      We adopt the **quadratic-plus-tail** potentials already allowed in your base module, which yield CDM-like behavior **early** and a **slow-roll** tendency **late** (addressing coincidence without post-hoc tuning): Exponential-shallow or **cosine tail** remnants of shift symmetry; parameters `(μ, f, Γ_*)` are **U-class** constants **frozen** by a D3 one-shot anchor.
  - module: COSMO-Γ-001_the_early_universe
    excerpt: |
      **Late-ISW** sign/magnitude fixed by the chosen tail (exponential vs cosine), preregistered with AIC/BIC comparisons against ΛCDM and (w_0w_a)CDM.
poetic_connections:
  motifs: [slow drum, cosmic whisper, dynamical unification, fading echo]
  evocative_lines:
    - "until the tail in V(Γ) slows the drum at late times, whispering as dark energy."
    - "These stages are not stitched together; they are one score, played on a single instrument."
  association_matrix:
    - [ "MISALIGNMENT", 0.8 ]
    - [ "ONE_SHOT_ANCHOR", 0.9 ]
    - [ "LATE_ISW_EFFECT", 0.7 ]
    - [ "COSMIC_COINCIDENCE", 0.9 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Quintessence
      domain: GR
      mapping_kind: conceptual|mathematical
      equation_hint: |
        3H\dot\Gamma \approx -V'(\Gamma)  \implies w_\Gamma \approx -1
      justification: |
        The Slow-roll Tail describes a scalar field slowly evolving in a shallow potential, causing cosmic acceleration. This is the defining mechanism of quintessence models. The Pirouette framework distinguishes itself by embedding this mechanism as the late-time, low-energy limit of a field with a more complex potential that also explains dark matter.
      references:
        - title: Cosmological Tracker Solutions
          where: Phys.Rev.D 59, 123504 (1999) [arXiv:astro-ph/9807002]
          date: 1998-07-01
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The parameters of the Slow-roll Tail, fixed by a `one-shot anchor`, can produce the observed late-time acceleration without violating early-universe constraints from Big Bang Nucleosynthesis (BBN)."
      domain: phenomenology
      falsifier: "If the parameter set required to match Ω_Γ,0 predicts a residual dark radiation component (ΔN_eff) that is inconsistent with measured primordial D/H and He-4 abundances, the model is falsified."
      status: proposed
      links: [COSMO-Γ-001_the_early_universe]
    - statement: "The specific shape of the potential tail predicts a unique late-time ISW signal in the CMB that is distinguishable from a cosmological constant (Λ)."
      domain: phenomenology
      falsifier: "A high-significance measurement from CMB surveys (e.g., Planck, CMB-S4) showing that the low-ℓ TT spectrum is consistent with ΛCDM and rules out the specific ISW signal predicted by the allowed tail shapes."
      status: under-test
      links: [COSMO-Γ-CMB]
naming_notes:
  collisions: [Slow-roll (inflation)]
  disambiguation: |
    The term "slow-roll" is used here to describe the late-time dynamics of the Γ field driving cosmic acceleration. This is mathematically analogous but physically distinct from the "slow-roll" conditions during primordial inflation, which occurs at vastly higher energy scales in the very early universe.
crosslinks:
  near_synonyms: [DARK_ENERGY_TAIL]
  antonyms: [QUADRATIC_CORE, MATTER_LIKE_OSCILLATIONS]
  prerequisites: [MISALIGNMENT, ONE_SHOT_ANCHOR]
  downstream_effects: [LATE_ISW_EFFECT]
license: CC-BY-SA-4.0
---

# Slow-roll Tail

## Canonical (Pirouette)
A feature of the Γ-field potential, `V(Γ)`, characterized by a shallow, low-energy region far from the potential minimum. After the early phase of matter-like oscillations, the field's amplitude decreases until it enters this tail region. Here, Hubble friction dominates the potential's restoring force, causing the field to evolve slowly (slow-roll), with its potential energy `V(Γ)` driving late-time cosmic acceleration. The parameters of the tail are not tuned but are fixed by the `one-shot anchor` that sets the field's present-day abundance.

## EFT-First Summary
The Slow-roll Tail is the Pirouette implementation of a quintessence field. It models late-time cosmic acceleration via a scalar field (Γ) evolving slowly in a shallow potential (`V_tail`). This mechanism is distinguished by being the late-time phase of a unified dark sector field that behaves like dark matter at early times, with parameters fixed by a non-tunable `one-shot anchor`. The resulting dynamics are observationally constrained by probes of the late-universe expansion history and the Integrated Sachs-Wolfe effect.

## Glossary Links
- See also: `MISALIGNMENT`, `ONE_SHOT_ANCHOR`, `LATE_ISW_EFFECT`, `MATTER_LIKE_OSCILLATIONS`