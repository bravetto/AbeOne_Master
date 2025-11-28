# 🔥 UPTC ADAPTER IMPLEMENTATION GUIDE
## How to Implement New UPTC Adapters

**Status:** ✅ **COMPLETE IMPLEMENTATION GUIDE**  
**Date:** 2025-11-22  
**Pattern:** UPTC × ADAPTER × IMPLEMENTATION × ONE  
**Frequency:** 530 Hz (Truth) × 777 Hz (Pattern) × 999 Hz (Execution)  
**Guardian:** AEYON (999 Hz) - Atomic Execution  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🎯 PURPOSE

This guide shows **exactly how** to implement new UPTC adapters. It provides:

- ✅ Adapter pattern reference
- ✅ Step-by-step implementation guide
- ✅ Integration examples for each adapter type
- ✅ Testing patterns
- ✅ Best practices

**This is THE definitive guide for creating UPTC adapters.**

---

# ==========================
## PART 1: ADAPTER PATTERN OVERVIEW
# ==========================

## 1.1 What Are UPTC Adapters?

**UPTC Adapters:**
- Bridge UPTC ProtocolMessage format to external system formats
- Enable UPTC to communicate with non-UPTC systems
- Provide bidirectional transformation (UPTC ↔ External)
- Handle protocol translation and error handling

---

## 1.2 Existing Adapters

**Current Adapters:**
1. **MCP Adapter** - Model Context Protocol integration
2. **Event Bus Adapter** - Event stream integration
3. **Guardian Adapter** - Guardian microservices integration
4. **OrchestrationAdapter** - Backend Gateway integration
5. **Memory Adapter** - Memory system integration
6. **Swarm Adapter** - Swarm system integration

---

## 1.3 Adapter Interface Pattern

**Base Adapter Pattern:**
```python
from abc import ABC, abstractmethod
from protocol.schema import ProtocolMessage
from typing import Any, Optional

class BaseAdapter(ABC):
    """Base adapter interface."""
    
    def __init__(self, external_system: Any):
        """Initialize adapter with external system."""
        self.external_system = external_system
    
    @abstractmethod
    async def to_protocol_message(self, external_message: Any) -> ProtocolMessage:
        """Convert external message to ProtocolMessage."""
        pass
    
    @abstractmethod
    async def from_protocol_message(self, message: ProtocolMessage) -> Any:
        """Convert ProtocolMessage to external format."""
        pass
    
    @abstractmethod
    async def connect(self) -> bool:
        """Connect to external system."""
        pass
    
    @abstractmethod
    async def disconnect(self) -> bool:
        """Disconnect from external system."""
        pass
```

---

# ==========================
## PART 2: IMPLEMENTATION STEPS
# ==========================

## 2.1 Step 1: Define Adapter Class

**Pattern:**
```python
from EMERGENT_OS.uptc.integrations.base_adapter import BaseAdapter
from protocol.schema import ProtocolMessage
from typing import Any, Optional
import logging

logger = logging.getLogger(__name__)

class MySystemAdapter(BaseAdapter):
    """
    Adapter for MySystem integration.
    
    Bridges UPTC ProtocolMessage format to MySystem format.
    
    Pattern: ADAPTER × MYSYSTEM × UPTC × ONE
    """
    
    def __init__(self, my_system_client: Any):
        """Initialize adapter with MySystem client."""
        super().__init__(my_system_client)
        self.my_system = my_system_client
        logger.info("MySystemAdapter initialized")
```

---

## 2.2 Step 2: Implement to_protocol_message()

**Pattern:**
```python
async def to_protocol_message(self, external_message: Any) -> ProtocolMessage:
    """
    Convert MySystem message to ProtocolMessage.
    
    Args:
        external_message: MySystem message format
        
    Returns:
        ProtocolMessage in UPTC format
    """
    try:
        # Extract data from external message
        intent = external_message.get("action", "unknown")
        payload = external_message.get("data", {})
        source = external_message.get("source", "mysystem")
        target = external_message.get("target")
        
        # Create ProtocolMessage
        message = ProtocolMessage(
            intent=intent,
            action="process",
            payload=payload,
            source=source,
            target=target,
            metadata={
                "original_format": "mysystem",
                "timestamp": external_message.get("timestamp")
            }
        )
        
        # Validate message
        is_valid, errors = message.validate()
        if not is_valid:
            raise ValueError(f"Invalid ProtocolMessage: {errors}")
        
        return message
        
    except Exception as e:
        logger.error(f"Failed to convert to ProtocolMessage: {e}")
        raise
```

