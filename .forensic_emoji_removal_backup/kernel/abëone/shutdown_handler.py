"""
Shutdown Handler - Graceful Shutdown Handler

Implements graceful shutdown handler for kernel and modules.

Pattern: SHUTDOWN × HANDLER × GRACEFUL × ONE
Philosophy: 80/20 → 97.8% Certainty
"""

from typing import Optional, Callable
import threading
import signal
import sys
from .shutdown_sequence import ShutdownSequence, ShutdownPhase, ShutdownHook


class ShutdownHandler:
    """
    Shutdown Handler.
    
    Responsibilities:
    - Handle shutdown signals
    - Execute graceful shutdown
    - Manage shutdown hooks
    - Handle shutdown timeouts
    """
    
    def __init__(self, shutdown_sequence: Optional[ShutdownSequence] = None):
        """Initialize shutdown handler."""
        self.shutdown_sequence = shutdown_sequence or ShutdownSequence()
        self.shutdown_in_progress: bool = False
        self._lock = threading.Lock()
        self._setup_signal_handlers()
    
    def _setup_signal_handlers(self) -> None:
        """Setup signal handlers for graceful shutdown."""
        signal.signal(signal.SIGINT, self._handle_shutdown_signal)
        signal.signal(signal.SIGTERM, self._handle_shutdown_signal)
    
    def _handle_shutdown_signal(self, signum, frame) -> None:
        """Handle shutdown signal."""
        print(f"\n🛑 Received shutdown signal: {signum}")
        self.shutdown()
    
    def register_shutdown_hook(self, hook_id: str, phase: ShutdownPhase,
                              hook_func: Callable[[], None], timeout: float = 5.0,
                              priority: int = 0) -> bool:
        """
        Register a shutdown hook.
        
        Args:
            hook_id: Hook identifier
            phase: Shutdown phase
            hook_func: Hook function
            timeout: Hook timeout
            priority: Hook priority
        
        Returns:
            True if registration successful
        """
        hook = ShutdownHook(
            hook_id=hook_id,
            phase=phase,
            hook_func=hook_func,
            timeout=timeout,
            priority=priority
        )
        return self.shutdown_sequence.register_hook(hook)
    
    def shutdown(self) -> bool:
        """
        Execute graceful shutdown.
        
        Returns:
            True if shutdown successful
        """
        with self._lock:
            if self.shutdown_in_progress:
                return False
            
            self.shutdown_in_progress = True
        
        print("🔄 Starting graceful shutdown...")
        
        try:
            success = self.shutdown_sequence.execute_shutdown()
            
            if success:
                duration = self.shutdown_sequence.get_shutdown_duration()
                print(f"✅ Graceful shutdown completed in {duration:.2f}s")
            else:
                print("⚠️ Graceful shutdown completed with warnings")
            
            return success
            
        except Exception as e:
            print(f"❌ Shutdown failed: {e}")
            return False
        finally:
            sys.exit(0)
    
    def is_shutdown_in_progress(self) -> bool:
        """
        Check if shutdown is in progress.
        
        Returns:
            True if shutdown is in progress
        """
        with self._lock:
            return self.shutdown_in_progress

