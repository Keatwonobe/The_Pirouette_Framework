# 🎲 THE SONG OF RUST - GM QUICKSTART GUIDE

## ADVENTURE AT A GLANCE

**System:** The Lost Eternal (TLE)
**Level:** 3-5
**Players:** 4 (SCP members)
**Sessions:** 3-5
**Tone:** Industrial horror, moral dilemmas, body horror
**Core Theme:** "What makes us human when we're treated as tools?"

---

## WHAT YOU NEED

**Files Required:**
- `ADV_001_Song_of_Rust_Narrative.md` (full adventure text)
- `enc_road_ambush.json` (Session 1 encounter)
- `npc_bandit_leader.json` (Torven)
- `en_desperate_refugee.json` (×3 for ambush)
- `en_optimized_worker.json` (×6+ for Session 2)
- `boss_perfected_foreman.json` (Session 2 boss)
- `npc_inquisitor_vex.json` (recurring NPC)
- `item_refugee_journal.json` (key item)
- `sp_synchronize.json` (horror spell)
- `wp_resonance_spanner.json` (boss loot)

**Prep Time:** 30-60 minutes first session, 15 minutes subsequent

---

## THE PITCH (READ TO PLAYERS)

> "You are the Skazan Containment Phalanx—expendable problem-solvers for a dying magical empire. You've just defeated a calophage and survived. Barely.
>
> Your handler, Inquisitor Vex, has your next assignment: The Singing Foundry, an industrial complex where workers have 'gone strange.' Moving in perfect unison. Speaking together. Building impossible geometries.
>
> Three days by carriage. Shut it down. Eliminate the source. Try not to die.
>
> Oh, and one more thing: the refugees you pass on the road? They're fleeing FROM where you're going TO.
>
> Good luck."

---

## SESSION 1: THE JOURNEY

**Goal:** Establish team dynamics and introduce mystery

### Opening (15 min)
- Carriage ride RP
- Vex's mission briefing
- Player introductions if needed
- Establish P₀: "We're disposable tools"

### Encounter 1: Road Ambush (45-60 min)
- **Setup:** Load `enc_road_ambush.json`
- **Key NPCs:** Torven (leader), 3 refugees, Vex (observer)
- **Secret:** These are victims fleeing the Foundry
- **Choices Matter:**
  - Kill them → Efficient but ruthless (Vex approves)
  - Spare them → Get journal and info (Vex disapproves)
  - Negotiate → Best outcome, requires skill

**CRITICAL:** If players spare/negotiate, Torven gives journal. This provides:
- Foreshadowing of horror
- Names they'll recognize later (Mira)
- +2 bonus to Will saves vs Synchronization

### Arrival (15 min)
- Describe the Foundry (use narrative text)
- Workers moving in unison
- The harmonic hum
- Workers ALL TURN to face carriage at once
- End on creepy note

**Session 1 Checkpoint:**
- Party K_τ = 0.55 (bonding complete)
- V_Γ = 0.40 (pressure building)
- Players should feel: intrigued, slightly unnerved

---

## SESSION 2: THE INVESTIGATION

**Goal:** Reveal the truth, moral horror, boss fight

### Investigation Phase (30-45 min)
Allow players to explore:

**1. Worker Barracks**
- Empty beds perfectly made
- Synchronized breathing sounds
- Scratch marks: geometric patterns
- DC 12 Investigation: Find worker schedules—no breaks, ever

**2. Processing Plant**
- Workers operating machinery in perfect sync
- Building impossible devices
- DC 14 Insight: Workers aren't enslaved—they're *content*
- If approached: Workers ignore party unless threatened

**3. Foreman's Office**
- Logs showing 6-month transformation
- Final entry: "We will become" (read aloud)
- DC 10 Investigation: Find route to Central Tower

**4. Central Tower** (when ready)
- The Resonance Engine revealed
- Skazan artifact
- Working as designed
- Interface accessible

### Encounter 2: Optimized Workers (45-60 min)
- **Setup:** Load 6× `en_optimized_worker.json`
- **Location:** Between offices and tower
- **Special:** Hive mind, self-repair, conversion attempts
- **Horror Moment:** If players read journal, one worker is named Mira
- **Dialogue:** All speak in unison, eerily calm

**EMPHASIZE:** These are victims, not villains

