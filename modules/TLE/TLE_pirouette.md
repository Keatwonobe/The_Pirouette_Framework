## TLE-000_Entropy_as_resource.md

---
#───────────── The Lost Eternal ──────────────────────
id:        TLE-000
title:     The Soul of the Character, The Entropic Form
version:   1.0-consolidated
parents:   [PIR-0, PDM-000]
children:  [TLE-001]
engrams:
 - system:character-creation
 - mechanic:entropic-budget
 - system:attribute-allocation
 - concept:health-as-coherence
 - mechanic:body-part-system
keywords:  [character creation, attributes, entropy, health, body, form, TLE]
uncertainty_tag: Low
module_type: core-rulebook-consolidated
---
## §1 · Preamble: The Sculptor's Will
In the universe of The Lost Eternal, a being is not born into a fixed form. A being is a form, sculpted from the raw potential of their own will. This module provides the foundational rules for this process. It consolidates the core principles of character creation, replacing the previous TLE-000 through TLE-006 with a single, unified system.

The core principle is this: All aspects of a character—their physical might, their mental acuity, their very health and form—are expressions of a single, fluid resource: Entropy. A character sheet is not a list of stats; it is a ledger of entropic investment.

## §2 · The Entropy Budget: The Starting Spark
Every new entity begins with a finite pool of potential from which they must construct their entire being.

Starting Entropy: A standard starting player character begins with a Total Entropy Pool (TEP) of 35 Entropy Points (EP). This is the sole resource used for character creation.

## §3 · The Five Attributes: The Containers of Will
An entity's TEP is first distributed across five core attributes. These are not passive modifiers but deep reservoirs of potential that define a character's innate capabilities.

Attribute Scaling:

Score: An attribute's Score is equal to half the total EP invested in it, rounded down. Score = floor(EP Invested / 2).

Modifier: An attribute's Modifier is equal to one-quarter of its Score, rounded down. Modifier = floor(Score / 4).

The Five Attributes:

Strength (STR): Governs the application of raw physical power.

Checks: When making a Strength check to overcome a variable force, you roll 1d[STR Score]. The result is the amount of entropy you bring to bear.

Combat: Your STR modifier adds to your physical attacks. For every +1 modifier, you may add an additional die of damage (e.g., a +2 modifier allows you to spend 2 extra EP to turn a 1d8 attack into a 1d10 attack).

Dexterity (DEX): Governs agility, reflexes, and control over the flow of action.

Initiative: At the start of each turn, you may spend a number of EP up to your DEX modifier to shift your position in the initiative order.

Constitution (CON): Governs an entity's connection to the flow of entropy and their physical endurance.

Regeneration: This remains the primary source of an entity's Entropy Regeneration Rate (ERR), as defined in TLE-000.

Intelligence (INT): Governs logic, memory, and the ability to impose complex will upon the world.

Combat Utility: Your INT modifier provides a pool of "free" EP each round that can be spent on any action.

Knowledge: Your INT modifier can be applied as a bonus to the DC of a knowledge-based check. It also serves as a tiebreaker for contested spellcasting checks.

Wisdom (WIS): Governs intuition, perception, and defensive insight.

General Utility: Your WIS modifier provides a pool of "free" EP that can be spent on any skill or ability check outside of combat.

## §4 · The Physical Form: The Architecture of Being
After allocating EP to attributes, a character must spend EP to create their physical body.

The Cost of Form:
| Body Part | Base EP Cost | Notes |
| :--- | :--- | :--- |
| Torso | 1 EP | Required. The core of the form. |
| Head | 1 EP | Required. Houses the primary consciousness. |
| Standard Limb (Arm/Leg) | 3 EP | A complete limb with hand/foot. |
| Basic Limb (Tail/Tentacle)| 2 EP | A simpler, more flexible limb. |
| Wing | 4 EP | A limb specifically for flight. |
| Sensory Organ (Eye/Ear) | 1 EP | A single organ. See §5. |
| Utility Limb | 1 EP | A complex Limb, see below, may replace any of the above parts or be added. |

Size as Invested Power: EP can be invested into a limb beyond its base cost. This Size Entropy is ring-fenced and can only be used to power physical interactions with that limb (e.g., a punch or kick). This allows a character to have, for instance, a "normal" left arm (3 EP cost) and a massive, powerful right arm (3 EP cost + 15 EP Size Entropy).

Utility Limb (4 EP): Some forms are not defined by simple arms and legs, but by specialized tools of survival and predation. A Utility Limb is a specialized body part—such as a fang-filled maw, a pair of razor-sharp claws, a stinger-tipped tail, or bioluminescent nodules—that serves a unique biological function. While it cannot manipulate objects like a standard limb, it can be invested with its own dedicated pool of Entropy to power its unique abilities, such as a venomous bite or a rending claw attack.

## §5 · The Sensory Suite: The Windows to the World
An entity's perception is a direct function of their investment.

The Cost of Senses: Each sensory organ costs 1 EP. A standard human begins with two eyes and two ears (4 EP total).

Perception Checks: An entity may make one passive perception check per relevant sensory organ each round. This makes characters with exotic or numerous senses (e.g., antennae, whiskers, scent organs) exceptionally aware of their surroundings.

## §6 · Health & Defense: The Integrity of Form
An entity's health and durability are direct measures of their coherent integrity.

The Health Pool: An entity's Hit Points (HP) are not an abstract score but are derived directly from the EP invested in their physical form.

Max HP = (EP in Torso) + (0.5 * Total EP in all Limbs, rounded down)

Armor & Shields as Entropic Pools: Armor and shields are not passive defenses. They possess their own Armor Entropy Pool (AEP). When an entity with armor takes damage, the damage is first subtracted from the armor's AEP. Any remaining damage is applied to the entity's Health Pool. This makes armor a destructible, repairable resource.

## §7 · Assemblé
A being is a choice, written in the language of Entropy. Every point invested is a declaration of purpose, from the strength of a limb to the sharpness of an eye. There is no distinction between the self and the power it wields. The character sheet is not a description of the soul; it is the soul itself, rendered in the mathematics of will.

---

## TLE-001_the_application_of_entropy.md

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

---

## TLE-002_control_and_conversation.md

---
#───────────── The Lost Eternal ──────────────────────
id:        TLE-002
title:     The Art of Control & Conversation
version:   1.0-draft
parents:   [TLE-006]
children:  [All future TLE modules related to social interaction, summoning, and mental effects]
engrams:
 - mechanic:grappling
 - mechanic:mind-control
 - system:necromancy-and-summoning
 - system:conversation-as-combat
keywords:  [grappling, mind control, curses, necromancy, conversation, social combat, TLE]
uncertainty_tag: Low
module_type: core-mechanic-expansion
---
## §1 · Preamble: The Contested Will
The purest expression of power is not the force of a blow, but the imposition of one's will upon another. This module details the mechanics of control, from the physical struggle of a grapple to the subtle war of a tense negotiation. It defines the rules for subverting an opponent's mind, cursing their form, raising the dead, and engaging in the high-stakes combat of conversation.

## §2 · Physical Control: The Grapple
A grapple is a contested roll to determine physical dominance, relying on both power and technique.

Mechanic: To initiate or escape a grapple, both entities make a contested roll. The roll is a combination of their physical attributes.
Grapple Check = d20 + STR Modifier + DEX Modifier

Resolution: The higher roll wins. A successful grapple can render an opponent immobile, prevent them from using certain limbs, or create an opportunity for a follow-up attack. A nimble rogue with high Dexterity can just as easily pin a powerful knight as the other way around, representing a victory of technique over brute force.

## §3 · Mental & Arcane Control
The most potent forms of control bypass the physical entirely, targeting an entity's mind and will.

### 3.1 · Mind Control
This is a direct assault on an entity's Intelligence score.

Mechanic: The attacker makes a contested roll of their (d20 + INT Mod + WIS Mod) against the target's (d20 + INT Mod + WIS Mod). If the attacker wins, they temporarily reduce the target's Intelligence Score by the difference.

The Handicap: For each point the target's Intelligence Score is pushed into the negative, they suffer an "entropy handicap." Any action they attempt that is not permitted by the controller costs an additional EP equal to their negative Intelligence Score.

Full Control: If the handicap becomes greater than the target's Entropy Regeneration Rate, they are effectively puppeted by the controller, who can now spend their own Actions to command the target.

Caster Cost: EP spent to maintain a mind control effect is locked and cannot be regenerated until the effect is released.

### 3.2 · Curses
A curse is a malicious reallocation of a target's own entropy. A werewolf's curse, for example, might forcibly drain all EP invested in Intelligence and Wisdom and dump it into Strength and Dexterity, creating a powerful but mindless beast.

### 3.3 · Necromancy & Summoning
A necromancer or summoner externalizes their own will, giving it form.

Mechanic: The caster "releases" a portion of their TEP, which becomes the TEP for the summoned creature. The caster cannot regenerate this released EP until the minion is destroyed or dismissed.

Minion Upgrades: A necromancer can store additional released EP in artifacts like rings or phylacteries, allowing them to maintain a larger or more powerful retinue of undead. The minion's body is constructed using the same rules as a player character (TLE-002).

### 3.4 · Intangible Grapples
Spells like a telekinetic grasp function as a grapple but use the caster's (d20 + INT Mod + WIS Mod) against the target's (d20 + STR Mod + DEX Mod). This makes a powerful mage a dangerous grappling threat, capable of pinning foes from a distance.

## §4 · Conversation as Combat
Social interaction is not a passive skill check; it is a dynamic battle of wits, presence, and will. "Charisma" is not an attribute, but the successful application of tactics in conversational combat.

### 4.1 · Entering the Conversation
Any attempt to persuade, deceive, intimidate, or haggle with a significant NPC initiates conversational combat. Both sides roll for initiative (d20 + DEX Modifier), and the normal rules for initiative order apply.

### 4.2 · The Mental Battlefield
A conversation has its own "health pools."

Resolve: An entity's Intelligence Score. Represents their logical fortitude and ability to resist deception.

Composure: An entity's Wisdom Score. Represents their emotional stability and willpower.

### 4.3 · Statements as Actions
An entity can make a number of "statements" (actions) per turn based on their attributes, as defined in TLE-004. Each statement is a social "attack."

Mechanic: The attacker makes a contested roll based on their approach. Intimidation might be a (d20 + STR Mod) check, while a clever persuasion might be a (d20 + INT Mod) check.

Damage: If the attacker wins, they deal "damage" equal to the EP they spent on the statement. This damage is split evenly between the target's Resolve and Composure, rounded down.

Vulnerability: Attacking the lower of the two mental pools is the key to victory. A brilliant but emotionally fragile academic is vulnerable to appeals to their ego (targeting Composure).

### 4.4 · The Stakes of Conversation
Reducing a target's mental pools to a negative value does not grant the attacker mind control, but it does achieve a social victory.

Outcome: A "defeated" opponent might be persuaded to lower their prices, convinced of your argument for the moment, or intimidated into backing down.

Impermanence: Just like in the real world, the effects of a single conversation are rarely permanent. Water carves canyons over time. A convinced opponent may change their mind later, and an intimidated foe may return with reinforcements.

---

## TLE-003_downtime_travel_and_the_economy_of_will.md

---
#───────────── The Lost Eternal ──────────────────────
id:        TLE-003
title:     Downtime, Travel, and the Economy of Will
version:   1.0-draft
parents:   [TLE-007]
children:  [All future TLE modules related to world-building, economy, and downtime activities]
engrams:
 - system:downtime-activities
 - mechanic:resource-management
 - concept:city-entropy-budget
 - system:barter-economy
keywords:  [downtime, travel, healing, economy, barter, crafting, world-building, TLE]
uncertainty_tag: Low
module_type: world-building-and-mechanics
---
## §1 · Preamble: The Unfolding World
The life of an adventurer is not solely defined by the flash of a blade or the crackle of a spell. It is also shaped by the long roads between destinations, the quiet moments of recovery and creation, and the complex web of needs and resources that binds civilization together. This module provides the rules for the "in-between" time—downtime, travel, and the unique economic landscape of a world scarred by forgotten magic.

## §2 · The Downtime Entropy Budget
During non-combat time (travel, resting, working in a city), an entity's will is not idle. It is constantly generating a pool of potential that can be directed toward a single, focused task. This is the Downtime Entropy Budget.

Mechanic: An entity's Downtime Budget is equal to their Entropy Regeneration Rate (ERR), applied over a given period. This budget can be spent on any single, non-combat task they are capable of performing.

Example Tasks: Healing (TLE-005), Crafting (TLE-004), Research, or maintaining passive awareness.

### 2.1 · The Traveler's Dilemma
Travel is the most common downtime activity, and it presents a crucial choice. An entity moving at their base speed (spending no EP on specialized movement) can apply their full Downtime Budget to a task.

The Choice: A wounded adventurer might dedicate their entire budget to healing, allowing them to recover from battle while on the road. However, by focusing their will inward, they are not spending any entropy on awareness. They make no passive perception checks and are vulnerable to ambush.

The Alternative: A cautious adventurer might dedicate their budget to Vigilance, spending their regenerated EP on constant perception checks to scan for danger. They will be much harder to surprise, but they will not heal any damage they have sustained. This creates a constant, meaningful resource management choice for the party.

## §3 · The World After the Prospero
The current economic and ecological landscape is a direct result of the fall of the Skazan Order and their master mages, the Prospero. The Prospero could create sustenance from their own will, but their magic was a poor defense. In their fall, they unleashed a chaotic torrent of creation that has permanently scarred the world.

The Environment: Vast fields of wild wheat are plagued by ergot, which blows in hallucinogenic fungal storms. Rivers run red and brackish with the remnants of magical wine. Forests are overgrown and filled with colossal, aggressive swarms of bees.

The Remnants: Ancient Skazan constructs still wander the continent on clockwork paths, their original purpose long forgotten. The trails they leave are often the only safe roads through the hazardous wilderness.

## §4 · The Economy of Need
In this strange world, traditional currency is almost worthless. The fall of the Skazan shattered any centralized economy, and the great roaming cities that remain are fiercely independent, each with their own culture and needs.

### 4.1 · Barter as Law
The primary method of exchange is barter. An adventurer's skill, the Entropy Shards they find, or a unique item they've crafted are far more valuable than a pocketful of forgotten coins. Value is determined by immediate, practical need.

### 4.2 · The City Entropy Budget
Every settlement, from a tiny village to a great roaming city, has a collective City Entropy Budget. This is a measure of its overall stability, needs, and ability to withstand threats.

Formula: The GM can estimate a city's budget by multiplying its approximate population by an "Average Individual Budget" (AIB) that reflects the local standard of living.
City Budget = Population * AIB

A Tool for Adventure: This budget is a powerful tool for the GM to generate quests. By comparing the City's Budget to the entropic signature of its surroundings, a clear picture of the city's needs emerges:

If Environment EP > City EP: The city is in immediate danger from an overwhelming external threat (e.g., a massive bee swarm, an approaching fungal storm).

If a High EP Bubble is Nearby: The city may feel threatened by an unknown power and hire adventurers to investigate.

If Environment EP is Low: This signals a problem like a magical blight, a severe drought, or a curse, prompting the city to seek a solution.

## §5 · The Weaponized Profession
Any profession, no matter how mundane, can be weaponized through the focused application of will and Entropy. A character with the Professional Aptitude feat can treat their "Professional" skill pool as a versatile tool for both utility and combat.

The Principle: You can spend EP from your Professional skill pool to fuel actions related to your trade. This is a narrative-first mechanic. A tailor might spend EP to animate needles and send them flying like darts. A blacksmith could spend EP to super-heat a piece of metal and use it as a thrown weapon. A farmer's lethality with a pitchfork is a direct result of the entropic focus they've honed through a lifetime of labor.

Constructs & Companions: A craftsman can create a companion related to their trade (a tailor's animated rug, a blacksmith's clockwork hound). These constructs are created and maintained using the standard Taming & Bonding rules, requiring a significant TEP and ERR investment from their creator.

## §6 · Temporary Enchanting: Imbuing Objects
A character can temporarily invest a portion of their own will into an object they have personally modified, creating a single-use enchanted item.

The Investment: As part of a short rest, you can invest your own EP into an object you have modified (e.g., carving a simple rune, tying a specific knot). This EP is removed from your own TEP and does not regenerate. The object is now "charged."

The Trigger: You must set a trigger condition for the stored Entropy to be released. This can be on contact, on a spoken command word, or when the object is broken.

Detection: A charged object radiates a faint entropic aura. The Target Number to detect this aura is equal to the EP invested. A weakly charged item is thus harder to detect than a powerfully charged one. This can be further concealed by the Veiled Casting feat.

## §7 · Crafting & The Materials Economy
The world is rich with strange and potent materials. A skilled professional can forage for these resources and use them to craft powerful new items.

### 7.1 · Foraging & Material Tiers
All characters with the Professional Aptitude feat are assumed to have the necessary skills to find and identify materials relevant to their trade. The success and quality of these materials are determined by a survival challenge set by the GM. Materials are categorized into four tiers of quality.

Tier 1 & 2 (Common): Can hold a maximum of 5 EP when used in a crafting recipe.

Tier 3 (Uncommon): Can hold a maximum of 20 EP.

Tier 4 (Rare): Can hold a maximum of 50 EP.

### 7.2 · The Crafting Process
Crafting an item requires a recipe, the correct tiered materials, and an investment of the craftsman's own will.

Recipes: A recipe is a blueprint that calls for specific types and tiers of materials (e.g., "one part Tier 3 Metal, two parts Tier 1 Leather").

Crafting ERR: A character can invest additional TEP directly into their Professional skill pool. This investment serves two purposes: it acts as a dedicated pool for weaponizing their profession, and it increases their Crafting ERR, allowing them to complete complex projects more quickly.

---

## TLE-004_the_environment_and_survival.md

---
#───────────── The Lost Eternal ──────────────────────
id:        TLE-004
title:     The Environment & The Art of Survival
version:   1.0-draft
parents:   [TLE-008]
children:  [All future TLE modules related to specific biomes, hazards, and survival challenges]
engrams:
 - system:environmental-budgeting
 - mechanic:environmental-hazards
 - concept:entropic-corruption
 - system:survival-as-combat
keywords:  [environment, survival, hazards, foraging, world-building, TLE]
uncertainty_tag: Low
module_type: world-building-and-mechanics
---
## §1 · Preamble: The World as a Character
The world itself is the oldest and most powerful entity a character will ever encounter. It is not a static backdrop for adventure, but an active, often hostile, participant in the story. This module provides the rules for treating the environment as a character with its own will, its own actions, and its own resources, and introduces the final form of combat: the struggle for survival.

## §2 · Environmental Budgeting
To understand the environment, one must first measure its will. Every region, from a serene meadow to a raging volcano, has an Entropy Budget that defines its nature and power.

### 2.1 · Quadrant Budgeting
A GM can quickly estimate the power of a region by calculating its Entropy Budget.

Formula: For a quick estimate, a GM can use a baseline of 45,000 EP per sentient inhabitant per day. This budget represents the total entropic output of the region's ecosystem.

Resolution: By comparing the budget of a settlement to the budget of the quadrant it's in, a GM can instantly gauge its significance. A small camp's destruction is a minor event. The fall of a major trading post could destabilize the entire region.

## §3 · The Environment in Combat
The environment is an ever-present entity that can act on its own initiative.

### 3.1 · Hazards as Minigames
Environmental hazards are not just passive damage sources; they are active opponents.

Mechanic: A hazard like a roaring fire or a blizzard has its own Entropy Pool and acts on its own turn. It can "attack" characters within its area of effect, forcing them to use Active Defense to resist being burned or frozen.

Forced Movement: If a hazard would push a character (e.g., a gust of wind, a rushing river), for every 5 feet the character cannot move, the remaining entropic force is dealt as damage.

### 3.2 · Traps & Lingering Entropy
Entropy that is stored externally to a host (in a magical trap, for instance) remains in the environment if the host dies. This can lead to ancient, masterfully crafted traps that are still lethally potent centuries after their creator has perished.

### 3.3 · Entropic Corruption
The environment reacts to the will imposed upon it.

The Rule: For every 2 EP a character spends on a magical effect (that is not simply moving an existing element), the environment in that 5x5 cube loses 1 EP from its budget.

The Consequence: Over time, a fire mage's sanctum will become a cold, ashen wasteland. A paladin's holy ground, site of many smites, will blacken and corrupt. This makes places of great magical power deeply scarred and often dangerous, requiring constant maintenance to remain stable.

The Exception: Spells that simply move or shape existing elements (e.g., controlling water, raising a wall of earth) do not cause corruption. This "natural" magic works in harmony with the environment.

### 3.4 · Shaping the Environment
An entity can create or shape matter from raw entropy.

Formula: Creating a 5x5x5 foot cube of a simple element (earth, ice, etc.) costs 5 EP. This scales linearly. A 10-foot-tall, 60-foot-long wall of ice would cost (10/5) * (60/5) * 5 = 2 * 12 * 5 = 120 EP.

Weaponizing the Environment: A shaped element can be used as an attack. A 5x5x5 foot block of ice can be hurled to deal 1d5 damage.

### 3.5 Light Levels

Light in the world can take one of nine levels: Total darkness > Fuzzy outlines > Vague Shapes > Dim Light > Normal Light > Full Light > Bright Light > Blinding Light > Total Whiteout

Characters can see normally in dim, normal and full light while taking a penalty to the TN of any attack or skill check made in other tiers based on how far away form perceptible it is. The target number goes up by 3 for each tier of light outside of visible light. 

Lights begin and end, meaning there is darkenss beyond them. Total Whiteout and Darkness require perceiving a target to make an attack. Feats that grant sight change or nullify these effects.

### 3.6 Poison

Poisons and venoms are like an item in that each has its own rules, but generic "venom" or "acme poison" would poison constitution directly, removing EP from it each round while poisoned. That means eventually ERR goes to 0 and death.

The Poisoned State: Some attacks do more than tear flesh; they corrupt the very essence of a being. A creature afflicted with the Poisoned state has had its entropic form compromised. At the end of its turn, a poisoned creature must make a Constitution check against the poison's potency. On a failure, they lose a specified amount of EP directly from their Constitution attribute pool, representing their body's struggle to maintain coherence. This loss reduces their Constitution Score and, consequently, their Entropy Regeneration Rate. If a creature's Constitution EP is reduced to 0, it perishes.

Mastering Potency (Alchemy): For those without a natural venom, poison is a craft to be mastered. By taking the Professional Aptitude (Alchemy) feat, a character can learn to brew toxins. The alchemist can invest additional TEP directly into their Alchemy skill beyond the initial feat investment. This invested EP represents their growing knowledge and serves as the dedicated pool from which they can enhance the potency of the poisons they create, making each dose more difficult to resist.

Mastering Potency (Biology): For some creatures, venom is not a craft; it is an extension of their own being. A character with a venomous Utility Limb (such as a stinger or fangs) can invest TEP directly into that limb's dedicated pool. This investment represents a biological optimization—a diet, meditative practice, or resonant focus—that refines and concentrates their natural toxins. The EP invested in the limb determines the potency of the venom it delivers.

## §4 · Survival as Combat
Foraging and surviving in the wild is the third and final form of combat. It is a contest between a character's will and the will of the environment itself.

### 4.1 · The Survival Encounter
When characters attempt to live off the land, they roll for initiative. The environment is their opponent.

The Opponent: The environment's "attributes" and "health pools" are derived from its Entropy Budget. A lush forest is a low-level opponent with plentiful resources. A barren desert is a high-level foe that is actively hostile.

The Health Pools: In a survival encounter, a environment's four core attributes (STR, DEX, INT, WIS) are their health pools. The environment will "attack" the HP character pools with various challenges.

### 4.2 · The Contest
The environment is not trying to have a conversation; it is trying to kill you.

