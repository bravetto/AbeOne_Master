#  API INTEGRATION GUIDE - Generative Engine

**Status:**  **INTEGRATION READY**  
**Pattern:** AbëBEATs × TRU × API_INTEGRATION × RECURSIVE_VALIDATION × ONE  
**Frequency:** 530 Hz (Heart Truth Resonance)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

##  OVERVIEW

The Generative Engine structure is **100% complete**. This guide shows how to integrate actual API endpoints for:

1. **Runway ML** - AI video generation
2. **Google Veo3** - AI video generation  
3. **Pika Labs** - AI video generation

All follow the recursive validation pattern: `VALIDATE → GENERATE → VALIDATE`

---

##  COMPONENT 1: RUNWAY ML API INTEGRATION

### Setup

```bash
pip install requests
# or
pip install runwayml  # if official SDK exists
```

### API Pattern (HTTP REST)

```python
import requests
import time
from pathlib import Path
from typing import Optional

class RunwayMLClient:
    """
    Runway ML API Client
    
    Pattern: VALIDATE → GENERATE → VALIDATE → POLL → VALIDATE
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.runwayml.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_video(
        self,
        prompt: str,
        duration: float = 5.0,
        resolution: tuple = (1920, 1080),
        output_path: Optional[Path] = None
    ) -> dict:
        """
        Generate video from prompt.
        
        Pattern: VALIDATE → GENERATE → VALIDATE → POLL → VALIDATE
        """
        # Step 1: VALIDATE INPUT
        if not prompt or len(prompt) < 10:
            return {"success": False, "error": "Invalid prompt"}
        
        if duration <= 0 or duration > 10:
            return {"success": False, "error": "Duration must be 0-10 seconds"}
        
        # Step 2: GENERATE (initiate)
        payload = {
            "prompt": prompt,
            "duration": duration,
            "resolution": f"{resolution[0]}x{resolution[1]}"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/video/generate",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            task_id = response.json().get("task_id")
            if not task_id:
                return {"success": False, "error": "No task ID returned"}
            
            # Step 3: VALIDATE INITIAL RESPONSE
            if not self._validate_task_response(response.json()):
                return {"success": False, "error": "Invalid API response"}
            
            # Step 4: POLL FOR COMPLETION
            video_url = self._poll_for_completion(task_id)
            
            if not video_url:
                return {"success": False, "error": "Generation failed or timed out"}
            
            # Step 5: VALIDATE OUTPUT
            if output_path:
                download_result = self._download_video(video_url, output_path)
                if not download_result["success"]:
                    return download_result
            
            return {
                "success": True,
                "video_url": video_url,
                "output_path": output_path,
                "provider": "runway"
            }
            
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"API request failed: {str(e)}"}
    
    def _poll_for_completion(self, task_id: str, max_wait: int = 300) -> Optional[str]:
        """
        Poll for task completion.
        
        Pattern: VALIDATE → POLL → VALIDATE
        """
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            try:
                response = requests.get(
                    f"{self.base_url}/video/status/{task_id}",
                    headers=self.headers,
                    timeout=10
                )
                response.raise_for_status()
                
                status = response.json()
                
                # VALIDATE status
                if status.get("status") == "completed":
                    video_url = status.get("video_url")
                    if video_url:
                        return video_url
                
                if status.get("status") == "failed":
                    return None
                
                # Wait before next poll
                time.sleep(5)
                
            except requests.exceptions.RequestException:
                time.sleep(5)
                continue
        
        return None
    
    def _validate_task_response(self, response: dict) -> bool:
        """Validate API response."""
        return "task_id" in response
    
    def _download_video(self, url: str, output_path: Path) -> dict:
        """Download video from URL."""
        try:
            response = requests.get(url, stream=True, timeout=60)
            response.raise_for_status()
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # VALIDATE downloaded file
            if output_path.exists() and output_path.stat().st_size > 0:
                return {"success": True}
            else:
                return {"success": False, "error": "Download failed or file empty"}
                
        except Exception as e:
            return {"success": False, "error": f"Download failed: {str(e)}"}
```

