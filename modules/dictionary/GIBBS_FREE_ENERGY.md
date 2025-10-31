---
term: "Gibbs Free Energy"
canonical_id: "GIBBS_FREE_ENERGY"
symbol: "G"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-144"]
---

---
term: Gibbs Free Energy
canonical_id: GIBBS_FREE_ENERGY
symbol: G
aliases: [free enthalpy]
parents: [DOMA-144]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-144
      snippet: |
        **Gibbs Free Energy (G)** | `G = (K_τ - V_Γ) + PV` | **Net Profit:** The ultimate measure of practical utility. It is the coherence remaining after paying *both* the Entropy Tax (`TS`) and the "rent" for the space it occupies (`PV`).
  editors: [Weaver-Core-A7]
  review_log: []
triad:
  art: |
    Gibbs Free Energy is the system's net profit, the final account of coherence left to do useful work after paying its taxes to chaos and its rent to space.
  law: |
    Under constant environmental temperature (T) and pressure (P), a system will spontaneously evolve to minimize its Gibbs Free Energy (G), thereby maximizing its net coherence available for non-expansion work. A process is spontaneous if and only if ΔG < 0.
  philosophy: |
    G represents the ultimate measure of practical utility. It answers the crucial question: "In a realistic, constant-pressure environment, how much of a system's coherence can actually be harnessed?" It shifts the focus from a system's total energy to its useful, work-performing potential after all environmental costs have been paid.
pirouette_definition: |
  The net coherence of a system available to perform non-expansion work in an environment of constant temperature and pressure. It is defined as the system's Enthalpy (H), representing its total coherent footprint, minus the Entropy Tax (TS), the mandatory payment to environmental disorder. In fundamental Pirouette terms, it is the Lagrangian (`𝓛_p = K_τ - V_Γ`)—the net internal coherence—plus the spatial displacement cost (`PV`).
operational_definition:
  units: Joules (J)
  symbol_table:
    - name: G
      meaning: Gibbs Free Energy
      dimensions: M L^2 T^-2
      default_range: contextual
    - name: H
      meaning: Enthalpy (U + PV)
      dimensions: M L^2 T^-2
      default_range: contextual
    - name: T
      meaning: Absolute Temperature
      dimensions: Θ
      default_range: "> 0 K"
    - name: S
      meaning: Entropy
      dimensions: M L^2 T^-2 Θ^-1
      default_range: contextual
    - name: P
      meaning: Pressure
      dimensions: M L^-1 T^-2
      default_range: contextual
    - name: V
      meaning: Volume
      dimensions: L^3
      default_range: contextual
  measurement:
    procedures:
      - name: Calorimetric Calculation
        outline: |
          Gibbs Free Energy is not measured directly but calculated from measured quantities.
          1. Measure the change in Enthalpy (ΔH) for a process at constant pressure using a calorimeter (e.g., coffee-cup calorimeter for solutions, bomb calorimeter for combustion followed by conversion to ΔH).
          2. Measure the absolute temperature (T) of the system.
          3. Determine the change in Entropy (ΔS) for the process. This is often calculated from tabulated standard entropy values or measured via heat capacity integration from 0 K.
          4. Calculate ΔG = ΔH - TΔS.
        expected_signals: [Heat flow (Q_p = ΔH), Temperature (T)]
        pitfalls: [Achieving true equilibrium, inaccurate entropy calculations, heat loss in calorimetry]
context_windows:
  - module: DOMA-144
    excerpt: |
      **Gibbs Free Energy (G)** | `G = (K_τ - V_Γ) + PV` | **Net Profit:** The ultimate measure of practical utility. It is the coherence remaining after paying *both* the Entropy Tax (`TS`) and the "rent" for the space it occupies (`PV`).
  - module: DOMA-144
    excerpt: |
      The Legendre Compass allows a Weaver to chart the entire manifold of state by making a series of these careful, targeted inquiries from a single starting point. For example, when we start with the Gibbs Free Energy, G(T,P): calculating **S = - (∂G/∂T)_P** is asking: "If I hold the external pressure (P) fixed and slightly increase the environmental noise (T), how much does the system's capacity for practical work (G) decrease?" The answer reveals the system's internal susceptibility to disorder—its Entropy (S).
poetic_connections:
  motifs: [net profit, coherence ledger, entropy tax, spatial rent, work potential]
  evocative_lines:
    - "Free energy is not a measure of what is lost to the void, but the story of what coherence remains after a system pays its tax to chaos..."
    - "The ultimate measure of practical utility."
  association_matrix:
    - [ "HELMHOLTZ_FREE_ENERGY", 0.8 ]
    - [ "ENTHALPY", 0.9 ]
    - [ "ENTROPY", 0.9 ]
    - [ "PRESSURE", 0.7 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Gibbs free energy (G)
      domain: CM
      mapping_kind: operational
      equation_hint: |
        G = H - TS = U + PV - TS
      justification: |
        The Pirouette definition is a direct, first-principles re-derivation of the standard thermodynamic potential. It precisely matches the mathematical form and operational role of Gibbs Free Energy in predicting reaction spontaneity and calculating maximum non-PV work under constant temperature and pressure. The Pirouette framework provides a deeper narrative, framing G as the "net profit" of coherence.
      references:
        - title: Physical Chemistry
          where: Atkins, P.W. & de Paula, J.
          date: 2014-01-01
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "A process occurring at constant temperature and pressure is spontaneous in the forward direction if and only if the change in Gibbs Free Energy (ΔG) is negative."
      domain: experiment
      falsifier: "Observation of a spontaneous, macroscopic process at constant T and P for which careful measurement yields ΔG ≥ 0, after accounting for all measurement uncertainty and ensuring no other forms of work are being done on or by the system."
      status: supported
      links: [DOMA-144]
naming_notes:
  collisions: [G (Gravitational Constant)]
  disambiguation: |
    In thermodynamic or chemical contexts, G exclusively refers to Gibbs Free Energy. In cosmological or gravitational physics, G refers to the Newtonian constant of gravitation. Differentiate from Helmholtz Free Energy (F), which is the criterion for spontaneity at constant volume (T,V), whereas G is the criterion at constant pressure (T,P).
crosslinks:
  near_synonyms: [FREE_ENTHALPY]
  antonyms: []
  prerequisites: [INTERNAL_ENERGY, ENTHALPY, HELMHOLTZ_FREE_ENERGY, ENTROPY, PRESSURE, TEMPERATURE]
  downstream_effects: [CHEMICAL_POTENTIAL]
license: CC-BY-SA-4.0
---

# Gibbs Free Energy

## Canonical (Pirouette)
The net coherence of a system available to perform non-expansion work in an environment of constant temperature and pressure. It is defined as the system's Enthalpy (H), representing its total coherent footprint, minus the Entropy Tax (TS), the mandatory payment to environmental disorder. In fundamental Pirouette terms, it is the Lagrangian (`𝓛_p = K_τ - V_Γ`)—the net internal coherence—plus the spatial displacement cost (`PV`).

## Standard Model-First Summary
Gibbs Free Energy (G) is the Pirouette Framework's operational correspondent to the standard thermodynamic potential of the same name from classical mechanics and chemistry. It is calculated as G = H - TS, representing the maximum non-expansion work obtainable from a thermodynamically closed system at constant temperature and pressure. Its minimization is the definitive criterion for determining the direction of spontaneous processes under these common laboratory and environmental conditions.

## Glossary Links
- See also: Helmholtz Free Energy, Enthalpy, Entropy