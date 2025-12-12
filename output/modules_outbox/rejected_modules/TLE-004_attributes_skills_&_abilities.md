---
#───────────── The Lost Eternal ──────────────────────
id:        TLE-003
title:     The Nature of Arcane Entropy
version:   1.0-draft
parents:   [TLE-000, TLE-002]
children:  [All future TLE modules related to magic, spells, and abilities]
engrams:
 - mechanic:freeform-magic-system
 - concept:magic-as-skill
 - mechanic:entropic-casting
 - strategy:magical-combat
keywords:  [magic, spellcasting, arcane, expression, transmutation, genesis, TLE]
uncertainty_tag: Low
module_type: core-mechanic-expansion
---
## §1 · Preamble: The Shape of the Soul
Where previous modules defined the physical form, this module specifies the intangible architecture of a being: its core attributes. In the world of The Lost Eternal, a character's strength, agility, and intellect are not abstract scores, but deep reservoirs of entropic potential. All Entropy Points (EP) an entity acquires must be invested into this foundational structure, shaping the very essence of their capabilities and their potential for growth.

## §2 · The Five Attributes: Containers of Potential (Revised)
An entity's Total Entropy Pool (TEP) is distributed across five core attributes. These attributes are not capped at 20 and can be increased indefinitely. They are not just passive modifiers; they are active pools of power that determine how an entity can channel its will.

### 2.1 · Attribute Scaling
Attribute Score: An attribute's Score is equal to half the total EP invested in it, rounded down. Score = floor(EP Invested / 2).

Attribute Modifier: An attribute's Modifier is equal to one-quarter of its Score, rounded down. Modifier = floor(Score / 4).

Example: Investing 40 EP into Strength results in a STR Score of 20 and a STR Modifier of +5.

### 2.2 · The Five Attributes
Strength (STR): Governs the application of raw physical power.

Checks: When making a Strength check to overcome a variable force, you roll 1d[STR Score]. The result is the amount of entropy you bring to bear.

Combat: Your STR modifier adds to your physical attacks. For every +1 modifier, you may add an additional die of damage (e.g., a +2 modifier allows you to spend 2 extra EP to turn a 1d8 attack into a 1d10 attack).

Dexterity (DEX): Governs agility, reflexes, and control over the flow of action.

Initiative: At the start of combat, you may spend a number of EP up to your DEX modifier to shift your position in the initiative order.

Constitution (CON): Governs an entity's connection to the flow of entropy and their physical endurance.

Regeneration: This remains the primary source of an entity's Entropy Regeneration Rate (ERR), as defined in TLE-000.

Intelligence (INT): Governs logic, memory, and the ability to impose complex will upon the world.

Combat Utility: Your INT modifier provides a pool of "free" EP each round that can be spent on any action.

Knowledge: Your INT modifier can be applied as a bonus to the DC of a knowledge-based check. It also serves as a tiebreaker for contested spellcasting checks.

Wisdom (WIS): Governs intuition, perception, and defensive insight.

General Utility: Your WIS modifier provides a pool of "free" EP that can be spent on any skill or ability check outside of combat.

Combat Defense: In combat, you may spend EP up to your WIS modifier to influence a contested roll defensively.

## 3 · The Action Economy (Revised)
An entity's speed and number of actions are not determined by their limbs, but by the total power of their being.

Number of Actions/Reactions: An entity can perform a number of distinct Actions or Reactions each turn equal to:
Actions per turn = floor( (STR Score + DEX Score + INT Score + WIS Score) / 6 )

Minimum: An entity can always perform at least one Action per turn.

## §4 · Skills & Ability Checks (Revised)
Skills and abilities are direct expressions of an entity's entropic investment, channeled through their attributes.

### 4.1 · Acquiring Skills
An entity can learn a new Skill by spending 3 EP from their TEP.

### 4.2 · The Universal Check
Static Check: Roll a d20 against a Difficulty Class (DC).

Untrained: Succeeds on a natural 20.

Trained: Check = d20 + EP in Skill.

Contested Check: Both sides roll their relevant Entropy Dice (e.g., 1d[STR Score] vs 1d[STR Score]), and the higher roll wins.

## §5 · Professions & The Art of Creation
The rules for learning professions and crafting items remain as described in version 1.1 of this module. The "crafting as combat" mechanic, where a crafter must "defeat" an item's Entropy Budget, is a core part of this system.