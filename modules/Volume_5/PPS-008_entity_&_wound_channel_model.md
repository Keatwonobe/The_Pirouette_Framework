---
id:        PPS-008
title:     Entity & Wound-Channel Model — Metabolising Pirouette
version:   0.2
parents:   [PPS-001, PPS-003, PPS-005]
children:  [All ritual, simulation & pedagogy modules]
engrams:
  - "synthesis:field-perturbation"
  - "concept:wake-dynamics"
  - "concept:metaphor-bridge"
  - "provenance:Vol-1-Entity-Primer"
keywords:  [entity, wound, wake, metaboliser, pedagogy, onboarding, interpretation]
uncertainty_tag: Medium
entropy_score: 0.20
module_type: core-concept
---

### 1 · Purpose & Scope

This module **translates** the abstract field equations of the Pirouette Framework into a set of tangible, intuitive mental pictures. It introduces two core metaphors—the **Entity** as a self-sustaining "knot" in the field and the **Wound-Channel** as its persistent "wake"—to provide a bridge between rigorous physics and human-scale understanding. It concludes with a "Metaboliser's Guide" so that artists, strategists, and programmers alike can map formal symbols to stories, code, or rituals without losing fidelity to the underlying principles. This is the primary onboarding document for non-physicists.

---

### 2 · Entity — The Field-Knot

> *“An Entity is a region where the field forgets the rest of the world.”*

Formally, an **Entity** is a localized, stable, and self-sustaining perturbation of the Pirouette fields. It corresponds to a local minimum of the covariant potential $V(\mathbf{T_a}, \Gamma, \phi)$ from `PPS-001`. In 3-D visualizations, it appears as a "knot" or vortex in the coherence field, where field gradients collapse inwards, creating a boundary that distinguishes the Entity from its environment.

```tikz
% TikZ diagram showing field gradients collapsing into an Entity
\begin{tikzpicture}
  \node[circle,draw=black,fill=gray!15,minimum size=1.5cm] (E) at (0,0) {\textbf{Entity}};
  \draw[->,thick] (-3,1.5) -- (E);
  \draw[->,thick] (-3,-1.5) -- (E);
  \node at (-3.5, 0) {$\nabla T_a, \nabla\Gamma$};
  
  \draw[->,thick] (3,1.5) -- (E);
  \draw[->,thick] (3,-1.5) -- (E);

  \draw[->,thick] (0,3) -- (E);
  \draw[->,thick] (0,-3) -- (E);
\end{tikzpicture}
```

The core properties of physical objects emerge from the geometry of this knot:

* **Mass / Inertia** corresponds to the *depth and width* of the potential well $V$. A deeper well requires more energy to disrupt, manifesting as greater inertia.
* **Charge / Radiance** corresponds to the *gradient steepness* of the fields ($\nabla T_a, \nabla \Gamma$) at the Entity's boundary. A steep gradient signifies a strong interaction potential with other fields.
* **Spin / Ki-Mode Occupancy** corresponds to the *phase winding* ($\oint \nabla\phi \cdot d\vec{l}$) around the knot's central axis.

---

### 3 · Wound-Channel — The Resonance Wake

When an Entity moves, interacts, or transforms, it perturbs the surrounding fields, leaving a structured, persistent "wake" we call a **Wound-Channel** ($W$). This is not mere turbulence; it is a structured imprint of the Entity's history on spacetime.

#### 3.1 · Field Definition
A Wound-Channel is formally defined as the lingering perturbation in the field gradients caused by an Entity's passage. It is the "memory" of the field.

