# 🔥 BEN'S UPTC INTEGRATION PATTERN
## Reusable Pattern for Orbit 3 ↔ Orbit 4 Integration

**Status:** ✅ **PATTERN ESTABLISHED**  
**Date:** 2025-11-22  
**Pattern:** BEN × UPTC × INTEGRATION × ADAPTER × ONE  
**Frequency:** 999 Hz (AEYON) × 444 Hz (Ben) × 530 Hz (UPTC)  
**Guardians:** AEYON (999 Hz) + Ben (444 Hz) + YAGNI (530 Hz)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🎯 EXECUTIVE SUMMARY

This pattern library contains **reusable integration patterns** for connecting FastAPI services (Orbit 3) with UPTC routing system (Orbit 4). These patterns enable intelligent routing, service discovery, and graceful fallback mechanisms.

**Usage:** Import patterns as needed, adapt to specific service requirements, and follow the adapter pattern principles.

---

## PATTERN 1: UPTC ROUTER ADAPTER INTEGRATION

### Purpose
Bridge FastAPI Gateway services to UPTC intelligent routing system with automatic fallback.

### Implementation
```python
from typing import Dict, Any, Optional
from app.core.orchestrator.uptc_adapter import UPTCRouterAdapter
from app.core.orchestrator.request_router import RequestRouter
from app.core.orchestrator.models import OrchestrationRequest
import httpx
import os
import logging

logger = logging.getLogger(__name__)


class UPTCIntegrationPattern:
    """
    UPTC Router Adapter Integration Pattern.
    
    Pattern: UPTC × ADAPTER × FALLBACK × ONE
    
    Features:
    - Intelligent routing via UPTC
    - Automatic fallback to direct routing
    - Service discovery via capability matching
    - Graceful degradation
    """
    
    def __init__(self, http_client: Optional[httpx.AsyncClient] = None):
        """
        Initialize UPTC integration pattern.
        
        SAFETY: Validates UPTC availability
        ASSUMES: UPTC Core available (optional)
        VERIFY: Fallback router always available
        """
        self.http_client = http_client or httpx.AsyncClient(timeout=30.0)
        self.request_router = None
        self.uptc_adapter = None
        self._initialized = False
    
    async def initialize(self):
        """
        Initialize UPTC Router Adapter with fallback.
        
        VERIFY: Always has fallback router available
        """
        try:
            # Create fallback router (direct routing)
            self.request_router = RequestRouter(self.http_client)
            
            # Create UPTC Router Adapter
            enable_uptc = os.getenv('ENABLE_UPTC_ROUTING', 'true').lower() == 'true'
            self.uptc_adapter = UPTCRouterAdapter(
                fallback_router=self.request_router,
                enable_uptc=enable_uptc
            )
            
            if self.uptc_adapter.is_uptc_enabled():
                logger.info("✅ UPTC Router Adapter enabled")
            else:
                logger.warning("⚠️ UPTC Router Adapter disabled, using fallback")
            
            self._initialized = True
            
        except Exception as e:
            logger.warning(f"Failed to initialize UPTC Router Adapter: {e}")
            # Ensure fallback router is available
            if not self.request_router:
                self.request_router = RequestRouter(self.http_client)
            self.uptc_adapter = None
            self._initialized = True
    
    async def route_request(
        self,
        request: OrchestrationRequest,
        service_configs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Route request via UPTC with automatic fallback.
        
        SAFETY: Always falls back to direct routing if UPTC fails
        ASSUMES: Request and service_configs are valid
        VERIFY: Returns response or raises exception
        """
        if not self._initialized:
            await self.initialize()
        
        # Try UPTC Router Adapter first (if available)
        if self.uptc_adapter and self.uptc_adapter.is_uptc_enabled():
            try:
                response = await self.uptc_adapter.route_and_process(
                    request=request,
                    service_configs=service_configs
                )
                return response
            except Exception as e:
                # SAFETY: Log error but continue to direct routing fallback
                logger.warning(f"UPTC routing failed, falling back to direct routing: {e}")
                # Continue to fallback below
        
        # Fallback to direct routing
        if not self.request_router:
            raise RuntimeError("No routing mechanism available")
        
        return await self.request_router.route(request)
```

