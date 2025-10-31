---
term: "Optimal Policy Placement Radius"
canonical_id: "OPTIMAL_POLICY_PLACEMENT_RADIUS"
symbol: "r_p"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["SOCIO-FIELD-002"]
---

---
term: Optimal Policy Placement Radius
canonical_id: OPTIMAL_POLICY_PLACEMENT_RADIUS
symbol: r_p
aliases: [Resonance Radius]
parents: [SOCIO-FIELD-002]
children: [SOCIO-POLICY-001, DOMA-096]
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
        where (\Delta E_{coh}) is the coherence energy restored per unit resource (R).
        Empirically, (r_p \approx r_c) (the coherence core boundary) minimizes systemic expenditure while maximizing coherence flux recovery.
  editors: [Pirouette-Agent-v2.3]
  review_log: []
triad:
  art: |
    The gentle tap on the keystone that settles the arch, not the hammer blow that shatters it. It is the acupuncturist's needle, placed not where the pain is loudest, but where the system's energy is most blocked, restoring flow with minimal effort.
  law: |
    The optimal radius `r_p` for an intervention is that which maximizes the ratio of restored coherence energy to expended resources, found where the derivative of this efficiency with respect to radius is zero. Empirically, `r_p` is located near the coherence core boundary `r_c`.
  philosophy: |
    To intervene effectively is to intervene wisely. This radius replaces brute-force action with precise, resonant leverage, affirming that the location of an action can be more critical than its magnitude. It shifts policy from a logic of power to a logic of systemic harmony and efficiency.
pirouette_definition: |
  The Optimal Policy Placement Radius, `r_p`, is the characteristic distance from the center of a coherence-critical region (`Ω_c`) at which a targeted intervention yields the maximum restoration of coherence energy (`ΔE_coh`) per unit of expended resource (`R`). It is mathematically defined as the radius `r` that extremizes the coherence-resource efficiency function, `d/dr(ΔE_coh / R) = 0`. Operationally, it identifies the spatial boundary where systemic leverage is highest, allowing for the most efficient stabilization of a social dissonance field approaching its curl threshold (`Θ_c`).
operational_definition:
  units: meters (m), or dimensionless in abstract graph topologies.
  symbol_table:
    - name: r_p
      meaning: Optimal Policy Placement Radius
      dimensions: L
      default_range: contextual
    - name: ΔE_coh
      meaning: Change in Coherence Energy
      dimensions: ML²T⁻²
      default_range: contextual
    - name: R
      meaning: Expended intervention resources
      dimensions: context-dependent (e.g., energy, capital, person-hours)
      default_range: contextual
    - name: r_c
      meaning: Coherence core boundary radius
      dimensions: L
      default_range: contextual
  measurement:
    procedures:
      - name: Resonance Scan
        outline: |
          1. Identify a coherence-critical region `Ω_c` where the Curl Threshold `Θ` is elevated.
          2. Define a standardized unit of intervention resource `R`.
          3. Deploy simulated or real-world test interventions at varying radii `r` from the region's center.
          4. Measure the post-intervention relaxation rate of `Θ` or another proxy for `ΔE_coh`.
          5. Plot the efficiency metric `(ΔE_coh / R)` as a function of `r`. The peak of this curve identifies `r_p`.
        expected_signals: [A unimodal peak in the efficiency-vs-radius plot, Fastest relaxation time for `Θ` at `r ≈ r_p`]
        pitfalls: [Misidentifying the center of the coherence-critical region, Confounding effects from external fields, Inconsistent definition of resource unit `R`]
context_windows:
  - module: SOCIO-FIELD-002
    excerpt: |
      The optimal policy placement radius (r_p) satisfies: [d/dr(ΔE_coh / R)|r=r_p = 0] where (ΔE_coh) is the coherence energy restored per unit resource (R). Empirically, (r_p ≈ r_c) (the coherence core boundary) minimizes systemic expenditure while maximizing coherence flux recovery.
  - module: SOCIO-FIELD-002
    excerpt: |
      Intervention A/B Testing: Deploy resonance-aligned aid (as defined in SOCIO-FIELD-001) at multiple radii and record post-(Θ) relaxation rates. Criticality Validation: Validate power-law scaling of post-intervention relaxation ((P(τ) ~ τ⁻α)).
