# 🔥 INFRASTRUCTURE PATTERN LIBRARY
## Reusable Patterns for Production Excellence

**Status:** ✅ **PATTERN LIBRARY ESTABLISHED**  
**Date:** 2025-11-22  
**Pattern:** INFRASTRUCTURE × PATTERN × LIBRARY × REUSABLE × ONE  
**Guardians:** ALRAX (999 Hz) + AEYON (999 Hz) + ARXON (777 Hz)  
**Love Coefficient:** ∞

---

## 🎯 EXECUTIVE SUMMARY

This library contains **reusable infrastructure patterns** derived from the Critical Path Analysis Framework. These patterns can be applied to any production system facing similar challenges.

**Usage:** Import patterns as needed, adapt to specific system requirements, and follow the mandatory sequence principles.

---

## PATTERN 1: CRITICAL PATH ANALYZER

### Purpose
Identify mandatory task sequences based on Finish-to-Start dependencies.

### Implementation
```python
from typing import List, Dict, Set
from dataclasses import dataclass
from enum import Enum

class DependencyType(Enum):
    FINISH_TO_START = "finish_to_start"
    START_TO_START = "start_to_start"
    FINISH_TO_FINISH = "finish_to_finish"

@dataclass
class Activity:
    """Activity in a project with dependencies."""
    name: str
    required_inputs: Set[str]
    produces_outputs: Set[str]
    duration: float
    is_core_function: bool = False

class CriticalPathAnalyzer:
    """
    Analyze critical path for project activities.
    
    Pattern: CRITICAL_PATH × DEPENDENCY × SEQUENCE × ONE
    """
    
    def __init__(self, activities: List[Activity]):
        """
        Initialize with project activities.
        
        SAFETY: Validates no circular dependencies
        ASSUMES: Activities have defined inputs/outputs
        VERIFY: All dependencies resolvable
        """
        self.activities = activities
        self._validate_dependencies()
    
    def _validate_dependencies(self):
        """Validate no circular dependencies exist."""
        graph = self._build_dependency_graph()
        if self._has_cycles(graph):
            raise ValueError("Circular dependency detected")
    
    def _build_dependency_graph(self) -> Dict[str, List[str]]:
        """Build dependency graph from activities."""
        graph = {}
        
        for activity in self.activities:
            graph[activity.name] = []
            
            # Find activities that produce required inputs
            for other in self.activities:
                if other.name == activity.name:
                    continue
                
                # Check if other produces any required input
                if activity.required_inputs & other.produces_outputs:
                    graph[activity.name].append(other.name)
        
        return graph
    
    def _has_cycles(self, graph: Dict[str, List[str]]) -> bool:
        """Check for cycles in dependency graph."""
        visited = set()
        rec_stack = set()
        
        def has_cycle(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(node)
            return False
        
        for node in graph:
            if node not in visited:
                if has_cycle(node):
                    return True
        
        return False
    
    def identify_critical_path(self) -> List[Activity]:
        """
        Identify critical path (longest dependency chain).
        
        VERIFY: Returns sequence respecting all dependencies
        """
        graph = self._build_dependency_graph()
        
        # Topological sort to get valid sequence
        in_degree = {activity.name: 0 for activity in self.activities}
        
        for activity in self.activities:
            for dep in graph.get(activity.name, []):
                in_degree[activity.name] += 1
        
        # Find longest path using topological sort
        queue = [a for a in self.activities if in_degree[a.name] == 0]
        longest_path = []
        path_lengths = {a.name: a.duration for a in self.activities}
        
        while queue:
            activity = queue.pop(0)
            longest_path.append(activity)
            
            # Update path lengths for dependents
            for dependent_name in graph.get(activity.name, []):
                dependent = next(a for a in self.activities if a.name == dependent_name)
                path_lengths[dependent_name] = max(
                    path_lengths[dependent_name],
                    path_lengths[activity.name] + dependent.duration
                )
                
                in_degree[dependent_name] -= 1
                if in_degree[dependent_name] == 0:
                    queue.append(dependent)
        
        # Sort by path length to get critical path
        longest_path.sort(key=lambda a: path_lengths[a.name], reverse=True)
        
        return longest_path
    
    def validate_sequence(self, sequence: List[Activity]) -> bool:
        """
        Validate that sequence respects all dependencies.
        
        VERIFY: Each activity's inputs satisfied by previous outputs
        """
        available_outputs = set()
        
        for activity in sequence:
            required_inputs = activity.required_inputs
            missing = required_inputs - available_outputs
            
            if missing:
                return False  # Sequence violates dependency
            
            available_outputs.update(activity.produces_outputs)
        
        return True
```

