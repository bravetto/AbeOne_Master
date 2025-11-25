"""
User Segmentation Logic for A/B Testing

Implements consistent hashing for user assignment to experiment variants
with support for traffic splitting, audience targeting, and exclusion criteria.
"""

import hashlib
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import redis
import logging
from dataclasses import asdict

from .models import ExperimentConfig, VariantConfig, UserSegment, ExperimentStatus

logger = logging.getLogger(__name__)

class UserSegmentationEngine:
    """
    User segmentation engine for A/B testing.
    
    Provides consistent user assignment to experiment variants using
    deterministic hashing and supports advanced targeting criteria.
    """
    
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client
        self.segment_cache_prefix = "ab_test:segment:"
        self.experiment_cache_prefix = "ab_test:experiment:"
        self.cache_ttl = 3600  # 1 hour
    
    def assign_user_to_variant(
        self, 
        user_id: str, 
        experiment_id: str,
        user_attributes: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """
        Assign user to experiment variant using consistent hashing.
        
        Args:
            user_id: Unique user identifier
            experiment_id: Experiment identifier
            user_attributes: Optional user attributes for targeting
            
        Returns:
            Variant name or None if user is excluded
        """
        try:
            # Check if user is already assigned
            cached_assignment = self._get_cached_assignment(user_id, experiment_id)
            if cached_assignment:
                return cached_assignment
            
            # Get experiment configuration
            experiment = self._get_experiment_config(experiment_id)
            if not experiment or experiment.status != ExperimentStatus.RUNNING:
                return None
            
            # Check exclusion criteria
            if self._is_user_excluded(user_id, experiment, user_attributes):
                return None
            
            # Check target audience criteria
            if not self._matches_target_audience(user_attributes, experiment.target_audience):
                return None
            
            # Assign user to variant using consistent hashing
            variant = self._assign_variant_consistent_hashing(user_id, experiment_id, experiment.traffic_split)
            
            if variant:
                # Cache the assignment
                self._cache_assignment(user_id, experiment_id, variant)
                
                # Store in database
                self._store_user_segment(user_id, experiment_id, variant)
                
                logger.info(f"User {user_id} assigned to variant {variant} for experiment {experiment_id}")
            
            return variant
            
        except Exception as e:
            logger.error(f"Error assigning user {user_id} to experiment {experiment_id}: {e}")
            return None
    
    def _assign_variant_consistent_hashing(
        self, 
        user_id: str, 
        experiment_id: str, 
        traffic_split: Dict[str, float]
    ) -> Optional[str]:
        """
        Assign variant using consistent hashing for deterministic results.
        
        Args:
            user_id: User identifier
            experiment_id: Experiment identifier
            traffic_split: Traffic distribution across variants
            
        Returns:
            Assigned variant name
        """
        # Create hash input
        hash_input = f"{experiment_id}:{user_id}"
        hash_value = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
        
        # Normalize to 0-1 range
        normalized_hash = (hash_value % 10000) / 10000.0
        
        # Assign based on traffic split
        cumulative_percentage = 0.0
        for variant_name, percentage in traffic_split.items():
            cumulative_percentage += percentage / 100.0
            if normalized_hash <= cumulative_percentage:
                return variant_name
        
        # Fallback to first variant
        return list(traffic_split.keys())[0] if traffic_split else None
    
    def _is_user_excluded(
        self, 
        user_id: str, 
        experiment: ExperimentConfig,
        user_attributes: Optional[Dict[str, Any]]
    ) -> bool:
        """
        Check if user should be excluded from experiment.
        
        Args:
            user_id: User identifier
            experiment: Experiment configuration
            user_attributes: User attributes
            
        Returns:
            True if user should be excluded
        """
        if not experiment.exclusion_criteria:
            return False
        
        for criteria in experiment.exclusion_criteria:
            if self._evaluate_exclusion_criteria(user_id, criteria, user_attributes):
                return True
        
        return False
    
    def _evaluate_exclusion_criteria(
        self, 
        user_id: str, 
        criteria: str, 
        user_attributes: Optional[Dict[str, Any]]
    ) -> bool:
        """
        Evaluate specific exclusion criteria.
        
        Args:
            user_id: User identifier
            criteria: Exclusion criteria string
            user_attributes: User attributes
            
        Returns:
            True if criteria matches (user should be excluded)
        """
        try:
            # Parse criteria (simple implementation)
            # Format: "attribute:operator:value"
            parts = criteria.split(":")
            if len(parts) != 3:
                return False
            
            attribute, operator, value = parts
            
            if not user_attributes or attribute not in user_attributes:
                return False
            
            user_value = user_attributes[attribute]
            
            # Evaluate based on operator
            if operator == "equals":
                return str(user_value) == value
            elif operator == "not_equals":
                return str(user_value) != value
            elif operator == "greater_than":
                return float(user_value) > float(value)
            elif operator == "less_than":
                return float(user_value) < float(value)
            elif operator == "contains":
                return value in str(user_value)
            elif operator == "not_contains":
                return value not in str(user_value)
            
            return False
            
        except Exception as e:
            logger.error(f"Error evaluating exclusion criteria '{criteria}': {e}")
            return False
    
    def _matches_target_audience(
        self, 
        user_attributes: Optional[Dict[str, Any]], 
        target_audience: Dict[str, Any]
    ) -> bool:
        """
        Check if user matches target audience criteria.
        
        Args:
            user_attributes: User attributes
            target_audience: Target audience configuration
            
        Returns:
            True if user matches target audience
        """
        if not target_audience or not user_attributes:
            return True  # No targeting criteria means all users
        
        for attribute, criteria in target_audience.items():
            if attribute not in user_attributes:
                return False
            
            user_value = user_attributes[attribute]
            
            # Handle different criteria types
            if isinstance(criteria, dict):
                if "min" in criteria and float(user_value) < criteria["min"]:
                    return False
                if "max" in criteria and float(user_value) > criteria["max"]:
                    return False
                if "values" in criteria and user_value not in criteria["values"]:
                    return False
            elif isinstance(criteria, list):
                if user_value not in criteria:
                    return False
            else:
                if str(user_value) != str(criteria):
                    return False
        
        return True
    
    def _get_cached_assignment(self, user_id: str, experiment_id: str) -> Optional[str]:
        """Get cached user assignment."""
        try:
            cache_key = f"{self.segment_cache_prefix}{experiment_id}:{user_id}"
            cached_value = self.redis_client.get(cache_key)
            return cached_value.decode() if cached_value else None
        except Exception as e:
            logger.error(f"Error getting cached assignment: {e}")
            return None
    
    def _cache_assignment(self, user_id: str, experiment_id: str, variant: str):
        """Cache user assignment."""
        try:
            cache_key = f"{self.segment_cache_prefix}{experiment_id}:{user_id}"
            self.redis_client.setex(cache_key, self.cache_ttl, variant)
        except Exception as e:
            logger.error(f"Error caching assignment: {e}")
    
    def _get_experiment_config(self, experiment_id: str) -> Optional[ExperimentConfig]:
        """Get experiment configuration from cache or database."""
        try:
            # Try cache first
            cache_key = f"{self.experiment_cache_prefix}{experiment_id}"
            cached_config = self.redis_client.get(cache_key)
            
            if cached_config:
                config_data = json.loads(cached_config)
                return ExperimentConfig(**config_data)
            
            # TODO: Implement database lookup
            # For now, return None
            return None
            
        except Exception as e:
            logger.error(f"Error getting experiment config: {e}")
            return None
    
    def _store_user_segment(self, user_id: str, experiment_id: str, variant: str):
        """Store user segment assignment in database."""
        try:
            # TODO: Implement database storage
            # For now, just log
            logger.info(f"Storing user segment: {user_id} -> {experiment_id}:{variant}")
        except Exception as e:
            logger.error(f"Error storing user segment: {e}")
    
    def get_user_variants(self, user_id: str) -> Dict[str, str]:
        """
        Get all active variant assignments for a user.
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary of experiment_id -> variant_name
        """
        try:
            # TODO: Implement database query
            # For now, return empty dict
            return {}
        except Exception as e:
            logger.error(f"Error getting user variants: {e}")
            return {}
    
    def invalidate_user_cache(self, user_id: str, experiment_id: Optional[str] = None):
        """
        Invalidate cached assignments for a user.
        
        Args:
            user_id: User identifier
            experiment_id: Optional specific experiment
        """
        try:
            if experiment_id:
                cache_key = f"{self.segment_cache_prefix}{experiment_id}:{user_id}"
                self.redis_client.delete(cache_key)
            else:
                # Delete all cached assignments for user
                pattern = f"{self.segment_cache_prefix}*:{user_id}"
                keys = self.redis_client.keys(pattern)
                if keys:
                    self.redis_client.delete(*keys)
        except Exception as e:
            logger.error(f"Error invalidating user cache: {e}")

class TrafficSplitter:
    """
    Traffic splitting utility for A/B testing.
    
    Provides utilities for managing traffic distribution across variants
    and supports dynamic traffic adjustment.
    """
    
    @staticmethod
    def validate_traffic_split(traffic_split: Dict[str, float]) -> bool:
        """
        Validate traffic split configuration.
        
        Args:
            traffic_split: Traffic distribution
            
        Returns:
            True if valid
        """
        if not traffic_split:
            return False
        
        total_percentage = sum(traffic_split.values())
        return abs(total_percentage - 100.0) < 0.01  # Allow small floating point errors
    
    @staticmethod
    def normalize_traffic_split(traffic_split: Dict[str, float]) -> Dict[str, float]:
        """
        Normalize traffic split to ensure percentages sum to 100.
        
        Args:
            traffic_split: Traffic distribution
            
        Returns:
            Normalized traffic split
        """
        total = sum(traffic_split.values())
        if total == 0:
            return traffic_split
        
        return {variant: (percentage / total) * 100 for variant, percentage in traffic_split.items()}
    
    @staticmethod
    def create_canary_split(base_split: Dict[str, float], canary_percentage: float) -> Dict[str, float]:
        """
        Create traffic split with canary deployment.
        
        Args:
            base_split: Base traffic distribution
            canary_percentage: Percentage for canary variant
            
        Returns:
            Traffic split with canary
        """
        if canary_percentage <= 0 or canary_percentage >= 100:
            return base_split
        
        # Reduce other variants proportionally
        reduction_factor = (100 - canary_percentage) / 100
        
        canary_split = {}
        for variant, percentage in base_split.items():
            canary_split[variant] = percentage * reduction_factor
        
        # Add canary variant
        canary_split["canary"] = canary_percentage
        
        return canary_split
