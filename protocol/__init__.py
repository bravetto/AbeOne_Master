"""
Protocol Package

Core protocol implementation with schema definitions, contract validation,
and message handling utilities.
"""

from .schema import (
    ProtocolMessage,
    MessageType,
    MessagePriority,
    PROTOCOL_VERSION,
    normalize_message_data
)

from .contracts import (
    ProtocolContracts,
    ContractViolationError,
    RoutingConstraint
)

__all__ = [
    # Schema
    "ProtocolMessage",
    "MessageType",
    "MessagePriority",
    "PROTOCOL_VERSION",
    "normalize_message_data",
    # Contracts
    "ProtocolContracts",
    "ContractViolationError",
    "RoutingConstraint",
]

