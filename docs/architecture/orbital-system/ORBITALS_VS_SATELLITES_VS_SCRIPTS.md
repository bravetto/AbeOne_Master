# 🌌 ORBITALS vs SATELLITES vs SCRIPTS - ARCHITECTURAL GUIDANCE

**Pattern:** ARCHITECTURE × ORGANIZATION × CLARITY × ONE  
**Frequency:** 777 Hz (META) × 530 Hz (Truth)  
**Guardians:** META (777 Hz) + YAGNI (530 Hz)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🎯 EXECUTIVE SUMMARY

**Decision Framework:**
- **Orbitals** = Major deployable systems/products (Planets)
- **Satellites** = Reusable utility systems/tools (Moons)
- **Scripts** = One-off utilities, automation, helpers (Tools)

**Key Principle:** Only elevate to orbital/satellite if it becomes a **reusable system**. Most scripts should stay as scripts.

---

## 🪐 ORBITALS (Planets - Major Systems)

### **Definition:**
Orbitals are **major, deployable systems/products** that orbit around the AbëONE kernel. They are self-contained, have their own lifecycle, and can be deployed independently.

### **Characteristics:**
- ✅ **Deployable** - Can be deployed as a service/product
- ✅ **Self-contained** - Has its own structure, configs, adapters
- ✅ **Orbit-Spec v1.0 compliant** - Follows orbital specification
- ✅ **Major system** - Significant functionality/product
- ✅ **Independent lifecycle** - Can be versioned, released independently

### **Examples:**
```
orbitals/
├── AIGuards-Backend-orbital/          # Guardian microservices cluster
├── AiGuardian-Chrome-Ext-orbital/     # Chrome extension product
├── AiGuardian-Sales-Page-orbital/     # Sales page product
├── AbeBEATs_Clean-orbital/            # Audio beat generation product
├── AbeTRUICE-orbital/                 # Video intelligence pipeline
├── Abeflows-orbital/                  # Workflow automation product
├── EMERGENT_OS-orbital/               # Core operating system
├── Advanced-Knock-orbital/            # Advanced convergence system
└── spec-kit-orbital/                  # Spec-driven development toolkit
```

### **When to Create an Orbital:**
- ✅ Building a **deployable product/service**
- ✅ Creating a **major system** with its own lifecycle
- ✅ Need **independent versioning/releases**
- ✅ System has **multiple components/modules**
- ✅ System needs **orbital adapters** (bus, guardians, kernel, module)

### **Orbital Structure:**
```
orbital-name-orbital/
├── adapters/              # Orbital adapters (bus, guardians, kernel, module)
├── config/                # Configuration files
├── deploy/                # Deployment scripts
├── docs/                  # Documentation
├── src/                   # Source code
├── tests/                 # Tests
├── module_manifest.json   # Module manifest
└── README.md              # Orbital README
```

---

## 🛰️ SATELLITES (Moons - Supporting Systems)

### **Definition:**
Satellites are **reusable utility systems/tools** that enhance orbital functionality. They provide shared services, templates, or tools that multiple orbitals can use.

### **Characteristics:**
- ✅ **Reusable** - Used by multiple orbitals/systems
- ✅ **Utility-focused** - Provides specific utility/service
- ✅ **Supporting role** - Enhances orbital functionality
- ✅ **Shared resource** - Can be imported/used by orbitals
- ✅ **Tool/system** - More than a simple script

### **Examples:**
```
satellites/
├── TemplateHeavenSatellite/    # Template repository (reusable templates)
├── WorkflowsSatellite/         # Workflow orchestration (reusable workflows)
├── WebIDESatellite/           # Web IDE system (reusable IDE)
├── AbeONESourceSatellite/     # Source management (reusable source tools)
├── AbëKEYsSatellite/          # Key management system (reusable key vault)
├── BryanSatellite/            # Marketing automation (reusable marketing tools)
└── GZ360Satellite/            # 360-degree system (reusable 360 tools)
```

### **When to Create a Satellite:**
- ✅ Building a **reusable utility/tool** used by multiple systems
- ✅ Creating a **shared service** (templates, workflows, tools)
- ✅ Need **cross-orbital functionality**
- ✅ System provides **reusable components**
- ✅ More than a script, less than a full product

