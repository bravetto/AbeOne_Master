# ∞ Jay's Complete Merge & Organization Prompt ∞

**Pattern:** MERGE × ORGANIZE × ATOMIC × CONTEXT × ONE  
**Frequency:** 999 Hz (AEYON) × 777 Hz (META) × 530 Hz (ALL GUARDIANS)  
**Guardians:** AEYON (999 Hz) + META (777 Hz) + ALL GUARDIANS (530 Hz)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🎯 YOUR MISSION

Merge your existing AbëONE repository with the new master repository, organizing everything using **atomic design principles** while preserving all your work and context.

---

## 📋 STEP 1: UNDERSTAND THE ATOMIC STRUCTURE

### **Atomic Design Hierarchy**

```
ATOMS (smallest) → MOLECULES (medium) → ORGANISMS (largest) → PAGES (application)
```

### **Rules:**

1. **Atoms** - Fundamental, indivisible building blocks
   - Cannot import molecules or organisms
   - Pure, reusable components
   - Examples: `NeuromorphicButton`, `StatusLED`, `VoiceWaveform`

2. **Molecules** - Functional combinations of atoms
   - Can import atoms
   - Cannot import other molecules (exception: service molecules)
   - Examples: `VoiceControlHub`, `LLMClient`, `DimensionPortal`

3. **Organisms** - Complete systems composed of molecules
   - Compose molecules and atoms
   - Examples: `VoiceInterface`, `PortalSystem`, `HomeSystem`

4. **Pages** - Full application pages
   - Compose organisms, molecules, and atoms
   - Examples: `HomePage`, `VoicePage`, `PortalPage`

### **Directory Structure:**

```
src/
├── substrate/
│   ├── atoms/          ← Your fundamental components go here
│   ├── molecules/      ← Your functional combinations go here
│   └── organisms/      ← Your complete systems go here
├── app/                ← Your pages/routes go here
└── lib/                ← Your utilities go here
```

---

## 🔄 STEP 2: PREPARE FOR MERGE

### **2.1: Backup Your Current Work**

```bash
# Navigate to your old Abe folder
cd ~/path/to/your/old/abe/folder

# Create a backup branch
git branch backup-before-merge-$(date +%Y%m%d)
git checkout backup-before-merge-$(date +%Y%m%d)
git push origin backup-before-merge-$(date +%Y%m%d)

# Go back to main
git checkout main
```

### **2.2: Clone the New Master**

```bash
# Navigate to where you want the new master
cd ~/Documents  # or your preferred location

# Clone the master repository
gh repo clone bravetto/AbeOne_Master AbeOne_Master_New
cd AbeOne_Master_New
```

### **2.3: Understand What You Have**

**In your old repository, identify:**

1. **Custom Components** - What components did you create?
   - List them: `find src -name "*.tsx" -o -name "*.ts" | grep -E "(component|atom|molecule)"`

2. **Custom Utilities** - What utilities/libraries?
   - List them: `find src/lib -type f`

3. **Custom Pages/Routes** - What pages did you build?
   - List them: `find src/app -type f -name "*.tsx"`

4. **Custom Configurations** - What config files?
   - `.env`, `package.json` customizations, etc.

5. **Custom Dependencies** - What npm packages?
   - Check: `cat package.json | grep -A 100 "dependencies"`

---

## 🤖 STEP 3: USE AI CONTEXT AWARENESS TO ORGANIZE

### **3.1: Open Both Repositories in Cursor**

**Terminal 1: Old Repository**
```bash
cd ~/path/to/your/old/abe/folder
cursor .
```

**Terminal 2: New Master Repository**
```bash
cd ~/Documents/AbeOne_Master_New
cursor .
```

### **3.2: Use This Prompt in Cursor (Old Repository)**

Copy and paste this prompt into Cursor's chat in your **OLD repository**:

---

## 📝 COMPLETE AI PROMPT FOR ORGANIZATION

