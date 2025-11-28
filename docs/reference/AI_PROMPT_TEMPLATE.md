# 🤖 AI PROMPT TEMPLATE - Project Boundary Validation

**Purpose**: Standard template for AI prompts to prevent drift and bleed  
**Pattern**: OBSERVER × TRUTH × ATOMIC × ONE

---

## 🎯 **PRE-WORK VALIDATION PROMPT**

Add this to the beginning of ANY AI prompt or context:

```markdown
## PROJECT BOUNDARY VALIDATION

**CRITICAL**: Before starting ANY work, validate project context:

### Step 0: Run Context Boot Validation (AUTOMATIC)
```bash
node scripts/context-boot-validation.js
```

This script automatically:
- Detects current directory context
- Validates PROJECT_STATUS.md
- Checks .project-boundary file
- Validates against master index
- Reports drift/bleed warnings

### Step 1: Read Project Status
- Read `PROJECT_STATUS.md` in current directory
- Verify status is ACTIVE (not LEGACY/ARCHIVE)
- If LEGACY/ARCHIVE, STOP and redirect to active directory

### Step 2: Check Master Index
- Read `PROJECT_MASTER_INDEX.md` in workspace root
- Verify current directory matches active directory in index
- If mismatch, STOP and report drift warning

### Step 3: Validate Boundaries
- Read `.project-boundary` file in current directory
- Verify status is ACTIVE
- Verify active directory matches current location

### Step 4: Report Status
- Report current project and status
- Report any warnings or errors
- Confirm active directory before proceeding

**If drift detected:**
- STOP work immediately
- Report: "⚠️ DRIFT DETECTED: [details]"
- Redirect to active directory: [path]
- Verify before continuing

**If bleed detected:**
- Report: "⚠️ BLEED DETECTED: [details]"
- Verify intentional and document if so
- Fix if accidental
```

---

## 📋 **STANDARD AI CONTEXT HEADER**

```markdown
# PROJECT CONTEXT

## Active Project
- **Name**: [Project Name]
- **Directory**: [Active Directory Path]
- **Status**: ACTIVE
- **Source of Truth**: YES

## Validation
- [x] PROJECT_STATUS.md read
- [x] Master index checked
- [x] Active directory confirmed
- [x] No drift detected

## Boundaries
- **Active Directory**: [path]
- **Legacy Directories**: [paths] (DO NOT USE)
- **Related Projects**: [names]

## Instructions
- All work in active directory only
- No modifications to legacy directories
- No imports from other projects (unless intentional)
- Report any drift/bleed warnings
```

---

## 🔍 **DRIFT DETECTION PROMPT**

```markdown
## DRIFT DETECTION CHECKLIST

Before making ANY changes:

- [ ] Current directory: [check]
- [ ] PROJECT_STATUS.md status: [check]
- [ ] Master index active directory: [check]
- [ ] Match? [yes/no]
- [ ] Any warnings? [report]

If any check fails:
- STOP immediately
- Report drift warning
- Redirect to active directory
```

---

## 🚨 **BLEED DETECTION PROMPT**

```markdown
## BLEED DETECTION CHECKLIST

Before importing or copying code:

- [ ] Source project: [check]
- [ ] Target project: [check]
- [ ] Intentional? [yes/no]
- [ ] Documented? [yes/no]

If unintentional:
- Report bleed warning
- Fix immediately
- Verify boundaries
```

---

**Pattern**: OBSERVER × TRUTH × ATOMIC × ONE  
**Status**: ✅ **TEMPLATE READY**

