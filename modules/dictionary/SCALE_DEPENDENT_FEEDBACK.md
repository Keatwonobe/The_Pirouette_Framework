---
term: "Scale-Dependent Feedback"
canonical_id: "SCALE_DEPENDENT_FEEDBACK"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-006"]
---

---
term: Scale-Dependent Feedback
canonical_id: SCALE_DEPENDENT_FEEDBACK
symbol: F(K_τ, ρ, r)
aliases: []
parents: [MATH-006]
children: []
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-006
      lines: "§2"
      snippet: |
        The core physical assumption is that Temporal Pressure Gamma is not a static background value. It is the sum of the ambient environmental pressure (Gamma_env) and a term that depends on the system's own state. We define the feedback law as: Gamma(r) = Gamma_env + lambda * F(K_tau, rho, r)
  editors: [autogenerator-v1]
  review_log: []
triad:
  art: |
    The universe as a self-regulating arena where a particle's attempt to escape only pulls its leash tighter. To exist as part of a whole is to be bound by the echo of your own resonance. The more a system's components try to separate, the more intensely the space between them insists they belong together.
  law: |
    Local Temporal Pressure (Γ) is not a static background; it includes a term proportional to the system's own resonant intensity (K_τ) at its characteristic scale (r). This feedback causes the effective potential V(r) to acquire a linear term (b*r), leading to a constant, non-diminishing restoring force at large distances. The strength of confinement is a direct measure of the feedback coupling.
  philosophy: |
    This mechanism reveals that fundamental forces like confinement are not externally imposed rules but emergent properties of a system's relationship with itself. It transforms the paradox of asymptotic freedom and confinement into the necessary physics of integrity and belonging. The universe builds its own walls out of the very act of trying to leave.
pirouette_definition: |
  The core process by which a system's own resonant intensity (K_τ) and characteristic scale (r) dynamically modify its local Temporal Pressure (Γ). This feedback loop, expressed as Γ(r) = Γ_env + λ·F(K_τ, ρ, r), is the source of the linear confinement term (b*r) in the effective potential V_eff(r) = a/r + b*r. It is the unifying mechanism responsible for both asymptotic freedom at small scales (weak feedback) and confinement at large scales (dominant feedback).
operational_definition:
  units: The feedback function F is typically dimensionless, giving the coupling constant λ units of Temporal Pressure (T⁻¹).
  symbol_table:
    - name: Γ(r)
      meaning: Local Temporal Pressure as a function of scale r
      dimensions: T⁻¹
      default_range: contextual
    - name: λ
      meaning: Feedback coupling constant
      dimensions: T⁻¹
      default_range: > 0 for confinement
    - name: F(K_τ, ρ, r)
      meaning: Dimensionless feedback function
      dimensions: dimensionless
      default_range: contextual; increases with r
    - name: V_eff(r)
      meaning: Effective potential energy
      dimensions: M L² T⁻²
      default_range: contextual
    - name: b
      meaning: Linear confinement coefficient (proportional to λ)
      dimensions: M L T⁻² (Force)
      default_range: > 0 for confinement
  measurement:
    procedures:
      - name: Potential Reconstruction from Bound State Spectra
        outline: |
          1. Observe the energy levels of a two-body bound system (e.g., quarkonium).
          2. Use inverse scattering or lattice simulation methods to reconstruct the effective potential V(r) that produces these energy levels.
          3. Fit the reconstructed potential to the form V_eff(r) = a/r + b*r.
          4. A statistically significant, non-zero value for the linear coefficient `b` confirms the presence and magnitude of Scale-Dependent Feedback.
        expected_signals: [A potential curve V(r) that becomes linear for large r, A constant force F(r) = -b at large r]
        pitfalls: [Insufficient energy range to distinguish the linear term from the Coulombic term, Contamination from higher-order relativistic effects]
context_windows:
  # Short, trimmed context quotes harvested from modules (3–6 sentences each).
  - module: MATH-006
    excerpt: |
      This module demonstrates that the paradoxical nature of the strong nuclear force—near-perfect freedom at close range and inescapable confinement at a distance—is not a paradox at all, but the logical outcome of a scale-dependent feedback loop. We will formalize the feedback mechanism where a system's own resonant intensity (K_tau) alters its local Temporal Pressure (Gamma).
  - module: MATH-006
    excerpt: |
      The linear confinement term, b*r, is the direct mathematical consequence of the feedback loop F becoming dominant at larger distances r. This term represents the energy stored in the field between the confined particles. The force does not diminish with distance. It approaches a constant, non-zero value.
