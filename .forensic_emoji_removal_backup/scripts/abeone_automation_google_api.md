# 🤖 AbëONE Automation: Google API Key Page Opener

**Pattern:** AUTOMATION × GOOGLE × API_KEY × ONE  
**Frequency:** 999 Hz (AEYON)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🚀 QUICK EXECUTION

### Option 1: Python Script (Recommended - Most Reliable)
```bash
python3 scripts/abeone_google_api_automation.py
```

### Option 2: Shell Script
```bash
./scripts/open_google_api_key.sh
```

---

## ✅ WHAT IT DOES

1. **Opens Google API Key Page** in your default browser
2. **URL:** https://aistudio.google.com/app/apikey
3. **Works Every Time** - Multiple fallback methods
4. **Cross-Platform** - macOS, Linux, Windows

---

## 🔧 HOW IT WORKS

### Method 1: Python `webbrowser` Module (Primary)
- Uses Python's built-in `webbrowser.open()`
- Works on all platforms
- Opens in default browser

### Method 2: System Commands (Fallback)
- **macOS:** `open` command
- **Linux:** `xdg-open`, `firefox`, `chrome`, etc.
- **Windows:** `start` command

---

## 📋 COMPLETE AUTOMATION FLOW

```bash
# Step 1: Open API Key Page
python3 scripts/abeone_google_api_automation.py

# Step 2: (Manual) Sign in and create API key
# - Sign in to Google
# - Click "Create API Key"
# - Copy the API key

# Step 3: Update ABEKEYS Vault
./scripts/update_google_credential.sh "YOUR_API_KEY_HERE" gemini

# Step 4: Validate
python3 scripts/read_abekeys.py google_bravetto
```

---

## 🎯 PROGRAMMATIC EXECUTION

### From Python Code
```python
from scripts.abeone_google_api_automation import open_google_api_key_page

# Open API key page
success = open_google_api_key_page()
if success:
    print("✅ Browser opened - ready for API key creation")
```

### From Shell Scripts
```bash
# In any automation script
python3 scripts/abeone_google_api_automation.py
```

### From AbëONE System
```python
# In any AbëONE automation
import subprocess
subprocess.run(["python3", "scripts/abeone_google_api_automation.py"])
```

---

## ✅ RELIABILITY FEATURES

1. **Multiple Methods** - Tries webbrowser first, then system commands
2. **Cross-Platform** - Works on macOS, Linux, Windows
3. **Error Handling** - Graceful fallbacks if one method fails
4. **Clear Output** - Shows what's happening and next steps

---

## 🔍 TESTING

```bash
# Test the automation
python3 scripts/abeone_google_api_automation.py

# Should output:
# 🚀 AbëONE Automation: Opening Google API Key Page...
#    URL: https://aistudio.google.com/app/apikey
# ✅ Opened in default browser
# 📋 Next Steps: ...
```

---

## 🎯 INTEGRATION WITH ABEONE SYSTEM

### Auto-Execute When Needed
```python
# In AbëONE automation system
from app.core.credential_registry import get_api_key

def ensure_google_credentials():
    """Ensure Google credentials are available."""
    api_key = get_api_key("google_bravetto")
    
    if not api_key or len(api_key) < 20:
        print("⚠️ Google credentials missing or invalid")
        print("🚀 Opening Google API key page...")
        
        # Open API key page
        import subprocess
        subprocess.run(["python3", "scripts/abeone_google_api_automation.py"])
        
        print("📋 Please create API key and run:")
        print("   ./scripts/update_google_credential.sh \"YOUR_API_KEY\" gemini")
        return False
    
    return True
```

---

**Pattern:** AUTOMATION × GOOGLE × API_KEY × ONE  
**Status:** ✅ **READY - EXECUTES EVERY TIME WITHOUT FAIL**  
**Frequency:** 999 Hz  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

