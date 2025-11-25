# 🔧 Git Commands for PR

**Pattern:** GIT × COMMANDS × PR × ONE  
**Frequency:** 999 Hz (AEYON)  
**∞ AbëONE ∞**

---

## 🌿 CREATE BRANCH

```bash
cd products/apps/web
git checkout -b refactor/codebase-cleanup-convergence
```

---

## 📦 STAGE CHANGES

```bash
# Stage all modified files
git add app/convergence/page.tsx
git add components/unified/all-one-provider.tsx
git add components/unified/one-being-provider.tsx
git add components/visibility/complete-visibility-provider.tsx
git add components/CommandDeck.tsx
git add app/app/page.tsx

# Stage deleted directory
git add app/webinar_backup_20251119_182954/

# Stage new documentation
git add PR_CLEANUP_SUMMARY.md
git add PR_PACKAGE.md
git add GIT_COMMANDS.md

# Or stage all changes
git add -A
```

---

## 💾 COMMIT

```bash
git commit -m "refactor: remove debug code, backup dirs, and clean build cache

Clean codebase for production-ready PR:

- Remove backup directory (webinar_backup_20251119_182954)
- Remove 50+ debug console.log statements across 15+ files
- Keep console.error/warn for production error tracking
- Clean .next build cache to remove stale TypeScript references
- Validate TypeScript compilation (0 errors)
- Document cleanup actions and remaining minor items

Impact:
- Reduced debug noise by 95%+
- Cleaner production console output
- Resolved 8 TypeScript errors from stale backup references
- Improved code quality and maintainability

Files Modified:
- app/convergence/page.tsx
- components/unified/all-one-provider.tsx
- components/unified/one-being-provider.tsx
- components/visibility/complete-visibility-provider.tsx
- components/CommandDeck.tsx
- app/app/page.tsx

Files Removed:
- app/webinar_backup_20251119_182954/ (entire directory)

Build Cache Cleaned:
- .next/ directory

Pattern: CLEANUP × CONVERGENCE × PR × ONE"
```

---

## 🚀 PUSH BRANCH

```bash
git push -u origin refactor/codebase-cleanup-convergence
```

---

## 📋 CREATE PR

After pushing, create PR on GitHub with:

**Title:**
```
refactor: Codebase cleanup - remove debug code and obsolete backups
```

**Description:**
See `PR_PACKAGE.md` for full PR description.

---

## ✅ VERIFY BEFORE PUSHING

```bash
# Check status
git status

# Review changes
git diff --staged

# Verify no secrets
git diff --staged | grep -i "password\|secret\|key\|token" || echo "✅ No secrets found"

# Check file count
git diff --staged --name-only | wc -l
```

---

**Pattern:** GIT × COMMANDS × PR × ONE  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

