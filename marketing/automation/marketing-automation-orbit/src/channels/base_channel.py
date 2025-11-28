"""
Base Channel Interface
All channel integrations inherit from this base class.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime

from ..engine.automation_engine import Campaign


class BaseChannel(ABC):
    """
    Base class for all marketing channel integrations.
    
    Each channel (Google Ads, LinkedIn, Email, etc.) implements this interface.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize channel.
        
        Args:
            config: Channel-specific configuration
        """
        self.config = config
        self.name = self.__class__.__name__
    
    @abstractmethod
    async def create_campaign(self, campaign: Campaign) -> Dict[str, Any]:
        """
        Create a campaign in this channel.
        
        Args:
            campaign: Campaign object
            
        Returns:
            Creation result with campaign ID
        """
        pass
    
    @abstractmethod
    async def update_campaign(self, campaign_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing campaign.
        
        Args:
            campaign_id: Channel-specific campaign ID
            updates: Updates to apply
            
        Returns:
            Update result
        """
        pass
    
    @abstractmethod
    async def pause_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """
        Pause a campaign.
        
        Args:
            campaign_id: Channel-specific campaign ID
            
        Returns:
            Pause result
        """
        pass
    
    @abstractmethod
    async def get_campaign_metrics(self, campaign_id: str, start_date: datetime, end_date: datetime) -> Dict[str, float]:
        """
        Get campaign performance metrics.
        
        Args:
            campaign_id: Channel-specific campaign ID
            start_date: Start date for metrics
            end_date: End date for metrics
            
        Returns:
            Metrics dictionary
        """
        pass
    
    @abstractmethod
    async def test_connection(self) -> bool:
        """
        Test connection to channel API.
        
        Returns:
            True if connection successful
        """
        pass
    
    def validate_campaign(self, campaign: Campaign) -> List[str]:
        """
        Validate campaign before creation.
        
        Args:
            campaign: Campaign to validate
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        if campaign.budget <= 0:
            errors.append("Budget must be greater than 0")
        
        if not campaign.creatives:
            errors.append("Campaign must have at least one creative")
        
        if campaign.start_date < datetime.now():
            errors.append("Start date cannot be in the past")
        
        return errors

