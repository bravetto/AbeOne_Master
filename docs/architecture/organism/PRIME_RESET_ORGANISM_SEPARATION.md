# PRIME RESET — ORGANISM SEPARATION PLAN

**Pattern:** PRIME × RESET × ORGANISM × SEPARATION × ONE  
**Frequency:** 999 Hz (AEYON) × 530 Hz (Truth) × 777 Hz (META)  
**Guardians:** AEYON (999 Hz) + META (777 Hz) + YAGNI (530 Hz) + JØHN (530 Hz)  
**Status:** ATOMIC STATE DEFINITION — EXECUTION READY  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## ATOMIC STATE DEFINITION

### ORGANISM = CORE ONLY

The master-AbëONE organism is the **minimal executable kernel** that orchestrates all orbitals. It contains:

1. **Kernel** (`kernel/abëone/`)
   - ONE_KERNEL.py
   - EVENT_BUS.py
   - GUARDIANS_REGISTRY.py
   - MODULE_REGISTRY.py
   - Guardians (guardian_one.py, guardian_two.py, guardian_three.py, guardian_five.py)
   - Core modules (abebeats/module.py, abebeats/pipeline.py)
   - Supporting infrastructure (health, logging, version_lock, etc.)

2. **Core Scripts** (`scripts/`)
   - Guardian scripts only (aeyon_guardian.py, meta_guardian.py, john_guardian.py, yagni_guardian.py, etc.)
   - Core validation scripts (abeone-validator.py, abeone_preflight_omega.py)
   - Kernel integration scripts (kernel-engine.py, kernel_sync.py)
   - Pattern engine (pattern-engine.py)
   - Prime engine (prime-engine.py)
   - Essential activation scripts (activate_the_one_system.py)
   - **EXCLUDE:** All orbital-specific scripts, deployment scripts, marketing scripts, analysis scripts

3. **Essential Config**
   - `.gitignore`
   - `pyrightconfig.json`
   - `package.json` (if needed for scripts)
   - `Makefile` (if essential)
   - `docker-compose.yml` (if needed for organism)
   - `Dockerfile` (if needed for organism)
   - `env.template`, `env.template.development`, `env.testing`
   - `openapi-complete.yaml` (if organism API)

4. **Core Manifests** (minimal)
   - `module_manifest.json` (organism modules only)
   - `orbital_manifest.json` (orbital registry — references only, no orbital code)

5. **Minimal README**
   - `README.md` (organism description only, no docs)

### ORBITALS = SEPARATE REPOS

All orbitals are **separate repositories** uploaded independently:

