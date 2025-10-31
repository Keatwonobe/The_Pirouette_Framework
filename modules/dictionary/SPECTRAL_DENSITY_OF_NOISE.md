---
term: "Spectral Density of Noise"
canonical_id: "SPECTRAL_DENSITY_OF_NOISE"
symbol: "S_η(ω)"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-008"]
---

---
term: Spectral Density of Noise
canonical_id: SPECTRAL_DENSITY_OF_NOISE
symbol: S_η(ω)
aliases: [Noise Power Spectrum, Power Spectrum of Environmental Noise]
parents: [MATH-008]
children: [MATH-009]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-008
      lines: "L102-104"
      snippet: |
        S_eta(omega) is the power spectrum of the environmental noise eta(t). It tells us how much noise power is present at each frequency omega.
  editors: [chain-of-thought-agent]
  review_log: []
triad:
  art: |
    The background hum of the universe, a spectrum of chaos against which a system's coherent song must be heard. It is the static on the line, the texture of the storm that tests the integrity of a rhythm.
  law: |
    The total degradation of a system's Time-Adherence (1 - T_a) is proportional to the integrated product of the environmental noise spectral density and the system's own frequency-dependent susceptibility, χ(ω).
  philosophy: |
    The spectral density of noise quantifies the structure of chaos, proving that not all disturbances are equal. By revealing which frequencies carry the most disruptive power, it reframes resilience not as brute resistance to force, but as a tuned filtering of a system's environment.
pirouette_definition: |
  The spectral density of noise, S_η(ω), is a function that quantifies the power distribution of environmental stochastic fluctuations, η(t), across angular frequency ω. Within the Pirouette Framework, η(t) represents perturbations to the local Temporal Pressure (Γ). S_η(ω) is a key component of the Fluctuation-Coherence Theorem, where it acts as the source term for the degradation of a system's Time-Adherence (T_a).
operational_definition:
  units: Power / Frequency (e.g., W/Hz). In natural units, [Energy].
  symbol_table:
    - name: S_η(ω)
      meaning: Power of the noise process η per unit angular frequency at ω.
      dimensions: M L² T⁻¹
      default_range: "[0, ∞)"
    - name: η(t)
      meaning: The stochastic noise process, representing fluctuations in Temporal Pressure Γ.
      dimensions: M L⁻¹ T⁻² (same as Pressure)
      default_range: "contextual, often normalized to mean zero"
    - name: ω
      meaning: Angular frequency.
      dimensions: T⁻¹
      default_range: "[0, ∞)"
  measurement:
    procedures:
      - name: Environmental Fluctuation Spectroscopy
        outline: |
          1. Position a calibrated sensor sensitive to fluctuations in the relevant field (e.g., Temporal Pressure Γ) in the system's immediate environment.
          2. Record a time-series of the fluctuations, η(t), with a sampling rate at least twice the highest frequency of interest (Nyquist criterion).
          3. Compute the Fourier Transform of the time-series' autocorrelation function (via Wiener-Khinchin theorem) or apply a windowed FFT algorithm (e.g., Welch's method) to the time-series data to estimate the power spectrum, S_η(ω).
        expected_signals: [Time-series data η(t)]
        pitfalls: [Sensor's own thermal noise floor contaminating the measurement, Insufficient sampling duration leading to poor low-frequency resolution, Spectral leakage due to finite signal windowing]
context_windows:
  - module: MATH-008
    excerpt: |
      The Fluctuation-Coherence Theorem states: Delta T_a is proportional to integral of [ S_eta(omega) * |chi(omega)|^2 ] d(omega). Where... S_eta(omega) is the power spectrum of the environmental noise eta(t). It tells us how much noise power is present at each frequency omega.
  - module: MATH-008
    excerpt: |
      We model the environmental noise as stochastic perturbations eta(t) of the Temporal Pressure Gamma... The evolution of the system's phase phi is no longer a simple deterministic equation, but a stochastic differential equation (SDE) of the Langevin type: d(phi)/dt = f(phi) + sigma(phi) * eta(t).
poetic_connections:
  motifs: [chaos, static, storm, dissonance, environmental texture, background hum]
  evocative_lines:
    - "A system does not break because the force against it is too great, but because the noise is too loud."
    - "how well a system can still hear its own song in the middle of the storm."
  association_matrix:
    - [ "TIME_ADHERENCE", 0.9 ]
    - [ "TEMPORAL_PRESSURE", 0.7 ]
    - [ "FLUCTUATION_COHERENCE_THEOREM", 1.0 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Power Spectral Density (PSD)
      domain: Statistical Mechanics | Signal Processing
      mapping_kind: mathematical
      equation_hint: |
        S_η(ω) = ∫ <η(t)η(t+τ)> exp(-iωτ) dτ
      justification: |
        S_η(ω) is mathematically identical to the Power Spectral Density (PSD) of a stochastic process η(t), defined via the Wiener-Khinchin theorem as the Fourier transform of the process's autocorrelation function. It describes the distribution of the process's power over frequency, a foundational concept in the study of any time-series data or stochastic system.
      references:
        - title: "Statistical Physics, Part 1"
          where: "Landau & Lifshitz, Vol. 5, §121"
          date: 1980-01-01
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The observed degradation in a system's Time-Adherence (ΔT_a) is quantitatively predicted by the Fluctuation-Coherence Theorem, using an externally measured S_η(ω) of its environment as input."
      domain: experiment
      falsifier: "An experiment where a system is subjected to a controlled, engineered noise spectrum S_η(ω) and its measured ΔT_a significantly deviates from the theorem's prediction. A deviation would occur if, for example, ΔT_a scaled non-linearly with the power in S_η(ω) in a regime where the theory predicts linear response."
      status: proposed
      links: [MATH-008]
naming_notes:
  collisions: [S is a common symbol for entropy or action.]
  disambiguation: |
    Distinguish from the system's own power spectrum, S_φ(ω), which describes the frequency content of the system's state path φ(t). S_η(ω) is the spectrum of the *external* environmental noise driving the system, whereas S_φ(ω) is the spectrum of the system's *response*.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [TEMPORAL_PRESSURE]
  downstream_effects: [TIME_ADHERENCE, FLUCTUATION_COHERENCE_THEOREM]
license: CC-BY-SA-4.0
---

# Spectral Density of Noise

## Canonical (Pirouette)
The spectral density of noise, S_η(ω), is a function that quantifies the power distribution of environmental stochastic fluctuations, η(t), across angular frequency ω. Within the Pirouette Framework, η(t) represents perturbations to the local Temporal Pressure (Γ). S_η(ω) is a key component of the Fluctuation-Coherence Theorem, where it acts as the source term for the degradation of a system's Time-Adherence (T_a).

## EFT-First Summary
The Spectral Density of Noise, S_η(ω), is the Pirouette Framework's direct application of the standard Power Spectral Density (PSD) from statistical mechanics and signal processing. It quantifies the power of environmental noise—modeled as fluctuations of the Temporal Pressure field Γ—at each frequency. As established in the Fluctuation-Coherence Theorem, this noise spectrum directly drives the decoherence of a system, making the PSD a critical diagnostic tool for predicting system stability.

## Glossary Links
- See also: Time-Adherence, Temporal Pressure, Fluctuation-Coherence Theorem