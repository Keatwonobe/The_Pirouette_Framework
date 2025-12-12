# TLE Combat Runner v3.2 - UPDATED REFERENCE CARD

## 🆕 NEW FEATURES

### ✨ Preflight Setup Phase
After loading codex and typing `init`, you enter **preflight mode** to configure the battlefield before combat starts.

```bash
# Preflight commands (range support!)
side 27-31 players        # Move chars 27-31 to players side
ai off 5-10               # Disable AI for chars 5-10
hostility 1-5 neutral     # Set chars 1-5 to neutral
stance 15-20 combat       # Set chars 15-20 to combat stance
look                      # View all characters
start / go                # Begin combat!
```

### ⚡ Player Reaction System
When a player character is hit, combat **pauses** for a reaction decision:

```
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  REACTION MOMENT: Keaton
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  Attacker: Raider_Grunt
  Incoming: 12 physical damage
  Your HP: 25/30
  Your EP: 18/20

Choose your reaction:
  1) TAKE IT - Accept full damage
  2) BLOCK - Spend EP to reduce (1 EP = -1 DMG, dice buy ok!)
  3) DODGE - DEX check vs DC 12

Enter: 1, 2, or 3
```

**Reaction Options:**
```bash
1                    # Take full damage
block 8              # Spend 8 EP (reduces by 8)
block 5 buy 3        # Spend 5 EP + 3 EP dice buy
dodge                # Roll DEX vs DC 12
```

---

## 📋 COMPLETE WORKFLOW

### Session Startup
```bash
# 1. Generate codex (one time)
python generate_codex.py

# 2. Open HTML
open tle_combat_runner.html
# → Auto-loads all 35 characters

# 3. Enter preflight
>> init

═══ PREFLIGHT SETUP ═══
Commands: start, look, ai, side, hostility, stance

# 4. Configure battlefield
>> look
[1] Keaton | players | HP 30/30
[2-16] Guards...
[17-31] Raiders...

>> ai off 2-5           # Manual control guards 2-5
>> side 27-31 players   # Move raiders 27-31 to players
>> hostility 6-10 neutral

# 5. Start combat
>> start

═══ INITIALIZING COMBAT ═══
Initiative Order:
  [1] Raider_Mage (Init: 18)
  ...
```

---

## 🎮 COMBAT FLOW WITH REACTIONS

### NPC attacks Player
```
[AI] Raider_Grunt attacking Keaton (spend 10, buy 2)
Dice Buy: 1d4-1 = [3]-1 = 2
Raw Damage: 7

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  REACTION MOMENT: Keaton
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  Incoming: 7 physical damage

>> block 5
Keaton BLOCKS with 5 total!
Damage reduced: 7 → 2
Keaton takes 2 physical damage (28/30 HP)

[AI Turn continues to next...]
```

### Player attacks NPC (no reaction)
```
>> attack 5 spend 8 buy 2
Keaton attacks Raider_Grunt!
  Dice Buy: 1d4-1 = [2]-1 = 1
  Total: 5 damage
Raider_Grunt takes 5 physical damage (10/15 HP)

[Turn ends automatically]
```

---

## 🔧 PREFLIGHT COMMANDS (Detailed)

### Range Syntax
```bash
# Single index
ai off 5

# Range
side 10-15 guards

# Multiple ranges
ai off 1-5 10-15 20

# During combat too!
side 27-31 players    # Works anytime
```

### AI Control
```bash
ai on 5-10           # Enable AI for chars 5-10
ai off 1-3           # Disable AI (manual control)
```

### Side Assignment
```bash
side 27-31 players   # Set chars 27-31 to players
side 5-10 guards     # Set to guards
side 15 neutral      # Set single char to neutral

# Valid sides: players, raiders, guards, neutral
# Auto-updates colors and default hostility
```

### Hostility
```bash
hostility 5-10 hostile   # Set to hostile
hostility 2-4 neutral    # Set to neutral
hostility 1 friendly     # Set to friendly

# Affects conversation DC and AI targeting
```

### Stance
```bash
stance 5-10 combat        # Combat mode
stance 2-4 conversation   # Talk mode
stance 15 neutral         # Neutral stance
```

---

## ⚡ REACTION COMMANDS (Detailed)

### Quick Options
```bash
1              # Take it (fast, full damage)
2              # Prompts for block amount
3              # Dodge attempt
```

### Advanced Block
```bash
block 8             # Spend 8 EP, reduce by 8
block 5 buy 3       # Spend 5 EP + gamble 3 EP on dice
                    # 3 EP = 1d6-1 (2-5 extra block)
                    # Fizzles on 1!

# Block calculation:
# Final Reduction = Base EP + Dice Damage
# Final Damage = max(0, Incoming - Reduction)
```

### Dodge Mechanic
```bash
dodge
# Rolls: d20 + DEX mod vs DC 12
# Success: 0 damage
# Fail: Full damage
```

