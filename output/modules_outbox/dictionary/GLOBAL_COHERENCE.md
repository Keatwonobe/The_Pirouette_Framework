---
term: "Global Coherence"
canonical_id: "GLOBAL_COHERENCE"
symbol: "C"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["XAP-002_appendix_addendum_014_016"]
---

---
term: Global Coherence
canonical_id: GLOBAL_COHERENCE
symbol: C
aliases: []
parents: [XAP-002_appendix_addendum_014_016]
children: []
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: XAP-002_appendix_addendum_014_016
      lines: "L43-L45"
      snippet: |
        Total Dark‑Residue \(D=\sum_j D_j\). Since each term is non‑positive, \(\dot D≤0\). Because \(C=1-D/S_{in}\), we obtain
        $$\dot C = \frac{\dot D}{S_{in}} ≥ 0.$$
        Thus any diffusion step that lowers local \(D_j\) *necessarily* raises global coherence \(C\).
  editors: [Automated Agent]
  review_log: []
triad:
  art: |
    A measure of a system's internal symphony, where disparate parts resonate in concert. It quantifies the quietening of discord that arises from isolated, high-friction actions.
  law: |
    Any spontaneous, diffusive process within a system that reduces local Dark-Residue will non-locally increase or maintain Global Coherence. The rate of coherence increase, dC/dt, is non-negative and directly proportional to the total rate of Dark-Residue dissipation.
  philosophy: |
    Global Coherence provides a formal basis for systemic altruism. It demonstrates that local optimizations which reduce friction (dissipate Dark-Residue) are not zero-sum but necessarily contribute to the stability and integrity of the whole.
pirouette_definition: |
  A dimensionless, system-wide metric quantifying the overall stability and integration of a system. It is defined as C = 1 - (D / S_in), where D is the total Dark-Residue and S_in is the total integrated entropy influx. C increases as Dark-Residue is dissipated via diffusive processes, approaching a theoretical maximum of 1 in a perfectly equilibrated, zero-residue system.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: C
      meaning: Global Coherence
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: D
      meaning: Total Dark-Residue
      dimensions: Entropy (J/K)
      default_range: contextual
    - name: S_in
      meaning: Total integrated entropy influx
      dimensions: Entropy (J/K)
      default_range: contextual
  measurement:
    procedures:
      - name: Graph-Based Simulation
        outline: |
          1. Model the system as a directed graph G(V,E) with an adjacency matrix A.
          2. Assign initial entropy values S_0 to each node and define the total entropy influx S_in over the measurement period.
          3. At each time step t, calculate the Dark-Residue D_j for each node j using D_j = Σ_k a_jk(S_j - S_k)_+.
          4. Sum to find total Dark-Residue D(t) = Σ D_j(t).
          5. Compute Global Coherence C(t) = 1 - D(t) / S_in.
        expected_signals: [A time-series C(t), typically a non-decreasing monotonic curve under pure diffusion.]
        pitfalls: [Inaccurate graph topology (missing/incorrect edges), incorrectly specified initial entropy state S_0, non-diffusive or external entropy sources not accounted for in S_in.]
context_windows:
  - module: XAP-002_appendix_addendum_014_016
    excerpt: |
      Total Dark‑Residue D = Σ D_j. Since each term is non‑positive, dD/dt ≤ 0. Because C = 1 - D/S_in, we obtain dC/dt ≥ 0. Thus any diffusion step that lowers local D_j *necessarily* raises global coherence C. Altruism—defined as policies accelerating diffusion—maximises the system‑wide dC/dt.
  - module: XAP-002_appendix_addendum_014_016
    excerpt: |
      Dataset `tle_campaign.csv` (12 sessions) yields the trajectory below:
      | Step | C    |
      |------|------|
      | 0    | 0.42 |
      | 4    | 0.58 |
      | 8    | 0.67 |
      | 12   | 0.73 |
poetic_connections:
  motifs: [Harmony, Integration, Systemic Health, Resonance, Stability]
  evocative_lines:
    - "any diffusion step that lowers local D_j *necessarily* raises global coherence C."
    - "Altruism—defined as policies accelerating diffusion—maximises the system‑wide dC/dt."
  association_matrix:
    - [ "Dark-Residue", -0.9 ]
    - [ "System Stability", 0.8 ]
formal_mappings:
  candidates:
    - target: Negative Normalized Relative Entropy
      domain: Math
      mapping_kind: conceptual
      equation_hint: |
        C ~ 1 - D_KL(P || P_eq) / Z
      justification: |
        Dark-Residue D measures the 'excess' entropy at nodes relative to their neighbors, akin to a local disequilibrium. Total D is a sum of these local divergences. C=1-D/S_in then acts like a normalized measure of how close the system is to equilibrium (D=0), conceptually similar to how negative relative entropy (Kullback-Leibler divergence) measures the closeness of a distribution P to an equilibrium distribution P_eq.
      references: []
      confidence: 0.4
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "For any isolated system modeled as a connected graph G and evolving under pure Laplacian diffusion (dS/dt = -LS), the Global Coherence C(t) is a non-decreasing function of time (dC/dt ≥ 0)."
      domain: theory
      falsifier: "A valid counterexample would be a system undergoing pure diffusion where C(t) decreases, which would require Σ dD_j/dt > 0, contradicting the proof in XAP-015."
      status: supported
      links: [XAP-002_appendix_addendum_014_016]
naming_notes:
  collisions: [Capacitance, specific heat capacity, speed of light (c)]
  disambiguation: |
    In Pirouette, C is reserved for Global Coherence. In contexts involving physics, use c for the speed of light. Where electrical concepts are present, use C_cap for capacitance to avoid ambiguity.
crosslinks:
  near_synonyms: []
  antonyms: [DARK_RESIDUE]
  prerequisites: [DARK_RESIDUE, ENTROPY]
  downstream_effects: [SYSTEM_STABILITY]
license: CC-BY-SA-4.0
---

# Global Coherence

## Canonical (Pirouette)
A dimensionless, system-wide metric quantifying the overall stability and integration of a system. It is defined as C = 1 - (D / S_in), where D is the total Dark-Residue and S_in is the total integrated entropy influx. C increases as Dark-Residue is dissipated via diffusive processes, approaching a theoretical maximum of 1 in a perfectly equilibrated, zero-residue system.

## EFT-First Summary
No direct mapping to a standard Effective Field Theory (EFT) term is currently adopted for Global Coherence (C). Conceptually, it functions as a normalized measure of a system's proximity to equilibrium, analogous to measures based on relative entropy or free energy in statistical mechanics. It quantifies the 'usable order' of the system by measuring its deviation from a state of maximal internal friction (Dark-Residue).

## Glossary Links
- See also: Dark-Residue, Entropy, System Stability