"""
Direct Guard Services API

This module provides direct access to guard services at root endpoints
for backward compatibility with existing integrations and testing tools.
"""

from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from app.api.dependencies import get_current_user
from app.api.v1.guards_integrated import GuardRequest, GuardResponse
from app.api.v1.guards_integrated import (
    process_tokenguard,
    process_trustguard,
    process_contextguard,
    process_biasguard,
    process_healthguard
)

router = APIRouter(tags=["Direct Guard Access"])

# Direct endpoint mappings for backward compatibility
GUARD_ENDPOINTS = {
    "tokenguard": process_tokenguard,
    "trustguard": process_trustguard,
    "contextguard": process_contextguard,
    "biasguard": process_biasguard,
    "healthguard": process_healthguard,
}


@router.post("/tokenguard", response_model=GuardResponse)
async def direct_tokenguard(
    request: GuardRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Direct access to TokenGuard service.

    This endpoint provides backward compatibility for existing integrations
    that expect TokenGuard at the root /tokenguard path.
    """
    return await process_tokenguard(request, current_user)


@router.post("/trustguard", response_model=GuardResponse)
async def direct_trustguard(
    request: GuardRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Direct access to TrustGuard service.

    This endpoint provides backward compatibility for existing integrations
    that expect TrustGuard at the root /trustguard path.
    """
    return await process_trustguard(request, current_user)


@router.post("/contextguard", response_model=GuardResponse)
async def direct_contextguard(
    request: GuardRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Direct access to ContextGuard service.

    This endpoint provides backward compatibility for existing integrations
    that expect ContextGuard at the root /contextguard path.
    """
    return await process_contextguard(request, current_user)


@router.post("/biasguard", response_model=GuardResponse)
async def direct_biasguard(
    request: GuardRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Direct access to BiasGuard service.

    This endpoint provides backward compatibility for existing integrations
    that expect BiasGuard at the root /biasguard path.
    """
    return await process_biasguard(request, current_user)


@router.post("/healthguard", response_model=GuardResponse)
async def direct_healthguard(
    request: GuardRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Direct access to HealthGuard service.

    This endpoint provides backward compatibility for existing integrations
    that expect HealthGuard at the root /healthguard path.
    """
    return await process_healthguard(request, current_user)

