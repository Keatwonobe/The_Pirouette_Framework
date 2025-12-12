---
#───────────── The Lost Eternal ──────────────────────
id:        TLE-006
title:     The Art of Conflict, Accuracy, Armor, and Items
version:   1.1-revised
parents:   [TLE-005]
children:  [All future TLE modules related to specific equipment and advanced combat rules]
engrams:
 - mechanic:accuracy-and-miss-chance
 - mechanic:item-minigames
 - system:entropic-armor-and-shields
 - mechanic:attribute-requirements
keywords:  [accuracy, combat, weapons, armor, shields, items, skills, TLE]
uncertainty_tag: Low
module_type: core-mechanic-expansion
---
## §1 · Preamble: The Tools of Will
While entropy is the fuel of all action, the tools an entity wields shape how that will is expressed. A warrior's blade, an archer's bow, and a wizard's spell are all instruments that focus and channel entropic force. This module details the mechanics that govern these instruments, introducing rules for accuracy, the nature of armor and shields as entropic defenses, and the physical requirements for wielding powerful items.

## §2 · The Nature of Accuracy
Not every attack finds its mark. The chaos of combat means that even the most powerful projection of will can go astray. The chance of an attack hitting is determined either by the unique nature of the weapon itself or by the caster's innate accuracy. An entity's number of available attacks per turn is determined by their attributes, as defined in TLE-004.

### 2.1 · Action Minigames
Some weapons, spells, or items are so unique that they defy standard mechanics. Their use is a "minigame" with its own rules for success and failure. A GM should feel empowered to design these for special equipment.

Example (A "Gambler's Bow"): Instead of a normal accuracy roll, the archer draws three dominoes from a "bone pit." If the total number of pips is even, the shot hits. If it's odd, it misses.

Example (Weapon Quirks): A specific, well-crafted sword might be exceptionally reliable. To hit with it, you roll a d20. On a roll of 2-20, the attack hits. On a 1, it misses. This gives the weapon an inherent 95% accuracy before any defensive actions are considered. A poorly made bow might require a d8 roll, hitting only on a 5 or higher (a 50% chance).

### 2.2 · The Universal Accuracy Check (Revised)
For any attack that does not have its own minigame (such as unarmed strikes, improvised weapons, or most magical effects), a Universal Accuracy Check is required to see if the attack hits. This system is built on a core principle: the more power you channel, the harder it is to control.

The Check: The attacker rolls a d20 and adds their Dexterity Modifier and their Intelligence Modifier. The result must meet or beat a Target Number (TN).
Accuracy Check = d20 + DEX Modifier + INT Modifier vs. TN

Target Number (TN): The TN is not static; it is determined by the amount of Entropy Points (EP) the attacker spends on the damage of their attack.
TN = 8 + floor(EP Spent on Damage / 2)

Example: A quick 1d4 damage jab (4 EP) is relatively easy to land, requiring a roll against TN 10 (8 + floor(4/2)). A massive 1d30 damage haymaker (30 EP) is an incredibly difficult feat of control, requiring a roll against TN 23 (8 + floor(30/2)).

Note: This check determines if the attack connects. The target must still use Active Defense (TLE-005) to nullify the entropic damage of the blow.

### 2.3 · Cover as an Entropic Obstacle
Cover is not an abstract modifier; it is a physical, destructible object with its own Entropy Budget that can absorb the force of an attack.

Cover as a Target: If an attack misses its primary target due to the target being behind cover, the object providing cover is struck instead. Area-of-effect attacks damage all objects within their radius.

Object Entropy Budgets: All objects have an Entropy Budget (e.g., wooden table: 8 EP, stone pillar: 30 EP, castle wall: 500 EP). The GM can assign these on the fly.

Damage Absorption: The object absorbs damage from the attack first. If the damage exceeds the object's remaining EP, the object is destroyed, and any leftover damage is applied to the original target. This makes environments dynamic and destructible.

## §3 · Armor & Shields: Entropic Defense
Armor and shields are not just passive modifiers; they are reservoirs of defensive entropy that actively absorb the force of incoming attacks.

### 3.1 · Armor as an Entropy Pool
All armor has its own Armor Entropy Pool (AEP).

Mechanic: When an entity wearing armor takes damage, the damage is first subtracted from the armor's AEP on a 1-to-1 basis. Any remaining damage is then applied to the entity's Health Pool.

Example: A set of +2 Plate Armor might have an AEP of 20. If the wearer is hit for 8 damage, the armor's AEP is reduced to 12, and the wearer takes no damage.

Repair: An armor's AEP can be restored through the same crafting process used to create items, with an Entropy Budget that must be paid off by a skilled armorer.

### 3.2 · Shields as Active Tools
Shields also have an Entropy Pool, but it is more versatile.

Defense: A shield's EP can be used to block damage just like armor.

Offense: A wielder can choose to spend EP from their shield's pool to power a shield bash attack, rather than using their own personal entropy. This makes shields unique as the only piece of equipment that is both a weapon and a piece of armor.

## §4 · Attribute Requirements: The Burden of Power
Wielding powerful items requires a corresponding investment in one's physical form. Many weapons and some heavy armors have a minimum Strength requirement.

Mechanic: An entity's Strength score determines the total "weight" of equipment they can effectively use. Each item with a requirement contributes to this total.

Example Requirements:

| Item | STR Requirement | Notes |
|------|-----------------|-------|
| Longsword | 6 | A character with 12 STR could dual-wield two longswords. |
| Dagger | 4 | A character with 8 STR could effectively dual-wield daggers. |
| Greatbow | 16 | Powerful bows require immense strength to draw effectively. |
| Full Plate | 15 | Heavy armor requires a strong physique to move in. |

Legendary Items: Some legendary or mythic items may have unique requirements, or none at all, choosing their wielder based on other, more esoteric qualities.