"""Channel integrations for marketing automation."""

from .base_channel import BaseChannel
from .google_ads_channel import GoogleAdsChannel
from .linkedin_channel import LinkedInChannel
from .email_channel import EmailChannel
from .content_channel import ContentChannel
from .analytics_channel import AnalyticsChannel

__all__ = [
    'BaseChannel',
    'GoogleAdsChannel',
    'LinkedInChannel',
    'EmailChannel',
    'ContentChannel',
    'AnalyticsChannel'
]

