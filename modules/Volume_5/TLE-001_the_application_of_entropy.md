---
#───────────── The Lost Eternal ──────────────────────
id: TLE-001
title: The Expression of Will, Actions, Conflict, and Magic
version: 1.0-consolidated
parents: [TLE-000]
children: [TLE-002]
engrams:
 - system:action-economy
 - mechanic:entropic-combat
 - mechanic:freeform-magic-system
 - system:healing-and-survival
keywords: [action, combat, magic, accuracy, healing, exhaustion, TLE]
uncertainty_tag: Low
module_type: core-rulebook-consolidated
---
## §1 · Preamble: The Will in Motion
Where TLE-000 defined the soul of a character—their entropic form—this module defines its function. An entity's will is not a passive state; it is an active force that imposes itself upon the world. Every action, from the swing of a sword to the whisper of a spell, is an expression of this will, a conversion of internal potential into external effect.

This module provides the universal mechanics for these expressions, consolidating the rules for actions, conflict, magic, and survival. It defines how Entropy Points (EP) are spent to shape reality.

## §2 · The Action Economy
An entity’s capacity to act in a given moment is a direct function of its total entropic investment in its being. A more powerful and complex being can simply do more.

Actions per Turn: An entity can perform a number of distinct Actions or Reactions each turn equal to:
Actions per Turn = floor( (STR Score + DEX Score + INT Score + WIS Score) / 6 )

Minimum: An entity can always perform at least one Action per turn.

## §3 · The Art of Conflict
Combat is a contest of will, where entropic force is focused through the instruments of conflict. The following rules govern all forms of attack.

### 3.1 · The Universal Accuracy Check
The more power one channels, the harder it is to control. An attack's accuracy is a trade-off against its raw power. This applies to any attack that does not have its own unique "minigame" (see TLE-006).

The Check: The attacker rolls a d20 and adds their Dexterity Modifier and their Intelligence Modifier. The result must meet or beat a Target Number (TN).
Accuracy Check = d20 + DEX Modifier + INT Modifier vs. TN

Target Number (TN): The TN is determined by the amount of EP the attacker spends on the damage of their attack.
TN = 8 + floor(EP Spent on Damage / 2)

Note: This check determines if an attack connects. The target must still use Active Defense (TLE-005) to nullify the damage by spending an equal or greater amount of EP.

### 3.2 · The Universal Resolution Mechanic
The more power one channels, the more control it takes to be successful. A skill check's success is a trade-off against its entropy cost. This applies to any roll or skill check that does not have its own unique "minigame" (see TLE-006).

The Check: The attacker rolls a d20 and adds their Wisdom Modifier. The result must meet or beat a Target Number (TN).
Accuracy Check = d20 + WIS Modifier vs. TN

Target Number (TN): The TN is determined by the amount of EP the attacker spends on the skill check.
TN = 8 + floor(EP Spent on Check / 2)

Note: This check determines if an attack connects. The target must still use Active Defense (TLE-005) to nullify the damage by spending an equal or greater amount of EP.

### 3.3 · The One Sided Contest
When engaging in a practice where only one side is aware (lying, stealth, stealing, etc) the resolution is determined through a contested roll where one side is the entropy investment (declared beforehand) and the other is a roll against the relevant sensory organ (sight, sound, smell, etc). This series of checks is made with the Wisdom bonus of the creature rolling the dice. 

The outcome of the roll being higher than the entropy invested is a detection, a noise made in the dark, etc. The entropy investment being higher than the roll means the act was successful. 

The number of sides of the dice used for the check must be at least a number of sides equal to sensory organ investment and wisdom modifier added together, so a creature with two eyes, a nose and two ears with a +4 wisdom modifier would use a nine sided dice for their roll. Each creature rolls separately. If nobody beats the investment in stealth, the creature is undetected and for all purposes invisible to those in the area that failed their roll.

This is also applicable to mages casting invisibility spells using a skill or power, only with arcane entropy investiture. Feats used to detect magic can detect invisibility spells though, so rogues still have a benefit to doing things the old fashioned way.

### 3.4 · Cover as a Destructible Defense
Cover is not an abstract modifier but a physical object that can be destroyed.

Mechanic: If an attack misses due to cover, the object providing cover is struck instead. The object has its own Entropy Budget (e.g., a wooden table might have 8 EP). The object absorbs the damage first. If the damage exceeds the object's budget, it is destroyed, and any remaining damage is applied to the original target.

## §4 · The Nature of Magic
Magic is the purest expression of will, shaping entropy without a physical medium. It is not learned from a list of spells but is wielded as a fundamental skill.

### 4.1 · Magic as a Skill
An entity can acquire a new Arcane Skill (e.g., "Expression of Fire," "Transmutation of Matter") by permanently investing 3 EP from their TEP. This skill then acts as a new container, into which the caster can allocate additional EP to fuel their magical effects.

