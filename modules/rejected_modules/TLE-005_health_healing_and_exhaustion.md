---
#───────────── The Lost Eternal ──────────────────────
id:        TLE-005
title:     Health, Healing, and Exhaustion
version:   1.0-draft
parents:   [TLE-004]
children:  [All future TLE modules related to survival and advanced combat]
engrams:
 - mechanic:entropic-health
 - mechanic:active-defense
 - system:healing-and-recovery
 - system:exhaustion
keywords:  [health, hit points, healing, injury, exhaustion, defense, TLE]
uncertainty_tag: Low
module_type: core-mechanic-expansion
---
## §1 · Preamble: The Entropy of Form
An entity's physical health is the most direct measure of its coherent integrity. It is not a passive score, but an active, entropic pool that represents the will required to hold one's form together against the pressures of a chaotic world. This module details the nature of this entropic health, the mechanics of active defense, and the slow, deliberate processes of healing and recovery.

## §2 · Health as an Entropic Pool
An entity's Hit Points (HP) are not a measure of flesh and blood, but a direct representation of the Entropy Points (EP) they have invested in their physical being. This is their Health Pool.

### 2.1 · Calculating the Health Pool
An entity's maximum HP is calculated from the EP they have allocated to their physical form.

Max HP = (EP in Torso) + (0.5 * Total EP in all Limbs)

### 2.2 · Damage & Unconsciousness
Damage from any source is subtracted directly from an entity's current Health Pool (their current HP).

Unconsciousness: When an entity's HP is reduced to 0, they fall unconscious.

Death: If an entity takes further damage while unconscious, their HP becomes negative. If their negative HP total exceeds one-quarter of their maximum HP, they die.

Total Destruction: If an entity's negative HP total becomes equal to or greater than their (Max HP + Total EP cost of all Body Parts), their form is utterly annihilated.

## §3 · Active Defense: The Contest of Wills (Revised)
Combat in The Lost Eternal is not a simple exchange of blows. Every attack is a projection of will that can be met with a counter-projection of will.

Mechanic: When an entity is targeted by an attack, they may use their reaction to actively defend. The defender spends EP to create a shield, ward, or parry.

Resolution: The amount of EP spent by the attacker is compared to the amount of EP spent by the defender.

If Defender EP ≥ Attacker EP, the attack is completely nullified.

If Attacker EP > Defender EP, the difference is applied as damage directly to the defender's Health Pool.
Damage = Attacker EP - Defender EP

### 3.1 · Coherence Strain
Defending against an overwhelmingly powerful blow strains an entity's very being.

Rule: Actively defending against an attack with an entropic force greater than your Constitution Score costs 1 additional EP for every point of difference.

Example: An entity with a CON Score of 20 can block a 20 EP attack for 20 EP. To block a 30 EP attack, it would cost them 30 + (30 - 20) = 40 EP.

### 3.2 · Critical Hits
A perfectly channeled entropic strike can find a fatal weakness, regardless of the defender's power.

Rule: When rolling for damage (e.g., 1d10), if the die roll is the maximum possible result (a 10 on a 1d10), it is a Critical Hit. The attacker immediately rolls the same damage die again and adds the result to the total. This can continue indefinitely if the attacker keeps rolling the maximum result.

Example: An attacker spends 10 EP for a 1d10 damage attack. They roll a 10. They roll again and get a 7. The total entropic force of the attack is 17. The defender must now spend 17 EP to block it.

## §4 · Healing: The Slow Art of Mending
Healing is the process of restoring lost entropy to a damaged Health Pool. It is a deliberate and costly act, whether performed by oneself or another.

### 4.1 · Magical & Alchemical Healing
Healing another being is a direct transfer of entropy.

Cost: To restore 1 HP to a target, a healer must spend 2 EP. One point is transferred to the target, and one is consumed by the act of transfer itself.

Sacrificial Healing: A healer can choose to transfer their own life force directly. They can restore a target's HP on a 1-to-1 basis by spending their own HP. This does not cost additional EP, but it can render the healer unconscious if they are not careful.

### 4.2 · Natural Healing (Resting)
Natural recovery is a slow, background process that follows the same rules as crafting. Every point of HP has an Entropy Budget that must be "paid off" by the body's natural regeneration.

HP Budget: The Entropy Budget to naturally heal 1 HP is 2,500 EP.

Process: When an entity is resting (engaging in no strenuous activity), their Entropy Regeneration Rate (ERR) is passively applied to this budget.

Example: An entity with an ERR of 6, resting for one hour (600 rounds), would passively generate 600 * 6 = 3,600 EP. This would be enough to pay off the budget for 1 HP (3600 - 2500 = 1100 remaining), with the remainder applied to the next point of damage.

## §5 · Exhaustion: The Fading Spark
All living things require rest to maintain their connection to the flow of entropy. Pushing beyond these limits has severe consequences.

Mechanic: For each consecutive 24-hour period an entity goes without a long rest (or equivalent sleep), their Entropy Regeneration Rate (ERR) is halved (rounded down).

Unconsciousness: If an entity's ERR drops below 1, they immediately fall unconscious and cannot be awakened by normal means until they have completed a long rest.

Example: A character with an ERR of 10:

Day 1 (no sleep): ERR becomes 5.

Day 2 (no sleep): ERR becomes 2.

Day 3 (no sleep): ERR becomes 1.

Day 4 (no sleep): ERR becomes 0. The character falls unconscious.