### **Satellite Structure:**
```
satellite-name-satellite/
├── adapters/              # Satellite adapters
├── config/                # Configuration files
├── deploy/                # Deployment scripts
├── docs/                  # Documentation
├── src/                   # Source code
├── tests/                 # Tests
├── module_manifest.json   # Module manifest
└── README.md              # Satellite README
```

---

## 🛠️ SCRIPTS (Tools - Utility Scripts)

### **Definition:**
Scripts are **one-off utilities, automation tools, and helpers** that perform specific tasks. They are simple, focused, and don't need the overhead of orbital/satellite structure.

### **Characteristics:**
- ✅ **Simple** - Single purpose, focused functionality
- ✅ **Utility** - Performs specific task/automation
- ✅ **No overhead** - Doesn't need orbital/satellite structure
- ✅ **One-off** - Typically used directly, not as a library
- ✅ **Helper** - Supports other systems, doesn't need adapters

### **Examples:**
```
scripts/
├── heal_hard_drive.py              # Hard drive healing utility
├── heal_all_gaps.py                # Gap healing utility
├── validate_project_boundaries.js  # Validation utility
├── gentle-drift-guardian.js        # Drift monitoring utility
├── create-engine.py                # Creation engine
├── converge-engine.py               # Convergence engine
└── hard_drive_healing/             # Healing system (organized scripts)
```

### **When to Keep as Scripts:**
- ✅ **Simple utility** - Single purpose, focused task
- ✅ **One-off automation** - Specific automation task
- ✅ **Helper tool** - Supports other systems
- ✅ **No reuse needed** - Used directly, not as library
- ✅ **Quick tool** - Doesn't warrant orbital/satellite overhead

### **Script Organization:**
```
scripts/
├── script-name.py           # Simple script
├── utility-name.js          # Simple utility
├── system-name/             # Organized script system (if needed)
│   ├── detection/
│   ├── diagnosis/
│   ├── recovery/
│   └── __init__.py
└── modules/                 # Shared modules (if needed)
```

---

## 🤔 DECISION FRAMEWORK

### **Should I Create an Orbital?**

**Ask yourself:**
1. Is this a **deployable product/service**?
2. Does it need **independent versioning/releases**?
3. Does it have **multiple components/modules**?
4. Does it need **orbital adapters**?
5. Is it a **major system** with its own lifecycle?

**If YES to 3+ → Create Orbital**

### **Should I Create a Satellite?**

**Ask yourself:**
1. Is this a **reusable utility/tool**?
2. Will **multiple systems** use it?
3. Does it provide **shared services**?
4. Is it more than a script but less than a product?
5. Does it need **cross-orbital functionality**?

**If YES to 3+ → Create Satellite**

### **Should I Keep as Scripts?**

**Ask yourself:**
1. Is this a **simple utility**?
2. Is it **one-off automation**?
3. Does it **support other systems**?
4. Is it used **directly, not as library**?
5. Does it need **quick execution**?

**If YES to 3+ → Keep as Script**

---

## 📊 COMPARISON MATRIX

| Aspect | Orbital | Satellite | Script |
|--------|---------|-----------|--------|
| **Purpose** | Deployable product/service | Reusable utility/tool | One-off utility/automation |
| **Complexity** | High (multiple components) | Medium (focused system) | Low (single purpose) |
| **Reusability** | Self-contained | Shared across systems | Direct use |
| **Structure** | Full orbital structure | Satellite structure | Simple file/folder |
| **Adapters** | Required | Optional | Not needed |
| **Lifecycle** | Independent versioning | Shared versioning | No versioning |
| **Deployment** | Deployable service | Shared resource | Direct execution |
| **Examples** | Backend, Chrome Ext | Templates, Workflows | Validation, Healing |

---

## 🎯 SPECIFIC GUIDANCE

### **Hard Drive Healing System**

**Current:** `scripts/hard_drive_healing/` (Script system)

**Should it be:**
- ❌ **Orbital?** No - Not a deployable product
- ✅ **Satellite?** Maybe - If other systems need disk healing
- ✅ **Script?** Yes - Current location is correct

**Recommendation:** Keep as script system. If multiple orbitals need disk healing, consider creating `DiskHealingSatellite`.

### **Gap Healing System**

**Current:** `scripts/heal_all_gaps.py` (Script)

**Should it be:**
- ❌ **Orbital?** No - Not a deployable product
- ✅ **Satellite?** Maybe - If other systems need gap healing
- ✅ **Script?** Yes - Current location is correct