poetic_connections:
  # Lightweight "word-association graph" and sticky lines.
  motifs: [leash, arena walls, self-regulation, echo, integrity, belonging]
  evocative_lines:
    - "Confinement is not a wall, but a leash."
    - "The mathematics of the Gladiator are the physics of belonging."
  association_matrix:
    # symmetric or directed; weights in [0,1]
    - [ "GLADIATOR_FORCE", 0.9 ]
    - [ "TEMPORAL_PRESSURE", 0.8 ]
    - [ "CONFINEMENT", 0.9 ]
    - [ "ASYMPTOTIC_FREEDOM", 0.7 ]
formal_mappings:
  # Candidate alignments to EFT/SM/CM/GR terms, each with justification and refs.
  candidates: []
  adopted:
    - target: QCD string tension (σ) and running coupling (α_s)
      domain: SM
      mapping_kind: mathematical
      equation_hint: |
        V_eff(r) = b*r + a/r  <==>  V_QCD(r) ≈ σ*r - (4/3) * (α_s(r)/r)
      justification: |
        The linear term `b*r` in the Pirouette potential directly maps to the `σ*r` term in the Cornell potential for quarkonium, where `σ` is the QCD string tension. The `a/r` term corresponds to the Coulomb-like one-gluon exchange, with the scale-dependence of `a` modeling the running of the coupling constant α_s. The feedback mechanism provides a physical origin for the phenomenological string tension.
      references:
        - title: Spectrum of Charmed Quark-Antiquark Bound States
          where: Phys. Rev. Lett. 34, 369 (1975)
          date: 1975-02-10
      confidence: 0.9
constraints_and_falsifiers:
  claims:
    - statement: "All systems exhibiting a linear confinement potential (F(r) → constant as r → ∞) are governed by a scale-dependent feedback loop acting on their local temporal pressure."
      domain: theory
      falsifier: "The discovery of a confined system where the potential is linear, but direct probes of the local spacetime metric show no corresponding modification or gradient in the temporal component. Alternatively, a complete theory of confinement (e.g., from first principles in QCD) that does not require a feedback mechanism."
      status: proposed
      links: [MATH-006]
naming_notes:
  collisions: [The term "feedback" is generic in control theory and engineering.]
  disambiguation: |
    Distinguish from generic control-theory feedback. In Pirouette, this term specifically refers to the process where a system's *own state* at a given *scale* alters the fundamental background field (Temporal Pressure) that governs its dynamics, creating the potential well in which it resides. It is not an external corrective signal but an intrinsic, self-generating constraint.
crosslinks:
  near_synonyms: []
  antonyms: [SCALE_INVARIANCE]
  prerequisites: [TEMPORAL_PRESSURE, RESONANT_INTENSITY]
  downstream_effects: [GLADIATOR_FORCE, CONFINEMENT, ASYMPTOTIC_FREEDOM, TEMPORAL_FORGE]
license: CC-BY-SA-4.0
---

# Scale-Dependent Feedback

## Canonical (Pirouette)
The core process by which a system's own resonant intensity (K_τ) and characteristic scale (r) dynamically modify its local Temporal Pressure (Γ). This feedback loop, expressed as Γ(r) = Γ_env + λ·F(K_τ, ρ, r), is the source of the linear confinement term (b*r) in the effective potential V_eff(r) = a/r + b*r. It is the unifying mechanism responsible for both asymptotic freedom at small scales (weak feedback) and confinement at large scales (dominant feedback).

## EFT-First Summary
Scale-Dependent Feedback is the Pirouette Framework's proposed mechanism for the origin of QCD confinement. The feedback loop generates an effective potential V(r) containing a linear term `b*r`, which is mathematically analogous to the `σ*r` term in the Cornell potential for quarkonium, where `σ` is the QCD string tension. This maps the abstract feedback process to the measurable, constant force between quarks at large distances, providing a physical explanation for why quarks are permanently confined within hadrons.

## Glossary Links
- See also: [Temporal Pressure](link), [Gladiator Force](link), [Confinement](link)