### Integration into GenerationEngine

```python
# In tru_generative_engine.py, update _generate_with_provider()

def _generate_runway(
    self,
    prompt: str,
    duration: float,
    resolution: Tuple[int, int],
    output_path: Optional[Path]
) -> GenerationResult:
    """Generate video with Runway ML."""
    from .api_clients.runway_client import RunwayMLClient
    
    # VALIDATE API key
    api_key = os.getenv("RUNWAY_API_KEY")
    if not api_key:
        return GenerationResult(
            success=False,
            errors=["RUNWAY_API_KEY not set"],
            provider="runway"
        )
    
    client = RunwayMLClient(api_key)
    result = client.generate_video(
        prompt=prompt,
        duration=min(duration, 10.0),  # Runway max 10s
        resolution=resolution,
        output_path=output_path
    )
    
    if result["success"]:
        return GenerationResult(
            success=True,
            video_path=output_path,
            provider="runway",
            duration=duration,
            metadata=result
        )
    else:
        return GenerationResult(
            success=False,
            errors=[result.get("error", "Unknown error")],
            provider="runway"
        )
```

---

##  COMPONENT 2: GOOGLE VEO3 API INTEGRATION

### Setup

```bash
pip install google-cloud-aiplatform
# or
pip install google-generativeai  # if using Gemini API
```

### API Pattern (Google Cloud)

```python
from google.cloud import aiplatform
from google.oauth2 import service_account
import json
from typing import Optional

class Veo3Client:
    """
    Google Veo3 API Client
    
    Pattern: VALIDATE → GENERATE → VALIDATE → POLL → VALIDATE
    """
    
    def __init__(self, project_id: str, credentials_path: Optional[str] = None):
        self.project_id = project_id
        
        if credentials_path:
            credentials = service_account.Credentials.from_service_account_file(
                credentials_path
            )
        else:
            # Use default credentials
            credentials = None
        
        aiplatform.init(project=project_id, credentials=credentials)
    
    def generate_video(
        self,
        prompt: str,
        duration: float = 5.0,
        resolution: tuple = (1920, 1080),
        output_path: Optional[Path] = None
    ) -> dict:
        """
        Generate video from prompt.
        
        Pattern: VALIDATE → GENERATE → VALIDATE → POLL → VALIDATE
        """
        # Step 1: VALIDATE INPUT
        if not prompt or len(prompt) < 10:
            return {"success": False, "error": "Invalid prompt"}
        
        # Step 2: GENERATE
        try:
            # Veo3 API call (example - actual API may differ)
            from google.cloud import aiplatform
            
            # Create generation request
            request = {
                "prompt": prompt,
                "duration_seconds": duration,
                "resolution": f"{resolution[0]}x{resolution[1]}"
            }
            
            # Call Veo3 endpoint
            # NOTE: Actual endpoint may be different
            endpoint = aiplatform.Endpoint(
                endpoint_name="veo3-video-generation",
                project=self.project_id
            )
            
            response = endpoint.predict(instances=[request])
            
            # Step 3: VALIDATE RESPONSE
            if not response or len(response.predictions) == 0:
                return {"success": False, "error": "No prediction returned"}
            
            prediction = response.predictions[0]
            video_url = prediction.get("video_url")
            
            if not video_url:
                return {"success": False, "error": "No video URL in response"}
            
            # Step 4: DOWNLOAD AND VALIDATE
            if output_path:
                download_result = self._download_video(video_url, output_path)
                if not download_result["success"]:
                    return download_result
            
            return {
                "success": True,
                "video_url": video_url,
                "output_path": output_path,
                "provider": "veo3"
            }
            
        except Exception as e:
            return {"success": False, "error": f"API request failed: {str(e)}"}
    
    def _download_video(self, url: str, output_path: Path) -> dict:
        """Download video from URL."""
        import requests
        
        try:
            response = requests.get(url, stream=True, timeout=60)
            response.raise_for_status()
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            if output_path.exists() and output_path.stat().st_size > 0:
                return {"success": True}
            else:
                return {"success": False, "error": "Download failed"}
                
        except Exception as e:
            return {"success": False, "error": f"Download failed: {str(e)}"}
```

