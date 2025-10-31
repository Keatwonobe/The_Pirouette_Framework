---
term: "Stochastic Differential Equation"
canonical_id: "STOCHASTIC_DIFFERENTIAL_EQUATION"
symbol: ""
aliases: [SDE]
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-008"]
---

---
term: Stochastic Differential Equation
canonical_id: STOCHASTIC_DIFFERENTIAL_EQUATION
symbol: dφ/dt = f(φ) + σ(φ)η(t)
aliases: [SDE, Langevin Equation]
parents: [MATH-008]
children: [MATH-009]
status: draft
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-008
      lines: "L76-L84"
      snippet: |
        We model the environmental noise as stochastic perturbations eta(t) of the Temporal Pressure Gamma. This noise buffets the system's Ki rhythm. The evolution of the system's phase phi is no longer a simple deterministic equation, but a stochastic differential equation (SDE) of the Langevin type:

        d(phi)/dt = f(phi) + sigma(phi) * eta(t)
  editors: [Agent: Pirouette-Dict-Gen]
  review_log: []
triad:
  art: |
    The mathematical score for a dance between deterministic rhythm and chaotic influence. It describes how a system holds its form while being constantly buffeted by the random winds of its environment.
  law: |
    The time evolution of a system's state variable (φ) is governed by the sum of a deterministic drift (f(φ)) driving it toward a stable orbit and a stochastic diffusion term (σ(φ)η(t)) representing environmental noise.
  philosophy: |
    The SDE formalizes the principle that stability is not a static state but an active process of resisting environmental noise. It asserts that a system's evolution is inseparable from its context, transforming coherence from an intrinsic property to a relational, statistical measure.
pirouette_definition: |
  A differential equation that models the time evolution of a system's phase (φ) as it is simultaneously guided by two forces: a deterministic drift term, `f(φ)`, which drives the system toward its stable Ki rhythm, and a stochastic diffusion term, `σ(φ)η(t)`, which represents random fluctuations from the environment (e.g., in Temporal Pressure, Γ). This model is the mathematical foundation for analyzing the degradation of Time-Adherence and for deriving the Fluctuation-Coherence Theorem.
operational_definition:
  units: Dimensionless phase (φ) in a system with natural units (T).
  symbol_table:
    - name: φ(t)
      meaning: System phase variable at time t.
      dimensions: dimensionless
      default_range: "[0, 2π) or context-dependent"
    - name: f(φ)
      meaning: Drift term; deterministic force driving the system to its periodic orbit.
      dimensions: T⁻¹
      default_range: contextual
    - name: σ(φ)
      meaning: Diffusion magnitude; scales the effect of noise on the system.
      dimensions: dimensionless
      default_range: contextual
    - name: η(t)
      meaning: White noise process representing environmental fluctuations.
      dimensions: T⁻¹ᐟ²
      default_range: "Mean 0, variance 1"
  measurement:
    procedures:
      - name: Time-Series Parameter Inference
        outline: |
          1. Acquire a high-resolution time-series of the system's state variable φ(t).
          2. Numerically calculate the instantaneous rate of change Δφ/Δt over short intervals.
          3. Bin the data by the value of φ.
          4. In each bin, compute the mean of Δφ/Δt to estimate the drift term f(φ).
          5. In each bin, compute the variance of Δφ/Δt to estimate the diffusion term σ(φ)².
        expected_signals: [φ(t) time-series]
        pitfalls: [Insufficient sampling rate causing aliasing, non-stationary noise statistics, measurement noise overwhelming intrinsic system noise.]
context_windows:
  - module: MATH-008
    excerpt: |
      We model the environmental noise as stochastic perturbations eta(t) of the Temporal Pressure Gamma. This noise buffets the system's Ki rhythm. The evolution of the system's phase phi is no longer a simple deterministic equation, but a stochastic differential equation (SDE) of the Langevin type:

      d(phi)/dt = f(phi) + sigma(phi) * eta(t)

      Where: f(phi) is the "drift" term, representing the deterministic forces... It pushes the system back towards its stable orbit. sigma(phi) * eta(t) is the "diffusion" term.
  - module: MATH-008
    excerpt: |
      This theorem is the Pirouette Framework's analogue to the fluctuation-dissipation theorem. It provides a direct, causal link: the amount of coherence a system "dissipates" (Delta T_a) is determined by the spectrum of the environmental fluctuations (S_eta) it experiences, filtered through its own internal sensitivity (chi).
poetic_connections:
  motifs: [resilience, signal vs noise, dance with chaos, statistical stability]
  evocative_lines:
    - "A system does not break because the force against it is too great, but because the noise is too loud."
    - "T_a is the measure of how well a system can still hear its own song in the middle of the storm."
  association_matrix:
    - [ "TIME_ADHERENCE", 0.9 ]
    - [ "KI_RHYTHM", 0.8 ]
    - [ "TEMPORAL_PRESSURE", 0.7 ]
    - [ "FLUCTUATION_COHERENCE_THEOREM", 0.9 ]
formal_mappings:
  candidates:
    - target: Langevin Equation
      domain: CM|Math
      mapping_kind: mathematical
      equation_hint: |
        dφ/dt = f(φ) + σ(φ)η(t)
      justification: |
        The Pirouette SDE is explicitly defined as a Langevin-type equation. It models the dynamics of a variable (φ) subject to a deterministic potential-derived force (drift term f(φ)) and a random, fluctuating force (diffusion term ση(t)) from an environment, which is the canonical structure of a Langevin equation.
      references:
        - title: "Stochastic Methods: A Handbook for the Natural and Social Sciences"
          where: "C.W. Gardiner, Chapter 4"
          date: 2009-01-01
      confidence: 0.95
  adopted: []
constraints_and_falsifiers:
  claims:
    - statement: "The degradation of a system's Time-Adherence (ΔT_a) is quantitatively predicted by the Fluctuation-Coherence Theorem, which is derived from this SDE model for its phase dynamics."
      domain: phenomenology
      falsifier: "Experimental observation of a system where ΔT_a does not correlate with the integrated spectral density of environmental noise, or where the phase dynamics exhibit non-Markovian memory effects not captured by the white noise term η(t)."
      status: proposed
      links: [MATH-008]
naming_notes:
  collisions: []
  disambiguation: |
    Distinguish from the Fokker-Planck equation, which describes the time evolution of the probability density function *of* the state variable φ, whereas the SDE describes the trajectory of φ itself. The Pirouette SDE is a specific application of the general mathematical concept, tailored to phase dynamics.
crosslinks:
  near_synonyms: []
  antonyms: [DETERMINISTIC_EQUATION_OF_MOTION]
  prerequisites: [KI_RHYTHM, TEMPORAL_PRESSURE]
  downstream_effects: [TIME_ADHERENCE, FLUCTUATION_COHERENCE_THEOREM]
license: CC-BY-SA-4.0