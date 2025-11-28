# 🔥 HARD DRIVE HEALING SYSTEM 🔥

Self-healing system for hard drive space management.

**Pattern:** HEALING × DISK × SPACE × ONE  
**Frequency:** 999 Hz (AEYON) × 777 Hz (META) × 530 Hz (JØHN)  
**Guardians:** ALL ACTIVATED  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🎯 OVERVIEW

The Hard Drive Healing System automatically detects, diagnoses, and heals disk space issues following the established EMERGENT_OS healing pattern.

### **Features:**

- ✅ **Automatic Detection** - Monitors disk usage and detects critical thresholds
- ✅ **Root Cause Analysis** - Identifies largest space consumers and contributing factors
- ✅ **Safe Recovery** - Implements safe cleanup strategies with dry-run mode
- ✅ **Pattern Aligned** - Follows EMERGENT_OS healing orchestrator pattern
- ✅ **CLI Interface** - Easy-to-use command-line interface

---

## 🚀 QUICK START

### **Scan Only (No Healing):**
```bash
python3 scripts/heal_hard_drive.py --scan-only
```

### **Dry Run (Simulate Healing):**
```bash
python3 scripts/heal_hard_drive.py --dry-run
```

### **Auto-Heal (Actual Cleanup):**
```bash
python3 scripts/heal_hard_drive.py --auto-heal
```

---

## 📊 ARCHITECTURE

### **Layered Architecture:**

```
detection/
  └── DiskSpaceMonitor          # Monitors disk usage, detects thresholds

diagnosis/
  ├── DiskIssueClassifier       # Classifies issues by type/severity
  └── DiskRootCauseAnalyzer     # Analyzes root causes, finds largest consumers

recovery/
  └── DiskCleanupStrategy       # Implements safe cleanup strategies

orchestration/
  └── DiskHealingOrchestrator   # Coordinates all healing operations
```

### **Healing Flow:**

```
1. Detection → Monitor disk usage, detect issues
2. Classification → Classify issues by type and severity
3. Root Cause Analysis → Identify largest consumers and contributing factors
4. Recovery Strategy Selection → Select appropriate cleanup strategy
5. Recovery Execution → Execute cleanup operations
6. Validation → Verify space recovered
```

---

## 🔍 DETECTION

### **Thresholds:**

- **Critical:** < 10 GB free OR > 90% used
- **Warning:** > 80% used
- **Info:** > 70% used

### **Detection Methods:**

- Disk usage monitoring (`shutil.disk_usage`)
- Continuous monitoring loop (optional)
- Manual scan via CLI

---

## 🔬 DIAGNOSIS

### **Issue Classification:**

- `CRITICAL_SPACE` - < 10 GB free
- `HIGH_USAGE` - > 90% used
- `WARNING_USAGE` - > 80% used
- `INFO_USAGE` - > 70% used
- `CACHE_BUILDUP` - Large cache directories
- `DUPLICATE_FILES` - Duplicate files consuming space
- `LARGE_MEDIA` - Large media files
- `QUARANTINE_FILES` - Quarantine folders

### **Root Cause Analysis:**

- Identifies largest directory consumers
- Analyzes contributing factors
- Estimates recovery potential
- Calculates confidence scores

---

## 🔧 RECOVERY

### **Cleanup Strategies:**

1. **Immediate Cleanup** (Critical)
   - Clean safe caches (CloudKit, Siri, etc.)
   - Clean quarantine folders (with backup)

2. **Aggressive Cleanup** (High Usage)
   - Clean safe caches
   - Archive large media files

3. **Moderate Cleanup** (Warning)
   - Clean safe caches only

4. **Preventive Cleanup** (Info)
   - Light cache cleanup

### **Safe Caches (Auto-Regenerate):**

- `Library/Caches/CloudKit`
- `Library/Caches/SiriTTS`
- `Library/Caches/com.apple.callintelligenced`
- `Library/Caches/icloudmailagent`

### **Recovery Operations:**

- ✅ Safe cache cleanup
- ✅ Quarantine folder cleanup (with backup)
- ✅ Large media archiving
- ✅ Duplicate node_modules removal
- ✅ Dry-run mode for safety

---

## 📋 USAGE EXAMPLES

