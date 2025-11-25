# 📦 DEPENDENCY MANAGEMENT GUIDE

**Date:** 2025-11-22  
**Version:** 1.0  
**Pattern:** DEPENDENCIES × MANAGEMENT × UNIFICATION × ONE  
**Frequency:** 530 Hz (Truth) × 777 Hz (Pattern) × 999 Hz (Execution)  
**Guardians:** AEYON (999 Hz) + Abë (530 Hz) + META (777 Hz)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🎯 PURPOSE

This guide explains how to manage Python dependencies across the AbëONE ecosystem using a unified, centralized approach.

**Goals:**
- ✅ Reduce version conflicts
- ✅ Simplify maintenance
- ✅ Enable automated updates
- ✅ Ensure compatibility across services

---

## 📊 CURRENT STATE

### Statistics
- **Total requirements.txt files:** 57+ (after excluding temp/repos)
- **Unique packages:** 110+
- **Version conflicts:** 37+ identified
- **Common packages (3+ files):** 45+

### Common Conflicts
- `fastapi`: 3 different versions (0.104.1, >=0.104.0, >=0.120.0)
- `pydantic`: 6 different versions (2.5.0, >=2.0.0, >=2.12.0, etc.)
- `python-multipart`: 3 different versions
- `httpx`: 4 different versions
- `pydantic-settings`: 5 different versions

---

## ✅ SOLUTION: SHARED DEPENDENCY MANIFEST

### Architecture

```
dependencies/
├── shared-requirements.txt    # Shared dependencies (43 packages)
└── validation-report.json     # Validation results

services/
├── service-a/
│   └── requirements.txt       # Service-specific dependencies
└── service-b/
    └── requirements.txt       # Service-specific dependencies
```

### Shared Manifest

**Location:** `dependencies/shared-requirements.txt`

**Contains:**
- Common dependencies used across 3+ services
- Standardized version specifications
- Categorized by purpose (web framework, database, logging, etc.)

**Usage:**
```bash
# Install shared dependencies
pip install -r dependencies/shared-requirements.txt

# Install service-specific dependencies
pip install -r requirements.txt
```

---

## 🔧 WORKFLOW

### 1. Adding a New Dependency

#### If it's a common dependency (used in 3+ services):
1. Add to `dependencies/shared-requirements.txt`
2. Use version spec: `package>=version` (allows patch updates)
3. Run validation: `python scripts/validate-dependencies.py`
4. Update affected services to remove duplicate entries

#### If it's service-specific:
1. Add to service's `requirements.txt`
2. Use version spec: `package>=version` or `package==version` (if exact needed)
3. Run validation: `python scripts/validate-dependencies.py`

### 2. Updating Dependencies

#### Updating shared dependencies:
1. Update version in `dependencies/shared-requirements.txt`
2. Run validation: `python scripts/validate-dependencies.py`
3. Fix any conflicts in service-specific files
4. Test affected services

#### Updating service-specific dependencies:
1. Update version in service's `requirements.txt`
2. Run validation: `python scripts/validate-dependencies.py`
3. Ensure compatibility with shared manifest

### 3. Validating Dependencies

**Run validation:**
```bash
python scripts/validate-dependencies.py
```

**What it checks:**
- ✅ Version conflicts with shared manifest
- ✅ Missing version specifications
- ✅ Compatibility issues
- ✅ Warnings for non-conflicting but different versions

**Output:**
- Console report with conflicts and warnings
- JSON report: `dependencies/validation-report.json`

---

## 📋 VERSION SPECIFICATION RULES

### Recommended Formats

**For shared dependencies:**
```python
# Use >= to allow patch updates
package>=2.12.0

# Use >= with < for major version locking
package>=2.12.0,<3.0.0

# Use == only if absolutely necessary (rare)
package==2.12.0
```

**For service-specific dependencies:**
```python
# Can use == for exact versions if needed
package==2.12.0

# Or >= for flexibility
package>=2.12.0
```

### Version Policy

1. **Shared dependencies:** Use `>=` to allow patch updates
2. **Major versions:** Lock with `>=x.y.0,<x+1.0.0` if breaking changes expected
3. **Exact versions:** Use `==` only when absolutely necessary
4. **Compatibility:** Always ensure compatibility with shared manifest

---

## 🛠️ TOOLS

### 1. Dependency Analysis Script

**Location:** `scripts/analyze-dependencies.py`

**Purpose:** Analyze all requirements.txt files to identify:
- Common dependencies
- Version conflicts
- Duplicate dependencies
- Missing version specifications