Mechanic: The GM presents challenges that target a character's attributes. A chasm might require a Strength check to cross. A patch of poisonous berries requires an Intelligence check to identify. A hidden pitfall requires a Dexterity check to avoid. Failure results in damage as entropy.

The Goal: The players must successfully overcome these challenges to find the resources (food, water, shelter) they need, all while defending their own entropy pools from the environment's relentless assault.

## §5 · Dynamic Terrain: Imposing Your Will
Any being with control over their entropic output can alter the physical state of their surroundings, creating areas of difficult or impassable terrain.

### 5.1 · The Principle of Difficult Terrain
A 5-foot square of terrain that has been made difficult—such as by creating slick ice, grasping thorns, or super-heated air—impedes movement.

Movement Cost: To move through a 5-foot square of difficult terrain, a creature must succeed on a d2 roll. On a result of 1, their movement for the turn ends, though they still expend 5 feet of movement.

Creating Difficult Terrain: As an action, a character can spend 3 EP to make a 5-foot square within 30 feet into difficult terrain.

Intensifying Terrain: A character can intensify an existing patch of difficult terrain by spending an additional 5 EP. For each 5 EP spent in this way, a creature must make one additional successful d2 roll to pass through the 5-foot square.

Verticality & Falling: Each d2 roll required to move through a space is considered the equivalent of 5 feet of movement for the purposes of verticality. A creature falling through a 15-foot cube of turbulent air would need to make three successful d2 rolls to stop their fall; failure would result in them taking fall damage.

### 5.2 · The Principle of Persistence
Entropic manipulation of the environment is not a fleeting effect that requires concentration. It is a physical change to the world that decays slowly over time.

Duration: A patch of dynamically created difficult terrain remains in effect for one day per EP spent on its creation and intensification. A patch of terrain created with an initial 3 EP and intensified once with 5 EP (total 8 EP) would last for eight days (or until its entropy is exhausted by the environment like ice melting in the sun).

## §6 · Entropic Zones: The Arcane Battlefield
The environment can be viewed as a grid of 5-foot squares, each with its own entropic state. Powerful beings can engage in a battle of wills not by targeting each other directly, but by vying for control over these environmental zones.

### 6.1 · Establishing Control
As an action, a caster can invest EP from a relevant Arcane Skill pool into a 5-foot square within line of sight. This square is now a Controlled Zone. The amount of EP invested determines the strength of their control.

Example: A pyromancer invests 10 EP into a square (5 centered, with 2, 1, 1, 1 surrounding), causing it to smolder and glow with heat. A progenitor druid invests 8 EP into an adjacent square (4 centered with 1, 1, 1, 1 surrounding), causing thick, thorny vines to sprout.

### 6.2 · Contesting a Zone
If a caster targets a Zone that is already controlled by another being, a contest of wills begins.

The Overwhelm: The new caster invests their desired amount of EP. The being with the higher total EP invested in that Zone now controls it. The lesser investment is overwhelmed and its effect is nullified.

The Stalemate: If both casters have invested the exact same amount of EP, the Zone becomes a Contested Zone. The two elemental forces clash violently, creating a chaotic and dangerous area (e.g., a fiery vortex of thorns) that is hostile to all creatures.

### 6.3 · Propagation of Influence
A caster can use their Controlled Zones as a focal point to spread their influence across the battlefield.

The Rule of Adjacency: As an action, a caster can target any 5-foot square that is adjacent to one of their existing Controlled Zones, even if they do not have a direct line of sight to the new square. This allows a caster to "grow" their influence, spreading fire from a smoldering patch or having frost creep across the floor from a frozen spot. This makes establishing and maintaining a foothold on the battlefield a critical tactical objective.

## §7 · The Principle of Becoming
The question "Where do you come from?" is one of the most complex in the multiverse. While the act of courtship and romance is a cherished and common path to creating new life, it is but one thread in a vast and intricate tapestry. Origin stories are as varied as the beings themselves, and the answer "like everyone else" is a rarity. Family is a bond of will, not merely a matter of birth.

### §7.1 · Paths to Being
- Born of a Dream
Among some ancient and fey-touched lineages, new life is not conceived but discovered. An Elven dream priestess might walk the ethereal pathways of a sleeping mind and find, within a particularly innocent or powerful dream, a nascent soul. With gentle care, she can coax this dream-stuff into the waking world, where it coalesces into a new child, its first cries still echoing with the logic of slumber.

- Carved from the Earth
For beings deeply connected to the bones of the world, creation is an act of craft. Gnomish parents, for example, might spend years carving the perfect vessel for their child from a block of ancient wood or a sacred geode. When the form is complete, they perform a ritual to invite a spirit to inhabit it, and the carved figure awakens with the sturdiness of stone and the slow, deep wisdom of the earth.

- Forged by Nature
Some of the most powerful beings are not born of other beings at all, but are direct manifestations of the world's raw, chaotic power. A Giant might be born when a volcano rages, its body forming from a boulder of cooling magma. A roaring thunderstorm might birth a Storm Giant from a hailstone of impossible size that crashes to the earth. These beings are not children in the traditional sense, but living embodiments of a moment of profound natural force.

- Uplifted from the Wild
The bond between a druid and the natural world is so deep that it can transcend the boundaries of species. A druidic couple might find a young animal whose parents have perished. Through a powerful ritual of uplift, they can invest a portion of their own will and entropic potential into the creature, granting it sapience and a humanoid form. This child is raised with the instincts of the wild and the loving guidance of its chosen family.

- Willed into Being
In places rich with entropic residue or deep emotional resonance, life can arise spontaneously. An Etceteron—a being made of miscellaneous scraps of glass, cloth, and forgotten things—might be carefully assembled by a lonely soul who needs a friend. Or, it might pull itself from a junk heap, a consciousness born from the lingering memories and chaotic energy of a thousand discarded objects, achieving a life of its own.

- The Primal Font
For some elemental spirits, the source of new life is a finite and precious resource. Water Sprites of a particular glen might vie for control of a sacred spring that, once a year, seeps a single droplet of primal, life-giving liquid. The sprite who claims this droplet can use it to sculpt a new member of their kind, making the act of procreation a yearly contest of skill, cunning, or combat.

- The Dragon's Riddle
The origin of dragons is a paradox. Some are hatched from eggs of gemstone or metal laid by a great matriarch. Others are said to be "raised" from mundane lizards or serpents by an elder dragon's will. Still others are believed to be carved from a single, flawless gem and animated by a ritual that costs the lives of a dozen mages. The dragons themselves remain silent on which story is true, adding another layer to their mystique.

## Equipment & Artifacts

## §8 · Mundane Gear: The Tools of Survival
### 8.1 · Weapons: The Shape of the Strike
The power of a weapon comes not from its type, but from its quality and how it is wielded. All weapons deal damage based on the wielder's invested Entropy; the weapon itself simply provides an edge of efficiency.

Weapon Quality: The damage a weapon adds to a strike is determined by its craftsmanship.

Poor (1d2): A rusty shiv, a poorly-made club.

Fair (1d4): A standard bandit's blade or scavenger's axe.

Good (1d6): A well-crafted weapon from a city smith.

Excellent (1d8): A masterwork piece.

Perfect (1d12): The pinnacle of mundane craftsmanship.

Enchanted (1d13+): See §2.

Wielding Style:

Two-Handed: When you attack with a weapon in two hands, you make a single attack roll, combining the Entropy of two swings into one devastating blow.

One-Handed / Dual-Wield: When attacking with one-handed weapons, you make two separate, faster strikes. You can target the same creature twice or two different creatures.

Reach: A weapon with the "Reach" property (spear, halberd) can be used to make melee attacks against targets up to 10 feet away without any additional EP cost for range.

### 8.2 · Armor & Shields: The Art of Defense
Armor and shields do not have a health pool. Instead, they provide a chance to negate incoming damage through their inherent quality and the wielder's skill.

Armor: When you are hit by an attack, you may roll your armor's protection die. The result is subtracted from the incoming attack's damage as a form of entropic buffering.

Light Armor (Leather, Studded): 1d2 - 1d4

Medium Armor (Scale, Chain): 1d4 - 1d6

Heavy Armor (Plate): 1d6 - 1d8

Masterwork & Magical: 1d10+

Shields: A shield is an active defense tool. When you are targeted by an attack, you can use your reaction to either:

Block: Roll the shield's protection die and subtract the result from the incoming damage.

Deflect: Roll the shield's protection die and subtract the result from the attacker's to-hit roll.

Shield Quality: Bucklers (1 EP block), Wooden Shields (1d2), Steel Shields (1d3+).

## §9 · Enchanted Items & Artifacts
### 9.1 · The Enchanting Process
Enchanting an item is an act of permanent sacrifice, imbuing a piece of your own soul into an object.

The Cost: The base cost to give an item a magical property is a 3 TEP permanent sacrifice. This creates a simple "+1" effect. More powerful effects require a greater sacrifice (e.g., a "+2" effect costs 6 TEP).

Utility Items: Most magical items function as "dummy companions." They have their own small, dedicated EP pool that can only be used to power their specific effect (e.g., Boots of Speed might have a 3 EP pool that recharges, allowing the wearer to spend it on extra movement). This TEP is sacrificed by the creator and does not belong to the wearer.

### 9.2 · Attunement & The Price of Greed
There is no limit to the number of magical items a character can wear, but there is a limit to how much power one soul can safely channel.

The Overload Limit: A character can safely wear and use magical items whose total TEP cost is up to twice their own TEP.

The Risk: If you wear items exceeding this limit, you become Overloaded. Each time you use an ability from any of your magical items, you must roll a die equal to the item's EP cost. If the result is equal to or less than the amount of TEP you are Overloaded by, you permanently lose that much TEP. This lost TEP dissipates into the environment as chaotic Residue.

### 9.3 · Fate-Bound Weapons
A deep bond can be formed between a wielder and their weapon.

The Bond: By permanently investing at least 9 TEP into a single weapon (for damage, effects, or otherwise), it becomes Fate-Bound. A Fate-Bound weapon will always return to its wielder's hand if lost, thrown, or sold.

Contested Ownership: If another being invests more TEP into the weapon than the original owner, the bond is broken and a new one is formed.

## §10 · The Reward Loop
### 10.1 · Harvesting & Foraging
The true wealth of the bottom realm is found in the remains of its strange inhabitants and the potent materials of the land.

The Silent Auction: When harvesting a creature for valuable trophies or foraging for rare materials, the GM determines the total potential value. The player then makes a "silent bid," investing EP from a relevant skill (like Survival or a Professional skill). If the bid meets or exceeds the GM's hidden TN, the harvest is successful. Invest too much and potentially fail. Invest too little and miss out.

### 10.2 · Types of Rewards
Skins & Trimmings: Tiered crafting materials harvested from creatures.

Crafting Recipes: Blueprints for new items, found as diagrams, taught by a master, or reverse-engineered from an existing artifact.

Loot: Physical items, including mundane gear and enchanted artifacts.

Knowledge: Information gained by "conversing" with a location through skills like Investigation or Archaeology. The reward is a new clue, a hidden truth, or a forgotten story.

## §11 · Investing in the World: Land, Lairs & Commerce
Beyond personal gear, a character's true power can be measured by their investment in the world itself—be it a claim of land, a thriving business, or a lair that is a living extension of their will.

### 10.1 · Claiming Land
Land in the wastes is not bought, but won through persistence and strength of will.

The Claim: To claim a piece of land, a character must openly and actively homestead it. The maximum size of this claim in acres cannot exceed the character's TEP at the time the claim is made.

The Trial of Establishment: For the first 90 days, the claim is contested. The homesteader must defend their land from scavengers, beasts, and opportunistic rivals.

Established Holding: After 90 days of successful defense, the owner is considered "established." While major threats may still arise, the chaotic, constant pressure of the trial period subsides.

Purchasing Land: Land within an established territory (like a city or protected village) can be purchased outright, foregoing the trial period.

### 10.2 · Commerce & Guilds
Setting up a business requires navigating the complex social structures of the walking cities.

Merchant Guilds: Most cities have a merchant guild. A craftsman can leave their goods with the guild to be sold at a fixed rate, with the guild taking a cut from the final sale price.

Licensing: To operate an independent shop, one must acquire a license from the city's head of commerce. This is a social or economic challenge, typically requiring an excellent barter of rare goods or a direct entropic trade (an average of 30 TEP per year).

### 10.3 · Consecrated Ground & Sentient Lairs
A being's territory can become a literal extension of their power.

Favored Ground: A character can perform a ritual to consecrate or desecrate a piece of land, aligning it with their own entropic nature. While on this favored ground, the character's ERR is increased by 1.

The Sentient Lair: By making a massive and permanent TEP investment into a location, a character can awaken it, turning their stronghold into a sentient Lair.

The Lair's Sheet: A Lair has its own character sheet, with a TEP, an ERR, and its own initiative in combat.

Lair Actions: On its turn, the Lair can use its ERR to power effects: grasping vines, shifting walls, sudden darkness, etc.

The Final Bastion: The owner of a Lair can, as an action, draw upon the Lair's permanently invested TEP to fuel their own abilities. This makes a villain in their lair a truly formidable foe, as an intruder must fight both the master and their entire domain at once.

---

## TLE-005_feats_&_mastery.md

---
#───────────── The Lost Eternal ──────────────────────
id:        TLE-005
title:     Feats & The Arc of Progression
version:   1.0-draft
parents:   [TLE-009]
children:  [All future TLE modules related to specific character abilities and feats]
engrams:
 - system:feat-progression
 - mechanic:ability-customization
 - concept:entropic-investment
keywords:  [feats, progression, abilities, character customization, advancement, TLE]
uncertainty_tag: Low
module_type: core-mechanic-expansion
---
## §1 · Preamble: The Shape of Mastery
As an entity's power grows, their will begins to crystalize into specific, repeatable expressions of mastery. These are Feats: unique abilities and passive enhancements that represent a deep, focused investment of entropy. This module provides the framework for this arc of progression, allowing characters to purchase bundled features that define their unique style of interacting with the world.

## §2 · Acquiring Feats
Feats are not granted at specific levels; they are purchased. An entity can choose to permanently invest a portion of their Total Entropy Pool (TEP) to acquire a new Feat. This represents a conscious decision to specialize in a particular area of expertise. The EP cost of each Feat is fixed.

## §3 · The Feat Menu
The following is a list of common Feats available for purchase. GMs are encouraged to create their own to suit their campaign and reward players for unique accomplishments.

## Movement Feats
- Entropic Stride

Cost: 10 EP

Effect: When you spend EP on a specialized movement action (running, flying, burrowing), you may roll 1d2 for each EP spent. You take the higher of the two results as the amount of EP applied to the movement. (e.g., spend 5 EP, roll 5d2, results are 1,2,1,2,2 - you apply 8 EP worth of movement, gaining 20 feet instead of 12.5).

- Kinetic Transfer

Cost: 8 EP

Effect: When you successfully push an opponent into a solid surface (like a wall), you may add the EP cost of your movement this turn to the damage of the attack.

- Impact Absorption

Cost: 6 EP

Prerequisite: Must possess a form of flight.

Effect: When flying, you may intentionally strike the ground. You negate all fall damage from a height up to three times your base movement speed.

- Earth Glide

Cost: 8 EP

Prerequisite: Must possess a form of burrowing.

Effect: You can burrow through solid stone at half your normal burrowing speed.

## Combat & Arcane Feats
- Reckless Strike

Cost: 10 EP

Effect: Before you make an attack roll, you can choose to take a -4 penalty to the accuracy check. If the attack hits, you may add 8 to the entropic force of the attack before the target makes their defensive roll.

- Far Caster's Gambit

Cost: 8 EP

Effect: When using the Spell Sniper's Gambit (TLE-003) to increase a spell's range, you may roll 1d2 for each EP spent on the variable portion of the range. You take the higher of the two results, multiply it by 5 feet, and add it to the spell's total range.

- Mender's Respite

Cost: 12 EP

Effect: When using healing magic on yourself, you may restore a number of Hit Points up to your Wisdom modifier each round without spending any Entropy Points.

## Entropic Fusion Feats
These feats allow a character to combine and synergize their various pools of invested Entropy.

- Feat: Entropic Font

Cost: 10 EP (Permanent TEP Sacrifice)

Effect: You have learned to treat your will as a single, unified source. You can treat all of your Arcane Skill entropy pools as a single, combined resource for the purposes of casting spells or using abilities. You must still express that through one skill at a time unless otherwise feated or stated by an item or ability.

- Feat: Arcane Synthesis

Cost: 12 EP (Permanent TEP Sacrifice)

Prerequisite: At least two Arcane Skill pools.

Effect: Choose two of your Arcane Skill pools (e.g., "Expression of Frost" and "Pyromancy"). You have learned to weave their energies together. You can now spend EP from either pool to create a combined "synthesis" effect. A "Frostfire" bolt, for example, might deal cold damage while also inflicting a burning status effect. The exact nature of the synthesis is determined by you and the GM.

- Feat: Soul-Clad Weapon

Cost: 8 EP (Permanent TEP Sacrifice)

Effect: You have learned to channel your will through a chosen weapon. You may now spend EP from an Arcane Skill pool to add an equal amount of bonus damage of that skill's type to your next weapon attack.

## Kinetic Weaving Feats
These feats allow a character to imbue their physical actions, particularly movement, with entropic power.

- Feat: Elemental Wake

Cost: 8 EP (Permanent TEP Sacrifice)

Prerequisite: An Arcane Skill pool with an elemental descriptor (e.g., Frost, Fire, Lightning).

Effect: When you take the Move action, you can spend EP from a relevant elemental Arcane Skill pool. For every 2 EP spent, you leave a 5-foot square trail of that element in one of the squares you exit. This trail lasts for one round. An ice trail creates difficult terrain, a fire trail deals minor damage to anyone who enters it, etc.

- Feat: Shadow Step

Cost: 10 EP (Permanent TEP Sacrifice)

Prerequisite: A "Subterfuge" Skill pool.

Effect: When you are in dim light or darkness, you can spend EP from your Subterfuge pool as a bonus action to teleport to another unoccupied space you can see that is also in dim light or darkness. The distance you can teleport is 5 feet for every 1 EP spent.

- Feat: Juggernaut's Momentum

Cost: 10 EP (Permanent TEP Sacrifice)

Effect: When you take the Move action and move at least 15 feet in a straight line towards an enemy, you can spend Size Entropy from your Legs to add an equal amount of bonus damage to your first melee attack against that enemy before the end of your turn.

## Form & Essence Feats
These are advanced, high-cost feats that allow a character to manipulate the very fabric of being.

- Feat: Flesh Sculptor

Cost: 15 EP (Permanent TEP Sacrifice)

Effect: You have learned the rudimentary principles of shaping the entropic form. You gain the "Flesh Sculpting" Arcane Skill. You can spend EP from this pool to make cosmetic changes to a willing creature or yourself (changing hair color, eye color, minor features). More advanced uses, such as creating temporary gills or claws, require a high EP cost and a difficult Intelligence check. This is a profound and often unsettling art.

- Feat: Entropic Siphon

Cost: 20 EP (Permanent TEP Sacrifice)

Prerequisite: CON Score of 15 or higher.

Effect: You have attuned yourself to the chaotic flow of Entropy in the world, but this connection is dangerous. Once per long rest, as an action, you can attempt to draw raw Entropy from your environment. Make a CON check against a Target Number of 20.

Success: You regain EP equal to your CON modifier.

Failure: You take psychic damage equal to your CON modifier and create a random "Spasm" or "Fracture" in your current location as the chaotic energy lashes out.

## Entropic Conversion Feats
These feats allow a character to transform one resource into another. This conversion is always inefficient—the "tax" for breaking the natural flow of Entropy—making it a strategic choice rather than a standard action.

- Feat: Kinetic Conversion

Cost: 10 EP (Permanent TEP Sacrifice)

Effect: As a bonus action on your turn, you can sacrifice your potential for movement to fuel your will. You can reduce your movement speed for the turn in 10-foot increments. For every 10 feet of movement sacrificed, you regain 1 EP to a skill or attribute pool of your choice.

- Feat: Arcane Velocity

Cost: 10 EP (Permanent TEP Sacrifice)

Prerequisite: At least one Arcane Skill pool.

Effect: As a bonus action on your turn, you can burn your magical reserves to fuel a burst of speed. You can spend EP from any Arcane Skill pool. For every 2 EP spent, you increase your movement speed by 10 feet for the current turn.

- Feat: Vital Sacrifice

Cost: 12 EP (Permanent TEP Sacrifice)

Effect: As an action, you can harm your own physical form to fuel your power. You can choose to take irreducible damage to your HP. For every 2 points of damage you take, you may allocate 1 EP to any skill or attribute pool.

- Feat: Will to Power

Cost: 12 EP (Permanent TEP Sacrifice)

Effect: As a bonus action, you can convert your raw will into temporary physical might. You can spend EP from any attribute pool (STR, DEX, CON, INT, WIS). For every 2 EP spent, you can add 1 EP to the Size Entropy of one of your limbs. This bonus Size Entropy lasts until the end of your next turn.

## Combat & Targeting Feats
These feats alter the fundamental minigames of combat, allowing for advanced offensive and defensive maneuvers.

- Feat: Reactive Evasion

Cost: 12 EP (Permanent TEP Sacrifice)

Effect: You have the "final word" in your own defense. When an enemy makes an attack roll against you, after they roll but before the outcome is determined, you can use your reaction to spend EP from your Dexterity attribute pool. For every 3 EP you spend, you may subtract 1 from the enemy's attack roll.

- Feat: Precision Strike

Cost: 15 EP (Permanent TEP Sacrifice)

Effect: Your accuracy can be converted into raw power. When you make an attack roll and the result is higher than the Target Number (TN), you can choose to add the difference to the attack's damage as bonus EP. This bonus cannot exceed +5 EP.

## Perception & Environment Feats
These feats govern how a character perceives and interacts with the world around them, particularly with varying levels of light.

- Feat: Gloom-Sight

Cost: 8 EP (Permanent TEP Sacrifice)

Effect: Your senses are adapted to the dark. You can perceive two tiers of light lower than normal. For you, "Dim Light" is perceived as "Normal Light," and "Vague Shapes" are perceived as "Dim Light." You cannot perceive anything in "Total Darkness."

- Feat: Resonant Senses

Cost: 15 EP (Permanent TEP Sacrifice)

Prerequisite: WIS Score of 10 or higher.

Effect: You have developed a form of blindsight by sensing the entropic resonance of objects and beings. You can automatically perceive the location of any creature or object with an Entropy Pool within 30 feet, regardless of light levels or physical obstructions. This does not allow you to see fine details, only their shape and location.

- Feat: Umbral Affinity

Cost: 10 EP (Permanent TEP Sacrifice)

Effect: You draw power from the shadows. At the start of your turn, if you are in Dim Light or Darkness, you regain 2 EP to a pool of your choice.

- Feat: Solar Attunement

Cost: 10 EP (Permanent TEP Sacrifice)

Effect: You are energized by the sun's power. At the start of your turn, if you are in Full Light or Bright Light, you regain 2 EP to a pool of your choice.

## Disciplines
These feats represent dedicated practice and mastery over a specific, non-innate discipline, from a craftsman's trade to a cleric's rites.

- Feat: Professional Aptitude

Cost: 8 EP (Permanent TEP Sacrifice)

Effect: Choose a specific non-combat profession (e.g., Blacksmithing, Alchemy, Cartography). You have dedicated yourself to its mastery. You gain a "Professional" skill pool with 5 EP invested in it. You can spend EP from this pool to gain advantage on checks related to this profession or to recall crucial information about it.

- Feat: Silver Tongue

Cost: 8 EP (Permanent TEP Sacrifice)

