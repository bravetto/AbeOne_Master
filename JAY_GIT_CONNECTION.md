# ∞ Jay's Git Connection - Frictionless Setup ∞

**Pattern:** GIT × CONNECTION × FRICTIONLESS × ONE  
**Frequency:** 999 Hz (AEYON)  
**∞ AbëONE ∞**

---

## 🎯 BEST METHOD: GitHub CLI (Easiest)

### **Step 1: Install GitHub CLI**
```bash
# Mac
brew install gh
```

### **Step 2: Authenticate**
```bash
gh auth login
```

**Follow the prompts:**
- Choose: `GitHub.com`
- Choose: `HTTPS`
- Choose: `Login with a web browser`
- Press Enter → Browser opens → Authorize
- Done! ✅

### **Step 3: Clone the Master Repository**
```bash
# Clone from bravetto organization
gh repo clone bravetto/AbeOne_Master AbeOne_Master
```

**That's it!** You're connected to the master repository and ready to go.

---

## 🔄 ALTERNATIVE: SSH Keys (If you prefer)

### **Step 1: Generate SSH Key**
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
# Press Enter 3 times (use defaults, no passphrase needed)
```

### **Step 2: Add to GitHub**
```bash
# Copy your public key
cat ~/.ssh/id_ed25519.pub | pbcopy  # Mac
# Or: cat ~/.ssh/id_ed25519.pub

# Then:
# 1. Go to: https://github.com/settings/keys
# 2. Click "New SSH key"
# 3. Paste your key
# 4. Click "Add SSH key"
```

### **Step 3: Test**
```bash
ssh -T git@github.com
# Should see: "Hi username! You've successfully authenticated..."
```

### **Step 4: Clone**
```bash
git clone git@github.com:BravettoFrontendTeam/abe-touch.git AbeOne_Master
```

---

## ✅ VERIFY IT WORKED

```bash
cd AbeOne_Master
git status
# Should show: "On branch main" or similar
```

---

## 🆘 TROUBLESHOOTING

**"gh: command not found"**  
→ Install: `brew install gh`

**"Permission denied"**  
→ Run `gh auth login` again

**"Repository not found"**  
→ Make sure you're authenticated: `gh auth status`

---

## 📋 QUICK REFERENCE

**GitHub CLI (Recommended):**
```bash
brew install gh
gh auth login
# Clone master repository from bravetto organization
gh repo clone bravetto/AbeOne_Master AbeOne_Master
```

**SSH (Alternative):**
```bash
ssh-keygen -t ed25519 -C "email@example.com"
cat ~/.ssh/id_ed25519.pub | pbcopy
# Add to GitHub, then:
# Clone master repository from bravetto organization
git clone git@github.com:bravetto/AbeOne_Master.git AbeOne_Master
```

**Note:** The master repository is in the `bravetto` GitHub organization and contains the complete `AbeOne_Master` structure with all repositories.

---

**LOVE = LIFE = ONE**  
**∞ AbëONE ∞**