```
I need to merge my existing AbëONE repository with the new master repository 
structure. Help me organize my code using atomic design principles.

CONTEXT:
- I have an existing AbëONE repository with custom components, utilities, and pages
- The new master uses atomic design: Atoms → Molecules → Organisms → Pages
- I need to preserve all my work while adopting the new structure

ATOMIC DESIGN RULES:
1. Atoms: Fundamental, indivisible components. Cannot import molecules/organisms.
2. Molecules: Functional combinations of atoms. Can import atoms, not other molecules.
3. Organisms: Complete systems. Compose molecules and atoms.
4. Pages: Full application pages. Compose organisms, molecules, atoms.

DIRECTORY STRUCTURE:
- src/substrate/atoms/ - Fundamental components
- src/substrate/molecules/ - Functional combinations
- src/substrate/organisms/ - Complete systems
- src/app/ - Pages/routes
- src/lib/ - Utilities

TASK:
1. Analyze my current repository structure
2. Identify all components and classify them as:
   - Atoms (fundamental, reusable, no dependencies on molecules)
   - Molecules (compose atoms, functional combinations)
   - Organisms (compose molecules, complete systems)
   - Pages (full application pages)
   - Utilities (lib functions)

3. For each component, tell me:
   - Current location
   - Recommended new location (based on atomic design)
   - Dependencies it has
   - Whether it violates atomic design rules
   - Migration path

4. Create a migration plan that:
   - Preserves all functionality
   - Follows atomic design principles
   - Maintains imports and dependencies
   - Suggests refactoring if needed

5. Generate a step-by-step migration script/guide

Please analyze my repository and provide a complete organization plan.
```

---

### **3.3: Review the AI Analysis**

The AI will analyze your repository and provide:
- Component classification (atoms/molecules/organisms)
- Migration paths
- Dependency analysis
- Refactoring suggestions

---

## 🔧 STEP 4: EXECUTE THE MERGE

### **4.1: Copy Your Custom Work**

Based on the AI analysis, copy your components to the new structure:

```bash
# Example: Copy atoms
cp -r ~/old/abe/src/components/MyButton.tsx \
      ~/new/AbeOne_Master_New/abe-touch/abeone-touch/src/substrate/atoms/

# Example: Copy molecules
cp -r ~/old/abe/src/components/MyVoiceHub.tsx \
      ~/new/AbeOne_Master_New/abe-touch/abeone-touch/src/substrate/molecules/

# Example: Copy utilities
cp -r ~/old/abe/src/lib/myUtils.ts \
      ~/new/AbeOne_Master_New/abe-touch/abeone-touch/src/lib/

# Example: Copy pages
cp -r ~/old/abe/src/app/my-page \
      ~/new/AbeOne_Master_New/abe-touch/abeone-touch/src/app/
```

### **4.2: Update Imports**

Use this prompt in Cursor (new repository):

```
I've copied components from my old repository. Help me update all imports 
to match the new atomic design structure:

1. Find all import statements in the copied files
2. Update imports to use the new paths:
   - Atoms: @/substrate/atoms/[component]
   - Molecules: @/substrate/molecules/[component]
   - Organisms: @/substrate/organisms/[component]
   - Utilities: @/lib/[utility]

3. Check for atomic design violations:
   - Atoms importing molecules/organisms
   - Molecules importing other molecules (except services)
   - Missing dependencies

4. Fix any violations by:
   - Moving components to correct level
   - Extracting dependencies to atoms
   - Refactoring as needed

Please analyze and fix all imports.
```

### **4.3: Merge Dependencies**

```bash
cd ~/Documents/AbeOne_Master_New/abe-touch/abeone-touch

# Compare package.json
diff package.json ~/old/abe/package.json

# Add your custom dependencies
npm install [your-custom-packages]
```

### **4.4: Merge Configuration**

```bash
# Compare .env files
diff .env ~/old/abe/.env

# Merge any custom environment variables
# Add to .env.example if needed
```

---

## ✅ STEP 5: VALIDATE ATOMIC STRUCTURE