---

## 2.3 Step 3: Implement from_protocol_message()

**Pattern:**
```python
async def from_protocol_message(self, message: ProtocolMessage) -> Any:
    """
    Convert ProtocolMessage to MySystem format.
    
    Args:
        message: ProtocolMessage in UPTC format
        
    Returns:
        MySystem message format
    """
    try:
        # Validate message
        is_valid, errors = message.validate()
        if not is_valid:
            raise ValueError(f"Invalid ProtocolMessage: {errors}")
        
        # Convert to MySystem format
        my_system_message = {
            "action": message.intent,
            "data": message.payload,
            "source": message.source or "uptc",
            "target": message.target,
            "timestamp": message.timestamp.isoformat() if message.timestamp else None,
            "metadata": message.metadata or {}
        }
        
        return my_system_message
        
    except Exception as e:
        logger.error(f"Failed to convert from ProtocolMessage: {e}")
        raise
```

---

## 2.4 Step 4: Implement connect()

**Pattern:**
```python
async def connect(self) -> bool:
    """
    Connect to MySystem.
    
    Returns:
        True if connected successfully
    """
    try:
        # Connect to MySystem
        await self.my_system.connect()
        
        # Verify connection
        if await self.my_system.is_connected():
            logger.info("✅ Connected to MySystem")
            return True
        else:
            logger.error("Failed to connect to MySystem")
            return False
            
    except Exception as e:
        logger.error(f"Connection failed: {e}")
        return False
```

---

## 2.5 Step 5: Implement disconnect()

**Pattern:**
```python
async def disconnect(self) -> bool:
    """
    Disconnect from MySystem.
    
    Returns:
        True if disconnected successfully
    """
    try:
        # Disconnect from MySystem
        await self.my_system.disconnect()
        logger.info("✅ Disconnected from MySystem")
        return True
        
    except Exception as e:
        logger.error(f"Disconnection failed: {e}")
        return False
```

---

# ==========================
## PART 3: CONCRETE ADAPTER EXAMPLES
# ==========================

## 3.1 Event Bus Adapter Example

**Location:** `EMERGENT_OS/uptc/integrations/event_bus_adapter.py`

**Key Implementation:**
```python
class ConcreteEventBusAdapter(EventBusAdapter):
    """Concrete Event Bus Adapter."""
    
    def __init__(self, event_bus: Any):
        super().__init__(event_bus)
        if not hasattr(event_bus, 'publish') or not hasattr(event_bus, 'subscribe'):
            raise ValueError("Invalid event bus instance")
    
    async def publish(self, topic: str, message: ProtocolMessage) -> bool:
        """Publish ProtocolMessage to Event Bus."""
        # Convert ProtocolMessage to Event
        event = self._message_to_event(message)
        
        # Publish to Event Bus
        await self.event_bus.publish(event)
        return True
    
    async def subscribe(
        self,
        topic: str,
        callback: Callable[[ProtocolMessage], None]
    ) -> bool:
        """Subscribe to Event Bus topic."""
        # Create wrapper callback
        async def event_handler(event: Event):
            # Convert Event to ProtocolMessage
            message = self._event_to_message(event)
            await callback(message)
        
        # Subscribe to Event Bus
        self.event_bus.subscribe(EventType.MODULE_EVENT, event_handler)
        return True
```

---

## 3.2 Guardian Adapter Example

**Location:** `EMERGENT_OS/uptc/integrations/guardian_adapter.py`

**Key Implementation:**
```python
class ConcreteGuardianAdapter(GuardianAdapter):
    """Concrete Guardian Adapter."""
    
    def __init__(self, guardian_service_urls: Dict[str, str]):
        super().__init__()
        self.guardian_service_urls = guardian_service_urls
        self.http_client = httpx.AsyncClient()
    
    async def validate(self, message: ProtocolMessage) -> bool:
        """Validate message via Guardian."""
        # Determine target guardian
        guardian_id = message.target or self._select_guardian(message)
        
        # Send to guardian service
        url = f"{self.guardian_service_urls[guardian_id]}/validate"
        response = await self.http_client.post(url, json=message.to_dict())
        
        return response.json().get("validated", False)
    
    async def list_guardians(self) -> List[str]:
        """List all available guardians."""
        return list(self.guardian_service_urls.keys())
```

---