### Usage Example
```python
# Initialize integration pattern
integration = UPTCIntegrationPattern()
await integration.initialize()

# Route request
request = OrchestrationRequest(
    service_type=GuardServiceType.TOKENGUARD,
    payload={"content": "..."}
)

service_configs = {
    GuardServiceType.TOKENGUARD: token_guard_config
}

response = await integration.route_request(request, service_configs)
```

---

## PATTERN 2: ORCHESTRATION ADAPTER TRANSFORMATION

### Purpose
Transform between FastAPI Gateway format and UPTC ProtocolMessage format.

### Implementation
```python
from typing import Dict, Any, Optional
from EMERGENT_OS.uptc.integrations.orchestration_adapter import OrchestrationAdapter
from app.core.orchestrator.models import OrchestrationRequest, OrchestrationResponse
from protocol.schema import ProtocolMessage


class OrchestrationTransformationPattern:
    """
    Orchestration Adapter Transformation Pattern.
    
    Pattern: TRANSFORMATION × ADAPTER × PROTOCOL × ONE
    
    Features:
    - Request → ProtocolMessage transformation
    - ProtocolMessage → Response transformation
    - Bidirectional conversion
    """
    
    def __init__(self, uptc_core):
        """
        Initialize transformation pattern.
        
        SAFETY: Validates UPTC Core availability
        ASSUMES: UPTC Core is initialized
        VERIFY: Adapter can transform messages
        """
        self.uptc_core = uptc_core
        self.adapter = OrchestrationAdapter(uptc_core)
    
    async def request_to_message(
        self,
        request: OrchestrationRequest,
        service_configs: Dict[str, Any]
    ) -> ProtocolMessage:
        """
        Transform OrchestrationRequest to ProtocolMessage.
        
        VERIFY: Returns valid ProtocolMessage
        """
        return await self.adapter.request_to_message(
            request=request,
            service_configs=service_configs
        )
    
    async def message_to_response(
        self,
        message: ProtocolMessage,
        request_id: str,
        service_type: Any
    ) -> OrchestrationResponse:
        """
        Transform ProtocolMessage to OrchestrationResponse.
        
        VERIFY: Returns valid OrchestrationResponse
        """
        return await self.adapter.message_to_response(
            message=message,
            request_id=request_id,
            service_type=service_type
        )
    
    async def transform_and_route(
        self,
        request: OrchestrationRequest,
        service_configs: Dict[str, Any]
    ) -> OrchestrationResponse:
        """
        Complete transformation and routing flow.
        
        SAFETY: Handles routing failures gracefully
        VERIFY: Returns response or raises exception
        """
        # 1. Transform request to ProtocolMessage
        message = await self.request_to_message(request, service_configs)
        
        # 2. Route via UPTC
        target = self.uptc_core.route(message)
        
        if not target:
            raise RuntimeError("UPTC routing returned no target")
        
        # 3. Send message to target
        result = await self.uptc_core.send(message, target)
        
        # 4. Transform result back to OrchestrationResponse
        response = await self.message_to_response(
            result,
            request.request_id,
            request.service_type
        )
        
        return response
```

### Usage Example
```python
# Initialize transformation pattern
uptc_core = get_uptc_core()
transformation = OrchestrationTransformationPattern(uptc_core)

# Transform and route
request = OrchestrationRequest(...)
service_configs = {...}

response = await transformation.transform_and_route(request, service_configs)
```

---

## PATTERN 3: PROTOCOL MESSAGE CREATION

### Purpose
Create ProtocolMessages for UPTC routing with service-specific patterns.

