# 🔓 UNLOCK IGNORE-PATTERN LOCKFILE

## Developer Override Guide

The `.ignore-pattern-lock.json` is **informational**, not restrictive. You can modify ignore patterns at any time.

---

## HOW TO UNLOCK/MODIFY

### Option 1: Modify Constants in Source Files

1. **Edit ignore constants** in:
   - `scripts/validate-project-boundaries.js` (GLOBAL_IGNORES)
   - `scripts/enhanced-import-validator.js` (GLOBAL_IGNORES)
   - `scripts/boundary-watcher.js` (GLOBAL_IGNORES_CHOKIDAR)

2. **Regenerate lockfile**:
   ```bash
   node scripts/compute-ignore-lock.js > .ignore-pattern-lock.json
   ```

3. **Verify**:
   ```bash
   node scripts/verify-ignore-lock.js
   ```

### Option 2: Direct Lockfile Edit (Not Recommended)

You can edit `.ignore-pattern-lock.json` directly, but you must:
1. Update the `digest` field with new SHA-256 hash
2. Update `build_id` with new hash
3. Update `timestamp` to current ISO8601
4. Run verification to ensure consistency

**Better**: Always modify source constants and regenerate.

---

## WORKFLOW FOR CHANGES

### Adding New Ignore Pattern

1. Add to `GLOBAL_IGNORES` in source files:
   ```javascript
   const GLOBAL_IGNORES = [
     'node_modules',
     '.git',
     // ... existing ...
     'new-pattern'  // ← Add here
   ];
   ```

2. Regenerate lockfile:
   ```bash
   node scripts/compute-ignore-lock.js > .ignore-pattern-lock.json
   ```

3. Verify:
   ```bash
   node scripts/verify-ignore-lock.js
   ```

### Removing Ignore Pattern

1. Remove from `GLOBAL_IGNORES` in source files
2. Regenerate lockfile
3. Verify

### Temporary Override (Development)

For temporary testing, you can:
- Modify constants in source files
- Test your changes
- Regenerate lockfile when satisfied
- Or revert changes and regenerate

---

## QUICK REFERENCE

```bash
# Regenerate lockfile from current constants
node scripts/compute-ignore-lock.js > .ignore-pattern-lock.json

# Verify lockfile integrity
node scripts/verify-ignore-lock.js

# Check current ignore patterns
grep -r "GLOBAL_IGNORES" scripts/
```

---

## IMPORTANT NOTES

- ✅ **Lockfile is developer-controlled** - You own it
- ✅ **"SEALED" is informational** - Indicates verified state, not locked state
- ✅ **Always regenerate after changes** - Keeps digests accurate
- ✅ **Verification catches drift** - Run after manual edits
- ⚠️ **Don't commit invalid hashes** - Always verify before commit

---

**Status**: Fully unlockable, developer-controlled, informational only