---

## 📊 EXAMPLE PREFLIGHT SESSION

```bash
>> init

═══ PREFLIGHT SETUP ═══

>> look
═══ BATTLEFIELD ROSTER ═══
PLAYERS: 3 combatants
  [1] Keaton (400, 300) [MANUAL]
  [2] Ally_A (420, 350) [MANUAL]
  [3] Ally_B (380, 280) [MANUAL]

GUARDS: 15 combatants
  [4] Guard_01 (850, 250) [AI]
  [5] Guard_02 (870, 300) [AI]
  ...
  [18] Guard_15 (920, 450) [AI]

RAIDERS: 17 combatants
  [19] Raider_01 (900, 400) [AI]
  ...
  [35] Raider_17 (980, 520) [AI]

>> ai off 4-8
AI disabled for Guard_01
AI disabled for Guard_02
AI disabled for Guard_03
AI disabled for Guard_04
AI disabled for Guard_05

>> side 27-31 players
Set Raider_09 to side 'players'
Set Raider_10 to side 'players'
Set Raider_11 to side 'players'
Set Raider_12 to side 'players'
Set Raider_13 to side 'players'

>> hostility 4-8 neutral
Set Guard_01 hostility to 'neutral'
Set Guard_02 hostility to 'neutral'
...

>> look
═══ BATTLEFIELD ROSTER ═══
PLAYERS: 8 combatants  ← NOW 8!
  [1] Keaton (400, 300) [MANUAL]
  ...
  [27-31] Now on player side [AI]

GUARDS: 15 combatants
  [4-8] Now MANUAL + NEUTRAL
  [9-18] Still AI + varies

RAIDERS: 12 combatants  ← NOW 12!
  [remaining raiders]

>> start

═══ INITIALIZING COMBAT ═══
...
```

---

## 🎯 REACTION EXAMPLES

### Example 1: Take It
```
REACTION MOMENT: Keaton
Incoming: 5 damage

>> 1
Keaton takes the hit!
Keaton takes 5 physical damage (25/30 HP)
```

### Example 2: Basic Block
```
REACTION MOMENT: Keaton
Incoming: 10 damage
Your EP: 15/20

>> block 7
Keaton BLOCKS with 7 total!
Damage reduced: 10 → 3
Keaton takes 3 physical damage (27/30 HP)
EP: 8/20
```

### Example 3: Block with Dice Buy
```
REACTION MOMENT: Keaton
Incoming: 12 damage
Your EP: 20/20

>> block 6 buy 3
Block Dice Buy: 1d6-1 = [5]-1 = 4
Keaton BLOCKS with 10 total!
  Base EP: 6 | Dice: 4
Damage reduced: 12 → 2
Keaton takes 2 physical damage (28/30 HP)
EP: 11/20
```

### Example 4: Dice Buy Fizzle
```
>> block 4 buy 2
Block Dice Buy: 1d4-1 = [1]-1 = 0 [FIZZLE]
Keaton BLOCKS with 4 total!
  Base EP: 4 | Dice: 0
Damage reduced: 8 → 4
EP: 14/20
```

### Example 5: Successful Dodge
```
REACTION MOMENT: Keaton
Incoming: 15 damage

>> dodge
Keaton attempts to DODGE!
Roll: d20(16) + 3 (DEX) = 19 vs DC 12
✓ SUCCESS! Keaton evades completely!
```

### Example 6: Failed Dodge
```
>> dodge
Roll: d20(8) + 2 (DEX) = 10 vs DC 12
✗ FAILURE! Taking full damage!
Keaton takes 15 physical damage (15/30 HP)
```

---

## 🔄 UPDATED COMMAND SUMMARY

### Preflight Only
```
start/go       Begin combat
ai <range>     Toggle AI
side <range>   Set team
hostility <r>  Set hostility
stance <r>     Set stance
```

### Combat Only
```
attack         Attack target
cast           Cast spell
check          Skill check
move           Reposition
talk           Conversation
pass           End turn
```

### Reaction Only (When Prompted)
```
1 / take       Accept damage
2 / block      Block (prompt or specify)
3 / dodge      DEX check
block <ep>     Direct block
block <e> buy  Block with dice
```

### Anytime
```
help           Show commands
look           Battlefield state
clear          Clear log
reload         Reload codex
```

---

## 💡 PRO TIPS

1. **Preflight is Your Friend** - Take time to set up sides/AI before `start`
2. **Range Commands Save Time** - `side 27-31 players` beats 5 individual commands
3. **Block Conservatively** - Save EP for critical moments
4. **Dodge is Risky** - 40% failure rate with +0 DEX
5. **Dice Buy Blocks** - High risk, high reward (can fizzle!)
6. **Look Often** - Check character indices before commands
7. **AI Reactions Are Instant** - AI doesn't get reaction prompts (design choice)

---

*Keep this card handy during sessions!* 🎲⚡
