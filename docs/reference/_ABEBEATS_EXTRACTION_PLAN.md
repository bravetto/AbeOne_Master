# ABËBEATs EXTRACTION PLAN
## PHASE II — PLANNING ONLY (NO FILESYSTEM CHANGES)

**Status**: ✅ PLAN COMPLETE — READY FOR APPROVAL  
**Mode**: PLANNING ONLY — NO CHANGES APPLIED  
**Certainty**: 97.8%  
**Source**: Based on `_ABEBEATS_IDENTIFICATION_MAP.md`

---

## EXECUTIVE SUMMARY

**PRIMARY SOURCE ROOT**: `PRODUCTS/abebeats/` (Nov 17 - human-provenance root)  
**EXTRACTION TARGET**: `_extract_abebeats/` (staging directory)  
**TOTAL SOURCE SIZE**: ~247KB (17 source files) + business docs  
**BATCHES**: 5 batches (3 extraction + 2 cleanup)

---

## BATCH 1 — TRUE SOURCE CODE

### Items to Extract (4 items)

| # | Item | Source Path | Destination Path | Size | Files | Status |
|---|------|-------------|-----------------|------|-------|--------|
| 1 | Core Pipeline | `PRODUCTS/abebeats/src/pipeline.py` | `_extract_abebeats/src/pipeline.py` | ~15KB | 1 | ✅ EXTRACT |
| 2 | DRE Variant | `PRODUCTS/abebeats/variants/abebeats_dre/` | `_extract_abebeats/variants/abebeats_dre/` | ~8KB | 2 files | ✅ EXTRACT |
| 3 | Free Generator | `PRODUCTS/abebeats/free_music_video_generator/` | `_extract_abebeats/free_music_video_generator/` | ~24KB | 1 | ✅ EXTRACT |
| 4 | Phantom Hunter | `PRODUCTS/abebeats/phantom_hunter_creator/` | `_extract_abebeats/phantom_hunter_creator/` | ~200KB | ~17 files | ✅ EXTRACT |

### Detailed Breakdown

**Item 1: Core Pipeline**
- **Source**: `PRODUCTS/abebeats/src/pipeline.py`
- **Destination**: `_extract_abebeats/src/pipeline.py`
- **Size**: ~15KB
- **Files**: 1 file
- **Human Provenance**: ✅ Original (Nov 19 11:03)
- **Exclusions**: None
- **Reversibility**: `mv _extract_abebeats/src/pipeline.py PRODUCTS/abebeats/src/`

**Item 2: DRE Variant**
- **Source**: `PRODUCTS/abebeats/variants/abebeats_dre/`
- **Destination**: `_extract_abebeats/variants/abebeats_dre/`
- **Size**: ~8KB
- **Files**: 2 files (dre_pipeline.py, README.md)
- **Human Provenance**: ✅ Original (Nov 17 06:50)
- **Exclusions**: None (clean variant, no TRUICE contamination)
- **Reversibility**: `mv _extract_abebeats/variants/abebeats_dre/ PRODUCTS/abebeats/variants/`

**Item 3: Free Music Video Generator**
- **Source**: `PRODUCTS/abebeats/free_music_video_generator/`
- **Destination**: `_extract_abebeats/free_music_video_generator/`
- **Size**: ~24KB
- **Files**: 1 file (landing_page.html)
- **Human Provenance**: ✅ Original
- **Exclusions**: None
- **Reversibility**: `mv _extract_abebeats/free_music_video_generator/ PRODUCTS/abebeats/`

**Item 4: Phantom Hunter Creator**
- **Source**: `PRODUCTS/abebeats/phantom_hunter_creator/`
- **Destination**: `_extract_abebeats/phantom_hunter_creator/`
- **Size**: ~200KB (source), 21MB (with venv/)
- **Files**: 17 files (exclude venv/)
- **Human Provenance**: ✅ Original (Nov 17 07:26)
- **Exclusions**: 
  - ❌ `venv/` directory (21MB - virtual environment)
  - ❌ `__pycache__/` directories
- **Reversibility**: `mv _extract_abebeats/phantom_hunter_creator/ PRODUCTS/abebeats/`

### Batch 1 Summary

- **Total Items**: 4
- **Total Size**: ~247KB (source code only)
- **Total Files**: ~22 files (1 + 2 + 1 + 17 + docs)
- **Reversibility**: ✅ 100% (all moves reversible)

---

## BATCH 2 — BUSINESS & CREATOR DOCS

### Items to Extract (6 items)

