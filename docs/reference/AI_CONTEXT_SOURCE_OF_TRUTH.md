# 🤖 AI CONTEXT SOURCE OF TRUTH

**File**: `.ai-context-source-of-truth.json`  
**Pattern**: OBSERVER × TRUTH × ATOMIC × ONE  
**Guardian**: AEYON (999 Hz)  
**Status**: ✅ **OPERATIONAL - ETERNAL - VALIDATED**

---

## 🎯 PURPOSE

Single source of truth optimized for AI consumption across context windows. Provides cross-context clarity for AI systems working with multiple projects simultaneously.

---

## ✨ KEY FEATURES

### 1. Multi-Project Awareness ✅
- **KNOWS** that users work on multiple projects simultaneously
- Tracks active projects across different context windows
- Maintains project relationships and dependencies

### 2. Cross-Context Clarity ✅
- Tracks current directory and project
- Maintains recent context history
- Provides active context windows list

### 3. AI-Optimized Format ✅
- JSON structure optimized for AI parsing
- Hierarchical organization
- Key fields clearly marked
- High readability

### 4. Automatic Updates ✅
- Updates on chat input (before response)
- Updates on chat output (after response)
- **2x per chat sequence** - ensures always current
- Non-blocking background updates

### 5. Eternal & Validated ✅
- Eternal: Designed to persist forever
- Validated: All patterns validated
- Source pattern compliant
- AI pattern optimized

---

## 📋 STRUCTURE

```json
{
  "_meta": {
    "version": "1.0.0",
    "lastUpdated": "ISO timestamp",
    "updateFrequency": "2x per chat sequence (input + output)",
    "eternal": true,
    "validated": true
  },
  "workspace": {
    "root": "AbeOne_Master",
    "currentDirectory": "current directory name",
    "currentProject": "current project name",
    "contextWindows": []
  },
  "projects": {
    "active": [...],
    "legacy": [...]
  },
  "contextTracking": {
    "multiProjectAware": true,
    "activeContexts": [...],
    "recentContexts": [...]
  },
  "aiOptimization": {
    "format": "JSON",
    "parsing": "optimized",
    "keyFields": [...],
    "updateTriggers": ["chat_input", "chat_output"]
  },
  "validation": {
    "sourcePattern": true,
    "aiPattern": true,
    "eternal": true,
    "autoUpdate": true
  }
}
```

---

## 🚀 USAGE

### For AI Systems

**Read Context**:
```bash
node scripts/read-ai-context.js
```

**Update Context** (automatic, but manual available):
```bash
node scripts/update-ai-context-source-of-truth.js
```

**Validate Context**:
```bash
node scripts/validate-ai-context-source.js
```

### For Humans

The source of truth updates automatically on every chat interaction. No manual intervention needed.

---

## 🔄 UPDATE MECHANISM

### Automatic Triggers

1. **Chat Input** → `node scripts/trigger-visual-update.js`
   - Updates source of truth
   - Updates visual status
   - Non-blocking

2. **Chat Output** → `node scripts/trigger-visual-update.js`
   - Updates source of truth
   - Updates visual status
   - Non-blocking

### What Gets Updated

- Current directory and project
- Recent context windows (last 10)
- Active contexts (current + recent unique, max 5)
- Project lastWorkedOn timestamps
- Project context windows (per project, max 5)
- Last updated timestamp

---

## ✅ VALIDATION

**Validated For**:
- ✅ AI pattern optimization
- ✅ Source pattern compliance
- ✅ Multi-project awareness
- ✅ Eternal design
- ✅ Auto-update mechanism

**Validation Command**:
```bash
node scripts/validate-ai-context-source.js
```

---

## 🎯 KEY PRINCIPLES

1. **Multi-Project Reality**: System KNOWS users work on multiple projects simultaneously
2. **Cross-Context Clarity**: Provides context across different AI context windows
3. **Always Current**: Updates 2x per chat sequence (input + output)
4. **AI-Optimized**: JSON format optimized for AI parsing and consumption
5. **Eternal**: Designed to persist and scale forever
6. **Non-Blocking**: Updates never block work

---

## 📊 EXAMPLE OUTPUT

```json
{
  "_meta": {
    "lastUpdated": "2025-11-19T00:25:32.995Z",
    "updateFrequency": "2x per chat sequence (input + output)"
  },
  "workspace": {
    "currentDirectory": "AbeOne_Master",
    "currentProject": "AbeOne_Master"
  },
  "contextTracking": {
    "multiProjectAware": true,
    "activeContexts": [
      {
        "directory": "AbeOne_Master",
        "project": "AbeOne_Master",
        "status": "unknown",
        "timestamp": "2025-11-19T00:25:32.995Z"
      }
    ]
  }
}
```

---

**Pattern**: OBSERVER × TRUTH × ATOMIC × ONE  
**Status**: ✅ **OPERATIONAL - ETERNAL - VALIDATED**  
**Update Frequency**: 2x per chat sequence  
**∞ AbëONE ∞**

