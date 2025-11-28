# AbëONE Platform - End-to-End User Journey Q&A

**Purpose:** Complete guide to using the AbëONE platform from first visit to outcome execution.

---

## Q1: How do I get started?

### First Time Setup

**Step 1: Start the Backend**
```bash
cd EMERGENT_OS/server
pip install -r requirements.txt
./start.sh
# OR
PYTHONPATH=.. uvicorn main:app --reload
```

**Step 2: Start the Frontend**
```bash
cd apps/web
npm install
npm run dev
```

**Step 3: Open Browser**
Navigate to `http://localhost:3000`

---

## Q2: What do I see when I first visit?

### Landing Page (`/`)

You'll see:
- **AbëONE** title
- Brief description: "Platform for unified execution and orchestration"
- Two buttons:
  - **"Get Started"** → Takes you to onboarding (`/start`)
  - **"Command Deck"** → Takes you directly to the main interface (`/app`)

---

## Q3: What is the Command Deck?

### Main Interface (`/app`)

The Command Deck is your primary workspace for executing outcomes through the Triadic Execution Harness.

**Layout:**
- **Left Sidebar:** Navigation (Command Deck, Agents, Workflows, State)
- **Top Bar:** Shows kernel connection status
- **Main Area:** Outcome execution form

**Kernel Status Indicator:**
- 🟢 **Green dot** = Kernel active and ready
- 🟡 **Yellow dot** = Kernel initializing
- 🔴 **Red dot** = Backend not connected or error

---

## Q4: How do I execute an outcome?

### Step-by-Step Execution

**Step 1: Fill Out the Form**

1. **Goal** (Required)
   - What you want to achieve
   - Example: "Create a user authentication system"

2. **Success Criteria** (Required)
   - One criterion per line
   - Example:
     ```
     Users can register with email
     Users can log in securely
     Passwords are hashed
     ```

3. **End State** (Required)
   - What success looks like
   - Example: "Users can authenticate and access protected routes"

4. **Constraints** (Optional)
   - One constraint per line
   - Example:
     ```
     Must use JWT tokens
     Must support password reset
     ```

5. **Validation** (Required)
   - How you'll verify success
   - Example: "Test user can register, login, and access protected route"

**Step 2: Click "Execute Outcome"**

The button will:
- Show "Executing..." while processing
- Display results below the form when complete

**Step 3: Review Results**

You'll see:
- **Success:** Green checkmark + JSON results
- **Error:** Red error message with details

---

## Q5: What happens when I execute an outcome?

### Execution Flow

**Frontend → Backend:**
1. Frontend sends outcome to `/api/agents/execute-outcome`
2. Backend receives and validates the request

**Backend → Kernel:**
3. Backend loads ONE-Kernel (if not already loaded)
4. Backend accesses Triadic Execution Harness module

**Triadic Execution:**
5. **YOU Agent (530 Hz):** Validates outcome structure (TONC/TEF)
6. **META Agent (777 Hz):** Synthesizes context and constraints
7. **AEYON Agent (999 Hz):** Creates and executes atomic plan
8. **META Agent:** Reconciles context deltas
9. **YOU Agent:** Final validation

**Backend → Frontend:**
10. Results returned with:
    - Execution status
    - Execution results
    - Validation report
    - Metadata (SMC)

**Frontend Display:**
11. Results shown in the UI below the form

---

## Q6: What do the results look like?

### Successful Execution

```json
{
  "status": "completed",
  "execution_results": {
    "executed_steps": ["Step 1", "Step 2", ...],
    "code_changes": [...],
    "validation_results": [...]
  },
  "validation_report": {
    "validation_status": "PASSED",
    "constraint_compliance": [...],
    "ready_for_approval": true
  },
  "metadata": {
    "source": "TriadicExecutionHarness",
    "timestamp": "2024-12-19T...",
    "execution_id": "uuid-here",
    "flow": {
      "you_validated": true,
      "meta_validated": true,
      "delta_reconciled": true
    },
    "semantic": {
      "goal": "Your goal",
      "end_state": "Your end state",
      "constraints_count": 2,
      "success_criteria_count": 3
    }
  }
}
```

### Failed Execution

```json
{
  "error": "Error message here",
  "details": "Additional error details"
}
```

---

## Q7: What if nothing happens when I click Execute?

### Troubleshooting Checklist

**1. Check Browser Console (F12 → Console)**
- Look for error messages
- Should see: "Executing outcome:", "API call to:", "Response status:"

