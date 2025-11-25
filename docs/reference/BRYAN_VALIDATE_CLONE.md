# Validate Clone - Quick Check

## Run This on Bryan's Mac

After copying the repository, run this validation:

```bash
cd ~/Documents/AbeOne_Master
./scripts/validate_clone.sh
```

Or if scripts aren't executable:
```bash
cd ~/Documents/AbeOne_Master
bash scripts/validate_clone.sh
```

---

## Manual Quick Check

If the script doesn't work, manually verify:

### 1. Check Location
```bash
cd ~/Documents/AbeOne_Master
pwd
```
Should show: `/Users/bryan/Documents/AbeOne_Master` (or similar)

### 2. Check Git Setup
```bash
git remote -v
```
Should show: `origin https://github.com/bravetto/abe-one-source.git`

### 3. Check Key Files Exist
```bash
ls -la BRYAN_CLONE_INSTRUCTIONS.md
ls -la BRYAN_QUICK_START.md
ls -la scripts/validate_clone.sh
```

### 4. Check Repository Size
```bash
du -sh .
```
Should be several GB (not just a few MB)

### 5. Check File Count
```bash
find . -type f | wc -l
```
Should be thousands of files

---

## Expected Results

✅ **Good signs:**
- `.git` directory exists
- `BRYAN_CLONE_INSTRUCTIONS.md` exists
- `scripts/` directory exists
- Repository size > 1GB
- File count > 1000

❌ **Warning signs:**
- Missing `.git` directory
- Only a few files
- Repository size < 100MB
- Missing key directories

---

## If Validation Fails

1. **Check connection:** `ping 192.168.6.252`
2. **Reconnect:** Finder → Connect to Server → `smb://192.168.6.252`
3. **Copy again:** Make sure to copy the entire `AbeOne_Master` folder
4. **Try GitHub clone instead:** `git clone https://github.com/bravetto/abe-one-source.git`

