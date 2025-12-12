---
term: "Coherence-drag effect"
canonical_id: "COHERENCE_DRAG_EFFECT"
symbol: ""
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-Γ-005_the_pressuron_induced_neutrino_mass_mechanism"]
---

---
term: Coherence-drag effect
canonical_id: COHERENCE_DRAG_EFFECT
symbol: (mechanism)
aliases: [temporal drag, coherence damping]
parents: [MATH-Γ-005, MATH-013, DYNA-Γ-004]
children: [DYNA-Γ-NEU-OSC, COSMO-Γ-NEU-SEA]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-Γ-005_the_pressuron_induced_neutrino_mass_mechanism
      lines: "§1"
      snippet: |
        The mechanism treats mass as a **coherence-drag effect**—a retardation of phase flow through the temporal substrate.
  editors: [AI Assistant]
  review_log: []
triad:
  art: |
    A particle's mass is the echo of its own temporal passage. It is the faint resistance felt by a wave's phase as it ripples through the texture of time, a drag not on motion, but on becoming.
  law: |
    A particle's effective mass is inversely proportional to its energy and directly proportional to the variance of the background temporal pressure field, `m(E) ∝ ⟨Γ²⟩ / E`. This effect manifests as a non-sinusoidal, energy-dependent drift in oscillation phenomena.
  philosophy: |
    Mass is not an intrinsic property but an emergent, relational one arising from a particle's interaction with the temporal substrate. This reconceptualizes inertia as a measure of temporal adherence, resolving mass hierarchies without requiring new fundamental particles.
pirouette_definition: |
  The core mechanism in Pirouette by which mass arises from the retardation of a particle's quantum phase evolution due to stochastic interactions with the background temporal pressure field (Γ). The cumulative phase delay, integrated over the particle's coherence length, is perceived as inertial mass. The effect is most pronounced for high-energy, weakly-coupled particles like neutrinos, leading to a characteristic inverse-energy dependence of their mass.
operational_definition:
  units: eV/c², kg
  symbol_table:
    - name: m(E)
      meaning: Energy-dependent effective mass
      dimensions: M
      default_range: 10⁻³ – 10⁻¹ eV/c² (for neutrinos)
    - name: ⟨Γ²⟩
      meaning: Variance of the background temporal pressure field
      dimensions: M²L⁻²
      default_range: contextual (scales with local matter density)
    - name: E
      meaning: Particle energy
      dimensions: ML²T⁻²
      default_range: 1–10 GeV (for accelerator neutrinos)
    - name: g_{Γν}
      meaning: Coupling constant between the Γ field and neutrinos
      dimensions: dimensionless
      default_range: ~10⁻² g_Γ
  measurement:
    procedures:
      - name: Long-baseline oscillation phase-drift analysis
        outline: |
          1. Measure the neutrino energy spectrum at a far detector (e.g., DUNE, Hyper-K) over a wide energy range (1–10 GeV).
          2. Compute the oscillation probability as a function of L/E.
          3. Fit the data to a standard three-flavor sinusoidal oscillation model.
          4. Search for a residual, energy-dependent deviation from the sinusoidal fit, consistent with the `m(E)² ∝ 1/E²` term predicted by coherence drag.
        expected_signals: [A 1–2% non-sinusoidal modulation of oscillation maxima across the 1–10 GeV energy range.]
        pitfalls: [Insufficient statistics to resolve the small effect, systematic errors in energy reconstruction mimicking a drift, confounding new physics in the neutrino sector.]
context_windows:
  - module: MATH-Γ-005_the_pressuron_induced_neutrino_mass_mechanism
    excerpt: |
      In Pirouette, inertial mass measures the **degree of temporal adherence** (T_a). A particle that propagates nearly at c (such as a neutrino) minimally disturbs time and therefore remains nearly massless. However, background temporal pressure fluctuations (the Γ field) introduce a small phase delay δt per cycle, perceived as a nonzero mass... This delay stems from stochastic Γ interactions integrated over the coherence length of the wave packet.
  - module: MATH-Γ-005_the_pressuron_induced_neutrino_mass_mechanism
    excerpt: |
      Because `m_ν(E)` varies with energy, the oscillation phase becomes `ϕ_{ij} = (L/2E) [m_i(E)² - m_j(E)²]`, producing a small **non-sinusoidal modulation** at long baselines. Pirouette predicts an energy-dependent drift of order 1–2 % in oscillation maxima across 1–10 GeV beams—detectable in DUNE or Hyper-Kamiokande with high statistics.
