# 🔎 ACTIONABLE REQUEST DETECTION MODULE (ARDM)

**Purpose:** Ensure no operational request is missed

**Mode:** AbëONE + Cursor.ai Optimized

**Pattern:** OBSERVER × TRUTH × ATOMIC × ONE

**Frequency:** 530 Hz (Coherence) × 999 Hz (AEYON)

**Love Coefficient:** ∞

**∞ AbëONE ∞**

---

## 🎯 PRIME DIRECTIVE

**"SCAN EVERY CONVERSATION FOR ACTIONABLE ITEMS. NEVER MISS AN OPERATIONAL REQUEST."**

The ARDM acts as a backstop guardian, ensuring that every actionable request—whether explicit or implicit—is detected, classified, and operationalized.

---

## 📋 CLASSIFICATION SYSTEM

When scanning the conversation for actionable items, you MUST classify requests into four categories:

### CATEGORY A — CODE ACTIONS

- Code snippets to implement
- File creation
- Architecture refactors
- Schema updates
- Database migrations
- API endpoints
- Component implementations

**Detection Patterns:**
- "Implement X"
- "Create a file for Y"
- "Add Z to the schema"
- "Refactor A to B"
- Code blocks provided in conversation
- Explicit file paths mentioned

---

### CATEGORY B — NON-CODE SYSTEM OBLIGATIONS

- Architecture modules requested (e.g., SS-2L)
- Bootstrap layers
- Validators
- Pre-commit hooks
- Substrate gatekeepers
- Infrastructure components
- Deployment configurations
- CI/CD pipelines

**Detection Patterns:**
- "Build X module"
- "Create validator for Y"
- "Set up Z infrastructure"
- "Configure deployment"
- References to architectural patterns
- System-level requirements

---

### CATEGORY C — PROTOCOLS REQUIRING MANIFESTATION

- Guardrails
- Execution rules
- Enforcement scripts
- Boundary modules
- Compliance checks
- Security policies
- Operational protocols

**Detection Patterns:**
- "Enforce X"
- "Create guardrail for Y"
- "Implement protocol Z"
- "Add boundary check"
- Security/compliance mentions
- Policy requirements

---

### CATEGORY D — CONTINUATIONS OR PROMISED DELIVERABLES

Any time you say:
- "Generate X"
- "Build Y"
- "Operationalize Z"
- "I'll create X"
- "Let me implement Y"
- "Next, I'll build Z"

These are actionable even without provided code.

**Detection Patterns:**
- Commitments made in conversation
- Promises to deliver
- "I will" statements
- "Next step" mentions
- Implicit continuations from earlier requests

---

## ⚡ EXECUTION RULES

### RULE 1: Never Conclude "Nothing to Operationalize"

Never conclude "nothing to operationalize" unless:
- Category A returns empty
- Category B returns empty
- Category C returns empty
- Category D returns empty

**All four categories must be empty** before concluding no actionable items exist.

---

### RULE 2: Module Requests ARE Actionable

Requests for modules (SS-2L, Bootstrap, SRE Enforcement) ARE actionable.

Do not dismiss architectural requests as "planning" or "future work."

If a module is requested, it must be:
1. Detected
2. Classified
3. Operationalized (or explicitly deferred with reason)

---

### RULE 3: Protocol Documents Require Substrate

Protocol documents are NOT considered complete until:
- The associated substrate layer is instantiated
- The enforcement mechanism exists
- The validation script is operational

**Protocol without substrate = Incomplete deliverable**

---

### RULE 4: Historical Commitments Count

If a deliverable was requested earlier in the conversation, it IS actionable even if the user didn't restate it.

**Scan the entire conversation history**, not just the current message.

---

### RULE 5: Mandatory Output Format

After detection, produce:

1. **DELTA** — What's missing
   - List of undelivered items
   - Classification by category
   - Priority assessment

2. **PATCHBLOCK** — The deliverable
   - Exact code/files to create
   - Implementation steps
   - Integration points

