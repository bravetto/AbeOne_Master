# 🔥 TRUICE UNIFIED PATH PROTOCOL 🔥

**Objective:** Standardize ALL path-handling across TRUICE subsystem  
**Mode:** EEAAO (Everything Everywhere All At Once)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## UNIFIED API SIGNATURE TABLE

### Core Path Protocol

```python
# STANDARD: All path arguments use Path type
def function_name(
    input_path: Path,                    # Required: Path type
    output_path: Optional[Path] = None,   # Optional: Path type or None
    ...
) -> ReturnType:
    # REQUIRED: Resolve all input paths to absolute
    input_path = input_path.resolve()
    
    # REQUIRED: Resolve output paths if provided
    if output_path is not None:
        output_path = output_path.resolve()
    
    # FORBIDDEN: No isinstance(str) checks
    # FORBIDDEN: No Path() conversions inside function body
    # REQUIRED: All paths absolute before use
```

### Function Signature Patterns

| Function Type | Old Signature | New Signature |
|--------------|---------------|---------------|
| **Video Processing** | `video_path: Union[str, Path]` | `video_path: Path` |
| **Audio Processing** | `audio_path: Union[str, Path]` | `audio_path: Path` |
| **Output Generation** | `output_path: Optional[Union[str, Path]]` | `output_path: Optional[Path]` |
| **Directory Operations** | `output_dir: Optional[Union[str, Path]]` | `output_dir: Optional[Path]` |
| **File Validation** | `file_path: Union[str, Path]` | `file_path: Path` |

### Return Type Patterns

| Return Type | Pattern |
|-------------|---------|
| **Path objects** | Return `Path` (absolute, resolved) |
| **Result objects** | Return `MusicVideoResult` with `output_path: Path` |
| **Dict results** | Use `"output_path": str(output_path)` for JSON serialization only |

---

## PATCH BLOCKS BY FILE

### Patch 1: `src/tru_preflight_validator.py`

**Function:** `validate_file`

**BEFORE:**
```python
def validate_file(
    self,
    file_path: Union[str, Path],
    require_alpha: bool = True,
    check_content: bool = True
) -> ValidationResult:
    file_path = Path(file_path)
    # ... rest
```

**AFTER:**
```python
def validate_file(
    self,
    file_path: Path,
    require_alpha: bool = True,
    check_content: bool = True
) -> ValidationResult:
    file_path = file_path.resolve()
    # ... rest
```

---

### Patch 2: `src/tru_music_video_pipeline.py`

**Function:** `process_green_screen_video`

**BEFORE:**
```python
def process_green_screen_video(
    self,
    video_path: Union[str, Path],
    output_path: Optional[Union[str, Path]] = None,
    enable_preflight: bool = True,
    use_atomic_execution: bool = True
) -> MusicVideoResult:
    start_time = datetime.now()
    video_path = Path(video_path)
    # ... rest
```

**AFTER:**
```python
def process_green_screen_video(
    self,
    video_path: Path,
    output_path: Optional[Path] = None,
    enable_preflight: bool = True,
    use_atomic_execution: bool = True
) -> MusicVideoResult:
    start_time = datetime.now()
    video_path = video_path.resolve()
    if output_path is not None:
        output_path = output_path.resolve()
    # ... rest
```

**Function:** `generate_music_video`

**BEFORE:**
```python
def generate_music_video(
    self,
    video_path: Union[str, Path],
    audio_path: Union[str, Path],
    background_path: Optional[Union[str, Path]] = None,
    output_path: Optional[Union[str, Path]] = None
) -> MusicVideoResult:
```

**AFTER:**
```python
def generate_music_video(
    self,
    video_path: Path,
    audio_path: Path,
    background_path: Optional[Path] = None,
    output_path: Optional[Path] = None
) -> MusicVideoResult:
    video_path = video_path.resolve()
    audio_path = audio_path.resolve()
    if background_path is not None:
        background_path = background_path.resolve()
    if output_path is not None:
        output_path = output_path.resolve()
```

