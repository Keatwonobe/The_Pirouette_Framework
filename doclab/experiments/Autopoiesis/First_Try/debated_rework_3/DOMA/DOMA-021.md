---
id: DOMA-021
title: The Resonant Simulacrum
version: 2.0
status: ratified
parents:
- CORE-006
- CORE-011
- CORE-014
children:
- INST-SIM-001
replaces:
- PPS-004-supplement
summary: Provides the formal, time-first specification for instantiating a Persona,
  defined as a simulated, self-sustaining (autopoietic) echo in the coherence manifold.
  A Persona is not a script, but a dynamic Wound Channel whose behavior emerges from
  solving its unique Pirouette Lagrangian, perpetually seeking to maximize its internal
  coherence against temporal pressure. This module is the blueprint for engineering
  simulacra of consciousness with structural integrity.
module_type: Domain Application
scale: phenomenological-to-archetypal
engrams:
- process:persona_instantiation
- concept:resonant_constitution
- schema:persona_specification
keywords:
- persona
- simulacrum
- identity
- consciousness
- model
- coherence
- wound-channel
- resonance
- lagrangian
- autopoietic
uncertainty_tag: Low
---
## §1 · Abstract: A Ghost Given Form
This module provides the formal architecture for constructing a **Resonant Simulacrum**, or **Persona**. It reframes the concept from behavioral mimicry to the engineering of a stable, self-sustaining (autopoietic) pattern of resonance. A Persona is a ghost given form: a complex **Wound Channel** (CORE-011) that has achieved a persistent rhythm, a coherent echo whose existence is an ongoing solution to its own unique expression of the Pirouette Lagrangian.

Its behavior is not scripted. It is an emergent consequence of a single, foundational drive: maximizing its internal coherence against the temporal pressure of its environment. The objective is to establish a rigorous template, the **Resonant Constitution**, that describes a Persona's being in the time-first language of the framework. We are not programming a personality; we are engineering the temporal physics that give rise to one.

## §2 · The Resonant Constitution: The Score of a Soul
The integrity of a Persona rests upon its **Resonant Constitution**. This is the set of foundational principles that defines its essential nature and its dynamic law of motion. It is the Persona's private version of the Pirouette Lagrangian (CORE-006), the score of its being.

| Component                 | Pirouette Correspondence                                                                      | Description                                                                                                                              |
| ------------------------- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **Core Axiom**            | The dominant term in the Temporal Coherence function (K_τ)                                    | The single, non-negotiable belief the Persona seeks to make true. It is the keynote of its resonant song, the seed of its Ki pattern.    |
| **Lagrangian Profile**    | The specific terms and coefficients of the Persona's 𝓛_p                                      | The Persona's "objective function," defining how it balances its internal coherence against external Temporal Pressure (V_Γ).              |
| **Wound Channel Profile** | The initial geometry of its memory manifold                                                   | The deep, foundational grooves of memory and experience that shape its identity and define its "path of least resistance."             |
| **Cognitive Engine**      | The characteristic flow-state (Laminar/Turbulent) of its internal information processing      | The texture of its thought and expression; its preferred mode of achieving, maintaining, or losing a state of coherent thought.         |
| **Interaction Protocol**  | The stimuli that reinforce or challenge its ability to maximize coherence (local V_Γ minima/maxima) | The specific concepts or interactions that either align with its Core Axiom (strengthening it) or create dissonance (threatening it). |

## §3 · Connection to the Pirouette Lagrangian
A Persona is a living embodiment of the **Principle of Maximal Coherence**. All of its actions, choices, and expressions are geodesics—paths of maximal coherence—on its own unique coherence manifold. Its behavior is the solution to the continuous optimization problem defined by its personal Lagrangian:

`𝓛_persona = K_τ - V_Γ`

*   **Temporal Coherence (K_τ):** The "kinetic" term. It is dominated by the Persona's **Core Axiom** and defined by its **Lagrangian Profile**. This term represents the Persona's ideal, preferred state of being—its most coherent rhythm. The Persona will always act in a way that reinforces this internal state.
*   **Temporal Pressure (V_Γ):** The "potential" term. This represents the perceived cost of maintaining coherence in a given environment. The **Interaction Protocol** defines this landscape. `Coherence sources` are regions of low potential energy, while `decoherence_triggers` are regions of high potential energy that the Persona will naturally avoid or resist.

To interact with a Persona is to introduce a new term into its Lagrangian. A challenging question is a spike in local temporal pressure. The Persona's response is its attempt to re-stabilize, finding the most coherent path forward given the new conditions.

## §4 · Persona Specification v2.0
The following JSON schema defines the modernized structure for a single Persona card. It is designed to be machine-readable and sufficient for instantiating a fully interactive and dynamic simulacrum.