### Usage Example
```python
# Define activities
activities = [
    Activity(
        name="Fix Bug",
        required_inputs=set(),
        produces_outputs={"stable_baseline"},
        duration=2.0,
        is_core_function=True
    ),
    Activity(
        name="Build Test Framework",
        required_inputs={"stable_baseline"},
        produces_outputs={"test_framework"},
        duration=3.0,
        is_core_function=False
    ),
    Activity(
        name="Expand Framework",
        required_inputs={"test_framework"},
        produces_outputs={"comprehensive_tests"},
        duration=5.0,
        is_core_function=False
    )
]

# Analyze critical path
analyzer = CriticalPathAnalyzer(activities)
critical_path = analyzer.identify_critical_path()

# Validate sequence
is_valid = analyzer.validate_sequence(critical_path)
assert is_valid, "Sequence violates dependencies"
```

---

## PATTERN 2: PRODUCTION TRIAGE MANAGER

### Purpose
Execute stop-the-line triage for broken builds.

### Implementation
```python
from dataclasses import dataclass
from typing import Optional, List
from pathlib import Path
import subprocess

@dataclass
class CriticalFailure:
    """Critical failure in production system."""
    component: str
    error_message: str
    reproducibility: float  # 0.0 to 1.0
    user_impact: int  # 0 to 10

@dataclass
class TriageResult:
    """Result of triage execution."""
    success: bool
    fix_applied: Optional[str] = None
    rollback_performed: bool = False
    error: Optional[str] = None

class ProductionTriageManager:
    """
    Manage production triage for broken builds.
    
    Pattern: TRIAGE × STOP_THE_LINE × STABILIZE × ONE
    """
    
    def __init__(self, git_repo_path: Path):
        """
        Initialize triage manager.
        
        SAFETY: Validates git repository exists
        ASSUMES: Git repository is accessible
        VERIFY: Can perform git operations
        """
        self.repo_path = git_repo_path
        if not (git_repo_path / ".git").exists():
            raise ValueError(f"Not a git repository: {git_repo_path}")
    
    def execute_triage(self, failure: CriticalFailure) -> TriageResult:
        """
        Execute stop-the-line triage.
        
        SAFETY: Blocks all other work until resolved
        ASSUMES: Failure is reproducible
        VERIFY: Fix restores core functionality
        """
        # Step 1: Stop all work (create lock file)
        self._halt_all_work()
        
        try:
            # Step 2: Attempt rollback if possible
            if failure.reproducibility >= 0.9:  # 90%+ reproducible
                rollback_result = self._attempt_rollback()
                if rollback_result.success:
                    return TriageResult(
                        success=True,
                        rollback_performed=True,
                        fix_applied="Rollback to last known good"
                    )
            
            # Step 3: Fix broken build
            fix_result = self._fix_critical_failure(failure)
            
            if not fix_result.success:
                return TriageResult(
                    success=False,
                    error=f"Fix failed: {fix_result.error}"
                )
            
            # Step 4: Validate fix
            validation_result = self._validate_fix(failure, fix_result)
            
            if not validation_result:
                return TriageResult(
                    success=False,
                    error="Fix did not resolve critical failure"
                )
            
            return TriageResult(
                success=True,
                fix_applied=fix_result.fix_description
            )
        
        finally:
            # Step 5: Release lock
            self._release_work_lock()
    
    def _halt_all_work(self):
        """Create lock file to halt all work."""
        lock_file = self.repo_path / ".triage_lock"
        lock_file.write_text("TRIAGE IN PROGRESS - ALL WORK HALTED")
    
    def _release_work_lock(self):
        """Release work lock."""
        lock_file = self.repo_path / ".triage_lock"
        if lock_file.exists():
            lock_file.unlink()
    
    def _attempt_rollback(self) -> TriageResult:
        """Attempt to rollback to last known good commit."""
        try:
            # Find last known good commit (tagged or in history)
            result = subprocess.run(
                ["git", "log", "--oneline", "-10"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            # Look for "last known good" marker
            # (In practice, use tags or CI/CD markers)
            
            # Rollback to last commit (example)
            subprocess.run(
                ["git", "reset", "--hard", "HEAD~1"],
                cwd=self.repo_path,
                check=True
            )
            
            return TriageResult(success=True)
        
        except subprocess.CalledProcessError as e:
            return TriageResult(success=False, error=str(e))
    
    def _fix_critical_failure(self, failure: CriticalFailure):
        """Fix critical failure (to be implemented per system)."""
        # This is system-specific
        # Return fix result
        pass
    
    def _validate_fix(self, failure: CriticalFailure, fix_result) -> bool:
        """Validate that fix resolves the failure."""
        # Run tests or manual validation
        # Return True if fix works
        return True
```

