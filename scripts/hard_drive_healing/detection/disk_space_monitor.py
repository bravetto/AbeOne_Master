"""
Disk Space Monitor

Monitors disk space utilization and detects critical thresholds.

Pattern: HEALING × DETECTION × DISK × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (Truth)
"""

import shutil
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from collections import deque


@dataclass
class DiskMetric:
    """Disk space metric."""
    mount_point: str
    timestamp: datetime
    total_bytes: int
    used_bytes: int
    free_bytes: int
    usage_percent: float


@dataclass
class DiskSpaceIssue:
    """Detected disk space issue."""
    mount_point: str
    usage_percent: float
    free_bytes: int
    threshold_percent: float
    threshold_bytes: int
    severity: str  # "critical", "warning", "info"
    timestamp: datetime


class DiskSpaceMonitor:
    """
    Monitors disk space and detects critical thresholds.
    
    Detects issues when:
    - Free space < 10 GB (critical)
    - Usage > 90% (critical)
    - Usage > 80% (warning)
    - Usage > 70% (info)
    """
    
    def __init__(
        self,
        critical_threshold_percent: float = 90.0,
        warning_threshold_percent: float = 80.0,
        info_threshold_percent: float = 70.0,
        critical_threshold_bytes: int = 10 * 1024 * 1024 * 1024,  # 10 GB
        warning_threshold_bytes: int = 20 * 1024 * 1024 * 1024,  # 20 GB
    ):
        """
        Initialize disk space monitor.
        
        Args:
            critical_threshold_percent: Critical usage threshold (percent)
            warning_threshold_percent: Warning usage threshold (percent)
            info_threshold_percent: Info usage threshold (percent)
            critical_threshold_bytes: Critical free space threshold (bytes)
            warning_threshold_bytes: Warning free space threshold (bytes)
        """
        self.critical_threshold_percent = critical_threshold_percent
        self.warning_threshold_percent = warning_threshold_percent
        self.info_threshold_percent = info_threshold_percent
        self.critical_threshold_bytes = critical_threshold_bytes
        self.warning_threshold_bytes = warning_threshold_bytes
        
        # Store disk metrics (sliding window)
        self.disk_metrics: Dict[str, deque] = {}
    
    def get_disk_usage(self, path: str = "/") -> DiskMetric:
        """
        Get current disk usage for a mount point.
        
        Args:
            path: Path to check (default: root)
        
        Returns:
            Disk metric
        """
        stat = shutil.disk_usage(path)
        
        total_bytes = stat.total
        used_bytes = stat.used
        free_bytes = stat.free
        usage_percent = (used_bytes / total_bytes) * 100.0
        
        return DiskMetric(
            mount_point=path,
            timestamp=datetime.now(),
            total_bytes=total_bytes,
            used_bytes=used_bytes,
            free_bytes=free_bytes,
            usage_percent=usage_percent
        )
    
    def record_disk_usage(self, path: str = "/"):
        """Record disk usage for a mount point."""
        metric = self.get_disk_usage(path)
        
        if path not in self.disk_metrics:
            self.disk_metrics[path] = deque(maxlen=1000)  # Max 1000 metrics
        
        self.disk_metrics[path].append(metric)
    
    def detect_disk_issues(self, path: str = "/") -> List[DiskSpaceIssue]:
        """
        Detect disk space issues for a mount point.
        
        Args:
            path: Path to check (default: root)
        
        Returns:
            List of detected disk space issues
        """
        issues = []
        
        # Get current usage
        metric = self.get_disk_usage(path)
        
        # Check critical threshold (free space)
        if metric.free_bytes < self.critical_threshold_bytes:
            issues.append(DiskSpaceIssue(
                mount_point=path,
                usage_percent=metric.usage_percent,
                free_bytes=metric.free_bytes,
                threshold_percent=self.critical_threshold_percent,
                threshold_bytes=self.critical_threshold_bytes,
                severity="critical",
                timestamp=datetime.now()
            ))
        
        # Check critical threshold (usage percent)
        elif metric.usage_percent >= self.critical_threshold_percent:
            issues.append(DiskSpaceIssue(
                mount_point=path,
                usage_percent=metric.usage_percent,
                free_bytes=metric.free_bytes,
                threshold_percent=self.critical_threshold_percent,
                threshold_bytes=self.critical_threshold_bytes,
                severity="critical",
                timestamp=datetime.now()
            ))
        
        # Check warning threshold
        elif metric.usage_percent >= self.warning_threshold_percent:
            issues.append(DiskSpaceIssue(
                mount_point=path,
                usage_percent=metric.usage_percent,
                free_bytes=metric.free_bytes,
                threshold_percent=self.warning_threshold_percent,
                threshold_bytes=self.warning_threshold_bytes,
                severity="warning",
                timestamp=datetime.now()
            ))
        
        # Check info threshold
        elif metric.usage_percent >= self.info_threshold_percent:
            issues.append(DiskSpaceIssue(
                mount_point=path,
                usage_percent=metric.usage_percent,
                free_bytes=metric.free_bytes,
                threshold_percent=self.info_threshold_percent,
                threshold_bytes=self.warning_threshold_bytes,
                severity="info",
                timestamp=datetime.now()
            ))
        
        return issues
    
    def get_home_directory_usage(self) -> DiskMetric:
        """Get disk usage for home directory."""
        home = Path.home()
        return self.get_disk_usage(str(home))
    
    def format_bytes(self, bytes: int) -> str:
        """Format bytes to human-readable string."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024.0:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.2f} PB"
    
    def get_current_usage(self, path: str = "/") -> Optional[DiskMetric]:
        """Get most recent disk usage for a mount point."""
        if path not in self.disk_metrics or not self.disk_metrics[path]:
            return self.get_disk_usage(path)
        
        return self.disk_metrics[path][-1]

