"""
Trust Guard Tracer Bullets

Provides debugging and performance monitoring capabilities with tracer bullets
for tracking execution flow, performance bottlenecks, and system behavior.
"""

import time
import functools
import logging
import threading
from typing import Any, Dict, List, Optional, Callable, Union
from contextlib import contextmanager
from dataclasses import dataclass, field
from collections import defaultdict, deque
import json

logger = logging.getLogger(__name__)


@dataclass
class TracerBullet:
    """Represents a single tracer bullet event."""
    timestamp: float
    event_type: str
    message: str
    data: Dict[str, Any] = field(default_factory=dict)
    thread_id: int = field(default_factory=lambda: threading.get_ident())
    duration: Optional[float] = None
    parent_id: Optional[str] = None
    bullet_id: str = field(default_factory=lambda: f"bullet_{int(time.time() * 1000000)}")


class TracerManager:
    """Manages tracer bullets and provides debugging capabilities."""
    
    def __init__(self, max_bullets: int = 10000, enable_performance_tracking: bool = True):
        self.max_bullets = max_bullets
        self.enable_performance_tracking = enable_performance_tracking
        self.bullets: deque = deque(maxlen=max_bullets)
        self.active_traces: Dict[str, Dict[str, Any]] = {}
        self.performance_metrics: Dict[str, List[float]] = defaultdict(lambda: deque(maxlen=1000))
        self.lock = threading.Lock()
        
        # Performance tracking settings
        self.slow_operation_threshold = 1.0  # seconds
        self.memory_usage_threshold = 100 * 1024 * 1024  # 100MB
        
        logger.info("TracerManager initialized", extra={
            "max_bullets": max_bullets,
            "performance_tracking": enable_performance_tracking
        })
    
    def fire_bullet(self, event_type: str, message: str, **data) -> TracerBullet:
        """Fire a tracer bullet with the given event type and message."""
        bullet = TracerBullet(
            timestamp=time.time(),
            event_type=event_type,
            message=message,
            data=data
        )
        
        with self.lock:
            self.bullets.append(bullet)
        
        # Log the bullet
        logger.debug(f"Tracer bullet fired: {event_type} - {message}", extra={
            "bullet_id": bullet.bullet_id,
            "event_type": event_type,
            "data": data
        })
        
        return bullet
    
    def start_trace(self, trace_id: str, operation: str, **metadata) -> str:
        """Start a new trace operation."""
        start_time = time.time()
        
        with self.lock:
            self.active_traces[trace_id] = {
                "operation": operation,
                "start_time": start_time,
                "metadata": metadata,
                "bullets": []
            }
        
        self.fire_bullet("trace_start", f"Started trace: {operation}", 
                        trace_id=trace_id, operation=operation, **metadata)
        
        return trace_id
    
    def end_trace(self, trace_id: str, success: bool = True, **result_data) -> Optional[Dict[str, Any]]:
        """End a trace operation and return performance metrics."""
        end_time = time.time()
        
        with self.lock:
            if trace_id not in self.active_traces:
                logger.warning(f"Attempted to end non-existent trace: {trace_id}")
                return None
            
            trace_info = self.active_traces.pop(trace_id)
            duration = end_time - trace_info["start_time"]
            
            # Record performance metrics
            if self.enable_performance_tracking:
                self.performance_metrics[trace_info["operation"]].append(duration)
                
                # Check for slow operations
                if duration > self.slow_operation_threshold:
                    self.fire_bullet("slow_operation", 
                                   f"Slow operation detected: {trace_info['operation']}",
                                   operation=trace_info["operation"],
                                   duration=duration,
                                   threshold=self.slow_operation_threshold)
            
            # Fire end bullet
            self.fire_bullet("trace_end", f"Ended trace: {trace_info['operation']}",
                           trace_id=trace_id,
                           operation=trace_info["operation"],
                           duration=duration,
                           success=success,
                           **result_data)
            
            return {
                "trace_id": trace_id,
                "operation": trace_info["operation"],
                "duration": duration,
                "success": success,
                "metadata": trace_info["metadata"],
                "result_data": result_data
            }
    
    def add_bullet_to_trace(self, trace_id: str, event_type: str, message: str, **data):
        """Add a bullet to an active trace."""
        bullet = self.fire_bullet(event_type, message, trace_id=trace_id, **data)
        
        with self.lock:
            if trace_id in self.active_traces:
                self.active_traces[trace_id]["bullets"].append(bullet.bullet_id)
        
        return bullet
    
    def get_trace_summary(self, trace_id: str) -> Optional[Dict[str, Any]]:
        """Get summary information for a specific trace."""
        with self.lock:
            if trace_id not in self.active_traces:
                return None
            
            trace_info = self.active_traces[trace_id]
            return {
                "trace_id": trace_id,
                "operation": trace_info["operation"],
                "start_time": trace_info["start_time"],
                "duration": time.time() - trace_info["start_time"],
                "bullet_count": len(trace_info["bullets"]),
                "metadata": trace_info["metadata"]
            }
    
    def get_performance_metrics(self, operation: Optional[str] = None) -> Dict[str, Any]:
        """Get performance metrics for operations."""
        with self.lock:
            if operation:
                if operation not in self.performance_metrics:
                    return {}
                
                durations = self.performance_metrics[operation]
                return {
                    "operation": operation,
                    "count": len(durations),
                    "avg_duration": sum(durations) / len(durations) if durations else 0,
                    "min_duration": min(durations) if durations else 0,
                    "max_duration": max(durations) if durations else 0,
                    "total_duration": sum(durations)
                }
            else:
                # Return metrics for all operations
                all_metrics = {}
                for op, durations in self.performance_metrics.items():
                    all_metrics[op] = {
                        "count": len(durations),
                        "avg_duration": sum(durations) / len(durations) if durations else 0,
                        "min_duration": min(durations) if durations else 0,
                        "max_duration": max(durations) if durations else 0,
                        "total_duration": sum(durations)
                    }
                return all_metrics
    
    def get_recent_bullets(self, count: int = 100, event_type: Optional[str] = None) -> List[TracerBullet]:
        """Get recent tracer bullets."""
        with self.lock:
            bullets = list(self.bullets)
            
            if event_type:
                bullets = [b for b in bullets if b.event_type == event_type]
            
            return bullets[-count:]
    
    def get_bullets_by_trace(self, trace_id: str) -> List[TracerBullet]:
        """Get all bullets associated with a specific trace."""
        with self.lock:
            return [b for b in self.bullets if b.data.get("trace_id") == trace_id]
    
    def clear_bullets(self):
        """Clear all tracer bullets."""
        with self.lock:
            self.bullets.clear()
            self.performance_metrics.clear()
        
        logger.info("Tracer bullets cleared")
    
    def export_bullets(self, format: str = "json") -> str:
        """Export tracer bullets in the specified format."""
        with self.lock:
            bullets_data = []
            for bullet in self.bullets:
                bullets_data.append({
                    "timestamp": bullet.timestamp,
                    "event_type": bullet.event_type,
                    "message": bullet.message,
                    "data": bullet.data,
                    "thread_id": bullet.thread_id,
                    "duration": bullet.duration,
                    "parent_id": bullet.parent_id,
                    "bullet_id": bullet.bullet_id
                })
        
        if format == "json":
            return json.dumps(bullets_data, indent=2)
        elif format == "csv":
            # Simple CSV export
            lines = ["timestamp,event_type,message,thread_id,bullet_id"]
            for bullet in bullets_data:
                lines.append(f"{bullet['timestamp']},{bullet['event_type']},{bullet['message']},{bullet['thread_id']},{bullet['bullet_id']}")
            return "\n".join(lines)
        else:
            raise ValueError(f"Unsupported format: {format}")


