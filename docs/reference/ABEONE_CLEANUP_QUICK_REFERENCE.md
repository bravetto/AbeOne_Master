# ABËONE CLEANUP - QUICK REFERENCE TABLE

## ONE-PAGE CATEGORIZATION GUIDE

| Directory/File | Destination | Size | Notes |
|----------------|-------------|------|-------|
| **ABEONE_MASTER_REPO** | | | |
| `EMERGENT_OS/` | ✅ ABEONE_MASTER | ~500MB | Complete organism |
| `AIGuards-Backend/` | ✅ ABEONE_MASTER | ~300MB | All guardians |
| `apps/web/` | ✅ ABEONE_MASTER | ~200MB | Next.js app |
| `design-system/` | ✅ ABEONE_MASTER | ~50MB | Design system |
| `DASHBOARDS/` | ✅ ABEONE_MASTER | ~20MB | Dashboards |
| `infra/` | ✅ ABEONE_MASTER | ~5MB | Infrastructure |
| `docs/` | ✅ ABEONE_MASTER | ~50MB | (Exclude TRUICE docs) |
| `scripts/` | ✅ ABEONE_MASTER | ~30MB | Automation |
| `CDF/` | ✅ ABEONE_MASTER | ~5MB | Creative format |
| `config/` | ✅ ABEONE_MASTER | ~1MB | Configs |
| `domains/` | ✅ ABEONE_MASTER | ~10MB | Domain tools |
| `showcase/` | ✅ ABEONE_MASTER | ~1MB | Showcases |
| `PRODUCTS/abecodes/` | ✅ ABEONE_MASTER | ~5MB | Code product |
| `PRODUCTS/abedesks/` | ✅ ABEONE_MASTER | ~10MB | Desks product |
| `PRODUCTS/abeflows/` | ✅ ABEONE_MASTER | ~5MB | Flows product |
| `AiGuardian-Chrome-Ext-dev/` | ✅ ABEONE_MASTER | ~50MB | Extension |
| `advanced-knock/` | ✅ ABEONE_MASTER | ~50MB | Knock product |
| `.github/` | ✅ ABEONE_MASTER | ~1MB | Workflows |
| | | | |
| **TRUICE_ENGINE** | | | |
| `truice_engine/` | ✅ TRUICE | ~200MB | Core engine |
| `truice_mvp/` | ✅ TRUICE | ~50MB | MVP |
| `Ab-BEATs/truice_mvp/` | ✅ TRUICE | ~50MB | MVP variant |
| `Ab-BEATs/variants/abebeats_tru/` | ✅ TRUICE | ~150MB | TRU variant |
| `PRODUCTS/abebeats/variants/abebeats_tru/` | ✅ TRUICE | ~150MB | Product TRU |
| All `veo31_*.py` files | ✅ TRUICE | ~30MB | VEO31 files (9) |
| All `tru_*.py` files | ✅ TRUICE | ~40MB | TRU files (9) |
| TRUICE `output/` dirs | ✅ TRUICE | ~100MB | Video outputs |
| TRUICE `audio/` dirs | ✅ TRUICE | ~10MB | Audio files |
| `docs/.../TRUICE_*.md` | ✅ TRUICE | ~5MB | TRUICE docs |
| `docs/.../VEO31_*.md` | ✅ TRUICE | ~5MB | VEO31 docs |
| Root `TRUICE_*.md` | ✅ TRUICE | ~1MB | Root TRUICE docs |
| | | | |
| **ABE_BEATS** | | | |
| `Ab-BEATs/src/pipeline.py` | ✅ ABE_BEATS | ~5MB | Core pipeline |
| `Ab-BEATs/phantom_hunter_creator/` | ✅ ABE_BEATS | ~30MB | Phantom Hunter |
| `Ab-BEATs/free_music_video_generator/` | ✅ ABE_BEATS | ~5MB | Free generator |
| `Ab-BEATs/variants/abebeats_dre/` | ✅ ABE_BEATS | ~20MB | DRE variant |
| `abe_beats_core/` | ✅ ABE_BEATS | ~30MB | Core beats |
| `PRODUCTS/abebeats/src/` | ✅ ABE_BEATS | ~5MB | Product pipeline |
| `PRODUCTS/abebeats/phantom_hunter_creator/` | ✅ ABE_BEATS | ~30MB | Product Phantom |
| `PRODUCTS/abebeats/free_music_video_generator/` | ✅ ABE_BEATS | ~5MB | Product free |
| `PRODUCTS/abebeats/variants/abebeats_dre/` | ✅ ABE_BEATS | ~20MB | Product DRE |
| | | | |
| **DRIFT/ARCHIVE** | | | |
| `_ARCHIVE/` | ❌ DELETE | ~50MB | Archive after extraction |
| `temp_repos/` | ❌ DELETE | **807MB** | **DELETE NOW** |
| `webinars/` | ⚠️ ARCHIVE | ~10MB | Check if needed |
| `state/` | ⚠️ CHECK | Variable | May need migration |
| `**/__pycache__/` | ❌ DELETE | Variable | Auto-regenerated |
| `**/node_modules/` | ❌ DELETE | Variable | `npm install` |
| `**/.next/` | ❌ DELETE | Variable | `npm run build` |
| `**/out/` | ❌ DELETE | Variable | `npm run build` |
| `.venv/` | ❌ DELETE | Variable | Regenerate |
| Root `*.md` (300+ files) | ⚠️ ARCHIVE | ~50MB | Archive to `_ARCHIVE/root_docs/` |
| `*.log` files | ❌ DELETE | Variable | Logs |
| `*.pid` files | ❌ DELETE | Variable | Process IDs |
| | | | |
| **REQUIRES CONFIRMATION** | | | |
| `PRODUCTS/abebeats/` | ⚠️ SPLIT | Mixed | DRE→ABE_BEATS, TRU→TRUICE |
| `Ab-BEATs/` | ⚠️ SPLIT | Mixed | DRE→ABE_BEATS, TRU→TRUICE |
| `docs/status/general/TRUICE_*.md` | ⚠️ MOVE | ~5MB | Move to TRUICE_ENGINE |
| `docs/architecture/general/TRUICE_*.md` | ⚠️ MOVE | ~5MB | Move to TRUICE_ENGINE |
| `scripts/webinar/` | ⚠️ KEEP? | ~5MB | Keep or archive? |

