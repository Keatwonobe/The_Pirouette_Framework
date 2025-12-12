---
term: "Effective Collisional Proxy"
canonical_id: "EFFECTIVE_COLLISIONAL_PROXY"
symbol: "σ_eff/m"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["COSMO-002"]
---

---
term: Effective Collisional Proxy
canonical_id: EFFECTIVE_COLLISIONAL_PROXY
symbol: σ_eff/m
aliases: []
parents: [COSMO-002]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COSMO-002
      lines: "Section 3 — Predictions & Scaling Laws"
      snippet: |
        P3 — Weak self‑interaction proxy
        An apparent “σ/m” constraint inferred in CDM language maps in Pirouette to a **derived** (non‑tunable) effective collisional proxy σ_eff/m determined by Γ soliton overlap; prediction: σ_eff/m ≲ 0.2 cm² g⁻¹ for Bullet‑like events when V(Γ) is COSMO‑Γ‑000‑frozen.
  editors: [GPT-4]
  review_log: []
triad:
  art: |
    Shadows of particles are cast by a rippling field; their dance of avoidance is mistaken for a touch. The proxy measures the momentum exchanged in this phantom collision, a friction born from pure potential.
  law: |
    In a simulated merger of two Γ-condensates, the resulting separation between the gravitational potential minimum (lensing peak) and the baryonic gas peak corresponds to an effective self-interaction cross-section, σ_eff/m. The value of this proxy is not a tunable parameter but a derived, falsifiable prediction of the frozen Γ-field potential, V(Γ).
  philosophy: |
    This term provides a crucial bridge, demonstrating that a field-theoretic dark matter model can reproduce phenomena traditionally interpreted through a particle lens. It replaces a tunable microphysical parameter (σ/m) with a derived, macroscopic consequence of the field's fundamental dynamics, enhancing the framework's predictive power and ontological economy.
pirouette_definition: |
  A derived, non-tunable quantity that quantifies the effective momentum transfer between two interacting Γ-condensates during a merger. It is defined as the equivalent self-interaction cross-section per unit mass (σ/m) that a particulate dark matter model would require to produce the same lensing-gas centroid offset (Δx). Its value is entirely determined by the frozen Γ-potential V(Γ), the halo structures, and the collision kinematics, serving as a key phenomenological test of the Γ-field model against observational data from cluster mergers.
operational_definition:
  units: cm² g⁻¹ (area per mass)
  symbol_table:
    - name: σ_eff/m
      meaning: Effective collisional proxy
      dimensions: L² M⁻¹
      default_range: 0–0.2 cm² g⁻¹
    - name: V(Γ)
      meaning: Γ-field self-interaction potential
      dimensions: M L⁻¹ T⁻²
      default_range: fixed by COSMO-Γ-000
    - name: Δx
      meaning: Centroid offset between lensing (κ) and X-ray (S_X) peaks
      dimensions: L
      default_range: 10–250 kpc
  measurement:
    procedures:
      - name: Inference from Merger Simulation Equivalence
        outline: |
          1. Select a set of merger parameters (masses, impact parameter, velocity, redshift).
          2. Simulate the merger using the `COSMO-Γ-MERGE` module with the frozen V(Γ) to compute the peak lensing-gas offset, Δx_Γ.
          3. Perform a suite of N-body/hydrodynamic simulations of the identical merger, replacing the Γ-field with particulate dark matter having a variable self-interaction cross-section, σ/m.
          4. The value of σ/m from the particle simulation that reproduces Δx_Γ is defined as the effective collisional proxy, σ_eff/m, for that specific merger configuration.
        expected_signals: [A non-zero Δx_Γ, A characteristic post-merger morphology of separated κ and S_X peaks]
        pitfalls: [Failing to control for baryonic physics (e.g., cooling, AGN feedback) which can also affect offsets, Numerical errors in shock-capturing or gravity solvers mimicking physical separation]
context_windows:
  - module: COSMO-002
    excerpt: |
      Γ condensates behave as effectively collisionless mass components across cluster‑scale encounters; gas shocks and lags. The peak offset Δx ≡ |x_κ − x_X| follows a universal scaling law determined by the Γ halo structure, not by an elastic DM cross‑section. The redshift evolution of Δx and the survival of κ peaks after core passage are fixed by the same parameters that set galactic cores.
  - module: COSMO-002
    excerpt: |
      An apparent “σ/m” constraint inferred in CDM language maps in Pirouette to a derived (non‑tunable) effective collisional proxy σ_eff/m determined by Γ soliton overlap; prediction: σ_eff/m ≲ 0.2 cm² g⁻¹ for Bullet‑like events when V(Γ) is COSMO‑Γ‑000‑frozen. Falsification: Required σ/m to match Δx exceeds σ_eff/m bound from the frozen V(Γ).
poetic_connections:
  motifs: [phantom collision, emergent friction, field interference, structural impedance]
  evocative_lines:
    - "Post‑pericenter, the Γ peaks re‑emerge with fractional mass retention..."
    - "The peak offset ... follows a universal scaling law ... not by an elastic DM cross‑section."
  association_matrix:
    - [ "GAMMA_CONDENSATE", 0.9 ]
    - [ "GAMMA_FIELD_POTENTIAL", 0.9 ]
    - [ "LENSING_GAS_OFFSET", 0.8 ]
formal_mappings:
  candidates:
    - target: Self-Interacting Dark Matter (SIDM) cross-section σ/m
      domain: CM
      mapping_kind: operational
      equation_hint: |
        Δx(SIDM, σ/m) ≈ Δx(Γ-field)  =>  σ_eff/m := σ/m
      justification: |
        The σ_eff/m is explicitly constructed to be the operational equivalent of the SIDM cross-section. It is the value of σ/m that an SIDM model would need to reproduce the astrophysical observables (specifically, lensing-gas offsets in mergers) predicted by the Γ-field dynamics. This provides a direct, quantitative bridge for comparing the phenomenological consequences of the two disparate dark matter paradigms.
      references:
        - title: "Dark Matter Self-Interactions and Halos of Dwarf Galaxies"
          where: "Astrophys. J. 524, L19 (1999)"
          date: 1999-10-10
      confidence: 0.95
  adopted:
    - target: SIDM cross-section σ/m
      rationale: The mapping is definitional within the Pirouette framework as the primary means of comparing Γ-field interaction strength to particle-based models.
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "For cluster mergers, the Γ-field with the frozen potential from COSMO-Γ-000 produces an effective collisional proxy σ_eff/m ≲ 0.2 cm² g⁻¹."
      domain: phenomenology
      falsifier: "An unambiguous measurement of a cluster merger system (e.g., from lensing and X-ray data) that requires σ/m > 0.2 cm² g⁻¹ to explain the observed lensing-gas offset, after accounting for all baryonic and projection effects."
      status: proposed
      links: [COSMO-002]
naming_notes:
  collisions: [The symbol 'σ' is standard for cross-section but also widely used for standard deviation. The context, particularly the division by mass 'm', clarifies its use here.]
  disambiguation: |
    This term does not imply that the Γ-field is composed of particles that undergo physical scattering. It is a proxy that quantifies the emergent, macroscopic resistance to interpenetration of two Γ-condensates due to non-linear field self-interactions. The interaction is mediated by the potential V(Γ), not by two-body collisions.
crosslinks:
  near_synonyms: []
  antonyms: [ELASTIC_CROSS_SECTION]
  prerequisites: [GAMMA_CONDENSATE, GAMMA_FIELD_POTENTIAL]
  downstream_effects: [LENSING_GAS_OFFSET, HALO_SURVIVABILITY]
license: CC-BY-SA-4.0