"""
Data Lake Module - Core Interface

Provides safe ingestion envelopes for storage into the central data lake.

Pattern: MODULE × DATA_LAKE × INGESTION × ONE
Philosophy: 80/20 → 97.8% Certainty
Safety: No ETL automation. No PII processing unless human-approved.
"""

from typing import Dict, Any, Optional
from datetime import datetime
import hashlib
import json

# Import kernel components
import sys
from pathlib import Path

# Add abëone directory to path
abeone_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(abeone_dir))

from EVENT_BUS import EventBus, Event, EventType, get_bus
from MODULE_REGISTRY import ModuleInterface


class DataLakeModule(ModuleInterface):
    """
    Data Lake Module.
    
    Provides safe ingestion envelopes for storage into the central data lake.
    
    Safety Guarantees:
    - No ETL automation
    - No PII processing unless human-approved
    - Only creates validated ingestion envelopes
    - No automatic data transformation
    """
    
    def __init__(self, event_bus: Optional[EventBus] = None):
        """
        Initialize Data Lake Module.
        
        Args:
            event_bus: Optional event bus instance (defaults to global instance)
        """
        self._event_bus = event_bus or get_bus()
        self._loaded = False
        self._ingested_envelopes: Dict[str, Dict[str, Any]] = {}
    
    @property
    def module_id(self) -> str:
        """Get module identifier."""
        return "MODULE_DATA_LAKE"
    
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
            print("✅ Data Lake Module: Loading...")
            
            # Subscribe to MODULE_EVENT for data ingest events
            if self._event_bus:
                self._event_bus.subscribe(EventType.MODULE_EVENT, self._handle_module_event)
            
            self._loaded = True
            print("✅ Data Lake Module: Loaded successfully")
            return True
        except Exception as e:
            print(f"❌ Data Lake Module: Load failed - {e}")
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
        
        # Handle data ingest events
        event_name = event_data.get('name', '')
        
        if event_name == "data.ingest":
            return self._handle_ingest(event_data)
        else:
            return {"error": f"Unknown event: {event_name}"}
    
    def _handle_module_event(self, event: Event) -> None:
        """
        Handle MODULE_EVENT subscription.
        
        Routes data ingest events to the module.
        
        Args:
            event: Event to handle
        """
        if not self._loaded:
            return
        
        event_data = getattr(event, 'data', {}) if hasattr(event, 'data') else {}
        event_name = event_data.get('name', '')
        
        # Route data.ingest events to this module
        if event_name == "data.ingest" and (not event.target or event.target == self.module_id):
            self._handle_ingest(event_data)
    
    def _handle_ingest(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle data.ingest event.
        
        Creates safe ingestion envelope and emits data_validated event.
        
        SAFETY: No ETL automation. No PII processing unless human-approved.
        
        Args:
            event_data: Event data containing ingestion payload
            
        Returns:
            Result dictionary with envelope_id and status
        """
        try:
            # Extract payload
            payload = event_data.get('payload', event_data)
            source = event_data.get('source', payload.get('source', 'unknown'))
            
            # Validate payload schema
            validation_result = self._validate_payload(payload, source)
            if not validation_result['valid']:
                return {
                    "success": False,
                    "error": validation_result['error']
                }
            
            # Create ingestion envelope
            envelope = self._create_envelope(payload, source)
            
            # Store envelope record
            envelope_id = envelope['checksum']  # Use checksum as ID
            self._ingested_envelopes[envelope_id] = envelope
            
            # Publish MODULE_EVENT.data_validated
            self._publish_data_validated(envelope)
            
            return {
                "success": True,
                "envelope_id": envelope_id,
                "status": "validated",
                "message": "Data ingestion envelope created and validated (no ETL automation, no PII processing)"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _validate_payload(self, payload: Dict[str, Any], source: str) -> Dict[str, Any]:
        """
        Validate ingestion payload schema.
        
        Validates that payload is a dictionary (required).
        Does NOT validate PII content - that requires human approval.
        
        Args:
            payload: Payload to validate
            source: Source identifier
            
        Returns:
            Validation result dictionary
        """
        # Validate payload: dict (required)
        if payload is None:
            return {
                "valid": False,
                "error": "Missing required field: payload"
            }
        if not isinstance(payload, dict):
            return {
                "valid": False,
                "error": "payload must be a dictionary"
            }
        
        # Validate source: str (required)
        if not source or not isinstance(source, str):
            return {
                "valid": False,
                "error": "source must be a non-empty string"
            }
        
        # SAFETY: No PII validation - requires human approval
        # We only validate structure, not content
        
        return {"valid": True}
    
    def _create_envelope(self, payload: Dict[str, Any], source: str) -> Dict[str, Any]:
        """
        Create safe ingestion envelope.
        
        Envelope Schema:
        - source: str
        - timestamp: iso8601
        - payload: dict
        - checksum: str
        
        SAFETY: No ETL automation. No PII processing.
        
        Args:
            payload: Payload dictionary
            source: Source identifier
            
        Returns:
            Ingestion envelope dictionary
        """
        # Get current timestamp in ISO8601 format
        timestamp = datetime.now().isoformat()
        
        # Calculate checksum from payload
        # SAFETY: Checksum is for integrity, not PII detection
        payload_json = json.dumps(payload, sort_keys=True)
        checksum = hashlib.sha256(payload_json.encode('utf-8')).hexdigest()
        
        # Create envelope
        envelope = {
            "source": source,
            "timestamp": timestamp,
            "payload": payload,
            "checksum": checksum
        }
        
        return envelope
    
    def _publish_data_validated(self, envelope: Dict[str, Any]) -> None:
        """
        Publish MODULE_EVENT.data_validated.
        
        Emits validated ingestion envelope for storage.
        
        SAFETY: No ETL automation. No PII processing unless human-approved.
        
        Args:
            envelope: Ingestion envelope dictionary
        """
        if not self._event_bus:
            return
        
        try:
            event = self._event_bus.create_event(
                event_type=EventType.MODULE_EVENT,
                source=self.module_id,
                target=None,  # Broadcast to MODULE_EVENT subscribers
                data={
                    "name": "data_validated",
                    "envelope_id": envelope['checksum'],
                    "envelope": {
                        "source": envelope['source'],
                        "timestamp": envelope['timestamp'],
                        "payload": envelope['payload'],
                        "checksum": envelope['checksum']
                    }
                }
            )
            
            self._event_bus.publish(event)
        except Exception as e:
            print(f"⚠️  Data Lake Module: Failed to publish data_validated event: {e}")
    
    def ingest(self, payload: Dict[str, Any], source: str) -> Dict[str, Any]:
        """
        Public API: Ingest data into data lake.
        
        Creates safe ingestion envelope and emits data_validated event.
        
        SAFETY: No ETL automation. No PII processing unless human-approved.
        
        Args:
            payload: Payload dictionary (required)
            source: Source identifier (required)
        
        Returns:
            Result dictionary with envelope_id and status
        """
        if not self._loaded:
            return {
                "success": False,
                "error": "Module not loaded"
            }
        
        # Create data.ingest event data
        event_data = {
            "name": "data.ingest",
            "source": source,
            "payload": payload
        }
        
        # Handle the ingest request
        return self._handle_ingest(event_data)
    
    def get_ingested_envelopes(self) -> Dict[str, Any]:
        """
        Get all ingested envelopes.
        
        Returns:
            Dictionary with ingested envelopes information
        """
        return {
            "ingested_count": len(self._ingested_envelopes),
            "envelopes": [
                {
                    "envelope_id": envelope['checksum'],
                    "source": envelope['source'],
                    "timestamp": envelope['timestamp'],
                    "checksum": envelope['checksum'],
                    "payload_keys": list(envelope['payload'].keys()) if isinstance(envelope['payload'], dict) else []
                }
                for envelope in self._ingested_envelopes.values()
            ]
        }
    
    def shutdown(self) -> None:
        """Called when module is shutting down."""
        print("✅ Data Lake Module: Shutting down...")
        
        # Unsubscribe from events
        if self._event_bus:
            try:
                self._event_bus.unsubscribe(EventType.MODULE_EVENT, self._handle_module_event)
            except Exception:
                pass  # Non-critical
        
        self._loaded = False
        self._ingested_envelopes.clear()
        
        print("✅ Data Lake Module: Shutdown complete")