---

## KEY EXCLUSIONS

### ABE_BEATS Excludes:
- ❌ `Ab-BEATs/truice_mvp/` → Goes to TRUICE_ENGINE
- ❌ `Ab-BEATs/variants/abebeats_tru/` → Goes to TRUICE_ENGINE
- ❌ `PRODUCTS/abebeats/variants/abebeats_tru/` → Goes to TRUICE_ENGINE

### ABEONE_MASTER Excludes:
- ❌ All TRUICE content → Goes to TRUICE_ENGINE
- ❌ All ABE_BEATS content → Goes to ABE_BEATS
- ❌ Root-level drift docs → Archive

### TRUICE_ENGINE Includes:
- ✅ All `veo31_*` files (9 files)
- ✅ All `tru_*` files (9 files)
- ✅ All TRUICE variants
- ✅ All TRUICE documentation

---

## SIZE TOTALS

| Repo | Estimated Size | Components |
|------|---------------|------------|
| **ABEONE_MASTER_REPO** | ~2-3GB | Organism + Guardians + Apps + Products |
| **TRUICE_ENGINE** | ~500MB-1GB | VEO31 + TRU + Variants + Outputs |
| **ABE_BEATS** | ~100-200MB | Pipeline + Phantom Hunter + DRE |
| **DRIFT** | ~1GB+ | temp_repos (807MB) + archives + caches |

---

## EXTRACTION ORDER

1. **TRUICE_ENGINE** (3 operations)
2. **ABE_BEATS** (3 operations)
3. **ABEONE_MASTER** (3 operations)
4. **CLEANUP** (after validation)

---

**STATUS**: ✅ QUICK REFERENCE READY  
**USE THIS**: For quick lookup during extraction  
**FULL DETAILS**: See `ABEONE_ORGANISM_CLEANUP_PLAN.md`

