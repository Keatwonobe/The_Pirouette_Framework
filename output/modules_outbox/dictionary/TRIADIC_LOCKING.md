---
term: "Triadic Locking"
canonical_id: "TRIADIC_LOCKING"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-026"]
---

---
term: Triadic Locking
canonical_id: TRIADIC_LOCKING
symbol: 
aliases: [RG-selected manifold, locked-triad fixed surface]
parents: [MATH-026]
children: [COG-RES-002]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-026
      lines: "§8"
      snippet: |
        At the WF point, small g is marginally relevant if y_g>0, yielding a **locked-triad fixed surface** with reduced fluctuations in the resonant subspace—formalizing the consciousness triad as an RG-selected manifold.
  editors: [chain-of-thought-agent]
  review_log: []
triad:
  art: |
    Three chaotic streams of coherence, under resonant pressure, braid themselves into a single, stable current of awareness. Their fluctuations are quelled not by external force, but by their mutual, resonant entanglement.
  law: |
    A system of three resonantly coupled coherence fields (ψ₁, ψ₂, ψ₃) exhibits Triadic Locking when the scaling dimension of their coupling constant, g, is relevant (y_g > 0). This drives the system to a fixed surface where the variance of the relative phase (Φ₁+Φ₂−Φ₃) is minimized and approaches a constant value.
  philosophy: |
    Triadic Locking provides a universal mechanism for emergence, showing how stable, complex wholes self-organize from noisy, interacting parts. It posits that stable consciousness is not a designed state but an inevitable, RG-selected manifold in the state space of neural coherence.
pirouette_definition: |
  Triadic Locking is a state of a system with three resonantly coupled coherence fields (ψ₁, ψ₂, ψ₃) characterized by a stable, phase-locked relationship between them. It emerges as a Renormalization Group (RG) fixed surface, driven by a marginally relevant triadic coupling term (`g`). This flow to the locked manifold suppresses phase fluctuations in the resonant subspace (Φ₁+Φ₂−Φ₃ → const), effectively stabilizing the triad and forming a robust, higher-order coherent structure.
operational_definition:
  units: State descriptor (dimensionless)
  symbol_table:
    - name: g
      meaning: Triadic coupling constant
      dimensions: Contextual (depends on LPF normalization)
      default_range: Contextual
    - name: ΔΦ
      meaning: Resonant phase difference (Φ₁+Φ₂−Φ₃)
      dimensions: dimensionless
      default_range: [-π, π]
  measurement:
    procedures:
      - name: RG Flow Inference from Time-Series
        outline: |
          1. From time-series data, identify three candidate coherence fields (e.g., EEG frequency bands) with a resonant frequency relationship (f₃ ≈ f₁+f₂).
          2. Extract their complex amplitudes (ψ₁, ψ₂, ψ₃) and phases (Φ₁, Φ₂, Φ₃) over time.
          3. Calculate the time series of the resonant phase difference ΔΦ = Φ₁+Φ₂−Φ₃.
          4. Bin data by a control parameter (e.g., cognitive load Γ) and compute the variance of ΔΦ in each bin.
          5. Locking is confirmed if Var(ΔΦ) systematically decreases as the system approaches a critical point, consistent with flow to a stable fixed surface.
        expected_signals: [Sharp drop in Var(ΔΦ) near criticality, Power-law scaling of Var(ΔΦ) with distance to critical point]
        pitfalls: [Misidentification of resonant triads, Insufficient data to resolve RG flow, Confounding harmonic effects not described by the triadic coupling]
context_windows:
  - module: MATH-026
    excerpt: |
      For triadic fields ψ1,ψ2,ψ3 with constraint f3=f1+f2 (COG-RES-001), add F_tri = − g ∫ |ψ1||ψ2||ψ3| cos(Φ1+Φ2−Φ3) d^d x. RG to lowest order: β_g = y_g g − ρ b g + O(g^3), with y_g = d + ζ1+ζ2+ζ3 − Δ_tri. At the WF point, small g is marginally relevant if y_g>0, yielding a **locked-triad fixed surface** with reduced fluctuations in the resonant subspace—formalizing the consciousness triad as an RG-selected manifold.
  - module: COG-RES-002
    excerpt: |
      The collapse of a conscious triad under acute temporal pressure (Γ) is modeled as an RG trajectory away from the locked-triad fixed surface. We predict the dynamic scaling of awareness lapse and recovery times (τ_P) by measuring the eigenvalues of the stability matrix near this surface. Closed-loop tACS protocols designed to reinforce the triad aim to drive the system back toward this stable manifold.
