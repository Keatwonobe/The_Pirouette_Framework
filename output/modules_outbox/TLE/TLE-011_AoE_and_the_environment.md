---
#───────────── The Lost Eternal ──────────────────────
id:        TLE-011
title:     The Living World, Environmental Interaction & Area of Effect
version:   1.0-ratified
parents:   [TLE-006]
children:  []
engrams:
 - system:area-of-effect-rules
 - mechanic:entropic-sprawl
 - concept:environmental-capacity
 - system:elemental-transmutation
keywords:  [AoE, environment, entropy, sprawl, transmutation, overload, TLE]
uncertainty_tag: Low
module_type: core-mechanic-framework
---
## §1 · Preamble: The World as a Canvas
The world is not a static stage; it is a living, resonant entity with its own capacity to absorb, resist, and react to the imposition of will. This module details the laws that govern the interaction between a character's power and the very substance of reality—the air, the earth, and the water around them. It provides a universal system for all Area of Effect (AoE) abilities, from a simple cone of fire to a world-shaking earthquake, grounding them in a single, elegant principle.

## §2 · The World's Entropic Capacity
Every substance in the world has a limit to the amount of entropic force it can contain before its nature is fundamentally altered. This is its Entropic Capacity (EC).

Mechanic: A GM can assign a default EC to any 5-foot cube of a substance (e.g., Air: 10, Water: 20, Earth: 30, Stone: 50).

Entropic Ablation: If the total EP from a single damage type invested in a square in one round exceeds its EC, the square undergoes Ablation. The substance is consumed or transformed. Superheated air might become a temporary vacuum. Earth might turn to molten slag. Water might flash into superheated steam. This creates dynamic, lasting changes to the battlefield.

## §3 · The Art of Transmutation
Magic is the art of reshaping entropy. As described in TLE-003, this can be done in several ways. The cost reflects the difficulty of the transformation.

Expression (1:1 Cost): Manipulating existing entropy. A 10 EP fire spell controls or shapes 10 EP worth of existing fire.

Transmutation (2:1 Cost): Changing one form to another. To transmute a 10 EP fire into inert dust would cost the caster 20 EP. This is the same principle that makes healing inefficient (TLE-005).

Genesis/Obliteration (3:1 Cost): Creating or destroying entropy. This remains the rarest and most costly form of magic.

## §4 · The Law of Entropic Sprawl (AoE Mechanics)
An Area of Effect spell is not a pre-defined template. It is a dynamic process of spreading entropic force from a point of origin, governed by a fundamental law of resonant stability.

The Law: The entropic power in any given 5-foot square cannot exceed the sum of the power in all adjacent squares (diagonals included) plus two.
EP_center ≤ (Σ EP_adjacent) + 2

Shaping the Sprawl: The caster does not simply choose a "cone shape." They choose a point of origin (which can be their own square or a square they can touch) and an EP Budget for the spell. On their turn, they can spend Actions to "push" EP from the origin square into adjacent squares, as long as the Law of Entropic Sprawl is never violated. This makes casting a large AoE a tactical, turn-by-turn process of shaping and growing the effect.

Example: A 25-foot Cone (12 squares, 50 EP Budget): The caster starts the flow.

Turn 1: The caster spends their first action to place 4 EP in the square in front of them. They use their second action to push 3 EP from that square into the three squares in the next rank of the cone. The total EP spent is 13. The cone is small but growing.

Turn 2: The caster continues to feed EP into the origin, which then flows outward, increasing the power in each square until the full 50 EP budget is distributed across the 12 squares (averaging ~4 EP per square).

The "Orbital Strike": A caster can pump their entire 50 EP budget into a single 5-foot square. However, according to the Law, that square must be surrounded by squares containing a total of at least 48 EP. The player must spend their time and EP building up this massive "containment field" before they can unleash the final, devastating blow.

## §5 · The Overload Cascade
This law provides a powerful and thematic consequence for failed single-target attacks, replacing the "harmless miss" from the playtest.

Mechanic: When a character fails an Accuracy Check for a single-target attack (TLE-001), the uncontrolled entropy detonates. This chaotic energy is not a simple explosion; it becomes a new source of EP that immediately and violently spreads from the target's square according to the Law of Entropic Sprawl, creating a chaotic, uncontrolled AoE effect. The attacker has no control over its shape or direction.

## §6 · The World's Fury: Natural Disasters
Massive environmental events are not special, magical effects. They are simply macro-scale expressions of the same entropic laws.

Mechanic: A GM can model a volcano, earthquake, or hurricane by assigning it a colossal Entropic Budget and having it act on its own initiative turn. The lava flow or shockwave spreads across the map according to the Law of Entropic Sprawl, providing a consistent, scalable mechanic for everything from a simple Fire Bolt to a world-ending cataclysm. This makes these events retroactively calculable and, for truly powerful entities, potentially summonable.

## §7 · Assemblé
The world is not a passive stage, but an active participant in the dance of will. Fire, earth, and magic all obey the same rhythmic law of spread and containment. In this world, power is not measured by the size of the explosion one can create, but by the skill to shape its flow. To be a master of magic is to be a master of this dance, learning to guide the sprawl of creation without being consumed by your own uncontrolled power.