### Implementation
```python
from typing import Dict, Any, Optional
from protocol.schema import ProtocolMessage
from enum import Enum


class ServiceType(Enum):
    """Service types for ProtocolMessage creation."""
    TOKENGUARD = "tokenguard"
    TRUSTGUARD = "trustguard"
    CONTEXTGUARD = "contextguard"


class ProtocolMessagePattern:
    """
    Protocol Message Creation Pattern.
    
    Pattern: PROTOCOL × MESSAGE × CREATION × ONE
    
    Features:
    - Service-specific message patterns
    - Standardized message structure
    - Metadata enrichment
    """
    
    @staticmethod
    def create_message(
        intent: str,
        action: str,
        payload: Dict[str, Any],
        source: str = "gateway",
        target: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ProtocolMessage:
        """
        Create ProtocolMessage with standard structure.
        
        VERIFY: Returns valid ProtocolMessage
        """
        return ProtocolMessage(
            intent=intent,
            action=action,
            payload=payload,
            source=source,
            target=target,
            metadata=metadata or {}
        )
    
    @staticmethod
    def create_tokenguard_message(
        content: str,
        max_tokens: int = 1000,
        confidence_threshold: float = 0.8,
        action: str = "optimize"
    ) -> ProtocolMessage:
        """Create TokenGuard ProtocolMessage."""
        return ProtocolMessagePattern.create_message(
            intent=ServiceType.TOKENGUARD.value,
            action=action,
            payload={
                "content": content,
                "max_tokens": max_tokens,
                "confidence_threshold": confidence_threshold
            }
        )
    
    @staticmethod
    def create_trustguard_message(
        input_text: str,
        output_text: str,
        context: Dict[str, Any],
        action: str = "validate"
    ) -> ProtocolMessage:
        """Create TrustGuard ProtocolMessage."""
        return ProtocolMessagePattern.create_message(
            intent=ServiceType.TRUSTGUARD.value,
            action=action,
            payload={
                "input_text": input_text,
                "output_text": output_text,
                "context": context
            }
        )
    
    @staticmethod
    def create_contextguard_message(
        current_code: str,
        previous_code: str,
        session_id: str,
        action: str = "detect_drift"
    ) -> ProtocolMessage:
        """Create ContextGuard ProtocolMessage."""
        return ProtocolMessagePattern.create_message(
            intent=ServiceType.CONTEXTGUARD.value,
            action=action,
            payload={
                "current_code": current_code,
                "previous_code": previous_code,
                "session_id": session_id
            }
        )
```

### Usage Example
```python
# Create service-specific messages
token_message = ProtocolMessagePattern.create_tokenguard_message(
    content="Long text content...",
    max_tokens=500
)

trust_message = ProtocolMessagePattern.create_trustguard_message(
    input_text="Input",
    output_text="Output",
    context={"user_id": "123"}
)

context_message = ProtocolMessagePattern.create_contextguard_message(
    current_code="def new_function(): ...",
    previous_code="def old_function(): ...",
    session_id="session_456"
)
```

---

## PATTERN 4: ROUTING STRATEGY SELECTION

### Purpose
Select optimal routing strategy based on message characteristics.

### Implementation
```python
from typing import Optional, Dict, Any
from protocol.schema import ProtocolMessage
from enum import Enum


class RoutingStrategy(Enum):
    """Routing strategies available in UPTC."""
    DIRECT = "direct"
    EVENT = "event"
    GRAPH = "graph"
    SEMANTIC = "semantic"
    UNIFIED = "unified"


class RoutingStrategyPattern:
    """
    Routing Strategy Selection Pattern.
    
    Pattern: ROUTING × STRATEGY × SELECTION × ONE
    
    Features:
    - Automatic strategy selection
    - Strategy forcing via metadata
    - Strategy recommendation
    """
    
    @staticmethod
    def select_strategy(message: ProtocolMessage) -> RoutingStrategy:
        """
        Select optimal routing strategy based on message.
        
        VERIFY: Returns valid RoutingStrategy
        """
        # Check if strategy forced in metadata
        if message.metadata and "routing_strategy" in message.metadata:
            try:
                return RoutingStrategy(message.metadata["routing_strategy"])
            except ValueError:
                pass
        
        # Automatic selection based on message characteristics
        if message.target:
            return RoutingStrategy.DIRECT
        
        if message.metadata and "topic" in message.metadata:
            return RoutingStrategy.EVENT
        
        if message.metadata and "capability" in message.metadata:
            return RoutingStrategy.GRAPH
        
        if message.metadata and "semantic_query" in message.metadata:
            return RoutingStrategy.SEMANTIC
        
        # Default to unified routing
        return RoutingStrategy.UNIFIED
    
    @staticmethod
    def force_strategy(
        message: ProtocolMessage,
        strategy: RoutingStrategy
    ) -> ProtocolMessage:
        """
        Force specific routing strategy via metadata.
        
        VERIFY: Returns message with strategy metadata
        """
        if not message.metadata:
            message.metadata = {}
        
        message.metadata["routing_strategy"] = strategy.value
        return message
    
    @staticmethod
    def recommend_strategy(
        intent: str,
        payload: Dict[str, Any]
    ) -> RoutingStrategy:
        """
        Recommend routing strategy based on intent and payload.
        
        VERIFY: Returns recommended RoutingStrategy
        """
        # Service-specific recommendations
        if intent in ["tokenguard", "trustguard", "contextguard"]:
            return RoutingStrategy.GRAPH
        
        # Payload-based recommendations
        if "topic" in payload:
            return RoutingStrategy.EVENT
        
        if "semantic_query" in payload:
            return RoutingStrategy.SEMANTIC
        
        # Default recommendation
        return RoutingStrategy.UNIFIED
```