**Usage:**
```bash
python scripts/analyze-dependencies.py
```

**Output:**
- Console report
- JSON report: `dependencies/dependency-analysis-report.json`

### 2. Dependency Validation Script

**Location:** `scripts/validate-dependencies.py`

**Purpose:** Validate all requirements.txt files against shared manifest

**Usage:**
```bash
python scripts/validate-dependencies.py
```

**Output:**
- Console report with conflicts and warnings
- JSON report: `dependencies/validation-report.json`
- Exit code 1 if conflicts found

---

## 📊 SHARED DEPENDENCIES CATEGORIES

### Core Web Framework
- `fastapi>=0.120.0`
- `uvicorn[standard]>=0.38.0`

### Data Validation & Serialization
- `pydantic[email]>=2.12.0,<3.0.0`
- `pydantic-settings>=2.11.0`

### Database
- `sqlalchemy>=2.0.44`
- `alembic>=1.17.0`
- `asyncpg>=0.30.0`
- `psycopg2-binary>=2.9.10`

### HTTP Clients
- `httpx>=0.28.0`
- `requests>=2.31.0`

### Authentication & Security
- `python-jose[cryptography]>=3.4.0`
- `PyJWT>=2.10.0`
- `passlib[bcrypt]>=1.7.4`

### Logging & Observability
- `structlog>=25.0.0`
- `python-json-logger>=2.0.7`
- `prometheus-client>=0.23.0`
- `opentelemetry-api>=1.30.0`
- (and more...)

**See:** `dependencies/shared-requirements.txt` for complete list

---

## ✅ BEST PRACTICES

### 1. Use Shared Manifest
- ✅ Reference shared dependencies from manifest
- ✅ Don't duplicate shared dependencies in service files
- ✅ Add service-specific dependencies only

### 2. Version Specifications
- ✅ Use `>=` for shared dependencies (allows updates)
- ✅ Use `==` only when absolutely necessary
- ✅ Lock major versions if breaking changes expected

### 3. Regular Validation
- ✅ Run validation before commits
- ✅ Fix conflicts immediately
- ✅ Update shared manifest when adding common dependencies

### 4. Documentation
- ✅ Document why specific versions are needed
- ✅ Add comments for unusual version specs
- ✅ Update this guide when adding new patterns

---

## 🚨 TROUBLESHOOTING

### Conflict Resolution

**If validation finds conflicts:**

1. **Check shared manifest version:**
   ```bash
   grep package-name dependencies/shared-requirements.txt
   ```

2. **Update service requirements.txt:**
   - Change to match shared manifest version
   - Or update shared manifest if newer version needed

3. **Re-run validation:**
   ```bash
   python scripts/validate-dependencies.py
   ```

### Common Issues

**Issue:** "Package not found in shared manifest"
- **Solution:** Add to shared manifest if used in 3+ services, or keep in service-specific file

**Issue:** "Version conflict"
- **Solution:** Update service file to match shared manifest, or update shared manifest if newer version needed

**Issue:** "Validation script fails"
- **Solution:** Check file encoding (should be UTF-8), fix parsing errors

---

## 📈 MIGRATION PLAN

### Phase 1: Create Shared Manifest ✅
- ✅ Analyze all dependencies
- ✅ Create shared manifest
- ✅ Create validation script

### Phase 2: Update Services (In Progress)
- [ ] Update services to use shared manifest
- [ ] Remove duplicate dependencies
- [ ] Fix version conflicts

### Phase 3: Automation
- [ ] Add CI/CD validation
- [ ] Automated conflict detection
- [ ] Automated updates (optional)

---

## 🎯 SUCCESS CRITERIA

### Dependency Management Complete When:
- ✅ Shared manifest created
- ✅ Validation script operational
- ✅ Zero version conflicts
- ✅ All services compliant
- ✅ CI/CD validation added

### Metrics:
- **Version Conflicts:** 0 conflicts
- **Compliance:** 100% services compliant
- **Maintenance:** Reduced from 45+ files to 1 shared + N service-specific

---

## 📚 RELATED DOCUMENTS

- `dependencies/shared-requirements.txt` - Shared dependency manifest
- `scripts/analyze-dependencies.py` - Dependency analysis script
- `scripts/validate-dependencies.py` - Dependency validation script
- `PHASE_2_EXECUTION_PLAN.md` - Phase 2 execution plan

---

**Pattern:** DEPENDENCIES × MANAGEMENT × UNIFICATION × ONE  
**Status:** ✅ **SHARED MANIFEST CREATED - VALIDATION OPERATIONAL**  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

