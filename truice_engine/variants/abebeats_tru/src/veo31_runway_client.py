"""
Veo 3.1 Runway API Client
Direct API Integration for Veo 3.1 Video Generation

Pattern: API × CLIENT × ORCHESTRATION × ONE
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
import logging
import httpx
import asyncio

logger = logging.getLogger(__name__)


@dataclass
class RunwayAPIResponse:
    """Runway API response wrapper"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    request_id: Optional[str] = None
    credits_used: Optional[int] = None


class RunwayAPIClient:
    """
    Runway API Client for Veo 3.1
    
    Provides direct API integration for:
    - Text-to-Video generation
    - Image-to-Video generation
    - Workflow execution
    - Status polling
    """
    
    BASE_URL = "https://api.runwayml.com/v1"
    
    def __init__(
        self,
        api_key: str,
        timeout: float = 300.0,
        max_retries: int = 3
    ):
        """
        Initialize Runway API Client.
        
        Args:
            api_key: Runway API key
            timeout: Request timeout in seconds
            max_retries: Maximum retry attempts
        """
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.client: Optional[httpx.AsyncClient] = None
        self.logger = logging.getLogger(f"{__name__}.RunwayAPIClient")
    
    async def initialize(self) -> bool:
        """Initialize HTTP client"""
        if self.client:
            return True
        
        try:
            self.client = httpx.AsyncClient(
                timeout=httpx.Timeout(self.timeout),
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
            )
            self.logger.info(" Runway API Client initialized")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize Runway API Client: {e}")
            return False
    
    async def close(self) -> None:
        """Close HTTP client"""
        if self.client:
            await self.client.aclose()
            self.client = None
    
    async def text_to_video(
        self,
        prompt_text: str,
        model: str = "veo3.1",
        ratio: str = "1920:1080",
        duration: int = 5
    ) -> RunwayAPIResponse:
        """
        Generate video from text prompt.
        
        Args:
            prompt_text: Text prompt (max 1000 chars)
            model: Model name (veo3, veo3.1, veo3.1_fast)
            ratio: Video ratio (e.g., "1920:1080")
            duration: Duration in seconds (2-10)
        
        Returns:
            RunwayAPIResponse
        """
        if not self.client:
            await self.initialize()
        
        payload = {
            "model": model,
            "promptText": prompt_text[:1000],  # Enforce limit
            "ratio": ratio,
            "duration": duration
        }
        
        return await self._make_request("POST", "/text_to_video", payload)
    
    async def image_to_video(
        self,
        prompt_image: str,  # URL or data URI
        prompt_text: Optional[str] = None,
        model: str = "veo3.1",
        ratio: str = "1920:1080",
        duration: int = 5,
        seed: Optional[int] = None
    ) -> RunwayAPIResponse:
        """
        Generate video from image.
        
        Args:
            prompt_image: Image URL or data URI
            prompt_text: Optional text prompt
            model: Model name
            ratio: Video ratio
            duration: Duration in seconds (2-10)
            seed: Optional seed for reproducibility
        
        Returns:
            RunwayAPIResponse
        """
        if not self.client:
            await self.initialize()
        
        payload = {
            "model": model,
            "promptImage": prompt_image,
            "ratio": ratio,
            "duration": duration
        }
        
        if prompt_text:
            payload["promptText"] = prompt_text[:1000]
        
        if seed is not None:
            payload["seed"] = seed
        
        return await self._make_request("POST", "/image_to_video", payload)
    
    async def execute_workflow(
        self,
        workflow_config: Dict[str, Any]
    ) -> RunwayAPIResponse:
        """
        Execute Runway Workflow.
        
        Args:
            workflow_config: Workflow configuration from Veo31PromptEngine
        
        Returns:
            RunwayAPIResponse
        """
        if not self.client:
            await self.initialize()
        
        return await self._make_request("POST", "/workflows/execute", workflow_config)
    
    async def get_status(
        self,
        request_id: str
    ) -> RunwayAPIResponse:
        """
        Get generation status.
        
        Args:
            request_id: Request ID from generation response
        
        Returns:
            RunwayAPIResponse with status
        """
        if not self.client:
            await self.initialize()
        
        return await self._make_request("GET", f"/generations/{request_id}")
    
    async def poll_until_complete(
        self,
        request_id: str,
        poll_interval: float = 5.0,
        max_wait: float = 600.0
    ) -> RunwayAPIResponse:
        """
        Poll generation status until complete.
        
        Args:
            request_id: Request ID
            poll_interval: Seconds between polls
            max_wait: Maximum wait time in seconds
        
        Returns:
            RunwayAPIResponse with final result
        """
        start_time = datetime.now()
        
        while True:
            elapsed = (datetime.now() - start_time).total_seconds()
            if elapsed > max_wait:
                return RunwayAPIResponse(
                    success=False,
                    error=f"Timeout after {max_wait}s"
                )
            
            response = await self.get_status(request_id)
            
            if not response.success:
                return response
            
            status = response.data.get("status", "unknown")
            
            if status == "completed":
                return response
            elif status == "failed":
                return RunwayAPIResponse(
                    success=False,
                    error=response.data.get("error", "Generation failed")
                )
            
            await asyncio.sleep(poll_interval)
    
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        payload: Optional[Dict[str, Any]] = None
    ) -> RunwayAPIResponse:
        """Make HTTP request with retry logic"""
        url = f"{self.BASE_URL}{endpoint}"
        
        for attempt in range(self.max_retries):
            try:
                if method == "GET":
                    response = await self.client.get(url)
                else:
                    response = await self.client.post(url, json=payload)
                
                response.raise_for_status()
                data = response.json()
                
                return RunwayAPIResponse(
                    success=True,
                    data=data,
                    request_id=data.get("id"),
                    credits_used=data.get("credits_used")
                )
            
            except httpx.HTTPStatusError as e:
                if e.response.status_code < 500 or attempt == self.max_retries - 1:
                    return RunwayAPIResponse(
                        success=False,
                        error=f"HTTP {e.response.status_code}: {e.response.text}"
                    )
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
            
            except Exception as e:
                if attempt == self.max_retries - 1:
                    return RunwayAPIResponse(
                        success=False,
                        error=str(e)
                    )
                await asyncio.sleep(2 ** attempt)
        
        return RunwayAPIResponse(
            success=False,
            error="Max retries exceeded"
        )

