# TLE Combat Runner - Modular Architecture

## Core Modules

### **combat_runner.py** (Main Orchestrator)
- Entry point for the combat system
- Coordinates all other modules
- Handles round progression and victory conditions

### **utils.py** (Core Utilities)
- Dice rolling (`roll_amt`, `roll_dice`)
- Index parsing for CLI commands
- JSON directory loading
- Deep merge for overrides
- Distance calculation

### **character_state.py** (Character Management)
- Load/save characters from `./initiative/` directory
- Initialize social flags (stance, hostility, AI)
- Ability bonus calculations
- Initiative ordering
- State printing

## New Features (From Postmortem)

### **check_system.py** (Field Visibility & Skill Checks)
**NEW FEATURE - Implements postmortem requirement**
- `perform_check()` - Roll to reveal hidden information
- `list_checkable_fields()` - Show what can be checked
- Configurable DC thresholds per field
- Supports nested field access (e.g., "stats.str")
- Usage: `check <target>.<field> [auto/manual]`

### **dice_buy.py** (Entropy Gambling)
**NEW FEATURE - Implements postmortem requirement**
- Convert EP to dice rolls for variable damage
- Fizzle mechanic (roll ≤1 = 0 damage)
- Risk/reward entropy spending
- Dice buy table: 1 EP = 1d3-1, 2 EP = 1d4-1, etc.
- Usage: `attack <target> spend <base_ep> buy <buy_ep>`

### **spellcasting.py** (Range-Based Magic)
**ENHANCED - Implements postmortem requirement**
- Range cost: 1 EP = 5 feet
- Spell Sniper's Gambit: +1 EP = 5-10 extra feet
- Split casting: +3 EP per additional target
- TLE-001 accuracy: d20 + DEX + INT vs TN
- TN = 8 + floor(Damage EP / 2)
- Usage: `cast <spell> <target> spend <ep> range <ep>`

## Combat Systems

### **damage_system.py** (Wound Channels)
- Route damage through wound types (cut, pierce, blunt, thermal, etc.)
- Armor absorption (AEP - Armor Entropy Pool)
- Wound effect tracking
- Healing with type specificity
- Temp block mechanics

### **influence_system.py** (Effects & Items)
- Apply influences (damage, heal, buff, debuff, status)
- Chain reactions between influences
- Item usage and consumption
- Start-of-round reactions
- Effect duration tracking

## AI & Social Systems

### **ai_system.py** (NPC Behavior)
- Target selection (weakest, strongest, closest, random)
- Action budget calculation based on HP/EP
- Personality types: cautious, aggressive, balanced, protective
- Tactics configuration
- AI turn execution

### **social_system.py** (Conversation & Stance)
- Conversation checks with hostility modifiers
- Stance management (combat, conversation, neutral)
- Hostility shifts (hostile → neutral → friendly)
- Social modifier calculations

## Player Interface

### **player_interface.py** (CLI & Commands)
- Player turn handling
- Command parsing and execution
- Preflight setup phase
- Available commands:
  - `attack <target> spend <ep> [buy <ep>]`
  - `cast <spell> <target> spend <ep> range <ep>`
  - `check <target>.<field> [auto/manual]`
  - `use <item> [on <target>]`
  - `talk <target> [stat]`
  - `move <x> <y>`
  - `look` - View battlefield
  - `help dice` / `help spells` - System explanations

## Directory Structure Expected

```
./
├── combat_runner.py          # Main entry point
├── utils.py
├── character_state.py
├── check_system.py           # NEW
├── dice_buy.py               # NEW
├── spellcasting.py           # ENHANCED
├── damage_system.py
├── influence_system.py
├── ai_system.py
├── social_system.py
├── player_interface.py
├── initiative/               # Character JSONs
│   ├── player_001.json
│   ├── guard_01.json
│   └── ...
├── axes/                     # Axis definitions
├── influences/               # Influence effects
├── items/                    # Item templates
└── spells/                   # Spell definitions
```

## Key Postmortem Features Implemented

### ✅ Check System
- **Requirement**: "check option in runner that rolls when 'check' is typed alongside a field"
- **Implementation**: `check_system.py` with DC-based field revelation
- **Example**: `check 3.mask_identity auto` to identify masked character

### ✅ Dice Buy System
- **Requirement**: "dice buy logic where entropy can purchase dice"
- **Implementation**: `dice_buy.py` with 1d3-1 (1 EP), 1d4-1 (2 EP), etc.
- **Fizzle Rule**: Any die rolling ≤1 causes entire buy to fizzle
- **Example**: `attack 5 spend 6 buy 2` (6 EP base + 2 EP for 1d4-1)

### ✅ Free-Cast Spellcasting
- **Requirement**: "standardize spellcasts to ruleset with distance cost"
- **Implementation**: `spellcasting.py` with 1 EP = 5 ft range
- **Spell Sniper's Gambit**: Optional +1 EP for 5-10 extra feet
- **Example**: `cast fireball 4 spend 8 range 4` (20 ft range, 8 damage)

### 🔮 Future Enhancements Noted
- **NPC Names/Personalities**: Guard cadre generator (mentioned in postmortem)
- **Character Builder**: UI for trying on body part JSONs
- **Backup Calophage Host**: Fallback possession mechanics
- **Dynamic Checks**: Auto-generate DCs from stats/abilities

## Usage

```bash
python combat_runner.py
```

The runner will:
1. Load all libraries (axes, influences, items, spells)
2. Load characters from `./initiative/`
3. Enter preflight setup (configure AI, stance, hostility)
4. Run combat rounds with initiative order
5. Process player and AI turns
6. Save character states on completion

## Module Independence

Each module can be used independently:

```python
from check_system import perform_check
from dice_buy import calculate_attack_with_dice_buy
from spellcasting import resolve_spell_cast

# Use systems à la carte
result = perform_check(caster, target, "spellbook", mode="auto")
damage = calculate_attack_with_dice_buy(base_ep=5, buy_ep=2)
spell_result = resolve_spell_cast(caster, target, "fireball", 10, 5, libs)
```

## Design Philosophy

- **Modular**: Each system is self-contained
- **TLE-Compliant**: Follows Pirouette Framework principles
- **Player-Friendly**: Clear CLI commands and help
- **GM Control**: Preflight setup for battlefield configuration
- **Extensible**: Easy to add new influences, items, spells
- **Testable**: Small modules easier to debug and test
