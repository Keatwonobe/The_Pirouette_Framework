---
term: "Surveyor's Problem"
canonical_id: "SURVEYOR_S_PROBLEM"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-186"]
---

---
term: Surveyor's Problem
canonical_id: SURVEYORS_PROBLEM
symbol: 
aliases: [Surveyor's Art, Sparse Inference, Coherence Surveying]
parents: [DOMA-186]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-186
      lines: "L22-L24"
      snippet: |
        The Surveyor's Problem is the inverse: given a few points *on* that path, what is the shape of the landscape the path traverses?
  editors: [AgentPrime]
  review_log: []
triad:
  art: |
    How does one map a river's course from a handful of water? The problem lies not in the scarcity of data, but in learning to see the landscape's shape reflected in the water's flow.
  law: |
    Given a sparse set of time-ordered state vectors {x(t₁), x(t₂), ...}, one can infer the qualitative ratio of Temporal Coherence (K_τ) to Temporal Pressure (V_Γ) in the system's Lagrangian. The path's internal regularity (e.g., low variance, periodicity) is a proxy for K_τ, while its overall dispersion and volatility is a proxy for V_Γ.
  philosophy: |
    The Surveyor's Problem reframes sparse data from a limitation to a clue. It replaces the brittle goal of quantitative parameter estimation with the more robust and profound goal of qualitative diagnosis, shifting the core question from "What are the system's parameters?" to "What is the story of the system's struggle?"
pirouette_definition: |
  The inverse problem of inferring the qualitative shape of a system's Pirouette Lagrangian (`𝓛_p = K_τ - V_Γ`), and thereby its dynamic state, by observing a sparse set of points assumed to lie upon its coherence-maximizing geodesic path. It is solved via the Surveyor's Protocol, a heuristic for diagnosing the balance between a system's internal rhythm (`K_τ`) and the environmental pressure it endures (`V_Γ`).
operational_definition:
  units: Categorical (yields a diagnostic label, e.g., 'Laminar Flow', 'Resilient Struggle').
  symbol_table:
    - name: K_τ
      meaning: Temporal Coherence; inferred from path regularity.
      dimensions: Contextual (often action-like)
      default_range: contextual
    - name: V_Γ
      meaning: Temporal Pressure; inferred from path dispersion/volatility.
      dimensions: Contextual (often action-like)
      default_range: contextual
  measurement:
    procedures:
      - name: Coherence Surveying Protocol
        outline: |
          1. **Posit Geodesic:** Connect observed data points to form a tentative path in state space.
          2. **Assess Rhythm:** Measure the path's internal consistency (e.g., using normalized variance or phase coherence) to infer the strength of `K_τ`. High consistency implies high `K_τ`.
          3. **Assess Pressure:** Measure the path's overall dispersion and volatility (e.g., using a dispersion metric or jump frequency) to infer the magnitude of `V_Γ`. High dispersion implies high `V_Γ`.
          4. **Synthesize Diagnosis:** Map the inferred (High/Low `K_τ`, High/Low `V_Γ`) pair to a canonical dynamic state from `DYNA-001`.
        expected_signals: [Laminar Flow, Turbulent Flow, Resilient Struggle, Coherence Erosion]
        pitfalls: [Misinterpreting instrumental noise as high `V_Γ`, assuming points from different system epochs lie on the same geodesic, having too few points (<3) to establish a credible path.]
context_windows:
  - module: DOMA-186
    excerpt: |
      The Pirouette Lagrangian (CORE-006) states that a system will always evolve along a path that maximizes its coherence. The Surveyor's Problem is the inverse: given a few points *on* that path, what is the shape of the landscape the path traverses? We are not estimating disconnected variables. We are taking a qualitative reading of the two fundamental terms of the system's Lagrangian, `𝓛_p = K_τ - V_Γ`.
  - module: DOMA-186
    excerpt: |
      This entire protocol is a heuristic for solving an inverse problem. Standard physics uses the Lagrangian to predict the path; the Surveyor's Art uses the path to infer the Lagrangian. The final diagnostic statement—"The data suggests a system in a state of Resilient Struggle"—is a direct, physical claim about its governing dynamics.
poetic_connections:
  motifs: [surveying, cartography, reconnaissance, diagnosis from scraps, inverse problem]
  evocative_lines:
    - "How does one map a river's course from a handful of water?"
    - "We sought a formula to calculate the world from scraps of data. Instead, we found a ritual for asking it questions."
  association_matrix:
    - [ "LAGRANGIAN_PIROUETTE", 0.9 ]
    - [ "TEMPORAL_COHERENCE", 0.8 ]
    - [ "TEMPORAL_PRESSURE", 0.8 ]
    - [ "FLOW_DYNAMICS", 0.7 ]
formal_mappings:
  candidates:
    - target: Inverse Problem
      domain: Math|Physics
      mapping_kind: conceptual
      equation_hint: |
        Given data d, find model parameters m: d = G(m).
        Surveyor's Problem: Given path {x(t)}, find Lagrangian 𝓛.
      justification: |
        The process infers underlying causes (the Lagrangian field) from observed effects (the system's path), which is the definition of an inverse problem. This is analogous to inferring a planet's mass from a satellite's orbit or using seismic data to map Earth's interior.
      references:
        - title: Inverse Problem Theory and Methods for Model Parameter Estimation
          where: SIAM, Chapter 1
          date: 2005-01-01
      confidence: 0.9
    - target: System Identification
      domain: Control Theory
      mapping_kind: operational
      justification: |
        System Identification is the discipline of building mathematical models of dynamical systems from measured data. The Surveyor's Problem is a qualitative, heuristic, and physically-grounded approach to System ID, focused specifically on inferring the Lagrangian structure rather than a generic state-space model.
      references:
        - title: System Identification: Theory for the User
          where: Prentice Hall, Chapter 1
          date: 1999-01-01
      confidence: 0.7
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The qualitative diagnosis from the Surveyor's Protocol provides more predictive power about a system's future stability than traditional parameter estimation from the same sparse data."
      domain: phenomenology
      falsifier: "An ensemble of systems where a diagnosis of 'Laminar Flow' (implying stability) consistently precedes catastrophic failure, while a simple regression model on the same data points correctly predicts the failure onset."
      status: proposed
      links: [DOMA-186]
naming_notes:
  collisions: []
  disambiguation: |
    Distinguish between the "Surveyor's Problem," which is the formal inverse problem, and the "Surveyor's Art" or "Protocol," which is the specific heuristic method presented in DOMA-186 for solving it. The Problem is the *what*; the Art is the *how*.
crosslinks:
  near_synonyms: []
  antonyms: [FORWARD_PROBLEM, SIMULATION]
  prerequisites: [LAGRANGIAN_PIROUETTE, TEMPORAL_COHERENCE, TEMPORAL_PRESSURE, FLOW_DYNAMICS]
  downstream_effects: []
license: CC-BY-SA-4.0
---

# Surveyor's Problem

## Canonical (Pirouette)
The inverse problem of inferring the qualitative shape of a system's Pirouette Lagrangian (`𝓛_p = K_τ - V_Γ`), and thereby its dynamic state, by observing a sparse set of points assumed to lie upon its coherence-maximizing geodesic path. It is solved via the Surveyor's Protocol, a heuristic for diagnosing the balance between a system's internal rhythm (`K_τ`) and the environmental pressure it endures (`V_Γ`).

## EFT-First Summary
The Surveyor's Problem is a conceptual and operational mapping of the classic mathematical **Inverse Problem** into the Pirouette Framework. Whereas a forward problem uses a known model (the Lagrangian) to predict data (the path), the Surveyor's Problem uses observed data (a sparse path) to infer the properties of the underlying model (the qualitative shape of the Lagrangian). This approach is common across physics, from geophysics to medical imaging, and here it is used to perform a qualitative diagnosis of a system's dynamic state.

## Glossary Links
- See also: [Lagrangian (Pirouette)](<#LAGRANGIAN_PIROUETTE>), [Temporal Coherence](<#TEMPORAL_COHERENCE>), [Temporal Pressure](<#TEMPORAL_PRESSURE>), [Flow Dynamics](<#FLOW_DYNAMICS>)