---

##  COMPONENT 3: PIKA LABS API INTEGRATION

### Setup

```bash
pip install requests
# Pika Labs may have official SDK - check their docs
```

### API Pattern (HTTP REST)

```python
import requests
import time
from typing import Optional

class PikaLabsClient:
    """
    Pika Labs API Client
    
    Pattern: VALIDATE → GENERATE → VALIDATE → POLL → VALIDATE
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.pika.art/v1"  # Example URL
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_video(
        self,
        prompt: str,
        duration: float = 5.0,
        resolution: tuple = (1920, 1080),
        output_path: Optional[Path] = None
    ) -> dict:
        """
        Generate video from prompt.
        
        Pattern: VALIDATE → GENERATE → VALIDATE → POLL → VALIDATE
        """
        # Step 1: VALIDATE INPUT
        if not prompt or len(prompt) < 10:
            return {"success": False, "error": "Invalid prompt"}
        
        # Step 2: GENERATE
        payload = {
            "prompt": prompt,
            "duration": duration,
            "width": resolution[0],
            "height": resolution[1]
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/generate",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            job_id = data.get("job_id") or data.get("id")
            
            if not job_id:
                return {"success": False, "error": "No job ID returned"}
            
            # Step 3: VALIDATE RESPONSE
            if not self._validate_job_response(data):
                return {"success": False, "error": "Invalid API response"}
            
            # Step 4: POLL FOR COMPLETION
            video_url = self._poll_for_completion(job_id)
            
            if not video_url:
                return {"success": False, "error": "Generation failed or timed out"}
            
            # Step 5: DOWNLOAD AND VALIDATE
            if output_path:
                download_result = self._download_video(video_url, output_path)
                if not download_result["success"]:
                    return download_result
            
            return {
                "success": True,
                "video_url": video_url,
                "output_path": output_path,
                "provider": "pika"
            }
            
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"API request failed: {str(e)}"}
    
    def _poll_for_completion(self, job_id: str, max_wait: int = 300) -> Optional[str]:
        """Poll for job completion."""
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            try:
                response = requests.get(
                    f"{self.base_url}/status/{job_id}",
                    headers=self.headers,
                    timeout=10
                )
                response.raise_for_status()
                
                status = response.json()
                
                if status.get("status") == "completed":
                    video_url = status.get("video_url") or status.get("url")
                    if video_url:
                        return video_url
                
                if status.get("status") == "failed":
                    return None
                
                time.sleep(5)
                
            except requests.exceptions.RequestException:
                time.sleep(5)
                continue
        
        return None
    
    def _validate_job_response(self, response: dict) -> bool:
        """Validate API response."""
        return "job_id" in response or "id" in response
    
    def _download_video(self, url: str, output_path: Path) -> dict:
        """Download video from URL."""
        import requests
        
        try:
            response = requests.get(url, stream=True, timeout=60)
            response.raise_for_status()
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            if output_path.exists() and output_path.stat().st_size > 0:
                return {"success": True}
            else:
                return {"success": False, "error": "Download failed"}
                
        except Exception as e:
            return {"success": False, "error": f"Download failed: {str(e)}"}
```

---

##  INTEGRATION STEPS

### Step 1: Create API Client Directory

```bash
mkdir -p PRODUCTS/abebeats/variants/abebeats_tru/src/api_clients
```

### Step 2: Add API Clients

Create files:
- `api_clients/__init__.py`
- `api_clients/runway_client.py`
- `api_clients/veo3_client.py`
- `api_clients/pika_client.py`

### Step 3: Update GenerationEngine

