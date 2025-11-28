#  Quick Resume Guide

**Purpose:** Jump back into work instantly without remembering anything

---

##  HOW TO RESUME WORK

### Step 1: Check Master Index
```bash
cat .projects/INDEX.md
```

### Step 2: Find Your Project
Look for project in the index table

### Step 3: Open Project Card
```bash
cat .projects/[project-name].md
```

### Step 4: Follow "Where We Left Off"
- See what was completed
- Check current state
- Review next steps

### Step 5: Quick Start
Copy commands from project card

---

##  EXAMPLE: Advanced Knock

1. **Check Index:**
   ```bash
   cat .projects/INDEX.md
   ```
   → See Advanced Knock is active

2. **Open Project Card:**
   ```bash
   cat .projects/advanced-knock.md
   ```
   → See where we left off

3. **Quick Start:**
   ```bash
   cd /Users/michaelmataluni/Documents/AbeOne_Master/advanced-knock
   ./launch.sh
   ```
   → System running

4. **Resume Work:**
   - See "Next Steps" in project card
   - Follow the plan
   - Update project card when done

---

##  FINDING PROJECTS

### By Name
```bash
grep -r "Project Name" .projects/
```

### By Status
```bash
grep -r "Status:" .projects/ | grep "Active"
```

### By Date
```bash
ls -lt .projects/*.md
```

---

##  UPDATING PROJECT CARDS

When you finish a work session:

1. **Update "Where We Left Off"**
   - Date
   - What was completed
   - Current state

2. **Update "Next Steps"**
   - What to do next
   - Any blockers
   - Priorities

3. **Update Status**
   - Active/On Hold/Complete

---

##  BEST PRACTICES

1. **Always Update:** Update project card at end of session
2. **Be Specific:** Include exact commands and paths
3. **Note Context:** What you were thinking/planning
4. **Mark Progress:** What's done, what's next

---

**Pattern:** AEYON × RESUME × GUIDE × ONE