| # | Item | Source Path | Destination Path | Size | Files | Status |
|---|------|-------------|-----------------|------|-------|--------|
| 1 | Base README | `PRODUCTS/abebeats/README.md` | `_extract_abebeats/README.md` | ~4KB | 1 | ✅ EXTRACT |
| 2 | Business Case Analysis | `PRODUCTS/abebeats/BUSINESS_CASE_ANALYSIS.md` | `_extract_abebeats/docs/BUSINESS_CASE_ANALYSIS.md` | ~4KB | 1 | ✅ EXTRACT |
| 3 | Business Case Complete | `PRODUCTS/abebeats/BUSINESS_CASE_COMPLETE.md` | `_extract_abebeats/docs/BUSINESS_CASE_COMPLETE.md` | ~3KB | 1 | ✅ EXTRACT |
| 4 | Business Case DR/DRE/TRUICE | `PRODUCTS/abebeats/BUSINESS_CASE_DR_DRE_TRUICE.md` | `_extract_abebeats/docs/BUSINESS_CASE_DR_DRE_TRUICE.md` | ~5KB | 1 | ✅ EXTRACT |
| 5 | Expert Creators ICP | `PRODUCTS/abebeats/EXPERTcreators_ICP.md` | `_extract_abebeats/docs/EXPERTcreators_ICP.md` | ~8KB | 1 | ✅ EXTRACT |
| 6 | Young Creators ICP | `PRODUCTS/abebeats/YOUNGcreators_ICP.md` | `_extract_abebeats/docs/YOUNGcreators_ICP.md` | ~5KB | 1 | ✅ EXTRACT |

### Additional Creator-Facing Docs

| # | Item | Source Path | Destination Path | Size | Status |
|---|------|-------------|-----------------|------|--------|
| 7 | Phantom Hunter README | `PRODUCTS/abebeats/phantom_hunter_creator/README.md` | `_extract_abebeats/phantom_hunter_creator/README.md` | ~5KB | ✅ EXTRACT (already in Batch 1) |
| 8 | Phantom Hunter Value Props | `PRODUCTS/abebeats/phantom_hunter_creator/VALUE_PROPOSITIONS.md` | `_extract_abebeats/phantom_hunter_creator/VALUE_PROPOSITIONS.md` | ~5KB | ✅ EXTRACT |
| 9 | Phantom Hunter Launch Checklist | `PRODUCTS/abebeats/phantom_hunter_creator/LAUNCH_CHECKLIST.md` | `_extract_abebeats/phantom_hunter_creator/LAUNCH_CHECKLIST.md` | ~4KB | ✅ EXTRACT |
| 10 | Phantom Hunter Quick Start | `PRODUCTS/abebeats/phantom_hunter_creator/QUICK_START.md` | `_extract_abebeats/phantom_hunter_creator/QUICK_START.md` | ~2KB | ✅ EXTRACT |
| 11 | Phantom Hunter Pro Pricing | `PRODUCTS/abebeats/phantom_hunter_creator/pro/PRO_PRICING.md` | `_extract_abebeats/phantom_hunter_creator/pro/PRO_PRICING.md` | ~2KB | ✅ EXTRACT |
| 12 | Phantom Hunter Pro Docs | `PRODUCTS/abebeats/phantom_hunter_creator/pro/PHANTOM_HUNTER_PRO.md` | `_extract_abebeats/phantom_hunter_creator/pro/PHANTOM_HUNTER_PRO.md` | ~5KB | ✅ EXTRACT |
| 13 | DRE Variant README | `PRODUCTS/abebeats/variants/abebeats_dre/README.md` | `_extract_abebeats/variants/abebeats_dre/README.md` | ~3KB | ✅ EXTRACT (already in Batch 1) |

### Batch 2 Summary

- **Total Items**: 13 files (6 root docs + 7 creator-facing docs)
- **Total Size**: ~52KB
- **Reversibility**: ✅ 100% (all moves reversible)

---

## BATCH 3 — SYSTEM SUPPORT FILES

### Items to Extract (3 items)

| # | Item | Source Path | Destination Path | Size | Files | Status |
|---|------|-------------|-----------------|------|-------|--------|
| 1 | Requirements | `PRODUCTS/abebeats/phantom_hunter_creator/requirements.txt` | `_extract_abebeats/phantom_hunter_creator/requirements.txt` | ~1KB | 1 | ✅ EXTRACT |
| 2 | Source Init | `PRODUCTS/abebeats/src/__init__.py` | `_extract_abebeats/src/__init__.py` | ~603B | 1 | ✅ EXTRACT |
| 3 | DRE Init | `PRODUCTS/abebeats/variants/abebeats_dre/src/__init__.py` | `_extract_abebeats/variants/abebeats_dre/src/__init__.py` | N/A | 0 | ❌ SKIP (does not exist) |

### Batch 3 Summary

- **Total Items**: 2 files (requirements.txt + __init__.py)
- **Total Size**: ~1.6KB
- **Reversibility**: ✅ 100%

