---
term: "Lattice spacing"
canonical_id: "LATTICE_SPACING"
symbol: "a"
aliases: []
status: "draft"
version: "0.1"
last_updated: "2025-10-18"
provenance: ["MATH-YM-003_nonperturbative_map"]
---

---
term: Lattice spacing
canonical_id: LATTICE_SPACING
symbol: a
aliases: [lattice constant]
parents: [MATH-YM-003_nonperturbative_map]
children: [XXP-EWQCD-EXP]
status: candidate
version: 0.1
last_updated: 2025-10-18
provenance:
  sources:
    - module: MATH-YM-003_nonperturbative_map
      lines: "§4"
      snippet: |
        a = \frac{r_0}{(r_0/a)*{\rm lat}}
        \quad\text{or}\quad
        a = \sqrt{\frac{t_0}{(t_0/a^2)*{\rm lat}}}.
  editors: [chain-of-thought-agent]
  review_log: []
triad:
  art: |
    The lattice spacing is the fundamental pixel size of spacetime in a simulation, the physical ruler by which all digital hadrons are measured. It transforms the abstract grid of points into a tangible piece of the universe.
  law: |
    The lattice spacing `a` is deterministically predicted from the Pirouette string tension `σ` via an intermediate, dimensionful reference scale (e.g., `r_0`, `t_0`) whose dimensionless value (e.g., `r_0/a`) is measured in simulation. This prediction must hold consistently across different lattice ensembles after a single, one-time normalization.
  philosophy: |
    The lattice spacing is the ultimate bridge between continuous theory and its discrete, computable representation. By predicting `a` from first principles, Pirouette promotes a simulation's free parameter into a falsifiable output, closing the loop between the framework's mechanics and the numerical experiment.
pirouette_definition: |
  The physical distance between adjacent sites on the discrete spacetime grid. In Pirouette, `a` is not a free parameter to be set but a predictable output of the nonperturbative pipeline. It is derived by converting the mechanically-predicted string tension (`σ`) into a physical reference scale (like the Sommer scale `r_0`), which is then divided by its corresponding dimensionless value measured in a lattice simulation.
operational_definition:
  units: Length (fm, GeV⁻¹)
  symbol_table:
    - name: a
      meaning: Lattice spacing
      dimensions: L
      default_range: 0.03–0.15 fm
    - name: σ
      meaning: Fundamental string tension
      dimensions: M L T⁻² (or M² in natural units)
      default_range: ~ (440 MeV)²
    - name: r_0
      meaning: Sommer scale
      dimensions: L
      default_range: ~ 0.5 fm
    - name: (r_0/a)ₗₐₜ
      meaning: Dimensionless Sommer scale measured on the lattice
      dimensions: dimensionless
      default_range: 3–10
  measurement:
    procedures:
      - name: Derivation from String Tension via Reference Scales
        outline: |
          1. Predict the string tension `σ` from Pirouette's mechanical parameters (`κ_3`, `ξ_Γ`) via the core scaling relation `σ = c_σ κ_3 / ξ_Γ²`.
          2. Calculate a physical reference scale, e.g., the Sommer scale `r_0`, from `σ` using its force-based definition: `r_0² F(r_0) = 1.65`, where `F(R) = dV/dR ≈ σ`.
          3. In a parallel lattice simulation, measure the dimensionless value of this scale, `(r_0/a)ₗₐₜ`, typically from the static quark-antiquark potential extracted from Wilson loops.
          4. The predicted lattice spacing is `a = r_0 / (r_0/a)ₗₐₜ`.
        expected_signals:
          - A consistent value of `a` (in fm or GeV⁻¹) across different lattice ensembles (i.e., different gauge couplings `β`).
          - Agreement between values of `a` determined using different reference scales (e.g., `r_0` vs. `t_0`).
        pitfalls:
          - Discretization artifacts at coarse lattice spacings can distort the static potential and thus the extraction of `(r_0/a)ₗₐₜ`.
          - Finite volume effects can contaminate the long-distance part of the potential used to determine `σ` and `r_0`.
