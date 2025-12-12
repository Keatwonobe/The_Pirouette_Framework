---
term: "Dual Non-Perturbative Track"
canonical_id: "DUAL_NON_PERTURBATIVE_TRACK"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-018"]
---

---
term: Dual Non-Perturbative Track
canonical_id: DUAL_NON_PERTURBATIVE_TRACK
symbol: N/A
aliases: [D7 Requirement, Non-Perturbative Mandate]
parents: [MATH-018]
children: [MATH-020]
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-018
      lines: "D7"
      snippet: |
        D7 — Dual Non‑Perturbative Track
        For observables sensitive to back‑reaction: (i) finite‑element/spectral solvers for the soliton echo problem; (ii) RG coarse‑graining on (Γ,K)‑space. Either track may be used, but at least one is required for claims beyond perturbation.
  editors: [System Agent]
  review_log: []
triad:
  art: |
    When whispers become roars, the theory must abandon simple echoes. It must seek either the true shape of the solitary wave, or grasp the river's changing course from a higher vantage.
  law: |
    Any claim for an observable sensitive to back-reaction must be supported by a calculation using either (i) a direct numerical solver for the full nonlinear field equations (soliton track) or (ii) a Renormalization Group analysis demonstrating control over the strong-coupling flow (RG track). Perturbative calculations alone are insufficient for such claims.
  philosophy: |
    To prevent the misuse of perturbation theory in regimes where its foundational assumptions have broken down. This mandate forces a direct confrontation with nonlinearity, ensuring that Pirouette's predictive power is rigorously tested and not reliant on uncontrolled extrapolation.
pirouette_definition: |
  A normative requirement (MATH-018 D7) that any theoretical claim for observables sensitive to strong coupling or significant back-reaction must be validated by at least one of two approved non-perturbative methods. The two options are: (1) the **soliton track**, which involves direct numerical solution of the full, nonlinear field equations using finite-element or spectral solvers, and (2) the **RG track**, which involves a Renormalization Group coarse-graining analysis of the theory's flow in parameter space to identify fixed points or controlled behavior. Failure to provide a calculation from at least one track invalidates any claims beyond the perturbative regime for the observable in question.
operational_definition:
  units: Not Applicable (methodological rule)
  symbol_table:
    - name: N/A
      meaning: This term is a procedural constraint, not a physical quantity, and has no associated symbol.
      dimensions: N/A
      default_range: N/A
  measurement:
    procedures:
      - name: Soliton Track Validation
        outline: |
          1. Formulate the full nonlinear equations of motion for the fields relevant to the observable.
          2. Implement a numerical solver (e.g., finite-element, spectral) to find stable, finite-energy field configurations (solitons).
          3. Compute the target observable from the properties (e.g., mass, charge distribution) of the converged soliton solution.
          4. Report solver tolerance, convergence metrics, and stability analysis.
        expected_signals: [Converged numerical solution, Stable energy minimum, Quantized topological charges]
        pitfalls: [Numerical instability, Incorrect boundary conditions, Missing relevant field couplings]
      - name: RG Track Validation
        outline: |
          1. Define the theory's action in a parameter space (e.g., over couplings Γ, K).
          2. Compute the beta functions describing the flow of couplings under a change of scale (coarse-graining).
          3. Integrate the RG flow to determine the theory's behavior at the relevant energy scale.
          4. Extract the observable's value from the properties of the theory at its IR fixed point or along its flow.
        expected_signals: [Well-defined IR or UV fixed points, Calculable critical exponents, Controlled flow trajectories]
        pitfalls: [Scheme-dependence artifacts, Uncontrolled/runaway flows indicating triviality, Missing operators in the effective action]
context_windows:
  - module: MATH-018
    excerpt: |
      Summary: [...] Extends to strongly‑coupled and gravitational limits via RG/soliton tracks.
  - module: MATH-018
    excerpt: |
      D7 — Dual Non‑Perturbative Track
      For observables sensitive to back‑reaction: (i) finite‑element/spectral solvers for the soliton echo problem; (ii) RG coarse‑graining on (Γ,K)‑space. Either track may be used, but at least one is required for claims beyond perturbation.
  - module: MATH-018
    excerpt: |
      Interfaces & Impact: [...] Non‑perturbative appendix should register to D7 or explicitly opt out (no claims beyond perturbation).
poetic_connections:
  motifs: [nonlinearity, strong coupling, computational rigor, falsifiability, emergent structure]
  evocative_lines:
    - "Either track may be used, but at least one is required for claims beyond perturbation."
    - "Gladiator feedback → nonlinear self‑coupling term; RG flow on (Γ,K) with fixed‑point structure."
  association_matrix:
    - [ "GLADIATOR_FEEDBACK", 0.8 ]
    - [ "SOLITON_ECHO", 0.8 ]
    - [ "PERTURBATIVE_EXPANSION", -0.9 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Lattice Field Theory (e.g., Lattice QCD)
      domain: QFT
      mapping_kind: operational
      equation_hint: |
        ⟨O⟩ ~ ∫ Dφ O[φ] exp(-S[φ]) / Z
      justification: |
        The soliton track's reliance on direct numerical solution of the full theory on a discretized basis (finite-elements, spectral methods) is operationally analogous to Lattice Field Theory, the primary ab initio method for non-perturbative calculations in the Standard Model. Both replace analytic expansion with direct, computational evaluation of the path integral or equations of motion.
      references:
        - title: Quantum Chromodynamics on the Lattice
          where: C. Gattringer, C. B. Lang
          date: 2010-01-01
      confidence: 0.9
    - target: Functional Renormalization Group (FRG)
      domain: QFT
      mapping_kind: mathematical
      equation_hint: |
        ∂_k Γ_k[Φ] = ½ Tr[ (Γ_k⁽²⁾[Φ] + R_k)⁻¹ ∂_k R_k ]
      justification: |
        The RG track is a direct application of Wilsonian RG principles, mathematically parallel to the FRG/Wetterich equation. Both methods study the full, non-perturbative flow of an effective action as a function of an energy scale, allowing for the study of fixed points, phase transitions, and strong-coupling phenomena beyond the reach of perturbation theory.
      references:
        - title: Introduction to the functional RG
          where: "P. Kopietz, L. Bartosch, F. Schütz"
          date: 2010-01-01
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "For observables sensitive to back-reaction, a calculation using one of the two non-perturbative tracks provides a more reliable prediction than a high-order perturbative calculation."
      domain: phenomenology
      falsifier: "An experiment measures an observable in a strongly-coupled regime, and the result agrees with a divergent perturbative series (e.g., after Borel resummation) but strongly disagrees with the well-converged predictions from both the soliton and RG tracks. This would suggest the non-perturbative formalisms are incorrectly formulated or missing essential physics."
      status: proposed
      links: [MATH-018, MATH-020]
naming_notes:
  collisions: []
  disambiguation: |
    The 'dual' nature of the track refers to the two *alternative* and sufficient methods (solvers or RG) available to satisfy the single non-perturbative requirement. It does not imply that both tracks must be used simultaneously for a given claim. A valid claim beyond perturbation theory requires a result from *at least one* of the two.
crosslinks:
  near_synonyms: []
  antonyms: [PERTURBATIVE_EXPANSION]
  prerequisites: [GLADIATOR_FEEDBACK, TEMPORAL_PRESSURE]
  downstream_effects: [NON_PERTURBATIVE_SOLVERS]
license: CC-BY-SA-4.0