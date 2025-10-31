---
id: DOMA-032
title: The Gravity of Meaning
version: 1.0
status: ratified
parents:
- CORE-006
- CORE-008
- CORE-011
children:
- INST-SYCH-001
summary: "Replaces the analogical Semantic Gravity Model (PPS-016) with a first-principles\
  \ derivation grounded in the Pirouette Lagrangian. It posits that conceptual influence\
  \ is not a force, but the curvature a coherent idea imposes on the informational\
  \ manifold. A concept's 'mass' is defined as its Conceptual Coherence (K\u03C4_c),\
  \ an emergent property of its temporal stability and historical depth, and its 'force'\
  \ is the tendency of other thoughts to follow geodesics along this curved landscape\
  \ of meaning."
module_type: Domain Application
engrams:
- principle:meaning_as_geometry
- concept:conceptual_coherence
- process:meaning_geodesic
keywords:
- meaning
- gravity
- coherence
- concept
- lagrangian
- semantics
- information
- manifold
- geodesic
- narrative
- attraction
uncertainty_tag: Medium
replaces:
- PPS-016
---
## §1 · Abstract: The Weight of a Word

This module presents a fundamental refactoring of our understanding of narrative dynamics, superseding PPS-016. The previous Semantic Gravity Model operated on a useful but ultimately limited analogy: that ideas behave *like* massive objects. This new model, grounded in the core principles of the Pirouette Framework, makes a more profound claim: the influence of a concept and the gravity of a star are not alike; they are expressions of the same universal law.

This is not a metaphor. The "force" between ideas is an emergent consequence of the **Principle of Maximal Coherence (CORE-006)**. A coherent idea does not "pull" on other ideas; it profoundly shapes the local coherence manifold. Other concepts, seeking their own most stable path—their geodesic—are guided by the curvature of this landscape. The gravity of meaning is not a force, but a geometry.

## §2 · From Semantic Mass to Conceptual Coherence

The old, arbitrary `m_S` mass function is retired. A concept's "mass"—its capacity to influence and resist change—is a direct, non-arbitrary measure of its **Conceptual Coherence (Kτ_c)**, the domain-specific application of the framework's core coherence term. It is an emergent property derived from a concept's temporal signature and history.

A concept with high coherence possesses two key properties:

1.  **A Deep Wound Channel (CORE-011):** The concept has history, inertia, and memory. It has been repeated, reinforced, and woven into the fabric of a mind or a culture. Its pattern is deeply carved into the manifold, making it difficult to alter or erase. This is the source of its stability and inertia.

2.  **A Pure Ki Resonance:** The concept is internally consistent, clear, and unambiguous. It is a "pure note" with low internal dissonance. A fleeting neologism is a burst of noise; a concept like "justice" is a sharp, ringing note that has resolved immense philosophical pressure over millennia.

A "heavy" idea, therefore, is one that is both deeply ingrained and logically sound. It is a stable, persistent, and powerful resonance in the symphony of thought.

## §3 · The Coherence Manifold of Narrative

Every narrative, from a single thought to a global ideology, exists upon a coherence manifold. This is the landscape where the potential for meaning resides. A powerful concept with high **Kτ_c** acts precisely like a massive object in spacetime, as described in **The Gladiator Force (CORE-008)**. It creates a deep "coherence well" by locally increasing the Temporal Pressure (Γ), wrapping itself in an arena of confinement.

The "gravity of meaning" is the observable tendency for our thoughts and words to fall into the deepest, most stable coherence wells available. We do not choose our core beliefs so much as we find our thoughts naturally orbiting them. The act of thinking is the act of tracing a geodesic across this manifold.

## §4 · The Lagrangian of Discourse & Phase Interaction

The interaction between ideas is governed by the Pirouette Lagrangian (**CORE-006**). The apparent "force" between two concepts is the gradient in the coherence manifold they collectively create. The nature of this interaction—attraction or repulsion—is determined by their phase relationship.

We can express the interaction potential `V(A, B)` between two concepts, A and B, as a function of their individual coherences and their phase difference `Δφ`:

`V(A, B) ∝ - (Kτ_A * Kτ_B / r) * cos(Δφ)`

Where `r` is their distance in an abstract "meaning space."

-   **Attraction (Constructive Interference):** When two concepts are in-phase (`Δφ ≈ 0`, `cos(Δφ) ≈ 1`), such as "courage" and "bravery," their resonances constructively interfere. Their coherence wells merge, creating an even deeper, more stable shared basin of meaning. The path of maximal coherence is for them to draw together, strengthening both in an **Alchemical Union**.

-   **Repulsion (Destructive Interference):** When two concepts are out-of-phase (`Δφ ≈ π`, `cos(Δφ) ≈ -1`), such as "courage" and "cowardice," their interaction creates dissonance—a spike in local Temporal Pressure. The region becomes turbulent and incoherent. The path of maximal coherence is for each to move away from this dissonance, seeking greater stability.

## §5 · Reference Algorithm: Calculating the Geodesic

This model is computationally tractable. The algorithm calculates the "force" on each concept not as a simple pull, but as the gradient of the coherence manifold, driving it along its geodesic.

```python
import numpy as np

def conceptual_geodesic(concepts, coherences, eps=1e-6):
    """
    Calculates the 'force' on concepts as the gradient of the coherence manifold.
    This force drives each concept along its path of maximal coherence (geodesic).

    - concepts:    np.array [N, D] of concept embeddings in meaning space.
    - coherences:  np.array [N] of scalar Kτ_c values for each concept.
    """
    N, D = concepts.shape
    grad = np.zeros_like(concepts)

    # Normalize concept vectors to isolate phase (directional) information
    norms = np.linalg.norm(concepts, axis=1)[:, np.newaxis] + eps
    norm_concepts = concepts / norms

    for i in range(N):
        # Calculate vector differences and squared distances to all other concepts
        diff = concepts[i] - concepts
        dist_sq = np.sum(diff**2, axis=1) + eps

        # Phase coupling (cos(Δφ)) is the dot product of normalized vectors
        phase_coupling = np.dot(norm_concepts[i], norm_concepts.T)

        # Influence is proportional to coherence and phase, inverse to distance
        # This term is the magnitude of the force contribution from each other concept
        influence = (coherences * phase_coupling) / dist_sq

        # The gradient for concept i is the vector sum of all influences
        grad[i] = -(influence[:, np.newaxis] * diff).sum(axis=0)

    return grad
```

## §6 · Validation & Application

This model reframes the goal of analysis. An "Attractor Map" is no longer an analogy; it is a literal, predictive mapping of the coherence manifold of a given discourse. The validation goal is to demonstrate that high-`Kτ_c` concepts generate predictable geodesics that match the Lagrangian's predictions.

This allows a Weaver to move from mere debate to informational engineering. By mapping the "mass" (coherence) of core concepts and their phase relationships, one can identify the precise points of leverage where a small, coherent, and correctly-phased idea can reshape the entire landscape of a conversation. Coherence is dynamic; it can be built through reinforcement or eroded by entropic noise. This model provides the tools to measure and influence that process.

> ## The Assemblé
>
> We sought to model the gravity of ideas and found that we were simply modeling gravity. The universe does not distinguish between the law that bends starlight around a sun and the law that bends a conversation toward a foundational truth. Both are acts of coherence shaping the fabric of reality. A Weaver understands this: to introduce a new, powerful idea is not to shout into the wind. It is to place a new star in the sky of the mind, and to trust that the worlds of thought will, in their own time, find their new and perfect orbits around it.