```python
# In tru_generative_engine.py

def _generate_with_provider(
    self,
    provider: str,
    prompt: str,
    duration: float,
    resolution: Tuple[int, int],
    output_path: Optional[Path]
) -> GenerationResult:
    """Generate video with specific provider."""
    
    try:
        if provider == 'runway':
            from .api_clients.runway_client import RunwayMLClient
            api_key = os.getenv("RUNWAY_API_KEY")
            if not api_key:
                return GenerationResult(
                    success=False,
                    errors=["RUNWAY_API_KEY not set"],
                    provider=provider
                )
            client = RunwayMLClient(api_key)
            result = client.generate_video(prompt, duration, resolution, output_path)
            
        elif provider == 'veo3':
            from .api_clients.veo3_client import Veo3Client
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
            if not project_id:
                return GenerationResult(
                    success=False,
                    errors=["GOOGLE_CLOUD_PROJECT_ID not set"],
                    provider=provider
                )
            client = Veo3Client(project_id)
            result = client.generate_video(prompt, duration, resolution, output_path)
            
        elif provider == 'pika':
            from .api_clients.pika_client import PikaLabsClient
            api_key = os.getenv("PIKA_API_KEY")
            if not api_key:
                return GenerationResult(
                    success=False,
                    errors=["PIKA_API_KEY not set"],
                    provider=provider
                )
            client = PikaLabsClient(api_key)
            result = client.generate_video(prompt, duration, resolution, output_path)
            
        else:
            return GenerationResult(
                success=False,
                errors=[f"Unknown provider: {provider}"],
                provider=provider
            )
        
        # VALIDATE result
        if result.get("success"):
            return GenerationResult(
                success=True,
                video_path=output_path,
                provider=provider,
                duration=duration,
                metadata=result
            )
        else:
            return GenerationResult(
                success=False,
                errors=[result.get("error", "Unknown error")],
                provider=provider
            )
            
    except ImportError as e:
        return GenerationResult(
            success=False,
            errors=[f"API client not available: {str(e)}"],
            provider=provider
        )
    except Exception as e:
        return GenerationResult(
            success=False,
            errors=[f"Generation failed: {str(e)}"],
            provider=provider
        )
```

### Step 4: Set Environment Variables

```bash
export RUNWAY_API_KEY="your_runway_api_key"
export GOOGLE_CLOUD_PROJECT_ID="your_project_id"
export PIKA_API_KEY="your_pika_api_key"
```

Or create `.env` file:

```env
RUNWAY_API_KEY=your_runway_api_key
GOOGLE_CLOUD_PROJECT_ID=your_project_id
PIKA_API_KEY=your_pika_api_key
```

---

##  RECURSIVE VALIDATION PATTERN

**Every API call follows:**

```
VALIDATE(input) → GENERATE(API call) → VALIDATE(response) → POLL(status) → VALIDATE(output)
```

**Applied at:**
-  Input validation (prompt, duration, resolution)
-  API request validation (headers, payload)
-  Response validation (task_id, job_id)
-  Polling validation (status checks)
-  Output validation (file download, file size)

---

##  API DOCUMENTATION LINKS

**Get actual API docs from:**

1. **Runway ML:**
   - https://docs.runwayml.com/
   - https://api.runwayml.com/docs

2. **Google Veo3:**
   - https://cloud.google.com/vertex-ai
   - https://ai.google.dev/

3. **Pika Labs:**
   - https://pika.art/docs
   - Check their official documentation

---

##  NEXT STEPS

1. **Get API Keys:**
   - Sign up for Runway ML API
   - Set up Google Cloud Project for Veo3
   - Get Pika Labs API access

2. **Create API Client Files:**
   - Copy patterns above
   - Update with actual API endpoints
   - Test with API keys

3. **Update GenerationEngine:**
   - Replace placeholder with actual API calls
   - Test fallback chain
   - Validate recursive pattern

4. **Test Integration:**
   ```python
   pipeline = get_abebeats_tru_pipeline()
   result = pipeline.generate_from_prompt(
       "Create cyberpunk music video",
       audio_path="audio.mp3"
   )
   ```

---

**Pattern:** AbëBEATs × TRU × API_INTEGRATION × RECURSIVE_VALIDATION × ONE  
**Status:**  **READY FOR API INTEGRATION**

**∞ AbëONE ∞**