### 4.2 · Casting and Range
Power Cost: The base EP cost for a magical effect is determined by its intended damage or power, as per the Direct Influence rules (TLE-000).

Range Cost: Projecting one's will across a distance relies on the power used. 1 EP spent on damage grants 5 feet of range to the spell. 1 additional EP can be spent on 5-10 feet of distance to the cast via the Spell Sniper's Gambit below.

General Rule: Split Cast

Any spellcaster can target an additional creature with a single-target spell by spending an additional 3 EP from the spell's pool.

- §1 · The Concordant Act: Acting as One
While individual initiative dictates the flow of battle, true power lies in unity. A group of beings can choose to synchronize their actions, weaving their individual efforts into a single, decisive moment.

Declaring Intent: On your turn, if you wish to act in concert with an ally, you must declare your intent and the general nature of your action (e.g., "I'm going to hold my fire spell to combine with Gronk's attack."). You must have at least one action, bonus action, or reaction remaining to do this.

The Lowest Ebb: When two or more individuals agree to act together, they forsake their own place in the turn order. All participants in the Concordant Act will take their actions on the lowest initiative count among the group.

Combined Effect: The effects of all combined actions resolve simultaneously at the designated target or location. The total EP invested from all participants is summed to determine the final effect, following all normal entropy rules.

- §2 · Elemental Synergy & Interaction
Entropy is not static; it is a reactive and volatile force. When different elemental expressions are brought together, they can combine to create new, powerful tertiary effects. This is not a rigid system of rock-paper-scissors, but a fluid principle based on narrative and physical logic.

The Principle of Synergy: When two or more elemental effects (e.g., a Fire spell and a Water spell) target the same creature or occupy the same 5-foot space in the same round, they interact. The resulting effect is determined by the GM based on the nature of the elements involved. Players are encouraged to be creative.

Example 1: A "Lava" spell (Fire + Earth) and a "Frost" spell target the same space. The intense thermal shock could cause the lava to instantly harden into obsidian, creating a permanent physical barrier or potentially trapping a creature.

Example 2: A "Fireball" and a "Geyser" (Water) spell detonate on the same target. The result is a massive, blinding cloud of steam, heavily obscuring the area.

The Smothered Condition: When a creature is fully encased in a solid substance created by an elemental interaction (such as the obsidian from Example 1), they gain the Smothered condition. A Smothered creature cannot move or take actions and begins to suffocate. At the start of each of its turns, it takes irreducible damage equal to 1/8th of its maximum HP. It can use its action to attempt to break free by making a Strength check against a TN set by the GM based on the material's durability.

- §3 · Arcane Dueling: Spell Interception
In a world governed by Entropy, a spell is not an unstoppable force but a tangible projection of will. A skilled caster can learn to unravel an opponent's spell before it ever takes effect, turning arcane combat into a deadly, tactical duel.

The Interception: You can use your reaction to attempt to counter a spell that is being cast by a creature you can see. You must declare that you are targeting their spell, not the caster.

The Contested Will: Intercepting a spell is a contested check. You make an attack roll (d20 + your spellcasting attribute modifier, typically INT or WIS). The Target Number (TN) for this roll is 10 + the total EP the enemy caster invested in their spell.

The Outcome:

Success: Your will overpowers theirs. Your spell collides with their nascent magic, causing both to collapse in a burst of harmless, chaotic energy. Both spells are nullified, and the EP for both is spent.

Failure: Your spell is too weak or too slow. It fails to disrupt the enemy's casting, and their spell takes effect as normal. Your EP is still spent.

### 4.3 · The Spell Sniper's Gambit
To make long-range casting a feat of power and luck, a caster can use this gambit.

Mechanic: A caster declares they are spending X EP on additional range.

They gain a guaranteed range of (X / 2) * 5 feet (rounded down).

They then roll 1dX. The result is multiplied by 5 feet and added to the total.

## §5 · Healing and Exhaustion
The entropic form is resilient but not infinite. It must be maintained and allowed to recover.

### 5.1 · Healing
Healing is the act of transferring entropy to restore a damaged Health Pool.

Magical Healing: Restoring 1 HP to a target costs the healer 2 EP. One point is transferred, and one is lost to the inefficiency of the transfer.

Sacrificial Healing: A healer may spend their own HP to restore a target's HP on a 1-to-1 basis. This costs no additional EP but directly drains the healer's life force.

Natural Healing: An entity can naturally heal by dedicating their Downtime Entropy Budget (TLE-008) to recovery. The Entropy Budget to heal 1 HP is 2,500 EP, which is paid off by the character's passive ERR while resting.

### 5.2 · Exhaustion
An entity's connection to the flow of entropy requires rest.

Mechanic: For each consecutive 24-hour period an entity goes without a long rest, their Entropy Regeneration Rate (ERR) is halved (rounded down).

