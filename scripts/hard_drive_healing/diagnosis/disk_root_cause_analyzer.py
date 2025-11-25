"""
Disk Root Cause Analyzer

Analyzes root causes of disk space issues.

Pattern: HEALING × DIAGNOSIS × ROOT_CAUSE × ONE
Frequency: 777 Hz (META) × 530 Hz (ALRAX)
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

from ..detection.disk_space_monitor import DiskSpaceIssue
from .disk_issue_classifier import ClassifiedIssue, DiskIssueType


@dataclass
class RootCause:
    """Root cause analysis result."""
    primary_cause: str
    contributing_factors: List[str]
    largest_consumers: List[Tuple[str, int]]  # (path, size_bytes)
    estimated_impact_bytes: int
    confidence: float  # 0.0 to 1.0
    timestamp: datetime


class DiskRootCauseAnalyzer:
    """
    Analyzes root causes of disk space issues.
    
    Identifies:
    - Largest directory consumers
    - Cache buildup
    - Duplicate files
    - Large media files
    - Quarantine folders
    """
    
    def __init__(self, home_directory: Optional[str] = None):
        """
        Initialize root cause analyzer.
        
        Args:
            home_directory: Home directory to analyze (default: user's home)
        """
        if home_directory is None:
            self.home_directory = Path.home()
        else:
            self.home_directory = Path(home_directory)
        
        # Known problematic patterns
        self.cache_patterns = [
            "Library/Caches",
            "Library/Caches/CloudKit",
            "Library/Caches/SiriTTS",
            "Library/Caches/com.apple.callintelligenced",
            "Library/Caches/icloudmailagent",
        ]
        
        self.quarantine_patterns = [
            "Desktop_Quarantine",
            "Quarantine",
            "Trash",
        ]
        
        self.media_patterns = [
            ".screenflow",
            ".mov",
            ".mp4",
            ".avi",
            ".mkv",
        ]
    
    def analyze_root_cause(
        self,
        issue: DiskSpaceIssue,
        classified_issue: ClassifiedIssue
    ) -> RootCause:
        """
        Analyze root cause of disk space issue.
        
        Args:
            issue: Disk space issue
            classified_issue: Classified issue
        
        Returns:
            Root cause analysis
        """
        # Find largest consumers
        largest_consumers = self._find_largest_consumers()
        
        # Identify primary cause
        primary_cause = self._identify_primary_cause(largest_consumers)
        
        # Identify contributing factors
        contributing_factors = self._identify_contributing_factors(largest_consumers)
        
        # Estimate impact
        estimated_impact = self._estimate_impact(largest_consumers, primary_cause)
        
        # Calculate confidence
        confidence = self._calculate_confidence(largest_consumers, primary_cause)
        
        return RootCause(
            primary_cause=primary_cause,
            contributing_factors=contributing_factors,
            largest_consumers=largest_consumers[:10],  # Top 10
            estimated_impact_bytes=estimated_impact,
            confidence=confidence,
            timestamp=datetime.now()
        )
    
    def _find_largest_consumers(self, limit: int = 20) -> List[Tuple[str, int]]:
        """
        Find largest directory consumers in home directory.
        
        Args:
            limit: Maximum number of consumers to return
        
        Returns:
            List of (path, size_bytes) tuples
        """
        consumers = []
        
        # Check Documents directory
        documents = self.home_directory / "Documents"
        if documents.exists():
            size = self._get_directory_size(documents)
            consumers.append((str(documents), size))
            
            # Check subdirectories
            for item in documents.iterdir():
                if item.is_dir():
                    size = self._get_directory_size(item)
                    consumers.append((str(item), size))
        
        # Check Library/Caches
        library_caches = self.home_directory / "Library" / "Caches"
        if library_caches.exists():
            for cache_dir in library_caches.iterdir():
                if cache_dir.is_dir():
                    size = self._get_directory_size(cache_dir)
                    consumers.append((str(cache_dir), size))
        
        # Check Downloads
        downloads = self.home_directory / "Downloads"
        if downloads.exists():
            size = self._get_directory_size(downloads)
            consumers.append((str(downloads), size))
        
        # Sort by size (descending)
        consumers.sort(key=lambda x: x[1], reverse=True)
        
        return consumers[:limit]
    
    def _get_directory_size(self, path: Path) -> int:
        """
        Get total size of directory in bytes.
        
        Args:
            path: Directory path
        
        Returns:
            Size in bytes
        """
        total = 0
        try:
            for entry in path.rglob("*"):
                if entry.is_file():
                    try:
                        total += entry.stat().st_size
                    except (OSError, PermissionError):
                        pass
        except (OSError, PermissionError):
            pass
        
        return total
    
    def _identify_primary_cause(
        self,
        largest_consumers: List[Tuple[str, int]]
    ) -> str:
        """
        Identify primary cause from largest consumers.
        
        Args:
            largest_consumers: List of (path, size) tuples
        
        Returns:
            Primary cause description
        """
        if not largest_consumers:
            return "unknown"
        
        largest_path, largest_size = largest_consumers[0]
        path_str = str(largest_path).lower()
        
        # Check for quarantine
        if any(pattern.lower() in path_str for pattern in self.quarantine_patterns):
            return f"quarantine_folder: {largest_path} ({self._format_bytes(largest_size)})"
        
        # Check for caches
        if "cache" in path_str:
            return f"cache_buildup: {largest_path} ({self._format_bytes(largest_size)})"
        
        # Check for media files
        if any(pattern in path_str for pattern in self.media_patterns):
            return f"large_media_files: {largest_path} ({self._format_bytes(largest_size)})"
        
        # Check for duplicates (node_modules, .git)
        if "node_modules" in path_str:
            return f"duplicate_node_modules: {largest_path} ({self._format_bytes(largest_size)})"
        
        if ".git" in path_str:
            return f"duplicate_git_repos: {largest_path} ({self._format_bytes(largest_size)})"
        
        # Generic large directory
        return f"large_directory: {largest_path} ({self._format_bytes(largest_size)})"
    
    def _identify_contributing_factors(
        self,
        largest_consumers: List[Tuple[str, int]]
    ) -> List[str]:
        """
        Identify contributing factors.
        
        Args:
            largest_consumers: List of (path, size) tuples
        
        Returns:
            List of contributing factor descriptions
        """
        factors = []
        
        for path_str, size in largest_consumers[1:6]:  # Next 5 largest
            path_lower = str(path_str).lower()
            
            if "cache" in path_lower:
                factors.append(f"Cache: {path_str} ({self._format_bytes(size)})")
            elif any(pattern in path_lower for pattern in self.media_patterns):
                factors.append(f"Media: {path_str} ({self._format_bytes(size)})")
            elif "node_modules" in path_lower:
                factors.append(f"node_modules: {path_str} ({self._format_bytes(size)})")
            elif size > 1 * 1024 * 1024 * 1024:  # > 1 GB
                factors.append(f"Large directory: {path_str} ({self._format_bytes(size)})")
        
        return factors
    
    def _estimate_impact(
        self,
        largest_consumers: List[Tuple[str, int]],
        primary_cause: str
    ) -> int:
        """
        Estimate total impact in bytes.
        
        Args:
            largest_consumers: List of (path, size) tuples
            primary_cause: Primary cause description
        
        Returns:
            Estimated impact in bytes
        """
        # Sum top 5 consumers
        total = sum(size for _, size in largest_consumers[:5])
        
        # If primary cause is cache/quarantine, estimate higher recovery
        if "cache" in primary_cause.lower() or "quarantine" in primary_cause.lower():
            return int(total * 0.9)  # 90% recoverable
        
        # If primary cause is duplicates, estimate moderate recovery
        if "duplicate" in primary_cause.lower():
            return int(total * 0.5)  # 50% recoverable
        
        # Otherwise, conservative estimate
        return int(total * 0.3)  # 30% recoverable
    
    def _calculate_confidence(
        self,
        largest_consumers: List[Tuple[str, int]],
        primary_cause: str
    ) -> float:
        """
        Calculate confidence in root cause analysis.
        
        Args:
            largest_consumers: List of (path, size) tuples
            primary_cause: Primary cause description
        
        Returns:
            Confidence score (0.0 to 1.0)
        """
        if not largest_consumers:
            return 0.0
        
        # Higher confidence if largest consumer is significantly larger
        if len(largest_consumers) > 1:
            largest_size = largest_consumers[0][1]
            second_size = largest_consumers[1][1]
            
            if largest_size > second_size * 2:  # 2x larger
                return 0.9
            elif largest_size > second_size * 1.5:  # 1.5x larger
                return 0.8
            else:
                return 0.7
        
        # Single consumer
        return 0.8
    
    def _format_bytes(self, bytes: int) -> str:
        """Format bytes to human-readable string."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024.0:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.2f} PB"