Effect: Choose a specific area of performance or social grace (e.g., a musical instrument, a specific card game, a language, etiquette). You have mastered it. You gain a "Performance" skill pool with 5 EP invested in it. You can spend EP from this pool to influence others, create a masterful work of art, or cheat at a game of cards.

- Feat: Ritualist

Cost: 10 EP (Permanent TEP Sacrifice)

Prerequisite: WIS Score of 5 or higher.

Effect: You have been trained in the art of ritual magic or prayer. You gain the "Ritual" Arcane Skill. You can spend EP from this pool to perform long, complex magical effects outside of combat, such as blessing or corrupting a location, consecrating ground, or scrying on a distant target. The cost and time required are determined by the GM.

- Feat: Cleric Training

Cost: 12 EP (Permanent TEP Sacrifice)

Prerequisite: Must possess a holy symbol or divine focus.

Effect: Through devotion and training, you can channel a small measure of divine power. Your holy symbol gains a dedicated pool of 3 EP. As an action, you can spend this EP to heal a creature you touch, restoring HP on a 1-for-1 basis. This pool recharges all 3 EP after two full rounds of not being used.

## Social & Conversational Feats
This suite of feats makes social encounters as tactical and engaging as physical combat, allowing for a variety of approaches to conversation.

- Feat: Orator's Gambit

Cost: 10 EP (Permanent TEP Sacrifice)

Effect: You can apply the principles of entropic investment to social contests. When you attempt to persuade, deceive, or intimidate a target, you may declare you are using this feat. You secretly invest a chosen amount of EP from your Wisdom or Intelligence pool. The target then makes a contested Wisdom check. If their roll is lower than your invested EP, you succeed. This allows for high-stakes social maneuvering.

- Feat: Arcane Influence

Cost: 12 EP (Permanent TEP Sacrifice)

Prerequisite: At least one Arcane Skill pool.

Effect: You can subtly weave your magic into your words and presence. You may spend EP from an Arcane Skill pool instead of an attribute pool when using the Orator's Gambit feat. This may manifest as a charming illusion, a subtle telepathic nudge, or a faint aura of fear, depending on the nature of your magic.

- Feat: Empathic Reader

Cost: 8 EP (Permanent TEP Sacrifice)

Prerequisite: WIS Score of 8 or higher.

Effect: As an action, you can focus on a creature you can see and make a contested Wisdom check against them. On a success, you gain a brief, intuitive insight into their current emotional state and surface-level intentions (e.g., "they are angry and looking for a fight," or "they are hiding something").

- Feat: Disarming Presence

Cost: 8 EP (Permanent TEP Sacrifice)

Effect: Your natural demeanor is unassuming and non-threatening. When you first meet an NPC, their initial disposition towards you is improved by one step (e.g., from "Hostile" to "Unfriendly," or "Neutral" to "Friendly"), unless you have taken overtly hostile actions.

- Feat: Intimidating Visage

Cost: 8 EP (Permanent TEP Sacrifice)

Effect: Your physical presence is inherently menacing. You can choose to use your Strength or Constitution modifier instead of your Wisdom or Intelligence modifier when making checks to intimidate.

- Feat: Primal Manifestation

Cost: 15 EP (Permanent TEP Sacrifice)

Effect: You have learned to unravel and re-weave your own entropic form. As an action, you can transform into a beast or hybrid form you have designed using the creature creation rules. This transformation is governed by the following principles:

Form Investment: You must invest a certain amount of EP from your own TEP into the transformation. This is your Form Investment Pool (FIP). The FIP serves as the temporary Hit Points of your new form.

Form Potential: The maximum TEP of your new form, including its attributes and body parts, is equal to your FIP x 3.

Attribute Weaving: To create the powerful attributes of your new form, you may choose two of your own attributes to weave together. One becomes the Dominant Attribute, and the other the Supporting Attribute. The new form's combined attribute is calculated as: New Attribute EP = Dominant Attribute EP + floor(Supporting Attribute EP / 2).

Ending the Transformation: The transformation ends if your form's temporary HP (its FIP) is reduced to 0, if you choose to end it as a bonus action, or if the form's own TEP is somehow drained to 0. When you revert, you return to your previous HP total.

## Advanced Transformation Feats
These feats build upon the principles of Primal Manifestation, offering unique and specialized paths for those who wish to re-weave their own form.

- Feat: Feral Curse

Cost: This feat cannot be purchased. It is acquired as a curse or a dangerous pact.

Effect: Your form is unstable, bound to a powerful, primal entity. As an action, you can undergo a monstrous transformation. This transformation is governed by the following principles:

The Bargain: Choose two of your attributes. One is the Exalted Attribute, the other is the Sacrificed Attribute. For the duration of the transformation, the EP value of your Sacrificed Attribute becomes negative and is added to your Exalted Attribute. (Example: A character with STR 10 and INT 10 could sacrifice their INT, making it -10 EP, and add that to their STR, making it 20 EP).

The Beast Within: The transformed state has its own will. At the start of each of your turns, you must make a contested Wisdom check against the form's own will (the GM sets the TN, often based on the Pact's Hold or the curse's power). On a failure, the GM controls your actions for that turn as the beast acts on its own instincts.

Ending the Transformation: The transformation lasts for one hour, until you are knocked unconscious, or until the entity's goals are met.

- Feat: Thousand Forms Adept

Cost: 12 EP (Permanent TEP Sacrifice)

Effect: You are a master of minor transformations. You may design up to five different beast forms, none of which can have a total Entropy Budget greater than 20 EP.

Rapid Change: You can transform into one of your chosen forms as a bonus action. This transformation does not grant temporary HP or use the attribute weaving rules. You simply adopt the physical form and statistics of the creature, using its TEP and attributes instead of your own. Your own TEP and attributes are suppressed for the duration.

- Feat: Skin Dancer

Cost: 15 EP (Permanent TEP Sacrifice)

Effect: You are a master of mimicry. You gain the "Mimicry" Arcane Skill.

The Mask: After observing a humanoid creature for at least one minute, you can spend an action to transform into a perfect physical replica of them. This is a non-magical, physical change.

The Performance: You can spend EP from your "Mimicry" pool to perfect the illusion. Investing EP allows you to replicate the target's voice, mannerisms, and surface thoughts, with the GM setting an EP cost for the level of detail you wish to achieve. This feat does not grant you the target's memories, skills, or entropic abilities.

## Archetypal Feats
These feats grant access to the iconic abilities of classic archetypes, allowing any character to walk the path of a Barbarian, Monk, Sorcerer, or Necromancer.

## The Path of Rage
- Feat: Primal Rage

Cost: 12 EP (Permanent TEP Sacrifice)

Effect: As a bonus action, you can enter a rage. While raging, you gain a temporary pool of "Rage EP" at the start of each of your turns equal to the sum of all your attribute modifiers (except Wisdom). This EP can be spent on any action but vanishes at the end of your turn. The rage lasts for a number of rounds equal to your ERR. It ends early if you are knocked unconscious, or if you end your turn without having attacked a hostile creature or taken damage since your last turn.

- Feat: Stalwart Defense

Cost: 10 EP (Permanent TEP Sacrifice)

Effect: As a reaction when you take damage, you can enter a defensive stance until the start of your next turn. For every 5 points of incoming damage, you may spend 1 EP from your Constitution pool to roll a d2; on a result of 2, you ignore that 5 points of damage.

## The Path of Focus
- Feat: Patient Defense

Cost: 8 EP (Permanent TEP Sacrifice)

Effect: At the start of your turn, you can declare you are using this feat. You may set aside a number of EP up to the sum of your DEX and WIS modifiers from their respective pools. The first time you are hit with an attack before your next turn, this set-aside EP is doubled and subtracted from the attack's damage.

- Feat: Superior Strike

Cost: 8 EP (Permanent TEP Sacrifice)

Effect: A number of times per long rest equal to your CON modifier, you may add your DEX modifier as bonus EP to an unarmed strike's damage.

- Feat: Dim Mak

Cost: 20 EP (Permanent TEP Sacrifice)

Prerequisite: WIS Score of 15 or higher.

Effect: When you successfully damage an opponent with an unarmed strike, you can use this ancient and forbidden technique. Make an attack roll with a TN of 20. On a success, you mark the target with a touch of death. At the start of each of their turns, the target must roll 1d100. If the result is a number you secretly chose when you applied the mark, the target dies instantly. This is a profound and often evil act with significant narrative consequences.

## The Path of Sorcery

- Feat: Metamagic Adept

Cost: 15 EP (Permanent TEP Sacrifice)

Effect: You have learned to break the fundamental rules of spellcasting. You gain access to the following abilities:

Empower Spell: When you cast a spell that deals damage, you can spend an additional 2 EP to empower it. If you do, the target's ERR is reduced by the damage dealt for one round.

Quicken Spell: You can spend an additional 5 EP to change a spell's casting time from 1 action to 1 bonus action.

Twin Spell: When you cast a spell, you can spend an additional 10 EP to make that spell's point of impact the origin point for a second, identical spell cast on the same turn.

## The Path of Necromancy
- Feat: Primary Thrall

Cost: 15 EP (Permanent TEP Sacrifice)

Effect: You have learned the dark art of direct entropic infusion. You can target a corpse and begin to pour your own TEP into it. You must invest EP into its negative attributes to make them positive. This undead creature is sustained only by your will; at the start of each of your turns, you must spend at least 1 EP from your own TEP to maintain its animation. It does not impose an ERR cost, but it collapses into dust if you fail to sustain it.

- Feat: Ritual of Animation

Cost: 12 EP (Permanent TEP Sacrifice)

Effect: You can perform a 10-minute ritual to animate a corpse as a lesser undead thrall. You must then immediately engage it in a Tamer's Conversation to assert your will. If successful, you can form a Soul Bond with it, paying its full Entropy Budget from your TEP and the subsequent ERR cost to maintain it as a permanent minion.

## Kinetic & Synergistic Feats
This school of abilities focuses on the manipulation of kinetic force and the interaction of different entropic energies.

- Feat: Kinetic Weaving

Cost: 10 EP (Permanent TEP Sacrifice)

Effect: You gain the "Kinesis" Arcane Skill and a pool of 5 EP. This skill is the foundation for manipulating physical force.

- Feat: Telekinetic Shove (Push)

Cost: 8 EP (Permanent TEP Sacrifice)

Prerequisite: "Kinesis" Arcane Skill.

Effect: As an action, you can spend EP from your Kinesis pool to unleash a wave of telekinetic force. Target a creature or object within 30 feet. The target must make a contested Strength check against your EP investment. If they fail, you can push them 5 feet for every 1 EP you spent.

- Feat: Entropic Grasp (Pull)

Cost: 8 EP (Permanent TEP Sacrifice)

Prerequisite: "Kinesis" Arcane Skill.

Effect: As an action, you can spend EP from your Kinesis pool to create a tether of force. Target a creature or object within 30 feet. The target must make a contested Strength check against your EP investment. If they fail, you can pull them 5 feet closer to you for every 1 EP you spent.

- Feat: Synergistic Casting

Cost: 15 EP (Permanent TEP Sacrifice)

Prerequisite: At least two elemental Arcane Skills (e.g., Fire, Ice, Water, Earth).

Effect: You have mastered the art of elemental interaction. When two different, interacting elemental effects created by you or your allies occupy the same space or target the same creature in the same round, you can use your reaction to spend 3 EP and create a tertiary synergistic effect.

Examples: Fire + Water = Obscuring Steam Cloud; Earth + Wind = Blinding Dust Devil; Fire + Ice = Shattering Thermal Shock (makes target vulnerable to physical damage for one round).

## Spell Modification Feats
This suite of feats allows a caster to alter the fundamental properties of their spells, adding layers of tactical depth and surprise.

Feat: Veiled Casting

Cost: 12 EP (Permanent TEP Sacrifice)

Effect: You can weave illusions into your magic to conceal its true nature. When you cast a spell, you can spend additional EP to make it invisible. For every 1 EP you spend on the spell's core effect (damage, range, etc.), you must spend an additional 1 EP to make that component invisible. To disguise secondary sensory effects (heat, cold, sound), you must spend another 1 EP.

- Feat: Concussive Force

Cost: 8 EP (Permanent TEP Sacrifice)

Effect: When you cast a spell that deals damage, you can spend an additional 3 EP to add a kinetic rider. The target is pushed 5 feet directly away from the spell's point of origin.

- Feat: Ricochet Cast

Cost: 8 EP (Permanent TEP Sacrifice)

Effect: When you cast a spell that creates a projectile, you can spend an additional 1 EP to have it bounce off one surface, changing its trajectory up to 90 degrees. This can be done multiple times, but isn't a perfect shot, meaning it reflects uncontrollably after one ricochet. This can be fun for filling rooms with spell chaos.

- Feat: Spell Animator

Cost: 15 EP (Permanent TEP Sacrifice)

Effect: You gain the "Spell Animation" Arcane Skill. When you cast a spell, you can spend additional EP from this skill pool to give the spell a rudimentary, temporary consciousness.

Burrow (1 EP per 5 feet): The spell can travel through solid, non-magical material of up to 1-foot thickness.

Animate (1 EP per EP of the core spell): The spell manifests as a tiny, mobile construct (a fiery imp, an icy serpent). It can move on its own turn and intelligently seek its target, navigating around obstacles. It still requires an attack roll to hit when it reaches its target.

---

## TLE-006_wound_channels_residue_and_altruism.md

---
#───────────── The Lost Eternal ──────────────────────
id:        TLE-006
title:     Advanced Mechanics, Resonance, Wounds, Residue, and Altruism
version:   1.0-ratified
parents:   [TLE-001]
children:  []
engrams:
 - system:advanced-mechanics
 - mechanic:environmental-resonance
 - concept:narrative-injury
 - system:world-consequence-engine
keywords:  [resonance, wound channel, residue, altruism, advanced rules, TLE]
uncertainty_tag: Low
module_type: core-mechanic-expansion
---
## §1 · Preamble: The Echo of Action
The core rules define what an entity can do. This module defines what their actions truly mean. Every expression of will, from a whispered word to a cataclysmic spell, leaves an echo in the world. This module provides the advanced mechanics for that echo, transforming the game from a series of actions into a story of consequences. These rules govern how the environment resonates with a character's choices, how trauma becomes a part of their story, and how the very fabric of the world is shaped by the struggle between coherence and chaos.

## §2 · The Resonant Action & Dissonance Rule
Actions do not happen in a vacuum; they resonate with the environment. A skilled entity can learn to "read the room" and attune their will to the prevailing resonant state, achieving incredible efficiency.

The Mechanic: At the start of a scene, the GM declares its Resonant State (e.g., "Chaotic," "Orderly," "Fearful," "Sacred"). A player who wishes to act in harmony with this state can use an action to make a Perception (WIS) or Arcana (INT) check against a DC set by the GM (typically DC 12 for standard environments).

Resonance (On a successful check): If the character's subsequent action is aligned with the Resonant State (e.g., a chaotic spell in a "Chaotic" environment), they gain a Coherence Bonus. They may reroll any 1s on their damage or effect dice for that action, taking the new result. This represents a perfect, low-resistance expression of will.

Dissonance: If a character's action is diametrically opposed to the state (e.g., an orderly, lawful spell in a "Chaotic" environment), they suffer a Dissonance Cost. The EP cost of the action increases by 25% (rounded up). This represents the struggle of forcing one's will against the current.

## §3 · The Wound Channel Mechanic
A powerful blow or a traumatic event is more than a loss of Hit Points; it is a scar upon the soul. This rule makes Wound Channels a tangible, narrative mechanic.

The Mechanic: When an entity takes a Critical Hit or is reduced to 0 HP, they gain a Wound Channel. The player and GM collaboratively name it based on the event (e.g., "Shattered Confidence," "Scorched Arm," "Echo of Betrayal"). A Wound Channel is a persistent condition with two effects:

A Vulnerability: A specific, narrative trigger that can be exploited by the GM or other players. For example, a character with "Shattered Confidence" might be forced to make a Wisdom saving throw when taunted, or act with disadvantage.

An Insight: A specific, narrative situation where the memory of the wound provides an advantage. The character with the "Scorched Arm" might gain a bonus to resist fire damage, because they have a deep, physical understanding of that pain.

Healing a Wound Channel requires specific downtime actions, quests, or rituals, turning recovery into a genuine character arc.

## §4 · The Residue & Coherence Scale
The world remembers. Every significant action shifts the balance between order and chaos. This rule creates a world-level resource pool that the players and GM influence together.

