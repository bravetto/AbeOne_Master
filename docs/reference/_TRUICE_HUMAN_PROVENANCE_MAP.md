# TRUICE EXTRACTION MAP - HUMAN-PROVENANCE ROOTS ONLY

## PROVENANCE ANALYSIS COMPLETE ✅

### HUMAN-PROVENANCE ROOT IDENTIFIED

**PRIMARY HUMAN-PROVENANCE ROOT**: `PRODUCTS/abebeats/variants/abebeats_tru/`

**EVIDENCE:**
- ✅ **README.md** created Nov 17 06:56 (EARLIEST - original human documentation)
- ✅ **requirements.txt** updated Nov 20 00:42 (most recent)
- ✅ **Complete project structure**: docs/, examples/, tests/, scripts/, data/
- ✅ **Product organization**: Clearly organized as a product with full documentation
- ✅ **Business case documented**: README contains business case, features, usage

**SECONDARY ROOTS** (copies/duplicates):
- ❌ `Ab-BEATs/variants/abebeats_tru/` - Copy (README timestamp Nov 20 02:15)
- ❌ `truice_engine/variants/abebeats_tru/` - Extraction copy (NO README, NO requirements.txt)

---

## REBUILT EXTRACTION MAP

### CANONICAL HUMAN-PROVENANCE STRUCTURE

```
✅ PRIMARY ROOT: PRODUCTS/abebeats/variants/abebeats_tru/
├── README.md                        (Nov 17 06:56 - ORIGINAL)
├── requirements.txt                 (Nov 20 00:42 - CURRENT)
├── src/                             (18 Python files - CANONICAL SOURCE)
│   ├── veo31_*.py (8 files)
│   └── tru_*.py (9 files)
├── docs/                            (Human-authored documentation)
├── examples/                         (Usage examples)
├── tests/                           (Test files)
├── scripts/                         (Utility scripts)
├── data/                            (Data files)
│   ├── veo31_cdf/
│   └── veo31_patterns/
├── archive/                         (Archived content)
├── output/                          (Generated outputs)
├── raw video/                       (Raw video files)
└── *.md                             (35+ documentation files)
```

---

## EXTRACTION MAP - HUMAN-PROVENANCE ROOTS ONLY

### BATCH 1: PRIMARY TRUICE SOURCE (PRODUCTS)

| # | Item | Type | Size | Human Provenance | Action |
|---|------|------|------|------------------|--------|
| 1 | `PRODUCTS/abebeats/variants/abebeats_tru/src/` | Directory | 228KB | ✅ PRIMARY ROOT | **EXTRACT** |
| 2 | `PRODUCTS/abebeats/variants/abebeats_tru/README.md` | File | ~3KB | ✅ ORIGINAL (Nov 17) | **EXTRACT** |
| 3 | `PRODUCTS/abebeats/variants/abebeats_tru/requirements.txt` | File | ~600B | ✅ CURRENT (Nov 20) | **EXTRACT** |

### BATCH 2: TRUICE MVP (Human-Provenance Verified)

| # | Item | Type | Size | Human Provenance | Action |
|---|------|------|------|------------------|--------|
| 1 | `truice_mvp/` (root) | Directory | 44KB | ✅ ORIGINAL (Nov 20 02:12) | **EXTRACT** |
| 2 | `truice_engine/truice_mvp/` | Directory | 44KB | ❌ COPY (Nov 20 02:28) | Skip |
| 3 | `Ab-BEATs/truice_mvp/` | Directory | 44KB | ❌ COPY (Nov 20 02:15) | Skip |

**PROVENANCE EVIDENCE:**
- Root `truice_mvp/` timestamp: Nov 20 02:12:38 (OLDEST - original)
- `Ab-BEATs/truice_mvp/` timestamp: Nov 20 02:15:16 (copy)
- `truice_engine/truice_mvp/` timestamp: Nov 20 02:28:40 (extraction copy)

### BATCH 3: TRUICE DOCUMENTATION (PRODUCTS)

