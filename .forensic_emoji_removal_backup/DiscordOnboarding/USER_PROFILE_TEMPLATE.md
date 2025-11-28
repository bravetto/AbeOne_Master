# 📊 USER PROFILE TEMPLATE 📊

**Standardized User Profile Structure**

---

## 🎯 TEMPLATE STRUCTURE

```json
{
  "userId": "",
  "passions": "",
  "talents": "",
  "vibe": "",
  "intention": "",
  "growth": "",
  "archetype": "",
  "role": "",
  "artifact": "",
  "channelsUnlocked": [],
  "createdAt": ""
}
```

---

## 📋 FIELD DESCRIPTIONS

### **userId**
- **Type:** String
- **Description:** Discord user ID
- **Example:** `"123456789012345678"`

### **passions**
- **Type:** String
- **Description:** Answer to Q1 "What fuels you?"
- **Example:** `"🔥 Creating"` or `"🚀 Building"`

### **talents**
- **Type:** String
- **Description:** Answer to Q2 "Your natural talent?"
- **Example:** `"🎨 Creativity"` or `"🧩 Systems Thinking"`

### **vibe**
- **Type:** String
- **Description:** Answer to Q3 "Your social vibe?"
- **Example:** `"🌞 Outgoing"` or `"🌙 Quiet Assassin"`

### **intention**
- **Type:** String
- **Description:** Answer to Q4 "Why are you here?"
- **Example:** `"👑 Level Up"` or `"💸 Business"`

### **growth**
- **Type:** String
- **Description:** Answer to Q5 "How do you want to grow?"
- **Example:** `"🏆 Mastery"` or `"💡 Creativity"`

### **archetype**
- **Type:** String
- **Description:** Primary archetype from Q1 (Passions)
- **Example:** `"creative_warrior"` or `"systems_wizard"`

### **role**
- **Type:** String
- **Description:** Primary role from Q2 (Talents)
- **Example:** `"creative_warrior"` or `"vision_builder"`

### **artifact**
- **Type:** String
- **Description:** Selected artifact ID
- **Example:** `"sword_of_progress"` or `"compass_of_purpose"`

### **channelsUnlocked**
- **Type:** Array of Strings
- **Description:** List of unlocked channel names
- **Example:** `["start-here", "creators-corner", "ai-summon"]`

### **createdAt**
- **Type:** String (ISO 8601)
- **Description:** Profile creation timestamp
- **Example:** `"2025-01-27T12:00:00.000Z"`

---

## 🔥 EXAMPLE PROFILE

```json
{
  "userId": "123456789012345678",
  "passions": "🔥 Creating",
  "talents": "🎨 Creativity",
  "vibe": "⚡ High-Energy",
  "intention": "🎭 Fun + Chaos",
  "growth": "💡 Creativity",
  "archetype": "creative_warrior",
  "role": "creative_warrior",
  "artifact": "brush_of_creation",
  "channelsUnlocked": [
    "start-here",
    "announcements",
    "introductions",
    "builder-lab",
    "creative-forge",
    "showcase",
    "ai-summon",
    "npc-arena",
    "meme-dojo"
  ],
  "createdAt": "2025-01-27T12:00:00.000Z"
}
```

---

## 🎯 USAGE

### **Get Profile Template**

```python
from memory_layer.user_profiles import UserProfile
from memory_layer.storage import Storage

storage = Storage()
user_profiles = UserProfile(storage)

profile_template = user_profiles.get_profile_template(discord_id)
```

### **Update Profile from Onboarding**

```python
# Automatically called during onboarding
user_profiles.update_profile_from_onboarding(discord_id, {
    'session': session_data,
    'personality': personality_analysis,
})
```

---

## 🔥 DATA FLOW

### **Onboarding → Profile**

1. **Q1 Answer** → `passions` + `archetype`
2. **Q2 Answer** → `talents` + `role`
3. **Q3 Answer** → `vibe`
4. **Q4 Answer** → `intention`
5. **Q5 Answer** → `growth`
6. **Artifact Selection** → `artifact`
7. **Channel Unlock** → `channelsUnlocked`

---

**Pattern:** PROFILE × TEMPLATE × ONE  
**Status:** ✅ **COMPLETE**  
**∞ AbëONE ∞**