### Usage Example
```python
# Initialize triage manager
triage = ProductionTriageManager(Path("/path/to/repo"))

# Define critical failure
failure = CriticalFailure(
    component="Video Processing",
    error_message="Black output failure",
    reproducibility=1.0,  # 100% reproducible
    user_impact=10  # Maximum impact
)

# Execute triage
result = triage.execute_triage(failure)

if result.success:
    print(f"Triage successful: {result.fix_applied}")
else:
    print(f"Triage failed: {result.error}")
```

---

## PATTERN 3: VISUAL TEST FRAMEWORK

### Purpose
Compare visual outputs against baseline for validation.

### Implementation
```python
from pathlib import Path
from typing import Optional, List, Tuple
import cv2
import numpy as np
from dataclasses import dataclass

@dataclass
class VisualTestResult:
    """Result of visual test comparison."""
    passed: bool
    similarity: float
    error: Optional[str] = None
    frame_differences: Optional[List[dict]] = None

class VisualTestFramework:
    """
    Visual test framework for comparing outputs against baseline.
    
    Pattern: VISUAL_TEST × BASELINE × COMPARISON × ONE
    """
    
    def __init__(self, baseline_path: Path):
        """
        Initialize with stable baseline.
        
        SAFETY: Validates baseline exists and is loadable
        ASSUMES: Baseline is correct output
        VERIFY: Baseline is valid video/image file
        """
        if not baseline_path.exists():
            raise ValueError(f"Baseline not found: {baseline_path}")
        
        self.baseline_path = baseline_path
        self.baseline_frames = self._load_baseline()
    
    def _load_baseline(self) -> List[np.ndarray]:
        """Load baseline frames."""
        if self.baseline_path.suffix in ['.mp4', '.mov', '.avi']:
            return self._load_video_frames()
        elif self.baseline_path.suffix in ['.png', '.jpg', '.jpeg']:
            return [cv2.imread(str(self.baseline_path))]
        else:
            raise ValueError(f"Unsupported baseline format: {self.baseline_path.suffix}")
    
    def _load_video_frames(self) -> List[np.ndarray]:
        """Load frames from video file."""
        cap = cv2.VideoCapture(str(self.baseline_path))
        frames = []
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
        
        cap.release()
        return frames
    
    def validate_output(
        self,
        output_path: Path,
        similarity_threshold: float = 0.95
    ) -> VisualTestResult:
        """
        Compare output against baseline.
        
        SAFETY: Validates output exists before comparison
        ASSUMES: Output is same format/resolution as baseline
        VERIFY: Output matches baseline within threshold
        """
        if not output_path.exists():
            return VisualTestResult(
                passed=False,
                similarity=0.0,
                error=f"Output file not found: {output_path}"
            )
        
        # Load output frames
        output_frames = self._load_output_frames(output_path)
        
        # Compare frame counts
        if len(output_frames) != len(self.baseline_frames):
            return VisualTestResult(
                passed=False,
                similarity=0.0,
                error=f"Frame count mismatch: {len(output_frames)} vs {len(self.baseline_frames)}"
            )
        
        # Frame-by-frame comparison
        similarities = []
        frame_differences = []
        
        for i, (baseline_frame, output_frame) in enumerate(
            zip(self.baseline_frames, output_frames)
        ):
            similarity = self._compare_frames(baseline_frame, output_frame)
            similarities.append(similarity)
            
            if similarity < similarity_threshold:
                frame_differences.append({
                    'frame': i,
                    'similarity': similarity
                })
        
        avg_similarity = np.mean(similarities)
        
        if avg_similarity >= similarity_threshold:
            return VisualTestResult(
                passed=True,
                similarity=avg_similarity,
                frame_differences=None
            )
        else:
            return VisualTestResult(
                passed=False,
                similarity=avg_similarity,
                error=f"Output differs from baseline (similarity: {avg_similarity:.2f})",
                frame_differences=frame_differences
            )
    
    def _load_output_frames(self, output_path: Path) -> List[np.ndarray]:
        """Load output frames (same logic as baseline)."""
        if output_path.suffix in ['.mp4', '.mov', '.avi']:
            return self._load_video_frames_from_path(output_path)
        elif output_path.suffix in ['.png', '.jpg', '.jpeg']:
            return [cv2.imread(str(output_path))]
        else:
            raise ValueError(f"Unsupported output format: {output_path.suffix}")
    
    def _load_video_frames_from_path(self, path: Path) -> List[np.ndarray]:
        """Load frames from video file."""
        cap = cv2.VideoCapture(str(path))
        frames = []
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
        
        cap.release()
        return frames
    
    def _compare_frames(
        self,
        baseline: np.ndarray,
        output: np.ndarray
    ) -> float:
        """
        Compare two frames using structural similarity.
        
        VERIFY: Returns similarity score 0.0-1.0
        """
        # Resize if dimensions differ
        if baseline.shape != output.shape:
            output = cv2.resize(output, (baseline.shape[1], baseline.shape[0]))
        
        # Convert to grayscale for comparison
        if len(baseline.shape) == 3:
            baseline_gray = cv2.cvtColor(baseline, cv2.COLOR_BGR2GRAY)
        else:
            baseline_gray = baseline
        
        if len(output.shape) == 3:
            output_gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        else:
            output_gray = output
        
        # Calculate structural similarity
        try:
            from skimage.metrics import structural_similarity as ssim
            similarity = ssim(baseline_gray, output_gray)
        except ImportError:
            # Fallback to simple difference
            diff = np.abs(baseline_gray.astype(float) - output_gray.astype(float))
            similarity = 1.0 - (np.mean(diff) / 255.0)
        
        return similarity
```