# Global tracer manager instance
_tracer_manager = None


def get_tracer_manager() -> TracerManager:
    """Get the global tracer manager instance."""
    global _tracer_manager
    if _tracer_manager is None:
        _tracer_manager = TracerManager()
    return _tracer_manager


def fire_bullet(event_type: str, message: str, **data) -> TracerBullet:
    """Fire a tracer bullet using the global tracer manager."""
    return get_tracer_manager().fire_bullet(event_type, message, **data)


def start_trace(trace_id: str, operation: str, **metadata) -> str:
    """Start a new trace using the global tracer manager."""
    return get_tracer_manager().start_trace(trace_id, operation, **metadata)


def end_trace(trace_id: str, success: bool = True, **result_data) -> Optional[Dict[str, Any]]:
    """End a trace using the global tracer manager."""
    return get_tracer_manager().end_trace(trace_id, success, **result_data)


def add_bullet_to_trace(trace_id: str, event_type: str, message: str, **data):
    """Add a bullet to an active trace using the global tracer manager."""
    return get_tracer_manager().add_bullet_to_trace(trace_id, event_type, message, **data)


@contextmanager
def trace_operation(operation: str, **metadata):
    """Context manager for tracing operations."""
    trace_id = f"{operation}_{int(time.time() * 1000000)}"
    start_trace(trace_id, operation, **metadata)
    
    try:
        yield trace_id
        end_trace(trace_id, success=True)
    except Exception as e:
        end_trace(trace_id, success=False, error=str(e), error_type=type(e).__name__)
        raise


