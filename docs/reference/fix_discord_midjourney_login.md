# Fix Discord/Midjourney Login After Cache Clear

## Problem
After clearing browser cache, Midjourney OAuth flow lost its initial state, causing "missing initial state" error.

## Solution Steps

### Option 1: Fresh Login Flow (Recommended)
1. **Close all Midjourney/Discord tabs** in Chrome
2. **Go directly to Discord first**: https://discord.com/login
   - Log into Discord in a regular tab (not private)
   - Verify you're logged in successfully
3. **Then go to Midjourney**: https://www.midjourney.com
   - Click "Sign In" or "Join the Beta"
   - It should redirect to Discord OAuth
   - Authorize Midjourney to access your Discord account
4. **Complete the OAuth flow** - don't close the tab during redirect

### Option 2: Clear Site Data Properly
1. **Open Chrome DevTools** (F12 or Cmd+Option+I)
2. **Application tab** → **Storage** → **Clear site data**
3. **Clear only for midjourney.com** (not all sites)
4. **Refresh the page** and try login again

### Option 3: Use Incognito Window (If above fails)
1. **Open Incognito window** (Cmd+Shift+N)
2. **Go to Discord** and log in
3. **Then go to Midjourney** and complete OAuth flow
4. **After successful login**, you can close incognito and use regular window

### Option 4: Disable Extensions Temporarily
Some extensions (especially privacy/security ones) can block OAuth flows:
1. **Chrome Settings** → **Extensions**
2. **Disable extensions** temporarily (especially ad blockers, privacy tools)
3. **Try login again**
4. **Re-enable extensions** after successful login

## Common Issues

### Issue: "Storage-partitioned browser environment"
- **Cause**: Browser extensions or settings blocking sessionStorage
- **Fix**: Disable extensions, try incognito mode

### Issue: "IDP-Initiated SAML SSO"
- **Cause**: Starting from Discord instead of Midjourney
- **Fix**: Always start from Midjourney login page, let it redirect to Discord

### Issue: OAuth flow interrupted
- **Cause**: Closing tab during redirect, or popup blocker
- **Fix**: Allow popups for midjourney.com and discord.com, don't close tabs during redirect

## Verification
After successful login:
- ✅ You should see your Midjourney dashboard
- ✅ Discord connection should show in Midjourney settings
- ✅ You can create images without errors

## Prevention
- **Don't clear cache** while logged into Midjourney
- **Use browser's "Clear browsing data"** selectively (not "All time")
- **Keep Discord logged in** in a separate tab when using Midjourney