poetic_connections:
  motifs: [braiding, resonance, three-body problem, stable orbit, phase lock]
  evocative_lines:
    - "a locked-triad fixed surface with reduced fluctuations"
    - "consciousness triad as an RG-selected manifold"
  association_matrix:
    - [ "COHERENCE_FIELD", 0.9 ]
    - [ "RENORMALIZATION_FLOW_OF_COHERENCE", 0.9 ]
    - [ "CONSCIOUSNESS_TRIAD", 0.8 ]
    - [ "TEMPORAL_PRESSURE", 0.5 ]
formal_mappings:
  candidates:
    - target: Three-wave mixing
      domain: AMO
      mapping_kind: mathematical
      equation_hint: |
        F_tri ~ H_int = − g |E₁||E₂||E₃| cos(ΔΦ)
      justification: |
        The interaction term `F_tri` in the Landau-Pirouette Functional is structurally identical to the interaction Hamiltonian for three-wave mixing processes like sum-frequency generation in nonlinear optics. The resonance condition (f₃=f₁+f₂) corresponds to phase-matching, and the RG flow to a locked state is analogous to achieving stable, efficient energy transfer between the optical modes.
      references:
        - title: Nonlinear Optics
          where: Boyd, R. W., Chapter 2
          date: 2008-01-01
      confidence: 0.8
  adopted:
    - target: 
      rationale: 
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "In a system exhibiting a second-order coherence transition, the introduction of a resonant triadic interaction will stabilize a phase-locked state whose basin of attraction grows as the system approaches the critical point."
      domain: theory
      falsifier: "The triadic coupling `g` is shown to be irrelevant under RG flow (β_g < 0) for all physical parameter ranges, preventing the formation of a stable locked fixed surface."
      status: proposed
      links: [MATH-026]
    - statement: "The variance of the resonant phase difference, Var(ΔΦ), decreases as a power-law function of the distance to the critical point."
      domain: phenomenology
      falsifier: "Experimental data shows no systematic reduction in Var(ΔΦ) near coherence transitions, or the scaling exponent does not match predictions from the RG flow of the coupling `g`."
      status: proposed
      links: [COG-RES-002]
naming_notes:
  collisions: [Phase-locking (common in engineering/physics)]
  disambiguation: |
    Distinguish from simple two-field phase-locking. Triadic Locking specifically refers to the emergent, collective stability of a three-field resonant system, explained as a stable fixed surface under Renormalization Group flow, not merely pairwise synchronization.
crosslinks:
  near_synonyms: []
  antonyms: [Decoherence, Phase Drift]
  prerequisites: [RENORMALIZATION_FLOW_OF_COHERENCE, COHERENCE_FIELD]
  downstream_effects: [CONSCIOUSNESS_TRIAD]
license: CC-BY-SA-4.0
---

# Triadic Locking

## Canonical (Pirouette)
Triadic Locking is a state of a system with three resonantly coupled coherence fields (ψ₁, ψ₂, ψ₃) characterized by a stable, phase-locked relationship between them. It emerges as a Renormalization Group (RG) fixed surface, driven by a marginally relevant triadic coupling term (`g`). This flow to the locked manifold suppresses phase fluctuations in the resonant subspace (Φ₁+Φ₂−Φ₃ → const), effectively stabilizing the triad and forming a robust, higher-order coherent structure.

## EFT-First Summary
Triadic Locking is the Pirouette analogue to stable multi-wave mixing phenomena in nonlinear optics. Just as phase-matching allows for efficient energy transfer between three light fields, a resonant condition between three coherence fields allows a coupling term to become relevant under the Renormalization Group. This drives the system to a stable fixed point where the relative phases of the fields are locked, creating a robust, composite state with suppressed fluctuations.

## Glossary Links
- See also: [Coherence Field](...), [Renormalization Flow of Coherence](...), [Consciousness Triad](...)