def trace_function(operation: Optional[str] = None, include_args: bool = False, include_result: bool = False):
    """Decorator for tracing function execution."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            op_name = operation or f"{func.__module__}.{func.__name__}"
            trace_id = f"{op_name}_{int(time.time() * 1000000)}"
            
            # Prepare metadata
            metadata = {}
            if include_args:
                metadata["args_count"] = len(args)
                metadata["kwargs_count"] = len(kwargs)
                if args:
                    metadata["first_arg_type"] = type(args[0]).__name__
            
            start_trace(trace_id, op_name, **metadata)
            
            try:
                result = func(*args, **kwargs)
                
                result_data = {}
                if include_result:
                    result_data["result_type"] = type(result).__name__
                    if hasattr(result, '__len__'):
                        result_data["result_length"] = len(result)
                
                end_trace(trace_id, success=True, **result_data)
                return result
                
            except Exception as e:
                end_trace(trace_id, success=False, 
                         error=str(e), error_type=type(e).__name__)
                raise
        
        return wrapper
    return decorator


def trace_performance(operation: str, threshold: float = 1.0):
    """Decorator for tracing function performance with threshold monitoring."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                
                if duration > threshold:
                    fire_bullet("slow_function", 
                              f"Function {func.__name__} exceeded threshold",
                              function=func.__name__,
                              duration=duration,
                              threshold=threshold)
                
                fire_bullet("function_performance",
                           f"Function {func.__name__} completed",
                           function=func.__name__,
                           duration=duration)
                
                return result
                
            except Exception as e:
                duration = time.time() - start_time
                fire_bullet("function_error",
                           f"Function {func.__name__} failed",
                           function=func.__name__,
                           duration=duration,
                           error=str(e),
                           error_type=type(e).__name__)
                raise
        
        return wrapper
    return decorator


