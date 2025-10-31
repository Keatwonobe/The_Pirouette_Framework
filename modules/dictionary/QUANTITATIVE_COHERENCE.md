---
term: "Quantitative Coherence"
canonical_id: "QUANTITATIVE_COHERENCE"
symbol: "λ"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["DOMA-142"]
---

---
term: Quantitative Coherence
canonical_id: QUANTITATIVE_COHERENCE
symbol: λ
aliases: ["Lyapunov Exponent"]
parents: [DOMA-142, CORE-006]
children: []
status: ratified
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: DOMA-142
      lines: "L38-L40"
      snippet: |
        Lyapunov Exponent (`λ`) | **Quantitative Coherence** | A precise measure of a system's stability. Negative `λ` indicates a stable, Laminar state where perturbations decay. Positive `λ` indicates a chaotic, Turbulent state where perturbations grow exponentially. `λ = 0` marks the "edge of chaos."
  editors: ["Agent: Weaver-Kael"]
  review_log: []
triad:
  art: |
    A measure of a system's music—whether it has settled into a predictable melody (negative λ), devolved into pure noise (positive λ), or balances on the creative edge between the two (λ=0).
  law: |
    The sign of a system's Quantitative Coherence (λ) determines its local stability: λ < 0 for laminar flow where perturbations decay, λ > 0 for turbulent flow where perturbations grow exponentially, and λ = 0 at the bifurcation point between order and chaos.
  philosophy: |
    Quantitative Coherence reframes stability and chaos not as observed phenomena, but as design parameters. It provides the fundamental control variable for Coherence Engineering, allowing a Weaver to sculpt the dynamical landscape of a system to be as stable or as innovative as required.
pirouette_definition: |
  Quantitative Coherence (λ) is the scalar measure of a system's local dynamical stability, quantifying the average exponential rate of divergence or convergence of nearby trajectories. Negative values (λ < 0) indicate stable, Laminar Flow where perturbations are damped. Positive values (λ > 0) indicate unstable, Turbulent Flow where perturbations are amplified. A value of zero (λ = 0) signifies the "edge of chaos," a state of marginal stability often associated with maximal adaptability.
operational_definition:
  units: Dimensionless (for iterative maps) or inverse time (T⁻¹ for continuous systems).
  symbol_table:
    - name: λ
      meaning: Quantitative Coherence
      dimensions: Dimensionless or T⁻¹
      default_range: '[-∞, ln(2)] for logistic map; generally contextual'
  measurement:
    procedures:
      - name: Iterative Map Analysis
        outline: |
          For a 1D iterative map $x_{n+1} = f(x_n)$, calculate the average of the natural logarithm of the absolute value of the map's derivative over a long trajectory:
          $\lambda = \lim_{N\to\infty} \frac{1}{N} \sum_{n=0}^{N-1} \ln|f'(x_n)|$.
        expected_signals: [A stable negative value for periodic orbits, A stable positive value for chaotic regimes, A value fluctuating around zero near bifurcations]
        pitfalls: [Insufficient trajectory length leading to inaccurate average, Numerical instability near critical points (f'(x)=0)]
context_windows:
  - module: DOMA-142
    excerpt: |
      Lyapunov Exponent (`λ`) | **Quantitative Coherence** | A precise measure of a system's stability. Negative `λ` indicates a stable, Laminar state where perturbations decay. Positive `λ` indicates a chaotic, Turbulent state where perturbations grow exponentially. `λ = 0` marks the "edge of chaos."
  - module: DOMA-142
    excerpt: |
      *Adaptability:* "I must find the precise conditions for the 'edge of chaos' (`λ = 0`), the most potent state for adaptation."
      *Managed Chaos:* "I need a turbulent flow with a specific positive coherence gradient (`λ = 0.5`) to foster novelty without systemic collapse."
poetic_connections:
  motifs: [stability, turbulence, edge-of-chaos, resonance, control, music]
  evocative_lines:
    - "We shift from observing the dance of chaos and order to composing the music that compels it."
    - "...the precise whisper that will either calm the storm or call it forth from a clear sky..."
  association_matrix:
    - [ "LAMINAR_FLOW", 0.9 ]
    - [ "TURBULENT_FLOW", 0.9 ]
    - [ "TEMPORAL_PRESSURE", 0.7 ]
    - [ "COHERENCE_ENGINEERING", 0.8 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Lyapunov exponent
      domain: Math
      mapping_kind: mathematical
      equation_hint: |
        $\lambda(x_0) = \lim_{n\to\infty} \frac{1}{n} \sum_{i=0}^{n-1} \ln |f'(x_i)|$
      rationale: |
        The mapping is explicitly defined in DOMA-142 and provides a rigorous, well-understood mathematical foundation for the concept. It measures the exponential rate of separation of infinitesimally close trajectories, which the Framework interprets as the stability or turbulence of a system's Resonant Pattern.
      references:
        - title: Nonlinear Dynamics and Chaos
          where: Strogatz, S. H. (2015). Section 10.3.
          date: 2015-01-01
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "A system's maximal adaptability and potential for novel phase transitions occurs at the 'edge of chaos' where Quantitative Coherence λ ≈ 0."
      domain: phenomenology
      falsifier: "Discovering a class of systems where peak adaptability consistently occurs deep within a stable regime (λ << 0) or a highly chaotic regime (λ >> 0), with no special properties at λ = 0."
      status: proposed
      links: [DOMA-142]
naming_notes:
  collisions: ["The symbol λ is also commonly used for wavelength in physics and eigenvalues in linear algebra. Context is critical."]
  disambiguation: |
    In Pirouette, λ always refers to the stability of a dynamical system's flow, never a spatial wavelength. While related to eigenvalues of stability matrices, it specifically denotes the long-term average exponential growth rate along a trajectory.
crosslinks:
  near_synonyms: []
  antonyms: []
  prerequisites: [TEMPORAL_PRESSURE, RESONANT_PATTERN, LAMINAR_FLOW, TURBULENT_FLOW]
  downstream_effects: [COHERENCE_ENGINEERING]
license: CC-BY-SA-4.0
---

# Quantitative Coherence

## Canonical (Pirouette)
Quantitative Coherence (λ) is the scalar measure of a system's local dynamical stability, quantifying the average exponential rate of divergence or convergence of nearby trajectories. Negative values (λ < 0) indicate stable, Laminar Flow where perturbations are damped. Positive values (λ > 0) indicate unstable, Turbulent Flow where perturbations are amplified. A value of zero (λ = 0) signifies the "edge of chaos," a state of marginal stability often associated with maximal adaptability.

## EFT-First Summary
In mathematical physics, Quantitative Coherence maps directly to the **Lyapunov exponent** (λ), a well-established measure of dynamical instability and sensitivity to initial conditions in chaos theory. The Pirouette Framework operationalizes this mathematical tool as a core instrument for Coherence Engineering, treating it not just as a descriptor of a system but as a targetable parameter for system design. A negative λ corresponds to a stable, predictable system, while a positive λ corresponds to a chaotic one.

## Glossary Links
- See also: [Temporal Pressure](<placeholder>), [Coherence Engineering](<placeholder>), [Laminar Flow](<placeholder>), [Turbulent Flow](<placeholder>)