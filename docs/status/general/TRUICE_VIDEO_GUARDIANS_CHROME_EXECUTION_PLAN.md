# 🔥 TRUICE VIDEO + 8 GUARDIANS + CHROME EXTENSION — EXECUTION PLAN

**Status:** ⚡ **READY TO EXECUTE**  
**Pattern:** TRUICE × GUARDIANS × CHROME × EXECUTION × ONE  
**Frequency:** 999 Hz (AEYON)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🎯 MISSION

**3 Critical Tasks:**
1. ✅ **Finish Truice Video** - Process green screen video into music video
2. ✅ **8 Guardian Microservices** - Make all 8 operational
3. ✅ **Fix Chrome Extension** - Fix Bias Guard in Chrome extension

---

## 📋 TASK 1: FINISH TRUICE VIDEO

### Current Status

**Location:** `PRODUCTS/abebeats/variants/abebeats_tru/`

**What Exists:**
- ✅ Green screen processing pipeline (`tru_music_video_pipeline.py`)
- ✅ Chroma key processing (advanced tolerance for dingy screens)
- ✅ Audio analysis and synchronization
- ✅ Background generation
- ✅ Composition engine

**What's Needed:**
- ⚠️ Complete the video generation workflow
- ⚠️ Test with Truice's green screen video
- ⚠️ Generate final output

### Execution Steps

**Step 1: Locate Truice Green Screen Video**
```bash
# Find Truice's green screen video file
find . -name "*truice*" -o -name "*green*screen*" -type f
```

**Step 2: Run Video Pipeline**
```python
from PRODUCTS.abebeats.variants.abebeats_tru.src.tru_music_video_pipeline import TruMusicVideoPipeline

pipeline = TruMusicVideoPipeline()

result = await pipeline.create_music_video(
    prompt="Truice viral single",
    audio_file="path/to/truice/audio.mp3",
    green_screen_footage="path/to/truice/green_screen.mp4",
    output_dir="output/truice_video"
)
```

**Step 3: Verify Output**
- ✅ Check video quality
- ✅ Verify chroma key (no green spill)
- ✅ Verify audio sync
- ✅ Verify background composition

---

## 📋 TASK 2: 8 GUARDIAN MICROSERVICES

### Current Status

**Location:** `AIGuards-Backend/aiguardian-repos/guardian-*-service/`

**What Exists:**
- ✅ All 8 Guardian services generated (guardian-one through guardian-eight)
- ✅ FastAPI structure complete
- ✅ Dockerfiles and K8s manifests
- ✅ Core infrastructure (config, logging, metrics)

**What's Needed:**
- ⚠️ Implement business logic for each Guardian
- ⚠️ Add Guardian-specific endpoints
- ⚠️ Integrate Guard Mesh clients
- ⚠️ Test and deploy

### Guardian Business Logic Implementation

**Guardian One (Intuition Synthesizer) - Port 8008**
```python
# services/guardian_service.py
async def analyze_intuition(self, content: str) -> Dict:
    # Intuitive pattern recognition
    patterns = await self.detect_patterns(content)
    insights = await self.generate_insights(patterns)
    return {"patterns": patterns, "insights": insights}
```

**Guardian Two (Synthesis Orchestrator) - Port 8009**
```python
async def synthesize(self, sources: List[Dict]) -> Dict:
    # Multi-source synthesis
    unified = await self.unify_sources(sources)
    return {"synthesis": unified}
```

**Guardian Three (Alignment Validator) - Port 8010**
```python
async def validate_alignment(self, content: str) -> Dict:
    # Truth alignment validation
    alignment = await self.check_alignment(content)
    return {"aligned": alignment}
```

**Guardian Four (Clarity Engine) - Port 8011**
```python
async def generate_clarity(self, content: str) -> Dict:
    # Clarity generation
    clarified = await self.simplify(content)
    return {"clarified": clarified}
```

**Guardian Five (Execution Orchestrator) - Port 8012**
```python
async def execute(self, plan: Dict) -> Dict:
    # Atomic execution
    result = await self.execute_atomically(plan)
    return {"result": result}
```

**Guardian Six (Memory Keeper) - Port 8013**
```python
async def store_memory(self, content: str) -> Dict:
    # Memory persistence
    memory_id = await self.persist(content)
    return {"memory_id": memory_id}
```

**Guardian Seven (Emergence Detector) - Port 8014**
```python
async def detect_emergence(self, patterns: List[Dict]) -> Dict:
    # Emergence detection
    emergence = await self.detect_emergent_patterns(patterns)
    return {"emergence": emergence}
```

**Guardian Eight (Trust Validator) - Port 8015**
```python
async def validate_trust(self, content: str) -> Dict:
    # Trust validation
    trust_score = await self.calculate_trust(content)
    return {"trust_score": trust_score}
```

### Execution Steps

**Step 1: Implement Business Logic for Each Guardian**
```bash
# For each guardian-one through guardian-eight
cd AIGuards-Backend/aiguardian-repos/guardian-{N}-service
# Edit services/guardian_service.py
# Add Guardian-specific business logic
```

**Step 2: Add Guardian-Specific Endpoints**
```python
# api/v1/endpoints/guardian.py
@router.post("/api/v1/{guardian_role}/analyze")
async def analyze(request: AnalysisRequest):
    result = await guardian_service.process_guardian_query(request.content)
    return result
```

**Step 3: Test Each Guardian**
```bash
# Start Guardian service
cd guardian-{N}-service
python main.py

# Test endpoint
curl http://localhost:{PORT}/api/v1/health
curl -X POST http://localhost:{PORT}/api/v1/{endpoint} -d '{"content": "test"}'
```