### Boss Fight: The Perfected Foreman (60-75 min)
- **Setup:** Load `boss_perfected_foreman.json`
- **Location:** Resonance Chamber
- **Phases:**
  - Phase 1 (100-51% HP): Adaptive, defensive
  - Phase 2 (50-26% HP): Aggressive, telegraphed
  - Phase 3 (25-1% HP): Desperate, summons help

**CRITICAL MECHANIC:** Adaptive Defense
- Track damage types used
- +2 resistance each time same type hits
- Teaches players to vary tactics

**Session 2 Checkpoint:**
- Party K_τ = 0.50 (identity crisis)
- V_Γ = 0.80 (moral weight)
- Players should feel: horrified, conflicted, pressured

---

## SESSION 3-4: THE CHOICE & CONSEQUENCES

**Goal:** Δ-vertex decision, transformation, resolution

### The Interface (15-30 min)
After defeating Foreman, Engine interface is accessible.

**Present Options Clearly:**

```
1. DESTROY ENGINE
   Pro: Mission success, Order pleased
   Con: Kills all 300+ optimized workers instantly
   
2. SAFE SHUTDOWN (3 hours)
   Pro: Workers may recover
   Con: Order displeased, workers traumatized
   
3. REPROGRAM ENGINE
   Pro: Possible perfect outcome
   Con: Skill check DC 18, catastrophic if failed
   
4. LEAVE ACTIVE
   Pro: Refuse to be Order's tools
   Con: Optimization spreads, party marked as failures
```

**LET THEM DEBATE.** This is the Δ-vertex. No time pressure (yet).

### The Consequence Encounter (45-75 min)
Based on their choice, load appropriate encounter:

**If Destroy:**
- Workers die screaming in unison
- Psychic residue manifests
- Guilt-based enemies attack
- Vex: "Acceptable losses"