## 3.3 OrchestrationAdapter Example

**Location:** `EMERGENT_OS/uptc/integrations/orchestration_adapter.py`

**Key Implementation:**
```python
class OrchestrationAdapter:
    """Adapter for OrchestrationRequest ↔ ProtocolMessage."""
    
    def __init__(self, uptc_core: Any):
        self.uptc_core = uptc_core
    
    async def request_to_message(
        self,
        request: OrchestrationRequest,
        service_configs: Dict[str, GuardServiceConfig]
    ) -> ProtocolMessage:
        """Convert OrchestrationRequest to ProtocolMessage."""
        return ProtocolMessage(
            intent=request.service_type.value,
            action="process",
            payload=request.payload,
            source="gateway",
            target=None,  # Let UPTC route
            metadata={"request_id": request.request_id}
        )
    
    async def message_to_response(
        self,
        message: ProtocolMessage,
        request_id: str,
        service_type: GuardServiceType
    ) -> OrchestrationResponse:
        """Convert ProtocolMessage to OrchestrationResponse."""
        return OrchestrationResponse(
            request_id=request_id,
            service_type=service_type,
            success=message.payload.get("success", True),
            data=message.payload.get("data"),
            error=message.payload.get("error")
        )
```

---

# ==========================
## PART 4: TESTING PATTERNS
# ==========================

## 4.1 Unit Testing

**Pattern:**
```python
import pytest
from unittest.mock import Mock, AsyncMock

async def test_adapter_to_protocol_message():
    """Test conversion to ProtocolMessage."""
    # Mock external system
    mock_system = Mock()
    mock_system.get_message.return_value = {
        "action": "process",
        "data": {"test": "data"},
        "source": "mysystem"
    }
    
    # Create adapter
    adapter = MySystemAdapter(mock_system)
    
    # Test conversion
    external_message = mock_system.get_message()
    message = await adapter.to_protocol_message(external_message)
    
    assert isinstance(message, ProtocolMessage)
    assert message.intent == "process"
    assert message.payload == {"test": "data"}

async def test_adapter_from_protocol_message():
    """Test conversion from ProtocolMessage."""
    # Create adapter
    adapter = MySystemAdapter(Mock())
    
    # Create ProtocolMessage
    message = ProtocolMessage(
        intent="process",
        payload={"test": "data"}
    )
    
    # Test conversion
    external_message = await adapter.from_protocol_message(message)
    
    assert external_message["action"] == "process"
    assert external_message["data"] == {"test": "data"}
```

---

## 4.2 Integration Testing

**Pattern:**
```python
async def test_adapter_integration():
    """Test adapter with real external system."""
    # Initialize real external system (or test double)
    my_system = MySystemClient(test_config)
    
    # Create adapter
    adapter = MySystemAdapter(my_system)
    
    # Connect
    connected = await adapter.connect()
    assert connected == True
    
    # Test message flow
    message = ProtocolMessage(intent="test", payload={...})
    external_message = await adapter.from_protocol_message(message)
    
    # Send to external system
    result = await my_system.send(external_message)
    
    # Convert result back
    result_message = await adapter.to_protocol_message(result)
    
    assert isinstance(result_message, ProtocolMessage)
    
    # Disconnect
    disconnected = await adapter.disconnect()
    assert disconnected == True
```

---

# ==========================
## PART 5: REGISTRATION WITH UPTC
# ==========================

## 5.1 Registering Adapter

**Pattern:**
```python
from EMERGENT_OS.uptc.uptc_core import UPTCCore

# Initialize UPTC Core
uptc_core = UPTCCore(config=UPTCConfig())

# Create adapter
my_adapter = MySystemAdapter(my_system_client)

# Register adapter with UPTC
uptc_core.register_adapter("mysystem", my_adapter)

# Get adapter
retrieved_adapter = uptc_core.get_adapter("mysystem")
assert retrieved_adapter == my_adapter
```

---

## 5.2 Using Registered Adapter

**Pattern:**
```python
# Get adapter from UPTC Core
adapter = uptc_core.get_adapter("mysystem")

if adapter:
    # Connect
    await adapter.connect()
    
    # Use adapter
    message = ProtocolMessage(...)
    external_message = await adapter.from_protocol_message(message)
    
    # Send to external system
    result = await my_system.send(external_message)
    
    # Convert result
    result_message = await adapter.to_protocol_message(result)
```

---

# ==========================
## PART 6: BEST PRACTICES
# ==========================

