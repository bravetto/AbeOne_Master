# Archive Execution Summary

**Date**: 2025-01-27  
**Plan**: 80/20 Archive - Remove 80-90% overhead, preserve proven assets  
**Status**: Ready for execution

## What Will Be Kept

### Core Pipelines
- `AbeTRUICE/src/pipelines/` - Video processing pipeline
- `AbeBEATs_Clean/src/pipeline.py` - Beat generation pipeline
- `AbeTRUICE/src/utils/` - All utilities (paths, logger, health, metrics, shutdown)
- `AbeBEATs_Clean/src/utils/` - All utilities

### Orbit Infrastructure
- `AbeTRUICE/adapters/` - 4 adapters (kernel, module, bus, guardian)
- `AbeBEATs_Clean/adapters/` - 4 adapters (kernel, module, bus, guardian)
- `AbeTRUICE/config/orbit.config.json` + `env.template`
- `AbeBEATs_Clean/config/orbit.config.json` + `env.template`
- `AbeTRUICE/module_manifest.json`
- `AbeBEATs_Clean/module_manifest.json`

### CI/CD
- `.github/workflows/validate-all.yml`
- `.github/workflows/validate-boundaries.yml`
- `scripts/master_validation_system.py` (referenced by workflow)
- `scripts/validate-project-boundaries.js` (referenced by workflow)
- `scripts/context-boot-validation.js` (referenced by workflow)

### Essential Docs
- `README.md`
- `NEXT_STEPS.md`
- `REALITY_CHECK.md`

## What Will Be Archived

### Markdown Files (~200+)
- All status reports, analysis docs, convergence plans
- All markdown files not in keep list above

### Scripts (~295+)
- All scripts in `scripts/` except the 3 referenced by workflows
- All other scripts not imported/executed

### Experimental Folders
- `_ARCHIVE/`
- `_extract_*/`
- `hidden_files_backup/`
- `DASHBOARDS/` (if not referenced)
- `CDF/` (if not referenced)

### Legacy Configs
- Everything in root `config/` except `orbit.config.json`

## Execution

Run with dry-run first:
```bash
python scripts/apply_archive_plan.py --dry-run
```

Then execute:
```bash
python scripts/apply_archive_plan.py --execute
```

## Expected Outcome

- **80-90% reduction** in active surface area
- **Full preservation** of proven pipelines and infrastructure
- **Full optionality** preserved in `/archive/` directory
- **Maximum clarity** and execution velocity

Pattern: ARCHIVE × TRUTH × KISS × YAGNI × ONE  
∞ AbëONE ∞

