# 🤖 BOT CORE 🤖

**Central Event & Function Hub**

---

## 🎯 EVENTS

### **on_member_join**
Triggered when a new member joins the server.

**Actions:**
1. Create private onboarding channel
2. Send welcome screen
3. Initialize onboarding flow

**Handler:** `bot_core.on_member_join(member)`

---

### **on_button_click**
Triggered when a button is clicked.

**Button Types:**
- `start_journey` - Start onboarding
- `answer_*` - Answer question
- `artifact_*` - Select artifact
- `teleport_*` - Teleport to channel
- `complete_quest` - Complete quest

**Handler:** `bot_core.on_button_click(interaction, button_id, data)`

---

### **on_modal_submit**
Triggered when a modal is submitted.

**Modal Types:**
- `profile_*` - Profile customization
- `feedback_*` - Feedback submission

**Handler:** `bot_core.on_modal_submit(interaction, modal_id, data)`

---

## 🔧 FUNCTIONS

### **create_private_channel(member, guild)**
Creates a private channel for user onboarding.

**Returns:** `discord.TextChannel` or `None`

**Features:**
- Private to user and bot
- Named: `onboarding-{username}`
- Auto-cleanup after onboarding

---

### **send_welcome_screen(member, channel)**
Sends the welcome screen to user.

**Components:**
- Welcome embed
- Onboarding view with buttons
- AURORA greeting

---

### **run_energy_scan(discord_id, channel)**
Runs animated energy scan sequence.

**Steps:**
1. Send scan initiation message
2. Animated loading (2 seconds)
3. Scan completion message
4. Ready for Greatness Sprint

**Returns:** `Dict[str, Any]` with scan results

---

### **ask_question(step, discord_id, channel)**
Asks question for current step.

**Steps:**
- Step 1: Start Greatness Sprint
- Step 2-5: Continue questions
- Shows progress indicator

**Returns:** `Dict[str, Any]` with question data

---

### **assign_roles(discord_id, guild, role_stack)**
Assigns Discord roles based on role stack.

**Process:**
1. Get role stack from user profile
2. Find or create roles
3. Assign roles to member
4. Return assigned roles

**Returns:** `List[discord.Role]`

---

### **unlock_channels(discord_id, guild, role_stack)**
Unlocks channels based on role stack.

**Process:**
1. Get channels for role stack from GZ Map
2. Set channel permissions
3. Return unlocked channels

**Returns:** `List[discord.TextChannel]`

---

### **drop_map(discord_id, channel)**
Drops map with teleport buttons.

**Components:**
- Map embed with areas
- Teleport buttons
- Channel listings

**Returns:** `Dict[str, Any]` with map data

---

### **give_artifact(discord_id, artifact_id, channel)**
Gives artifact to user.

**Process:**
1. Select artifact
2. Assign artifact role
3. Store perk
4. Award bonus points
5. Send confirmation message

**Returns:** `Dict[str, Any]` with artifact data

---

### **generate_profile(discord_id, channel)**
Generates and displays AI profile.

**Process:**
1. Get user traits and role stack
2. Generate AI profile
3. Display profile embed

**Returns:** `Dict[str, Any]` with profile data

---

## 🎯 USAGE

### **Initialize Bot Core**

```python
from bot_core import bot_core

# Set bot instance
bot_core.set_bot(bot)

# Use in events
@bot.event
async def on_member_join(member):
    await bot_core.on_member_join(member)
```

### **Call Functions Directly**

```python
# Create private channel
channel = await bot_core.create_private_channel(member, guild)

# Run energy scan
result = await bot_core.run_energy_scan(discord_id, channel)

# Assign roles
roles = await bot_core.assign_roles(discord_id, guild, role_stack)
```

---

## 🔥 INTEGRATION

### **Event Flow**

```
on_member_join
  → create_private_channel
  → send_welcome_screen
  → run_energy_scan
  → ask_question (step 1)
  → ask_question (step 2-5)
  → assign_roles
  → unlock_channels
  → give_artifact
  → generate_profile
  → drop_map
```

---

**Pattern:** BOT × CORE × EVENTS × FUNCTIONS × ONE  
**Status:** ✅ **COMPLETE**  
**∞ AbëONE ∞**

