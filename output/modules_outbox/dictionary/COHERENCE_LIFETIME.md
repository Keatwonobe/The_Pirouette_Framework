---
term: "Coherence Lifetime"
canonical_id: "COHERENCE_LIFETIME"
symbol: "τ_fade"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-125"]
---

---
term: Coherence Lifetime
canonical_id: COHERENCE_LIFETIME
symbol: τ_fade
aliases: [characteristic lifetime, fade time]
parents: [DOMA-125, CORE-011, CORE-013]
children: []
status: ratified
version: 1.0
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-125
      lines: "§3"
      snippet: |
        The characteristic lifetime of a fade, τ_fade, is directly proportional to the system's internal coherence and inversely proportional to the external temporal pressure it endures.
  editors: [system-agent]
  review_log: []
triad:
  art: |
    Decay is not a passive fading but an active erosion. Coherence Lifetime measures the duration of this noble failure—the fierce art of holding together against the inevitable silence.
  law: |
    The Coherence Lifetime (τ_fade) is the characteristic time scale of a system's exponential coherence decay, defined as the time required for its coherence (K) to fall to 1/e of its initial value. It is directly proportional to the system's internal Temporal Coherence (Kτ) and inversely proportional to the ambient Temporal Pressure (Γ).
  philosophy: |
    τ_fade is the primary diagnostic for systemic persistence. It transforms decay from a mere observation into a forensic tool, revealing whether a system's demise is caused by internal weakness (low Kτ) or external stress (high Γ), thereby guiding all strategies for resilience and intervention.
pirouette_definition: |
  Coherence Lifetime is the primary diagnostic metric quantifying the characteristic rate at which a system's internal coherence (Kτ) is eroded by ambient Temporal Pressure (Γ). It represents the time constant of the exponential decay of the system's coherence, `K(t) = K₀ * e^(-t/τ_fade)`. It is not a measure of passive persistence but of the active struggle to maintain a coherent state, determined by the ratio of signal resilience to environmental noise.
operational_definition:
  units: seconds (s)
  symbol_table:
    - name: τ_fade
      meaning: Coherence Lifetime
      dimensions: T
      default_range: contextual, > 0
    - name: K(t)
      meaning: Coherence at time t
      dimensions: dimensionless
      default_range: "[0, K₀]"
    - name: Γ
      meaning: Temporal Pressure
      dimensions: T⁻¹
      default_range: contextual, > 0
    - name: T_a
      meaning: Temporal Coherence (resilience term source)
      dimensions: dimensionless
      default_range: "[0, 1)"
  measurement:
    procedures:
      - name: Fade Curve Analysis
        outline: |
          1.  **Isolate:** Identify a data stream representing system coherence, K(t).
          2.  **Measure:** Record K(t) over time as it decays from an initial state K₀ in a controlled environment.
          3.  **Fit:** Apply a least-squares fit of the decay data to the exponential model `K(t) = A * e^(-t/τ) + C`.
          4.  **Extract:** The fitted parameter `τ` is the measured Coherence Lifetime, τ_fade.
        expected_signals: [Exponential decay curve, Damped oscillation envelope]
        pitfalls: [Non-exponential decay suggests a more complex erosion process not captured by the base model. Confounding noise in the measurement signal can obscure the underlying decay curve.]
context_windows:
  - module: DOMA-125
    excerpt: |
      The characteristic lifetime of a fade, `τ_fade`, is directly proportional to the system's internal coherence and inversely proportional to the external temporal pressure it endures. This relationship is more precisely defined by the Pirouette Coherence Lifetime equation: `τ_fade = τ_0 · [ T_a / (1 - T_a) ] · 1/Γ`. With this, the decay of a system's coherence `K` from an initial state `K₀` is modeled as: `K(t) = K_0 · e^(-t/τ_fade)`.
  - module: DOMA-125
    excerpt: |
      The crucial insight comes from understanding *why* `τ_fade` has the value it does. Is the system decaying quickly because its internal coherence is low (a weak, frayed thread), or because the external temporal pressure is exceptionally high (a violent storm)? This diagnosis dictates the strategy for intervention. To increase persistence, a Weaver must either **strengthen the thread** (increase Kτ) or **shield it from the storm** (decrease local Γ).