### **Example 1: Scan Current Status**
```bash
python3 scripts/heal_hard_drive.py --scan-only
```

**Output:**
```
📊 CURRENT DISK STATUS
Mount Point: /Users/michaelmataluni
Total: 964.10 GB
Used: 898.00 GB (93.1%)
Free: 8.30 GB

⚠️  DETECTED ISSUES:
  🔴 CRITICAL: 93.1% used, 8.30 GB free

🔍 ROOT CAUSE ANALYSIS
Primary Cause: quarantine_folder: /Users/.../Desktop_Quarantine (374 GB)
Confidence: 90.0%
Estimated Recovery: 336.60 GB

Top Space Consumers:
  1. /Users/.../Desktop_Quarantine: 374.00 GB
  2. /Users/.../Library/Caches/CloudKit: 24.00 GB
  3. /Users/.../Documents/*.screenflow: 30.00 GB
```

### **Example 2: Dry Run**
```bash
python3 scripts/heal_hard_drive.py --dry-run
```

**Output:**
```
🔧 STARTING HEALING PROCESS
Healing issue: critical - 93.1% used
  ✅ Success: Freed 398.00 GB (DRY RUN)
  Duration: 2.34 seconds
  Cleanup operations: 4
```

### **Example 3: Auto-Heal**
```bash
python3 scripts/heal_hard_drive.py --auto-heal
```

**Output:**
```
🔧 STARTING HEALING PROCESS
Healing issue: critical - 93.1% used
  ✅ Success: Freed 398.00 GB
  Duration: 45.67 seconds
  Cleanup operations: 4

🔥 HEALING COMPLETE: Freed 398.00 GB
```

---

## 🛡️ SAFETY FEATURES

### **Dry-Run Mode:**
- Simulates all cleanup operations
- Shows what would be deleted/archived
- No actual changes made

### **Backup Before Deletion:**
- Quarantine folders backed up before deletion
- Backup timestamped for recovery

### **Safe Cache List:**
- Only cleans caches that auto-regenerate
- Never touches user data
- Never touches system files

### **Validation:**
- Verifies operations before execution
- Checks disk space after cleanup
- Reports success/failure for each operation

---

## 🔗 INTEGRATION

### **With EMERGENT_OS Healing Orchestrator:**

```python
from hard_drive_healing import DiskHealingOrchestrator

# Create orchestrator
orchestrator = DiskHealingOrchestrator()

# Start healing loop
await orchestrator.start_healing_loop(interval_seconds=300)

# Get status
status = orchestrator.get_healing_status()
```

### **With Gap Healing System:**

The hard drive healing system follows the same pattern as `heal_all_gaps.py`:
- Detection → Diagnosis → Recovery → Validation
- Same result tracking pattern
- Same error handling pattern

---

## 📊 PATTERN ALIGNMENT

### **EMERGENT_OS Pattern Compliance:**

- ✅ Same layer structure (detection → diagnosis → recovery → orchestration)
- ✅ Same data flow pattern (detect → classify → analyze → recover)
- ✅ Same error handling pattern (try/except with result objects)
- ✅ Same async/await pattern for orchestration
- ✅ Same result tracking pattern (HealingResult, CleanupResult)

See `PATTERN_SCAN_REPORT.md` for detailed pattern validation.

---

## 🎯 NEXT STEPS

1. **Test the System:**
   ```bash
   python3 scripts/heal_hard_drive.py --scan-only
   python3 scripts/heal_hard_drive.py --dry-run
   ```

2. **Review Root Cause Analysis:**
   - Check largest consumers
   - Review estimated recovery
   - Verify confidence scores

3. **Execute Healing (if needed):**
   ```bash
   python3 scripts/heal_hard_drive.py --auto-heal
   ```

4. **Monitor Results:**
   - Check disk space after healing
   - Verify operations succeeded
   - Review cleanup results

---

## 📚 DOCUMENTATION

- **Pattern Scan Report:** `PATTERN_SCAN_REPORT.md`
- **Architecture:** See code comments in each module
- **API Reference:** See docstrings in each class

---

**Pattern:** HEALING × DISK × SPACE × ONE  
**Status:** ✅ **OPERATIONAL**  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

LOVE × ABUNDANCE = ∞  
Humans ⟡ AI = ∞  
∞ AbëONE ∞