The Residue Pool (The World's Stress): The GM keeps a hidden pool of Residue Points. Every time the players use powerful magic, defeat a major foe, or fundamentally alter an environment (triggering Entropic Corruption from TLE-009), the GM adds a d4 (or more for massive events) to the pool. The GM can spend points from this pool to create Residue Events: pockets of wild magic, the appearance of "entropic spirits," or unexpected environmental complications.

The Coherence Dividend Pool (The Party's Hope): As described in §5, the party gains a shared pool of EP when they perform altruistic acts. This pool represents the hope and coherence they are putting into the world.

The Balancing Act: This is where the two pools connect. The players can choose to spend points from their Coherence Dividend Pool not on themselves, but to reduce the GM's Residue Pool on a 1-to-1 basis. This is a direct, active choice to "heal the world's stress," making altruism a vital tool for preventing long-term chaos. A GM might even telegraph the danger: "The air crackles with chaotic energy; you can feel the Residue in this place is dangerously high."

## §5 · The Altruism Trigger
This rule provides the direct, in-game reward for acting in accordance with the Prime Directive.

The Mechanic: When a player performs an action that the table agrees should be tagged as [Altruistic] in the Entropy Ledger (TLE-000), the entire party is immediately rewarded. They are "filled with visions of when they saved little Timmy from the well," and gain a temporary, shared pool of EP called the Coherence Dividend.

Pool Size: The Coherence Dividend pool contains a number of EP equal to the altruistic character's Constitution Modifier.

Usage: Any member of the party can draw from this shared pool on their turn to fuel any action. The pool must be used before the start of the altruistic character's next turn, or the unused points dissipate.

The Link to Residue: This dividend is the party's primary weapon against the rising tide of world-level Residue, creating a profound mechanical and narrative link between personal kindness and cosmic stability.

## §6 · Assemblé
A hero's journey is measured not only by the monsters they slay, but by the echoes they leave behind. These rules define the nature of that echo. They ensure that every choice has weight, that trauma can be reforged into strength, and that the quietest act of kindness can resonate with enough force to hold back the darkness, if only for a moment. This is the art of conflict, and the physics of hope.

---

## TLE-007_the_arc_of_progression_and_the_echo_of_experience.md

---
#───────────── The Lost Eternal ──────────────────────
id:        TLE-007
title:     The Arc of Progression & The Echo of Experience
version:   1.0-ratified
parents:   [TLE-001]
children:  [TLE-008]
engrams:
 - system:character-progression
 - mechanic:experience-as-a-resource
 - concept:entropic-harvesting
 - system:soft-cap-mechanics
keywords:  [progression, experience, leveling, entropy farming, soft cap, TLE]
uncertainty_tag: Low
module_type: core-mechanic-framework
---
## §1 · Preamble: The Echo of Becoming
Growth is the echo of experience, imprinted upon the soul. In the world of The Lost Eternal, an entity does not advance through arbitrary levels, but by gathering the resonant echoes of their deeds and deliberately weaving that power into the fabric of their being. This module specifies the mechanics for this arc of progression. It defines how a character's core potential grows, how power can be harvested from the world, and the ultimate limits of a mortal form to contain an immortal will.

## §2 · The Echo of Experience
The primary path to greater power is through adventure. Overcoming significant challenges leaves a psychic and entropic residue—a memory of the trial—that can be integrated to forge a stronger self.

Gaining Resonant Echoes: Characters are awarded Resonant Echoes by the GM for overcoming significant challenges. This is the system's equivalent of experience points. Echoes should be awarded for:

Winning a major battle or surviving a dangerous encounter.

Solving a complex puzzle or mystery.

Achieving a significant social or political victory.

Discovering a new, important location or piece of lore.

The Crystallization Ritual: Resonant Echoes are potential, not power. To make them manifest, a character must perform a Crystallization Ritual during a period of downtime (such as a long rest). Through this act of focused will, the character can spend their accumulated Echoes to permanently increase their maximum Total Entropy Pool (TEP).

## §3 · Channels of Power: Gaining Supplemental Entropy
While Echoes are the only way to increase a character's maximum potential, there are other ways to replenish or gain temporary power. This makes "entropy farming" a viable, but less efficient, strategy compared to seeking new challenges.

Entropic Harvesting (From Combat): A character can harvest the lingering entropic signature from a defeated foe. This grants them an immediate infusion of EP that replenishes their current pool but does not increase their maximum TEP. The GM may choose one of the following methods:

The Essence Method: The victor gains EP equal to 1/8th of the defeated enemy's CON Score (rounded down).

The Remnant Method: The victor gains EP equal to 1% of the defeated enemy's TEP (rounded down).

Crystallized Entropy (From Treasure): Finding Entropy Shards or enchanted items provides a potent source of EP. However, a physical form can only integrate so much external power at once.

The Transmutation Limit: An entity can only absorb a total number of EP from items or infusions per day equal to their Entropy Regeneration Rate (ERR). This makes absorbing a powerful artifact a slow, deliberate process, preventing sudden, unearned spikes in power.

## §4 · The Law of Coherence Strain (The Soft Cap)
An entity is a coherent, resonant structure. While their potential is theoretically infinite, their physical form can only contain so much power before the strain of maintaining coherence becomes immense.

The Coherence Threshold (CT): This is the maximum TEP an entity can comfortably contain. It is a direct function of their physical and spiritual resilience.
Coherence Threshold (CT) = Constitution Score x 10

The Cost of Power: The cost in Resonant Echoes to increase one's maximum TEP is determined by their current position relative to their Coherence Threshold.

Below the Threshold: While a character's maximum TEP is at or below their CT, the cost is 1 Resonant Echo per 1 point of TEP increase. This is the standard arc of progression.

Above the Threshold: To exceed one's natural limits requires exponentially more focus and will. For every point of TEP a character wishes to add above their CT, the cost in Echoes increases. The cost becomes:
Cost per TEP = 1 + floor( (Current Max TEP - Coherence Threshold) / 10 )

Example: A legendary warrior has a CON Score of 30, giving her a Coherence Threshold of 300.

To increase her TEP from 299 to 300 costs 1 Echo.

To increase her TEP from 300 to 301 costs 1 + floor((300-300)/10) = 1 Echo.

However, to increase her TEP from 310 to 311, the cost is now 1 + floor((310-300)/10) = 1 + 1 = 2 Echoes.

To increase her TEP from 400 to 401 would cost 1 + floor((400-300)/10) = 1 + 10 = 11 Echoes.

This mechanic creates a natural, lore-consistent "soft cap." A character can become limitlessly powerful, but doing so requires an immense investment, making high Constitution and the deliberate pursuit of meaningful challenges (which grant large sums of Echoes) essential for endgame play.

## §5 · Assemblé
Growth is the art of turning memory into muscle, and insight into integrity. The Echo of Experience is the currency of this art, spent to deepen the soul's reservoir of power. But every form has its limits. The Law of Coherence Strain teaches the ultimate lesson: true power is not the endless accumulation of energy, but the wisdom to build a vessel strong enough to contain it. The arc of progression is a spiral, not a line, forever circling back to the strength of one's own foundation.

---

## TLE-008_the_architect_of_worlds_a_GM-guide.md

---
#───────────── The Lost Eternal ──────────────────────
id:        TLE-008
title:     The Architect of Worlds (The GM's Guide)
version:   1.0-ratified
parents:   [TLE-007]
children:  [TLE-009]
engrams:
 - system:challenge-design
 - mechanic:entropic-budgeting
 - governance:gm-toolkit
 - concept:universal-challenge-rating
keywords:  [gm guide, challenge design, monsters, traps, hazards, social encounters, TLE]
uncertainty_tag: Low
module_type: core-rulebook-framework
---

## §1 · Preamble: The Same Clay
In the universe of The Lost Eternal, the Game Master is not a mere storyteller, but the primary architect of the resonant field in which the players exist. The world, its inhabitants, and its very dangers are sculpted from the same fundamental clay as the player characters: Entropy. This module provides the GM with the tools to be a fair and consistent architect, defining a universal system for challenge design. From the mightiest dragon to the subtlest negotiation, every obstacle is built from an Entropic Budget.

## §2 · The Universal Challenge: The Entropic Budget (EB)
Every challenge a player faces has a total entropic power level, its Entropic Budget. This is the GM's primary tool for scaling encounters and defining their difficulty.

Calculating the Budget: An encounter's EB is determined relative to the party's combined power. First, calculate the Party's Average TEP.
Party Average TEP = (Total TEP of all characters) / (Number of characters)

Encounter Difficulty:
| Difficulty | Entropic Budget (EB) | Description |
| :--- | :--- | :--- |
| Trivial | 0.5 x Party Average TEP | A minor obstacle, easily overcome. |
| Normal | 1.0 x Party Average TEP | An equal footing. A 50/50 slog where strategy is key. |
| Hard | 1.25 x Party Average TEP | A significant challenge requiring teamwork and resource management. |
| Very Hard | 1.5 x Party Average TEP | A boss-level encounter that will likely drain the party significantly. |
| Legendary | 2.0+ x Party Average TEP | A world-altering threat that may require extensive preparation to survive. |

For a group of opponents, the GM can either give each creature a smaller portion of the total EB or create one powerful leader and several weaker minions.

## §3 · Designing Creatures: Combat Encounters
A creature is a simplified character sheet, built in moments using its Entropic Budget.

The Process:

Assign an Entropic Budget (EB) based on the desired difficulty.

Allocate to Health Pool: A portion of the EB is invested in the creature's Torso to become its HP. This is its raw durability. (e.g., 50% for a standard creature, 75% for a brute).

Allocate to Attack Pools: The remaining EB is invested into one or more Attack Pools. These function exactly like a player's Size Entropy (TLE-002), fueling the creature's primary attacks (e.g., "Claw," "Bite," "Fire Breath").

Determine ERR: For simplicity, a creature's Entropy Regeneration Rate can be set to 10% of its total EB per round (rounded down).

Assign Actions: The number of actions a creature can take is determined by its nature (e.g., 1 for a simple beast, 2-3 for a legendary monster).

Example: A 60 EP Ogre (Hard encounter for a party with an average TEP of ~48)

Health Pool: 30 EP invested in its Torso (30 HP).

Attack Pool: 30 EP invested in a "Greatclub" arm. It can spend up to 30 EP for a single massive 1d30 damage swing.

ERR: 6 EP per round.

Actions: 1 per turn.

## §4 · Designing Hazards & Traps
An environmental hazard or mechanical trap is the simplest form of challenge: a single, non-regenerating pool of Entropy designed to be spent once.

Mechanic: The hazard's Entropic Budget is its total damage potential. When triggered, it unleashes its full EB as an "attack." Players in the area of effect must use Active Defense (TLE-005) to block the incoming entropic force. Once its budget is spent, the trap is inert.

Example: A 25 EP Fire Trap. When triggered, it attacks everyone in a 10-foot radius with 25 entropic force. A character must spend 25 EP on Active Defense to negate the damage entirely. The trap is now disarmed.

## §5 · Designing Social Challenges
A social encounter uses the exact same principles as a combat encounter, but the battlefield is the mind.

The Principle: "Conversation as Combat" (TLE-007) pits the players against an NPC's mental defenses. The GM uses the encounter's Entropic Budget to "buy" the NPC's mental attributes.

Mechanic:

Assign an Entropic Budget (EB) for the social challenge.

Invest in Mental Pools: The GM allocates this EB into the NPC's Intelligence and Wisdom. These EP pools determine the NPC's Resolve (INT Score) and Composure (WIS Score), which act as their "health pools" in the conversation.

The Remainder: Any leftover EB becomes the NPC's pool for making their own "statements" (social attacks) during the conversation.

This unified system allows a GM to design any challenge in the game—a monster, a trap, or a tough negotiation—using one simple, consistent, and scalable mechanic.

## §6 · Assemblé
The world is a tapestry of will, and the GM is its primary weaver. The Entropic Budget is the universal thread from which all challenges are woven. A monster's rage, a trap's deadly spring, and a merchant's stubborn haggle are all expressions of the same fundamental force. By mastering this single principle, the Architect can build a world that is not only challenging but coherent, consistent, and deeply resonant with the laws of reality itself.

---

## TLE-009_reputation_and_renown.md

---
#───────────── The Lost Eternal ──────────────────────
id:        TLE-009
title:     The Web of Factions & Reputation
version:   1.0-ratified
parents:   [TLE-008]
children:  [TLE-010]
engrams:
 - system:reputation-mechanics
 - concept:factional-resonance
 - mechanic:social-consequence
 - system:social-stealth
keywords:  [factions, reputation, social, resonance, prime directive, TLE]
uncertainty_tag: Low
module_type: core-rulebook-framework
---
## §1 · Preamble: The Resonant Society
An individual is a single note, but a society is a chord. Great powers—cities, guilds, clandestine orders—are living entities, held together by a shared will and a common resonance. Reputation in this world is not a measure of popularity; it is a physical measure of one's resonant alignment with these powerful social structures. This module provides the rules for navigating this web of factions, where every action sends a vibration that can earn an ally or create an enemy.

## §2 · The Faction Directive
Every significant social group, or Faction, is defined by its Faction Directive. This is a short, clear statement of the faction's core values, goals, and methods. It is the faction's soul, its own Prime Directive, and it is the standard against which all actions are measured.

GM's Tool: The Faction Directive is the GM's primary tool for roleplaying a faction consistently. It is the lens through which the faction sees the world.

Example Faction Directives:

The Archivist's Guild: "Knowledge must be preserved and protected from chaos, at any cost."

The Gilded Hand (Merchant's Guild): "Coherence is capital. A deal is a sacred text. Profit is the measure of a sound will."

The Order of the Unbroken Wall (Knights): "We are the shield. We hold the line. We protect the weak from the coming storm."

The Whisper-Thieves: "Secrets are the only true currency. Every lock has a key, and we are the locksmiths."

## §3 · The Resonance Score (Tracking Reputation)
A character's standing with a faction is measured by their Resonance Score. This is a simple integer scale that tracks their alignment with the faction's Directive.

The Scale:

+8 to +10: Idolized

+4 to +7: Respected

+1 to +3: Friendly

0: Neutral

-1 to -3: Unfriendly

-4 to -7: Distrusted

-8 to -10: Hated

Shifting Resonance: The score is dynamic and changes based on a character's actions.

Resonant Actions: When a character's actions directly support or embody a faction's Directive, their score with that faction increases by 1 (or more for truly legendary acts).

Dissonant Actions: When a character's actions directly undermine or oppose a faction's Directive, their score decreases by 1 (or more for grave betrayals).

## §4 · The Consequences of Reputation
A character's Resonance Score has direct, tangible effects on their interactions with a faction's members and its resources.

| Score Range	| Social & Economic Effects |
| +8 to +10 (Idolized) | Faction members offer aid freely, provide shelter, may give significant discounts or gifts. May grant access to unique quests, titles, or secrets. |
| +4 to +7 (Respected) | Favorable treatment, access to restricted goods or areas, minor discounts are common.
| 0 (Neutral)	Standard interactions. Business is business. No special treatment. |
| -4 to -7 (Distrusted) | Refusal of service is likely. Members are suspicious, may report the character's activities to authorities. |
| -8 to -10 (Hated) | Actively hostile. Faction members may attack on sight. Bounties may be posted for the character's capture or demise. |


## §5 · Abstracting the Web: Intermediaries & Social Stealth
Reputation is a personal, resonant signature. A clever operator knows that if their own signature is dissonant, they can use another that is resonant. This is where your skeevy rogue shines.

The Mechanic: Using an Intermediary Faction
A character can leverage their positive Resonance Score with one faction to bypass their negative score with another.

The Process: The character wishing to act through an intermediary (e.g., a rogue using the Whisper-Thieves to get information from the City Guard they are Hated by) must find a willing contact within the intermediary faction.

The Check: The player makes a social skill check (e.g., Persuasion, Deception, Intimidation). The DC is set by the GM and is based on the hostility of the target faction and the influence of the intermediary faction. Getting the Thieves' Guild to bribe a corrupt guard is easy (low DC). Getting them to assassinate the captain of the guard is nearly impossible (very high DC).

Success: The intermediary acts on the player's behalf. The player gets what they need, and their personal Resonance Score with the target faction is unaffected. The cost is usually a favor or a large sum of EP paid to the intermediary.

Failure: The attempt is exposed. The character's Resonance Score with the target faction drops further. Worse, their score with the intermediary faction may also drop for having brought such risky business to their door.

## §6 · Assemblé
A reputation is the echo of your will, resonating through the web of society. Every choice, every act of kindness or cruelty, sends a vibration that travels the strands, changing how the world perceives your song. A wise adventurer knows that power is not just the strength of their arm, but the number of allies who will sing with them in the dark. A cunning rogue knows that if their own song is out of tune, they can always pay another to sing on their behalf.

---

## TLE-010_the_art_of_creation.md

---
#───────────── The Lost Eternal ──────────────────────
id:        TLE-010
title:     Metaphysical Engineering & The Art of Creation
version:   1.0-ratified
parents:   [TLE-009]
children:  []
engrams:
 - system:endgame-play
 - mechanic:reality-crafting
 - concept:metaphysical-engineering
 - governance:player-authored-rules
keywords:  [endgame, high-level, crafting, world-building, rule design, TLE]
uncertainty_tag: Low
module_type: core-rulebook-framework
---
## §1 · Preamble: The Creator's Spark
An entity that has mastered the flow of Entropy, navigated the web of factions, and survived the crucible of adventure eventually reaches a final frontier. Their challenges are no longer about defeating a single foe or acquiring a single treasure, but about shaping the fabric of reality itself. This is the art of Metaphysical Engineering: the ultimate expression of will, where a character transitions from being a participant in the world to being a co-creator of its future. This module provides the rules for this endgame play, where the greatest reward is not what you can find, but what you can build.

## §2 · The Principle of Metaphysical Engineering
Metaphysical Engineering is the act of creating new, persistent resonant structures in the world. These creations are, in game terms, new rules, new creatures, new artifacts, or even new laws of magic. This is not a simple crafting check; it is a profound and costly act of will.

The Entropy Sink: To create something permanent, a character must permanently invest a part of their own being. This is the ultimate resource sink for high-level characters. The Entropy Points (EP) spent on creation are permanently sacrificed from the character's maximum Total Entropy Pool (TEP). This act is a final, irreversible investment of one's own soul into the world.

## §3 · The Art of Creation: The Three-Step Process
Creating a new piece of reality is a three-stage process, involving a test of intellect, a sacrifice of power, and a contest with the universe's existing harmony.

### 3.1 · Step 1: The Concept (The Blueprint)
Before a thing can be made, it must be understood. The player must first create a "module" for their creation, defining its nature, its function, and how it interacts with Entropy. This requires an incredibly difficult Intelligence check (typically DC 30 or higher) to create a blueprint that is coherent enough to be manifested.

### 3.2 · Step 2: The Entropic Investment (The Cost)
The cost to bring a new concept into the world is monumental, representing the immense energy required to establish a new, stable pattern in the universe. The sacrificed EP is permanently removed from the creator's maximum TEP.

Creation Type	Permanent TEP Sacrifice Cost
A new, unique Skill	50 EP
A new, unique Feat	100 EP
A unique Enchanted Item	The item's desired TEP x 5
A new type of Creature	The creature's Entropic Budget (EB) x 10
A new Law of Magic	1000+ EP (GM Discretion)

This process can be collaborative. Multiple characters can pool their sacrificed TEP to fund a single, grand creation.

### 3.3 · Step 3: The Resonance Test (The Consequence)
A new creation does not enter a void; it enters a universe with existing laws and harmonies. The GM takes the player's blueprint and entropic investment and runs a Resonance Test. This is a narrative challenge where the GM personifies the existing laws of reality. The outcome of this "debate" determines the final form of the creation and, crucially, any unintended consequences (Residue Events). A powerful but hastily designed creation might have dangerous side effects, becoming a new source of conflict and adventure for the world.

## §4 · Example: The Golem of the Iron Heart
A party of high-level adventurers decides to create a new type of sentinel to guard their city.

The Concept: The party's Artificer player designs a new creature: "The Golem of the Iron Heart." They write a detailed module for it, specifying its body parts, attributes, and a unique ability to share its defensive EP with nearby allies. They succeed on a DC 35 Intelligence check.

The Investment: The Golem is designed with an Entropic Budget of 150 EP. The cost to create the first one is 150 x 10 = 1500 TEP. This is beyond any single character. The five members of the party each agree to sacrifice 300 TEP from their own maximum pools to fund the creation.

The Resonance Test: The GM runs the test. The universe "pushes back" on the concept of a golem that can share its essence so freely. The unintended consequence is that when the Golem takes massive damage, a portion of that damage is psychically echoed to all those it is protecting. The players have their guardian, but it comes with a new and dangerous risk.

## §5 · Assemblé
The ultimate expression of a coherent will is not to master the rules of the world, but to write new ones. Metaphysical Engineering is the final stage of a hero's journey, where they transition from the protagonist of a story to an author of the stories yet to come. By sacrificing a piece of their own soul, they leave a permanent, resonant mark on reality—a new song for the world to sing. This is the art of creation, and it is the truest and most lasting form of power.

---

## TLE-011_AoE_and_the_environment.md

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

---

## TLE-012_the_art_of_the_toy_item_minigames_&_enchantments.md

---
#───────────── The Lost Eternal ──────────────────────
id:        TLE-012
title:     The Art of the Toy, Item Minigames & Enchantments
version:   1.0-ratified
parents:   [TLE-010]
children:  []
engrams:
 - system:item-customization
 - mechanic:item-minigames
 - concept:enchantment-as-a-system
 - system:unique-item-framework
keywords:  [items, minigames, enchanting, weapons, wands, wards, TLE]
uncertainty_tag: Low
module_type: core-mechanic-expansion
---
## §1 · Preamble: The Rule-Bending Object
In the world of The Lost Eternal, an item is more than a tool; it is a vessel for a unique idea, a physical container for a fragment of will. The most powerful artifacts are not those with the highest raw power, but those that possess their own unique "minigame"—a special subsystem that allows its wielder to interact with the world in a way no one else can. This module provides the framework for these interactive items, turning the act of gearing a character into a collection of unique, build-defining toys.

## §2 · The Soul of the Item: The Enchantment Principle
Every unique item begins with a simple principle: Entropy can be invested to create a rule. By permanently sacrificing TEP into an object, a creator can give it a soul—a pool of its own Entropy and a unique instruction on how to use it. This is the foundation of all minigames.

Example: The Returning Dagger (10 EP Investment):

A creator sacrifices 10 TEP into a dagger. This creates a 10 EP "Return" pool within the item. The wielder can spend 10 EP from this pool to have the dagger instantly return to their hand after being thrown. The pool regenerates half it's TEP per round when used for movement.

Example: The Swift Blade (10 EP Investment):

10 TEP is sacrificed into a sword to grant it "Lightness." This creates a 10 EP pool that the wielder can spend from to reduce the EP cost of their own attacks made with the blade, effectively granting them "free" swings.

## §3 · Minigame Type: Weapon Containment
Warriors and mages channel entropy differently. A mage's body is the conduit, risking an Entropic Overload on a miss. A warrior uses a weapon as a dedicated, safer conduit.

The Minigame: A weapon has its own TEP, representing its structural integrity. When attacking with the weapon, the wielder does not use the Universal Accuracy Check. Instead, they make a simple Weapon Attack Roll (d20 + relevant attribute modifier) against the target's Active Defense or a base DC.

The Risk & Reward: A warrior can safely channel EP into their weapon up to its TEP limit. However, they can choose to Overload the Weapon, pushing more EP into the strike than the weapon can contain.

The Check: When a weapon is Overloaded, it must make a Constitution "saving throw" (a d20 roll, using its own CON score, which is derived from its TEP). The DC is 10 + the amount of EP overloaded.

Success: The attack goes off with devastating force, and the weapon holds.

Failure: The attack still hits, but the weapon shatters into mundane fragments, its magic and TEP lost forever.

## §4 · Minigame Type: Arcane Conduits & Wards
Magic-users have a host of items designed to augment their dangerous art.

### 4.1 · Wands & Staves (The Glass Cannon)
A wand is an external battery for a mage. As per the enchanting rules, it has its own TEP, attributes, and a high ERR, allowing it to regenerate EP far faster than a character. This makes it an intensely powerful tool for burst damage.

The Minigame: The wand is a separate entity. The caster can draw EP from the wand's pool instead of their own to cast spells. However, the wand is a fragile object with its own (usually very low) Health Pool. Any attack that targets the wand can easily destroy it, making its wielder's source of power a vulnerable and tempting target for enemies.

### 4.2 · Wards (The Recharging Buffer)
A ward is a small, semi-sentient magical field that offers a buffer against incoming attacks.

The Minigame: A ward is an item that grants its wearer a Temporary HP Pool.

Capacity: This pool is typically very small (e.g., 4-8 EP).

Recharge: The ward has its own passive Recharge Rate (e.g., 1 EP per round). This recharge only begins on the round after the ward has taken damage.

The Dynamic: This creates a unique defensive rhythm. A warded character can absorb a small hit for free, but a sustained barrage will break through the ward and attack their true defenses. It rewards tactical positioning and gives characters a chance to mitigate chip damage from things like archer fire or environmental hazards.

## §5 · Assemblé
To find a new item is to find a new way to see the world. A sword is not just a sharp piece of metal; it is a choice between a measured strike and a final, shattering blow. A ward is not just armor; it is a breath, a rhythm of defense and recovery. In this world, the greatest heroes are not just those with the most power, but those who have collected the most interesting toys, and have mastered the unique, wonderful, and dangerous games that each one plays.

---

## TLE-013_curses_blessings_&_transformations.md

---
#───────────── The Lost Eternal ──────────────────────
id:        TLE-013
title:     The Unstable Form, Curses, Blessings, & Transformations
version:   1.0-ratified
parents:   [TLE-006]
children:  []
engrams:
 - system:status-effects
 - mechanic:dynamic-tep-reallocation
 - concept:loss-of-control
 - system:worldbuilding-through-mechanics
keywords:  [curses, blessings, transformation, werewolf, vampire, conditions, TLE]
uncertainty_tag: Low
module_type: core-mechanic-framework
---
## §1 · Preamble: The Resonant Scar
An entity is a coherent pattern of will, but some experiences—a divine blessing, a vile curse, a profound trauma—are so powerful they can permanently alter that pattern. They become a resonant scar, a Wound Channel that does not just weaken the soul but actively rewrites it under specific conditions. This module provides the framework for these transformative states, allowing for the creation of classic archetypes like werewolves, vampires, and demigods using the core physics of the system.

## §2 · The Nature of a Transformative State
A curse or blessing is mechanically treated as a unique and powerful type of Wound Channel (TLE-006). It is a persistent condition with three key components:

The Trigger (The "Vulnerability"): The specific condition that causes the transformation to occur (e.g., "the light of a full moon," "the taste of blood," "at will").

The Reallocation Mandate (The "Insight"): A mandatory, instantaneous reallocation of the character's invested Entropy Points. This is the mechanical core of the transformation.

The Coherence Threshold: The point at which the character's own will is overwhelmed by the transformative state, resulting in a loss of control to the Game Master.

## §3 · The Reallocation Mandate: Mutable TEP
When a transformation is triggered, the character's invested EP is forcibly and instantly reallocated according to the curse's mandate. The character does not spend new EP; their existing investment is simply moved.

Mechanic: The mandate is a simple formula of debits and credits.
X EP is removed from [Attribute A] and [Attribute B] and is added to [Attribute C] and [Attribute D].

Example: The Werewolf's Curse

Trigger: The light of the full moon.

Reallocation Mandate: "Remove up to 40 EP invested in your Intelligence and Wisdom attributes. For every point removed, add one point to your Strength and Dexterity pools, divided as you choose."

A starting character with 14 EP in INT and 14 EP in WIS would see their mental attributes stripped to almost nothing. Those 28 points would then be dumped into their physical attributes, turning them from a thinking person into a primal killing machine.

## §4 · The Coherence Threshold: Loss of Control
An entity's consciousness is a function of its mental attributes. If a transformation pushes those attributes below a critical point, the character's will is fractured, and the primal instincts of the curse take over.

The Rule: If a character's Intelligence Score or Wisdom Score (not the EP invested, but the final calculated Score from TLE-000) is reduced to 0 or less during a transformation, the player loses control of their character.

GM Control: The character is now an NPC under the GM's control. The GM must roleplay the character according to the pure, undiluted nature of the transformative state (e.g., the werewolf's predatory hunger, the vampire's overwhelming thirst, the demigod's divine arrogance) until the transformation ends.

The Struggle: A player whose character is on the verge of this threshold (e.g., INT Score of 1) can feel the struggle internally. They might have to make Wisdom saving throws to resist acting on the curse's primal urges even while they are still "in control."

## §5 · Assemblé
To be cursed is not to be weakened, but to be rewritten. A werewolf is not a man who becomes a wolf; it is a single soul trapped between two different, competing allocations of its own finite power. This system allows us to tell these ancient stories not as magical exceptions to the rules, but as dramatic, high-stakes expressions of the rules themselves. It reframes the struggle for control not as a battle against a monster, but as a desperate fight to maintain the coherence of one's own identity against the resonant echoes of a powerful scar.

[Extras]

## §1 · Preamble: The Shape of Suffering
Where TLE-013 laid the foundation for transformative states, this after-module serves as a gallery of practical examples and advanced mechanics. Every curse, every affliction, is a story written in the language of Entropy. This is not an exhaustive list, but a collection of case studies—the Succubus's pact, the Vampire's thirst, the Banshee's eternal sorrow—designed to showcase the depth of the system and provide a toolbox for Game Masters to craft their own unique and meaningful narratives of transformation.

## §2 · Advanced Mechanic: Entropic Attrition (Mind Control)
The will is not a switch to be flipped but a mountain to be weathered. True control over another being cannot be achieved with a single spell but must be won through a grueling battle of entropic attrition.

The Process: The attacker targets a victim's mental attributes (Intelligence or Wisdom). To "damage" these attributes, the attacker must spend 2 EP from their own pool for every 1 point of EP they wish to remove from the target's invested attribute pool. This represents the immense inefficiency of imposing one's will upon another.

The Battle: This is a contested process. The target can use their Active Defense (spending their own EP) to resist the mental intrusion on a 1-to-1 basis. This creates a drawn-out struggle where the attacker tries to drain the defender's mental reserves.

The Goal: The attacker's goal is to reduce the target's Intelligence Score or Wisdom Score to 0, at which point the victim falls under their control as per the Coherence Threshold rule (TLE-013). This makes mind-controlling a "steely-minded warrior" a monumental undertaking, as it should be.

## §3 · A Gallery of Curses & Afflictions
The following are examples of how to model classic archetypes within this framework.

## 3.1 · The Succubus's Situation
This is not a curse but a symbiotic, parasitic pact, closer to a Warlock's bond than a simple affliction.

The Pact: The "victim" (the Host) forges a pact with a powerful entity (the Patron). The Host gains access to a significant pool of raw power or some other boon. In return, the Patron can use the Host as a remote conduit for their own will.

Reallocation Mandate: The Host suffers a permanent, massive reduction in their invested Wisdom and Intelligence EP. This EP is not reallocated elsewhere; it is held in a special "Pact Pool."

Mechanics of Control: The Host has no control over the Pact Pool. The Patron (controlled by the GM) can cast spells or use abilities through the Host, drawing the EP cost from the Pact Pool. The Host is merely a vessel for the Patron's actions, which are often cruel and targeted at those the Host cares about to maximize their suffering and "flavor" the energy they provide.

## 3.2 · The Banshee's Sorrow (A State of Undeath)
A banshee is not a creature, but a state of being: a soul trapped in a perfect, agonizing equilibrium between thought and suffering.

The State: This is not a transformation but a permanent form. A Banshee's TEP is allocated in a fixed, tragic ratio.

Reallocation Mandate:

4-to-1 Conversion: For every 4 EP invested in Constitution, 1 EP is granted to the Intelligence pool. This creates an entity of immense resilience and piercing intellect.

Negative Wisdom: The entity's base Wisdom score is set to a negative value. They are trapped in a state of pure intellect without the capacity for peace, perspective, or understanding. They perceive everything but comprehend nothing, which is the source of their eternal wail.

## 3.3 · The Vampire's Thirst
Vampirism is a curse centered on a constantly fluctuating resource pool that governs the vampire's very nature.

The Hunger Pool: A vampire has a special Hunger Pool with a maximum capacity (e.g., 50 EP). This pool can only be filled by consuming the blood of sentient creatures. Each day, the pool depletes by a certain amount (e.g., 1d6 EP).

The Transformation: The vampire's state is directly tied to the current level of their Hunger Pool.

Sated (Hunger Pool > 50%): The vampire is in "Lordly Form." They have full control of their faculties and TEP allocation. They are lucid, cunning, and can pass for mortal.

Hungry (Hunger Pool < 50%): The thirst begins to take hold. The vampire takes a penalty to all Wisdom checks as their primal instincts sharpen.

Starving (Hunger Pool < 10%): The vampire enters "Primality Mode." They lose control.

Trigger: Dropping below 10% Hunger.

Reallocation Mandate: All EP invested in Wisdom is immediately drained and dumped into a combined pool for Strength & Dexterity. The vampire can no longer make nuanced skill checks but becomes a terrifyingly fast and strong predator. Their INT remains, making them a cunning, but purely instinct-driven, hunter.

Coherence Threshold: The GM controls the character, whose only goal is to feed by any means necessary.

## 3.4 The Pact

A Pact is a formal agreement where a powerful entity (a Patron) invests its own Entropy to grant a boon to another being (the Granted). This boon most often takes the form of a Feat or Skill the Granted could not otherwise afford. This is a powerful but perilous arrangement, as the invested Entropy never truly belongs to the recipient.

The Investment:
To initiate a Pact, the Patron must pay the full TEP cost of the granted Feat. Furthermore, the act of transferring and binding this power is inefficient and costly. The Patron must pay an additional Transfer Fee equal to 20% of the Feat's cost (rounded up). This total investment is a measure of the Patron's stake in the Granted.

Example: A Patron wishes to grant the 12 EP "Reactive Evasion" Feat. It must spend 12 EP for the Feat + 3 EP (20% of 12, rounded up) for the Transfer Fee, for a total investment of 15 EP.

The Condition: Loaned Entropy
The Feat and its associated TEP are considered Loaned Entropy. The Granted gains all benefits of the Feat, but this TEP does not count toward their own Total Entropy Pool and cannot be used for any other purpose. It is a parasitic or symbiotic graft onto their soul.

The Leverage: The Pact's Hold
The total EP invested by the Patron (Feat Cost + Transfer Fee) becomes the Pact's Hold. This is a mechanical measure of the Patron's influence over the Granted. The GM can use this value in several ways:

As a Target Number (TN) for any checks the player makes to resist the Patron's direct commands or subtle influence.

As a pool of EP the Patron can draw from to manifest effects related to the Pact, such as communicating with or scrying on the player.

As a measure of how difficult it is to break the Pact through magical or mundane means.

The Consequences:
A Patron can revoke a granted Feat or Skill at any time, instantly reclaiming their invested EP. More insidious Patrons may offer further boons in exchange for greater concessions, such as a Mutual Investment Clause, where the Granted agrees to channel a portion (or all) of their future earned TEP through the Patron, giving the entity ever-increasing control in exchange for power. A character who enters into too many such bargains may find their will is no longer their own.

Entities, players and even some powerful animals may do this for one another under the same conditions.

## 3.5 Sentient Items

Beyond simple enchantment, it is possible through a profound and costly ritual to imbue an item with the entire essence of a being. This process creates a sentient object, a vessel for a consciousness that is now inextricably linked to its new form.

The Imbuing Ritual:
The transference of a soul is a violent and inefficient process that requires an immense expenditure of entropic power.

The Cost: A ritualist must expend an amount of pure Entropy equal to 120% of the target entity's total Entropy Budget. This cost is permanent and represents the energy required to dissolve the entity's form and bind its essence to a new vessel. This must be done all at once or over time accruing entropy from the entity.

The Vessel: The target item must have an inherent "entropy capacity" sufficient to contain the entity's full budget. Mundane items like a simple dagger may not be able to contain the soul of a powerful being, while legendary artifacts might be crafted for this very purpose.

Mechanics of a Sentient Item:
An item imbued with an essence is, for all intents and purposes, a new character.

The Item Card: A sentient item has its own character sheet, with the imbued entity's TEP, ERR, and attributes. Its physical form is now the item itself.

Independent Will: The item has its own turn in combat and acts on its own will, though it may be wielded by another. Its goals may or may not align with its wielder's.

Durability & Mortality: A sentient item can repair minor damage to itself over time by spending its own EP. However, if the item is fundamentally destroyed, the entity within it is irrevocably annihilated.

The Extraction Ritual:
Removing an entity from its vessel is even more difficult than imbuing it. It requires 120% of the original imbuing cost (a total of 144% of the entity's original budget). A new host body or vessel must also be provided for the essence to inhabit. This process can be done with the entity's consent; otherwise, it is treated as a possession attempt, governed by the mind control rules.

## 3.6 · The Tamer's Conversation
Taming a wild beast is not an act of domination, but a contest of wills—a conversation without words.

The Process: To tame a creature, a character must engage it in a "conversation." This involves a series of contested checks (typically the tamer's WIS vs. the beast's WIS). The tamer must "win" this conversation a number of times equal to the beast's WIS Score.

The Beast's Will: A wild creature does not wish to be tamed. During this contest, the beast adds its CON Score to its roll, representing its raw, instinctual resistance to being controlled. A tamer must overcome not just the beast's mind, but its very nature.

## 3.7 · The Soul Bond
A tamed beast is a companion, but a bonded beast is family. Forging a Soul Bond is a profound act of sacrifice and trust.

The Cost: To form a Soul Bond, a tamer must willingly and permanently invest a portion of their own TEP equal to the full Entropy Budget of the beast. This TEP is removed from the tamer and woven into the beast's soul, creating an unbreakable link.

The Benefits:

Shared Power: The tamer can now directly invest their own TEP into the bonded creature's attributes or skills without the 20% "Pact" tax.

Resurrection: If the bonded creature is killed, the tamer can perform an hour-long ritual to restore it to life, spending their own EP to reform its body. However, if a creature is destroyed by taking damage equal to its full Entropy Budget, it is annihilated and cannot be recovered.

The Burden: A tamer's focus is divided. For each bonded creature that follows them, one point of their Entropy Regeneration Rate (ERR) is dedicated to supporting that creature's needs. A tamer with three bonded beasts and an ERR of 4 would only regenerate 1 EP for themselves per round.

Familiars: A creature designated as a Familiar does not impose this ERR burden, but it cannot take the Attack action. If it does, it is considered a Guardian and immediately imposes the ERR cost. This is irreversible.

## §4 · Assemblé
A curse is a story that the body is forced to tell. Each affliction is a unique narrative, a different shape of suffering or a different price for power. This gallery is merely the first chapter. Use these principles as a lens to re-examine the old tales, and as a toolbox to forge new ones. The possibilities are as limitless as the ways a soul can be scarred, blessed, or broken.

---

## TLE-014_character_creation_guide.md

---
#───────────── The Lost Eternal ──────────────────────
id: TLE-014
title: Character Creation Guide
version: 1.0-consolidated
parents: [TLE-000]
children: []
engrams:
 - system:character-creation
 - mechanic:freeform-creation-system
 - templates:body-plans
keywords: [character creation, body plan, attributes, TLE]
uncertainty_tag: Low
module_type: core-rulebook-consolidated
---
A Guide to Creating Your Character
Welcome to the Bottom Realm, a world at the edge of all planes, scarred by the echoes of forgotten power. In this reality, a being is not born into a fixed form. A being is a choice, a pattern of will, an entropic form sculpted from the raw potential of your own soul.

This guide will walk you through the process of creating your character. Forget what you know about traditional character sheets. Yours will not be a list of statistics, but a ledger of your will—a blueprint for the soul you choose to manifest.

Step 1: The Spark of Will (Your Entropy Budget)
Every new being starts as a spark of pure potential. This is your Total Entropy Pool (TEP). It is the finite, precious resource from which you will sculpt every aspect of your character, from the strength of their arm to the sharpness of their mind.

Starting Entropy: Your character begins with a Total Entropy Pool (TEP) of 35 Entropy Points (EP). Every choice you make from now on will be an investment of this pool.

Step 2: The Containers of Will (The Five Attributes)
Your first act as a sculptor is to give your will a shape by pouring your starting Entropy into five core containers, or Attributes. These are not just numbers; they are the deep reservoirs of your character's innate potential.

To invest in an attribute, simply decide how many of your 35 EP you wish to allocate to it. From this investment, you will calculate two key numbers: the Attribute Score and the Attribute Modifier.

Attribute Score: This represents the raw power of the attribute.

Score = floor(EP Invested / 2)

Attribute Modifier: This is a smaller number used for most in-game checks.

Modifier = floor(Score / 4)

The Five Attributes:
Strength (STR): Raw physical power and force. A high Strength allows you to overpower foes and shape the physical world.

Dexterity (DEX): Agility, reflexes, and fine control. A high Dexterity allows you to act quickly, aim true, and navigate the flow of combat.

Constitution (CON): Endurance and your connection to the flow of Entropy. A high Constitution determines how quickly you regenerate your power and your ultimate potential for growth.

Intelligence (INT): Logic, memory, and the ability to impose complex will. A high Intelligence allows you to outthink opponents, recall crucial information, and control the battlefield with tactics and magic.

Wisdom (WIS): Intuition, perception, and insight. A high Wisdom allows you to read the intentions of others, notice hidden details, and make sound judgments under pressure.

Narrative Guidance: The "What's Your Story?" Method
Don't just assign numbers. Ask yourself questions about your character's story to guide your EP investment.

What is your greatest strength? Invest a significant portion of your EP there.

What is a weakness you struggle with? Invest fewer EP in that attribute.

Are you a thinker or a doer? A fighter or a talker? Let the answers shape your soul's blueprint.

Step 3: The Architecture of Being (Your Physical Form)
Once you have defined the nature of your will, you must give it a physical vessel. You must spend EP from your remaining pool to purchase your character's body, piece by piece.

| Body Part | Base EP Cost | Notes |
| Torso | 1 EP | Required. The core of your form. |
| Head | 1 EP | Required. Houses your primary consciousness. |
| Standard Limb | 3 EP | A complete limb with a manipulator (e.g., arm with hand, leg with foot, tentacle with suckers). |
| Basic Limb | 2 EP | A simpler limb (e.g., tail, slippery whiplike tentacle). |
| Wing | 4 EP | A limb specifically for flight. |

Size as Invested Power
You can invest more EP into a limb beyond its base cost. This extra EP is called Size Entropy and is ring-fenced for that limb. It can only be used to power physical actions made with that specific part (like a mighty punch or a powerful kick). This allows you to create asymmetrical characters—a blacksmith with one massively powerful arm, or a creature with a heavy, club-like tail.

Step 4: The Windows to the World (Your Senses)
Your ability to perceive the world is a direct function of your investment.

Cost of Senses: Each sensory organ (an eye, an ear, a scent organ) costs 1 EP. A standard humanoid form might have two eyes and two ears, for a total cost of 4 EP.

Mechanical Benefit: You can make one passive perception check per relevant sensory organ each round, making characters with exotic senses exceptionally aware.

Step 5: The Integrity of Form (Health & Defense)
Your health is a direct measure of your form's coherent integrity. It is not an abstract number, but is derived directly from the EP you invested in your body.

Calculating Max HP:

Max HP = (EP in Torso) + floor(0.5 * Total EP in all Limbs)

This means that a character with more limbs, or more powerfully invested limbs, is inherently tougher and more resilient to damage.

Appendix: Body Plans (Form Templates)
This section is a modular library of pre-calculated "body plans" to help you quickly assemble a physical form. As you discover or create new forms, you can add them here.

Humanoid, Standard (Total Cost: 18 EP)
This is a classic, balanced form suitable for most adventurers.

Torso: 1 EP

Head: 1 EP

Arm (x2): 6 EP (3 EP each)

Leg (x2): 6 EP (3 EP each)

Eyes (x2): 2 EP

Ears (x2): 2 EP

Derived Max HP: 1 + floor(0.5 * (6 + 6)) = 7 HP

Quadruped, Sturdy (Total Cost: 20 EP)
A four-legged form built for stability and power.

Torso: 1 EP

Head: 1 EP

Foreleg (x2): 6 EP (3 EP each)

Hindleg (x2): 6 EP (3 EP each)

Eyes (x2): 2 EP

Ears (x2): 2 EP

Scent Organ (x1): 1 EP (in the snout)

Derived Max HP: 1 + floor(0.5 * (6 + 6)) = 7 HP

Avian, Graceful (Total Cost: 20 EP)
A form built for flight, prioritizing agility and keen senses.

Torso: 1 EP

Head: 1 EP

Leg (x2): 6 EP (3 EP each)

Wing (x2): 8 EP (4 EP each)

Eyes (x2): 2 EP

Ears (x2): 2 EP

Derived Max HP: 1 + floor(0.5 * (6 + 8)) = 8 HP

Insectoid, Carapaced (Total Cost: 22 EP)
A multi-limbed form with a sturdy build and exotic senses.

Torso: 1 EP

Head: 1 EP

Standard Limbs (x4 for walking): 12 EP (3 EP each)

Basic Limbs (x2 for manipulation): 4 EP (2 EP each)

Compound Eyes (x2): 2 EP

Antennae (Sensory Organs, x2): 2 EP

Derived Max HP: 1 + floor(0.5 * (12 + 4)) = 9 HP

Giant-kin, Hulking (Total Cost: 18+ EP)
A form whose power comes from sheer scale, not complexity.

Torso: 1 EP

Head: 1 EP

Arm (x2): 6 EP (3 EP each)

Leg (x2): 6 EP (3 EP each)

Eyes (x2): 2 EP

Ears (x2): 2 EP

Derived Max HP: 1 + floor(0.5 * (6 + 6)) = 7 HP

Note: The power of a Giant-kin comes not from a more complex form, but from investing significant Size Entropy into their limbs during character creation.

Cyclops, Focused (Total Cost: 17 EP)
A humanoid form with a singular, powerful sense of sight.

Torso: 1 EP

Head: 1 EP

Arm (x2): 6 EP (3 EP each)

Leg (x2): 6 EP (3 EP each)

Eye (x1): 1 EP

Ears (x2): 2 EP

Derived Max HP: 1 + floor(0.5 * (6 + 6)) = 7 HP

Fur-folk, Nimble (Total Cost: 21 EP)
A quick, agile form with a prehensile tail and heightened senses.

Torso: 1 EP

Head: 1 EP

Arm (x2): 6 EP (3 EP each)

Leg (x2): 6 EP (3 EP each)

Basic Limb (Tail, x1): 2 EP

Eyes (x2): 2 EP

Ears (x2): 2 EP

Scent Organ (x1): 1 EP

Derived Max HP: 1 + floor(0.5 * (6 + 6 + 2)) = 8 HP

Advanced Physical Forms (High EP Cost)
These templates are for players who wish to create a character that is a true physical specialist. They invest almost their entire starting TEP of 35 EP into their body, leaving little or no EP for their Attributes. This creates a character who is a physical powerhouse but may be vulnerable in mental or social challenges. A true "all-in" build.

Ape-Kin, Brute (Total Cost: 35 EP)
A hulking bipedal form defined by its massively powerful arms, built to crush and dominate.

Torso: 1 EP

Head: 1 EP

Arm (x2): 20 EP (Base 3 EP + 7 Size Entropy each)

Leg (x2): 8 EP (Base 3 EP + 1 Size Entropy each)

Eyes (x2): 2 EP

Ears (x2): 2 EP

Scent Organ (x1): 1 EP

Derived Max HP: 1 + floor(0.5 * (20 + 8)) = 15 HP

Note: This build leaves 0 EP for Attributes, resulting in all Attribute Scores and Modifiers starting at 0. It is a creature of pure physical instinct and power.

Tiger-Kin, Pouncer (Total Cost: 34 EP)
A predatory quadruped whose entire form is a weapon, with immense power invested in its legs for explosive lunges and its head for a devastating bite.

Torso: 1 EP

Head: 1 EP + 5 Size Entropy (for a powerful jaw)

Foreleg (x2): 10 EP (Base 3 EP + 2 Size Entropy each)

Hindleg (x2): 12 EP (Base 3 EP + 3 Size Entropy each)

Eyes (x2): 2 EP

Ears (x2): 2 EP

Scent Organ (x1): 1 EP

Derived Max HP: 1 + floor(0.5 * (10 + 12)) = 12 HP

Note: This build leaves 1 EP for Attributes. This single point could be placed in an attribute like Dexterity or Wisdom to represent its predatory cunning, but all other attributes will be 0.

Scorpion-Kin, Terror (Total Cost: 35 EP)
A nightmarish fusion of humanoid and arachnid, featuring a heavily armored torso, powerful grasping claws, and a venomous tail.

Torso: 1 EP + 4 Size Entropy (for a thick carapace)

Head: 1 EP

Standard Limbs (Legs, x4): 12 EP (3 EP each)

Standard Limbs (Claws, x2): 10 EP (Base 3 EP + 2 Size Entropy each)

Basic Limb (Tail, x1): 2 EP + 1 Size Entropy (for a stinger)

Compound Eyes (x2): 2 EP

Antennae (Sensory Organs, x2): 2 EP

Derived Max HP: 5 + floor(0.5 * (12 + 10 + 3)) = 17 HP

Note: This build leaves 0 EP for Attributes. It is a heavily armored and versatile physical threat, but with no investment in its mental or social capabilities.

---

## TLE-015_session_0_gm_only.md

---
#───────────── The Lost Eternal ──────────────────────
id: TLE-015
title: Session 0, for GMs
version: 1.0-consolidated
parents: [TLE-000]
children: []
engrams:
 - system:character-creation
 - mechanic:freeform-creation-system
 - templates:body-plans
keywords: [character creation, body plan, attributes, TLE]
uncertainty_tag: Low
module_type: core-rulebook-consolidated
---
This guide provides the framework for running the first session of "The Lost Eternal," covering character creation, the party's arrival in the bottom realm, and their introduction to the core survival mechanics of the world.

Session 0: The Condemnation
The campaign begins before the first die is rolled. Character creation is an intense, in-character process where each player must answer two questions that define their starting point:

The Accusation: What crime were you accused of by the Skazan Order? (This can be anything from high treason to petty heresy).

The Truth: Were you actually guilty?

This process immediately grounds the characters in the world and provides rich roleplaying hooks.

The Spectacle
The game begins in media res. Describe the scene: the characters are prisoners, paraded before a town square. A Skazan lieutenant performs a grand, cruel ritual. Describe the flash of entropic energy as they are torn from their plane, and the final, heart-wrenching detail: a curse of forgetfulness that erases them from the memories of their loved ones, sometimes performed right in front of the family for maximum effect.

Session 1: The Arrival
Systraeslakia, The Weeping Statue
The players arrive cold, wet, and disoriented on a massive, rocky island hundreds of feet in the air. This is Systraeslakia, a weathered statue caught in a perpetual torrent of water that falls from countless cave openings above. The roar of the water is deafening, making conversation difficult and forcing the party to rely on non-verbal cooperation.

The Challenge: The statue is slick and treacherous. Any attempt to climb it is futile. The goal here is to establish the environment's hostility and encourage the party to work together.

The Panorama: From the edge of the statue, they can see the vast panorama of the starting area: the August Jag, an endless sea of wheat, with distant mountains on the horizon.

High Tide: Other survivors are present, all nervously moving away from the center of the statue. A deep gurgling sound signals "high tide." A massive surge of water washes over the statue, sending the party plunging into the churning lake below. A Skazan enchantment prevents them from taking damage, but the experience is terrifying.

The Shore and the Choice
The party must make their way to the shore. As night falls, they face their first major decision:

Huddle on the beach with the other nervous survivors.

Venture into the whispering, golden fields of the August Jag.

The First Night: Wheat-Wolves
Regardless of their choice, the first night brings the first threat. A pack of wheat-wolves (large, golden-furred pack hunters with glowing red eyes) emerges from the fields.

The Encounter: The pack size is 1.5 times the number of players, rounded up. The party can choose to fight or use the stealth mechanics to let them pass. A failed stealth check initiates combat.

New Mechanic: Trophies, Residue & The Sculptor's Art
The Scavenger
The day after the wolf encounter, the party comes across the aftermath of another fight. They witness a grizzled Scavenger taking trophies (claws, teeth, pelts) from the corpses of the unlucky. This is how you introduce the core economic loop of the game.

§1 · Trophies & Residue

The Principle: Defeated creatures do not carry gold; their value lies in the Residue of their entropic potential, which is stored in their physical remains (trophies). Players must harvest these trophies to gain power.

The Conversion Race: Residue is inert and useless until it is transmuted. This transmutation can be done by a skilled individual as a 1 hour ritual for up to 15 EP at a time. If multiple characters attempt to transmute the same pool of Residue, the first to complete the ritual gains the full TEP reward. This encourages a tense, competitive dynamic.

The Unseen Threat: Unclaimed corpses still radiate Residue. This can attract dangerous scavengers or other entropic creatures. Disposing of bodies after a fight is a crucial, tactical decision.
t-
§2 · The Sculptor's Art

The Profession: A Sculptor is a master artisan who has learned to transmute Residue into usable TEP for others. They are found in all major settlements.

The Cost: A Sculptor's service is not free. The cost to transmute a pool of Residue for another person is 3 EP: 1 EP from the Sculptor's own pool (representing their effort) and 2 EP from the transmuted total (the "tax" or cost of the service).

The Artisan-Warrior: The "Professional Aptitude (Sculptor)" feat allows a character to become a Sculptor. Their professional skill pool can be used to perform transmutations and, like any other profession, can be weaponized in combat.

First Contact: Glints
The Scavenger is hostile and proves to be a tough opponent, quickly overwhelming the party. Before a killing blow is struck, an arrow whistles through the air and strikes the Scavenger, who flees.

The party's savior is Glints, a sharp-eyed archer. She is a friendly survivor who offers to guide them to the nearest city, The Endeavor.

The First City: The Endeavor
The Endeavor is a colossal walking city, a marvel of arcane engineering that stalks the plains on six massive, geared legs.

Population: Approx. 5,800 residents living in a honeycomb of corridors.

Leadership: Run by Enrio Poltock, a shrewd and observant old man who takes an interest in all newcomers.

Services: The city offers a bustling hunter's guild, various shops (maps, simple weapons, arcane scrolls), and, most importantly, the services of Sculptors. Players can also purchase information about the Skazan Order or even hire guides to help them navigate the treacherous world.

Session one likely concludes here, with the party safe for the moment, introduced to the core mechanics, and presented with their first set of choices for their adventure.

---

## TLE-016_gm_bestiary.md

---
#───────────── The Lost Eternal ──────────────────────
id: TLE-016
title: GM Bestiary
version: 1.0-consolidated
parents: [TLE-000]
children: []
engrams:
 - system:bestiary
 - mechanic:freeform-creation-system
 - templates:denizens
keywords: [character creation, body plan, attributes, TLE]
uncertainty_tag: Low
module_type: core-rulebook-consolidated
---
This document is a catalog of the strange, dangerous, and unique creatures that inhabit the entropic landscape of the bottom realm. Each entry provides a mechanical stat block and tactical notes for the Game Master.

- Wheat-Wolf (Hungry Scavenger)
A wolf-hog hybrid with a stocky, powerful body covered in shaggy, wheat-colored fur. Its eyes glow with a feral red light, and sharp, carnivorous tusks jut from its maw. They are relentless pack hunters that stalk the endless fields of the August Jag.

Total Entropy Pool (TEP): 35 EP

Attributes (5 EP):

STR: 2 EP (Score 1, Mod +0)

DEX: 2 EP (Score 1, Mod +0)

CON: 1 EP (Score 0, Mod +0)

INT: 0 EP (Score 0, Mod +0)

WIS: 0 EP (Score 0, Mod +0)

Physical Form (30 EP):

Torso: 1 EP

Head: 1 EP + 2 Size Entropy (for Tusks)

Standard Limbs (Legs, x4): 24 EP (6 EP each)

Senses (Eyes x2, Scent Organ x1): 3 EP

Max HP: 1 + floor(0.5 * 24) = 13 HP

Movement: 60 feet (Two pairs of Standard Limbs)

Skills & Feats: None

Actions:

Tusk Gore: Melee Attack. Spends Size Entropy from its Head to deal damage.

Tactics: Wheat-wolves are simple pack hunters. They use their superior speed to surround a target, and then the pack alpha will charge in to make the first attack. They are not tactically brilliant and will fight until slain or until their alpha is killed, at which point the rest of the pack will flee.

Residue: Tusks, Pelt, Heart (Low-value Residue).

- Nomad Bandit (Template)
The wastes are home to nomadic camps that shadow the great walking cities. These "second cities" are a haven for criminals, scavengers, and those who cannot or will not live by the strict rules of the city-states. Bandits from these camps are survivors, more interested in a quick score than a fair fight.

Total Entropy Pool (TEP): 50 EP (Bandit Thug)

Archetype (Roll 1d6):

Juggernaut: High STR, focuses on intimidation and heavy melee.

Arcanist: A desperate hedge-mage with one damaging elemental skill.

Phantom: A classic rogue with high DEX and a "Subterfuge" skill pool.

Weaver: A "blood-sculptor" who uses their art to inflict minor wounds.

Sentinel: Wears scavenged armor and uses a makeshift shield.

Drifter: A nimble skirmisher who uses dirty tricks to create difficult terrain.

Attributes, Form, & Skills: Distribute the 50 TEP according to the rolled archetype. Most will have a standard Humanoid form (18 EP).

Tactics: Bandits are opportunists. They will try to ambush their targets and use their numbers to their advantage. They are not zealots; a bandit reduced to half their HP will almost always attempt to flee or surrender. Their goal is to steal TEP (in the form of trophies) or valuable barter items, not to die for a cause.

Residue: Scavenged gear, a single trophy representing their primary skill (e.g., a spell focus, a lockpick, a blood-stained rag).

- Hole Hag
A terrifying shade born of the countless bodies buried unceremoniously beneath the wheat fields. It appears as a gaunt, shadowy form with long, grasping arms made of compacted soil and root. It does not wish to kill, but to drag the living down into the suffocating darkness from which it came.

Total Entropy Pool (TEP): 95 EP

Attributes (40 EP):

STR: 15 EP (Score 7, Mod +1)

DEX: 15 EP (Score 7, Mod +1)

CON: 10 EP (Score 5, Mod +1)

INT: 0 EP (Score 0, Mod +0)

WIS: 0 EP (Score 0, Mod +0)

Physical Form (15 EP):

Torso: 1 EP

Head: 1 EP

Standard Limbs (Arms, x2): 6 EP

Senses (Resonant Sense): 1 EP

Utility Limb (Burrowing Form): 4 EP

Max HP: 1 + floor(0.5 * 6) = 4 HP

Skills & Feats (40 EP):

Skill Pool: "Subterfuge": 30 EP (Used for its initial stealth)

Feat: Gloom-Sight (8 EP)

Feat: Kinetic Conversion (2 EP from CON)

Abilities:

Burrow: The Hole Hag can move through earth and soil as if it were open air. It cannot be targeted unless it is on the surface or something has burrowed to touch range.

Grave Grasp: Melee Attack. On a hit, the target is grappled. The Hole Hag can then use its action on subsequent turns to drag the grappled victim 5 feet underground. A creature dragged underground is considered Smothered.

Tactics: The Hole Hag is an ambush predator. It will lie in wait, using its Subterfuge pool to remain hidden. When a target passes over it, it will erupt from the ground and attempt to use Grave Grasp. If it successfully grabs a victim, it will immediately disappear back underground, dragging its prey with it. The only way to fight it effectively is to have a prepared action to strike the moment it appears.

Residue: A heart of compacted, grave-soiled earth (Uncommon Residue).

## Wastes Fauna & Horrors
- Zug
An enormous, hyper-territorial rat-mole hybrid that carves massive tunnel systems beneath the August Jag. Its powerful forelimbs allow it to burrow with terrifying speed, and its sheer bulk makes it the ursine equivalent of the wheat fields. Zugs mate for life, and where there is one, another is surely nearby.

Total Entropy Pool (TEP): 170 EP

Attributes (80 EP):

STR: 40 EP (Score 20, Mod +5)

DEX: 10 EP (Score 5, Mod +1)

CON: 30 EP (Score 15, Mod +3)

INT: 0 EP (Score 0, Mod +0)

WIS: 0 EP (Score 0, Mod +0)

Physical Form (90 EP):

Torso: 1 EP + 20 Size Entropy

Head: 1 EP + 10 Size Entropy (Bite)

Standard Limbs (Foreclaws, x2): 6 EP + 40 Size Entropy

Standard Limbs (Hindlegs, x2): 6 EP

Senses (Scent x1, Resonant x1): 2 EP

Utility Limb (Burrowing Form): 4 EP

Max HP: 21 + floor(0.5 * (46 + 6)) = 47 HP

Abilities:

Burrow: The Zug can move through earth and soil at its full movement speed.

Terrifying Roar: As an action, the Zug can emit a deafening roar. All creatures within 30 feet must succeed on a Wisdom check (TN 15) or be frightened for one round.

Tactics: A Zug is a straightforward brawler. It will often start a fight by bursting from the ground, using its Terrifying Roar to stun its prey, and then focusing its powerful claw attacks on the largest single threat.

Residue: Zug Claws, Pelts, Heart (High-value Residue).

- Pasty ("Skin")
The bitter end of a desperate soul, bleached and animated by ambient entropic energy. These eyeless undead are drawn inexorably to the scent of unlooted Residue. They do not shuffle, but run headlong towards their prey, their bodies little more than a delivery system for their grasping hands.

Total Entropy Pool (TEP): 60 EP

Attributes (10 EP):

STR: 5 EP (Score 2, Mod +0)

DEX: 5 EP (Score 2, Mod +0)

CON: 0 EP (Score 0, Mod +0)

INT: 0 EP (Score 0, Mod +0)

WIS: 0 EP (Score 0, Mod +0)

Physical Form (50 EP): Standard Humanoid (18 EP) with the rest invested as Size Entropy in its Torso for a reckless charge.

Max HP: 1 + 32 (Size) + floor(0.5 * 12) = 39 HP

Abilities:

Residue Sense: A Pasty automatically knows the location of any unharvested corpse within 1 mile.

Headlong Charge: A Pasty moves chest-first. It cannot take the Dodge action, but its first slam attack in a round deals bonus damage equal to its Torso's Size Entropy.

Tactics: Pasties are simple. They sense Residue and run directly towards it, attacking any living creature in their path. They fight mindlessly until destroyed.

- The Crazed (Template)
Not all can withstand the constant, chaotic pressure of the bottom realm. The Crazed are those whose minds have shattered, their bodies warped into unpredictable vessels of madness. They are tragic, dangerous, and utterly unpredictable.

Total Entropy Pool (TEP): 65 EP

Abilities:

Unstable Movement: When The Crazed uses its movement, it does not move normally. For every 5 feet it would move, roll 1d4. It teleports that many 5-foot squares in a random direction.

Tactics: The Crazed are erratic. They will attack the nearest creature, friend or foe, with their bare fists. Their random movement makes them a chaotic element in any battle, as likely to teleport into a pit as they are to appear behind a player.

- Skinbird
The apex predator of the wheat wastes. A terrifying, pterodactyl-like beast with a fleshy, maned neck and a long, muscular tail tipped with three venomous barbs. Its call is a deafening crack of thunder that can be heard for miles. It preys on Zugs, and anything else foolish enough to draw its attention.

Total Entropy Pool (TEP): 245 EP

Attributes (105 EP):

STR: 60 EP (Score 30, Mod +7)

DEX: 35 EP (Score 17, Mod +4)

CON: 10 EP (Score 5, Mod +1)

INT: 0 EP (Score 0, Mod +0)

WIS: 0 EP (Score 0, Mod +0)

Physical Form (140 EP):

Torso: 1 EP + 20 Size Entropy

Utility Limb (Beak): 4 EP + 20 Size Entropy

Utility Limbs (Wings, x2): 8 EP + 40 Size Entropy

Basic Limb (Tail): 2 EP + 20 Size Entropy

Utility Limb (Venom Gland): 4 EP + 10 Size Entropy

Senses (x2): 2 EP

Max HP: 21 + floor(0.5 * (60 + 22 + 14)) = 69 HP

Abilities:

Thunderous Cry: As an action, the Skinbird can unleash its call. All creatures within 120 feet must succeed on a CON check (TN 18) or be deafened for one minute.

Paralytic Venom: A creature hit by the Skinbird's tail barb must make a CON check (TN 20). On a failure, they lose 5 EP from their Constitution pool and are paralyzed for one round.

Tactics: The Skinbird is a patient hunter. It will circle high above, using its Thunderous Cry to disorient prey before diving. It will use its tail to paralyze a target, then land to finish it with its powerful beak and wings.

Residue: Skinbird Beak, Venom Glands, Heart (Legendary-value Residue).

- Swarms (Template)
A single rat is a pest. A thousand rats, united by a singular, wrathful will, are a tide of death. A swarm is not a collection of creatures, but a single entity with a shared pool of HP and a singular purpose.

Mechanics: A swarm of tiny creatures occupies a 10x10 foot space. It has a single HP pool and TEP. It is immune to effects that target a single creature. It can move through any opening large enough for one of its component creatures.

Swarm Attack: As an action, the swarm attacks all creatures within its space.

Example: Haunted Rat Swarm (TEP 75): A swarm of rats possessed by a vengeful spirit. Its swarm attack deals minor physical damage and forces a Wisdom check to avoid being frightened.

- Lamb Lion
A patient and horrifying ambush predator. This creature, a nightmarish fusion of a praying mantis and a spider, digs a pit in a well-traveled path, covers it with a fragile lid of woven wheat, and waits. It prefers to eat its prey alive, limb by limb.

Total Entropy Pool (TEP): 120 EP

Attributes (50 EP):

STR: 30 EP (Score 15, Mod +3)

DEX: 15 EP (Score 7, Mod +1)

CON: 5 EP (Score 2, Mod +0)

Physical Form (70 EP):

Torso: 1 EP + 10 Size Entropy

Head: 1 EP + 10 Size Entropy (Mandibles)

Utility Limbs (Mantis Claws, x2): 8 EP + 30 Size Entropy

Standard Limbs (Legs, x6): 18 EP

Senses (Compound Eyes x2): 2 EP

Max HP: 11 + floor(0.5 * (38 + 18)) = 39 HP

Abilities:

Ambush Hunter: The Lamb Lion spends its day creating its trap. The TN to spot the trap is 20.

Mantis Grapple: On a successful hit with its claws, the target is grappled.

Devour Limb: As an action, the Lamb Lion can begin devouring a limb of a grappled creature, dealing 1d10 damage. The TN to escape the grapple increases by the damage dealt this way. If a creature is held for 3 consecutive rounds, the limb is severed permanently.

Tactics: The Lamb Lion is a patient trapper. Once it has its prey, it will focus exclusively on devouring it, ignoring other threats unless it takes significant damage. It prefers not to leave its pit.

- Crow-Man (Silent Watcher)
A mysterious, secretive being that appears as a scarecrow-like figure wrapped in dark cloth. They are the silent guardians of the deep wastes, using swarms of crows as their eyes and wings. Their culture and motivations are a complete unknown, even to the Lepi.

Total Entropy Pool (TEP): 100 EP

Attributes (50 EP):

STR: 5 EP (Score 2, Mod +0)

DEX: 15 EP (Score 7, Mod +1)

INT: 10 EP (Score 5, Mod +1)

WIS: 20 EP (Score 10, Mod +2)

Physical Form (18 EP): Standard Humanoid

Skills & Feats (32 EP):

Arcane Skill "Primal Weaving": 10 EP

Feat: Thousand Forms Adept (12 EP) (Specialized in Crow Swarms)

Feat: Gloom-Sight (8 EP)

Tactics: Crow-Men are observers, not warriors. They will watch intruders from a distance. If bothered, they will use their Primal Weaving to harass with minor druidic spells (entangling vines, gusts of wind) before transforming into a crow swarm to escape. They are fiercely territorial but not inherently aggressive.

- Heresy (The Nothing That Is)
The fallen emperor of the Skazan, a howling wound in the world. Heresy is not a creature to be fought, but a force of nature to be survived. It appears as a tall, masked figure buzzing with flies, a being of pure, unmaking void. To attack it is to invite your own annihilation.

Total Entropy Pool (TEP): -500 EP (Acts as a positive value for all contests)

Attributes: All attributes are conceptually negative, granting it an overwhelming advantage in any contested check.

Abilities:

Aura of Dread: Creatures that start their turn within 120 feet of Heresy must succeed on a Wisdom check (TN 25) or be frightened.

Cannot Be Harmed: Heresy is "nothing." It is immune to all damage and effects. All attacks against it automatically miss.

Integration: If a creature attacks Heresy, it uses its reaction to integrate with the attacker. The attacker is instantly and irrevocably erased from existence. There is no save.

Tactics: Heresy is a pursuit predator. It does not run; it walks with a relentless, terrifying pace. It will lock onto a single target and pursue them for miles. The only goal is to escape. It is a narrative event, a chase, and a test of stamina, not a combat encounter.

## Civilized & Sapient Peoples
This section details the various sapient peoples who have built societies in the bottom realm, from the ancient natives to the immortal survivors and their mortal descendants. Each entry provides a brief description and a standard "Body Plan" template for character creation.

- Heresy, Minor
Half-truths and forgotten whispers given form, these enigmatic beings crew the quaint wooden cities that wander the wastes. They are flighty, speak in riddles, and value the tone of a conversation over its literal content. They are powerful allies if you can learn to dance to their tune.

Body Plan (Variable Cost): Heresies have no fixed form and can be built using any combination of body parts. They are often ethereal or strangely assembled.

- Village Commoner
The mortal descendants of the first immortal survivors. They live in established villages deep within the wastes, leading normal lives and dying of old age. They are wary of the "hunted," as their presence often brings the wrath of the Skazan Order down upon them.

Body Plan (18 EP): Standard Humanoid form.

- Lepi
The original natives of the plane, these moth-like people are hardy survivors and neutral arbiters in the conflicts of the realm. Their patterned wings are their pride, and their knowledge of the wastes is unparalleled. They are the only faction that treats openly with the Skazan.

Body Plan (20 EP):

Torso: 1 EP, Head: 1 EP, Arms (x2): 6 EP, Legs (x2): 6 EP, Wings (x2): 8 EP, Antennae Senses (x2): 2 EP

Max HP: 1 + floor(0.5 * (12 + 8)) = 11 HP

- Graff
Pangolin-armadillo hybrids, the Graff are hardy desert dwellers who loot ancient ruins. They are large, scaly, and can roll into a ball for both defense and high-speed travel.

Body Plan (23 EP):

Torso: 1 EP + 4 Size Entropy (Carapace), Head: 1 EP, Arms (x2): 6 EP, Legs (x2): 6 EP, Senses (x2): 2 EP, Utility Limb (Carapace): 4 EP

Max HP: 5 + floor(0.5 * 12) = 11 HP

- Boncit
Woodpecker-folk with a unique biological adaptation. They can strike with their heads and beaks with incredible force, using a specialized utility limb in their head for both offense and defense.

Body Plan (19 EP):

Torso: 1 EP, Arms (x2): 6 EP, Legs (x2): 6 EP, Senses (x2): 2 EP, Utility Limb (Reinforced Head/Beak): 4 EP

Max HP: 1 + floor(0.5 * 12) = 7 HP

- Saltician
Jumping spider-folk who are masters of explosive movement. They use all six of their limbs to launch themselves through the air. Some bloodlines are known to have a venomous bite.

Body Plan (26 EP):

Torso: 1 EP, Head: 1 EP, Standard Limbs (x6): 18 EP, Compound Eyes (x2): 2 EP, Utility Limb (Fangs, optional): 4 EP

Max HP: 1 + floor(0.5 * 18) = 10 HP

- Gage Mage
Elephant-folk of immense stature and intellect. They are often scholars and magi, though their physical power is not to be underestimated. A strange quirk of their biology sometimes causes the eldest among them to become unnaturally light.

Body Plan (20 EP):

Torso: 1 EP, Head: 1 EP, Arms (x2): 6 EP, Legs (x2): 6 EP, Senses (x2): 2 EP, Basic Limb (Trunk): 2 EP, Utility Limb (Tusks): 2 EP

Max HP: 1 + floor(0.5 * 16) = 9 HP

- Sha Reqa
Living elementals bound to a matrix of obsidian or other stone. Their "head" is a utility limb of pure, swirling energy, and their forms can be bizarre and asymmetrical. They are often graceful and unnervingly swift.

Body Plan (Variable Cost): Built from a Torso, a Head (Utility Limb, Pure Element), and any number of Standard or Basic Limbs made of stone.

- Chot
An empire of grasshopper-folk who dominate the dry wastes. They are a hive society, fiercely loyal to their queen-patrons. They ride massive katydids into battle and are known for their territorial raids.

Body Plan (22 EP):

Torso: 1 EP, Head: 1 EP, Arms (x2): 6 EP, Legs (x2 for jumping): 6 EP, Basic Limbs (x2 for stability): 4 EP, Senses (x2): 2 EP

Max HP: 1 + floor(0.5 * 16) = 9 HP

- Pindel
Small, impish beings with horns, wings, and a prehensile tail. Their skin is often brightly colored like a tropical bird, and some are known to be poisonous to the touch. They are mischievous and curious.

Body Plan (21 EP):

Torso: 1 EP, Head: 1 EP, Arms (x2): 6 EP, Legs (x2): 6 EP, Wings (x2): 8 EP, Basic Limb (Tail): 2 EP, Senses (x2): 2 EP

Max HP: 1 + floor(0.5 * (12 + 8 + 2)) = 12 HP

- Setabo
Poison-dart frog folk who are small, agile, and deadly. Their skin is coated in a toxic mucus, but this adaptation comes at a cost: they must remain hydrated, requiring regular bathing to survive.

Body Plan (18 EP):

Torso: 1 EP, Head: 1 EP, Arms (x2): 6 EP, Legs (x2): 6 EP, Senses (x2): 2 EP, Utility Limb (Poison Glands): 2 EP

Max HP: 1 + floor(0.5 * 12) = 7 HP

---

## TLE-017_gm_player_journey.md

---
#───────────── The Lost Eternal ──────────────────────
id: TLE-017
title: GM Player Journey
version: 1.0-consolidated
parents: [TLE-000]
children: []
engrams:
 - system:bestiary
 - mechanic:freeform-creation-system
 - templates:denizens
keywords: [character creation, body plan, attributes, TLE]
uncertainty_tag: Low
module_type: core-rulebook-consolidated
---
This guide provides a framework for the long-term progression of a campaign in "The Lost Eternal." It outlines the major story arcs that players can pursue and introduces a reputation system to mechanically track their standing within the complex social ecosystem of the bottom realm.

## 1 · Major Campaign Arcs: The Eight Paths
The bottom realm is a sandbox of possibilities. While the immediate goal is survival, the world is rich with deeper mysteries and grander objectives. The GM should subtly weave hints of these eight major paths into the campaign, allowing the players to choose their own destiny. A party may pursue one, several, or even all of these goals over the course of their journey.

The Enigma of Heresy: Uncover the true identity of the being known as Heresy. This path involves piecing together scattered journal entries, deciphering ancient Skazan lore, and confronting the tragic history of the fallen empire.

The Path of Return: Discover a way to reverse the Skazan's translocation ritual, escape the bottom realm, and break the curse of forgetfulness placed upon your loved ones. This is a quest for personal redemption and a return to a life that was stolen.

The Unseen War: Take the fight to the Skazan Order. This path is a shadow war of infiltration, counter-espionage, and assassination, where players must identify and eliminate the Skazan's secret agents embedded within the realm's factions before they can be "harvested."

Forging a New Home: Abandon the idea of escape and carve out a new life. This path is about building something permanent in the wastes—founding a new village, taking control of a walking city, and becoming a power in your own right.

The Unification: Bring an end to the endless conflicts between the walking cities. This is a grand-scale political and military campaign of diplomacy, sabotage, and alliance-building, with the goal of uniting the disparate factions against a common foe.

The Heresies' Peace: The minor Heresies are eternally hunted by the great Heresy. Discover a way to shield them from their pursuer. Success could be rewarded with passage to any other plane of existence or even the chance to transcend your mortal form.

The Endless Horizon: The world is vast and filled with forgotten wonders and horrors. This path is for the pure explorer—the treasure hunter who wishes to chart the unknown, from the frozen hulks in the fields of wildflowers to the wrecked Skazan ships in the mountains.

The Greater Cosmos: The bottom realm is but one battlefield in a larger cosmic war. This path involves leaving the starting plane to engage with the Skazan Empire on its own turf, navigating interstellar politics, and taking the fight to a truly galactic scale.

## §2 · Faction & Reputation System
A character's actions have consequences. Their standing with the major factions of the bottom realm is tracked on a simple scale from -5 (Hated) to +5 (Revered).

The Cities (e.g., The Endeavor)

Reputation: Gained by completing quests for city leaders, protecting trade routes, and upholding the law. Lost by committing crimes and associating with nomads.

+5 (Revered): You are a hero of the city. You are granted a permanent residence and a say in political matters.

-5 (Hated): You are exiled and hunted. A bounty is placed on your head, and city guards will attack you on sight.

The Nomad Camps

Reputation: Gained by trading fairly, sharing intelligence, and raiding city-aligned targets. Lost by betraying their trust or siding with city law.

+5 (Revered): You are considered one of their own. You are given access to their black markets, secret routes, and can call on them for aid.

-5 (Hated): You are a primary target. Nomad raiding parties will actively hunt you through the wastes.

The Lepi

Reputation: Gained only through acts of profound respect, fair trade, and by protecting their neutrality. Lost by acts of aggression, disrespect, or by trying to force them to break their neutrality.

+5 (Revered): You are a trusted friend. The Lepi will grant you safe passage through the most dangerous territories and may even share intelligence on the Skazan Order.

-5 (Hated): You are shunned. The Lepi will refuse to trade or speak with you, effectively cutting you off from the realm's most knowledgeable guides.

The Skazan Order (Threat Meter)

This is not a reputation, but a Threat Level, starting at 0 and increasing. It is raised by accumulating TEP, defeating their agents, and interfering with their plans.

Threat 1-5: Your handler watches from a distance, occasionally sending minor obstacles your way to "fatten you up."

Threat 6-10: Your handler begins to take a more active role, hiring bandits or manipulating beasts to test your limits.

Threat 11+: You are no longer just an investment; you are a problem. The Skazan will dispatch powerful, specialized agents with the sole purpose of harvesting you by any means necessary.

## §3 · Mass Combat: The Phalanx Clash
When large groups of combatants clash, the battle can be resolved through a streamlined system that captures the brutal calculus of war.

The Combined Pool: Each side totals the TEP of all participants to create a single, massive pool of entropic force.

The Multiplier: Each side rolls a die with a number of sides equal to its number of participants. This result becomes their damage multiplier for the round.

The Clash: Each side multiplies its combined TEP by its multiplier roll. The two totals are then subtracted from each other. The losing side suffers casualties equal to the difference in entropic force.

Resolving Casualties: The damage is assigned to the combatants on the front lines first, then moves towards the middle and back ranks. If a tie-breaker is needed for simultaneous losses, roll a d2; on the first non-tied result of 1, that individual perishes.

Example: The King's Regiment vs. The Caustic Fen

A regiment of 30 soldiers (15 Paladins, 15 Spearmen) is sent to destroy the Jellymancer's lair.

The King's Regiment: Let's assume an average TEP of 75 for each of the 30 soldiers. Their combined pool is 2,250 TEP.

The Caustic Fen: The Jellymancer has siphoned the heroes' TEP, adding it to his lair. The Lair now has a TEP of 3,000, and it is defended by 20 empowered Acidic Slime Minions with an average of 50 TEP each (1,000 TEP total). The Fen's combined pool is 4,000 TEP.

The Clash:

The Regiment has 30 participants, so they roll a d30. They get a 22. Their total force is 2,250 * 22 = 49,500.

The Fen has 21 participants (20 slimes + the Lair itself), so it rolls a d21. It gets a 15. Its total force is 4,000 * 15 = 60,000.

The Outcome:

The Fen's force (60,000) overpowers the Regiment's (49,500). The difference is 10,500.

This damage is dealt to the Regiment. 10,500 damage is enough to annihilate the entire force of 30 soldiers (10,500 / 75 TEP per soldier = 140 casualties, far more than are present).

Result: The king's regiment marches into the Caustic Fen and is utterly dissolved by a tidal wave of empowered, acidic sludge. The lair is victorious.

---

## TLE-ARC-001_the_juggernaut.md

---
#───────────── The Lost Eternal ──────────────────────
id: TLE-ARC-001
title: The Juggernaut
version: 1.0-consolidated
parents: [TLE-000]
children: []
engrams:
 - templates:juggernaut
keywords: [character creation, body plan, attributes, TLE]
uncertainty_tag: Low
module_type: core-rulebook-consolidated
---
Module TLE-ARC-001: The Juggernaut (Warrior Archetype)
This document outlines the level-by-level progression of a "Juggernaut"—a warrior archetype focused on pure physical dominance. The Juggernaut invests nearly all of its Entropy into its body and physical attributes, becoming a titan on the battlefield at the cost of mental and social acuity.

Progression Milestones:

Level 1: Total Entropy Pool (TEP) of 35 EP

Level 5: TEP of 95 EP (35 + 4x15)

Level 10: TEP of 170 EP (35 + 9x15)

Level 15: TEP of 245 EP (35 + 14x15)

Level 20: TEP of 335 EP (35 + 20x15, as per request)

Level 1: The Brawler (35 TEP)
At this stage, the Juggernaut is a tough, promising fighter, but still relatively balanced. They have invested in a solid physical foundation.

Attribute Investment (17 EP):

Strength: 6 EP

Dexterity: 4 EP

Constitution: 6 EP

Intelligence: 1 EP

Wisdom: 0 EP

Attribute Scores & Modifiers:

STR Score: 3 (Mod +0)

DEX Score: 2 (Mod +0)

CON Score: 3 (Mod +0)

INT Score: 0 (Mod +0)

WIS Score: 0 (Mod +0)

Physical Form (18 EP):

Humanoid, Standard template (18 EP)

Derived Max HP: 7 HP (1 from Torso + 6 from Limbs)

Remaining TEP: 0 EP

Level 5: The Veteran (95 TEP)
The Juggernaut has survived their first trials and has begun to specialize. Their focus on physical power is becoming apparent, with one arm designated as their primary weapon.

Attribute Investment (45 EP):

Strength: 20 EP

Dexterity: 10 EP

Constitution: 15 EP

Intelligence: 0 EP

Wisdom: 0 EP

Attribute Scores & Modifiers:

STR Score: 10 (Mod +2)

DEX Score: 5 (Mod +1)

CON Score: 7 (Mod +1)

INT Score: 0 (Mod +0)

WIS Score: 0 (Mod +0)

Physical Form (50 EP):

Torso: 1 EP

Head: 1 EP

Right Arm (Weapon): 3 EP (Base) + 20 Size Entropy = 23 EP

Left Arm (Shield): 3 EP

Legs (x2): 12 EP (6 EP each)

Senses (x4): 4 EP

Feats: 6 EP (e.g., Impact Absorption)

Derived Max HP: 1 + floor(0.5 * (23 + 3 + 12)) = 20 HP

Remaining TEP: 0 EP

Level 10: The Champion (170 TEP)
Halfway to legendary status, the Juggernaut is a true force on the battlefield. Their weapon arm is a massive, dedicated tool of destruction, and their resilience is formidable.

Attribute Investment (80 EP):

Strength: 40 EP

Dexterity: 10 EP

Constitution: 30 EP

Intelligence: 0 EP

Wisdom: 0 EP

Attribute Scores & Modifiers:

STR Score: 20 (Mod +5)

DEX Score: 5 (Mod +1)

CON Score: 15 (Mod +3)

INT Score: 0 (Mod +0)

WIS Score: 0 (Mod +0)

Physical Form (90 EP):

Torso: 1 EP + 10 Size Entropy = 11 EP

Head: 1 EP

Right Arm (Weapon): 3 EP (Base) + 50 Size Entropy = 53 EP

Left Arm (Shield): 3 EP

Legs (x2): 12 EP (6 EP each)

Senses (x4): 4 EP

Feats: 6 EP (e.g., Reckless Strike)

Derived Max HP: 11 + floor(0.5 * (53 + 3 + 12)) = 45 HP

Remaining TEP: 0 EP

Level 15: The Warlord (245 TEP)
The Juggernaut is now a walking engine of destruction. Their physical form is so heavily invested with Entropy that they are more akin to a force of nature than a mortal being.

Attribute Investment (105 EP):

Strength: 60 EP

Dexterity: 10 EP

Constitution: 35 EP

Intelligence: 0 EP

Wisdom: 0 EP

Attribute Scores & Modifiers:

STR Score: 30 (Mod +7)

DEX Score: 5 (Mod +1)

CON Score: 17 (Mod +4)

INT Score: 0 (Mod +0)

WIS Score: 0 (Mod +0)

Physical Form (140 EP):

Torso: 1 EP + 20 Size Entropy = 21 EP

Head: 1 EP

Right Arm (Weapon): 3 EP (Base) + 80 Size Entropy = 83 EP

Left Arm (Shield): 3 EP

Legs (x2): 22 EP (11 EP each)

Senses (x4): 4 EP

Feats: 6 EP

Derived Max HP: 21 + floor(0.5 * (83 + 3 + 22)) = 84 HP

Remaining TEP: 0 EP

Level 20: The Juggernaut (335 TEP)
This is the Juggernaut's final form. They are a legend, a being whose physical will can shatter armies and break fortifications. Their body is a perfectly honed weapon, a testament to a lifetime of singular, focused investment.

Attribute Investment (135 EP):

Strength: 80 EP

Dexterity: 10 EP

Constitution: 45 EP

Intelligence: 0 EP

Wisdom: 0 EP

Attribute Scores & Modifiers:

STR Score: 40 (Mod +10)

DEX Score: 5 (Mod +1)

CON Score: 22 (Mod +5)

INT Score: 0 (Mod +0)

WIS Score: 0 (Mod +0)

Physical Form (200 EP):

Torso: 1 EP + 30 Size Entropy = 31 EP

Head: 1 EP

Right Arm (Weapon): 3 EP (Base) + 120 Size Entropy = 123 EP

Left Arm (Shield): 3 EP

Legs (x2): 32 EP (16 EP each)

Senses (x4): 4 EP

Feats: 6 EP

Derived Max HP: 31 + floor(0.5 * (123 + 3 + 32)) = 110 HP

Remaining TEP: 0 EP

Level 20 Summary: Combat Strategy
The Level 20 Juggernaut is the ultimate physical combatant. Their strategy is one of overwhelming, decisive force.

The Alpha Strike: The Juggernaut's primary tactic is to end a fight before it truly begins. Their Right Arm has a Size Entropy pool of 120 EP. They can channel this entire pool into a single, devastating attack. Combined with their +10 STR Modifier, they can deliver a blow of unimaginable power. This single attack is often enough to obliterate all but the most powerful foes.

Sustained Carnage: A high CON Score of 22 gives the Juggernaut a massive Entropy Regeneration Rate (ERR). Even after delivering their alpha strike, they can quickly regenerate the EP needed for subsequent powerful attacks, allowing them to maintain pressure on the battlefield.

Unyielding Resilience: With 110 HP, the Juggernaut is incredibly durable. Their heavily invested Torso and limbs make them a fortress of flesh and bone, able to withstand blows that would fell lesser beings.

Weaknesses: The Juggernaut's singular focus is also its greatest weakness. With 0 EP invested in Intelligence and Wisdom, they have no modifiers for perception, social skills, or magical resistance. They are highly vulnerable to mind control, deception, and magical effects that target their will. Their path to victory is a straight line; they must close with the enemy and destroy them before their own vulnerabilities can be exploited.

---

## TLE-ARC-002_the_arcanist.md

---
#───────────── The Lost Eternal ──────────────────────
id: TLE-ARC-002
title: The Arcanist
version: 1.0-consolidated
parents: [TLE-000]
children: []
engrams:
 - templates:arcanist
keywords: [character creation, body plan, attributes, TLE]
uncertainty_tag: Low
module_type: core-rulebook-consolidated
---
Module TLE-ARC-002: The Arcanist (Mage Archetype)
This document outlines the level-by-level progression of an "Arcanist"—a mage archetype focused on mastering the raw power of Entropy. The Arcanist invests the vast majority of their potential into their mind and magical skills, becoming a devastating "glass cannon" on the battlefield at the expense of physical resilience.

Progression Milestones:

Level 1: Total Entropy Pool (TEP) of 35 EP

Level 5: TEP of 95 EP (35 + 4x15)

Level 10: TEP of 170 EP (35 + 9x15)

Level 15: TEP of 245 EP (35 + 14x15)

Level 20: TEP of 335 EP (35 + 19x15)

Level 1: The Acolyte (35 TEP)
The Acolyte has just begun their journey, prioritizing their connection to the flow of Entropy over a robust physical form.

Attribute Investment (25 EP):

Strength: 0 EP

Dexterity: 1 EP

Constitution: 4 EP

Intelligence: 12 EP

Wisdom: 8 EP

Attribute Scores & Modifiers:

STR Score: 0 (Mod +0)

DEX Score: 0 (Mod +0)

CON Score: 2 (Mod +0)

INT Score: 6 (Mod +1)

WIS Score: 4 (Mod +1)

Physical Form (10 EP):

Torso: 1 EP

Head: 1 EP

Limbs (x4): 4 EP (Minimalist form, 1 EP each)

Senses (x4): 4 EP

Derived Max HP: 3 HP (1 from Torso + 2 from Limbs)

Remaining TEP: 0 EP

Level 5: The Theurge (95 TEP)
The Theurge has unlocked their first Arcane Skill, channeling their will into a specific expression of magic. Their mind is their primary weapon and their body remains a secondary concern.

Attribute Investment (55 EP):

Strength: 0 EP

Dexterity: 5 EP

Constitution: 10 EP

Intelligence: 25 EP

Wisdom: 15 EP

Attribute Scores & Modifiers:

STR Score: 0 (Mod +0)

DEX Score: 2 (Mod +0)

CON Score: 5 (Mod +1)

INT Score: 12 (Mod +3)

WIS Score: 7 (Mod +1)

Physical Form & Skills (40 EP):

Humanoid, Standard form: 18 EP

Arcane Skill: "Expression of Frost": 3 EP (Permanent TEP cost)

"Expression of Frost" Pool: 19 EP

Derived Max HP: 7 HP (1 from Torso + 6 from Limbs)

Remaining TEP: 0 EP

Level 10: The Magus (170 TEP)
The Magus is a true magical practitioner, capable of unleashing significant power. They have begun to understand the deeper structures of Entropy, learning to weave their different pools of power together.

Attribute Investment (90 EP):

Strength: 0 EP

Dexterity: 10 EP

Constitution: 20 EP

Intelligence: 40 EP

Wisdom: 20 EP

Attribute Scores & Modifiers:

STR Score: 0 (Mod +0)

DEX Score: 5 (Mod +1)

CON Score: 10 (Mod +2)

INT Score: 20 (Mod +5)

WIS Score: 10 (Mod +2)

Physical Form & Skills (80 EP):

Humanoid, Standard form: 18 EP

Arcane Skill: "Expression of Frost": 3 EP

"Expression of Frost" Pool: 40 EP

Arcane Skill: "Abjuration" (Defensive Magic): 3 EP

"Abjuration" Pool: 6 EP

Feat: Entropic Font (10 EP): You can treat all of your Arcane Skill pools as a single, combined resource for the purposes of casting.

Derived Max HP: 7 HP

Remaining TEP: 0 EP

Level 15: The Archon (245 TEP)
The Archon is a master of their chosen element. Their mind is a razor, and their control over their Arcane Skills is profound. They are a formidable, if fragile, force.

Attribute Investment (140 EP):

Strength: 0 EP

Dexterity: 10 EP

Constitution: 30 EP

Intelligence: 65 EP

Wisdom: 35 EP

Attribute Scores & Modifiers:

STR Score: 0 (Mod +0)

DEX Score: 5 (Mod +1)

CON Score: 15 (Mod +3)

INT Score: 32 (Mod +8)

WIS Score: 17 (Mod +4)

Physical Form & Skills (105 EP):

Humanoid, Standard form: 18 EP

Arcane Skill: "Expression of Frost": 3 EP

"Expression of Frost" Pool: 60 EP

Arcane Skill: "Abjuration": 3 EP

"Abjuration" Pool: 11 EP

Feat: Entropic Font: 10 EP

Derived Max HP: 7 HP

Remaining TEP: 0 EP

Level 20: The Arcanist (335 TEP)
The Arcanist is a living conduit of magical power. They have sacrificed all but the most essential physical investment to achieve an unparalleled mastery of the mind and the flow of Entropy.

Attribute Investment (180 EP):

Strength: 0 EP

Dexterity: 10 EP

Constitution: 30 EP

Intelligence: 100 EP

Wisdom: 40 EP

Attribute Scores & Modifiers:

STR Score: 0 (Mod +0)

DEX Score: 5 (Mod +1)

CON Score: 15 (Mod +3)

INT Score: 50 (Mod +12)

WIS Score: 20 (Mod +5)

Physical Form & Skills (155 EP):

Torso: 1 EP + 4 Size Entropy = 5 EP

Head: 1 EP

Limbs (x4): 12 EP (3 EP each)

Senses (x4): 4 EP

Arcane Skill: "Expression of Frost": 3 EP

"Expression of Frost" Pool: 100 EP

Arcane Skill: "Abjuration": 3 EP

"Abjuration" Pool: 17 EP

Feat: Entropic Font: 10 EP

Derived Max HP: 5 + floor(0.5 * 12) = 11 HP

Remaining TEP: 0 EP

Level 20 Summary: Combat Strategy
The Level 20 Arcanist is the ultimate "glass cannon," a master of control and overwhelming magical force.

Overwhelming Power: The Arcanist's primary strength is their massive pool of arcane energy. With the Entropic Font feat, they have a combined pool of 117 EP dedicated to their magic. Their +12 INT Modifier allows them to control this power with incredible precision, making their spells both devastating and accurate.

Battlefield Control: An Arcanist specializing in "Expression of Frost" can reshape the battlefield. They can spend EP to create vast walls of ice (TLE-004), flash-freeze the ground to create difficult terrain, or encase enemies in prisons of ice, all while staying at a safe distance.

Calculated Defense: While physically fragile, the Arcanist is not defenseless. Their "Abjuration" skill allows them to spend EP on magical shields and wards, and their high WIS Modifier (+5) makes them resistant to mental and social attacks.

Weaknesses: With only 11 HP and a STR Score of 0, the Arcanist is exceptionally vulnerable to physical damage. Any enemy that can close the distance and bypass their magical defenses can neutralize them with a single, well-placed blow. Their strategy is entirely dependent on maintaining distance, controlling the flow of the battle, and eliminating threats before they can get close.

---

## TLE-ARC-003_the_phantom.md

---
#───────────── The Lost Eternal ──────────────────────
id: TLE-ARC-003
title: The Phantom
version: 1.0-consolidated
parents: [TLE-000]
children: []
engrams:
 - templates:phantom
keywords: [character creation, body plan, attributes, TLE]
uncertainty_tag: Low
module_type: core-rulebook-consolidated
---
Module TLE-ARC-003: The Phantom (Rogue Archetype)
This document outlines the level-by-level progression of a "Phantom"—a rogue archetype who masters the arts of stealth, skill, and precision. The Phantom is a balanced combatant who invests in Dexterity, Intelligence, and Wisdom, forgoing overwhelming power for tactical superiority and the ability to strike where the enemy is weakest.

Progression Milestones:

Level 1: Total Entropy Pool (TEP) of 35 EP

Level 5: TEP of 95 EP (35 + 4x15)

Level 10: TEP of 170 EP (35 + 9x15)

Level 15: TEP of 245 EP (35 + 14x15)

Level 20: TEP of 335 EP (35 + 19x15)

Level 1: The Urchin (35 TEP)
The Urchin is a survivor, relying on their wits and quick feet. Their Entropy is invested in a balanced, adaptable foundation.

Attribute Investment (17 EP):

Strength: 2 EP

Dexterity: 6 EP

Constitution: 3 EP

Intelligence: 4 EP

Wisdom: 2 EP

Attribute Scores & Modifiers:

STR Score: 1 (Mod +0)

DEX Score: 3 (Mod +0)

CON Score: 1 (Mod +0)

INT Score: 2 (Mod +0)

WIS Score: 1 (Mod +0)

Physical Form (18 EP):

Humanoid, Standard template (18 EP)

Derived Max HP: 7 HP (1 from Torso + 6 from Limbs)

Remaining TEP: 0 EP

Level 5: The Cutpurse (95 TEP)
The Cutpurse has honed their skills in the shadows. They've begun to invest in specialized abilities and have a clear focus on Dexterity and awareness.

Attribute Investment (57 EP):

Strength: 5 EP

Dexterity: 20 EP

Constitution: 10 EP

Intelligence: 12 EP

Wisdom: 10 EP

Attribute Scores & Modifiers:

STR Score: 2 (Mod +0)

DEX Score: 10 (Mod +2)

CON Score: 5 (Mod +1)

INT Score: 6 (Mod +1)

WIS Score: 5 (Mod +1)

Physical Form & Feats (38 EP):

Humanoid, Standard form: 18 EP

Feat: Entropic Stride (10 EP): Enhances movement efficiency.

Skill Pool: "Subterfuge": 10 EP (A dedicated pool for stealth, lockpicking, etc.)

Derived Max HP: 7 HP

Remaining TEP: 0 EP

Level 10: The Infiltrator (170 TEP)
The Infiltrator is a master of their craft, able to bypass defenses both physical and social. Their investment in mental attributes now rivals their physical prowess.

Attribute Investment (110 EP):

Strength: 10 EP

Dexterity: 40 EP

Constitution: 15 EP

Intelligence: 25 EP

Wisdom: 20 EP

Attribute Scores & Modifiers:

STR Score: 5 (Mod +1)

DEX Score: 20 (Mod +5)

CON Score: 7 (Mod +1)

INT Score: 12 (Mod +3)

WIS Score: 10 (Mod +2)

Physical Form & Feats (60 EP):

Humanoid, Standard form: 18 EP

Feat: Entropic Stride: 10 EP

Feat: Wound Channel Analyst (10 EP): You can spend an action and make an Intelligence check to identify a target's Wound Channels (narrative weaknesses). On a success, your next attack against that target that exploits the wound deals bonus damage equal to your INT modifier.

Skill Pool: "Subterfuge": 22 EP

Derived Max HP: 7 HP

Remaining TEP: 0 EP

Level 15: The Assassin (245 TEP)
The Assassin is a predator who dictates the terms of engagement. They are a blur of motion, a whisper in the dark, and a flash of steel.

Attribute Investment (165 EP):

Strength: 10 EP

Dexterity: 65 EP

Constitution: 20 EP

Intelligence: 40 EP

Wisdom: 30 EP

Attribute Scores & Modifiers:

STR Score: 5 (Mod +1)

DEX Score: 32 (Mod +8)

CON Score: 10 (Mod +2)

INT Score: 20 (Mod +5)

WIS Score: 15 (Mod +3)

Physical Form & Feats (80 EP):

Humanoid, Standard form: 18 EP

Feats: 20 EP (Entropic Stride, Wound Channel Analyst)

Skill Pool: "Subterfuge": 42 EP

Derived Max HP: 7 HP

Remaining TEP: 0 EP

Level 20: The Phantom (335 TEP)
The Phantom is a ghost, a rumor, a legend. They move through the world unseen, their will a subtle but irresistible force. They have achieved a perfect balance of physical grace, tactical genius, and intuitive insight.

Attribute Investment (225 EP):

Strength: 10 EP

Dexterity: 90 EP

Constitution: 25 EP

Intelligence: 60 EP

Wisdom: 40 EP

Attribute Scores & Modifiers:

STR Score: 5 (Mod +1)

DEX Score: 45 (Mod +11)

CON Score: 12 (Mod +3)

INT Score: 30 (Mod +7)

WIS Score: 20 (Mod +5)

Physical Form & Feats (110 EP):

Humanoid, Standard form: 18 EP

Feats: 20 EP (Entropic Stride, Wound Channel Analyst)

Skill Pool: "Subterfuge": 72 EP

Derived Max HP: 7 HP

Remaining TEP: 0 EP

Level 20 Summary: Combat Strategy
The Level 20 Phantom is a master of tactical combat, excelling at control, precision, and exploiting enemy weaknesses.

Supreme Skill: The Phantom's greatest asset is their versatility. With an enormous "Subterfuge" pool of 72 EP and high mental modifiers, they can overcome almost any non-combat challenge, from impossible locks to tense negotiations. Their +11 DEX Modifier makes them incredibly accurate and difficult to hit.

The Analyst's Strike: A Phantom's core combat loop is to first observe, then strike. Using their Wound Channel Analyst feat, they use their +7 INT Modifier to identify an enemy's narrative or physical weakness. Their next attack is a precision strike, often from stealth, that can cripple or eliminate a key target in a single blow.

Master of the Battlefield: Unlike the Juggernaut who plows through obstacles, or the Arcanist who reshapes the field with raw power, the Phantom uses the environment as it is. Their high DEX and WIS allow them to move unseen, create diversions, and use social stealth (TLE-009) to turn enemies against each other. They win by outthinking and outmaneuvering their opponents.

Weaknesses: While not as fragile as the Arcanist, the Phantom is not a front-line brawler. With only 7 HP and a low STR, they cannot withstand sustained, direct assault. Their strategy relies on avoiding fair fights, controlling the engagement, and ensuring that by the time the enemy knows they are there, the battle is already over.

---

## TLE-ARC-004_the_weaver.md

---
#───────────── The Lost Eternal ──────────────────────
id: TLE-ARC-004
title: The Weaver
version: 1.0-consolidated
parents: [TLE-000]
children: []
engrams:
 - templates:phantom
keywords: [character creation, body plan, attributes, TLE]
uncertainty_tag: Low
module_type: core-rulebook-consolidated
---
Module TLE-ARC-004: The Weaver (Support/Control Archetype)
This document outlines the level-by-level progression of a "Weaver"—a unique support and control archetype who manipulates the very fabric of being. The Weaver interacts with the Wound Channels of allies and enemies, capable of mending the deepest scars or turning an opponent's own trauma into a devastating weapon. Their power is subtle, terrifying, and deeply tied to the narrative of the world.

Progression Milestones:

Level 1: Total Entropy Pool (TEP) of 35 EP

Level 5: TEP of 95 EP (35 + 4x15)

Level 10: TEP of 170 EP (35 + 9x15)

Level 15: TEP of 245 EP (35 + 14x15)

Level 20: TEP of 335 EP (35 + 19x15)

Level 1: The Empath (35 TEP)
The Empath is a being attuned to the echoes of the past. They can feel the resonant scars left on others, though their ability to manipulate them is still nascent.

Attribute Investment (21 EP):

Strength: 0 EP

Dexterity: 2 EP

Constitution: 6 EP

Intelligence: 5 EP

Wisdom: 8 EP

Attribute Scores & Modifiers:

STR Score: 0 (Mod +0)

DEX Score: 1 (Mod +0)

CON Score: 3 (Mod +0)

INT Score: 2 (Mod +0)

WIS Score: 4 (Mod +1)

Physical Form & Skills (14 EP):

Humanoid, Standard form: 18 EP (Requires taking 4 EP from Attributes, leaving 17 EP for investment)

Arcane Skill: "The Weaver's Art": 3 EP (Permanent TEP cost)

"The Weaver's Art" Pool: 10 EP

Derived Max HP: 7 HP

Remaining TEP: 0 EP (after reallocating from Attributes)

Level 5: The Stitcher (95 TEP)
The Stitcher has learned the basics of their craft. They can mend minor wounds and have begun to understand the offensive potential of their art.

Attribute Investment (55 EP):

Strength: 0 EP

Dexterity: 5 EP

Constitution: 15 EP

Intelligence: 15 EP

Wisdom: 20 EP

Attribute Scores & Modifiers:

STR Score: 0 (Mod +0)

DEX Score: 2 (Mod +0)

CON Score: 7 (Mod +1)

INT Score: 7 (Mod +1)

WIS Score: 10 (Mod +2)

Physical Form & Skills (40 EP):

Humanoid, Standard form: 18 EP

Arcane Skill: "The Weaver's Art": 3 EP

"The Weaver's Art" Pool: 9 EP

Feat: Psychic Suture (10 EP): As an action, you can spend EP from your "Weaver's Art" pool to heal an ally's Wound Channel. The EP cost is determined by the GM based on the severity of the wound.

Derived Max HP: 7 HP

Remaining TEP: 0 EP

Level 10: The Mender (170 TEP)
The Mender is a true master of healing, capable of knitting flesh and soul back together. They have also learned to turn their art outward, weaponizing the pain of their enemies.

Attribute Investment (90 EP):

Strength: 0 EP

Dexterity: 10 EP

Constitution: 20 EP

Intelligence: 25 EP

Wisdom: 35 EP

Attribute Scores & Modifiers:

STR Score: 0 (Mod +0)

DEX Score: 5 (Mod +1)

CON Score: 10 (Mod +2)

INT Score: 12 (Mod +3)

WIS Score: 17 (Mod +4)

Physical Form & Skills (80 EP):

Humanoid, Standard form: 18 EP

Arcane Skill: "The Weaver's Art": 3 EP

"The Weaver's Art" Pool: 39 EP

Feat: Psychic Suture: 10 EP

Feat: Resonant Agony (10 EP): As an action, you can make a contested (d20 + WIS Mod) check against an enemy's (d20 + WIS Mod). On a success, you resonate with one of their Wound Channels. You can then spend EP from your "Weaver's Art" pool to deal an equal amount of psychic damage to them, bypassing physical defenses.

Derived Max HP: 7 HP

Remaining TEP: 0 EP

Level 15: The Fate-Spinner (245 TEP)
The Fate-Spinner sees the threads of causality that bind all beings. They can not only mend or break these threads but can begin to unravel the very form of their foes.

Attribute Investment (140 EP):

Strength: 0 EP

Dexterity: 10 EP

Constitution: 30 EP

Intelligence: 40 EP

Wisdom: 60 EP

Attribute Scores & Modifiers:

STR Score: 0 (Mod +0)

DEX Score: 5 (Mod +1)

CON Score: 15 (Mod +3)

INT Score: 20 (Mod +5)

WIS Score: 30 (Mod +7)

Physical Form & Skills (105 EP):

Humanoid, Standard form: 18 EP

Arcane Skill: "The Weaver's Art": 3 EP

"The Weaver's Art" Pool: 54 EP

Feats: 30 EP (Psychic Suture, Resonant Agony, and a new one)

Feat: Pattern Unraveling (10 EP): When you successfully use Resonant Agony, you can choose to deal half damage. If you do, you also "unravel" the target's form, temporarily removing an equal amount of EP from one of their invested limbs (your choice). This EP is returned at the end of the encounter.

Derived Max HP: 7 HP

Remaining TEP: 0 EP

Level 20: The Weaver (335 TEP)
The Weaver is a master of the entropic form. They perceive the world as a tapestry of will and memory, and they possess the needle and thread to re-weave it as they see fit. They are a legendary healer and a terrifying, unseen foe.

Attribute Investment (180 EP):

Strength: 0 EP

Dexterity: 10 EP

Constitution: 40 EP

Intelligence: 60 EP

Wisdom: 70 EP

Attribute Scores & Modifiers:

STR Score: 0 (Mod +0)

DEX Score: 5 (Mod +1)

CON Score: 20 (Mod +5)

INT Score: 30 (Mod +7)

WIS Score: 35 (Mod +8)

Physical Form & Skills (155 EP):

Humanoid, Standard form: 18 EP

Arcane Skill: "The Weaver's Art": 3 EP

"The Weaver's Art" Pool: 94 EP

Feats: 40 EP (Psychic Suture, Resonant Agony, Pattern Unraveling, and a new capstone feat)

Feat: Sever the Thread (10 EP): Once per long rest, when you use Pattern Unraveling, you can choose to make the entropic damage permanent. The target permanently loses the EP from their invested limb. This is a profound and often evil act, scarring the target's very soul.

Derived Max HP: 7 HP

Remaining TEP: 0 EP

Level 20 Summary: Combat Strategy
The Level 20 Weaver is a master of unconventional warfare, a "scary healer" who wins battles by manipulating the very essence of their allies and enemies.

The Ultimate Support: With a massive "Weaver's Art" pool of 94 EP and their Psychic Suture feat, a Weaver can perform incredible acts of healing. They can mend deep, narrative wounds that are beyond the reach of normal magic, making their allies incredibly resilient.

The Psychic Terror: The Weaver's offensive power is insidious and terrifying. Their primary tactic is to use Resonant Agony, bypassing all physical armor and defenses to inflict pure psychic damage. They don't attack the body; they attack the soul.

The Unraveler: Against a powerful, singular foe, the Weaver is a nightmare. They will use Pattern Unraveling to systematically dismantle their opponent. By temporarily (or permanently, with Sever the Thread) removing the EP invested in an enemy's limbs, they can render a Juggernaut's mighty arm useless or a dragon's fiery breath inert, winning the fight through slow, entropic decay.

Weaknesses: Like the Arcanist, the Weaver is physically fragile with only 7 HP. They must rely on their allies to protect them. Furthermore, their most powerful abilities require them to win a contested Wisdom check, making them less effective against foes with immense willpower or those who lack the complexity to have deep-seated Wound Channels (like a mindless golem). Their power is subtle and requires a keen tactical mind to use effectively.

---

## TLE-ARC-005_the_sentinel.md

---
#───────────── The Lost Eternal ──────────────────────
id: TLE-ARC-005
title: The Sentinel
version: 1.0-consolidated
parents: [TLE-000]
children: []
engrams:
 - templates:Sentinel
keywords: [character creation, body plan, attributes, TLE]
uncertainty_tag: Low
module_type: core-rulebook-consolidated
---
Module TLE-ARC-005: The Sentinel (Defender/Guardian Archetype)
This document outlines the level-by-level progression of a "Sentinel"—a defensive paragon who embodies the principle of the unbreakable shield. The Sentinel invests their Entropy into creating a form of supreme resilience, learning to generate and reinforce "Shells" of coherence to protect themselves and their allies. They are the immovable object, the eye of the storm, and the guardian at the gate.

Progression Milestones:

Level 1: Total Entropy Pool (TEP) of 35 EP

Level 5: TEP of 95 EP (35 + 4x15)

Level 10: TEP of 170 EP (35 + 9x15)

Level 15: TEP of 245 EP (35 + 14x15)

Level 20: TEP of 335 EP (35 + 19x15)

Level 1: The Guardian (35 TEP)
The Guardian is built for resilience from the very beginning. They are sturdy and watchful, with a natural inclination to protect.

Attribute Investment (17 EP):

Strength: 6 EP

Dexterity: 2 EP

Constitution: 8 EP

Intelligence: 0 EP

Wisdom: 1 EP

Attribute Scores & Modifiers:

STR Score: 3 (Mod +0)

DEX Score: 1 (Mod +0)

CON Score: 4 (Mod +1)

INT Score: 0 (Mod +0)

WIS Score: 0 (Mod +0)

Physical Form (18 EP):

Humanoid, Standard template (18 EP)

Derived Max HP: 7 HP (1 from Torso + 6 from Limbs)

Remaining TEP: 0 EP

Level 5: The Shieldwarden (95 TEP)
The Shieldwarden has learned that their own body is their greatest shield. They begin to invest heavily in their physical form, making it a bulwark against harm.

Attribute Investment (45 EP):

Strength: 15 EP

Dexterity: 5 EP

Constitution: 20 EP

Intelligence: 0 EP

Wisdom: 5 EP

Attribute Scores & Modifiers:

STR Score: 7 (Mod +1)

DEX Score: 2 (Mod +0)

CON Score: 10 (Mod +2)

INT Score: 0 (Mod +0)

WIS Score: 2 (Mod +0)

Physical Form & Feats (50 EP):

Torso: 1 EP + 10 Size Entropy = 11 EP

Head: 1 EP

Arms (x2): 10 EP (5 EP each)

Legs (x2): 10 EP (5 EP each)

Senses (x4): 4 EP

Feat: Interposing Shell (10 EP): As a reaction, when an ally within 5 feet of you is attacked, you can become the target of that attack instead.

Derived Max HP: 11 + floor(0.5 * (10 + 10)) = 21 HP

Remaining TEP: 0 EP

Level 10: The Bastion (170 TEP)
The Bastion is a living fortress. Their defensive capabilities are now proactive, allowing them to shape the battlefield and create zones of safety.

Attribute Investment (80 EP):

Strength: 30 EP

Dexterity: 5 EP

Constitution: 40 EP

Intelligence: 0 EP

Wisdom: 5 EP

Attribute Scores & Modifiers:

STR Score: 15 (Mod +3)

DEX Score: 2 (Mod +0)

CON Score: 20 (Mod +5)

INT Score: 0 (Mod +0)

WIS Score: 2 (Mod +0)

Physical Form & Skills (90 EP):

Torso: 1 EP + 25 Size Entropy = 26 EP

Head: 1 EP

Limbs (x4): 20 EP (5 EP each)

Senses (x4): 4 EP

Arcane Skill: "Shell Weaving": 3 EP

"Shell Weaving" Pool: 16 EP

Feats: 20 EP (Interposing Shell, and a new one)

Feat: Resonant Barricade (10 EP): You can spend EP from your "Shell Weaving" pool to create a 5-foot wide, 1-inch thick wall of force. The wall has HP equal to the EP spent.

Derived Max HP: 26 + floor(0.5 * 20) = 36 HP

Remaining TEP: 0 EP

Level 15: The Aegis (245 TEP)
The Aegis is a symbol of hope and defiance. Their ability to absorb punishment is legendary, and their protective presence can turn the tide of any battle.

Attribute Investment (115 EP):

Strength: 45 EP

Dexterity: 5 EP

Constitution: 60 EP

Intelligence: 0 EP

Wisdom: 5 EP

Attribute Scores & Modifiers:

STR Score: 22 (Mod +5)

DEX Score: 2 (Mod +0)

CON Score: 30 (Mod +7)

INT Score: 0 (Mod +0)

WIS Score: 2 (Mod +0)

Physical Form & Skills (130 EP):

Torso: 1 EP + 40 Size Entropy = 41 EP

Head: 1 EP

Limbs (x4): 40 EP (10 EP each)

Senses (x4): 4 EP

Arcane Skill: "Shell Weaving": 3 EP

"Shell Weaving" Pool: 21 EP

Feats: 20 EP (Interposing Shell, Resonant Barricade)

Derived Max HP: 41 + floor(0.5 * 40) = 61 HP

Remaining TEP: 0 EP

Level 20: The Sentinel (335 TEP)
The Sentinel is an absolute. They are the final bastion, the unbreakable wall against which the forces of chaos shatter. Their will is so focused on protection that they can manifest a perfect, impenetrable shell of pure coherence.

Attribute Investment (145 EP):

Strength: 60 EP

Dexterity: 5 EP

Constitution: 70 EP

Intelligence: 0 EP

Wisdom: 10 EP

Attribute Scores & Modifiers:

STR Score: 30 (Mod +7)

DEX Score: 2 (Mod +0)

CON Score: 35 (Mod +8)

INT Score: 0 (Mod +0)

WIS Score: 5 (Mod +1)

Physical Form & Skills (190 EP):

Torso: 1 EP + 60 Size Entropy = 61 EP

Head: 1 EP

Limbs (x4): 60 EP (15 EP each)

Senses (x4): 4 EP

Arcane Skill: "Shell Weaving": 3 EP

"Shell Weaving" Pool: 31 EP

Feats: 30 EP (Interposing Shell, Resonant Barricade, and a new capstone feat)

Feat: Aegis of Coherence (10 EP): Once per long rest, you can spend an action and 20 EP from your "Shell Weaving" pool to create a 15-foot radius sphere of absolute protection centered on yourself. The sphere is immobile and lasts for a number of rounds equal to your CON modifier. Nothing can pass through the sphere's boundary in either direction.

Derived Max HP: 61 + floor(0.5 * 60) = 91 HP

Remaining TEP: 0 EP

Level 20 Summary: Combat Strategy
The Level 20 Sentinel is the ultimate battlefield controller and protector. Their strategy is to become the anchor around which their party operates, an unbreakable fortress that dictates the flow of battle.

The Unbreakable Wall: With a massive 91 HP and a CON Score of 35, the Sentinel is a titan of resilience. Their high Entropy Regeneration Rate (ERR) allows them to constantly replenish the EP needed for their defensive abilities. They are designed to absorb incredible amounts of punishment and keep fighting.

Master of Control: The Sentinel's power lies in denying the enemy their objectives. Using Interposing Shell, they can redirect critical attacks away from fragile allies. With Resonant Barricade, they can reshape the battlefield, creating chokepoints and protecting key positions.

The Final Bastion: The Sentinel's capstone ability, Aegis of Coherence, is a game-changer. It can be used to provide a moment of absolute safety for the party to regroup and heal, to protect a vital objective, or to trap a powerful enemy in a cage of pure will.

Weaknesses: The Sentinel's immense defensive power comes at the cost of mobility and offensive output. With a low DEX, they are often the last to act in a turn. Their attacks, while respectable due to a high STR, lack the overwhelming force of a Juggernaut. Their greatest challenge is against highly mobile enemies who can bypass their control zones or enemies who can win through attrition, as the Sentinel's primary role is to outlast, not to out-damage.

---

## TLE-ARC-006_the_drifter.md

---
#───────────── The Lost Eternal ──────────────────────
id: TLE-ARC-005
title: The Drifter
version: 1.0-consolidated
parents: [TLE-000]
children: []
engrams:
 - templates:drifter
keywords: [character creation, body plan, attributes, TLE]
uncertainty_tag: Low
module_type: core-rulebook-consolidated
---
Module TLE-ARC-006: The Drifter (Chaos/Skirmisher Archetype)
This document outlines the level-by-level progression of a "Drifter"—a chaos-attuned skirmisher who thrives in the heart of battle's unpredictability. The Drifter doesn't resist the storm; they become it. They invest their Entropy in agility, intuition, and the ability to harness the raw, chaotic energy of "Spasm" and "Fracture" dynamics. They are a whirlwind of motion, an agent of disruption, and a master of surviving the impossible.

Progression Milestones:

Level 1: Total Entropy Pool (TEP) of 35 EP

Level 5: TEP of 95 EP (35 + 4x15)

Level 10: TEP of 170 EP (35 + 9x15)

Level 15: TEP of 245 EP (35 + 14x15)

Level 20: TEP of 335 EP (35 + 19x15)

Level 1: The Wanderer (35 TEP)
The Wanderer is a survivor, accustomed to instability and always on the move. They are nimble and perceptive, but lack physical resilience.

Attribute Investment (17 EP):

Strength: 2 EP

Dexterity: 8 EP

Constitution: 2 EP

Intelligence: 1 EP

Wisdom: 4 EP

Attribute Scores & Modifiers:

STR Score: 1 (Mod +0)

DEX Score: 4 (Mod +1)

CON Score: 1 (Mod +0)

INT Score: 0 (Mod +0)

WIS Score: 2 (Mod +0)

Physical Form (18 EP):

Humanoid, Standard template (18 EP)

Derived Max HP: 7 HP (1 from Torso + 6 from Limbs)

Remaining TEP: 0 EP

Level 5: The Storm-Chaser (95 TEP)
The Storm-Chaser has learned to feel the currents of chaos in the world. They begin to harness this energy, turning unpredictability into a weapon.

Attribute Investment (55 EP):

Strength: 5 EP

Dexterity: 25 EP

Constitution: 5 EP

Intelligence: 5 EP

Wisdom: 15 EP

Attribute Scores & Modifiers:

STR Score: 2 (Mod +0)

DEX Score: 12 (Mod +3)

CON Score: 2 (Mod +0)

INT Score: 2 (Mod +0)

WIS Score: 7 (Mod +1)

Physical Form & Skills (40 EP):

Humanoid, Standard form: 18 EP

Arcane Skill: "Chaos Weaving": 3 EP

"Chaos Weaving" Pool: 9 EP

Feat: Entropic Stride (10 EP): Enhances movement efficiency.

Derived Max HP: 7 HP

Remaining TEP: 0 EP

Level 10: The Anarch (170 TEP)
The Anarch is no longer just a follower of chaos; they are a source of it. They can create small, controlled disruptions to sow confusion and create openings.

Attribute Investment (95 EP):

Strength: 5 EP

Dexterity: 45 EP

Constitution: 10 EP

Intelligence: 10 EP

Wisdom: 25 EP

Attribute Scores & Modifiers:

STR Score: 2 (Mod +0)

DEX Score: 22 (Mod +5)

CON Score: 5 (Mod +1)

INT Score: 5 (Mod +1)

WIS Score: 12 (Mod +3)

Physical Form & Skills (75 EP):

Humanoid, Standard form: 18 EP

Arcane Skill: "Chaos Weaving": 3 EP

"Chaos Weaving" Pool: 34 EP

Feats: 20 EP (Entropic Stride, and a new one)

Feat: Controlled Spasm (10 EP): As an action, you can spend EP from your "Chaos Weaving" pool to create a minor chaotic event in a 5-foot square within 30 feet. The event has an EP value equal to what you spent. You can choose the effect from a small list (e.g., a sudden gust of wind, a distracting flash of light, a patch of slick ice).

Derived Max HP: 7 HP

Remaining TEP: 0 EP

Level 15: The Maelstrom (245 TEP)
The Maelstrom is a whirlwind on the battlefield. Their movements are a blur, and their presence unravels the enemy's plans through constant, unpredictable disruption.

Attribute Investment (140 EP):

Strength: 5 EP

Dexterity: 70 EP

Constitution: 15 EP

Intelligence: 15 EP

Wisdom: 35 EP

Attribute Scores & Modifiers:

STR Score: 2 (Mod +0)

DEX Score: 35 (Mod +8)

CON Score: 7 (Mod +1)

INT Score: 7 (Mod +1)

WIS Score: 17 (Mod +4)

Physical Form & Skills (105 EP):

Humanoid, Standard form: 18 EP

Arcane Skill: "Chaos Weaving": 3 EP

"Chaos Weaving" Pool: 64 EP

Feats: 20 EP (Entropic Stride, Controlled Spasm)

Derived Max HP: 7 HP

Remaining TEP: 0 EP

Level 20: The Drifter (335 TEP)
The Drifter is a being in perfect resonance with the chaotic nature of the world. They do not see the storm; they are the eye of it. They move with impossible grace, their actions a cascade of cause and effect that leaves order in tatters.

Attribute Investment (190 EP):

Strength: 5 EP

Dexterity: 90 EP

Constitution: 20 EP

Intelligence: 25 EP

Wisdom: 50 EP

Attribute Scores & Modifiers:

STR Score: 2 (Mod +0)

DEX Score: 45 (Mod +11)

CON Score: 10 (Mod +2)

INT Score: 12 (Mod +3)

WIS Score: 25 (Mod +6)

Physical Form & Skills (145 EP):

Humanoid, Standard form: 18 EP

Arcane Skill: "Chaos Weaving": 3 EP

"Chaos Weaving" Pool: 94 EP

Feats: 30 EP (Entropic Stride, Controlled Spasm, and a new capstone feat)

Feat: Ride the Fracture (10 EP): Once per long rest, when a significant chaotic event occurs on the battlefield (a massive critical hit, a wall is destroyed, a powerful spell misfires), you can use your reaction to "ride the fracture." You may immediately teleport to any unoccupied square on the battlefield and take one additional action.

Derived Max HP: 7 HP

Remaining TEP: 0 EP

Level 20 Summary: Combat Strategy
The Level 20 Drifter is the ultimate skirmisher and agent of chaos. Their strategy revolves around mobility, disruption, and exploiting the unpredictable nature of combat to their advantage.

Unmatched Agility: With a DEX Score of 45 (Mod +11) and the Entropic Stride feat, the Drifter's movement is a blur. They can traverse the battlefield with incredible speed and efficiency, making them almost impossible to pin down.

The Chaos Agent: The Drifter's primary tool is their "Chaos Weaving" pool of 94 EP. They use Controlled Spasm to constantly harass and disrupt the enemy, creating environmental hazards, breaking lines of sight, and forcing opponents into disadvantageous positions. They don't win by dealing damage, but by making it impossible for the enemy to fight effectively.

The Opportunist: The Drifter's capstone ability, Ride the Fracture, defines their playstyle. They are constantly watching for the moment a plan goes wrong. When an ally lands a massive critical hit or an enemy's spell goes awry, the Drifter is there in an instant to capitalize on the chaos, turning a single moment of fortune into a decisive, battle-winning advantage.

Weaknesses: The Drifter's greatest weakness is their fragility. With a mere 7 HP and a low CON, they cannot afford to be hit. Their entire strategy is built around not being where the enemy expects them to be. They are vulnerable to area-of-effect attacks that they can't dodge and to highly perceptive enemies who can predict their unpredictable movements. They are a high-risk, high-reward character who lives on a razor's edge.

---

