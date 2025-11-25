"""
SEO Module - Core Interface

Provides SEO payloads, validation logic, and safe transformation helpers.

Pattern: MODULE × SEO × VALIDATION × ONE
Philosophy: 80/20 → 97.8% Certainty
Safety: No autonomous crawling. All operations user-triggered.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid
import re
from urllib.parse import urlparse

# Import kernel components
import sys
from pathlib import Path

# Add abëone directory to path
abeone_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(abeone_dir))

from EVENT_BUS import EventBus, Event, EventType, get_bus
from MODULE_REGISTRY import ModuleInterface


class SeoModule(ModuleInterface):
    """
    SEO Module.
    
    Provides SEO payloads, validation logic, and safe transformation helpers.
    
    Safety Guarantees:
    - No autonomous crawling
    - All operations user-triggered
    - Schema validation only
    """
    
    def __init__(self, event_bus: Optional[EventBus] = None):
        """
        Initialize SEO Module.
        
        Args:
            event_bus: Optional event bus instance (defaults to global instance)
        """
        self._event_bus = event_bus or get_bus()
        self._loaded = False
        self._validated_requests: Dict[str, Dict[str, Any]] = {}
        self._max_depth = 3  # Safety limit
    
    @property
    def module_id(self) -> str:
        """Get module identifier."""
        return "MODULE_SEO"
    
    @property
    def version(self) -> str:
        """Get module version."""
        return "1.0.0"
    
    def on_load(self) -> bool:
        """
        Called when module is loaded.
        
        Sets up event subscriptions and initializes the module.
        
        Returns:
            True if load successful
        """
        try:
            print(" SEO Module: Loading...")
            
            # Subscribe to MODULE_EVENT for SEO events
            if self._event_bus:
                self._event_bus.subscribe(EventType.MODULE_EVENT, self._handle_module_event)
            
            self._loaded = True
            print(" SEO Module: Loaded successfully")
            return True
        except Exception as e:
            print(f" SEO Module: Load failed - {e}")
            return False
    
    def on_event(self, event: Any) -> Any:
        """
        Called when module receives an event.
        
        Args:
            event: Event to handle
            
        Returns:
            Event handling result
        """
        if not self._loaded:
            return {"error": "Module not loaded"}
        
        # Extract event data
        event_data = getattr(event, 'data', {}) if hasattr(event, 'data') else {}
        if isinstance(event, dict):
            event_data = event
        
        # Handle SEO events
        event_name = event_data.get('name', '')
        
        if event_name == "seo.audit_request":
            return self._handle_audit_request(event_data)
        elif event_name == "seo.page_analysis":
            return self._handle_page_analysis(event_data)
        elif event_name == "seo.keyword_request":
            return self._handle_keyword_request(event_data)
        else:
            return {"error": f"Unknown event: {event_name}"}
    
    def _handle_module_event(self, event: Event) -> None:
        """
        Handle MODULE_EVENT subscription.
        
        Routes SEO events to the module.
        
        Args:
            event: Event to handle
        """
        if not self._loaded:
            return
        
        event_data = getattr(event, 'data', {}) if hasattr(event, 'data') else {}
        event_name = event_data.get('name', '')
        
        # Route SEO events to this module
        seo_events = ["seo.audit_request", "seo.page_analysis", "seo.keyword_request"]
        if event_name in seo_events and (not event.target or event.target == self.module_id):
            self.on_event(event)
    
    def _handle_audit_request(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle seo.audit_request event.
        
        Validates the audit request payload and publishes seo_audit_validated event.
        
        Args:
            event_data: Event data containing audit request payload
            
        Returns:
            Result dictionary with validation status
        """
        try:
            # Extract payload
            payload = event_data.get('payload', event_data)
            
            # Validate payload schema
            validation_result = self._validate_audit_payload(payload)
            if not validation_result['valid']:
                return {
                    "success": False,
                    "error": validation_result['error']
                }
            
            # Generate request ID
            request_id = str(uuid.uuid4())
            
            # Create validated request
            validated_request = {
                "request_id": request_id,
                "payload": payload,
                "validated_at": datetime.now().isoformat(),
                "validated": True,
                "protocol": "seo.audit_request"
            }
            
            # Store validated request
            self._validated_requests[request_id] = validated_request
            
            # Publish MODULE_EVENT.seo_audit_validated (user-triggered)
            self._publish_seo_audit_validated(validated_request)
            
            return {
                "success": True,
                "request_id": request_id,
                "status": "validated",
                "message": "SEO audit request validated and published"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _handle_page_analysis(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle seo.page_analysis event.
        
        Validates the page analysis payload and publishes seo_page_analysis_validated event.
        
        Args:
            event_data: Event data containing page analysis payload
            
        Returns:
            Result dictionary with validation status
        """
        try:
            # Extract payload
            payload = event_data.get('payload', event_data)
            
            # Validate payload schema
            validation_result = self._validate_page_analysis_payload(payload)
            if not validation_result['valid']:
                return {
                    "success": False,
                    "error": validation_result['error']
                }
            
            # Generate request ID
            request_id = str(uuid.uuid4())
            
            # Create validated request
            validated_request = {
                "request_id": request_id,
                "payload": payload,
                "validated_at": datetime.now().isoformat(),
                "validated": True,
                "protocol": "seo.page_analysis"
            }
            
            # Store validated request
            self._validated_requests[request_id] = validated_request
            
            # Publish MODULE_EVENT.seo_page_analysis_validated (user-triggered)
            self._publish_seo_page_analysis_validated(validated_request)
            
            return {
                "success": True,
                "request_id": request_id,
                "status": "validated",
                "message": "SEO page analysis request validated and published"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _handle_keyword_request(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle seo.keyword_request event.
        
        Validates the keyword request payload and publishes seo_keyword_validated event.
        
        Args:
            event_data: Event data containing keyword request payload
            
        Returns:
            Result dictionary with validation status
        """
        try:
            # Extract payload
            payload = event_data.get('payload', event_data)
            
            # Validate payload schema
            validation_result = self._validate_keyword_payload(payload)
            if not validation_result['valid']:
                return {
                    "success": False,
                    "error": validation_result['error']
                }
            
            # Generate request ID
            request_id = str(uuid.uuid4())
            
            # Create validated request
            validated_request = {
                "request_id": request_id,
                "payload": payload,
                "validated_at": datetime.now().isoformat(),
                "validated": True,
                "protocol": "seo.keyword_request"
            }
            
            # Store validated request
            self._validated_requests[request_id] = validated_request
            
            # Publish MODULE_EVENT.seo_keyword_validated (user-triggered)
            self._publish_seo_keyword_validated(validated_request)
            
            return {
                "success": True,
                "request_id": request_id,
                "status": "validated",
                "message": "SEO keyword request validated and published"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _validate_audit_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate SEO audit request payload schema.
        
        Required fields:
        - url: str
        - depth: int (max 3 for safety)
        
        Optional fields:
        - competitor_urls: list[str]
        
        Args:
            payload: Payload to validate
            
        Returns:
            Validation result dictionary
        """
        # Validate url: str (required)
        url = payload.get('url')
        if not url:
            return {
                "valid": False,
                "error": "Missing required field: url"
            }
        if not isinstance(url, str):
            return {
                "valid": False,
                "error": "url must be a string"
            }
        
        # Validate URL format
        if not self._is_valid_url(url):
            return {
                "valid": False,
                "error": "url must be a valid URL"
            }
        
        # Validate depth: int (required, max 3)
        depth = payload.get('depth')
        if depth is None:
            return {
                "valid": False,
                "error": "Missing required field: depth"
            }
        if not isinstance(depth, int):
            return {
                "valid": False,
                "error": "depth must be an integer"
            }
        if depth < 0 or depth > self._max_depth:
            return {
                "valid": False,
                "error": f"depth must be between 0 and {self._max_depth} (safety limit)"
            }
        
        # Validate competitor_urls: list[str] (optional)
        competitor_urls = payload.get('competitor_urls')
        if competitor_urls is not None:
            if not isinstance(competitor_urls, list):
                return {
                    "valid": False,
                    "error": "competitor_urls must be a list"
                }
            for competitor_url in competitor_urls:
                if not isinstance(competitor_url, str):
                    return {
                        "valid": False,
                        "error": "All competitor_urls must be strings"
                    }
                if not self._is_valid_url(competitor_url):
                    return {
                        "valid": False,
                        "error": f"Invalid competitor URL: {competitor_url}"
                    }
        
        return {"valid": True}
    
    def _validate_page_analysis_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate SEO page analysis payload schema.
        
        Required fields:
        - url: str
        
        Args:
            payload: Payload to validate
            
        Returns:
            Validation result dictionary
        """
        # Validate url: str (required)
        url = payload.get('url')
        if not url:
            return {
                "valid": False,
                "error": "Missing required field: url"
            }
        if not isinstance(url, str):
            return {
                "valid": False,
                "error": "url must be a string"
            }
        
        # Validate URL format
        if not self._is_valid_url(url):
            return {
                "valid": False,
                "error": "url must be a valid URL"
            }
        
        return {"valid": True}
    
    def _validate_keyword_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate SEO keyword request payload schema.
        
        Required fields:
        - keyword: str
        
        Optional fields:
        - url: str
        - competitor_urls: list[str]
        
        Args:
            payload: Payload to validate
            
        Returns:
            Validation result dictionary
        """
        # Validate keyword: str (required)
        keyword = payload.get('keyword')
        if not keyword:
            return {
                "valid": False,
                "error": "Missing required field: keyword"
            }
        if not isinstance(keyword, str):
            return {
                "valid": False,
                "error": "keyword must be a string"
            }
        if len(keyword.strip()) == 0:
            return {
                "valid": False,
                "error": "keyword cannot be empty"
            }
        
        # Validate url: str (optional)
        url = payload.get('url')
        if url is not None:
            if not isinstance(url, str):
                return {
                    "valid": False,
                    "error": "url must be a string"
                }
            if not self._is_valid_url(url):
                return {
                    "valid": False,
                    "error": "url must be a valid URL"
                }
        
        # Validate competitor_urls: list[str] (optional)
        competitor_urls = payload.get('competitor_urls')
        if competitor_urls is not None:
            if not isinstance(competitor_urls, list):
                return {
                    "valid": False,
                    "error": "competitor_urls must be a list"
                }
            for competitor_url in competitor_urls:
                if not isinstance(competitor_url, str):
                    return {
                        "valid": False,
                        "error": "All competitor_urls must be strings"
                    }
                if not self._is_valid_url(competitor_url):
                    return {
                        "valid": False,
                        "error": f"Invalid competitor URL: {competitor_url}"
                    }
        
        return {"valid": True}
    
    def _is_valid_url(self, url: str) -> bool:
        """
        Validate URL format.
        
        Args:
            url: URL string to validate
            
        Returns:
            True if URL is valid
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    def _publish_seo_audit_validated(self, validated_request: Dict[str, Any]) -> None:
        """
        Publish MODULE_EVENT.seo_audit_validated (user-triggered).
        
        Args:
            validated_request: Validated request dictionary
        """
        if not self._event_bus:
            return
        
        try:
            event = self._event_bus.create_event(
                event_type=EventType.MODULE_EVENT,
                source=self.module_id,
                target=None,  # Broadcast to MODULE_EVENT subscribers
                data={
                    "name": "seo_audit_validated",
                    "request_id": validated_request['request_id'],
                    "payload": validated_request['payload'],
                    "validated_at": validated_request['validated_at']
                }
            )
            
            self._event_bus.publish(event)
        except Exception as e:
            print(f"  SEO Module: Failed to publish seo_audit_validated event: {e}")
    
    def _publish_seo_page_analysis_validated(self, validated_request: Dict[str, Any]) -> None:
        """
        Publish MODULE_EVENT.seo_page_analysis_validated (user-triggered).
        
        Args:
            validated_request: Validated request dictionary
        """
        if not self._event_bus:
            return
        
        try:
            event = self._event_bus.create_event(
                event_type=EventType.MODULE_EVENT,
                source=self.module_id,
                target=None,  # Broadcast to MODULE_EVENT subscribers
                data={
                    "name": "seo_page_analysis_validated",
                    "request_id": validated_request['request_id'],
                    "payload": validated_request['payload'],
                    "validated_at": validated_request['validated_at']
                }
            )
            
            self._event_bus.publish(event)
        except Exception as e:
            print(f"  SEO Module: Failed to publish seo_page_analysis_validated event: {e}")
    
    def _publish_seo_keyword_validated(self, validated_request: Dict[str, Any]) -> None:
        """
        Publish MODULE_EVENT.seo_keyword_validated (user-triggered).
        
        Args:
            validated_request: Validated request dictionary
        """
        if not self._event_bus:
            return
        
        try:
            event = self._event_bus.create_event(
                event_type=EventType.MODULE_EVENT,
                source=self.module_id,
                target=None,  # Broadcast to MODULE_EVENT subscribers
                data={
                    "name": "seo_keyword_validated",
                    "request_id": validated_request['request_id'],
                    "payload": validated_request['payload'],
                    "validated_at": validated_request['validated_at']
                }
            )
            
            self._event_bus.publish(event)
        except Exception as e:
            print(f"  SEO Module: Failed to publish seo_keyword_validated event: {e}")
    
    def audit_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Public API: Request an SEO audit.
        
        Validates the payload schema and publishes seo_audit_validated event.
        
        Args:
            payload: SEO audit request payload containing:
                - url: str (required)
                - depth: int (required, max 3 for safety)
                - competitor_urls: list[str] (optional)
        
        Returns:
            Result dictionary with request_id and status
        """
        if not self._loaded:
            return {
                "success": False,
                "error": "Module not loaded"
            }
        
        # Create audit_request event data
        event_data = {
            "name": "seo.audit_request",
            "payload": payload
        }
        
        # Handle the request
        return self._handle_audit_request(event_data)
    
    def page_analysis(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Public API: Request a page analysis.
        
        Validates the payload schema and publishes seo_page_analysis_validated event.
        
        Args:
            payload: SEO page analysis payload containing:
                - url: str (required)
        
        Returns:
            Result dictionary with request_id and status
        """
        if not self._loaded:
            return {
                "success": False,
                "error": "Module not loaded"
            }
        
        # Create page_analysis event data
        event_data = {
            "name": "seo.page_analysis",
            "payload": payload
        }
        
        # Handle the request
        return self._handle_page_analysis(event_data)
    
    def keyword_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Public API: Request keyword analysis.
        
        Validates the payload schema and publishes seo_keyword_validated event.
        
        Args:
            payload: SEO keyword request payload containing:
                - keyword: str (required)
                - url: str (optional)
                - competitor_urls: list[str] (optional)
        
        Returns:
            Result dictionary with request_id and status
        """
        if not self._loaded:
            return {
                "success": False,
                "error": "Module not loaded"
            }
        
        # Create keyword_request event data
        event_data = {
            "name": "seo.keyword_request",
            "payload": payload
        }
        
        # Handle the request
        return self._handle_keyword_request(event_data)
    
    def get_validated_count(self) -> int:
        """
        Get count of validated requests.
        
        Returns:
            Number of validated requests
        """
        return len(self._validated_requests)
    
    def shutdown(self) -> None:
        """Called when module is shutting down."""
        print(" SEO Module: Shutting down...")
        
        # Unsubscribe from events
        if self._event_bus:
            try:
                self._event_bus.unsubscribe(EventType.MODULE_EVENT, self._handle_module_event)
            except Exception:
                pass  # Non-critical
        
        self._loaded = False
        self._validated_requests.clear()
        
        print(" SEO Module: Shutdown complete")