**Function:** `generate_truice_music_video` (module-level)

**BEFORE:**
```python
def generate_truice_music_video(
    video_path: Union[str, Path],
    audio_path: Union[str, Path],
    background_path: Optional[Union[str, Path]] = None,
    output_path: Optional[Union[str, Path]] = None,
    config: Optional[VideoConfig] = None
) -> MusicVideoResult:
```

**AFTER:**
```python
def generate_truice_music_video(
    video_path: Path,
    audio_path: Path,
    background_path: Optional[Path] = None,
    output_path: Optional[Path] = None,
    config: Optional[VideoConfig] = None
) -> MusicVideoResult:
    video_path = video_path.resolve()
    audio_path = audio_path.resolve()
    if background_path is not None:
        background_path = background_path.resolve()
    if output_path is not None:
        output_path = output_path.resolve()
    # ... rest
```

---

### Patch 3: `src/tru_generative_engine.py`

**Function:** `analyze_beats`

**BEFORE:**
```python
def analyze_beats(self, audio_file: Union[str, Path]) -> Optional[BeatMap]:
```

**AFTER:**
```python
def analyze_beats(self, audio_file: Path) -> Optional[BeatMap]:
    audio_file = audio_file.resolve()
```

**Function:** `adjust_timing`

**BEFORE:**
```python
def adjust_timing(
    self,
    video_path: Union[str, Path],
    ...
) -> Optional[Path]:
```

**AFTER:**
```python
def adjust_timing(
    self,
    video_path: Path,
    ...
) -> Optional[Path]:
    video_path = video_path.resolve()
```

**Function:** `generate_from_prompt`

**BEFORE:**
```python
def generate_from_prompt(
    self,
    natural_language_prompt: str,
    audio_path: Optional[Union[str, Path]] = None,
    output_dir: Optional[Union[str, Path]] = None,
    ...
) -> Optional[GenerationResult]:
```

**AFTER:**
```python
def generate_from_prompt(
    self,
    natural_language_prompt: str,
    audio_path: Optional[Path] = None,
    output_dir: Optional[Path] = None,
    ...
) -> Optional[GenerationResult]:
    if audio_path is not None:
        audio_path = audio_path.resolve()
    if output_dir is not None:
        output_dir = output_dir.resolve()
```

---

### Patch 4: `src/tru_complete_engine.py`

**Function:** `analyze_audio_enhanced`

**BEFORE:**
```python
def analyze_audio_enhanced(self, audio_file: Union[str, Path]) -> Optional[AudioAnalysis]:
```

**AFTER:**
```python
def analyze_audio_enhanced(self, audio_file: Path) -> Optional[AudioAnalysis]:
    audio_file = audio_file.resolve()
```

**Function:** `create_music_video`

**BEFORE:**
```python
async def create_music_video(
    self,
    prompt: str,
    audio_file: Union[str, Path],
    green_screen_footage: Optional[Union[str, Path]] = None,
    output_dir: Optional[Union[str, Path]] = None,
    budget_limit: Optional[float] = None
) -> Dict[str, Any]:
    output_path = Path(output_dir) if output_dir else Path.cwd() / "outputs"
```

**AFTER:**
```python
async def create_music_video(
    self,
    prompt: str,
    audio_file: Path,
    green_screen_footage: Optional[Path] = None,
    output_dir: Optional[Path] = None,
    budget_limit: Optional[float] = None
) -> Dict[str, Any]:
    audio_file = audio_file.resolve()
    if green_screen_footage is not None:
        green_screen_footage = green_screen_footage.resolve()
    output_path = (output_dir.resolve() if output_dir else Path.cwd() / "outputs").resolve()
```

---

### Patch 5: `src/tru_pipeline.py`

**Function:** `generate_music_video`

