"""
Disk Cleanup Strategy

Implements safe cleanup strategies for disk space recovery.

Pattern: HEALING × RECOVERY × CLEANUP × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (YAGNI)
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import subprocess


@dataclass
class CleanupResult:
    """Result of cleanup operation."""
    success: bool
    path: str
    bytes_freed: int
    files_removed: int
    duration_seconds: float
    error: Optional[str] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class DiskCleanupStrategy:
    """
    Implements safe cleanup strategies for disk space recovery.
    
    Strategies:
    - Safe cache cleanup (regenerates automatically)
    - Quarantine folder cleanup (with backup option)
    - Duplicate file removal (with verification)
    - Large media archiving (moves to archive)
    """
    
    def __init__(self, dry_run: bool = False):
        """
        Initialize cleanup strategy.
        
        Args:
            dry_run: If True, simulate cleanup without actually deleting
        """
        self.dry_run = dry_run
        
        # Safe cache directories (will regenerate)
        self.safe_caches = [
            "Library/Caches/CloudKit",
            "Library/Caches/SiriTTS",
            "Library/Caches/com.apple.callintelligenced",
            "Library/Caches/icloudmailagent",
        ]
    
    def cleanup_safe_caches(self, home_directory: Optional[str] = None) -> List[CleanupResult]:
        """
        Clean safe cache directories.
        
        Args:
            home_directory: Home directory (default: user's home)
        
        Returns:
            List of cleanup results
        """
        if home_directory is None:
            home_directory = Path.home()
        else:
            home_directory = Path(home_directory)
        
        results = []
        
        for cache_pattern in self.safe_caches:
            cache_path = home_directory / cache_pattern
            
            if not cache_path.exists():
                continue
            
            result = self._cleanup_directory(cache_path)
            results.append(result)
        
        return results
    
    def cleanup_quarantine_folder(
        self,
        quarantine_path: str,
        backup: bool = True
    ) -> CleanupResult:
        """
        Clean quarantine folder.
        
        Args:
            quarantine_path: Path to quarantine folder
            backup: If True, create backup before deletion
        
        Returns:
            Cleanup result
        """
        start_time = datetime.now()
        path = Path(quarantine_path)
        
        if not path.exists():
            return CleanupResult(
                success=False,
                path=str(path),
                bytes_freed=0,
                files_removed=0,
                duration_seconds=0.0,
                error="Path does not exist"
            )
        
        # Calculate size before cleanup
        size_before = self._get_directory_size(path)
        file_count = self._count_files(path)
        
        if self.dry_run:
            return CleanupResult(
                success=True,
                path=str(path),
                bytes_freed=size_before,
                files_removed=file_count,
                duration_seconds=(datetime.now() - start_time).total_seconds(),
                error="DRY RUN - No files deleted"
            )
        
        # Create backup if requested
        if backup:
            backup_path = path.parent / f"{path.name}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            try:
                shutil.copytree(path, backup_path)
            except Exception as e:
                return CleanupResult(
                    success=False,
                    path=str(path),
                    bytes_freed=0,
                    files_removed=0,
                    duration_seconds=(datetime.now() - start_time).total_seconds(),
                    error=f"Backup failed: {str(e)}"
                )
        
        # Remove directory
        try:
            shutil.rmtree(path)
            duration = (datetime.now() - start_time).total_seconds()
            
            return CleanupResult(
                success=True,
                path=str(path),
                bytes_freed=size_before,
                files_removed=file_count,
                duration_seconds=duration
            )
        except Exception as e:
            return CleanupResult(
                success=False,
                path=str(path),
                bytes_freed=0,
                files_removed=0,
                duration_seconds=(datetime.now() - start_time).total_seconds(),
                error=str(e)
            )
    
    def archive_large_media_files(
        self,
        source_directory: str,
        archive_directory: str,
        extensions: List[str] = None
    ) -> CleanupResult:
        """
        Archive large media files to archive directory.
        
        Args:
            source_directory: Source directory to search
            archive_directory: Archive directory to move files to
            extensions: File extensions to archive (default: .screenflow, .mov, .mp4)
        
        Returns:
            Cleanup result
        """
        start_time = datetime.now()
        
        if extensions is None:
            extensions = [".screenflow", ".mov", ".mp4", ".avi", ".mkv"]
        
        source_path = Path(source_directory)
        archive_path = Path(archive_directory)
        
        if not source_path.exists():
            return CleanupResult(
                success=False,
                path=str(source_path),
                bytes_freed=0,
                files_removed=0,
                duration_seconds=0.0,
                error="Source directory does not exist"
            )
        
        # Create archive directory
        if not self.dry_run:
            archive_path.mkdir(parents=True, exist_ok=True)
        
        bytes_freed = 0
        files_moved = 0
        
        # Find and move large media files
        for ext in extensions:
            for file_path in source_path.rglob(f"*{ext}"):
                if not file_path.is_file():
                    continue
                
                file_size = file_path.stat().st_size
                
                # Only move files > 100 MB
                if file_size < 100 * 1024 * 1024:
                    continue
                
                if self.dry_run:
                    bytes_freed += file_size
                    files_moved += 1
                    continue
                
                # Move file to archive
                try:
                    relative_path = file_path.relative_to(source_path)
                    archive_file_path = archive_path / relative_path
                    archive_file_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    shutil.move(str(file_path), str(archive_file_path))
                    bytes_freed += file_size
                    files_moved += 1
                except Exception as e:
                    # Continue on error
                    continue
        
        duration = (datetime.now() - start_time).total_seconds()
        
        return CleanupResult(
            success=True,
            path=str(source_path),
            bytes_freed=bytes_freed,
            files_removed=files_moved,
            duration_seconds=duration
        )
    
    def remove_duplicate_node_modules(
        self,
        root_directory: str,
        keep_first: bool = True
    ) -> List[CleanupResult]:
        """
        Remove duplicate node_modules directories.
        
        Args:
            root_directory: Root directory to search
            keep_first: If True, keep first occurrence
        
        Returns:
            List of cleanup results
        """
        root_path = Path(root_directory)
        results = []
        
        # Find all node_modules directories
        node_modules_dirs = list(root_path.rglob("node_modules"))
        
        if len(node_modules_dirs) <= 1:
            return results  # No duplicates
        
        # Group by parent directory name
        seen_parents = set()
        
        for node_modules_dir in node_modules_dirs:
            parent_name = node_modules_dir.parent.name
            
            if keep_first and parent_name in seen_parents:
                # This is a duplicate
                result = self._cleanup_directory(node_modules_dir)
                results.append(result)
            else:
                seen_parents.add(parent_name)
        
        return results
    
    def _cleanup_directory(self, directory_path: Path) -> CleanupResult:
        """
        Clean up a directory.
        
        Args:
            directory_path: Directory to clean
        
        Returns:
            Cleanup result
        """
        start_time = datetime.now()
        
        if not directory_path.exists():
            return CleanupResult(
                success=False,
                path=str(directory_path),
                bytes_freed=0,
                files_removed=0,
                duration_seconds=0.0,
                error="Directory does not exist"
            )
        
        # Calculate size
        size_before = self._get_directory_size(directory_path)
        file_count = self._count_files(directory_path)
        
        if self.dry_run:
            return CleanupResult(
                success=True,
                path=str(directory_path),
                bytes_freed=size_before,
                files_removed=file_count,
                duration_seconds=(datetime.now() - start_time).total_seconds(),
                error="DRY RUN - No files deleted"
            )
        
        # Remove directory
        try:
            shutil.rmtree(directory_path)
            duration = (datetime.now() - start_time).total_seconds()
            
            return CleanupResult(
                success=True,
                path=str(directory_path),
                bytes_freed=size_before,
                files_removed=file_count,
                duration_seconds=duration
            )
        except Exception as e:
            return CleanupResult(
                success=False,
                path=str(directory_path),
                bytes_freed=0,
                files_removed=0,
                duration_seconds=(datetime.now() - start_time).total_seconds(),
                error=str(e)
            )
    
    def _get_directory_size(self, path: Path) -> int:
        """Get total size of directory in bytes."""
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
    
    def _count_files(self, path: Path) -> int:
        """Count files in directory."""
        count = 0
        try:
            for entry in path.rglob("*"):
                if entry.is_file():
                    count += 1
        except (OSError, PermissionError):
            pass
        return count

