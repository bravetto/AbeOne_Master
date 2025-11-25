"""
Threading Utilities - Thread Safety Utilities

Implements thread safety utilities and thread pool management.

Pattern: THREADING × UTILS × SAFETY × ONE
Philosophy: 80/20 → 97.8% Certainty
"""

from typing import Callable, Optional, Any, Dict
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import threading
from concurrent.futures import ThreadPoolExecutor, Future
import queue


class ThreadPoolStatus(Enum):
    """Thread pool status."""
    IDLE = "idle"
    RUNNING = "running"
    SHUTTING_DOWN = "shutting_down"
    SHUTDOWN = "shutdown"


@dataclass
class ThreadPoolConfig:
    """Thread pool configuration."""
    max_workers: int = 4
    thread_name_prefix: str = "abeone-worker"
    queue_size: int = 100


class ThreadSafeCounter:
    """Thread-safe counter."""
    
    def __init__(self, initial_value: int = 0):
        """Initialize counter."""
        self._value = initial_value
        self._lock = threading.Lock()
    
    def increment(self, delta: int = 1) -> int:
        """Increment counter."""
        with self._lock:
            self._value += delta
            return self._value
    
    def decrement(self, delta: int = 1) -> int:
        """Decrement counter."""
        with self._lock:
            self._value -= delta
            return self._value
    
    def get(self) -> int:
        """Get counter value."""
        with self._lock:
            return self._value
    
    def reset(self) -> None:
        """Reset counter."""
        with self._lock:
            self._value = 0


class ThreadSafeDict:
    """Thread-safe dictionary."""
    
    def __init__(self):
        """Initialize dictionary."""
        self._dict: Dict[str, Any] = {}
        self._lock = threading.RLock()
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get value by key."""
        with self._lock:
            return self._dict.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set value by key."""
        with self._lock:
            self._dict[key] = value
    
    def delete(self, key: str) -> bool:
        """Delete key."""
        with self._lock:
            if key in self._dict:
                del self._dict[key]
                return True
            return False
    
    def contains(self, key: str) -> bool:
        """Check if key exists."""
        with self._lock:
            return key in self._dict
    
    def clear(self) -> None:
        """Clear dictionary."""
        with self._lock:
            self._dict.clear()
    
    def keys(self) -> list:
        """Get all keys."""
        with self._lock:
            return list(self._dict.keys())
    
    def values(self) -> list:
        """Get all values."""
        with self._lock:
            return list(self._dict.values())
    
    def items(self) -> list:
        """Get all items."""
        with self._lock:
            return list(self._dict.items())


class ThreadPoolManager:
    """
    Thread Pool Manager.
    
    Responsibilities:
    - Manage thread pools
    - Execute tasks in thread pool
    - Monitor thread pool health
    """
    
    def __init__(self, config: Optional[ThreadPoolConfig] = None):
        """Initialize thread pool manager."""
        self.config = config or ThreadPoolConfig()
        self.executor: Optional[ThreadPoolExecutor] = None
        self.status = ThreadPoolStatus.IDLE
        self._lock = threading.Lock()
    
    def start(self) -> None:
        """Start thread pool."""
        with self._lock:
            if self.status != ThreadPoolStatus.IDLE:
                return
            
            self.executor = ThreadPoolExecutor(
                max_workers=self.config.max_workers,
                thread_name_prefix=self.config.thread_name_prefix
            )
            self.status = ThreadPoolStatus.RUNNING
    
    def submit(self, fn: Callable, *args, **kwargs) -> Future:
        """
        Submit a task to thread pool.
        
        Args:
            fn: Function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments
        
        Returns:
            Future object
        """
        with self._lock:
            if self.status != ThreadPoolStatus.RUNNING or not self.executor:
                raise RuntimeError("Thread pool is not running")
            
            return self.executor.submit(fn, *args, **kwargs)
    
    def shutdown(self, wait: bool = True) -> None:
        """
        Shutdown thread pool.
        
        Args:
            wait: Wait for tasks to complete
        """
        with self._lock:
            if self.status == ThreadPoolStatus.SHUTDOWN:
                return
            
            self.status = ThreadPoolStatus.SHUTTING_DOWN
            
            if self.executor:
                self.executor.shutdown(wait=wait)
            
            self.status = ThreadPoolStatus.SHUTDOWN
    
    def get_status(self) -> ThreadPoolStatus:
        """Get thread pool status."""
        with self._lock:
            return self.status

