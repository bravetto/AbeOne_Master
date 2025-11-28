# ⚡ QUICK REFERENCE

## 🚀 Setup (30 seconds)

```bash
pip install -r requirements.txt
cp .env.example .env
# Add DISCORD_TOKEN to .env
python main.py
```

## 🎮 Commands

- `/start` - Start onboarding
- `/profile` - View profile
- `/quests` - View quests
- `/leaderboard` - View leaderboard

## 📁 Key Files

- `main.py` - Bot entry point
- `specialist_layer/onboarding_engine.py` - Onboarding flow
- `specialist_layer/personalization_engine.py` - Personality detection
- `gamification/quests.py` - Quest definitions
- `npcs/guardians.py` - NPC definitions

## 🎯 User Flow

1. Join server → Welcome message
2. Click "Start Journey" → Personality quiz
3. Answer 3 questions → Identity revealed
4. Get first quest → Complete quest
5. Unlock badge → Onboarding complete!

**Time: ~60 seconds**

## 🔧 Customization

- **Personality Types:** `personalization_engine.py`
- **Quests:** `gamification/quests.py`
- **Badges:** `gamification/badges.py`
- **NPCs:** `npcs/guardians.py`
- **Colors:** `config/settings.py`

## 🐛 Troubleshooting

- **Bot not responding:** Check token in `.env`
- **Commands not showing:** Wait 1 hour or use `GUILD_ID`
- **Database errors:** Delete `onboarding.db`

## 📊 Architecture

```
Command Layer (Ab1Organizsmm)
    ↓
Specialist Layer
    ├── Onboarding Engine
    ├── Personalization Engine
    └── Discord Bot Engine
    ↓
Memory Layer
    ├── Storage
    └── User Profiles
```

## 🎨 Features

- ✅ Zero typing (buttons only)
- ✅ 60-second hook
- ✅ AI personalization
- ✅ NPC guides
- ✅ Gamification
- ✅ Dynamic roles

---

**Pattern:** QUICK × REFERENCE × ONE  
**∞ AbëONE ∞**