context_windows:
  - module: MATH-YM-003_nonperturbative_map
    excerpt: |
      **Conversions (deterministic once (σ) fixed):**
      [
      r_0 = \sqrt{\frac{1.65}{\sigma + \pi/(12 r_0^2)}}
      ;\approx; \sqrt{\frac{1.65}{\sigma}};\Big(1+\mathcal{O}(\sqrt{\sigma})\Big),
      ]
      [
      a = \frac{r_0}{(r_0/a)*{\rm lat}}
      \quad\text{or}\quad
      a = \sqrt{\frac{t_0}{(t_0/a^2)*{\rm lat}}}.
      ]
      Thus, **Pirouette → (σ) → (r_0,t_0) → (a)** gives a **numerical lattice spacing** prediction.
  - module: MATH-YM-003_nonperturbative_map
    excerpt: |
      **Falsifiability (nonperturbative gates)**
      - **Scale inconsistency:** Pirouette-predicted (a) disagrees with lattice-extracted (a) across ensembles after the one-time normalization → fails the (σ→ r_0,t_0) map.
poetic_connections:
  motifs: [discretization, scale setting, grid, pixelation, physical ruler]
  evocative_lines:
    - "every lattice number has a seat in the hall—and every seat points back to the same temporal instrument."
    - "This closes the loop between the **coherence barrier** and **hadronic phenomenology**."
  association_matrix:
    - [ "STRING_TENSION", 0.9 ]
    - [ "SOMMER_SCALE", 0.9 ]
    - [ "LAMBDA_QCD", 0.6 ]
formal_mappings:
  candidates: []
  adopted:
    - target: Lattice spacing (a)
      domain: LGT/LQCD
      mapping_kind: operational
      equation_hint: |
        m_{phys} = m_{lat} / a
      justification: |
        The symbol `a` and its definition as the physical distance between lattice sites is the universal convention in the lattice quantum field theory community. Pirouette uses the term in precisely this sense, but uniquely treats it as a predictable output derived from mechanical principles rather than an input parameter determined post-hoc by matching to a single experimental observable.
      references:
        - title: "Gauge Fields on a Lattice"
          where: "C. Gattringer, C. B. Lang, section 1.2"
          date: 2010-01-01
      confidence: 1.0
constraints_and_falsifiers:
  claims:
    - statement: "The lattice spacing `a` predicted by the Pirouette pipeline (`κ₃`, `ξ_Γ` → `σ` → `r₀`) must agree with the value determined from lattice simulations across multiple, independent ensembles and reference scales after a single global normalization."
      domain: phenomenology
      falsifier: "A statistically significant disagreement between the predicted `a` and the measured `a` for a given lattice ensemble, or a drift in the required normalization constant `c_σ` needed to achieve a match on different ensembles."
      status: proposed
      links: [MATH-YM-003_nonperturbative_map]
naming_notes:
  collisions: [acceleration, annihilation operator, fine-structure constant]
  disambiguation: |
    In the context of the Pirouette Framework and its interface with numerical simulations, the symbol `a` almost exclusively refers to the lattice spacing. It should be distinguished from dimensionless lattice extents, typically denoted `L/a` or `N_s`, `N_t`.
crosslinks:
  near_synonyms: []
  antonyms: [CONTINUUM_LIMIT]
  prerequisites: [STRING_TENSION, SOMMER_SCALE]
  downstream_effects: [HADRON_MASS, DECAY_CONSTANT]
license: CC-BY-SA-4.0
---

# Lattice spacing

## Canonical (Pirouette)
The physical distance between adjacent sites on the discrete spacetime grid. In Pirouette, `a` is not a free parameter to be set but a predictable output of the nonperturbative pipeline. It is derived by converting the mechanically-predicted string tension (`σ`) into a physical reference scale (like the Sommer scale `r_0`), which is then divided by its corresponding dimensionless value measured in a lattice simulation.

## EFT-First Summary
The lattice spacing `a` is the standard quantity from Lattice Quantum Chromodynamics (LQCD) that sets the physical scale of a numerical simulation. It converts dimensionless lattice results (e.g., a hadron mass `m_{lat}`) into physical units (e.g., `m_{phys} = m_{lat} / a`). While conventionally determined by fixing one physical observable as an input, Pirouette predicts `a` from its own fundamental parameters, turning scale setting into a physical test of the framework.

## Glossary Links
- See also: [String Tension](<link>), [Sommer Scale](<link>), [Continuum Limit](<link>)