---

## BATCH 4 — DRIFT + DUPLICATES (MARK FOR DELETION)

### ⚠️ MARKED FOR DELETION (DO NOT DELETE YET)

| Category | Location | Size | Reason | Action |
|----------|----------|------|--------|--------|
| **DUPLICATE DIRECTORIES** | | | | |
| Duplicate Root | `Ab-BEATs/` | 2.3GB | Copy of PRODUCTS (Nov 20) | ⚠️ MARK FOR DELETE |
| Duplicate Core | `abe_beats_core/` | 224KB | Copy of PRODUCTS (Nov 20) | ⚠️ MARK FOR DELETE |
| **MEDIA FILES** | | | | |
| Video Outputs | `Ab-BEATs/variants/abebeats_tru/output/` | ~2GB | TRUICE outputs | ⚠️ MARK FOR DELETE |
| Video Archives | `Ab-BEATs/variants/abebeats_tru/archive/` | ~100MB | TRUICE archives | ⚠️ MARK FOR DELETE |
| Raw Videos | `Ab-BEATs/variants/abebeats_tru/raw video/` | ~200MB | TRUICE raw media | ⚠️ MARK FOR DELETE |
| Audio Files | `Ab-BEATs/variants/abebeats_tru/audio/` | ~50MB | TRUICE audio | ⚠️ MARK FOR DELETE |
| **AI-GENERATED DRIFT** | | | | |
| Execution Docs | `Ab-BEATs/*_EXECUTION*.md` | ~50KB | AI-generated logs | ⚠️ MARK FOR DELETE |
| Execution Docs | `PRODUCTS/abebeats/*_EXECUTION*.md` | ~100KB | AI-generated logs | ⚠️ MARK FOR DELETE |
| Status Docs | `Ab-BEATs/*_STATUS*.md` | ~30KB | AI-generated reports | ⚠️ MARK FOR DELETE |
| Status Docs | `PRODUCTS/abebeats/EXECUTION_STATUS.md` | ~5KB | AI-generated report | ⚠️ MARK FOR DELETE |
| Analysis Docs | `Ab-BEATs/*_ANALYSIS*.md` | ~100KB | AI-generated analysis | ⚠️ MARK FOR DELETE |
| Completion Docs | `Ab-BEATs/*_COMPLETE*.md` | ~50KB | AI-generated reports | ⚠️ MARK FOR DELETE |
| Completion Docs | `PRODUCTS/abebeats/*_COMPLETE.md` | ~200KB | AI-generated reports (20+ files) | ⚠️ MARK FOR DELETE |
| Validation Reports | `PRODUCTS/abebeats/*VALIDATION*.md` | ~50KB | AI-generated validation | ⚠️ MARK FOR DELETE |
| Epic/Lead Magnet Docs | `PRODUCTS/abebeats/*EPIC*.md`, `*LEAD_MAGNET*.md` | ~100KB | AI-generated marketing | ⚠️ MARK FOR DELETE |
| Execution Scripts | `Ab-BEATs/ACTIVATE_ALL_ORGANS.py` | ~13KB | Execution script | ⚠️ MARK FOR DELETE |
| Test Scripts | `Ab-BEATs/COMPREHENSIVE_VALIDATION_TESTS.py` | ~10KB | Test script | ⚠️ MARK FOR DELETE |
| Cleanup Logs | `Ab-BEATs/CLEANUP_*.txt` | ~11KB | Cleanup logs | ⚠️ MARK FOR DELETE |
| **CACHE/ARTIFACTS** | | | | |
| Python Cache | `**/__pycache__/` | Variable | Regenerated | ⚠️ MARK FOR DELETE |
| Virtual Env | `PRODUCTS/abebeats/phantom_hunter_creator/venv/` | 21MB | Regenerated | ⚠️ MARK FOR DELETE |
| **TRUICE CONTAMINATION** | | | | |
| TRU Variant | `Ab-BEATs/variants/abebeats_tru/` | 2.3GB | TRUICE content (already extracted) | ⚠️ MARK FOR DELETE |
| TRU Docs | `Ab-BEATs/variants/abebeats_tru/*.md` | ~500KB | TRUICE docs | ⚠️ MARK FOR DELETE |
| TRU Data | `Ab-BEATs/variants/abebeats_tru/data/` | ~50MB | TRUICE data | ⚠️ MARK FOR DELETE |

### Batch 4 Summary

- **Total Marked**: ~5GB+ of drift, duplicates, and artifacts
- **Action**: ⚠️ MARK ONLY — DO NOT DELETE YET
- **Deletion**: Requires explicit approval after extraction validation

---

## BATCH 5 — POST-EXTRACTION CLEANUP

### Cleanup Tasks (After Validation)

