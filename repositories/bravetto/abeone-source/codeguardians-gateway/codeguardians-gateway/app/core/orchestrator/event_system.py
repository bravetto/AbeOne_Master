"""
Event System - Simple and Elegant Event-Driven Architecture

Production-hardened event system for decoupled communication.
"""

import asyncio
import logging
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from prometheus_client import Counter

from app.utils.logging import get_logger

logger = get_logger(__name__)

# Prometheus metrics
EVENT_PUBLISHED = Counter(
    'REPLACE_ME',
    'Total events published',
    ['event_type']
)

EVENT_HANDLED = Counter(
    'REPLACE_ME',
    'Total events handled',
    ['event_type', 'handler']
)


class EventType(str, Enum):
    """Event types in the system."""
    SERVICE_HEALTH_CHANGED = "service_health_changed"
    SERVICE_DISCOVERED = "service_discovered"
    SERVICE_REGISTERED = "service_registered"
    SERVICE_UNREGISTERED = "service_unregistered"
    REQUEST_ROUTED = "request_routed"
    REQUEST_FAILED = "request_failed"
    CIRCUIT_BREAKER_OPENED = "circuit_breaker_opened"
    CIRCUIT_BREAKER_CLOSED = "circuit_breaker_closed"
    FORENSIC_ANALYSIS_TRIGGERED = "forensic_analysis_triggered"
    ARCHITECTURE_REVIEW_REQUESTED = "architecture_review_requested"


@dataclass
class Event:
    """Event data structure."""
    event_type: EventType
    timestamp: datetime = field(default_factory=datetime.now)
    data: Dict[str, Any] = field(default_factory=dict)
    source: Optional[str] = None


class EventBus:
    """
    Simple and elegant event bus for decoupled communication.
    
    PRODUCTION HARDENED:
    - Async event handling
    - Error resilience
    - Metrics integration
    - Simple API
    """
    
    def __init__(self):
        """Initialize event bus."""
        self._handlers: Dict[EventType, List[Callable]] = {}
        self._running = True
    
    def subscribe(self, event_type: EventType, handler: Callable[[Event], None]):
        """
        Subscribe to an event type.
        
        Args:
            event_type: Type of event to subscribe to
            handler: Async or sync handler function
        """
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
        logger.debug(f"Handler subscribed to {event_type.value}")
    
    def unsubscribe(self, event_type: EventType, handler: Callable[[Event], None]):
        """Unsubscribe from an event type."""
        if event_type in self._handlers:
            try:
                self._handlers[event_type].remove(handler)
                logger.debug(f"Handler unsubscribed from {event_type.value}")
            except ValueError:
                pass
    
    async def publish(self, event: Event):
        """
        Publish an event to all subscribers.
        
        PRODUCTION: Async handling, error resilience, metrics
        """
        if not self._running:
            return
        
        EVENT_PUBLISHED.labels(event_type=event.event_type.value).inc()
        
        handlers = self._handlers.get(event.event_type, [])
        if not handlers:
            logger.debug(f"No handlers for event {event.event_type.value}")
            return
        
        # Execute handlers concurrently
        tasks = []
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    tasks.append(self._safe_handle_async(handler, event))
                else:
                    tasks.append(self._safe_handle_sync(handler, event))
            except Exception as e:
                logger.error(f"Error creating handler task: {e}", exc_info=True)
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _safe_handle_async(self, handler: Callable, event: Event):
        """Safely handle async event handler."""
        try:
            await handler(event)
            EVENT_HANDLED.labels(
                event_type=event.event_type.value,
                handler=handler.__name__
            ).inc()
        except Exception as e:
            logger.error(
                f"Error in async handler {handler.__name__} for {event.event_type.value}: {e}",
                exc_info=True
            )
    
    async def _safe_handle_sync(self, handler: Callable, event: Event):
        """Safely handle sync event handler."""
        try:
            handler(event)
            EVENT_HANDLED.labels(
                event_type=event.event_type.value,
                handler=handler.__name__
            ).inc()
        except Exception as e:
            logger.error(
                f"Error in sync handler {handler.__name__} for {event.event_type.value}: {e}",
                exc_info=True
            )
    
    def shutdown(self):
        """Shutdown event bus."""
        self._running = False
        self._handlers.clear()
        logger.info("Event bus shutdown")


# Global event bus instance
_event_bus: Optional[EventBus] = None


def get_event_bus() -> EventBus:
    """Get global event bus instance."""
    global _event_bus
    if _event_bus is None:
        _event_bus = EventBus()
    return _event_bus

