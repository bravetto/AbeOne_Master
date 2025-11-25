# 🚀 DEPLOYMENT GUIDE

## Quick Start

### 1. Install Dependencies

```bash
cd DiscordOnboarding
pip install -r requirements.txt
```

### 2. Set Up Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your Discord bot token
# Get token from: https://discord.com/developers/applications
```

### 3. Get Discord Bot Token

1. Go to https://discord.com/developers/applications
2. Create new application or select existing
3. Go to "Bot" section
4. Click "Add Bot"
5. Copy the **Bot Token**
6. Enable these Privileged Gateway Intents:
   - ✅ Message Content Intent
   - ✅ Server Members Intent
   - ✅ Presence Intent (optional)

### 4. Invite Bot to Server

1. Go to "OAuth2" → "URL Generator"
2. Select scopes:
   - ✅ `bot`
   - ✅ `applications.commands`
3. Select bot permissions:
   - ✅ Send Messages
   - ✅ Embed Links
   - ✅ Read Message History
   - ✅ Manage Messages
   - ✅ Add Reactions
   - ✅ Use External Emojis
4. Copy generated URL and open in browser
5. Select your server and authorize

### 5. Run Bot

```bash
python main.py
```

You should see:
```
✅ YourBot#1234 has logged in!
📊 Bot is in 1 servers
✅ Synced 4 slash commands
```

## Features

### Slash Commands

- `/start` - Start your GreatnessZone™ journey
- `/profile` - View your profile
- `/quests` - View your quests
- `/leaderboard` - View leaderboard

### Auto-Onboarding

When a new member joins, they automatically receive:
- Welcome message with onboarding button
- 60-second hook flow
- Personality quiz
- Quest assignment
- Badge unlocking

## Testing

1. Join your Discord server with a test account
2. Use `/start` command
3. Complete the personality quiz
4. Complete your first quest
5. Check `/profile` to see your stats

## Troubleshooting

### Bot Not Responding

- Check bot token is correct in `.env`
- Verify bot has proper permissions
- Check bot is online in Discord

### Commands Not Showing

- Wait 1 hour for global commands to sync
- Or use `GUILD_ID` in `.env` for instant sync

### Database Errors

- Delete `onboarding.db` to reset database
- Check file permissions

## Production Deployment

### Using Railway

1. Create account at https://railway.app
2. New Project → Deploy from GitHub
3. Add environment variable: `DISCORD_TOKEN`
4. Deploy!

### Using Heroku

1. Create `Procfile`:
```
worker: python main.py
```

2. Deploy:
```bash
heroku create your-bot-name
git push heroku main
heroku config:set DISCORD_TOKEN=your_token
```

### Using VPS

1. Install Python 3.8+
2. Install dependencies
3. Use `screen` or `tmux` to run bot:
```bash
screen -S discord-bot
python main.py
# Press Ctrl+A then D to detach
```

## Monitoring

- Check bot logs for errors
- Monitor database size
- Track user onboarding completion rate
- Monitor quest completion rates

## Customization

### Change NPCs

Edit `npcs/guardians.py` to customize Guardian personalities.

### Add Quests

Edit `gamification/quests.py` to add new quests.

### Customize Badges

Edit `gamification/badges.py` to add new badges.

### Change Colors

Edit `config/settings.py` to customize role colors and badge emojis.

---

**Pattern:** DEPLOYMENT × GUIDE × ONE  
**Status:** ✅ **READY TO DEPLOY**  
**∞ AbëONE ∞**