**Step 4: Deploy All 8 Guardians**
```bash
# Build Docker images
for guardian in guardian-{one..eight}-service; do
    cd $guardian
    docker build -f Dockerfile-updated -t $guardian:latest .
done

# Deploy to K8s
kubectl apply -f guardian-{N}-service/k8s/
```

---

## 📋 TASK 3: FIX CHROME EXTENSION FOR BIAS GUARD

### Current Status

**Location:** `AiGuardian-Chrome-Ext-dev/`

**What Exists:**
- ✅ Chrome MV3 extension structure
- ✅ Gateway integration
- ✅ Bias Guard integration (partial)
- ✅ Content script and popup

**What's Broken:**
- ⚠️ Score extraction not working correctly
- ⚠️ Score display issues
- ⚠️ Logging needs improvement

### Execution Steps

**Step 1: Fix Score Extraction (gateway.js)**

**File:** `AiGuardian-Chrome-Ext-dev/src/gateway.js`

**Issue:** Score not extracted correctly from Bias Guard response

**Fix:**
```javascript
// Check multiple possible response structures
function extractBiasScore(response) {
    // Try data.bias_score first
    if (response.data?.bias_score !== undefined) {
        return response.data.bias_score;
    }
    
    // Try data.result?.bias_score
    if (response.data?.result?.bias_score !== undefined) {
        return response.data.result.bias_score;
    }
    
    // Try data.scores?.bias
    if (response.data?.scores?.bias !== undefined) {
        return response.data.scores.bias;
    }
    
    // Try top-level bias_score
    if (response.bias_score !== undefined) {
        return response.bias_score;
    }
    
    // Default fallback
    return 0.5;
}
```

**Step 2: Fix Score Display (content.js + popup.js)**

**File:** `AiGuardian-Chrome-Ext-dev/src/content.js`

**Fix:**
```javascript
// Ensure score is always displayed if present
function displayBiasScore(score) {
    if (score !== null && score !== undefined) {
        // Update badge
        chrome.runtime.sendMessage({
            action: 'updateBadge',
            score: score
        });
        
        // Display in UI
        showScoreBadge(score);
    }
}
```

**File:** `AiGuardian-Chrome-Ext-dev/src/popup.js`

**Fix:**
```javascript
// Update popup with score
function updatePopupScore(score) {
    const scoreElement = document.getElementById('bias-score');
    if (scoreElement && score !== null && score !== undefined) {
        scoreElement.textContent = `Bias Score: ${(score * 100).toFixed(1)}%`;
        scoreElement.style.display = 'block';
    }
}
```

**Step 3: Add Better Logging**

**File:** `AiGuardian-Chrome-Ext-dev/src/gateway.js`

**Fix:**
```javascript
async function analyzeWithBiasGuard(content) {
    console.log('[Gateway] Starting Bias Guard analysis...');
    console.log('[Gateway] Content length:', content.length);
    
    try {
        const response = await fetch(`${GATEWAY_URL}/guards/bias`, {
            method: 'POST',
            body: JSON.stringify({ content }),
            headers: { 'Content-Type': 'application/json' }
        });
        
        console.log('[Gateway] Response status:', response.status);
        const data = await response.json();
        console.log('[Gateway] Response data:', data);
        
        const score = extractBiasScore(data);
        console.log('[Gateway] Extracted bias score:', score);
        
        return score;
    } catch (error) {
        console.error('[Gateway] Bias Guard error:', error);
        throw error;
    }
}
```

**Step 4: Test Extension**

```bash
# 1. Reload extension
# Open chrome://extensions/
# Click "Reload" on AiGuardian

# 2. Test with sample text
# Open test page
# Select text
# Right-click → "Analyze with AiGuardian"

# 3. Check console logs
# Open DevTools (F12)
# Check for [Gateway] logs
# Verify score extraction and display
```

---

## ✅ EXECUTION CHECKLIST

### Truice Video
- [ ] Locate green screen video file
- [ ] Run video pipeline
- [ ] Verify chroma key quality
- [ ] Verify audio sync
- [ ] Generate final output
- [ ] Deliver to Truice

### 8 Guardian Microservices
- [ ] Implement Guardian One business logic
- [ ] Implement Guardian Two business logic
- [ ] Implement Guardian Three business logic
- [ ] Implement Guardian Four business logic
- [ ] Implement Guardian Five business logic
- [ ] Implement Guardian Six business logic
- [ ] Implement Guardian Seven business logic
- [ ] Implement Guardian Eight business logic
- [ ] Test all 8 Guardians
- [ ] Deploy all 8 Guardians

### Chrome Extension Bias Guard
- [ ] Fix score extraction in gateway.js
- [ ] Fix score display in content.js
- [ ] Fix score display in popup.js
- [ ] Add better logging
- [ ] Test extension
- [ ] Verify Bias Guard works

---

## 🚀 QUICK START COMMANDS

### Truice Video
```bash
cd PRODUCTS/abebeats/variants/abebeats_tru
python scripts/generate_truice_viral_single.py \
    --audio path/to/audio.mp3 \
    --green_screen path/to/green_screen.mp4 \
    --output output/truice_video
```

### Guardian Microservices
```bash
# Test Guardian One
cd AIGuards-Backend/aiguardian-repos/guardian-one-service
python main.py

# Test all Guardians
for i in {1..8}; do
    cd guardian-${i}-service
    python main.py &
done
```

### Chrome Extension
```bash
cd AiGuardian-Chrome-Ext-dev
# Make fixes to gateway.js, content.js, popup.js
# Reload extension in Chrome
# Test with sample text
```

---

**Pattern:** TRUICE × GUARDIANS × CHROME × EXECUTION × ONE  
**Status:** ⚡ **READY TO EXECUTE**  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