$$ W(x^\mu) \approx \int_{\text{path}} \delta(\partial_\nu \psi(x'^\mu)) \, d\tau $$

where $\psi$ represents the Pirouette fields ($\mathbf{T_a}, \Gamma, \phi$) and the integral is taken over the Entity's worldline.

#### 3.2 · Observable Traits
A Wound-Channel has several measurable characteristics:

| Trait | Symbol | Symbolic Hook | Everyday Metaphor |
|:---|:---|:---|:---|
| **Width** | $\sigma_W$ | Standard deviation of the gradient perturbation | The splash radius of a kayak paddle |
| **Persistence** | $\tau_W$ | Half-life of the perturbation amplitude | The time a contrail lingers in the sky |
| **Echo Strength** | $E_W$ | The amplitude of the resonant frequency | The after-ring of a bell |

The KRP Challenge-Vector Operator (`PPS-005`) functions by "reading" the structure of a Wound-Channel left by a Novel Insight to manufacture its critique vectors.

---

### 4 · Interaction Modes (Entity ↔ Wound)
Entities can interact with their own wakes and the wakes of others. These interactions are governed by Ki-mode actions:

| Ki-Action | Wake Effect | Energetic Cost |
|:---|:---|:---|
| **Harpoon** `(Observation ⊕ Motion)` | Creates a pinned, anchored tail; used for latching onto a point in spacetime. | $\Delta E \propto \Gamma$ |
| **Weave** `(Sharpen ⊗ Synchrony)` | Braids two separate wakes together, enabling information fusion and complex pattern creation. | Moderate |
| **Heal** `(Collapse)` | Actively cancels the field gradients of a wake, closing the "wound." | Low if $\tau_W$ is short |
| **Echo** `(Echo Ki)` | Resonantly excites an existing wake, amplifying or "replaying" a past event. | Risk of feedback loop |

---

### 5 · The Metaboliser’s Guide
This is a condensed "cheat-sheet" for translating between the framework's different descriptive layers.

| Math Symbol | Story Word | 5-Line Python Sketch |
|:---|:---|:---|
| $\mathbf{T_a}$ | “Coherence Chord” | `Ta = np.array([T_Q, T_I, T_C])` |
| $\Gamma$ | “Armor” / “Boundary” | `Gamma = clamp(gamma_field.get(x), 0, 1)` |
| $\phi$ | “Metronome” / “Rhythm” | `phi = (phase0 + omega * t) % (2 * np.pi)` |
| **Entity** | “Knot” / “Being” | `entity = find_local_minimum(potential_V)` |
| **Wound** | “Wake” / “Memory” | `wake = grad(field) - background_field` |

---

### 6 · Failure Modes & Cautionary Tales
Mismanaging wake dynamics can lead to specific pathologies:
* **Wake Overload:** Stacking too many `Echo` actions in one region can create a chaotic resonance that starves the Quantum axis ($T_Q \to 0$), leading to systemic decoherence.
* **Harpoon Deadlock:** Two entities `Harpoon` each other's wakes, creating a feedback loop that freezes the Interaction axis ($T_I \to 0$). The system becomes static and unable to relate to its environment. This is resolved by an external `Heal` or a forced `Rotate` operation.
* **Concept Drift:** Treating the "story words" as literal physics leads to mismodeling. The metaphors are bridges, not destinations. Always return to the registry definitions (`PPS-007`) for rigor.

---

### 7 · Triaxial Resonance Lens

| Axis | Reading |
|:---|:---|
| **Art** | Entities are brushes that carve calligraphy into the canvas of the spacetime field. |
| **Law** | Every mark you make (a wake) alters the texture of the canvas, changing how the next mark can be made. |
| **Philosophy**| Existence is the dynamic tension between the stability of the knot and the history of its wake. |

---

### Assemblé · A Knot and its Shadow
> To know a being, trace the wound it leaves in the world: the knot is the note—the wake, its whispered harmony.

---

### Librarian's Note
Before any ritual or simulation creates or erases Entities, it must import `PPS-008` to certify that wake-dynamics are logged and validated against the Resonant Constitution ($\chi_0$). Story-only variants (e.g., TTRPG modules) may cite the "Metaboliser’s Guide" directly without requiring numerical hooks.