| # | Item | Type | Size | Human Provenance | Action |
|---|------|------|------|------------------|--------|
| 1 | `PRODUCTS/abebeats/variants/abebeats_tru/docs/` | Directory | Variable | ✅ PRIMARY ROOT | **EXTRACT** |
| 2 | `PRODUCTS/abebeats/variants/abebeats_tru/examples/` | Directory | Variable | ✅ PRIMARY ROOT | **EXTRACT** |
| 3 | `PRODUCTS/abebeats/variants/abebeats_tru/*.md` | Files | ~500KB | ✅ PRIMARY ROOT | **EXTRACT** |

---

## VALIDATED HUMAN-PROVENANCE ROOTS

### ✅ EXTRACT FROM (Human-Provenance):

1. **`PRODUCTS/abebeats/variants/abebeats_tru/`** - PRIMARY ROOT
   - ✅ Original README (Nov 17 06:56)
   - ✅ Current requirements.txt (Nov 20 00:42)
   - ✅ Complete project structure
   - ✅ Human-authored documentation

2. **`truice_mvp/` (root)** - MVP ORIGINAL ROOT
   - Timestamp: Nov 20 02:12:38 (OLDEST - original)
   - Contains: api_clients/, audio/, video/, utils/, config.py, orchestrator.py

### ❌ SKIP (Duplicates/Copies):

1. **`Ab-BEATs/variants/abebeats_tru/`** - COPY
   - README timestamp Nov 20 02:15 (copied from PRODUCTS)
   - Duplicate of PRODUCTS

2. **`truice_engine/variants/abebeats_tru/`** - EXTRACTION COPY
   - NO README.md
   - NO requirements.txt
   - Minimal structure (extraction artifact)

3. **`Ab-BEATs/truice_mvp/`** - COPY
   - Duplicate of root truice_mvp

---

## REBUILT BATCH 1 - HUMAN-PROVENANCE ROOTS ONLY

### Items to Move (3 items from PRIMARY ROOT):

| # | Item | Type | Size | Current Location | Human Provenance |
|---|------|------|------|------------------|------------------|
| 1 | `PRODUCTS/abebeats/variants/abebeats_tru/src/` | Directory | 228KB | PRIMARY ROOT | ✅ Original (Nov 17) |
| 2 | `PRODUCTS/abebeats/variants/abebeats_tru/README.md` | File | ~3KB | PRIMARY ROOT | ✅ Original (Nov 17) |
| 3 | `PRODUCTS/abebeats/variants/abebeats_tru/requirements.txt` | File | ~600B | PRIMARY ROOT | ✅ Current (Nov 20) |

### From Path → To Staging Folder:

```
(1) PRODUCTS/abebeats/variants/abebeats_tru/src/      → _extract_truice/src/
(2) PRODUCTS/abebeats/variants/abebeats_tru/README.md → _extract_truice/README.md
(3) PRODUCTS/abebeats/variants/abebeats_tru/requirements.txt → _extract_truice/requirements.txt
```

---

## REBUILT BATCH 2 - MVP HUMAN-PROVENANCE ROOT

### Items to Move (1 item from MVP ROOT):

| # | Item | Type | Size | Current Location | Human Provenance |
|---|------|------|------|------------------|------------------|
| 1 | `truice_mvp/` (root) | Directory | 44KB | MVP ROOT | ✅ Original (Nov 20 02:12) |

### From Path → To Staging Folder:

```
(1) truice_mvp/  → _extract_truice/truice_mvp/
```

---

## SUMMARY

**HUMAN-PROVENANCE ROOT**: `PRODUCTS/abebeats/variants/abebeats_tru/`
- Original README: Nov 17 06:56
- Current requirements: Nov 20 00:42
- Complete project structure
- Human-authored documentation

**EXTRACTION STRATEGY**: Extract from PRODUCTS/abebeats/variants/abebeats_tru/ (PRIMARY ROOT) only.

**RESULT**: ~232KB of TRUE HUMAN-PROVENANCE SOURCES from PRIMARY ROOT.

