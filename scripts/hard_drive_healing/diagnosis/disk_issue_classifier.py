"""
Disk Issue Classifier

Classifies disk space issues by type and severity.

Pattern: HEALING × DIAGNOSIS × CLASSIFICATION × ONE
Frequency: 777 Hz (META) × 530 Hz (Truth)
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from ..detection.disk_space_monitor import DiskSpaceIssue


class DiskIssueType(Enum):
    """Types of disk issues."""
    CRITICAL_SPACE = "critical_space"  # < 10 GB free
    HIGH_USAGE = "high_usage"  # > 90% used
    WARNING_USAGE = "warning_usage"  # > 80% used
    INFO_USAGE = "info_usage"  # > 70% used
    CACHE_BUILDUP = "cache_buildup"  # Large cache directories
    DUPLICATE_FILES = "duplicate_files"  # Duplicate files consuming space
    LARGE_MEDIA = "large_media"  # Large media files
    QUARANTINE_FILES = "quarantine_files"  # Quarantine folders


@dataclass
class ClassifiedIssue:
    """Classified disk issue."""
    issue_type: DiskIssueType
    severity: str  # "critical", "warning", "info"
    mount_point: str
    usage_percent: float
    free_bytes: int
    estimated_recovery_bytes: int
    recovery_strategy: str
    timestamp: datetime
    original_issue: DiskSpaceIssue


class DiskIssueClassifier:
    """
    Classifies disk space issues by type and severity.
    
    Classification logic:
    - Critical space (< 10 GB free) → CRITICAL_SPACE
    - High usage (> 90%) → HIGH_USAGE
    - Warning usage (> 80%) → WARNING_USAGE
    - Info usage (> 70%) → INFO_USAGE
    """
    
    def __init__(self):
        """Initialize disk issue classifier."""
        pass
    
    def classify_issue(self, issue: DiskSpaceIssue) -> ClassifiedIssue:
        """
        Classify a disk space issue.
        
        Args:
            issue: Disk space issue to classify
        
        Returns:
            Classified issue
        """
        # Determine issue type based on severity and thresholds
        if issue.severity == "critical":
            if issue.free_bytes < 10 * 1024 * 1024 * 1024:  # < 10 GB
                issue_type = DiskIssueType.CRITICAL_SPACE
                estimated_recovery = self._estimate_critical_recovery(issue)
                recovery_strategy = "immediate_cleanup"
            else:
                issue_type = DiskIssueType.HIGH_USAGE
                estimated_recovery = self._estimate_high_usage_recovery(issue)
                recovery_strategy = "aggressive_cleanup"
        elif issue.severity == "warning":
            issue_type = DiskIssueType.WARNING_USAGE
            estimated_recovery = self._estimate_warning_recovery(issue)
            recovery_strategy = "moderate_cleanup"
        else:
            issue_type = DiskIssueType.INFO_USAGE
            estimated_recovery = self._estimate_info_recovery(issue)
            recovery_strategy = "preventive_cleanup"
        
        return ClassifiedIssue(
            issue_type=issue_type,
            severity=issue.severity,
            mount_point=issue.mount_point,
            usage_percent=issue.usage_percent,
            free_bytes=issue.free_bytes,
            estimated_recovery_bytes=estimated_recovery,
            recovery_strategy=recovery_strategy,
            timestamp=datetime.now(),
            original_issue=issue
        )
    
    def _estimate_critical_recovery(self, issue: DiskSpaceIssue) -> int:
        """Estimate recovery potential for critical issues."""
        # Critical issues: estimate 50-100 GB recovery potential
        # Based on typical cleanup: caches, temp files, duplicates
        return 50 * 1024 * 1024 * 1024  # 50 GB estimate
    
    def _estimate_high_usage_recovery(self, issue: DiskSpaceIssue) -> int:
        """Estimate recovery potential for high usage issues."""
        # High usage: estimate 30-50 GB recovery potential
        return 30 * 1024 * 1024 * 1024  # 30 GB estimate
    
    def _estimate_warning_recovery(self, issue: DiskSpaceIssue) -> int:
        """Estimate recovery potential for warning issues."""
        # Warning: estimate 10-30 GB recovery potential
        return 10 * 1024 * 1024 * 1024  # 10 GB estimate
    
    def _estimate_info_recovery(self, issue: DiskSpaceIssue) -> int:
        """Estimate recovery potential for info issues."""
        # Info: estimate 5-10 GB recovery potential
        return 5 * 1024 * 1024 * 1024  # 5 GB estimate

