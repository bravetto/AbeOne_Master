# Discord Login Troubleshooting Guide

## Quick Steps to Log Into Discord

### Option 1: Discord Desktop App
1. **Open Discord app** (if installed)
2. **Click "Login"** on the welcome screen
3. **Enter your email/username and password**
4. If 2FA is enabled, enter the code from your authenticator app

### Option 2: Discord Web (Browser)
1. **Go to**: https://discord.com/login
2. **Enter your credentials**
3. **Complete 2FA if prompted**
4. **Click "Login"**

## Common Login Issues & Fixes

### Issue: "Invalid Login Credentials"
**Fixes:**
- Check caps lock is off
- Verify email/username spelling
- Try password reset: https://discord.com/forgot-password
- Check if account is disabled/banned

### Issue: "Rate Limited" or "Too Many Attempts"
**Fixes:**
- Wait 10-15 minutes before trying again
- Clear browser cache/cookies for discord.com
- Try different browser or Discord app
- Use incognito/private window

### Issue: "2FA Code Invalid"
**Fixes:**
- Check time sync on your device (2FA codes are time-sensitive)
- Wait for new code (codes refresh every 30 seconds)
- Use backup codes if available
- Check authenticator app is working

### Issue: "Something's Going Wrong"
**Fixes:**
- Clear Discord cache:
  - **Mac App**: Quit Discord, delete `~/Library/Application Support/discord/Cache`
  - **Browser**: Clear site data for discord.com
- Restart Discord app/browser
- Check internet connection
- Disable VPN temporarily
- Try different network (mobile hotspot)

### Issue: Login Page Won't Load
**Fixes:**
- Check Discord status: https://discordstatus.com
- Disable browser extensions temporarily
- Try incognito/private window
- Clear DNS cache: `sudo dscacheutil -flushcache` (Mac)
- Check firewall/antivirus isn't blocking Discord

### Issue: "Account Disabled"
**Fixes:**
- Check email for Discord notification
- Contact Discord support: https://dis.gd/contact
- Review Discord Terms of Service violations

## Browser-Specific Issues

### Chrome Extensions Blocking Login
1. **Disable extensions** temporarily
2. **Try login**
3. **Re-enable extensions** after successful login

### Privacy/Ad Blockers
- Add discord.com to whitelist
- Disable temporarily for login

### Session Storage Issues (After Cache Clear)
- **Don't clear cache** while logged in
- **Use "Clear browsing data"** selectively
- **Try incognito window** if regular window fails

## Verification Steps

After successful login, you should see:
- ✅ Your Discord home screen with servers
- ✅ Your username in bottom left
- ✅ Server list on left sidebar
- ✅ Ability to send messages

## Security Tips

1. **Enable 2FA** for account security
2. **Save backup codes** in secure location
3. **Don't share login credentials**
4. **Log out** on shared devices
5. **Check active sessions** in User Settings → Privacy & Safety

## Still Having Issues?

1. **Check Discord Status**: https://discordstatus.com
2. **Contact Support**: https://dis.gd/contact
3. **Try Different Device**: Mobile app, different browser
4. **Check Email**: Look for Discord security emails

## Quick Commands

**Open Discord Web:**
```bash
open https://discord.com/login
```

**Clear Discord Cache (Mac App):**
```bash
rm -rf ~/Library/Application\ Support/discord/Cache
```

**Check if Discord is running:**
```bash
ps aux | grep -i discord
```

