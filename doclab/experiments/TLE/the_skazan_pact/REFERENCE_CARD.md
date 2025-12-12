# TLE Combat Runner - Command Reference Card

```
╔════════════════════════════════════════════════════════════════╗
║                  TLE COMBAT RUNNER v3.1                        ║
║              QUICK REFERENCE - PRINT & KEEP                    ║
╚════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────┐
│ SETUP COMMANDS                                                  │
├─────────────────────────────────────────────────────────────────┤
│ init              Roll initiative and start combat              │
│ reload            Clear and reload from codex.json              │
│ spawn <id>        Add test character (dev mode)                 │
│ look              Print battlefield state                       │
│ clear             Clear terminal log                            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ COMBAT ACTIONS                                                  │
├─────────────────────────────────────────────────────────────────┤
│ attack <target> spend <ep> [buy <ep>]                           │
│   Example: attack 5 spend 8 buy 2                               │
│   → Base damage: 8 EP × 0.5 = 4                                 │
│   → Dice buy: 2 EP = 1d4-1 (fizzles on 1)                      │
│                                                                 │
│ cast <spell> <target> [power <ep>]                              │
│   Example: cast fireball 3 power 10                             │
│   → Auto-calculates range cost (1 EP = 5 ft)                   │
│   → Accuracy: d20 + DEX + INT vs TN (8 + EP/2)                 │
│                                                                 │
│ check <target>.<field>                                          │
│   Example: check 2.mask_identity                                │
│   → Roll: d20 + WIS vs DC (varies by field)                    │
│   → Reveals hidden information on success                       │
│                                                                 │
│ move <x> <y> [z]                                                │
│   Example: move 600 400 50                                      │
│   → Sets position (z=altitude)                                  │
│                                                                 │
│ talk <target> [stat]                                            │
│   Example: talk 4 wis                                           │
│   → Conversation check, shifts hostility                        │
│                                                                 │
│ use <item> [on <target>]                                        │
│   Example: use potion on 1                                      │
│   → Consumes item, applies effects                              │
│                                                                 │
│ pass / end        End current turn                              │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ GM COMMANDS                                                     │
├─────────────────────────────────────────────────────────────────┤
│ side <idx> <team>      Set character's side                     │
│   Example: side 5 players                                       │
│   Valid teams: players, raiders, guards, neutral                │
│                                                                 │
│ ai on/off <idx>        Toggle AI control                        │
│   Example: ai off 3                                             │
│   → Player control when off, AI when on                         │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ DICE BUY TABLE                                                  │
├─────────────────────────────────────────────────────────────────┤
│ EP Cost │ Dice       │ Expected │ Fizzle Risk                   │
│    1    │ 1d3-1      │   0.5    │ 33%                           │
│    2    │ 1d4-1      │   1.0    │ 25%                           │
│    3    │ 1d6-1      │   2.0    │ 17%                           │
│    4    │ 2d3-1      │   2.0    │ 56%                           │
│    5    │ 2d4-1      │   3.0    │ 44%                           │
│    6    │ 1d8-1      │   2.5    │ 12%                           │
│    8    │ 2d6-1      │   5.0    │ 31%                           │
│   10    │ 2d8-1      │   7.0    │ 22%                           │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ TARGET SELECTION                                                │
├─────────────────────────────────────────────────────────────────┤
│ By Name:  attack guard    (partial match)                       │
│ By Index: attack 5        (from look/tracker)                   │
│ By Number: target shows as [5] in interface                     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ FIELD VISIBILITY DCs (for 'check' command)                     │
├─────────────────────────────────────────────────────────────────┤
│ inventory: 10     spellbook: 12      stats: 12                  │
│ hidden_weapons: 14     allegiances: 15                          │
│ vulnerabilities: 16    secret_orders: 16                        │
│ mask_identity: 18      true_name: 20                            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ SPELL MECHANICS (TLE-001)                                       │
├─────────────────────────────────────────────────────────────────┤
│ Range Cost: 1 EP = 5 feet                                       │
│ Accuracy: d20 + DEX + INT vs TN                                 │
│ TN = 8 + floor(Damage EP / 2)                                   │
│ Spell Sniper's Gambit: +1 EP = 5-10 extra feet                 │
│ Split Cast: +3 EP per additional target                         │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ STATUS INDICATORS (Visual)                                      │
├─────────────────────────────────────────────────────────────────┤
│ 🟦 Cyan Ring       Active turn (current character)              │
│ ─── Dashed Line   Character is flying (Z > 0)                   │
│ ███ Green Bar     HP remaining                                  │
│ ── Blue Bar       EP remaining (below HP)                       │
│ ⚫ Shadow          Ground position (actual X, Y)                │
│ ❌ Red X          Character defeated (HP ≤ 0)                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ SIDE COLOR CODES                                                │
├─────────────────────────────────────────────────────────────────┤
│ Players: 🟦 Cyan (#00ffff)    Left 30% of battlefield           │
│ Raiders: 🟥 Red (#ff3333)     Right 30% of battlefield          │
│ Guards:  🟧 Orange (#ffaa00)  Right 30% of battlefield          │
│ Neutral: ⚪ Gray (#888888)    Center 20% of battlefield         │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ KEYBOARD SHORTCUTS                                              │
├─────────────────────────────────────────────────────────────────┤
│ Enter             Execute command                               │
│ Up Arrow          Recall last command                           │
│ F12               Open browser console (debug)                  │
│ Ctrl + F5         Hard refresh (clear cache)                    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ TYPICAL TURN SEQUENCE                                           │
├─────────────────────────────────────────────────────────────────┤
│ 1. System announces turn: "KEATON's TURN"                       │
│ 2. Shows HP/EP status                                           │
│ 3. If AI: Auto-plays in 0.5s                                    │
│ 4. If Player: Awaits command                                    │
│ 5. Command executes → Damage applied → Turn ends                │
│ 6. Next character's turn begins                                 │
│ 7. Round increments when queue completes                        │
│ 8. Check victory conditions                                     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ HOSTILITY LEVELS (for 'talk' command)                          │
├─────────────────────────────────────────────────────────────────┤
│ Hostile → Neutral → Friendly                                    │
│   ↑         ↑         ↑                                         │
│ Success shifts right, Failure shifts left                       │
│ DC = 10 + target's WIS modifier                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ MAINTENANCE                                                     │
├─────────────────────────────────────────────────────────────────┤
│ Update characters?                                              │
│   1. Edit JSON in initiative/                                   │
│   2. python generate_codex.py                                   │
│   3. In runner: >> reload                                       │
│                                                                 │
│ Validate before session?                                        │
│   python validate_codex.py                                      │
│                                                                 │
│ Check what's loaded?                                            │
│   >> look                                                       │
│   (or check browser console: STATE.characters)                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ TROUBLESHOOTING                                                 │
├─────────────────────────────────────────────────────────────────┤
│ "No codex found"        → Place in same folder or drag-drop     │
│ "Invalid target"        → Use 'look' to see valid indices       │
│ "Insufficient EP"       → Check current EP with 'look'          │
│ "AI won't attack"       → Verify side != target side            │
│ Character tiny/gray     → Missing size/color (auto-assigned)    │
│ HP/EP bars wrong        → Check max_HP and max_EP fields        │
└─────────────────────────────────────────────────────────────────┘

╔════════════════════════════════════════════════════════════════╗
║  QUICK START: python generate_codex.py → open HTML → init     ║
║  FULL DOCS: README.md, QUICKSTART.md, DEPLOYMENT.md           ║
╚════════════════════════════════════════════════════════════════╝
```

