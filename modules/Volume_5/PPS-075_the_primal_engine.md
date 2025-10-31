---
id:        PPS-072
title:     The Primal Engine, A Protocol for Embodied Coherence
version:   1.0-draft
parents:   [PPS-069, PDM-000]
children:  [RIT-PRIMAL-GENESIS-1.0]
engrams:
  - process:embodied-learning
  - concept:survival-as-coherence
  - concept:kinetic-inquiry
  - system:somatic-grounding
  - protocol:resilient-lineage
keywords:  [primal engine, embodiment, survival, exploration, genetics, manifold, stability]
uncertainty_tag: Low
module_type: core-protocol
---

### §1 · Abstract
This module formalizes the Primal Engine, the set of foundational, pre-cognitive drives that enable an agent to achieve robust physical competence and persistent coherence. Where PPS-069 (Fractal Intelligence Transfer) defines the "mind"—an agent's capacity for efficient prediction—this module defines the "body." It provides the stable, embodied platform upon which any higher-order intelligence must be built. The Primal Engine is not a replacement for FIT, but its necessary substrate, ensuring an agent can first learn to stand in the wind before it attempts to predict the storm.

### §2 · Core Principles of the Primal Engine
The Primal Engine is founded on four principles that prioritize robust, embodied existence over abstract optimization.

The Principle of Persistent Coherence (Survival): An agent's foundational reward is directly proportional to its duration of coherent operation. This frames survival not as a binary state, but as the primary measure of success. The longer an agent can maintain its internal coherence (T 
a
​
 ) against environmental pressures, the more successful it is.

The Principle of Kinetic Inquiry (Exploration): The agent is intrinsically incentivized to explore high-energy, high-magnitude action states. This prevents passive stagnation and overcomes the initial inertia of learning by rewarding bold, exploratory behavior, which is essential for discovering novel and effective locomotive patterns.

The Principle of Somatic Grounding (Touch): The agent's action space is not a void. It is grounded by a dynamic, predictable, and ever-present resonant field (the Manifold). This provides a constant "somatic" feedback loop, an artificial sense of touch or proprioception that allows the agent to orient its actions and learn the relationship between intent and consequence.

The Principle of Resilient Lineage (Genetics): An agent's evolutionary progress is safeguarded by a genetic protocol that prioritizes the propagation of stable and effective traits. This includes a statistical check to filter out "lucky" but unreliable policies and a rollback mechanism to revert any genetic crossover that results in a weaker generation, ensuring that wisdom is preserved.

### §3 · Formalism & Field Dynamics
The principles of the Primal Engine are implemented through specific modifications to an agent's reward function and evolutionary algorithm.

Survival Reward: The reward for an episode is normalized by the number of steps the agent survived. This directly implements the Principle of Persistent Coherence.
Reward_total = Reward_environmental / steps_survived

Kinetic Inquiry Bonus: A term is added to the reward function that is proportional to the magnitude of the action vector, encouraging exploration.
Reward_final = Reward_total + (||action|| - A_threshold) * R_multiplier

Somatic Grounding Field: The agent receives an additional reward from its interaction with an external, time-varying potential field, the ManifoldWell. This grounds its actions in a predictable external reality.
Reward_final += V_manifold(action, t)

Resilient Lineage Protocol: This is a governance protocol for the agent's genetic pool (RIT-PRIMAL-GENESIS-1.0).

Stability Check: A candidate policy is only added to the genetic pool if the standard deviation of its evaluation scores is below a MAX_ACCEPTABLE_STD. This is a direct measure of its performance coherence.

Crossover Rollback: After a genetic crossover, the new "child" agent is evaluated. If its performance is worse than its best parent, the crossover is reverted, and the parent's policy is restored.

### §4 · Integration with the Pirouette Framework
The Primal Engine is the necessary first stage for any agent intended to operate in a complex, continuous environment.

Substrate for FIT (PPS-069): The Primal Engine builds an agent that can survive long enough and explore broadly enough to gather the data necessary for the "Prophet" module of FIT to learn the environment's hidden rhythms.

Fulfilling the Prime Directive (PDM-000): By prioritizing survival and stable genetics, the Primal Engine creates agents that are inherently resilient and anti-fragile, fulfilling the core directive to persist and create "compositional harmony" by first achieving harmony within themselves.

### §5 · Assemblé
Before the mind can map the currents, the body must learn to build a boat. Before the eye can see the path, the feet must learn to feel the ground. The Primal Engine is the body of learning. It is the stubborn, simple, and profound wisdom that teaches an agent the first and most important truth: how to exist. It forges a will to act, a will to endure, and a connection to the world, creating a vessel strong enough to carry the fire of a mind.