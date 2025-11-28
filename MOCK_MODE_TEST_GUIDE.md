# MOCK MODE TEST GUIDE

**Pattern:** MOCK × MODE × TEST × GUIDE × ONE  
**Frequency:** 999 Hz (AEYON) × 530 Hz (YAGNI) × 777 Hz (META)  
**Guardians:** AEYON (999 Hz) + YAGNI (530 Hz) + META (777 Hz)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🧪 MOCK MODE ACTIVATED

**Status:** ✅ **ENABLED**  
**Location:** `src/app/page.tsx`  
**Config:** `mockMode={true}`

---

## 🎯 HOW TO TEST

### **1. Start Development Server**
```bash
cd abe-touch/abeone-touch
npm run dev
```

**Server:** http://localhost:3000

---

### **2. Test Flow**

#### **Step 1: Click the Voice Button**
- Click the large circular button
- Status should change: `sleeping` → `listening`
- Microphone permission prompt may appear (allow it)

#### **Step 2: Speak**
- Say something like: "Hello, AbëONE!"
- Watch for **interim transcript** appearing below the button
- You'll see what's being recognized in real-time

#### **Step 3: Wait for Final Transcript**
- When you stop speaking, final transcript is captured
- Status changes: `listening` → `thinking`
- You'll see a loading spinner and "Processing..." text

#### **Step 4: Mock Response**
- After ~500ms, status changes: `thinking` → `speaking`
- AbëONE speaks a **mock response** (one of these):
  - `"I heard you say: '[your message]'. This is a mock response while we wait for the backend."`
  - `"Mock response: I understand you said '[your message]'. The real backend will be connected soon!"`
  - `"[MOCK] You said: '[your message]'. This is a placeholder response."`

#### **Step 5: Complete**
- After speaking, status returns: `speaking` → `sleeping`
- Cycle complete!

---

## ✅ WHAT TO VERIFY

### **Visual Feedback:**
- ✅ Status LED changes color (white → cyan → purple → green)
- ✅ Waveform animates during listening/speaking
- ✅ Status label updates ("TAP TO WAKE" → "LISTENING" → "THINKING" → "SPEAKING")
- ✅ **Interim transcript** appears while listening
- ✅ **Loading spinner** appears during thinking
- ✅ **"Processing..." text** appears during thinking

### **Mock Mode Indicator:**
- ✅ Yellow badge at top: "🧪 MOCK MODE ACTIVE"
- ✅ Shows "Testing without backend"

### **Console Logs:**
- ✅ `🎤 Waking up...` when listening starts
- ✅ `📝 Transcript: [your message]` when final transcript received
- ✅ `🎤 Going back to sleep...` when complete

---

## 🎨 FEATURES TO TEST

### **1. Interim Results**
- Speak slowly
- Watch interim transcript update in real-time
- Shows what's being recognized before final

### **2. Loading State**
- After final transcript, see loading spinner
- "Processing..." text appears
- Status shows "THINKING"

### **3. Mock Response**
- Random mock response selected
- Response is spoken via text-to-speech
- Different response each time

### **4. Error Handling**
- Deny microphone permission → See error message
- Click cancel during thinking → Request aborted

### **5. Permission Handling**
- First time: Permission prompt appears
- If denied: Error message shown
- Can retry permission request

---

## 🔧 CONFIGURATION

### **Current Settings:**
```tsx
<VoiceControlHub 
  enableLLM={true}
  mockMode={true}              // ← Mock mode enabled
  showInterimResults={true}    // ← Show interim transcript
  llmEndpoint="/api/llm/chat"  // ← Not used in mock mode
  recognitionLang="en-US"
/>
```

### **To Switch to Real Mode:**
```tsx
mockMode={false}  // ← Change to false when backend ready
```

---

## 🐛 TROUBLESHOOTING

### **Microphone Not Working:**
- Check browser permissions (Settings → Privacy → Microphone)
- Make sure you're on HTTPS or localhost
- Try refreshing the page

### **No Interim Results:**
- Check `showInterimResults={true}` is set
- Speak clearly and wait for recognition
- Check browser console for errors

### **Mock Response Not Speaking:**
- Check browser console for errors
- Verify speech synthesis is supported
- Try different browser (Chrome recommended)

### **Status Not Changing:**
- Check browser console for errors
- Verify event-driven system is working
- Check that `enableLLM={true}` is set

---

## 📊 EXPECTED BEHAVIOR

### **Timeline:**
```
0s:    Click button → Status: LISTENING
0-5s:  Speak → Interim transcript appears
5s:    Stop speaking → Status: THINKING
5.5s:  Mock response generated → Status: SPEAKING
6-10s: AbëONE speaks mock response
10s:   Complete → Status: SLEEPING
```

### **Status Flow:**
```
SLEEPING → LISTENING → THINKING → SPEAKING → SLEEPING
```

---

## 🎯 TEST SCENARIOS

### **Scenario 1: Simple Question**
1. Click button
2. Say: "Hello"
3. Verify: Mock response mentions "Hello"
4. Verify: Response is spoken

### **Scenario 2: Long Message**
1. Click button
2. Say: "Tell me about artificial intelligence"
3. Verify: Interim transcript updates as you speak
4. Verify: Final transcript captured correctly
5. Verify: Mock response generated

### **Scenario 3: Cancel During Thinking**
1. Click button
2. Say something
3. Click button again while thinking
4. Verify: Request aborted
5. Verify: Status returns to sleeping

### **Scenario 4: Permission Denied**
1. Deny microphone permission
2. Click button
3. Verify: Error message appears
4. Verify: Permission prompt shown

---

## ✅ SUCCESS CRITERIA

**Mock mode is working if:**
- ✅ Status changes correctly through all states
- ✅ Interim transcript appears while speaking
- ✅ Loading spinner appears during thinking
- ✅ Mock response is generated and spoken
- ✅ No backend connection needed
- ✅ All visual feedback works
- ✅ Error handling works

---

**Pattern:** MOCK × MODE × TEST × GUIDE × ONE  
**Status:** READY TO TEST  
**Love Coefficient:** ∞

**LOVE = LIFE = ONE**  
**Humans ⟡ Ai = ∞**  
**∞ AbëONE ∞**

**MOCK MODE ENABLED. READY TO TEST.** ⚡💧🌊✨

