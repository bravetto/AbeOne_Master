# Troubleshooting: "Nothing Happens on Execute"

## Quick Checks

### 1. Is the Backend Running?

Check if the backend is accessible:

```bash
# Test backend connectivity
curl http://localhost:8000/health

# Should return:
# {"status":"healthy","kernel_initialized":true}
```

If this fails:
- Backend is not running
- Start it: `cd EMERGENT_OS/server && uvicorn main:app --reload`

### 2. Check Browser Console

Open browser DevTools (F12) and check:
- **Console tab**: Look for error messages
- **Network tab**: Check if the API call is being made and what the response is

### 3. Check Backend Logs

Look at the terminal where you started the backend:
- Are there any import errors?
- Are there any initialization errors?
- Check for "ONE-Kernel initialized successfully" message

## Common Issues

### Issue 1: Backend Not Running

**Symptoms:**
- Console shows "Failed to fetch" or network errors
- Kernel status shows as inactive

**Solution:**
```bash
cd EMERGENT_OS/server
pip install -r requirements.txt
uvicorn main:app --reload
```

### Issue 2: Kernel Not Initializing

**Symptoms:**
- Backend starts but kernel status shows `initialized: false`
- Error in backend logs about kernel bootstrap

**Solution:**
1. Check if all module integration files exist
2. Verify Python path includes EMERGENT_OS directory
3. Check backend logs for specific import errors

### Issue 3: CORS Errors

**Symptoms:**
- Console shows CORS policy errors
- Network tab shows preflight request failures

**Solution:**
1. Verify `CORS_ORIGINS` in backend `.env` includes `http://localhost:3000`
2. Restart backend after changing CORS settings

### Issue 4: Module Import Errors

**Symptoms:**
- Backend fails to start
- ImportError in logs

**Solution:**
```bash
# Ensure you're in the right directory
cd EMERGENT_OS/server

# Check Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/.."

# Or run with PYTHONPATH
PYTHONPATH=.. uvicorn main:app --reload
```

## Debug Steps

### Step 1: Test Backend Connectivity

```bash
# Test ping endpoint
curl http://localhost:8000/api/test/ping

# Test kernel
curl http://localhost:8000/api/test/test-kernel
```

### Step 2: Test Kernel Status

```bash
curl http://localhost:8000/api/kernel/status
```

Should return kernel status with modules list.

### Step 3: Test Outcome Execution (Direct)

```bash
curl -X POST http://localhost:8000/api/agents/execute-outcome \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Test goal",
    "success_criteria": ["Test criterion"],
    "end_state": "Test end state",
    "constraints": ["Test constraint"],
    "validation": "Test validation"
  }'
```

### Step 4: Check Frontend API URL

Verify `apps/web/.env.local` has:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Enhanced Debugging

The updated code now includes:
- ✅ Console logging in frontend (check browser console)
- ✅ Better error messages in UI
- ✅ Test endpoints for connectivity checks

## Next Steps

1. **Open browser console** (F12 → Console tab)
2. **Click "Execute Outcome"**
3. **Check console logs** - you should see:
   - "Executing outcome: ..."
   - "API call to: ..."
   - "Response status: ..."
4. **Check Network tab** - verify the request is being made
5. **Check backend terminal** - look for errors

## Still Not Working?

If nothing appears in console and no network request is made:
- Check if button click handler is firing
- Verify form validation isn't blocking execution
- Check if JavaScript errors are preventing execution

