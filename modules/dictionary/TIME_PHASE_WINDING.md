---
term: "Time-Phase Winding"
canonical_id: "TIME_PHASE_WINDING"
symbol: "w"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-QED-003_minimal_coupling_as_clock_synchronization"]
---

---
term: Time-Phase Winding
canonical_id: TIME_PHASE_WINDING
symbol: w
aliases: []
parents: [MATH-QED-003]
children: [MATH-QED-004]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-QED-003_minimal_coupling_as_clock_synchronization
      lines: "§5"
      snippet: |
        If (∮ ∂_μθ,dx^μ ≡ 2π w) (integer **time-phase winding** (w)), then
        [
        2π w ;-; q ∮ A_μ dx^μ ;=; 2π n
        ]
  editors: [GPT-4 (Pirouette Dictionary Agent)]
  review_log: []
triad:
  art: |
    A knot in the river of time. Charge is the toll, paid in integers, for navigating around it and returning to where you started.
  law: |
    The path integral of the time-phase gradient (∂_μθ) around any closed loop must equal 2π times an integer, w. This integer mandates that the observable U(1) holonomy (Φ_A) coupled to a particle of charge q is quantized, such that qΦ_A = 2π(w-n) for some integer n.
  philosophy: |
    Time is not a featureless backdrop; it has a topological structure. Winding is the simplest non-trivial feature of that structure, providing the fundamental reason why charge must exist, be conserved, and appear in discrete packets. It grounds electromagnetism in the geometry of the temporal medium itself.
pirouette_definition: |
  A dimensionless integer topological invariant, `w`, of the background time-phase field (θ). It is defined as `w ≡ (1/2π) ∮_C ∂_μθ dx^μ` for any closed path `C`. The requirement that `w` be an integer ensures the single-valuedness of the physical state. In the presence of a Ki-defect, non-zero `w` around the defect's core acts as a topological source for quantized electric charge by constraining the total holonomy of the coupled U(1) gauge field.
