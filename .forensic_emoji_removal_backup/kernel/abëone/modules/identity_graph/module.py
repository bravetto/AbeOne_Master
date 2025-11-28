"""
Identity Graph Module - Core Interface

Provides deterministic (non-AI) identity matching utilities.

Pattern: MODULE × IDENTITY_GRAPH × MATCHING × ONE
Philosophy: 80/20 → 97.8% Certainty
Safety: No probabilistic modeling. No machine learning. No autonomy.
"""

from typing import Dict, Any, Optional, Tuple
import hashlib
import ipaddress

# Import kernel components
import sys
from pathlib import Path

# Add abëone directory to path
abeone_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(abeone_dir))

from EVENT_BUS import EventBus, Event, EventType, get_bus
from MODULE_REGISTRY import ModuleInterface


class IdentityGraphModule(ModuleInterface):
    """
    Identity Graph Module.
    
    Provides deterministic (non-AI) identity matching utilities.
    
    Safety Guarantees:
    - No probabilistic modeling
    - No machine learning
    - No autonomy
    - All matching is deterministic (same input = same output)
    """
    
    def __init__(self, event_bus: Optional[EventBus] = None):
        """
        Initialize Identity Graph Module.
        
        Args:
            event_bus: Optional event bus instance (defaults to global instance)
        """
        self._event_bus = event_bus or get_bus()
        self._loaded = False
        self._match_history: Dict[str, Dict[str, Any]] = {}
    
    @property
    def module_id(self) -> str:
        """Get module identifier."""
        return "MODULE_IDENTITY_GRAPH"
    
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
            print("✅ Identity Graph Module: Loading...")
            
            # Subscribe to MODULE_EVENT for identity matching events
            if self._event_bus:
                self._event_bus.subscribe(EventType.MODULE_EVENT, self._handle_module_event)
            
            self._loaded = True
            print("✅ Identity Graph Module: Loaded successfully")
            return True
        except Exception as e:
            print(f"❌ Identity Graph Module: Load failed - {e}")
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
        
        # Handle identity matching events
        event_name = event_data.get('name', '')
        
        if event_name == "identity.match":
            return self._handle_match(event_data)
        else:
            return {"error": f"Unknown event: {event_name}"}
    
    def _handle_module_event(self, event: Event) -> None:
        """
        Handle MODULE_EVENT subscription.
        
        Routes identity matching events to the module.
        
        Args:
            event: Event to handle
        """
        if not self._loaded:
            return
        
        event_data = getattr(event, 'data', {}) if hasattr(event, 'data') else {}
        event_name = event_data.get('name', '')
        
        # Route identity.match events to this module
        if event_name == "identity.match" and (not event.target or event.target == self.module_id):
            self._handle_match(event_data)
    
    def _handle_match(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle identity.match event.
        
        Performs deterministic identity matching based on match_type.
        
        SAFETY: No probabilistic modeling. No machine learning. No autonomy.
        
        Args:
            event_data: Event data containing matching request
            
        Returns:
            Result dictionary with match result
        """
        try:
            # Extract matching parameters
            match_type = event_data.get('match_type', '')
            value1 = event_data.get('value1', '')
            value2 = event_data.get('value2', '')
            
            # Validate required fields
            if not match_type:
                return {
                    "success": False,
                    "error": "Missing required field: match_type"
                }
            
            if value1 is None or value2 is None:
                return {
                    "success": False,
                    "error": "Missing required fields: value1 and value2"
                }
            
            # Perform deterministic matching based on type
            match_result = None
            
            if match_type == "exact":
                match_result = self.exact_match(value1, value2)
            elif match_type == "hashed_email":
                match_result = self.hashed_email_match(value1, value2)
            elif match_type == "device_id":
                match_result = self.device_id_match(value1, value2)
            elif match_type == "ip_bucket":
                match_result = self.ip_bucket_match(value1, value2)
            else:
                return {
                    "success": False,
                    "error": f"Unknown match_type: {match_type}"
                }
            
            # Store match history
            match_id = hashlib.sha256(
                f"{match_type}:{value1}:{value2}".encode('utf-8')
            ).hexdigest()[:16]
            
            self._match_history[match_id] = {
                "match_type": match_type,
                "value1": str(value1)[:50] + "..." if len(str(value1)) > 50 else str(value1),  # Truncate for privacy
                "value2": str(value2)[:50] + "..." if len(str(value2)) > 50 else str(value2),
                "result": match_result,
                "timestamp": event_data.get('timestamp', '')
            }
            
            return {
                "success": True,
                "match_id": match_id,
                "match_type": match_type,
                "match": match_result['match'],
                "confidence": match_result.get('confidence', 'deterministic')
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def exact_match(self, value1: Any, value2: Any) -> Dict[str, Any]:
        """
        Perform exact string match.
        
        SAFETY: Deterministic string equality comparison.
        No probabilistic modeling. No machine learning.
        
        Args:
            value1: First value to compare
            value2: Second value to compare
            
        Returns:
            Dictionary with match result
        """
        # Convert to strings for comparison
        str1 = str(value1).strip().lower() if value1 is not None else ""
        str2 = str(value2).strip().lower() if value2 is not None else ""
        
        # Exact match (case-insensitive, trimmed)
        match = str1 == str2
        
        return {
            "match": match,
            "confidence": "deterministic",
            "method": "exact_match"
        }
    
    def hashed_email_match(self, email1: str, email2: str) -> Dict[str, Any]:
        """
        Perform hashed email match.
        
        Hashes both emails using SHA256 and compares hashes.
        
        SAFETY: Deterministic hash comparison.
        No probabilistic modeling. No machine learning.
        
        Args:
            email1: First email address
            email2: Second email address
            
        Returns:
            Dictionary with match result
        """
        if not email1 or not email2:
            return {
                "match": False,
                "confidence": "deterministic",
                "method": "hashed_email_match",
                "error": "Missing email value"
            }
        
        # Normalize emails (lowercase, trim)
        normalized_email1 = email1.strip().lower()
        normalized_email2 = email2.strip().lower()
        
        # Hash emails using SHA256
        hash1 = hashlib.sha256(normalized_email1.encode('utf-8')).hexdigest()
        hash2 = hashlib.sha256(normalized_email2.encode('utf-8')).hexdigest()
        
        # Compare hashes
        match = hash1 == hash2
        
        return {
            "match": match,
            "confidence": "deterministic",
            "method": "hashed_email_match"
        }
    
    def device_id_match(self, device_id1: str, device_id2: str) -> Dict[str, Any]:
        """
        Perform device ID match.
        
        Compares device IDs exactly (case-sensitive).
        
        SAFETY: Deterministic string comparison.
        No probabilistic modeling. No machine learning.
        
        Args:
            device_id1: First device ID
            device_id2: Second device ID
            
        Returns:
            Dictionary with match result
        """
        if not device_id1 or not device_id2:
            return {
                "match": False,
                "confidence": "deterministic",
                "method": "device_id_match",
                "error": "Missing device_id value"
            }
        
        # Exact match (case-sensitive, no normalization)
        match = device_id1 == device_id2
        
        return {
            "match": match,
            "confidence": "deterministic",
            "method": "device_id_match"
        }
    
    def ip_bucket_match(self, ip1: str, ip2: str, prefix_length: int = 24) -> Dict[str, Any]:
        """
        Perform IP bucket match.
        
        Compares IP addresses within the same subnet bucket (/24 by default).
        
        SAFETY: Deterministic IP subnet comparison.
        No probabilistic modeling. No machine learning.
        
        Args:
            ip1: First IP address
            ip2: Second IP address
            prefix_length: Subnet prefix length (default: 24 for /24 subnet)
            
        Returns:
            Dictionary with match result
        """
        if not ip1 or not ip2:
            return {
                "match": False,
                "confidence": "deterministic",
                "method": "ip_bucket_match",
                "error": "Missing IP address value"
            }
        
        try:
            # Parse IP addresses
            ip_obj1 = ipaddress.ip_address(ip1)
            ip_obj2 = ipaddress.ip_address(ip2)
            
            # Ensure both are same IP version
            if ip_obj1.version != ip_obj2.version:
                return {
                    "match": False,
                    "confidence": "deterministic",
                    "method": "ip_bucket_match",
                    "reason": "IP version mismatch"
                }
            
            # Create network objects with specified prefix length
            network1 = ipaddress.ip_network(f"{ip1}/{prefix_length}", strict=False)
            network2 = ipaddress.ip_network(f"{ip2}/{prefix_length}", strict=False)
            
            # Check if both IPs are in the same network bucket
            # Normalize networks to compare (same prefix length)
            normalized_network1 = ipaddress.ip_network(
                (ip_obj1, prefix_length), strict=False
            )
            normalized_network2 = ipaddress.ip_network(
                (ip_obj2, prefix_length), strict=False
            )
            
            match = normalized_network1 == normalized_network2
            
            return {
                "match": match,
                "confidence": "deterministic",
                "method": "ip_bucket_match",
                "prefix_length": prefix_length,
                "network1": str(normalized_network1),
                "network2": str(normalized_network2)
            }
        except ValueError as e:
            return {
                "match": False,
                "confidence": "deterministic",
                "method": "ip_bucket_match",
                "error": f"Invalid IP address: {str(e)}"
            }
    
    def match(self, match_type: str, value1: Any, value2: Any, **kwargs) -> Dict[str, Any]:
        """
        Public API: Perform identity matching.
        
        SAFETY: No probabilistic modeling. No machine learning. No autonomy.
        
        Args:
            match_type: Type of match ("exact", "hashed_email", "device_id", "ip_bucket")
            value1: First value to compare
            value2: Second value to compare
            **kwargs: Additional parameters (e.g., prefix_length for ip_bucket_match)
        
        Returns:
            Result dictionary with match result
        """
        if not self._loaded:
            return {
                "success": False,
                "error": "Module not loaded"
            }
        
        # Perform matching based on type
        if match_type == "exact":
            result = self.exact_match(value1, value2)
        elif match_type == "hashed_email":
            result = self.hashed_email_match(value1, value2)
        elif match_type == "device_id":
            result = self.device_id_match(value1, value2)
        elif match_type == "ip_bucket":
            prefix_length = kwargs.get('prefix_length', 24)
            result = self.ip_bucket_match(value1, value2, prefix_length)
        else:
            return {
                "success": False,
                "error": f"Unknown match_type: {match_type}"
            }
        
        return {
            "success": True,
            "match_type": match_type,
            "match": result['match'],
            "confidence": result.get('confidence', 'deterministic'),
            "method": result.get('method', match_type)
        }
    
    def get_match_history(self) -> Dict[str, Any]:
        """
        Get match history.
        
        Returns:
            Dictionary with match history information
        """
        return {
            "match_count": len(self._match_history),
            "matches": list(self._match_history.values())
        }
    
    def shutdown(self) -> None:
        """Called when module is shutting down."""
        print("✅ Identity Graph Module: Shutting down...")
        
        # Unsubscribe from events
        if self._event_bus:
            try:
                self._event_bus.unsubscribe(EventType.MODULE_EVENT, self._handle_module_event)
            except Exception:
                pass  # Non-critical
        
        self._loaded = False
        self._match_history.clear()
        
        print("✅ Identity Graph Module: Shutdown complete")