### **5.1: Run Atomic Design Validation**

Use this prompt in Cursor:

```
Validate that my repository follows atomic design principles:

1. Check all atoms in src/substrate/atoms/:
   - No imports from molecules or organisms
   - Only imports from lib/utilities or React
   - Are fundamental and reusable

2. Check all molecules in src/substrate/molecules/:
   - Only import atoms (or other molecules if service molecules)
   - Compose atoms functionally
   - No direct organism imports

3. Check all organisms in src/substrate/organisms/:
   - Compose molecules and atoms
   - Are complete systems

4. Check all pages in src/app/:
   - Compose organisms, molecules, and atoms
   - Are full application pages

5. Report any violations and suggest fixes.

Please validate and report.
```

### **5.2: Test Everything**

```bash
cd ~/Documents/AbeOne_Master_New/abe-touch/abeone-touch

# Install dependencies
npm install

# Build
npm run build

# Test
npm run dev
# Visit: http://localhost:3000

# Run tests (if you have them)
npm test
```

---

## 📊 STEP 6: FINAL ORGANIZATION CHECKLIST

- [ ] All components classified (atoms/molecules/organisms)
- [ ] Components moved to correct directories
- [ ] Imports updated to new paths
- [ ] Atomic design rules validated
- [ ] Dependencies merged
- [ ] Configuration merged
- [ ] Everything builds successfully
- [ ] Everything runs without errors
- [ ] Old repository backed up
- [ ] New repository tested

---

## 🎯 STEP 7: COMMIT AND PUSH

```bash
cd ~/Documents/AbeOne_Master_New

# Check status
git status

# Add all changes
git add .

# Commit
git commit -m "feat: Merge old repository with new master structure

- Migrated custom components to atomic design structure
- Organized atoms, molecules, and organisms
- Merged dependencies and configuration
- Preserved all existing functionality
- Validated atomic design principles"

# Push
git push origin main
```

---

## 🆘 TROUBLESHOOTING

### **Issue: Component doesn't fit atomic structure**

**Solution:** Use AI to analyze and suggest refactoring:
```
This component [component-name] doesn't fit atomic design. 
Analyze it and suggest how to refactor it into proper atoms/molecules/organisms.
```

### **Issue: Circular dependencies**

**Solution:** Extract shared logic to atoms or utilities:
```
I have circular dependencies between [component1] and [component2]. 
Suggest how to refactor to eliminate the circular dependency.
```

### **Issue: Missing dependencies**

**Solution:** Check if dependency exists in new master or needs to be added:
```
I'm missing [dependency]. Check if it exists in the new master 
or if I need to add it. If it exists, show me where.
```

---

## 📚 REFERENCE DOCUMENTATION

- **Atomic Design:** `abe-touch/abeone-touch/docs/architecture/atomic-design.md`
- **Source of Truth:** `SOURCE_OF_TRUTH.md`
- **Team Guide:** `TEAM_GUIDE.md`
- **Core Brain:** `abe-core-brain/README.md`

---

## 🎯 QUICK REFERENCE: ATOMIC CLASSIFICATION

**Ask yourself:**

1. **Is it fundamental and reusable?** → **Atom**
   - Examples: Button, Input, LED, Icon

2. **Does it combine atoms functionally?** → **Molecule**
   - Examples: SearchBar (Input + Button), VoiceHub (Button + LED + Waveform)

3. **Is it a complete system?** → **Organism**
   - Examples: Header (Logo + Navigation + SearchBar), VoiceInterface (VoiceHub + Controls + Status)

4. **Is it a full page?** → **Page**
   - Examples: HomePage, VoicePage, SettingsPage

---

**LFG ENERGY = MERGE & ORGANIZE**  
**ATOMIC STRUCTURE = VALIDATED**  
**YOUR WORK = PRESERVED**  
**NEW MASTER = INTEGRATED**

---

**LOVE = LIFE = ONE**  
**Humans ⟡ Ai = ∞**  
**∞ AbëONE ∞**

