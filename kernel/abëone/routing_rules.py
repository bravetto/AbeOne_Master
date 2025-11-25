"""
Routing Rules Engine - Event Bus Routing Rules

Implements sophisticated routing rules engine for event bus.

Pattern: ROUTING × RULES × ENGINE × ONE
Philosophy: 80/20 → 97.8% Certainty
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from .EVENT_BUS import EventType, Event


class RoutingStrategy(Enum):
    """Routing strategy types."""
    BROADCAST = "broadcast"  # Broadcast to all subscribers
    TARGET = "target"  # Route to specific target
    FILTER = "filter"  # Route based on filter
    PRIORITY = "priority"  # Route based on priority
    ROUND_ROBIN = "round_robin"  # Round-robin routing


@dataclass
class RoutingRule:
    """Routing rule definition."""
    rule_id: str
    event_type: EventType
    strategy: RoutingStrategy
    target: Optional[str] = None
    filter_func: Optional[Callable[[Event], bool]] = None
    priority: int = 0
    enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


class RoutingRulesEngine:
    """
    Routing Rules Engine.
    
    Responsibilities:
    - Manage routing rules
    - Evaluate routing rules
    - Route events based on rules
    """
    
    def __init__(self):
        """Initialize routing rules engine."""
        self.rules: Dict[str, RoutingRule] = {}
        self.default_rules: Dict[EventType, RoutingStrategy] = {
            EventType.SYSTEM_EVENT: RoutingStrategy.BROADCAST,
            EventType.MODULE_EVENT: RoutingStrategy.TARGET,
            EventType.GUARDIAN_EVENT: RoutingStrategy.TARGET,
            EventType.OBSERVER_EVENT: RoutingStrategy.BROADCAST
        }
    
    def add_rule(self, rule: RoutingRule) -> bool:
        """
        Add a routing rule.
        
        Args:
            rule: Routing rule to add
        
        Returns:
            True if rule added successfully
        """
        if rule.rule_id in self.rules:
            return False  # Rule already exists
        
        self.rules[rule.rule_id] = rule
        return True
    
    def remove_rule(self, rule_id: str) -> bool:
        """
        Remove a routing rule.
        
        Args:
            rule_id: Rule identifier
        
        Returns:
            True if rule removed successfully
        """
        if rule_id not in self.rules:
            return False
        
        del self.rules[rule_id]
        return True
    
    def get_rule(self, rule_id: str) -> Optional[RoutingRule]:
        """
        Get routing rule by ID.
        
        Args:
            rule_id: Rule identifier
        
        Returns:
            Routing rule or None
        """
        return self.rules.get(rule_id)
    
    def evaluate_rules(self, event: Event) -> List[RoutingRule]:
        """
        Evaluate routing rules for an event.
        
        Args:
            event: Event to evaluate
        
        Returns:
            List of matching routing rules
        """
        matching_rules: List[RoutingRule] = []
        
        for rule in self.rules.values():
            if not rule.enabled:
                continue
            
            if rule.event_type != event.event_type:
                continue
            
            # Check filter function if present
            if rule.filter_func and not rule.filter_func(event):
                continue
            
            matching_rules.append(rule)
        
        # Sort by priority (higher priority first)
        matching_rules.sort(key=lambda r: r.priority, reverse=True)
        
        return matching_rules
    
    def get_routing_strategy(self, event: Event) -> RoutingStrategy:
        """
        Get routing strategy for an event.
        
        Args:
            event: Event to route
        
        Returns:
            Routing strategy
        """
        # Evaluate rules
        matching_rules = self.evaluate_rules(event)
        
        if matching_rules:
            # Use first matching rule (highest priority)
            return matching_rules[0].strategy
        
        # Use default strategy for event type
        return self.default_rules.get(event.event_type, RoutingStrategy.BROADCAST)
    
    def validate_rule(self, rule: RoutingRule) -> Tuple[bool, Optional[str]]:
        """
        Validate a routing rule.
        
        Args:
            rule: Routing rule to validate
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not rule.rule_id:
            return False, "Rule ID is required"
        
        if not rule.event_type:
            return False, "Event type is required"
        
        if not rule.strategy:
            return False, "Routing strategy is required"
        
        # Validate strategy-specific requirements
        if rule.strategy == RoutingStrategy.TARGET and not rule.target:
            return False, "Target is required for TARGET strategy"
        
        if rule.strategy == RoutingStrategy.FILTER and not rule.filter_func:
            return False, "Filter function is required for FILTER strategy"
        
        return True, None
    
    def get_all_rules(self) -> List[RoutingRule]:
        """
        Get all routing rules.
        
        Returns:
            List of all routing rules
        """
        return list(self.rules.values())
    
    def enable_rule(self, rule_id: str) -> bool:
        """
        Enable a routing rule.
        
        Args:
            rule_id: Rule identifier
        
        Returns:
            True if rule enabled successfully
        """
        if rule_id not in self.rules:
            return False
        
        self.rules[rule_id].enabled = True
        return True
    
    def disable_rule(self, rule_id: str) -> bool:
        """
        Disable a routing rule.
        
        Args:
            rule_id: Rule identifier
        
        Returns:
            True if rule disabled successfully
        """
        if rule_id not in self.rules:
            return False
        
        self.rules[rule_id].enabled = False
        return True