**Recommendation:** Keep as script. If multiple orbitals need gap healing, consider creating `GapHealingSatellite`.

### **Create Engine**

**Current:** `scripts/create-engine.py` (Script)

**Should it be:**
- ❌ **Orbital?** No - Not a deployable product
- ✅ **Satellite?** Yes - Used by multiple systems
- ❌ **Script?** Maybe - Could be elevated

**Recommendation:** Consider `CreationSatellite` if used by multiple orbitals.

### **Validation Scripts**

**Current:** `scripts/validate_*.py` (Multiple scripts)

**Should they be:**
- ❌ **Orbital?** No - Not deployable products
- ✅ **Satellite?** Yes - Used by multiple systems
- ❌ **Script?** Maybe - Could be organized

**Recommendation:** Consider `ValidationSatellite` to organize validation tools.

---

## 🚀 MIGRATION GUIDELINES

### **Script → Satellite Migration**

**When to migrate:**
- Script is used by **3+ orbitals/systems**
- Script provides **reusable functionality**
- Script needs **shared configuration**
- Script needs **cross-system integration**

**Migration steps:**
1. Create `satellites/ScriptNameSatellite/`
2. Move script to `satellites/ScriptNameSatellite/src/`
3. Add adapters if needed
4. Add `module_manifest.json`
5. Update imports in orbitals

### **Script → Orbital Migration**

**When to migrate:**
- Script becomes a **deployable product/service**
- Script needs **independent versioning**
- Script has **multiple components**
- Script needs **full orbital structure**

**Migration steps:**
1. Create `orbitals/ScriptName-orbital/`
2. Move script to `orbitals/ScriptName-orbital/src/`
3. Add full orbital structure (adapters, config, deploy)
4. Add `module_manifest.json`
5. Update imports in orbitals

---

## ✅ BEST PRACTICES

### **1. Start Simple**
- ✅ Start as **script** if unsure
- ✅ Elevate to **satellite** when reused
- ✅ Elevate to **orbital** when it becomes a product

### **2. YAGNI Principle**
- ✅ Don't create orbital/satellite **until needed**
- ✅ Keep scripts simple **until complexity requires structure**
- ✅ Avoid premature abstraction

### **3. Organization**
- ✅ Group related scripts in **folders** (`hard_drive_healing/`)
- ✅ Use **modules** for shared code (`scripts/modules/`)
- ✅ Keep **utilities** organized (`scripts/utilities/`)

### **4. Documentation**
- ✅ Document **purpose** clearly
- ✅ Explain **when to use** orbital/satellite/script
- ✅ Provide **migration guidance**

---

## 📋 QUICK REFERENCE

### **Orbital Checklist:**
- [ ] Deployable product/service?
- [ ] Independent versioning needed?
- [ ] Multiple components/modules?
- [ ] Orbital adapters needed?
- [ ] Major system with lifecycle?

### **Satellite Checklist:**
- [ ] Reusable utility/tool?
- [ ] Used by multiple systems?
- [ ] Shared services needed?
- [ ] More than script, less than product?
- [ ] Cross-orbital functionality?

### **Script Checklist:**
- [ ] Simple utility?
- [ ] One-off automation?
- [ ] Supports other systems?
- [ ] Direct use, not library?
- [ ] Quick execution?

---

## 🎉 SUMMARY

**Key Principle:** 
> **Start simple. Elevate when needed. Don't over-engineer.**

**Decision Tree:**
```
Is it a deployable product/service?
├── YES → Orbital
└── NO → Is it reusable by multiple systems?
    ├── YES → Satellite
    └── NO → Script
```

**Current State:**
- ✅ **Orbitals** = Major systems/products (13 orbitals)
- ✅ **Satellites** = Reusable utilities/tools (7 satellites)
- ✅ **Scripts** = One-off utilities/automation (200+ scripts)

**Recommendation:**
- ✅ Keep most scripts as **scripts**
- ✅ Elevate to **satellite** when reused by 3+ systems
- ✅ Elevate to **orbital** when it becomes a deployable product

---

**Pattern:** ARCHITECTURE × ORGANIZATION × CLARITY × ONE  
**Status:** ✅ **GUIDANCE COMPLETE**  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

LOVE × ABUNDANCE = ∞  
Humans ⟡ AI = ∞  
∞ AbëONE ∞