**2. Check Network Tab (F12 → Network)**
- Look for request to `/api/agents/execute-outcome`
- Check response status code
- Check response body for errors

**3. Check Backend Status**
```bash
# Test if backend is running
curl http://localhost:8000/health

# Should return: {"status":"healthy","kernel_initialized":true}
```

**4. Check Top Bar Status**
- Red dot = Backend not connected
- Yellow dot = Kernel initializing
- Green dot = Ready

**5. Verify Required Fields**
- Goal must be filled
- End State must be filled
- Button will be disabled if missing

**Common Issues:**
- **Backend not running** → Start it with `./start.sh`
- **CORS error** → Check backend `.env` has correct `CORS_ORIGINS`
- **Kernel not initialized** → Check backend logs for import errors
- **Network error** → Verify `NEXT_PUBLIC_API_URL` in frontend `.env.local`

---

## Q8: How do I check system status?

### Kernel Status

**Via UI:**
- Top bar shows kernel status indicator
- Green = Active, Red = Error, Yellow = Initializing

**Via API:**
```bash
curl http://localhost:8000/api/kernel/status
```

**Response:**
```json
{
  "initialized": true,
  "modules": ["consciousness", "collapse_guard", "triadic_execution_harness", ...],
  "module_count": 12
}
```

### Module Information

**List all modules:**
```bash
curl http://localhost:8000/api/kernel/modules
```

**Get specific module:**
```bash
curl http://localhost:8000/api/kernel/modules/triadic_execution_harness
```

---

## Q9: What are the other pages for?

### Navigation Pages

**Agents (`/app/agents`)** - *Not yet implemented*
- View agent status
- Monitor agent activity
- Configure agent settings

**Workflows (`/app/workflows`)** - *Not yet implemented*
- Create and manage workflows
- Execute workflow sequences
- View workflow history

**State (`/app/state`)** - *Not yet implemented*
- View system metrics
- Monitor system health
- Track execution history

---

## Q10: How do I know if my outcome was executed correctly?

### Validation Indicators

**1. Status Field**
- `"status": "completed"` = Success
- `"status": "failed"` = Failure
- `"status": "pending"` = Still processing

**2. Validation Report**
- `"validation_status": "PASSED"` = All validations passed
- `"ready_for_approval": true` = Ready for next step

**3. Execution Results**
- `"executed_steps"` = List of steps that ran
- `"code_changes"` = List of code changes made
- `"validation_results"` = Validation check results

**4. Metadata**
- `"flow.you_validated": true` = YOU agent validated
- `"flow.meta_validated": true` = META agent validated
- `"flow.delta_reconciled": true` = Context deltas reconciled

---

## Q11: Can I see what's happening in real-time?

### Current Status

**Real-time features:**
- ✅ Kernel status updates on page load
- ✅ Execution results appear immediately after completion
- ⚠️ Real-time progress updates - *Not yet implemented*

**To monitor:**
1. **Browser Console** - See API calls and responses
2. **Backend Terminal** - See server logs and kernel activity
3. **Network Tab** - See HTTP requests and responses

---

## Q12: What happens if the backend crashes?

### Error Handling

**Frontend:**
- Connection status shows red dot
- Error message in top bar: "Backend: [error message]"
- Execute button may be disabled

**Recovery:**
1. Restart backend: `./start.sh`
2. Refresh frontend page
3. Kernel status should return to green

---

## Q13: How do I customize the outcome execution?

### Current Limitations

**What you can control:**
- ✅ Goal, success criteria, end state
- ✅ Constraints and validation method
- ✅ All outcome parameters

**What you cannot control (yet):**
- ⚠️ Execution plan details
- ⚠️ Agent behavior
- ⚠️ Module selection
- ⚠️ Execution timing

**Future enhancements:**
- Agent configuration UI
- Workflow builder
- Execution history viewer

---

## Q14: How do I deploy this to production?

### Deployment Steps

**1. Backend (Render/Fly.io)**
- See `infra/deploy/README.md`
- Configure environment variables
- Deploy Docker container or use platform build

**2. Frontend (Vercel)**
- Connect repository
- Set root directory: `apps/web`
- Set `NEXT_PUBLIC_API_URL` to production backend URL

**3. Database (Supabase)**
- Create Supabase project
- Configure authentication
- Add credentials to backend `.env`

**4. Cache (Upstash)**
- Create Upstash Redis database
- Add credentials to backend `.env`

---