operational_definition:
  units: dimensionless (integer)
  symbol_table:
    - name: w
      meaning: Time-Phase Winding number
      dimensions: dimensionless
      default_range: w ∈ ℤ
    - name: θ(x)
      meaning: Background time-phase field
      dimensions: dimensionless (angle)
      default_range: contextual
    - name: A_μ
      meaning: U(1) gauge potential
      dimensions: M L T⁻² I⁻¹
      default_range: contextual
    - name: q
      meaning: Electric charge
      dimensions: I T
      default_range: integer multiples of e
  measurement:
    procedures:
      - name: Topological Charge Inference via Aharonov-Bohm Effect
        outline: |
          1. Prepare a coherent beam of particles with known charge q (e.g., electrons).
          2. Create a setup where the beam is split and traverses a closed loop C, encircling a region suspected to have non-trivial winding w.
          3. Control or nullify the magnetic flux Φ_B through the loop, thereby controlling the magnetic part of the U(1) holonomy Φ_A = ∮ A_μ dx^μ.
          4. Measure the interference pattern to determine the Aharonov-Bohm phase shift, γ_C.
          5. The total phase is constrained by `γ_C = 2πw - qΦ_A` (mod 2π). By measuring γ_C and Φ_A, the integer w can be inferred.
        expected_signals: [Quantized phase shifts in interference patterns, Discrete jumps in measured holonomy corresponding to paths enclosing different winding numbers.]
        pitfalls: [External magnetic fields creating confounding flux, Decoherence of the test particle's wavefunction, Mischaracterizing the topology of the path C.]
context_windows:
  - module: MATH-QED-003_minimal_coupling_as_clock_synchronization
    excerpt: |
      If (∮ ∂_μθ,dx^μ ≡ 2π w) (integer **time-phase winding** (w)), then the single-valuedness of the physics requires `q Φ_A = 2π(w-n)`, where `Φ_A` is the U(1) holonomy and `n` is another integer. This yields **quantized (q)** tied to the integer winding of the Ki loop.
  - module: MATH-QED-003_minimal_coupling_as_clock_synchronization
    excerpt: |
      **Interpretation:** **charge universality** = **one U(1) time-phase** + **defect winding**. In practice, fixing one species (electron) to charge (-e) sets the unit (q_0); all other charged spinor Ki-defects share the same (|q|) by the single-clock postulate.
poetic_connections:
  motifs: [topology, winding, knot, clock-turn, integer-toll, charge-source]
  evocative_lines:
    - "Charge is how many turns of that internal clock you must make to come back to yourself."
    - "The vertex is just two clocks agreeing on what 'now' means while moving through a living medium of time."
  association_matrix:
    - [ "CHARGE_QUANTIZATION", 0.9 ]
    - [ "AHARONOV_BOHM_EFFECT", 0.9 ]
    - [ "U(1)_GAUGE_SYMMETRY", 0.8 ]
    - [ "KI_DEFECT", 0.6 ]
formal_mappings:
  candidates:
    - target: Winding number / Topological charge
      domain: Math|QFT
      mapping_kind: mathematical
      equation_hint: |
        w = \frac{1}{2\pi i} \oint_C g^{-1} dg, \text{ for } g = e^{i\theta} \in U(1)
      justification: |
        The definition of `w` is formally identical to the winding number that classifies maps from a circle `S¹` (the path `C`) to the group `U(1)` (the space of phases `e^(iθ)`). This is a standard concept in topology used to define topological charges for vortices, skyrmions, and other defects in condensed matter and field theory.
      references:
        - title: Topology, Geometry and Gauge Fields
          where: "Nakahara, M. (2003), Chapter 4"
          date: 2003-01-01
      confidence: 0.95
  adopted:
    - target: Winding number
      rationale: The mathematical structure and physical interpretation as a conserved integer quantity classifying a field's topology is a direct and unambiguous match.
      confidence: 0.95
constraints_and_falsifiers:
  claims:
    - statement: "The time-phase winding `w` is an integer, which is the ultimate source of the observed quantization of electric charge for all fundamental particles."
      domain: theory
      falsifier: "The discovery of a fundamental particle with charge not an integer or rational multiple of `e`, violating the quantization rule `qΦ_A = 2π(w-n)`."
      status: supported
      links: [MATH-QED-003]
    - statement: "All U(1) electric charge originates from the coupling of matter to a single background time-phase field with a topological winding structure."
      domain: theory
      falsifier: "Evidence that different particle families (e.g., leptons vs. quarks) couple to distinct U(1) gauge fields with fundamentally different charge units, breaking the single-clock postulate."
      status: proposed
      links: [MATH-QED-003]
naming_notes:
  collisions: [The symbol 'w' is sometimes used for work, and is visually similar to omega 'ω' used for frequency.]
  disambiguation: |
    Distinguish from angular frequency `ω`. Time-Phase Winding `w` is a dimensionless, integer-valued topological invariant of a static field configuration, not a rate of phase change over time.
crosslinks:
  near_synonyms: [TOPOLOGICAL_CHARGE]
  antonyms: [TRIVIAL_TOPOLOGY]
  prerequisites: [TIME_PHASE_FIELD, KI_DEFECT]
  downstream_effects: [CHARGE_QUANTIZATION, FINE_STRUCTURE_CONSTANT]
license: CC-BY-SA-4.0
---

# Time-Phase Winding

## Canonical (Pirouette)
Time-Phase Winding (`w`) is a dimensionless integer topological invariant of the background time-phase field (θ). It is defined as the normalized path integral of the field's gradient around a closed loop: `w ≡ (1/2π) ∮ ∂_μθ dx^μ`. This integer value quantifies a non-trivial "twist" in the structure of the temporal medium. The existence of non-zero winding around a Ki-defect core necessitates the quantization of electric charge for any matter field coupled to it, thereby acting as the fundamental topological source of the U(1) interaction.

## EFT-First Summary
In the language of effective field theory, Time-Phase Winding corresponds to a **topological charge** or **winding number** of the background U(1) bundle. This integer (`w`) contributes directly to the Aharonov-Bohm phase, `γ = 2πw - qΦ_A`, where `q` is electric charge and `Φ_A` is the standard U(1) holonomy. The requirement that physics be single-valued (`e^(iγ) = 1`) forces charge `q` to be quantized in units that make the total phase an integer multiple of 2π. This mechanism provides a geometric origin for the Dirac quantization condition.

## Glossary Links
- See also: [Charge Quantization](<...>), [Ki-Defect](<...>), [U(1) Gauge Symmetry](<...>), [Aharonov-Bohm Effect](<...>)