"""
TRUICE Path Adapter - Backward Compatibility Layer

Provides thin adapters for legacy code using str paths.
Pattern: ADAPTER × COMPATIBILITY × ONE
∞ AbëONE ∞
"""

from pathlib import Path
from typing import Union, Optional, Callable, TypeVar, cast, Any
import functools

T = TypeVar('T')

def ensure_path(path: Union[str, Path]) -> Path:
    """
    Convert str or Path to resolved Path.
    
    SAFETY: Always returns absolute, resolved Path
    ASSUMES: Path is valid (will raise if not)
    VERIFY: Path exists before use (caller responsibility)
    """
    if isinstance(path, str):
        return Path(path).resolve()
    return path.resolve()

def path_adapter(func: Callable[..., T]) -> Callable[..., T]:
    """
    Decorator to adapt functions accepting Union[str, Path] to Path-only.
    
    Usage:
        @path_adapter
        def my_function(video_path: Path) -> Result:
            # Function body uses Path directly
            pass
        
        # Can still be called with str:
        my_function("path/to/video.mp4")  # Works
        my_function(Path("path/to/video.mp4"))  # Works
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Convert all Union[str, Path] args to Path
        new_args = []
        for arg in args:
            if isinstance(arg, (str, Path)):
                new_args.append(ensure_path(arg))
            else:
                new_args.append(arg)
        
        # Convert all Union[str, Path] kwargs to Path
        new_kwargs = {}
        for key, value in kwargs.items():
            if isinstance(value, (str, Path)):
                new_kwargs[key] = ensure_path(value)
            elif isinstance(value, type(None)):
                new_kwargs[key] = None
            else:
                new_kwargs[key] = value
        
        return func(*new_args, **new_kwargs)
    
    return cast(Callable[..., T], wrapper)

def ensure_optional_path(path: Optional[Union[str, Path]]) -> Optional[Path]:
    """
    Convert Optional[Union[str, Path]] to Optional[Path].
    
    SAFETY: Returns None if input is None, resolved Path otherwise
    """
    if path is None:
        return None
    return ensure_path(path)