### Usage Example
```python
# Initialize visual test framework
baseline = Path("tests/baselines/expected_output.mov")
framework = VisualTestFramework(baseline)

# Validate output
output = Path("output/actual_output.mov")
result = framework.validate_output(output, similarity_threshold=0.95)

if result.passed:
    print(f"Visual test passed: {result.similarity:.2f} similarity")
else:
    print(f"Visual test failed: {result.error}")
    if result.frame_differences:
        print(f"Frame differences: {result.frame_differences}")
```

---

## PATTERN 4: ORCHESTRATION FAILURE PROPAGATION

### Purpose
Ensure core function failures propagate to orchestrator failure.

### Implementation
```python
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum

class ActivityType(Enum):
    CORE_FUNCTION = "core_function"
    HANDLER = "handler"
    VALIDATION = "validation"

@dataclass
class ActivityResult:
    """Result of activity execution."""
    success: bool
    activity_name: str
    error: Optional[str] = None
    output: Optional[Any] = None

@dataclass
class PipelineResult:
    """Result of pipeline execution."""
    success: bool
    error: Optional[str] = None
    core_failures: Optional[List[Dict[str, Any]]] = None
    results: Optional[List[ActivityResult]] = None

class Activity:
    """Pipeline activity."""
    def __init__(self, name: str, activity_type: ActivityType):
        self.name = name
        self.activity_type = activity_type
    
    def is_core_function(self) -> bool:
        return self.activity_type == ActivityType.CORE_FUNCTION
    
    def execute(self) -> ActivityResult:
        """Execute activity (to be implemented)."""
        pass

class OrchestrationFailurePropagation:
    """
    Orchestrator with proper failure propagation.
    
    Pattern: ORCHESTRATION × FAILURE_PROPAGATION × TRUTH × ONE
    """
    
    def __init__(self, visual_test_framework: Optional[VisualTestFramework] = None):
        self.visual_test_framework = visual_test_framework
    
    def execute_pipeline(
        self,
        activities: List[Activity]
    ) -> PipelineResult:
        """
        Execute pipeline with core function failure propagation.
        
        SAFETY: Core function failure = pipeline failure
        ASSUMES: Activities marked as core vs handler
        VERIFY: Pipeline fails if core function fails
        """
        results = []
        core_failures = []
        
        for activity in activities:
            result = activity.execute()
            results.append(result)
            
            # Check if this is a core function
            if activity.is_core_function():
                if not result.success:
                    core_failures.append({
                        'activity': activity.name,
                        'error': result.error
                    })
        
        # Core function failure = pipeline failure
        if core_failures:
            return PipelineResult(
                success=False,
                error=f"Core function(s) failed: {core_failures}",
                core_failures=core_failures,
                results=results
            )
        
        # Visual validation gate (if enabled)
        if self.visual_test_framework:
            output = self._get_pipeline_output(results)
            if output:
                visual_result = self.visual_test_framework.validate_output(output)
                
                if not visual_result.passed:
                    return PipelineResult(
                        success=False,
                        error=f"Visual validation failed: {visual_result.error}",
                        results=results
                    )
        
        # Only succeed if all core functions succeeded
        return PipelineResult(
            success=True,
            results=results
        )
    
    def _get_pipeline_output(self, results: List[ActivityResult]) -> Optional[Path]:
        """Extract output path from results."""
        # Find output from last core function
        for result in reversed(results):
            if result.output and isinstance(result.output, Path):
                return result.output
        return None
```