1. **AIGuards-Backend-orbital/** → Separate repo
2. **AiGuardian-Chrome-Ext-orbital/** → Separate repo
3. **AiGuardian-Sales-Page-orbital/** → Separate repo
4. **EMERGENT_OS/** → Separate repo (if separate from kernel)
5. **aiguardian-repos/** → Separate repo (guardian microservices)
6. **products/** → Separate repo (or per-product repos)
7. **satellites/** → Separate repo (or per-satellite repos)
8. **orbital/** → Separate repo
9. **orbitals/** → Separate repo

### EXCLUSIONS = NOT ORGANISM

**Remove from organism commit:**

1. **All Documentation**
   - `*.md` files (except `README.md`)
   - `docs/` directory
   - All markdown reports, analysis, guides

2. **All Reports/Analysis**
   - `*.json` files (except `module_manifest.json`, `orbital_manifest.json`)
   - `*.txt` report files
   - `*.html` dashboard/report files
   - `*.cdf` files

3. **All Orbitals**
   - `*-orbital/` directories
   - `orbitals/` directory
   - `orbital/` directory
   - `satellites/` directory
   - `products/` directory (unless core organism product)

4. **All Meta/Archive**
   - `archive/` directory
   - `hidden_files_backup/` directory
   - `temp_repos/` directory
   - `outputs/` directory
   - `logs/` directory (gitignored, but remove if present)

5. **All Non-Core Scripts**
   - Marketing scripts
   - Deployment scripts (unless core organism)
   - Analysis scripts
   - Orbital-specific scripts
   - Client-specific scripts

6. **All Non-Core Directories**
   - `ABEGENIUS/` (unless core organism)
   - `abellm-vscode-extension/` (unless core organism)
   - `abeloves_conversations/` (unless core organism)
   - `abeloves_relationships/` (unless core organism)
   - `CDF/` (unless core organism)
   - `DASHBOARDS/` (unless core organism)
   - `design-system/` (unless core organism)
   - `DiscordOnboarding/` (unless core organism)
   - `clients/` (unless core organism)
   - `codeguardians-gateway/` (unless core organism)
   - `download/` (unless core organism)
   - `Downloads/` (unless core organism)
   - `marketing/` (unless core organism)
   - `showcase/` (unless core organism)
   - `truice_engine/` (unless core organism)
   - `hypervector-system/` (unless core organism)
   - `atomic/` (unless core organism)
   - `dev-environment/` (unless core organism)
   - `infra/` (unless core organism)
   - `monitoring/` (unless core organism)
   - `protocol/` (unless core organism)
   - `router/` (unless core organism)
   - `shared/` (unless core organism)
   - `src/` (unless core organism)
   - `state/` (unless core organism)
   - `templates/` (unless core organism)
   - `test-env/` (unless core organism)
   - `tests/` (unless core organism)
   - `validation/` (unless core organism)
   - `guards/` (unless core organism)
   - `guardians/` (unless core organism)

---

## EXECUTION PLAN

### PHASE 1: IDENTIFY ORGANISM FILES

**Core Organism Files:**
```
kernel/abëone/                    # Complete kernel
scripts/                          # Filtered to core only
  - aeyon_guardian.py
  - meta_guardian.py
  - john_guardian.py
  - yagni_guardian.py
  - abeone-validator.py
  - abeone_preflight_omega.py
  - kernel-engine.py
  - kernel_sync.py
  - pattern-engine.py
  - prime-engine.py
  - activate_the_one_system.py
  - [other core guardian/validation scripts]
.gitignore
pyrightconfig.json
package.json                       # If needed
Makefile                          # If essential
docker-compose.yml                # If needed
Dockerfile                        # If needed
env.template
env.template.development
env.testing
openapi-complete.yaml             # If organism API
module_manifest.json
orbital_manifest.json
README.md                         # Minimal organism README
```

### PHASE 2: CREATE ORGANISM COMMIT

**Commit Strategy:**
1. Create new branch: `organism-only`
2. Remove all exclusions (docs, orbitals, reports, etc.)
3. Keep only organism files
4. Update `README.md` to organism-only description
5. Commit: `feat: organism-only — core kernel and essential scripts`

**Git Commands:**
```bash
# Create organism-only branch
git checkout -b organism-only

# Remove all documentation
find . -name "*.md" ! -name "README.md" -type f -delete
rm -rf docs/

# Remove all reports/analysis
find . -name "*.json" ! -name "module_manifest.json" ! -name "orbital_manifest.json" ! -name "package.json" -type f -delete
find . -name "*.txt" -type f -delete
find . -name "*.html" -type f -delete
find . -name "*.cdf" -type f -delete

# Remove all orbitals
rm -rf *-orbital/
rm -rf orbitals/
rm -rf orbital/
rm -rf satellites/
rm -rf products/
rm -rf aiguardian-repos/
rm -rf EMERGENT_OS/  # If separate

# Remove all non-core directories
rm -rf archive/ hidden_files_backup/ temp_repos/ outputs/ logs/
rm -rf ABEGENIUS/ abellm-vscode-extension/ abeloves_conversations/ abeloves_relationships/
rm -rf CDF/ DASHBOARDS/ design-system/ DiscordOnboarding/
rm -rf clients/ codeguardians-gateway/ download/ Downloads/
rm -rf marketing/ showcase/ truice_engine/ hypervector-system/
rm -rf atomic/ dev-environment/ infra/ monitoring/
rm -rf protocol/ router/ shared/ src/ state/ templates/
rm -rf test-env/ tests/ validation/ guards/ guardians/

# Filter scripts to core only
# Keep only core guardian/validation/kernel scripts
# Remove all orbital-specific, marketing, deployment, analysis scripts

# Commit organism-only
git add .
git commit -m "feat: organism-only — core kernel and essential scripts

- Core kernel (kernel/abëone/)
- Core guardian scripts
- Core validation scripts
- Essential config files
- Minimal manifests
- No docs, no orbitals, no reports"
```

### PHASE 3: UPLOAD ORBITALS SEPARATELY

**For Each Orbital:**
1. Create separate repository
2. Copy orbital directory
3. Add orbital-specific README
4. Commit and push

**Orbital Upload Commands:**
```bash
# For each orbital:
cd AIGuards-Backend-orbital/
git init
git add .
git commit -m "feat: AIGuards-Backend orbital — initial commit"
git remote add origin <orbital-repo-url>
git push -u origin main
```

---

## EPISTEMIC CLARITY

### ATOMIC STATE = MINIMAL ORGANISM

**The organism is:**
- **Kernel** — Core orchestration engine
- **Guardians** — Core guardian scripts
- **Validation** — Core validation scripts
- **Config** — Essential configuration
- **Manifests** — Module and orbital registries (references only)

**The organism is NOT:**
- Documentation
- Reports/Analysis
- Orbitals (separate repos)
- Products (separate repos)
- Satellites (separate repos)
- Marketing/Deployment scripts
- Client-specific code

### SEPARATION PRINCIPLE

**One Commit = One Organism**
- Master-AbëONE commit contains ONLY the organism
- Orbitals are separate repositories
- Each orbital is independently versioned
- Organism references orbitals via manifests (registry only)

### PRAGMATIC RULES

1. **If it's not kernel or core guardian → exclude**
2. **If it's orbital-specific → separate repo**
3. **If it's documentation → exclude**
4. **If it's a report/analysis → exclude**
5. **If it's client-specific → exclude**

---

## FINAL COMMIT MESSAGE

```
feat: organism-only — master-AbëONE core kernel

Core organism containing:
- kernel/abëone/ — Complete kernel (ONE_KERNEL, EVENT_BUS, GUARDIANS_REGISTRY, MODULE_REGISTRY)
- scripts/ — Core guardian and validation scripts only
- Essential config files
- Minimal manifests (module_manifest.json, orbital_manifest.json)

Excluded:
- All documentation (*.md except README.md)
- All reports/analysis (*.json, *.txt, *.html, *.cdf)
- All orbitals (separate repositories)
- All non-core scripts and directories

Orbitals uploaded separately:
- AIGuards-Backend-orbital
- AiGuardian-Chrome-Ext-orbital
- AiGuardian-Sales-Page-orbital
- EMERGENT_OS
- aiguardian-repos
- products
- satellites
- orbital
- orbitals

Pattern: ORGANISM × KERNEL × GUARDIANS × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (Truth) × 777 Hz (META)
```

---

## VALIDATION CHECKLIST

**Before Commit:**
- [ ] Only `kernel/abëone/` present
- [ ] Only core scripts in `scripts/`
- [ ] No `*.md` files except `README.md`
- [ ] No `*.json` files except manifests
- [ ] No `*.txt`, `*.html`, `*.cdf` files
- [ ] No `*-orbital/` directories
- [ ] No `orbitals/`, `orbital/`, `satellites/`, `products/` directories
- [ ] No `docs/` directory
- [ ] No non-core directories
- [ ] `README.md` describes organism only
- [ ] Manifests reference orbitals (registry only)

**After Commit:**
- [ ] Organism is minimal and executable
- [ ] Orbitals are separate repositories
- [ ] No drift from atomic state definition
- [ ] Epistemic clarity achieved

---

**Pattern:** PRIME × RESET × ORGANISM × SEPARATION × ONE  
**Status:** ATOMIC STATE DEFINED — EXECUTION READY  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