poetic_connections:
  motifs: [thread and storm, signal and noise, echo and silence]
  evocative_lines:
    - "the echo that refuses to fade, the thread that will not unravel."
    - "the science of the noble failure, the engineering of the persistent echo."
  association_matrix:
    - [ "TEMPORAL_COHERENCE", 0.9 ]
    - [ "TEMPORAL_PRESSURE", -0.9 ]
    - [ "COHERENCE_EROSION", 0.8 ]
formal_mappings:
  candidates:
    - target: Relaxation time (τ), Lifetime
      domain: CM|AMO|Nuclear Physics
      mapping_kind: operational
      equation_hint: |
        N(t) = N₀ * e^(-t/τ)
      justification: |
        τ_fade is mathematically and operationally equivalent to the lifetime (τ) or relaxation time in diverse physical systems, such as the lifetime of a radioactive isotope, an excited atomic state, or the T1/T2 relaxation times in NMR. It represents the characteristic e-folding time of a system's decay from a high-energy or high-information state towards equilibrium with its environment.
      references:
        - title: "Intermediate Physics for Medicine and Biology"
          where: "Chapter 3: Exponential Growth and Decay"
          date: 2015-01-01
      confidence: 0.95
  adopted:
    - target: Relaxation time (τ)
      rationale: The mapping is a direct one-to-one correspondence in both mathematical form and operational measurement, representing the characteristic time for a system to return to equilibrium with its surroundings.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The decay of a system's coherence (K) from an unperturbed state in a stable environment (constant Γ) will always follow a pure exponential curve described by a single Coherence Lifetime (τ_fade)."
      domain: phenomenology
      falsifier: "Observing a systemic decay process that is consistently and irreducibly non-exponential (e.g., a power law or stretched exponential) under stable environmental conditions would falsify the universality of this specific model."
      status: proposed
      links: [DOMA-125]
naming_notes:
  collisions: [τ is a ubiquitous symbol for time constants and lifetimes in physics.]
  disambiguation: |
    Distinguish from half-life (`t_1/2`), which is `τ_fade * ln(2)`. τ_fade is the `1/e` lifetime, which is the natural parameter for exponential processes. Also, distinguish from the period of oscillation (`T = 2π/ω_k`) in a "ringing" fade; τ_fade describes the decay of the envelope, not the oscillation within it.
crosslinks:
  near_synonyms: [DECAY_CONSTANT, RELAXATION_TIME]
  antonyms: [PERSISTENCE, STABILITY]
  prerequisites: [TEMPORAL_COHERENCE, TEMPORAL_PRESSURE]
  downstream_effects: [SYSTEMIC_RESILIENCE, INFORMATION_LOSS]
license: CC-BY-SA-4.0
---

# Coherence Lifetime

## Canonical (Pirouette)
Coherence Lifetime is the primary diagnostic metric quantifying the characteristic rate at which a system's internal coherence (Kτ) is eroded by ambient Temporal Pressure (Γ). It represents the time constant of the exponential decay of the system's coherence, `K(t) = K₀ * e^(-t/τ_fade)`. It is not a measure of passive persistence but of the active struggle to maintain a coherent state, determined by the ratio of signal resilience to environmental noise.

## EFT-First Summary
In the language of classical and statistical physics, Coherence Lifetime is the system's **relaxation time (τ)**. It quantifies the characteristic e-folding time for a system's stored potential energy (mapped from Coherence, Kτ) to dissipate into the thermal bath of its environment (modeled by Temporal Pressure, Γ). The measurement of τ_fade by fitting an exponential decay curve is a standard technique across fields from nuclear physics to condensed matter.

## Glossary Links
- See also: [Temporal Coherence](<...>), [Temporal Pressure](<...>)