poetic_connections:
  motifs: [leverage, acupuncture, resonance, keystone, fulcrum, sweet-spot]
  evocative_lines:
    - "minimizes systemic expenditure while maximizing coherence flux recovery."
    - "antagonistic circulation overpowers cooperative potential"
  association_matrix:
    - [ "COHERENCE_CORE_BOUNDARY", 0.9 ]
    - [ "CURL_THRESHOLD", 0.8 ]
    - [ "RESONANCE_ALIGNED_INTERVENTION", 0.95 ]
formal_mappings:
  candidates:
    - target: Center of Percussion ("sweet spot")
      domain: CM
      mapping_kind: conceptual
      equation_hint: ~
      justification: |
        The center of percussion on a rigid body (e.g., a bat) is the point where an impact produces minimal shock or vibration at the pivot (e.g., the hands). An intervention at `r_p` is analogous to striking the "sweet spot" of a social system, maximizing the desired effect (coherence recovery) while minimizing undesirable systemic recoil or wasted energy.
      references:
        - title: Physics for Scientists and Engineers
          where: Chapter on Rotational Dynamics
          date: ~
      confidence: 0.8
    - target: Impedance Matching
      domain: CM
      mapping_kind: conceptual
      equation_hint: ~
      justification: |
        Impedance matching maximizes power transfer between a source and a load. `r_p` identifies the spatial "impedance" point in a social field where an intervention (source) can most efficiently transfer "coherence energy" (power) to the system (load), minimizing reflection or dissipation of the effort.
      references: ~
      confidence: 0.7
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "An intervention deployed at radius `r_p` will cause a statistically significant faster relaxation of the Curl Threshold (`Θ`) back to baseline compared to interventions of equal resource cost (`R`) deployed at other radii `r ≠ r_p`."
      domain: experiment
      falsifier: "In controlled simulations or real-world A/B tests, the post-intervention relaxation rate of `Θ` shows no significant correlation with the intervention radius `r`, or the optimal radius is highly unstable and unpredictable."
      status: proposed
      links: [SOCIO-FIELD-002, SOCIO-POLICY-001]
naming_notes:
  collisions: [The symbol `r_p` could be confused with a "particle radius" or "pivot radius" in other physics contexts.]
  disambiguation: |
    Within Pirouette, `r_p` specifically refers to *policy placement* and should be distinguished from `r_c`, the *coherence core* boundary, though they are often empirically co-located. The subscript `p` always denotes 'policy' in this context.
crosslinks:
  near_synonyms: [RESONANCE_RADIUS]
  antonyms: [RANDOMIZED_INTERVENTION_ZONE]
  prerequisites: [CURL_THRESHOLD, COHERENCE_ENERGY, COHERENCE_CORE_BOUNDARY]
  downstream_effects: [RESONANCE_ALIGNED_INTERVENTION, GOVERNANCE_PRINCIPLES]
license: CC-BY-SA-4.0
---

# Optimal Policy Placement Radius

## Canonical (Pirouette)
The Optimal Policy Placement Radius, `r_p`, is the characteristic distance from the center of a coherence-critical region (`Ω_c`) at which a targeted intervention yields the maximum restoration of coherence energy (`ΔE_coh`) per unit of expended resource (`R`). It is mathematically defined as the radius `r` that extremizes the coherence-resource efficiency function, `d/dr(ΔE_coh / R) = 0`. Operationally, it identifies the spatial boundary where systemic leverage is highest, allowing for the most efficient stabilization of a social dissonance field approaching its curl threshold (`Θ_c`).

## EFT-First Summary
The Optimal Policy Placement Radius acts as the "center of percussion" or "sweet spot" for a social system. Just as striking a baseball bat at this point maximizes energy transfer to the ball while minimizing sting to the hands, an intervention at `r_p` maximizes the restorative effect on social coherence while minimizing wasteful systemic backlash or resource expenditure. It represents the point of maximum leverage in a turbulent social field, identified by optimizing the efficiency of an intervention.

## Glossary Links
- See also: Curl Threshold, Coherence Core Boundary, Resonance-Aligned Intervention