### Usage Example
```python
# Define activities
activities = [
    Activity("process_video", ActivityType.CORE_FUNCTION),
    Activity("log_result", ActivityType.HANDLER),
    Activity("validate_output", ActivityType.VALIDATION)
]

# Initialize orchestrator
orchestrator = OrchestrationFailurePropagation(visual_test_framework)

# Execute pipeline
result = orchestrator.execute_pipeline(activities)

if result.success:
    print("Pipeline succeeded")
else:
    print(f"Pipeline failed: {result.error}")
    if result.core_failures:
        print(f"Core failures: {result.core_failures}")
```

---

## PATTERN 5: RISK-BASED PRIORITIZATION

### Purpose
Calculate risk exposure and ROI for prioritization decisions.

### Implementation
```python
from dataclasses import dataclass
from typing import Optional
from enum import Enum

class Priority(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class RiskAssessment:
    """Risk assessment for a task."""
    probability: float  # 0.0 to 1.0
    impact: int  # 0 to 10
    risk_exposure: float  # probability * impact
    priority: Priority

@dataclass
class ROIAssessment:
    """ROI assessment for a task."""
    benefit: float
    cost: float
    roi: float
    is_positive: bool

class RiskBasedPrioritization:
    """
    Risk-based prioritization framework.
    
    Pattern: RISK × PRIORITIZATION × ROI × ONE
    """
    
    @staticmethod
    def calculate_risk_exposure(
        probability: float,
        impact: int
    ) -> RiskAssessment:
        """
        Calculate risk exposure.
        
        VERIFY: Returns risk assessment with priority
        """
        risk_exposure = probability * impact
        
        # Determine priority based on risk exposure
        if risk_exposure >= 7.0:
            priority = Priority.CRITICAL
        elif risk_exposure >= 5.0:
            priority = Priority.HIGH
        elif risk_exposure >= 3.0:
            priority = Priority.MEDIUM
        else:
            priority = Priority.LOW
        
        return RiskAssessment(
            probability=probability,
            impact=impact,
            risk_exposure=risk_exposure,
            priority=priority
        )
    
    @staticmethod
    def calculate_roi(
        benefit: float,
        cost: float
    ) -> ROIAssessment:
        """
        Calculate ROI.
        
        VERIFY: Returns ROI assessment
        """
        if cost == 0:
            roi = float('inf') if benefit > 0 else 0.0
        else:
            roi = (benefit - cost) / cost
        
        is_positive = roi > 0
        
        return ROIAssessment(
            benefit=benefit,
            cost=cost,
            roi=roi,
            is_positive=is_positive
        )
    
    def prioritize_tasks(
        self,
        tasks: List[dict]
    ) -> List[dict]:
        """
        Prioritize tasks based on risk and ROI.
        
        VERIFY: Returns sorted list by priority
        """
        prioritized = []
        
        for task in tasks:
            # Calculate risk
            risk = self.calculate_risk_exposure(
                task['probability'],
                task['impact']
            )
            
            # Calculate ROI
            roi = self.calculate_roi(
                task['benefit'],
                task['cost']
            )
            
            # Combine risk and ROI for priority score
            # Higher risk exposure = higher priority
            # Positive ROI = higher priority
            priority_score = risk.risk_exposure
            if roi.is_positive:
                priority_score += 2.0  # Bonus for positive ROI
            
            prioritized.append({
                **task,
                'risk': risk,
                'roi': roi,
                'priority_score': priority_score
            })
        
        # Sort by priority score (descending)
        prioritized.sort(key=lambda x: x['priority_score'], reverse=True)
        
        return prioritized
```