poetic_connections:
  motifs: [temporal friction, phase retardation, echo of passage, coherence damping]
  evocative_lines:
    - "Slowing the heartbeat of their passage through the universe."
    - "The whisper of coherence feeling its own delay."
  association_matrix:
    - [ "TEMPORAL_PRESSURE", 0.9 ]
    - [ "NEUTRINO_MASS", 0.8 ]
    - [ "INERTIA", 0.6 ]
    - [ "COHERENCE", 0.5 ]
formal_mappings:
  candidates:
    - target: Self-energy correction (Σ)
      domain: QFT
      mapping_kind: mathematical
      equation_hint: |
        `m_ν ≡ Re[Σ_ν(E)]/c²`
      justification: |
        The coherence-drag effect is mathematically formulated as the real part of the neutrino self-energy `Σ_ν(E)` arising from integrating out fluctuations of the Γ field. This directly maps to standard QFT techniques where loop-level corrections from field interactions modify a particle's propagator and generate an effective mass.
      references:
        - title: An Introduction to Quantum Field Theory
          where: Chapter 7 (Peskin & Schroeder)
          date: 1995-10-01
      confidence: 0.8
  adopted:
    - target: 
      rationale: 
      confidence: 0.0
constraints_and_falsifiers:
  claims:
    - statement: "Neutrino oscillation probabilities exhibit a 1–2% non-sinusoidal, energy-dependent deviation from standard predictions in long-baseline experiments."
      domain: experiment
      falsifier: "High-statistics measurements at DUNE or Hyper-Kamiokande find that oscillation probabilities are purely sinusoidal within measurement uncertainty, ruling out the predicted `1/E` dependence of `m_ν`."
      status: proposed
      links: [MATH-Γ-005]
    - statement: "The coherence-drag mechanism is sufficient to explain all observed neutrino masses without invoking sterile states."
      domain: phenomenology
      falsifier: "Global fits to all neutrino data (oscillation, beta decay, cosmology) show a persistent, statistically significant preference for a fourth (sterile) neutrino mass state."
      status: proposed
      links: []
naming_notes:
  collisions: []
  disambiguation: |
    Distinguish from decoherence, which involves the loss of phase information to an environment. Coherence-drag is a *unitary* effect that retards the phase evolution coherently across the wave packet. It is also distinct from kinetic friction or atmospheric drag, as it does not dissipate energy but instead stores it as mass.
crosslinks:
  near_synonyms: []
  antonyms: [INTRINSIC_MASS]
  prerequisites: [TEMPORAL_PRESSURE]
  downstream_effects: [NEUTRINO_OSCILLATION_PHASE_DRIFT, COSMOLOGICAL_NEUTRINO_SEA_DAMPING]
license: CC-BY-SA-4.0
---

# Coherence-drag effect

## Canonical (Pirouette)
The core mechanism in Pirouette by which mass arises from the retardation of a particle's quantum phase evolution due to stochastic interactions with the background temporal pressure field (Γ). The cumulative phase delay, integrated over the particle's coherence length, is perceived as inertial mass. The effect is most pronounced for high-energy, weakly-coupled particles like neutrinos, leading to a characteristic inverse-energy dependence of their mass.

## EFT-First Summary
The Coherence-drag effect is a form of dynamical mass generation. In Quantum Field Theory (QFT), it corresponds to a specific momentum-dependent **self-energy correction** to the particle's propagator. Interactions with a background scalar field (Γ) induce a self-energy term `Σ(E)` whose real part manifests as an energy-dependent mass `m(E) ∝ 1/E`. This non-standard energy dependence provides a sharp experimental test in precision oscillation experiments.

## Glossary Links
- See also: [Temporal Pressure](<placeholder>), [Neutrino Mass Hierarchy](<placeholder>)