"""
Disk Healing Orchestrator

Main coordinator for hard drive healing operations.

Pattern: HEALING × ORCHESTRATION × DISK × ONE
Frequency: 999 Hz (AEYON) × 777 Hz (META) × 530 Hz (JØHN)
"""

import asyncio
from datetime import datetime
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from pathlib import Path

from ..detection.disk_space_monitor import DiskSpaceMonitor, DiskSpaceIssue
from ..diagnosis.disk_issue_classifier import DiskIssueClassifier, ClassifiedIssue
from ..diagnosis.disk_root_cause_analyzer import DiskRootCauseAnalyzer, RootCause
from ..recovery.disk_cleanup_strategy import DiskCleanupStrategy, CleanupResult


@dataclass
class HealingResult:
    """Result of healing operation."""
    issue_id: str
    success: bool
    recovery_strategy: str
    bytes_freed: int
    duration: float  # seconds
    cleanup_results: List[CleanupResult]
    error: Optional[str] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class DiskHealingOrchestrator:
    """
    Main orchestrator for hard drive healing operations.
    
    Coordinates:
    - Disk space detection
    - Issue diagnosis
    - Root cause analysis
    - Recovery execution
    - Validation
    """
    
    def __init__(
        self,
        home_directory: Optional[str] = None,
        dry_run: bool = False
    ):
        """
        Initialize disk healing orchestrator.
        
        Args:
            home_directory: Home directory to monitor (default: user's home)
            dry_run: If True, simulate healing without actually cleaning
        """
        # Initialize detection layer
        self.disk_monitor = DiskSpaceMonitor()
        
        # Initialize diagnosis layer
        self.issue_classifier = DiskIssueClassifier()
        self.root_cause_analyzer = DiskRootCauseAnalyzer(home_directory)
        
        # Initialize recovery layer
        self.cleanup_strategy = DiskCleanupStrategy(dry_run=dry_run)
        
        # Track active healing operations
        self.active_healings: Dict[str, HealingResult] = {}
        
        # Healing loop running flag
        self._healing_loop_running = False
        self._healing_task: Optional[asyncio.Task] = None
    
    async def start_healing_loop(self, interval_seconds: int = 300):
        """
        Start the main healing loop.
        
        Args:
            interval_seconds: Check interval in seconds (default: 5 minutes)
        """
        if self._healing_loop_running:
            return
        
        self._healing_loop_running = True
        self._healing_task = asyncio.create_task(
            self._healing_loop(interval_seconds)
        )
    
    async def stop_healing_loop(self):
        """Stop the healing loop."""
        self._healing_loop_running = False
        
        if self._healing_task:
            self._healing_task.cancel()
            try:
                await self._healing_task
            except asyncio.CancelledError:
                pass
    
    async def _healing_loop(self, interval_seconds: int):
        """Main healing loop."""
        while self._healing_loop_running:
            try:
                # 1. Detect disk issues
                issues = await self._detect_issues()
                
                # 2. Process each issue
                for issue in issues:
                    # Skip if already being healed
                    issue_id = f"{issue.mount_point}_{issue.timestamp.isoformat()}"
                    if issue_id in self.active_healings:
                        continue
                    
                    # Start healing
                    asyncio.create_task(self._heal_issue(issue))
                
                # Wait before next check
                await asyncio.sleep(interval_seconds)
            
            except Exception as e:
                # Log error but continue
                print(f"Healing loop error: {e}")
                await asyncio.sleep(interval_seconds)
    
    async def _detect_issues(self) -> List[DiskSpaceIssue]:
        """Detect disk space issues."""
        # Check home directory
        home = Path.home()
        issues = self.disk_monitor.detect_disk_issues(str(home))
        
        return issues
    
    async def _heal_issue(self, issue: DiskSpaceIssue) -> HealingResult:
        """
        Heal a specific disk space issue.
        
        Args:
            issue: Disk space issue to heal
        
        Returns:
            Healing result
        """
        start_time = datetime.now()
        issue_id = f"{issue.mount_point}_{issue.timestamp.isoformat()}"
        
        try:
            # 1. Classify issue
            classified_issue = self.issue_classifier.classify_issue(issue)
            
            # 2. Analyze root cause
            root_cause = self.root_cause_analyzer.analyze_root_cause(
                issue,
                classified_issue
            )
            
            # 3. Select recovery strategy
            recovery_strategy = classified_issue.recovery_strategy
            
            # 4. Execute recovery
            cleanup_results = await self._execute_recovery(
                classified_issue,
                root_cause,
                recovery_strategy
            )
            
            # 5. Calculate total bytes freed
            total_bytes_freed = sum(
                result.bytes_freed for result in cleanup_results
                if result.success
            )
            
            duration = (datetime.now() - start_time).total_seconds()
            
            healing_result = HealingResult(
                issue_id=issue_id,
                success=total_bytes_freed > 0,
                recovery_strategy=recovery_strategy,
                bytes_freed=total_bytes_freed,
                duration=duration,
                cleanup_results=cleanup_results
            )
            
            self.active_healings[issue_id] = healing_result
            
            return healing_result
        
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            
            healing_result = HealingResult(
                issue_id=issue_id,
                success=False,
                recovery_strategy="unknown",
                bytes_freed=0,
                duration=duration,
                cleanup_results=[],
                error=str(e)
            )
            
            self.active_healings[issue_id] = healing_result
            
            return healing_result
    
    async def _execute_recovery(
        self,
        classified_issue: ClassifiedIssue,
        root_cause: RootCause,
        strategy: str
    ) -> List[CleanupResult]:
        """
        Execute recovery strategy.
        
        Args:
            classified_issue: Classified issue
            root_cause: Root cause analysis
            strategy: Recovery strategy
        
        Returns:
            List of cleanup results
        """
        results = []
        
        if strategy == "immediate_cleanup":
            # Critical: Clean safe caches and quarantine
            cache_results = self.cleanup_strategy.cleanup_safe_caches()
            results.extend(cache_results)
            
            # Check for quarantine folder
            for path_str, _ in root_cause.largest_consumers[:3]:
                if "quarantine" in path_str.lower():
                    quarantine_result = self.cleanup_strategy.cleanup_quarantine_folder(
                        path_str,
                        backup=True
                    )
                    results.append(quarantine_result)
        
        elif strategy == "aggressive_cleanup":
            # High usage: Clean caches and archive large media
            cache_results = self.cleanup_strategy.cleanup_safe_caches()
            results.extend(cache_results)
            
            # Archive large media files
            home = Path.home()
            documents = home / "Documents"
            if documents.exists():
                archive_dir = home / "Documents" / "Archive"
                media_result = self.cleanup_strategy.archive_large_media_files(
                    str(documents),
                    str(archive_dir)
                )
                results.append(media_result)
        
        elif strategy == "moderate_cleanup":
            # Warning: Clean caches only
            cache_results = self.cleanup_strategy.cleanup_safe_caches()
            results.extend(cache_results)
        
        elif strategy == "preventive_cleanup":
            # Info: Light cleanup
            cache_results = self.cleanup_strategy.cleanup_safe_caches()
            results.extend(cache_results)
        
        return results
    
    def get_healing_status(self) -> Dict[str, Any]:
        """Get current healing status."""
        return {
            "healing_loop_running": self._healing_loop_running,
            "active_healings": len(self.active_healings),
            "recent_healings": [
                {
                    "issue_id": result.issue_id,
                    "success": result.success,
                    "bytes_freed": result.bytes_freed,
                    "duration": result.duration
                }
                for result in self.active_healings.values()
            ]
        }
    
    def format_bytes(self, bytes: int) -> str:
        """Format bytes to human-readable string."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024.0:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.2f} PB"