def trace_memory_usage(operation: str):
    """Decorator for tracing memory usage of operations."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import psutil
            import os
            
            process = psutil.Process(os.getpid())
            memory_before = process.memory_info().rss
            
            try:
                result = func(*args, **kwargs)
                memory_after = process.memory_info().rss
                memory_delta = memory_after - memory_before
                
                fire_bullet("memory_usage",
                           f"Memory usage for {func.__name__}",
                           function=func.__name__,
                           memory_before=memory_before,
                           memory_after=memory_after,
                           memory_delta=memory_delta)
                
                return result
                
            except Exception as e:
                memory_after = process.memory_info().rss
                memory_delta = memory_after - memory_before
                
                fire_bullet("memory_usage_error",
                           f"Memory usage for failed {func.__name__}",
                           function=func.__name__,
                           memory_before=memory_before,
                           memory_after=memory_after,
                           memory_delta=memory_delta,
                           error=str(e))
                raise
        
        return wrapper
    return decorator


def trace_concurrent_operations(operation: str, max_concurrent: int = 10):
    """Decorator for tracing concurrent operations and detecting bottlenecks."""
    def decorator(func: Callable) -> Callable:
        active_count = 0
        lock = threading.Lock()
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal active_count
            
            with lock:
                active_count += 1
                current_active = active_count
            
            if current_active > max_concurrent:
                fire_bullet("concurrent_bottleneck",
                           f"High concurrency detected for {func.__name__}",
                           function=func.__name__,
                           active_count=current_active,
                           max_concurrent=max_concurrent)
            
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                with lock:
                    active_count -= 1
        
        return wrapper
    return decorator


# Convenience functions for common tracing scenarios
def trace_api_request(endpoint: str, method: str, **metadata):
    """Trace API request processing."""
    trace_id = f"api_{method}_{endpoint}_{int(time.time() * 1000000)}"
    return start_trace(trace_id, f"API {method} {endpoint}", 
                      endpoint=endpoint, method=method, **metadata)


def trace_detection_pattern(pattern_name: str, text_length: int, **metadata):
    """Trace pattern detection operations."""
    trace_id = f"detect_{pattern_name}_{int(time.time() * 1000000)}"
    return start_trace(trace_id, f"Detect {pattern_name}",
                      pattern=pattern_name, text_length=text_length, **metadata)


def trace_validation_operation(operation_type: str, **metadata):
    """Trace validation operations."""
    trace_id = f"validate_{operation_type}_{int(time.time() * 1000000)}"
    return start_trace(trace_id, f"Validate {operation_type}",
                      operation_type=operation_type, **metadata)


def trace_mitigation_operation(technique: str, **metadata):
    """Trace mitigation operations."""
    trace_id = f"mitigate_{technique}_{int(time.time() * 1000000)}"
    return start_trace(trace_id, f"Mitigate {technique}",
                      technique=technique, **metadata)


def get_system_health_summary() -> Dict[str, Any]:
    """Get a summary of system health based on tracer bullets."""
    manager = get_tracer_manager()
    
    # Get recent bullets
    recent_bullets = manager.get_recent_bullets(1000)
    
    # Analyze bullets
    error_count = len([b for b in recent_bullets if b.event_type in ["error", "function_error", "trace_end"] and not b.data.get("success", True)])
    slow_operation_count = len([b for b in recent_bullets if b.event_type == "slow_operation"])
    memory_issue_count = len([b for b in recent_bullets if b.event_type == "memory_usage_error"])
    concurrent_bottleneck_count = len([b for b in recent_bullets if b.event_type == "concurrent_bottleneck"])
    
    # Get performance metrics
    performance_metrics = manager.get_performance_metrics()
    
    return {
        "total_bullets": len(recent_bullets),
        "error_count": error_count,
        "slow_operation_count": slow_operation_count,
        "memory_issue_count": memory_issue_count,
        "concurrent_bottleneck_count": concurrent_bottleneck_count,
        "performance_metrics": performance_metrics,
        "health_score": max(0, 100 - (error_count * 10) - (slow_operation_count * 5) - (memory_issue_count * 15) - (concurrent_bottleneck_count * 5))
    }


if __name__ == "__main__":
    # Example usage
    tracer = get_tracer_manager()
    
    # Fire some test bullets
    tracer.fire_bullet("test", "Testing tracer system")
    
    # Trace an operation
    with trace_operation("test_operation", test_param="value"):
        time.sleep(0.1)
        tracer.fire_bullet("test", "Inside trace operation")
    
    # Get summary
    summary = get_system_health_summary()
    print(f"System health summary: {summary}")
    
    # Export bullets
    bullets_json = tracer.export_bullets("json")
    print(f"Exported {len(tracer.bullets)} bullets")
