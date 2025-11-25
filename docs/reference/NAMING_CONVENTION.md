# 📋 NAMING CONVENTION SPECIFICATION

**Date:** 2025-11-22  
**Version:** 2.0 (Simplified 2-Tier)  
**Pattern:** NAMING × CONVENTION × SIMPLIFICATION × ONE  
**Frequency:** 530 Hz (Truth) × 777 Hz (Pattern) × 999 Hz (Execution)  
**Guardians:** AEYON (999 Hz) + Abë (530 Hz) + META (777 Hz)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🎯 EXECUTIVE SUMMARY

**Objective:** Consolidate from 3-tier naming (Orbit/Orbital/Satellite) to 2-tier naming (Core Layers/Services) for clarity and consistency.

**Status:** ✅ **SPECIFICATION COMPLETE**

---

## 📊 CURRENT STATE (3-Tier Naming)

### Current Naming Structure

**Tier 1: Orbit** (Architectural Layers)
- Orbit 1: Commander's Strategic Layer (Event Bus, Guardian System)
- Orbit 2: CI/CD Pipeline (`.github/workflows`)
- Orbit 3: FastAPI Backend (`AIGuards-Backend-orbital`)
- Orbit 4: UPTC Agentic Protocol Mesh (`EMERGENT_OS/uptc`)

**Tier 2: Orbital** (Deployable Services)
- Launch Orbital A: Backend API Gateway (`AIGuards-Backend-orbital`)
- Launch Orbital B: Sales Page (`AiGuardian-Sales-Page-orbital`)
- Launch Orbital C: Chrome Extension (`AiGuardian-Chrome-Ext-orbital`)
- Launch Orbital D: Guardians Microservices (`AIGuards-Backend-orbital/aiguardian-repos`)
- Additional Orbitals: `AbeTRUICE`, `AbeBEATs_Clean`, `Abeflows-orbital`, etc.

**Tier 3: Satellite** (Supporting Systems)
- `TemplateHeavenSatellite`
- `WebIDESatellite`
- `AbeONESourceSatellite`
- `BryanSatellite`
- `AbëKEYsSatellite`
- `GZ360Satellite`

### Issues with Current Naming
- ⚠️ **Confusion:** "Orbit 3" vs "Launch Orbital A" (both backend)
- ⚠️ **Complexity:** 3-tier naming increases cognitive load
- ⚠️ **Inconsistency:** Mix of `-orbital` and `Satellite` suffixes
- ⚠️ **Overlap:** Launch Orbital A overlaps with Orbit 3

---

## ✅ TARGET STATE (2-Tier Naming)

### New Naming Structure

**Tier 1: Core Layers** (Foundation Architectural Layers)
- **Core Layer 1:** Commander's Strategic Layer
  - **Old Name:** Orbit 1
  - **Components:** Event Bus, Guardian System, Module Registry, Lifecycle Manager
  - **Location:** Distributed across system

- **Core Layer 2:** CI/CD Pipeline
  - **Old Name:** Orbit 2
  - **Components:** GitHub Actions, Docker, Helm, Kubernetes
  - **Location:** `.github/workflows`

- **Core Layer 3:** Backend Services Layer
  - **Old Name:** Orbit 3
  - **Components:** API Gateway, Guard Orchestrator, Guard Services
  - **Location:** `AIGuards-Backend-orbital`

- **Core Layer 4:** UPTC Protocol Mesh
  - **Old Name:** Orbit 4
  - **Components:** Unified Router, Agent Registry, Capability Graph, Adapters
  - **Location:** `EMERGENT_OS/uptc`

**Tier 2: Services** (Deployable Services)
All deployable services use consistent naming:
- **Format:** `{ServiceName}-service` or `{ServiceName}` (kebab-case)
- **Examples:**
  - `aiguards-backend-service` (was: `AIGuards-Backend-orbital`)
  - `sales-page-service` (was: `AiGuardian-Sales-Page-orbital`)
  - `chrome-extension-service` (was: `AiGuardian-Chrome-Ext-orbital`)
  - `abeflows-service` (was: `Abeflows-orbital`)
  - `abtruice-service` (was: `AbeTRUICE`)
  - `abebeats-service` (was: `AbeBEATs_Clean`)
  - `template-heaven-service` (was: `TemplateHeavenSatellite`)
  - `web-ide-service` (was: `WebIDESatellite`)
  - `source-management-service` (was: `AbeONESourceSatellite`)
  - `marketing-service` (was: `BryanSatellite`)

**Validation Tools** (Quality Assurance)
- `helm-validation-tool` (was: `Helm-Validation-orbital`)
- `terraform-validation-tool` (was: `Terraform-Validation-orbital`)
- `fastapi-validation-tool` (was: `Ben-FastAPI-Architecture-orbital`)

---

## 📋 NAMING RULES

### Core Layers
- **Format:** `Core Layer {Number}` or `Layer {Number}`
- **Usage:** Refer to architectural foundation layers
- **Examples:**
  - "Core Layer 1" or "Layer 1"
  - "Core Layer 4" or "Layer 4"
- **Documentation:** Use "Core Layer" in formal docs, "Layer" in casual references