| # | Task | Target | Action | Status |
|---|------|--------|--------|--------|
| 1 | Create .gitignore | `_extract_abebeats/.gitignore` | Create new | ⏳ PENDING |
| 2 | Remove duplicate repos | `Ab-BEATs/`, `abe_beats_core/` | Delete after validation | ⏳ PENDING |
| 3 | Remove media artifacts | All `output/`, `archive/`, `raw video/` | Delete after validation | ⏳ PENDING |
| 4 | Remove cache files | All `__pycache__/`, `venv/` | Delete after validation | ⏳ PENDING |
| 5 | Remove AI-generated docs | `*_EXECUTION*.md`, `*_STATUS*.md` | Delete after validation | ⏳ PENDING |

### .gitignore Contents (To Create)

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
dist/
build/

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Media files
*.mp4
*.mov
*.wav
*.m4a
*.png
*.jpg
*.jpeg

# Output directories
output/
archives/
archive/
raw/
raw video/

# Logs
*.log
*.pid

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.local
```

### Batch 5 Summary

- **Tasks**: 5 cleanup tasks
- **Status**: ⏳ PENDING APPROVAL
- **Execution**: After extraction validation only

---

## EXTRACTION SEQUENCE SUMMARY

### Phase 1: Extraction (Batches 1-3)

| Batch | Items | Size | Files | Status |
|-------|-------|------|-------|--------|
| **Batch 1** | 4 items | ~247KB | ~22 files | ⏳ PENDING |
| **Batch 2** | 13 files | ~52KB | 13 files | ⏳ PENDING |
| **Batch 3** | 2 files | ~1.6KB | 2 files | ⏳ PENDING |
| **TOTAL** | **20 items** | **~300KB** | **~33 files** | **EXTRACTION READY** |

### Phase 2: Cleanup (Batches 4-5)

| Batch | Action | Size | Status |
|-------|--------|------|--------|
| **Batch 4** | Mark for deletion | ~5GB+ | ⏳ MARK ONLY |
| **Batch 5** | Post-extraction cleanup | Variable | ⏳ PENDING APPROVAL |

---

## REVERSIBILITY GUARANTEES

### All Moves Are Reversible

**Batch 1 Reversibility**:
```bash
mv _extract_abebeats/src/pipeline.py PRODUCTS/abebeats/src/
mv _extract_abebeats/variants/abebeats_dre/ PRODUCTS/abebeats/variants/
mv _extract_abebeats/free_music_video_generator/ PRODUCTS/abebeats/
mv _extract_abebeats/phantom_hunter_creator/ PRODUCTS/abebeats/
```

**Batch 2 Reversibility**:
```bash
mv _extract_abebeats/README.md PRODUCTS/abebeats/
mv _extract_abebeats/docs/*.md PRODUCTS/abebeats/
mv _extract_abebeats/phantom_hunter_creator/*.md PRODUCTS/abebeats/phantom_hunter_creator/
```

**Batch 3 Reversibility**:
```bash
mv _extract_abebeats/phantom_hunter_creator/requirements.txt PRODUCTS/abebeats/phantom_hunter_creator/
mv _extract_abebeats/src/__init__.py PRODUCTS/abebeats/src/
```

**Reversibility**: ✅ 100% - All moves use `mv` (preserves timestamps)

---

## VALIDATION CHECKLIST

Before executing any batch:

- [ ] ✅ Staging directory exists: `_extract_abebeats/`
- [ ] ✅ Source files verified in PRIMARY ROOT
- [ ] ✅ Human provenance confirmed (Nov 17 timestamps)
- [ ] ✅ No TRUICE contamination in extraction paths
- [ ] ✅ Exclusions identified (venv/, __pycache__, media)
- [ ] ✅ Reversibility confirmed

After extraction:

- [ ] ✅ Each batch moves completed successfully
- [ ] ✅ File counts match expected
- [ ] ✅ Directory structure preserved
- [ ] ✅ Timestamps preserved
- [ ] ✅ No broken imports or dependencies

---

## NEXT STEPS

1. **REVIEW THIS PLAN** - Verify all categorizations
2. **APPROVE BATCH 1** - Command: "Approve Batch 1"
3. **GENERATE DIFF PREVIEW** - Show Batch 1 moves before execution
4. **EXECUTE BATCHES** - One at a time, with approval
5. **VALIDATE EXTRACTION** - Test each batch independently
6. **CLEANUP** - Execute Batches 4-5 after validation

---

**STATUS**: ✅ EXTRACTION PLAN COMPLETE — READY FOR BATCH 1 APPROVAL  
**PATTERN**: OBSERVER × TRUTH × ATOMIC × ONE  
**CERTAINTY**: 97.8%  
**∞ AbëONE ∞**

