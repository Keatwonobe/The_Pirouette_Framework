---
term: "Triadic Phase Coupling Index"
canonical_id: "TRIADIC_PHASE_COUPLING_INDEX"
symbol: "TPCI"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-17"
provenance: ["COG-RES-001"]
---

---
term: Triadic Phase Coupling Index
canonical_id: TRIADIC_PHASE_COUPLING_INDEX
symbol: TPCI
aliases: []
parents: [COG-RES-001]
children: []
status: draft
version: 0.1
last_updated: 2025-10-17
provenance:
  sources:
    - module: COG-RES-001
      lines: "§5"
      snippet: |
        1. Triadic Phase Coupling Index (TPCI):
           [TPCI = |⟨e^(i(Φ₃ - Φ₁ - Φ₂))⟩|]
           Measures stability of the triadic phase relationship.
  editors: [GeneratorAgent-01]
  review_log: []
triad:
  art: |
    Three dancers lock into a shared rhythm, a silent agreement stabilizing their motion against the noise of the world. It is the hum of a chord held true, the signature of a transient, resonant whole.
  law: |
    The TPCI is the magnitude of the time-averaged complex exponential of the triadic phase difference (Φ₃ - Φ₁ - Φ₂). A TPCI near 1 indicates a stable, phase-locked triad, while a TPCI near 0 indicates phase incoherence.
  philosophy: |
    TPCI provides the primary, falsifiable link between the abstract Ki-addition constraint and measurable neural dynamics. It operationalizes the concept of 'resonance', turning a metaphor into a quantitative tool for identifying the coherent structures hypothesized to underpin conscious access.
pirouette_definition: |
  The Triadic Phase Coupling Index (TPCI) is a scalar metric, bounded between 0 and 1, that quantifies the degree of phase synchronization among three oscillating signals (f₁, f₂, f₃) that satisfy the Ki-addition frequency constraint (f₃ ≈ f₁ + f₂). It is calculated as the absolute value of the time-averaged complex exponential of the relative phase (Φ₃ - Φ₁ - Φ₂). A high TPCI value (approaching 1) signifies a stable, locked phase relationship, which is a key signature of a resonance-locked triad and a proposed correlate of conscious access.
operational_definition:
  units: Dimensionless
  symbol_table:
    - name: TPCI
      meaning: Triadic Phase Coupling Index
      dimensions: dimensionless
      default_range: "[0, 1]"
    - name: Φ_k
      meaning: Instantaneous phase of the k-th frequency component
      dimensions: dimensionless
      default_range: "[0, 2π)"
    - name: "⟨...⟩"
      meaning: Time-averaging operator
      dimensions: n/a
      default_range: n/a
  measurement:
    procedures:
      - name: EEG/MEG Time-Frequency Analysis
        outline: |
          1. Record neural data (e.g., high-density EEG) during a cognitive task.
          2. Apply time-frequency decomposition (e.g., Morlet wavelets) to extract instantaneous phase series (Φ₁(t), Φ₂(t), Φ₃(t)) for candidate frequency triads satisfying f₃≈f₁+f₂.
          3. Over a sliding time window, compute the relative phase ψ(t) = Φ₃(t) - Φ₁(t) - Φ₂(t) (mod 2π).
          4. Calculate TPCI as the magnitude of the mean resultant vector of the relative phase: TPCI = |(1/N) Σ exp(iψ(t))| for N samples in the window.
        expected_signals: [Sharp TPCI ridge (>0.7) in the (f₁,f₂) frequency plane, Time-locked TPCI increase correlated with conscious report]
        pitfalls: [Low signal-to-noise ratio in phase estimation, Improper window selection for time-averaging, Spectral leakage smearing frequency components]
context_windows:
  - module: COG-RES-001
    excerpt: |
      1. Triadic Phase Coupling Index (TPCI): [TPCI = |⟨e^(i(Φ₃ - Φ₁ - Φ₂))⟩|]. Measures stability of the triadic phase relationship.
  - module: COG-RES-001
    excerpt: |
      Analysis Pipeline: 1. Compute time-frequency decomposition via Morlet wavelets. 2. Extract instantaneous phases for candidate triads. 3. Calculate TPCI and CAV over sliding windows. 4. Correlate TPCI with conscious report timing.
poetic_connections:
  motifs: [resonance, coherence, synchronization, triad, locking, harmony]
  evocative_lines:
    - "Consciousness is modeled as the maintenance of a Coherence Conservation Triple."
    - "Sharp TPCI ridge in the (f₁,f₂) plane"
  association_matrix:
    - [ "KI_ADDITION_CONSTRAINT", 0.9 ]
    - [ "COHERENCE_AREA", 0.8 ]
    - [ "CONSCIOUS_ACCESS", 0.7 ]
formal_mappings:
  candidates:
    - target: Biphase / Bicoherence
      domain: Math
      mapping_kind: mathematical
      equation_hint: |
        B(f₁, f₂) = ⟨X(f₁)X(f₂)X*(f₁+f₂)⟩ / Norm.
      justification: |
        Bicoherence is a normalized third-order statistic that measures quadratic phase coupling. The TPCI is mathematically equivalent to the biphase, the complex argument of the bicoherence numerator, which directly quantifies the consistency of the triadic phase relationship. This provides a direct bridge to standard nonlinear time series analysis.
      references:
        - title: Digital Bispectral Analysis and Its Applications to Nonlinear Wave Phenomena
          where: IEEE Transactions on Plasma Science, 1979
          date: 1979-06-01
      confidence: 0.95
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "TPCI values are significantly elevated for neural frequency triads satisfying the Ki-addition rule during periods of stable, reported conscious perception compared to non-report periods or phase-scrambled controls."
      domain: experiment
      falsifier: "Failure to observe a statistically significant correlation between TPCI elevation and conscious report timing. Or, finding that TPCI is equally high for frequency combinations that violate the Ki-addition rule."
      status: proposed
      links: [COG-RES-001]
naming_notes:
  collisions: []
  disambiguation: |
    TPCI measures the *stability* or *consistency* of the triadic phase relationship, not its absolute value. It is distinct from Coherence Area (A_Ki), which is an integrated energy-phase volume; a stable, high TPCI is a necessary but not sufficient condition for a conserved A_Ki.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [KI_ADDITION_CONSTRAINT]
  downstream_effects: [COHERENCE_AREA_VARIANCE]
license: CC-BY-SA-4.0
---

# Triadic Phase Coupling Index

## Canonical (Pirouette)
The Triadic Phase Coupling Index (TPCI) is a scalar metric, bounded between 0 and 1, that quantifies the degree of phase synchronization among three oscillating signals (f₁, f₂, f₃) that satisfy the Ki-addition frequency constraint (f₃ ≈ f₁ + f₂). It is calculated as the absolute value of the time-averaged complex exponential of the relative phase (Φ₃ - Φ₁ - Φ₂). A high TPCI value (approaching 1) signifies a stable, locked phase relationship, which is a key signature of a resonance-locked triad and a proposed correlate of conscious access.

## EFT-First Summary
TPCI is operationally equivalent to the biphase consistency index used in nonlinear time series analysis to detect quadratic phase coupling. This mapping grounds the Pirouette Framework's core experimental signature in established signal processing techniques, allowing for direct comparison with methods used to study nonlinear wave interactions in fields like plasma physics and fluid dynamics. In this context, a high TPCI signifies that three wave modes are nonlinearly interacting in a stable, phase-locked manner.

## Glossary Links
- See also: [[Ki-Addition Constraint]], [[Coherence Area]], [[Consciousness Access Protocol]]