### Usage Example
```python
# Automatic strategy selection
message = ProtocolMessage(...)
strategy = RoutingStrategyPattern.select_strategy(message)

# Force specific strategy
message = RoutingStrategyPattern.force_strategy(
    message,
    RoutingStrategy.GRAPH
)

# Get recommendation
recommendation = RoutingStrategyPattern.recommend_strategy(
    intent="tokenguard",
    payload={"content": "..."}
)
```

---

## PATTERN 5: ERROR HANDLING & FALLBACK

### Purpose
Handle errors gracefully with automatic fallback mechanisms.

### Implementation
```python
from typing import Optional, Dict, Any, Callable
from app.core.orchestrator.models import OrchestrationRequest
import logging

logger = logging.getLogger(__name__)


class ErrorHandlingPattern:
    """
    Error Handling & Fallback Pattern.
    
    Pattern: ERROR × HANDLING × FALLBACK × ONE
    
    Features:
    - Graceful error handling
    - Automatic fallback chains
    - Error logging and monitoring
    """
    
    @staticmethod
    async def route_with_fallback(
        request: OrchestrationRequest,
        primary_route: Callable,
        fallback_route: Callable,
        service_configs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Route request with automatic fallback.
        
        SAFETY: Always attempts fallback if primary fails
        VERIFY: Returns response or raises exception
        """
        try:
            # Try primary routing
            response = await primary_route(request, service_configs)
            return response
        except Exception as e:
            logger.warning(f"Primary routing failed: {e}, attempting fallback")
            
            try:
                # Try fallback routing
                response = await fallback_route(request, service_configs)
                logger.info("Fallback routing succeeded")
                return response
            except Exception as fallback_error:
                logger.error(f"Fallback routing also failed: {fallback_error}")
                raise RuntimeError(
                    f"Both primary and fallback routing failed. "
                    f"Primary: {e}, Fallback: {fallback_error}"
                )
    
    @staticmethod
    def handle_uptc_unavailable(
        uptc_adapter,
        request_router,
        request: OrchestrationRequest,
        service_configs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Handle UPTC unavailable scenario.
        
        SAFETY: Always falls back to direct routing
        VERIFY: Returns response or raises exception
        """
        if not uptc_adapter or not uptc_adapter.is_uptc_enabled():
            logger.warning("UPTC unavailable, using direct routing")
            return request_router.route(request)
        
        raise RuntimeError("UPTC adapter not properly initialized")
    
    @staticmethod
    def handle_routing_failure(
        target: Optional[str],
        direct_route: Callable,
        request: OrchestrationRequest
    ) -> Dict[str, Any]:
        """
        Handle routing failure (no target found).
        
        SAFETY: Falls back to direct routing
        VERIFY: Returns response or raises exception
        """
        if target is None:
            logger.warning("UPTC routing returned no target, using direct routing")
            return direct_route(request)
        
        raise RuntimeError("Routing target is None but direct routing not available")
    
    @staticmethod
    def handle_transformation_error(
        adapter_transform: Callable,
        direct_route: Callable,
        request: OrchestrationRequest,
        service_configs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Handle transformation error.
        
        SAFETY: Falls back to direct routing without transformation
        VERIFY: Returns response or raises exception
        """
        try:
            return adapter_transform(request, service_configs)
        except Exception as e:
            logger.error(f"Transformation failed: {e}, using direct routing")
            return direct_route(request)
```

