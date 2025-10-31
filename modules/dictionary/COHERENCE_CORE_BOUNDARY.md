---
term: "Coherence Core Boundary"
canonical_id: "COHERENCE_CORE_BOUNDARY"
symbol: "r_c"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["SOCIO-FIELD-002"]
---

---
term: Coherence Core Boundary
canonical_id: COHERENCE_CORE_BOUNDARY
symbol: r_c
aliases: []
parents: [SOCIO-FIELD-002]
children: [SOCIO-POLICY-001]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: SOCIO-FIELD-002
      lines: "§6"
      snippet: |
        The optimal policy placement radius (r_p) satisfies:
        [\frac{d}{dr}\left(\frac{\Delta E_{coh}}{R}\right)|_{r=r_p} = 0]
        ...
        Empirically, (r_p \approx r_c) (the coherence core boundary) minimizes systemic expenditure while maximizing coherence flux recovery.
  editors: [System]
  review_log: []
triad:
  art: |
    The shoreline of a calm social sea, where resonant whispers can turn back the rising tide of discord. It is the last, best place to build a lighthouse before the storm.
  law: |
    The optimal radius for resonance-aligned intervention (`r_p`) empirically converges to the Coherence Core Boundary (`r_c`), minimizing systemic expenditure per unit of recovered coherence flux.
  philosophy: |
    To move intervention from a brute-force art to a precise science. By identifying the system's natural leverage point, `r_c` enables governance that is minimally invasive yet maximally effective, respecting systemic integrity while restoring stability.
pirouette_definition: |
  The Coherence Core Boundary (`r_c`) is the empirically determined spatial radius marking the transition from a scalar potential-dominated (cooperative) social region to a curl-dominated (antagonistic) one. It corresponds to the location where the Curl Threshold (`Θ`) approaches its critical value (`Θ_c`) and serves as the optimal placement radius (`r_p`) for resonance-aligned interventions.
operational_definition:
  units: Length (e.g., meters in geo-social contexts, or a dimensionless graph distance).
  symbol_table:
    - name: r_c
      meaning: Coherence Core Boundary
      dimensions: L
      default_range: contextual
    - name: r_p
      meaning: Optimal policy placement radius
      dimensions: L
      default_range: contextual
    - name: Θ
      meaning: Curl Threshold
      dimensions: dimensionless
      default_range: contextual
    - name: Θ_c
      meaning: Critical Curl Threshold
      dimensions: dimensionless
      default_range: contextual
  measurement:
    procedures:
      - name: Boundary Inference via Intervention Sweep
        outline: |
          1. Monitor the Curl Threshold (`Θ`) across a social system using interaction graph data.
          2. Deploy a set of controlled, resource-normalized interventions (`R`) at varying radii `r` from a center of dissonance.
          3. Measure the post-intervention coherence flux recovery (`ΔE_coh`) or the relaxation time of `Θ`.
          4. The radius `r` that maximizes the efficiency `ΔE_coh / R` is identified as `r_p`, providing an empirical estimate for `r_c`.
        expected_signals: [A sharp peak in intervention efficiency at `r ≈ r_c`, Power-law scaling of post-intervention relaxation time `τ`]
        pitfalls: [Confounding variables from simultaneous external shocks, Insufficient data density to resolve the dissonance field `D` accurately, Misidentification of the dissonance center]
context_windows:
  - module: SOCIO-FIELD-002
    excerpt: |
      The optimal policy placement radius (r_p) satisfies the condition of maximum efficiency, where coherence energy restored (`ΔE_coh`) per unit resource (`R`) is extremized. Empirically, `r_p ≈ r_c` (the coherence core boundary) minimizes systemic expenditure while maximizing coherence flux recovery. Intervening inside this boundary is inefficient; intervening outside is often too late.
  - module: SOCIO-POLICY-001
    excerpt: |
      Effective governance protocols must target the Coherence Core Boundary (`r_c`) identified by SOCIO-FIELD-002. Interventions placed deep inside this boundary are wasteful, buffered by systemic inertia. Those placed far outside are caught in the non-linear cascade they are meant to prevent. Targeting `r_c` is the core principle of 'Minimum Effective Resonance'.
poetic_connections:
  motifs: [shoreline, event horizon, meniscus, boundary layer, trim tab]
  evocative_lines:
    - "minimizes systemic expenditure while maximizing coherence flux recovery."
    - "the optimal conditions for resonance-aligned intervention."
  association_matrix:
    - [ "CURL_THRESHOLD", 0.9 ]
    - [ "RESONANCE", 0.8 ]
    - [ "TEMPORAL_PRESSURE", 0.5 ]
formal_mappings:
  candidates:
    - target: Boundary layer
      domain: CM
      mapping_kind: conceptual
      equation_hint: |
        `r_c` is where `|∇ × A|^2` begins to dominate `|∇ϕ|^2`.
      justification: |
        The Coherence Core Boundary marks the transition from a smooth, potential-driven "flow" of social coherence to a turbulent, curl-dominated regime. This is analogous to the boundary layer in fluid mechanics separating laminar flow from widespread vortex shedding and turbulence. Both represent an interface where system dynamics undergo a qualitative shift.
      references: []
      confidence: 0.6
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "Intervention efficacy, measured as coherence restored per unit resource, is maximized when the intervention is placed at the empirically determined Coherence Core Boundary (r_c)."
      domain: phenomenology
      falsifier: "Systematic A/B testing reveals that intervention efficacy is maximized significantly inside the core (r << r_c), far outside it (r >> r_c), or shows no clear spatial dependence."
      status: proposed
      links: [SOCIO-FIELD-002, SOCIO-POLICY-001]
naming_notes:
  collisions: [`r_c` is often used for 'critical radius' in physics (e.g., Schwarzschild radius, critical radius for nucleation).]
  disambiguation: |
    Distinguish from a 'critical radius' in physics, which often implies irreversible collapse or nucleation. The Coherence Core Boundary is not a point of no return but a leverage point for restoration. It marks the *edge* of a stable region, not its center of collapse.
crosslinks:
  near_synonyms: [OPTIMAL_INTERVENTION_RADIUS]
  antonyms: [COHERENCE_SINGULARITY]
  prerequisites: [CURL_THRESHOLD]
  downstream_effects: [POLICY_RESONANCE]
license: CC-BY-SA-4.0
---

# Coherence Core Boundary

## Canonical (Pirouette)
The Coherence Core Boundary (`r_c`) is the empirically determined spatial radius marking the transition from a scalar potential-dominated (cooperative) social region to a curl-dominated (antagonistic) one. It corresponds to the location where the Curl Threshold (`Θ`) approaches its critical value (`Θ_c`) and serves as the optimal placement radius (`r_p`) for resonance-aligned interventions.

## EFT-First Summary
The Coherence Core Boundary (`r_c`) is conceptually analogous to the **boundary layer** in fluid dynamics. It marks the spatial transition where the 'flow' of social coherence shifts from a predictable, laminar state (governed by a scalar potential) to a turbulent, dissipative state dominated by vortices of social antagonism (curl). Interventions are most effective when applied at this layer, similar to how small inputs can steer a large fluid system by acting at the laminar-turbulent interface.

## Glossary Links
- See also: Curl Threshold (Θ), Policy Resonance, Temporal Pressure (Γ)