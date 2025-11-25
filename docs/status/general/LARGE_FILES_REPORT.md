# Large Files Report - AbeOne Master Repository

**Total Repository Size**: 3.9GB

## Top-Level Directory Breakdown

| Size | Directory | Notes |
|------|-----------|-------|
| 1.0G | PRODUCTS | Contains large media files |
| 813M | AiGuardian-Chrome-Ext-dev | Active Chrome extension project |
| 528M | apps | Web applications |
| 407M | advanced-knock | Advanced knock project |
| 337M | AiGuardian-Chrome-Ext-dev.crx | Chrome extension package file |
| 328M | _ARCHIVE | Archived legacy projects |
| 16M | AIGuards-Backend | Backend services |
| 8.7M | EMERGENT_OS | Core OS files |

## Largest Individual Files (>50MB)

| Size | File Path | Type |
|------|-----------|------|
| 629M | PRODUCTS/abebeats/variants/abebeats_tru/raw/Super | Media file |
| 337M | AiGuardian-Chrome-Ext-dev.crx | Chrome extension package |
| 327M | _ARCHIVE/legacy-projects/AI-Guardians-chrome-ext/.git/objects/pack/pack-*.pack | Git pack file |
| 327M | AiGuardian-Chrome-Ext-dev/.git/objects/pack/pack-*.pack | Git pack file |
| 312M | PRODUCTS/abebeats/variants/abebeats_tru/output/tunnel_background.mp4 | Video file |
| 111M | .venv/lib/python3.13/site-packages/llvmlite/binding/libllvmlite.dylib | Python library |
| 105M | apps/web/node_modules/@next/swc-darwin-arm64/next-swc.darwin-arm64.node | Next.js binary |
| 105M | advanced-knock/frontend/node_modules/@next/swc-darwin-arm64/next-swc.darwin-arm64.node | Next.js binary |
| 52M | AiGuardian-Chrome-Ext-dev/assets/brand/AI | Brand assets |

## Node Modules Breakdown

| Size | Location |
|------|----------|
| 412M | apps/web/node_modules |
| 366M | advanced-knock/frontend/node_modules |
| 179M | AiGuardian-Chrome-Ext-dev/node_modules |

**Total node_modules**: ~957MB

## Git Repository Sizes

| Size | Location |
|------|----------|
| 331M | AiGuardian-Chrome-Ext-dev/.git |
| 327M | _ARCHIVE/legacy-projects/AI-Guardians-chrome-ext/.git |
| 4.6M | AIGuards-Backend/.git |
| 1.3M | EMERGENT_OS/aiagentsuite/.git |

**Total .git directories**: ~664MB

## Recommendations for Size Reduction

1. **Media Files** (941MB):
   - Consider moving large video/media files to external storage or CDN
   - `PRODUCTS/abebeats/variants/abebeats_tru/raw/Super` (629M)
   - `PRODUCTS/abebeats/variants/abebeats_tru/output/tunnel_background.mp4` (312M)

2. **Git History** (664MB):
   - Consider git garbage collection: `git gc --aggressive`
   - Archive old git repositories if not actively used

3. **Chrome Extension Package** (337M):
   - `.crx` file could be regenerated, consider removing if not needed

4. **Node Modules** (957MB):
   - Standard for Node.js projects, but can be regenerated
   - Consider using `.gitignore` to exclude if not already

5. **Python Virtual Environment** (111M+):
   - `.venv` can be regenerated, consider excluding from version control

## File Count Summary

- **Large files (>50MB)**: 9 files
- **Total size**: ~3.9GB
- **Primary contributors**: Media files, Git history, node_modules, Python venv