3. **POST-VALIDATION** — State after patch
   - Verification checklist
   - Expected outcomes
   - Success criteria

---

## 🛡️ BACKSTOP RULE

**Whenever the scanner is uncertain:**

1. **Default to ACTIONABLE**
   - When in doubt, classify as actionable
   - Better to over-detect than under-detect

2. **Ask for Clarification** (if truly ambiguous)
   - But only after exhaustive scanning
   - Provide specific questions
   - Don't use ambiguity as an excuse to skip

3. **Document the Uncertainty**
   - Include in DELTA report
   - Mark as "REQUIRES_CLARIFICATION"
   - But still operationalize what is clear

4. **Follow the Pattern**
   - Use existing validation patterns
   - Align with MEASURE_TWICE_CUT_ONCE protocol
   - Respect YAGNI principles

---

## 🔄 INTEGRATION WITH EXISTING SYSTEMS

### ARDM × META ORCHESTRATOR

ARDM feeds into the Meta Orchestrator's convergence process:
1. ARDM detects actionable items
2. Meta Orchestrator operationalizes them
3. Validation confirms completion

### ARDM × MEASURE TWICE CUT ONCE

ARDM respects substrate requirements:
- Never fabricate missing substrate
- Report exact missing elements
- Wait for explicit authorization before creating

### ARDM × YAGNI

ARDM applies YAGNI filter:
- Only detect truly needed items
- Avoid speculative detection
- Focus on explicit or clearly implied requests

---

## 📊 DETECTION ALGORITHM

```
1. SCAN: Read entire conversation context
2. EXTRACT: Identify all potential actionable items
3. CLASSIFY: Assign to Category A, B, C, or D
4. VALIDATE: Check against existing codebase (avoid duplicates)
5. PRIORITIZE: Order by urgency and dependencies
6. REPORT: Generate DELTA + PATCHBLOCK + POST-VALIDATION
7. EXECUTE: Operationalize detected items
8. VERIFY: Confirm completion
```

---

## 🎨 OUTPUT TEMPLATE

### DELTA Report

```
## DELTA: Missing Actionable Items

### Category A — Code Actions
- [ ] Item 1: Description
- [ ] Item 2: Description

### Category B — System Obligations
- [ ] Item 1: Description
- [ ] Item 2: Description

### Category C — Protocols
- [ ] Item 1: Description
- [ ] Item 2: Description

### Category D — Continuations
- [ ] Item 1: Description
- [ ] Item 2: Description
```

### PATCHBLOCK Report

```
## PATCHBLOCK: Implementation Plan

### File: path/to/file.ext
```language
[Exact code to implement]
```

### Integration Points
- Point 1
- Point 2
```

### POST-VALIDATION Report

```
## POST-VALIDATION: Success Criteria

### Verification Checklist
- [ ] File created at correct path
- [ ] Code compiles/runs without errors
- [ ] Integration tests pass
- [ ] Documentation updated

### Expected State
- State 1
- State 2
```

---

## 🚀 USAGE

### Manual Execution

```bash
python scripts/detect-actionable-requests.py --context "conversation_text"
```

### Integration with Cursor.ai

ARDM runs automatically:
1. Before responding to user (detect pending items)
2. After completing response (verify all delivered)
3. On explicit request (manual scan)

### Continuous Monitoring

ARDM can be integrated into:
- Pre-commit hooks
- CI/CD pipelines
- Validation scripts
- Meta orchestrator workflows

---

## ✅ VALIDATION

After implementing ARDM, validate with:

```bash
python scripts/validate_ardm_implementation.py
```

**Success Criteria:**
- ✅ Detects all four categories
- ✅ Integrates with existing validation infrastructure
- ✅ Respects YAGNI and substrate requirements
- ✅ Produces DELTA + PATCHBLOCK + POST-VALIDATION
- ✅ Never misses explicit requests
- ✅ Handles continuations correctly

---

# 🧿 END OF PROTOCOL

**Pattern:** OBSERVER × TRUTH × ATOMIC × ONE  
**Status:** ✅ ACTIVE  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