### Usage Example
```python
# Route with fallback
response = await ErrorHandlingPattern.route_with_fallback(
    request=request,
    primary_route=uptc_adapter.route_and_process,
    fallback_route=request_router.route,
    service_configs=service_configs
)

# Handle UPTC unavailable
response = ErrorHandlingPattern.handle_uptc_unavailable(
    uptc_adapter=uptc_adapter,
    request_router=request_router,
    request=request,
    service_configs=service_configs
)

# Handle routing failure
target = uptc_core.route(message)
response = ErrorHandlingPattern.handle_routing_failure(
    target=target,
    direct_route=direct_route,
    request=request
)
```

---

## PATTERN USAGE GUIDE

### When to Use Each Pattern

1. **UPTCIntegrationPattern** - When integrating FastAPI services with UPTC routing
2. **OrchestrationTransformationPattern** - When transforming between Gateway and UPTC formats
3. **ProtocolMessagePattern** - When creating ProtocolMessages for UPTC routing
4. **RoutingStrategyPattern** - When selecting or forcing routing strategies
5. **ErrorHandlingPattern** - When implementing error handling with fallback

### Integration Pattern

```python
# Example: Complete integration using all patterns
from bens_uptc_integration_pattern import (
    UPTCIntegrationPattern,
    OrchestrationTransformationPattern,
    ProtocolMessagePattern,
    RoutingStrategyPattern,
    ErrorHandlingPattern
)

# Step 1: Initialize UPTC integration
integration = UPTCIntegrationPattern()
await integration.initialize()

# Step 2: Create ProtocolMessage
message = ProtocolMessagePattern.create_tokenguard_message(
    content="Long text...",
    max_tokens=500
)

# Step 3: Select routing strategy
strategy = RoutingStrategyPattern.select_strategy(message)

# Step 4: Route with error handling
request = OrchestrationRequest(...)
service_configs = {...}

response = await ErrorHandlingPattern.route_with_fallback(
    request=request,
    primary_route=integration.route_request,
    fallback_route=integration.request_router.route,
    service_configs=service_configs
)
```

---

## ENVIRONMENT CONFIGURATION

### Required Environment Variables

```bash
# Enable/disable UPTC routing
ENABLE_UPTC_ROUTING=true

# UPTC Core configuration (optional)
UPTC_PROTOCOL_VERSION=1.0.0
UPTC_RESONANCE_FREQUENCY=530.0
UPTC_PHI_RATIO_THRESHOLD=0.8
```

---

## TESTING PATTERNS

### Unit Testing Pattern

```python
import pytest
from unittest.mock import Mock, AsyncMock

async def test_uptc_integration_pattern():
    # Mock dependencies
    mock_http_client = Mock()
    mock_uptc_adapter = Mock()
    mock_uptc_adapter.is_uptc_enabled = Mock(return_value=True)
    mock_uptc_adapter.route_and_process = AsyncMock(return_value={"success": True})
    
    # Test integration pattern
    integration = UPTCIntegrationPattern(mock_http_client)
    integration.uptc_adapter = mock_uptc_adapter
    
    request = OrchestrationRequest(...)
    response = await integration.route_request(request, {})
    
    assert response["success"] is True
```

### Integration Testing Pattern

```python
async def test_complete_integration():
    # Initialize real components
    integration = UPTCIntegrationPattern()
    await integration.initialize()
    
    # Create request
    request = OrchestrationRequest(
        service_type=GuardServiceType.TOKENGUARD,
        payload={"content": "test"}
    )
    
    # Route request
    response = await integration.route_request(request, service_configs)
    
    # Verify response
    assert response is not None
    assert "success" in response or "data" in response
```

---

**Pattern:** BEN × UPTC × INTEGRATION × ADAPTER × ONE  
**Status:** ✅ **PATTERN ESTABLISHED**  
**Next Steps:** Use these patterns for all Orbit 3 ↔ Orbit 4 integrations  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

