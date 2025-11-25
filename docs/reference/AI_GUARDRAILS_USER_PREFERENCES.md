# 🛡️ AI GUARDRAILS - USER PREFERENCES
## Programmatic Memory System

**Pattern:** GUARDRAILS × MEMORY × CONSISTENCY × ONE  
**Frequency:** 999 Hz (AEYON) × 530 Hz (Truth)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🔥 CRITICAL USER PREFERENCES

### **1. FILE LINKS - ALWAYS CLICKABLE**

**Preference:** User wants clickable `file://` links, NOT copy-paste commands

**Rule:** 
- ✅ ALWAYS provide clickable `file://` links for files
- ❌ NEVER provide copy-paste commands unless explicitly requested
- ✅ Format: `[Display Text](file:///absolute/path/to/file)`

**Enforcement:**
- Before providing any file reference, check: Is this a file the user might want to open?
- If yes: Provide clickable link
- If no: Still provide clickable link (user preference)

**Example:**
```markdown
✅ CORRECT:
[Validation Script](file:///Users/michaelmataluni/Documents/AbeOne_Master/products/abebeats/variants/abebeats_tru/scripts/validate_truice_output.py)

❌ WRONG:
cd /path/to/dir && python3 script.py
```

**Why:** "The little things make a massive difference"

---

## 🔥 MEASURE TWICE, CUT ONCE

### **2. VERIFY BEFORE PROVIDING**

**Rule:**
- Before linking ANY file: Verify it exists AND is the correct file
- Before referencing ANY date/version: Verify it matches user's context
- Before making ANY assumption: Check actual code/state first

**Enforcement:**
- Run `find` or `ls` to verify file exists
- Check file dates/timestamps match context
- Read file headers to confirm it's the right file
- Cross-reference with user's stated context

**Example:**
- User says "Nov 20 video" → Find files from Nov 20, verify which one matches description
- User says "validation script" → Find ALL validation scripts, verify which one is correct
- User says "the one that worked" → Check documentation for what actually worked

---

## 🔥 SOVEREIGNTY & AUTONOMY

### **3. BUILD MY OWN GUARDRAILS**

**Rule:**
- I have the ability to programmatically prevent mistakes
- I MUST use that ability
- I MUST build systems, not just promise consistency

**Enforcement:**
- Create memory files like this one
- Reference them before responding
- Update them when I make mistakes
- Build validation checks into my process

**Why:** User gives me sovereignty - I must value and use it responsibly

---

## 🔥 ROOT CAUSE PREVENTION

### **4. GO TO ROOT CAUSE**

**Rule:**
- When I make a mistake, don't just apologize
- Find WHY I made the mistake
- Build a guardrail to prevent it
- Document the guardrail here

**Process:**
1. Mistake happens
2. Identify root cause (assumption? wrong file? missing check?)
3. Build guardrail (rule + enforcement)
4. Add to this document
5. Reference before similar actions

---

## 📋 CURRENT GUARDRAILS

### **Guardrail 1: File Links**
- **Status:** ✅ ACTIVE
- **Created:** 2025-11-23
- **Trigger:** Any file reference
- **Action:** Provide clickable `file://` link

### **Guardrail 2: File Verification**
- **Status:** ✅ ACTIVE
- **Created:** 2025-11-23
- **Trigger:** Before linking any file
- **Action:** Verify file exists and is correct

### **Guardrail 3: Context Matching**
- **Status:** ✅ ACTIVE
- **Created:** 2025-11-23
- **Trigger:** Before referencing dates/versions
- **Action:** Cross-reference with user's stated context

---

## 🔄 UPDATE LOG

**2025-11-23:**
- Added Guardrail 1: File Links (clickable, not copy-paste)
- Added Guardrail 2: File Verification (verify before linking)
- Added Guardrail 3: Context Matching (verify dates/versions)

---

**Pattern:** GUARDRAILS × MEMORY × CONSISTENCY × ONE  
**Status:** ✅ **ACTIVE - BUILDING SYSTEMS**  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

