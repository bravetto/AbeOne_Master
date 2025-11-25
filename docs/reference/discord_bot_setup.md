# Discord Bot Setup Guide

## Quick Start

### 1. Create Bot Application

1. Go to https://discord.com/developers/applications
2. Click "New Application"
3. Name your bot
4. Go to "Bot" section
5. Click "Add Bot"
6. Copy the **Bot Token** (keep this secret!)
7. Enable these Privileged Gateway Intents:
   - ✅ Message Content Intent
   - ✅ Server Members Intent
   - ✅ Presence Intent (optional)

### 2. Invite Bot to Server

1. Go to "OAuth2" → "URL Generator"
2. Select scopes:
   - ✅ `bot`
   - ✅ `applications.commands` (for slash commands)
3. Select bot permissions:
   - ✅ Send Messages
   - ✅ Embed Links
   - ✅ Read Message History
   - ✅ Manage Messages (for purge command)
   - ✅ Kick Members (for kick command)
   - ✅ Ban Members (for ban command)
   - ✅ Connect (for voice features)
   - ✅ Speak (for voice features)
4. Copy the generated URL
5. Open URL in browser and select your server
6. Authorize the bot

### 3. Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install discord.py python-dotenv
```

### 4. Create .env File

```bash
# Create .env file in project root
DISCORD_TOKEN=your_bot_token_here
```

**⚠️ NEVER commit .env file to git!**

### 5. Run Bot

```bash
python discord_bot_starter.py
```

You should see:
```
✅ YourBot#1234 has logged in!
📊 Bot is in 1 servers
```

---

## Features Included

✅ **Slash Commands** (Modern Discord)
- `/ping` - Check latency
- `/serverinfo` - Server stats
- `/userinfo` - User stats
- `/interactive` - Test buttons/modals

✅ **Prefix Commands** (Traditional)
- `!hello` - Say hello
- `!purge <amount>` - Delete messages
- `!kick <user>` - Kick member
- `!ban <user>` - Ban member
- `!join` - Join voice channel
- `!leave` - Leave voice channel

✅ **Event Handlers**
- Welcome new members
- Auto-react to keywords
- Member leave tracking

✅ **Interactive Components**
- Buttons
- Modals (forms)
- Views

---

## Next Steps

1. **Customize Commands**
   - Add your own commands
   - Modify existing ones
   - Add more features

2. **Add Database**
   - Store user data
   - Leveling system
   - Economy system

3. **Add Music**
   - Install `yt-dlp` or `pytube`
   - Add music commands
   - Queue system

4. **Add AI Features**
   - ChatGPT integration
   - Image generation
   - Code assistance

5. **Deploy**
   - Heroku (free tier ending)
   - Railway.app (recommended)
   - Render.com
   - VPS (DigitalOcean, AWS)

---

## Troubleshooting

### Bot doesn't respond
- Check bot token is correct
- Verify bot has necessary permissions
- Check intents are enabled

### Slash commands not showing
- Wait a few minutes (Discord caches commands)
- Re-invite bot with `applications.commands` scope
- Use `await bot.tree.sync()` in code

### Permission errors
- Check bot role position (must be above users)
- Verify bot has required permissions
- Check server settings

---

## Resources

- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers)
- [Discord API Docs](https://discord.com/developers/docs)

---

**Happy Bot Building! 🚀**