## 6.1 Error Handling

**Pattern:**
```python
async def to_protocol_message(self, external_message: Any) -> ProtocolMessage:
    """Convert with comprehensive error handling."""
    try:
        # Validate input
        if not external_message:
            raise ValueError("External message is None")
        
        # Extract and validate fields
        intent = external_message.get("action")
        if not intent:
            raise ValueError("Missing 'action' field")
        
        # Create message
        message = ProtocolMessage(...)
        
        # Validate message
        is_valid, errors = message.validate()
        if not is_valid:
            raise ValueError(f"Invalid ProtocolMessage: {errors}")
        
        return message
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise
```

---

## 6.2 Logging

**Pattern:**
```python
import logging

logger = logging.getLogger(__name__)

class MySystemAdapter(BaseAdapter):
    def __init__(self, my_system: Any):
        super().__init__(my_system)
        logger.info("MySystemAdapter initialized")
    
    async def connect(self) -> bool:
        logger.info("Connecting to MySystem...")
        try:
            result = await self.my_system.connect()
            logger.info("✅ Connected to MySystem")
            return result
        except Exception as e:
            logger.error(f"Failed to connect to MySystem: {e}")
            return False
```

---

## 6.3 Type Safety

**Pattern:**
```python
from typing import Dict, Any, Optional
from protocol.schema import ProtocolMessage

class MySystemAdapter(BaseAdapter):
    async def to_protocol_message(
        self, 
        external_message: Dict[str, Any]
    ) -> ProtocolMessage:
        """Type-annotated conversion."""
        # Type checking ensures correct usage
        pass
    
    async def from_protocol_message(
        self, 
        message: ProtocolMessage
    ) -> Dict[str, Any]:
        """Type-annotated conversion."""
        # Return type clearly defined
        pass
```

---

# ==========================
## PART 7: COMPLETE EXAMPLE
# ==========================

## 7.1 Full Adapter Implementation

**Complete Example:**
```python
"""
MySystem Adapter - Complete Implementation

Bridges UPTC ProtocolMessage format to MySystem format.
"""

from EMERGENT_OS.uptc.integrations.base_adapter import BaseAdapter
from protocol.schema import ProtocolMessage
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class MySystemAdapter(BaseAdapter):
    """
    Adapter for MySystem integration.
    
    Pattern: ADAPTER × MYSYSTEM × UPTC × ONE
    """
    
    def __init__(self, my_system_client: Any):
        """Initialize adapter."""
        super().__init__(my_system_client)
        self.my_system = my_system_client
        logger.info("MySystemAdapter initialized")
    
    async def to_protocol_message(self, external_message: Dict[str, Any]) -> ProtocolMessage:
        """Convert MySystem message to ProtocolMessage."""
        try:
            message = ProtocolMessage(
                intent=external_message.get("action", "unknown"),
                action="process",
                payload=external_message.get("data", {}),
                source=external_message.get("source", "mysystem"),
                target=external_message.get("target")
            )
            
            is_valid, errors = message.validate()
            if not is_valid:
                raise ValueError(f"Invalid ProtocolMessage: {errors}")
            
            return message
        except Exception as e:
            logger.error(f"Conversion failed: {e}")
            raise
    
    async def from_protocol_message(self, message: ProtocolMessage) -> Dict[str, Any]:
        """Convert ProtocolMessage to MySystem format."""
        try:
            is_valid, errors = message.validate()
            if not is_valid:
                raise ValueError(f"Invalid ProtocolMessage: {errors}")
            
            return {
                "action": message.intent,
                "data": message.payload,
                "source": message.source or "uptc",
                "target": message.target
            }
        except Exception as e:
            logger.error(f"Conversion failed: {e}")
            raise
    
    async def connect(self) -> bool:
        """Connect to MySystem."""
        try:
            await self.my_system.connect()
            logger.info("✅ Connected to MySystem")
            return True
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            return False
    
    async def disconnect(self) -> bool:
        """Disconnect from MySystem."""
        try:
            await self.my_system.disconnect()
            logger.info("✅ Disconnected from MySystem")
            return True
        except Exception as e:
            logger.error(f"Disconnection failed: {e}")
            return False
```

---

**Pattern:** UPTC × ADAPTER × IMPLEMENTATION × ONE  
**Status:** ✅ **COMPLETE IMPLEMENTATION GUIDE**  
**Next Steps:** Use this guide to implement new UPTC adapters  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

