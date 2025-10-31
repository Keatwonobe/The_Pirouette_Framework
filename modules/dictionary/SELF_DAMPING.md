---
term: "Self-Damping"
canonical_id: "SELF_DAMPING"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-014"]
---

---
term: Self-Damping
canonical_id: SELF_DAMPING
symbol: C₂
aliases: [Second-order correction, O(α²) self-interaction]
parents: [MATH-013, MATH-014]
children: [MATH-014]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-014
      snippet: |
        We will show that the negative second-order correction arises from a "self-damping" effect, and that a positive third-order correction emerges from a "resonant leak" in that same damping field.
  editors: [GPT-4]
  review_log: []
triad:
  art: |
    An echo of an echo, turning back upon itself to quiet its own vibration. The particle tempers its own exuberance through a geometric sigh, a self-interaction that brings its state closer to stillness and stability.
  law: |
    The universal O(α²) correction to a lepton's anomalous magnetic moment (C₂) is negative. Its inclusion in the g-2 calculation must reduce the discrepancy between the first-order prediction and the experimental value for all leptons, forming a convergent perturbative series.
  philosophy: |
    Self-Damping demonstrates that the framework's geometry contains inherent feedback loops. The particle's interaction with its own history creates a regulatory, stabilizing effect, preventing runaway self-energy and producing a convergent, physically realistic result without ad-hoc renormalization.
pirouette_definition: |
  Self-Damping is the conceptual name for the geometric self-interaction that produces the negative second-order universal correction (C₂) to a lepton's anomalous magnetic moment. It represents a reactive, tempering feedback from the particle's own coherence field, reducing the magnitude of the anomaly predicted by the first-order interaction alone. This effect is the necessary precursor to the third-order "Resonant Leak" phenomenon.
operational_definition:
  units: dimensionless
  symbol_table:
    - name: C₂
      meaning: The numerical coefficient of the (α/π)² term in the universal expansion of a lepton's anomalous magnetic moment.
      dimensions: dimensionless
      default_range: ≈ -0.328
  measurement:
    procedures:
      - name: Asymptotic Refinement of g-2
        outline: |
          1. Calculate the first-order (C₁) contribution to the lepton anomalous magnetic moment, a_ℓ.
          2. Calculate the second-order (C₂) contribution from the framework's geometric self-interaction model.
          3. Form the truncated series a_ℓ⁽²⁾ = C₁(α/π) + C₂(α/π)².
          4. Compare the residuals |a_ℓ⁽¹⁾ - a_ℓ(exp)| and |a_ℓ⁽²⁾ - a_ℓ(exp)| against high-precision experimental data for electrons and muons.
        expected_signals: 
          - The residual for a_ℓ⁽²⁾ is significantly smaller than for a_ℓ⁽¹⁾.
          - The calculated C₂ is negative and consistent with the established Standard Model value.
        pitfalls: 
          - Calculating a positive or flavor-dependent C₂.
          - The C₂ term over-corrects the anomaly, pushing the theoretical prediction further from the experimental value.
context_windows:
  - module: MATH-014
    excerpt: |
      We have established that the electron's anomalous magnetic moment arises from a geometric dialogue with its own past. The first echo gave us the α/2π term. This module pushes deeper, into the subtle harmonics of that echo... We will show that the negative second-order correction arises from a "self-damping" effect, and that a positive third-order correction emerges from a "resonant leak" in that same damping field.
  - module: MATH-014
    excerpt: |
      If your provisional C₂ nudges a_μ **toward** the observed central value before adding Δa_μ(Γ), the combined prediction typically lands **closer** still once the pressuron term is included. This is the desired pattern.
poetic_connections:
  motifs: [feedback loop, self-regulation, geometric friction, echo]
  evocative_lines:
    - "The Anatomy of an Echo"
    - "The particle tempers its own exuberance"
  association_matrix:
    - [ "RESONANT_LEAK", 0.9 ]
    - [ "COHERENCE_FIELD", 0.7 ]
    - [ "SCHWINGER_TERM", 0.5 ]
formal_mappings:
  candidates:
    - target: Two-loop QED correction coefficient for g-2
      domain: SM
      mapping_kind: mathematical
      equation_hint: |
        C₂ = (197/144) + (π²/12) - (π²/2)ln(2) + (3/4)ζ(3) ≈ -0.328478...
      justification: |
        Self-Damping is the Pirouette framework's geometric re-interpretation of the physical processes described by the seven second-order Feynman diagrams in QED contributing to g-2. The predicted numerical coefficient C₂ must match the established QED calculation to high precision to be considered a valid alternative description.
      references:
        - title: "Quantum Electrodynamics"
          where: "Peskin & Schroeder, Chapter 6"
          date: 1995-10-01
      confidence: 0.4
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The Pirouette geometric calculation for the universal second-order g-2 correction (C₂) yields a negative value consistent with the QED result."
      domain: theory
      falsifier: "The calculation yields a positive C₂, a value numerically inconsistent with the QED result, or demonstrates that C₂ is fundamentally lepton-flavor dependent (beyond trivial mass insertions)."
      status: proposed
      links: [MATH-014]
naming_notes:
  collisions: []
  disambiguation: |
    Distinguish from dissipative damping in classical mechanics. Self-Damping is a conservative, geometric effect arising from the particle's interaction with its own past, not an energy loss to an external thermal environment. It is a feature of the particle's quantum vacuum interaction.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [SCHWINGER_TERM]
  downstream_effects: [RESONANT_LEAK, G_MINUS_2_ANOMALY]
license: CC-BY-SA-4.0
---

# Self-Damping

## Canonical (Pirouette)
Self-Damping is the conceptual name for the geometric self-interaction that produces the negative second-order universal correction (C₂) to a lepton's anomalous magnetic moment. It represents a reactive, tempering feedback from the particle's own coherence field, reducing the magnitude of the anomaly predicted by the first-order interaction alone. This effect is the necessary precursor to the third-order "Resonant Leak" phenomenon.

## EFT-First Summary
In the language of the Standard Model, Self-Damping corresponds to the full set of two-loop QED contributions to the lepton anomalous magnetic moment. The Pirouette framework proposes a geometric origin for the processes represented by the seven relevant Feynman diagrams, aiming to derive the well-known numerical coefficient `C₂ ≈ -0.328` from first principles. This term is crucial for achieving percent-level agreement between theory and experiment for the electron's g-2.

## Glossary Links
- See also: Resonant Leak, G-minus-2 Anomaly, Schwinger Term