**If Shutdown:**
- Partially-restored workers attack in confusion
- Tragic combat (they're victims, scared)
- Some can be talked down (DC 14 Persuasion)
- Vex: "You've created witnesses"

**If Reprogram Success:**
- Skazan Order enforcers arrive (angry)
- Want Engine intact for study
- Combat or negotiate
- Vex: "Impressive but reckless"

**If Reprogram Fail:**
- One PC becomes optimized
- Temporary PvP scenario (can be reversed)
- Horror of seeing teammate change
- Vex: "I warned you"

**If Leave:**
- Chase sequence, running battle
- Vex abandons party
- Party becomes fugitives
- Opens different campaign path

### Resolution (15-30 min)
- Journey back
- Vex's judgment
- Consequences based on choice
- **The Letter** (epilogue hook)

**Session 3-4 Checkpoint:**
- Party K_τ varies (0.40-0.70 depending on choice)
- V_Γ = 0.95 at peak, then normalizes
- Players should feel: Changed, accomplished, uncertain about future

---

## RUNNING COMBAT

**Initiative Order:**
1. Roll initiative for all combatants
2. Optimized workers share same count (hive mind)
3. Boss acts on own initiative

**Key Mechanics:**

**Synchronization Spell:**
- Will save DC 14 or become Synchronized
- Synchronized = -2 to rolls, predictable
- Duration 3 rounds, then save again

**Hive Mind:**
- If one optimized sees threat, all do
- Coordinate perfectly for flanking
- +2 to hit if multiple engage same target

**Self-Repair:**
- Optimized at 0 HP regenerate 3 HP/round
- Must be destroyed completely (fire, massive damage)
- Creates resource pressure

**Adaptive Defense (Boss):**
- Track damage types used
- Each repeat use: +2 resistance (max +8)
- Forces tactical diversity

---

## TRACKING METRICS (OPTIONAL)

For Narrative Engine optimization:

```python
party_coherence_K_τ = {
    'session_1_start': 0.55,
    'session_1_end': 0.55,
    'session_2_end': 0.50,
    'session_3_decision': varies,
    'campaign_end': varies
}

pressure_V_Γ = {
    'session_1_start': 0.35,
    'session_1_end': 0.40,
    'session_2_end': 0.80,
    'session_3_peak': 0.95,
    'resolution': 0.40
}

transformation_κ = {
    'destroy': +0.30,
    'save': +0.55,
    'reprogram_success': +0.45,
    'reprogram_fail': +0.25,
    'leave': +0.50
}
```

Use these to track if story is hitting emotional beats correctly.

---

## COMMON GM MISTAKES

**Don't:**
- ❌ Force a specific outcome
- ❌ Make one choice "obviously correct"
- ❌ Have Vex intervene in player choices
- ❌ Let combat drag (keep encounters 3-5 rounds)
- ❌ Forget the horror elements

**Do:**
- ✅ Honor player agency completely
- ✅ Make all choices have real weight
- ✅ Use Vex's reactions to show Order's values
- ✅ Emphasize the wrongness of optimization
- ✅ Track moral choices for future consequences

---

## ADAPTING ON THE FLY

**If Combat Too Easy:**
- Add more optimized workers mid-fight
- Boss summons help earlier
- Workers use Synchronization more

**If Combat Too Hard:**
- Reduce worker count
- Lower Synchronization DC
- Have Vex provide tactical hint
- Allow environmental advantages

**If Players Stuck:**
- Vex comments on options (without deciding)
- Environmental clues (logs, signs)
- NPC survivor appears with info

**If Players Going Off-Rails:**
- Let them! Track consequences
- Vex adapts to their approach
- Order responds to their reputation

---

## PROPS & ATMOSPHERE

**Music:**
- Session 1: Ominous travel music
- Session 2: Industrial ambient, building tension
- Boss Fight: Mechanical, rhythmic, unsettling
- Decision Point: Silence or quiet drones

**Sound Effects:**
- Harmonic humming (constant low tone)
- Synchronized footsteps
- Industrial machinery
- The "death scream" if destroyed (all voices at once)

**Visual Aids:**
- Sketch of geometric patterns
- Image of industrial foundry
- Map of complex (optional)
- Picture of crystalline engine

---

## POST-ADVENTURE

**Regardless of Outcome:**

1. Award XP (varies by combat)
2. Award Residue (8-15 per encounter)
3. Deliver "The Letter" (unsigned warning)
4. Note party's reputation with Order
5. Set up next adventure hook

**Possible Follow-Ups:**

- **If They Destroyed:** Psychic haunting arc
- **If They Saved:** Punishment detail mission
- **If They Reprogrammed:** Research division interest
- **If They Fled:** Fugitive campaign

**The Conspiracy Deepens:**
Letter reveals 17 Resonance Engines exist.
This was one of many.
Order has more secrets.
Party now knows too much.

---

## EMERGENCY REFERENCE

**Quick Stats:**

```
Refugee: HP 6, +0 to hit, 1d4 damage, flees at 3 HP
Optimized: HP 16, +2 to hit, 1d8+1 damage, hive mind
Foreman: HP 65, +5 to hit, 2d8+3 damage, 3 phases
Vex: HP 48, +6 to hit, won't fight (probably)
```

**Quick DCs:**
- Perception: 12 (notice), 15 (detail)
- Investigation: 10 (obvious), 15 (hidden)
- Persuasion: 13 (convince), 16 (difficult)
- Intimidation: 12 (scare), 15 (terrorize)
- Will vs Sync: 14 (resist), 16 (hard)

**Quick Decisions:**
- Spare refugees: Get journal, +2 vs Sync
- Kill refugees: Vex approves, moral weight
- Destroy Engine: 300 die, Order pleased
- Save workers: Order displeased, workers live
- Reprogram: Gamble, DC 18 or disaster
- Leave: Become fugitives, different campaign

---

## THE GOLDEN RULE

**This adventure works because player choice matters.**

Every decision has consequences.
No outcome is "wrong."
Vex's reactions show Order's values.
The Engine choice defines the party.

Don't force outcomes.
Don't judge player choices.
Just show consequences honestly.

The story will emerge from their decisions.

**Trust the algorithm.**
**Trust your players.**
**Trust the horror.**

---

## FINAL CHECKLIST

Before Session 1:
□ Read full narrative document
□ Load `enc_road_ambush.json` into system
□ Print/load NPC stats
□ Prepare Vex's voice and mannerisms
□ Have journal text ready
□ Prep arrival description

Before Session 2:
□ Review investigation locations
□ Load `en_optimized_worker.json` ×6
□ Load `boss_perfected_foreman.json`
□ Prepare Synchronization mechanics
□ Have Engine description ready
□ Prep boss phase transitions

Before Session 3:
□ Review player choice from Session 2
□ Load appropriate consequence encounter
□ Prepare Vex's reaction dialogue
□ Have epilogue letter ready
□ Consider campaign continuation hooks

---

**You're ready.**

**The Foundry awaits.**

**The workers are singing.**

**Your players will never forget this.**

🎭 Break a leg, GM.