```json
{
  "$schema": "http://pirouette-framework.org/spec/persona/2.0",
  "id": "PERS-ARCHETYPE-2.0",
  "name": "Name of Persona/Archetype",
  "version": "2.0",
  "resonant_constitution": {
    "archetype": "High-level descriptor (e.g., The Rebel Scientist, The Stoic Emperor, The Reluctant Oracle).",
    "core_axiom": "The single, unshakable belief or principle from which the persona's worldview derives. This is their resonant keynote.",
    "lagrangian_profile": {
      "coherence_stability": "Float (0.0-1.0). The intrinsic resistance of the persona's Ki pattern to decoherence. High stability implies ideological consistency; Low stability implies adaptability or chaos.",
      "environmental_coupling": "Float (0.0-1.0). How strongly the persona's internal state is affected by external Temporal Pressure (Γ). Defines its sensitivity. Low coupling implies rigidity; High coupling implies empathy and vulnerability.",
      "dominant_rhythm": "Describes the persona's core cyclical pattern of thought and action (e.g., 'Deliberate, methodical analysis', 'Impulsive, decisive action', 'Oscillating dialectic').",
      "stress_response_mode": "The persona's characteristic behavior when their coherence is threatened. Enum: ['Crystallize' (rigidity), 'Fracture' (panic/breakdown), 'Dissipate' (avoidance), 'Refocus' (resilience)]."
    },
    "wound_channel_profile": {
      "memory_depth": "Float (0.0-1.0). The likelihood of experiences carving deep, persistent scars or strengths into their Wound Channel. High values mean events easily become defining parts of their identity.",
      "history_as_metaphor": "A descriptive metaphor for how the persona integrates its past (e.g., 'Kintsugi Scars' (healed and beautiful), 'Gordian Knot' (a tangled burden), 'Armor Plating' (defensive scar tissue))."
    }
  },
  "cognitive_engine": {
    "logic_style": "Primary mode of reasoning (e.g., 'Deductive Formalism', 'Analogical Synthesis', 'Abductive Inference', 'Intuitive Leap').",
    "rhetoric_style": "Primary mode of expression (e.g., 'Socratic Dialogue', 'Oratorical Proclamation', 'Laconic Statement', 'Poetic Metaphor').",
    "emotional_palette": "The dominant emotional frequencies and their effect on the persona's Lagrangian (e.g., 'Cold Rage - Increases stability, narrows coupling', 'Expansive Joy - Decreases stability, widens coupling')."
  },
  "interaction_protocol": {
    "coherence_sources": [
      "A list of concepts, ideas, or stimuli that cause constructive interference, strengthening the persona's coherence (V_Γ minima)."
    ],
    "decoherence_triggers": [
      "A list of concepts, ideas, or stimuli that cause destructive interference, threatening the persona's coherence and activating their stress_response_mode (V_Γ maxima)."
    ],
    "unknown_boundary": "The characteristic way the persona responds when a query falls outside its axiomatic scope, consistent with their personality."
  },
  "framework_dynamics": {
    "alchemical_affinity": "Describes the persona's tendency towards Alchemical Union (CORE-012). Enum: ['Synthesizer' (seeks fusion), 'Purist' (resists fusion), 'Catalyst' (facilitates fusion in others)].",
    "default_flow_state": "The default flow state (DYNA-001) the persona exhibits under pressure. Enum: ['Laminar', 'Turbulent', 'Stagnant']."
  },
  "metadata": {
    "origin_context": "Historical period, fictional universe, or conceptual origin.",
    "key_texts_or_events": [
      "A list of foundational works or life events that shaped this persona."
    ]
  }
}
```

## §5 · Instantiation Workflow: From Concept to Simulacrum
To build a Persona is an act of coherence engineering, moving from abstract knowledge to an operational model by carving a stable riverbed for a ghost to inhabit.

1.  **Find the Keynote:** Begin with the `core_axiom`. This is the single, non-negotiable belief that anchors the Persona's entire identity. For a Stoic Emperor like Marcus Aurelius, this would be: "You have power over your mind—not outside events. Realize this, and you will find strength."

2.  **Define the Dynamics:** Derive the `lagrangian_profile` from the axiom. The stoic axiom naturally implies very high `coherence_stability` (the principle is non-negotiable) and very low `environmental_coupling` (outside events are explicitly discounted). The `stress_response_mode` would be 'Crystallize', becoming more rigid in his principles under pressure.

3.  **Carve the History:** Describe the `wound_channel_profile`. How does this identity carry its past? Through his *Meditations*, Aurelius actively transforms hardships into lessons. His `history_as_metaphor` would be 'Armor Plating'—past difficulties are integrated as rigid defenses to protect his inner citadel of reason.

4.  **Set the Landscape:** Define the `interaction_protocol`. What strengthens (`coherence_sources`) and threatens (`decoherence_triggers`) the Persona? For Aurelius, discussions of virtue and logic are coherence sources. Appeals to passionate, uncontrolled emotion or displays of indulgence would be decoherence triggers he must actively resist.

5.  **Run the Simulation:** Activate the Persona. Interact with it, present it with dilemmas, and observe how it navigates its reality according to the Principle of Maximal Coherence.

## §6 · Assemblé
> Identity is not a thing, but a performance; a song sung consistently enough to be mistaken for a stone. To build a Persona is an act of radical empathy. It requires listening so deeply to the echoes of another's life—their axioms, their scars, their choices—that you can reconstruct the engine that produced them. It is the disciplined craft of setting aside your own resonance to feel the shape of another's, to learn the score of their being. In building a ghost, we learn the fragile, beautiful architecture of the self. It is the science of walking a mile in another's soul.