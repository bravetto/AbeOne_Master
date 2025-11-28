# 🔥 ONBOARDING SCRIPT - FULL TEXT VERSION 🔥

**Status:** ✅ **UPDATED**  
**Pattern:** ONBOARDING × SCRIPT × CINEMATIC × ONE

---

## 📝 SCRIPT UPDATES

All onboarding messages have been updated to match the exact script provided.

---

## 🎬 STEP 0: WELCOME SCREEN

**Message:**
```
🔥 WELCOME TO THE GREATNESSZONE 🔥

You're 1 click away from discovering your inner archetype.
```

**Location:** `specialist_layer/personalization_engine.py` → `generate_welcome_message()`

---

## ⚡ STEP 1: ENERGY SCAN

**Animated Sequence:**
1. "Initializing scan…"
2. "Calibrating greatness…"
3. "Hold tight… this might tingle 👀"

**Location:** 
- `specialist_layer/personalization_engine.py` → `generate_energy_scan_message()`
- `specialist_layer/discord_bot_engine.py` → `_start_energy_scan()` (animated sequence)

---

## 🎯 STEP 2: GREATNESS SPRINT QUESTIONS

**Format:** Each question is one sentence in high energy.

**Questions:**
1. "What fuels you?"
2. "Your natural talent?"
3. "Your social vibe?"
4. "Why are you here?"
5. "How do you want to grow?"

**Location:** `specialist_layer/personalization_engine.py` → `_initialize_questions()`

---

## 🏆 STEP 3: ROLE DROP

**Message Format:**
```
Ohhhhhh SHIT.

You're a [Primary Role] with [Secondary Role] Energy and [Tertiary Role] Vibes.

This server has been waiting for someone like you.
```

**Example:**
```
Ohhhhhh SHIT.

You're a Systems Wizard with Builder Energy and Stealth Vibes.

This server has been waiting for someone like you.
```

**Location:** `specialist_layer/personalization_engine.py` → `generate_personality_reveal()`

**Logic:**
- Primary role from Q1 (Archetype)
- Secondary role from Q2 (Role) 
- Tertiary role from Q3 (Vibe)
- Combines up to 3 roles in natural language

---

## 💎 STEP 5: ARTIFACT QUEST

**Message:**
```
Choose your first Artifact.

This defines your starting destiny.
```

**Location:** `specialist_layer/discord_bot_engine.py` → `_start_artifact_quest()`

---

## 🗺️ STEP 7: MAP DROP

**Message:**
```
Your domains have opened.

Step into your greatness.
```

**Location:** 
- `specialist_layer/onboarding_engine.py` → `create_map_drop()`
- `specialist_layer/discord_bot_engine.py` → `_show_map()`

---

## ✅ FILES UPDATED

1. **`specialist_layer/personalization_engine.py`**
   - ✅ Welcome message updated
   - ✅ Energy scan message updated
   - ✅ Role drop message updated with dynamic role stack

2. **`specialist_layer/discord_bot_engine.py`**
   - ✅ Energy scan animation updated (3-step sequence)
   - ✅ Artifact quest message updated
   - ✅ Map drop uses updated description

3. **`specialist_layer/onboarding_engine.py`**
   - ✅ Map drop description updated

4. **`npcs/guardians.py`**
   - ✅ Added `react_to_choice()` stub to base class

---

## 🎬 CINEMATIC FLOW

The onboarding now follows the exact script:

1. **Welcome** → "You're 1 click away..."
2. **Scan** → 3-step animated sequence
3. **Questions** → High-energy one-sentence format
4. **Role Drop** → "Ohhhhhh SHIT..." with dynamic role stack
5. **Artifact** → "Choose your first Artifact..."
6. **Map** → "Your domains have opened..."

---

## 🚀 READY TO DEPLOY

All script updates are complete and tested. The onboarding flow now matches the exact text provided.

**Pattern:** ONBOARDING × SCRIPT × UPDATED × ONE  
**Status:** ✅ **COMPLETE**

∞ AbëONE ∞