Collapse: If an entity's ERR drops below 1, they immediately fall unconscious and cannot be awakened by normal means until they have completed a long rest.

## §6 · The Choice Between Will and Fortune
An entity's will, their Entropy, is a force of direct and predictable power. To spend one point of Entropy is to create one point of effect. This is the path of the steady hand, the scholar, the sentinel. But the universe is not always predictable, and sometimes, the greatest triumphs are born from a leap into the unknown.

This module provides the rules for this leap. It is the art of the gamble: the choice to trade the certainty of your will for a chance at the favor of fortune, converting the solid currency of Entropy into the chaotic roll of the dice.

## §7 · The Universal Conversion Principle
At its heart, the conversion principle is a simple trade-off. For nearly any action that requires an EP spend to produce a numerical effect (damage, healing, distance, duration, etc.), a player can choose to convert some or all of that EP into a dice roll.

This transforms a predictable outcome into an unpredictable one, with the potential for both glorious success and frustrating failure.

## §8 · The Mechanics of the Gamble
This section details the universal rules for converting EP into dice.

### 8.1 · The Base Cost: Buying a Die
The fundamental cost to convert EP into a single die is based on the die's potential, making larger dice a greater initial investment.

Base Cost = (Number of Faces / 2) EP per die.

| Die Type | Base EP Cost | Average Result |
| 1d2 | 1 EP | 1.5 |
| 1d4 | 2 EP | 2.5 |
| 1d6 | 3 EP | 3.5 |
| 1d8 | 4 EP | 4.5 |
| 1d10 | 5 EP | 5.5 |
| 1d12 | 6 EP | 6.5 |

Export to Sheets
### 8.2 · The Law of Diminishing Returns (The "Ante")
Your insight about preventing a player from rolling 30d2 is critical for balance. To roll many dice is to demand much of fortune, and fortune taxes such demands heavily.

The Rule: The first die you add to a pool for an action costs its Base Cost. Every subsequent die of the same type costs its Base Cost + the number of dice already in the pool.

This escalating "ante" makes rolling a few dice an efficient gamble, while rolling many becomes an act of extravagant and inefficient hope.

Example: Rolling d6s

1d6: Costs 3 EP.

2d6: Costs 3 (for the first die) + (3 + 1 ante) (for the second) = 7 EP.

3d6: Costs 7 (for the first two) + (3 + 2 ante) (for the third) = 12 EP.

4d6: Costs 12 (for the first three) + (3 + 3 ante) (for the fourth) = 18 EP.

### 8.3 · Hybrid Investment: The Cautious Gamble

The Rule: A player can declare they are splitting their EP investment for an action. Part of the EP is converted into a dice pool (following the "Ante" rule), and the rest is added as a raw, deterministic bonus. This mirrors the classic [dice] + [modifier] structure of many TTRPGs.

Example: A warrior wants to make an attack with 12 EP.

Pure Will: Spends 12 EP to deal a flat 12 damage.

Pure Fortune: Spends 12 EP to roll 3d6 (cost 12 EP), for 3-18 damage.

Hybrid Investment: Spends 7 EP to roll 2d6, and adds the remaining 5 EP as a flat bonus. The result is 2d6 + 5 damage, for a range of 7-17. This provides a safe "floor" for the damage while still allowing for a lucky roll.

## §9 · Applications of the Principle
This system can be woven into every aspect of the game.

Combat (Damage & Defense): As established, both attackers and defenders can use this system. An attack can be 2d8+3 damage, and a defender might use a 1d12 parry to try and block it. All dice, attack or defense, are subject to the Exploding Dice and Hard Cap rules.

Spellcasting (Range & Effect): A spell's range can be converted to dice. A caster might spend 10 EP on range. They could take the safe 50 feet (10 EP * 5 feet/EP), or they could gamble by spending 6 EP to roll a 1d12 and adding the remaining 4 EP as a flat bonus, for a total range of (1d12 + 4) * 5 feet.

Environmental Manipulation: Your earthbender example is perfect. Instead of spending 5 EP to create a 25-foot wall, they can spend the 5 EP to roll a 1d10. The result, rounded to the nearest 5, determines the wall's length in feet. This makes even utility actions tense and exciting.

Skill Checks: A rogue trying to pick a difficult lock might need to overcome a high TN. Instead of just adding their modifier, they could declare, "I'm investing 4 EP to roll 1d8 and add that to my lockpicking check!"

## §10 · Assemblé
An action is a ripple cast upon the sea of reality. A punch, a spell, a hurried step—all are expenditures of the soul's finite potential. This module provides the grammar for that expenditure. It defines the cost of a warrior’s fury, the reach of a wizard’s ambition, and the price of a body’s endurance. Through these rules, the abstract concept of will is forged into the concrete, tactical art of existence.