**BEFORE:**
```python
def generate_music_video(
    self,
    video_path: Union[str, Path],
    audio_path: Union[str, Path],
    background_path: Optional[Union[str, Path]] = None,
    output_path: Optional[Union[str, Path]] = None
) -> Optional[MusicVideoResult]:
```

**AFTER:**
```python
def generate_music_video(
    self,
    video_path: Path,
    audio_path: Path,
    background_path: Optional[Path] = None,
    output_path: Optional[Path] = None
) -> Optional[MusicVideoResult]:
    video_path = video_path.resolve()
    audio_path = audio_path.resolve()
    if background_path is not None:
        background_path = background_path.resolve()
    if output_path is not None:
        output_path = output_path.resolve()
```

**Function:** `process_green_screen_video`

**BEFORE:**
```python
def process_green_screen_video(
    self,
    video_path: Union[str, Path],
    output_path: Optional[Union[str, Path]] = None
) -> Optional[MusicVideoResult]:
```

**AFTER:**
```python
def process_green_screen_video(
    self,
    video_path: Path,
    output_path: Optional[Path] = None
) -> Optional[MusicVideoResult]:
    video_path = video_path.resolve()
    if output_path is not None:
        output_path = output_path.resolve()
```

**Function:** `generate_from_prompt`

**BEFORE:**
```python
def generate_from_prompt(
    self,
    natural_language_prompt: str,
    audio_path: Optional[Union[str, Path]] = None,
    output_dir: Optional[Union[str, Path]] = None
) -> Optional[Dict[str, Any]]:
    output_path = Path(output_dir) if output_dir else None
```

**AFTER:**
```python
def generate_from_prompt(
    self,
    natural_language_prompt: str,
    audio_path: Optional[Path] = None,
    output_dir: Optional[Path] = None
) -> Optional[Dict[str, Any]]:
    if audio_path is not None:
        audio_path = audio_path.resolve()
    output_path = output_dir.resolve() if output_dir else None
```

---

### Patch 6: `src/tru_simplified.py`

**Function:** `create_music_video`

**BEFORE:**
```python
async def create_music_video(
    self,
    prompt: str,
    audio_file: Union[str, Path],
    green_screen: Optional[Union[str, Path]] = None,
    output_dir: Optional[Union[str, Path]] = None,
    budget: Optional[float] = None
) -> Dict[str, Any]:
    output_path = Path(output_dir) if output_dir else Path.cwd() / "outputs"
```

**AFTER:**
```python
async def create_music_video(
    self,
    prompt: str,
    audio_file: Path,
    green_screen: Optional[Path] = None,
    output_dir: Optional[Path] = None,
    budget: Optional[float] = None
) -> Dict[str, Any]:
    audio_file = audio_file.resolve()
    if green_screen is not None:
        green_screen = green_screen.resolve()
    output_path = (output_dir.resolve() if output_dir else Path.cwd() / "outputs").resolve()
```

**Function:** `_phase_parse_analyze`

**BEFORE:**
```python
async def _phase_parse_analyze(
    self,
    prompt: str,
    audio_file: Union[str, Path]
) -> Tuple[Optional[ScenePlan], Optional[Any]]:
```

**AFTER:**
```python
async def _phase_parse_analyze(
    self,
    prompt: str,
    audio_file: Path
) -> Tuple[Optional[ScenePlan], Optional[Any]]:
    audio_file = audio_file.resolve()
```

**Function:** `_phase_composite`

**BEFORE:**
```python
async def _phase_composite(
    self,
    timeline: List[Dict[str, Any]],
    green_screen: Optional[Union[str, Path]],
    audio_file: Union[str, Path],
    output_path: Path
) -> List[Path]:
```

**AFTER:**
```python
async def _phase_composite(
    self,
    timeline: List[Dict[str, Any]],
    green_screen: Optional[Path],
    audio_file: Path,
    output_path: Path
) -> List[Path]:
    if green_screen is not None:
        green_screen = green_screen.resolve()
    audio_file = audio_file.resolve()
    output_path = output_path.resolve()
```