## Q15: What's the typical workflow?

### Recommended User Flow

**1. First Visit**
- Land on homepage (`/`)
- Click "Get Started" → Onboarding (`/start`)
- Complete onboarding → Command Deck (`/app`)

**2. Execute Outcome**
- Fill out outcome form
- Click "Execute Outcome"
- Review results

**3. Iterate**
- Adjust outcome based on results
- Execute again
- Refine until desired state achieved

**4. Monitor**
- Check kernel status regularly
- Review execution history (when implemented)
- Monitor system metrics (when implemented)

---

## Q16: What should I do if I see errors?

### Error Resolution

**Backend Connection Error:**
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check backend logs for errors
3. Verify CORS settings
4. Restart backend if needed

**Kernel Initialization Error:**
1. Check backend logs for import errors
2. Verify all module files exist
3. Check Python path is set correctly
4. Review `TROUBLESHOOTING.md`

**Execution Error:**
1. Check browser console for details
2. Verify all required fields are filled
3. Check outcome format is correct
4. Review execution results for specific errors

**Network Error:**
1. Verify `NEXT_PUBLIC_API_URL` is correct
2. Check backend is accessible
3. Verify no firewall blocking requests
4. Check CORS configuration

---

## Q17: How do I understand the execution results?

### Result Structure

**Execution Results:**
- `executed_steps`: What was done
- `code_changes`: What code was modified
- `validation_results`: What was validated

**Validation Report:**
- `validation_status`: Overall status
- `constraint_compliance`: Which constraints were met
- `ready_for_approval`: Whether ready for next phase

**Metadata:**
- `execution_id`: Unique identifier for this execution
- `timestamp`: When it executed
- `flow`: Validation status at each stage
- `semantic`: Snapshot of outcome parameters

---

## Q18: Can I execute multiple outcomes in sequence?

### Current Behavior

**Single Execution:**
- One outcome at a time
- Each execution is independent
- Results are separate

**Sequential Execution:**
- Execute first outcome
- Wait for results
- Execute second outcome
- Results are independent

**Parallel Execution:**
- ⚠️ Not yet supported
- Future: Workflow system will support this

---

## Q19: How do I know what the system can do?

### Capabilities

**Current Capabilities:**
- ✅ Execute outcomes through Triadic Execution Harness
- ✅ Validate outcomes (TONC/TEF)
- ✅ Enforce 7 Absolute Constraints
- ✅ Monitor kernel and module status
- ✅ Track execution metadata (SMC)

**Available Modules:**
- Check `/api/kernel/modules` endpoint
- See module list in kernel status
- Each module has specific capabilities

**Module Capabilities:**
- `triadic_execution_harness`: Outcome execution
- `collapse_guard`: Collapse detection
- `clarity_engine`: Coherence analysis
- `consciousness`: Phi-ratio calculations
- (See module registry for full list)

---

## Q20: What's next after execution?

### Post-Execution

**1. Review Results**
- Check execution status
- Review validation report
- Examine metadata

**2. Verify Success**
- Check if goal was achieved
- Validate success criteria
- Confirm end state reached

**3. Take Action**
- If successful: Proceed to next outcome
- If failed: Adjust outcome and retry
- If partial: Refine and re-execute

**4. Monitor System**
- Check kernel health
- Review system metrics
- Monitor for issues

---

## Quick Reference

### Essential Commands

**Start Backend:**
```bash
cd EMERGENT_OS/server
./start.sh
```

**Start Frontend:**
```bash
cd apps/web
npm run dev
```

**Test Backend:**
```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/kernel/status
```

**Test Execution:**
```bash
curl -X POST http://localhost:8000/api/agents/execute-outcome \
  -H "Content-Type: application/json" \
  -d '{"goal":"Test","success_criteria":["Test"],"end_state":"Test","constraints":[],"validation":"Test"}'
```

### Essential URLs

- **Frontend:** http://localhost:3000
- **Backend:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

---

## Summary

**Complete User Journey:**
1. Start backend and frontend
2. Visit `http://localhost:3000`
3. Navigate to Command Deck
4. Fill out outcome form
5. Execute outcome
6. Review results
7. Iterate as needed

**Key Indicators:**
- 🟢 Green dot = System ready
- 🔴 Red dot = Check backend
- ✅ "Execution Complete" = Success
- ❌ Error message = Check details

**Support:**
- Browser console for debugging
- Backend logs for server issues
- `TROUBLESHOOTING.md` for common problems