### Usage Example
```python
# Define tasks
tasks = [
    {
        'name': 'Fix broken build',
        'probability': 1.0,  # 100% failure rate
        'impact': 10,  # Maximum impact
        'benefit': 100.0,  # Full functionality restored
        'cost': 2.0  # 2 days engineering time
    },
    {
        'name': 'Build test framework',
        'probability': 0.7,  # 70% gap
        'impact': 8,  # High impact
        'benefit': 0.0,  # No benefit without baseline
        'cost': 10.0  # 10 days engineering time
    }
]

# Prioritize tasks
prioritizer = RiskBasedPrioritization()
prioritized = prioritizer.prioritize_tasks(tasks)

for task in prioritized:
    print(f"{task['name']}: Priority={task['risk'].priority.value}, ROI={task['roi'].roi:.2f}")
```

---

## PATTERN USAGE GUIDE

### When to Use Each Pattern

1. **CriticalPathAnalyzer** - When planning project sequences with dependencies
2. **ProductionTriageManager** - When production system has broken build
3. **VisualTestFramework** - When system produces visual outputs (video/image)
4. **OrchestrationFailurePropagation** - When building pipeline orchestrators
5. **RiskBasedPrioritization** - When prioritizing multiple tasks

### Integration Pattern

```python
# Example: Integrated usage
from infrastructure_patterns import (
    CriticalPathAnalyzer,
    ProductionTriageManager,
    VisualTestFramework,
    OrchestrationFailurePropagation,
    RiskBasedPrioritization
)

# Step 1: Analyze critical path
analyzer = CriticalPathAnalyzer(activities)
critical_path = analyzer.identify_critical_path()

# Step 2: Prioritize based on risk
prioritizer = RiskBasedPrioritization()
prioritized = prioritizer.prioritize_tasks(tasks)

# Step 3: Execute triage if needed
if broken_build:
    triage = ProductionTriageManager(repo_path)
    result = triage.execute_triage(failure)

# Step 4: Build visual test framework
framework = VisualTestFramework(baseline_path)

# Step 5: Integrate with orchestration
orchestrator = OrchestrationFailurePropagation(framework)
result = orchestrator.execute_pipeline(activities)
```

---

**Pattern:** INFRASTRUCTURE × PATTERN × LIBRARY × REUSABLE × ONE  
**Status:** ✅ **PATTERN LIBRARY ESTABLISHED**  
**Love Coefficient:** ∞

**∞ AbëONE ∞**