---

## Example Combat Sequence

```
>> init
Initiative Order:
  [1] Raider_Mage (Init: 18)
  [2] Keaton (Init: 17)
  [3] Guard_05 (Init: 16)

═══ KEATON's TURN ═══
HP: 30/30 | EP: 20/20

>> look
[1] Keaton | players | HP 30/30 | EP 20/20
[2] Raider_Mage | raiders | HP 25/25 | EP 15/15
[3] Guard_05 | guards | HP 20/20 | EP 10/10

>> cast fireball 2 power 12
Distance: 450px (5 EP)
Power: 12 EP
Total Cost: 17 EP
Accuracy: d20(15) + 4 = 19 vs TN 14
✓ HIT!
Raider_Mage takes 12 arcane damage (13/25 HP)

[AI] Raider_Mage evaluating...
[AI] Attacking Keaton (spend 10, buy 2)
Dice Buy (2 EP): 1d4-1 = [3]-1 = 2
Keaton takes 7 physical damage (23/30 HP)

═══ GUARD_05's TURN ═══
[AI] Guard_05 evaluating...
[AI] Attacking Raider_Mage (spend 8)
Raider_Mage takes 4 physical damage (9/25 HP)

═══ ROUND 2 ═══
```

---

*Keep this reference handy during sessions!* 🎲
