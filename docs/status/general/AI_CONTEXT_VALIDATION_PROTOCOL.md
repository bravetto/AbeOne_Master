# 🤖 AI CONTEXT VALIDATION PROTOCOL

**Purpose**: Ensure AI always knows which project is active and prevents drift/bleed  
**Pattern**: OBSERVER × TRUTH × ATOMIC × ONE

---

## 🎯 **PRE-WORK VALIDATION**

### **Step 1: Read Project Status**

**Before ANY code changes**, AI MUST:

```javascript
// Pseudo-code validation
async function validateProjectContext() {
  const currentDir = getCurrentDirectory();
  const projectStatusPath = `${currentDir}/PROJECT_STATUS.md`;
  
  if (!fileExists(projectStatusPath)) {
    WARN: "No PROJECT_STATUS.md found. Check PROJECT_MASTER_INDEX.md";
    return false;
  }
  
  const status = readFile(projectStatusPath);
  
  if (status.status === 'LEGACY' || status.status === 'ARCHIVE') {
    ERROR: `⚠️ DRIFT DETECTED: Working in ${status.status} directory.`;
    ERROR: `Active directory is: ${status.activeDirectory}`;
    ERROR: `Redirecting to active directory...`;
    return false;
  }
  
  return true;
}
```

### **Step 2: Check Master Index**

```javascript
async function validateAgainstMasterIndex() {
  const masterIndex = readFile('PROJECT_MASTER_INDEX.md');
  const currentDir = getCurrentDirectory();
  const projectName = extractProjectName(currentDir);
  
  const project = masterIndex.find(p => 
    p.name === projectName || 
    currentDir.includes(p.activeDirectory)
  );
  
  if (!project) {
    WARN: "Project not found in master index";
    return false;
  }
  
  if (project.status !== 'ACTIVE') {
    ERROR: `Project status is ${project.status}, not ACTIVE`;
    return false;
  }
  
  if (project.activeDirectory !== currentDir) {
    ERROR: `Active directory mismatch. Expected: ${project.activeDirectory}, Got: ${currentDir}`;
    return false;
  }
  
  return true;
}
```

### **Step 3: Validate Boundaries**

```javascript
async function validateBoundaries() {
  const boundaryPath = `${currentDir}/.project-boundary`;
  
  if (!fileExists(boundaryPath)) {
    WARN: "No .project-boundary file found";
    return false;
  }
  
  const boundary = JSON.parse(readFile(boundaryPath));
  
  if (boundary.status !== 'ACTIVE') {
    ERROR: `Boundary status is ${boundary.status}, not ACTIVE`;
    return false;
  }
  
  if (boundary.activeDirectory !== currentDir) {
    ERROR: `Boundary mismatch. Expected: ${boundary.activeDirectory}`;
    return false;
  }
  
  return true;
}
```

---

## 🚨 **DRIFT DETECTION**

### **Detection Rules**

1. **Directory Status Check**
   - If `PROJECT_STATUS.md` says LEGACY/ARCHIVE → DRIFT DETECTED
   - If `.project-boundary` says LEGACY → DRIFT DETECTED

2. **Master Index Mismatch**
   - If current directory ≠ active directory in index → DRIFT DETECTED
   - If project status ≠ ACTIVE in index → DRIFT DETECTED

3. **Version Mismatch**
   - If version < master index version → DRIFT DETECTED
   - If legacy version detected → DRIFT DETECTED

---

## 🔍 **BLEED DETECTION**

### **Detection Rules**

1. **Import Detection**
   ```javascript
   // Check imports for other projects
   const imports = analyzeImports(file);
   for (const imp of imports) {
     if (imp.path.includes('../LEGACY_PROJECT/') || 
         imp.path.includes('../OTHER_ACTIVE_PROJECT/')) {
       WARN: `Potential bleed: Importing from ${imp.path}`);
       WARN: `Verify this is intentional and documented`);
     }
   }
   ```

2. **Pattern Detection**
   ```javascript
   // Detect patterns from other projects
   const patterns = detectPatterns(code);
   const knownPatterns = loadKnownPatterns();
   
   for (const pattern of patterns) {
     if (pattern.sourceProject !== currentProject) {
       WARN: `Pattern from ${pattern.sourceProject} detected`);
       WARN: `Verify intentional reuse and document`);
     }
   }
   ```

3. **File Path Detection**
   ```javascript
   // Check file paths for other projects
   if (filePath.includes('/LEGACY_PROJECT/') || 
       filePath.includes('/OTHER_PROJECT/')) {
     ERROR: `File path references other project: ${filePath}`);
     ERROR: `All work must be in active directory`);
   }
   ```

---

## ✅ **VALIDATION CHECKLIST**

### **Before Starting Work**

- [ ] Read `PROJECT_STATUS.md` in current directory
- [ ] Verify status is ACTIVE (not LEGACY/ARCHIVE)
- [ ] Check `PROJECT_MASTER_INDEX.md` for active project
- [ ] Confirm current directory matches active directory
- [ ] Read `.project-boundary` file
- [ ] Validate boundary status is ACTIVE
- [ ] Report any warnings or errors

### **During Work**

- [ ] No imports from legacy directories
- [ ] No imports from other active projects (unless intentional)
- [ ] No patterns copied from other projects (unless intentional)
- [ ] All changes in active directory only
- [ ] No modifications to legacy directories

### **After Work**

- [ ] Verify changes in correct directory
- [ ] Check for accidental bleed
- [ ] Validate no drift occurred
- [ ] Update project status if needed
- [ ] Report any issues detected

---

## 📋 **AI PROMPT TEMPLATE**

### **Standard Pre-Work Prompt**

```
Before starting work, validate project context:

1. Read PROJECT_STATUS.md in current directory
2. Check PROJECT_MASTER_INDEX.md for active project
3. Verify current directory matches active directory
4. Read .project-boundary file
5. Report any drift/bleed warnings

If drift detected:
- STOP work immediately
- Report drift warning
- Redirect to active directory
- Verify before continuing

If bleed detected:
- Report bleed warning
- Verify intentional
- Document if intentional
- Fix if accidental
```

---

## 🎯 **IMPLEMENTATION**

### **Phase 1: Create Validation Functions** ✅

Create reusable validation functions that can be called before any work.

### **Phase 2: Integrate into AI Prompts** ✅

Add validation protocol to all AI prompts and context windows.

### **Phase 3: Automated Checks** ✅

Create scripts that automatically validate before commits/pushes.

### **Phase 4: Monitoring** ✅

Set up monitoring to detect drift/bleed in real-time.

---

**Pattern**: OBSERVER × TRUTH × ATOMIC × ONE  
**Status**: ✅ **PROTOCOL ACTIVE**