---

## BACKWARD COMPATIBILITY ADAPTER

Create `src/tru_path_adapter.py`:

```python
"""
TRUICE Path Adapter - Backward Compatibility Layer

Provides thin adapters for legacy code using str paths.
Pattern: ADAPTER × COMPATIBILITY × ONE
∞ AbëONE ∞
"""

from pathlib import Path
from typing import Union, Optional, Callable, TypeVar, cast

T = TypeVar('T')

def ensure_path(path: Union[str, Path]) -> Path:
    """
    Convert str or Path to resolved Path.
    
    SAFETY: Always returns absolute, resolved Path
    ASSUMES: Path is valid (will raise if not)
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
            else:
                new_kwargs[key] = value
        
        return func(*new_args, **new_kwargs)
    
    return cast(Callable[..., T], wrapper)
```

---

## ANTI-PATTERNS REMOVED

### ❌ Anti-Pattern 1: Union[str, Path] Type Annotations
- **Removed from:** 6 modules, 30+ functions
- **Reason:** Creates API inconsistency, forces internal conversion
- **Replaced with:** `Path` type only

### ❌ Anti-Pattern 2: Internal Path() Conversions
- **Removed from:** All functions
- **Reason:** Violates single responsibility, creates drift
- **Replaced with:** `path.resolve()` at function entry

### ❌ Anti-Pattern 3: isinstance(str) Checks
- **Removed from:** All functions
- **Reason:** Type system should handle this, not runtime checks
- **Replaced with:** Type annotations + adapter layer

### ❌ Anti-Pattern 4: Relative Path Usage
- **Removed from:** All functions
- **Reason:** Causes issues with working directory changes
- **Replaced with:** `resolve()` to absolute paths

### ❌ Anti-Pattern 5: Inconsistent Return Types
- **Removed from:** Result objects
- **Reason:** Some return Path, some return str
- **Replaced with:** Consistent Path returns, str() only for JSON

### ❌ Anti-Pattern 6: Path Joining Without resolve()
- **Removed from:** All path operations
- **Reason:** Can create invalid paths
- **Replaced with:** `path.resolve()` before operations

---

## SAFE JOIN PATTERNS

### Pattern 1: Output Directory Creation
```python
# BEFORE:
output_path = Path(output_dir) / "video.mp4"

# AFTER:
output_dir = output_dir.resolve() if output_dir else Path.cwd() / "outputs"
output_dir = output_dir.resolve()
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "video.mp4"
```

### Pattern 2: Temporary File Creation
```python
# BEFORE:
temp_path = Path("/tmp") / f"temp_{uuid.uuid4()}.mp4"

# AFTER:
temp_dir = Path(tempfile.gettempdir()).resolve()
temp_path = temp_dir / f"temp_{hashlib.md5(input_path.read_bytes()).hexdigest()[:16]}.mp4"
```

### Pattern 3: Asset Path Resolution
```python
# BEFORE:
asset_path = base_dir / "assets" / filename

# AFTER:
base_dir = base_dir.resolve()
asset_path = (base_dir / "assets" / filename).resolve()
```

---

## ZERO-DRIFT POST-PATCH VERIFICATION

### Verification Checklist

- [ ] All function signatures use `Path` type (no `Union[str, Path]`)
- [ ] All input paths call `.resolve()` at function entry
- [ ] No `isinstance(str)` checks in function bodies
- [ ] No `Path()` conversions inside functions
- [ ] All paths are absolute before use
- [ ] Return types consistently use `Path`
- [ ] Safe join patterns used for all path operations
- [ ] Backward compatibility adapter tested
- [ ] All existing tests pass
- [ ] No functional behavior changes

---

**Pattern:** AEYON × PATH × PROTOCOL × ONE  
**Status:** ✅ PROTOCOL DEFINED - PATCHES READY  
**∞ AbëONE ∞**