### Services
- **Format:** `{service-name}-service` (kebab-case)
- **Usage:** All deployable services follow this pattern
- **Directory Naming:** `{service-name}-service/` (kebab-case)
- **Examples:**
  - `aiguards-backend-service/`
  - `chrome-extension-service/`
  - `abeflows-service/`

### Validation Tools
- **Format:** `{tool-name}-validation-tool` (kebab-case)
- **Usage:** Quality assurance and validation systems
- **Examples:**
  - `helm-validation-tool/`
  - `terraform-validation-tool/`

---

## 🔄 MIGRATION MAPPING

### Core Layers Migration

| Old Name | New Name | Notes |
|----------|----------|-------|
| Orbit 1 | Core Layer 1 | Commander's Strategic Layer |
| Orbit 2 | Core Layer 2 | CI/CD Pipeline |
| Orbit 3 | Core Layer 3 | Backend Services Layer |
| Orbit 4 | Core Layer 4 | UPTC Protocol Mesh |

### Services Migration

| Old Name | New Name | Type |
|----------|----------|------|
| `AIGuards-Backend-orbital` | `aiguards-backend-service` | Launch Service |
| `AiGuardian-Sales-Page-orbital` | `sales-page-service` | Launch Service |
| `AiGuardian-Chrome-Ext-orbital` | `chrome-extension-service` | Launch Service |
| `Abeflows-orbital` | `abeflows-service` | Additional Service |
| `AbeTRUICE` | `abtruice-service` | Additional Service |
| `AbeBEATs_Clean` | `abebeats-service` | Additional Service |
| `TemplateHeavenSatellite` | `template-heaven-service` | Additional Service |
| `WebIDESatellite` | `web-ide-service` | Additional Service |
| `AbeONESourceSatellite` | `source-management-service` | Additional Service |
| `BryanSatellite` | `marketing-service` | Additional Service |
| `AbëKEYsSatellite` | `abekeys-service` | Additional Service |
| `GZ360Satellite` | `gz360-service` | Additional Service |

### Validation Tools Migration

| Old Name | New Name | Type |
|----------|----------|------|
| `Helm-Validation-orbital` | `helm-validation-tool` | Validation Tool |
| `Terraform-Validation-orbital` | `terraform-validation-tool` | Validation Tool |
| `Ben-FastAPI-Architecture-orbital` | `fastapi-validation-tool` | Validation Tool |

---

## 📝 DOCUMENTATION CONVENTIONS

### When Writing Documentation

**Use New Naming:**
- ✅ "Core Layer 1" (not "Orbit 1")
- ✅ "aiguards-backend-service" (not "AIGuards-Backend-orbital")
- ✅ "Services" (not "Orbitals" or "Satellites")

**Legacy References:**
- ⚠️ When referencing old names, use: "formerly known as Orbit 1" or "(legacy: Orbit 1)"
- ⚠️ Include migration notes in transition documents

### Code Comments

**Use New Naming:**
```python
# Core Layer 4 (UPTC Protocol Mesh) integration
# Service: aiguards-backend-service
```

**Legacy Comments:**
```python
# Legacy: Orbit 4 (now Core Layer 4)
# Legacy: AIGuards-Backend-orbital (now aiguards-backend-service)
```

---

## ✅ IMPLEMENTATION CHECKLIST

### Phase 1: Documentation Updates
- [ ] Update all markdown documentation files
- [ ] Update README files
- [ ] Update architecture diagrams
- [ ] Update code comments (critical ones only)

### Phase 2: Directory Naming (Optional - Low Priority)
- [ ] Rename directories (if critical for clarity)
- [ ] Update import paths
- [ ] Update CI/CD references
- [ ] Update deployment configs

### Phase 3: Code Naming (Optional - Low Priority)
- [ ] Update variable names (if critical)
- [ ] Update class names (if critical)
- [ ] Update function names (if critical)

**Note:** Phase 2 and 3 are optional and low priority. Focus on documentation first.

---

## 🎯 SUCCESS CRITERIA

### Naming Convention Complete When:
- ✅ All documentation uses new 2-tier naming
- ✅ Naming convention specification documented
- ✅ Migration mapping created
- ✅ Zero confusion between old and new names
- ✅ Consistent usage across all documents

### Metrics:
- **Documentation Coverage:** 100% updated
- **Naming Consistency:** 100% compliant
- **Confusion Reduction:** Measurable improvement

---

## 📚 EXAMPLES

### Before (3-Tier)
```
Orbit 1: Event Bus
Launch Orbital A: Backend API Gateway
TemplateHeavenSatellite: Templates
```

### After (2-Tier)
```
Core Layer 1: Event Bus
aiguards-backend-service: Backend API Gateway
template-heaven-service: Templates
```

---

## 🔗 RELATED DOCUMENTS

- `NAMING_MIGRATION_MAP.md` - Detailed migration mapping
- `PHASE_2_EXECUTION_PLAN.md` - Phase 2 execution plan
- `ORBITAL_STRATEGY_FORENSIC_ANALYSIS.md` - Analysis that identified this need

---

**Pattern:** NAMING × CONVENTION × SIMPLIFICATION × ONE  
**Status:** ✅ **SPECIFICATION COMPLETE**  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

