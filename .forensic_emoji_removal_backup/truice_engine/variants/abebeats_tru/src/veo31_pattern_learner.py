"""
Veo 3.1 Pattern Learning System
Learn from Successful Prompt Patterns

Uses PatternLearningSystem pattern from Emergence Core.

Pattern: LEARNING × PATTERN × EFFECTIVENESS × ONE
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict
import logging
import json
from pathlib import Path

from .veo31_prompt_engine import LayeredPrompt, CharacterBible, Veo31PromptConfig

logger = logging.getLogger(__name__)


@dataclass
class LearnedPromptPattern:
    """Learned prompt pattern from successful generations"""
    pattern_id: str
    pattern_type: str  # "layered_prompt", "character_bible", "workflow"
    prompt_structure: Dict[str, Any]
    success_rate: float  # 0.0 - 1.0
    usage_count: int
    last_success: Optional[datetime] = None
    last_seen: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "pattern_id": self.pattern_id,
            "pattern_type": self.pattern_type,
            "prompt_structure": self.prompt_structure,
            "success_rate": self.success_rate,
            "usage_count": self.usage_count,
            "last_success": self.last_success.isoformat() if self.last_success else None,
            "last_seen": self.last_seen.isoformat() if self.last_seen else None,
            "metadata": self.metadata
        }


@dataclass
class PromptGenerationResult:
    """Result of prompt generation"""
    success: bool
    prompt_used: Dict[str, Any]
    video_quality_score: Optional[float] = None  # 0.0 - 1.0
    user_satisfaction: Optional[float] = None  # 0.0 - 1.0
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class Veo31PatternLearner:
    """
    Pattern Learning System for Veo 3.1 Prompts
    
    Learns from successful prompt patterns and suggests improvements.
    
    Pattern: GENERATE → EXECUTE → LEARN → IMPROVE
    """
    
    def __init__(self, storage_path: Optional[Path] = None):
        """
        Initialize Pattern Learner.
        
        Args:
            storage_path: Path for persistent storage
        """
        self.logger = logging.getLogger(f"{__name__}.Veo31PatternLearner")
        self.storage_path = storage_path or Path(__file__).parent.parent / "data" / "veo31_patterns"
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.learned_patterns: Dict[str, LearnedPromptPattern] = {}
        self.generation_history: List[PromptGenerationResult] = []
        self.pattern_statistics: Dict[str, Dict[str, Any]] = defaultdict(dict)
        
        # Load existing patterns
        self._load_patterns()
    
    def record_generation(
        self,
        prompt: LayeredPrompt,
        config: Veo31PromptConfig,
        result: PromptGenerationResult
    ) -> None:
        """
        Record prompt generation result for learning.
        
        Args:
            prompt: LayeredPrompt used
            config: Configuration used
            result: Generation result
        """
        self.generation_history.append(result)
        
        # Extract pattern signature
        pattern_signature = self._extract_pattern_signature(prompt, config)
        pattern_id = self._generate_pattern_id(pattern_signature)
        
        # Update or create pattern
        if pattern_id in self.learned_patterns:
            pattern = self.learned_patterns[pattern_id]
            pattern.usage_count += 1
            pattern.last_seen = datetime.now()
            
            if result.success:
                pattern.last_success = datetime.now()
                # Update success rate (exponential moving average)
                alpha = 0.1
                pattern.success_rate = (
                    alpha * (1.0 if result.success else 0.0) +
                    (1 - alpha) * pattern.success_rate
                )
        else:
            # Create new pattern
            pattern = LearnedPromptPattern(
                pattern_id=pattern_id,
                pattern_type="layered_prompt",
                prompt_structure=pattern_signature,
                success_rate=1.0 if result.success else 0.0,
                usage_count=1,
                last_success=datetime.now() if result.success else None,
                last_seen=datetime.now(),
                metadata={
                    "model": config.model,
                    "duration": config.duration,
                    "use_workflow": config.use_workflow
                }
            )
            self.learned_patterns[pattern_id] = pattern
        
        # Update statistics
        self._update_statistics(pattern_id, result)
        
        # Save patterns periodically
        if len(self.generation_history) % 10 == 0:
            self._save_patterns()
    
    def suggest_improvements(
        self,
        prompt: LayeredPrompt,
        config: Veo31PromptConfig
    ) -> List[str]:
        """
        Suggest improvements based on learned patterns.
        
        Args:
            prompt: Current prompt
            config: Current configuration
        
        Returns:
            List of improvement suggestions
        """
        suggestions = []
        
        # Find similar successful patterns
        similar_patterns = self._find_similar_patterns(prompt, config)
        
        for pattern in similar_patterns[:3]:  # Top 3
            if pattern.success_rate > 0.7:
                # Extract what made it successful
                if "cinematography" in pattern.prompt_structure:
                    current_cinema = prompt.cinematography.lower()
                    learned_cinema = pattern.prompt_structure.get("cinematography", "").lower()
                    
                    if learned_cinema and learned_cinema not in current_cinema:
                        suggestions.append(
                            f"Consider adding: '{pattern.prompt_structure['cinematography']}' "
                            f"(success rate: {pattern.success_rate:.1%})"
                        )
        
        # Check for common failure patterns
        failure_patterns = [
            p for p in self.learned_patterns.values()
            if p.success_rate < 0.3 and p.usage_count >= 3
        ]
        
        for failure in failure_patterns:
            if self._is_similar_structure(prompt, failure.prompt_structure):
                suggestions.append(
                    f"⚠️ Warning: Similar pattern has low success rate ({failure.success_rate:.1%})"
                )
        
        return suggestions
    
    def get_best_patterns(
        self,
        pattern_type: Optional[str] = None,
        min_success_rate: float = 0.7,
        min_usage: int = 3
    ) -> List[LearnedPromptPattern]:
        """
        Get best performing patterns.
        
        Args:
            pattern_type: Filter by type
            min_success_rate: Minimum success rate
            min_usage: Minimum usage count
        
        Returns:
            List of best patterns
        """
        patterns = list(self.learned_patterns.values())
        
        # Filter
        filtered = [
            p for p in patterns
            if (pattern_type is None or p.pattern_type == pattern_type) and
            p.success_rate >= min_success_rate and
            p.usage_count >= min_usage
        ]
        
        # Sort by success rate and usage
        filtered.sort(key=lambda p: (p.success_rate, p.usage_count), reverse=True)
        
        return filtered
    
    def _extract_pattern_signature(
        self,
        prompt: LayeredPrompt,
        config: Veo31PromptConfig
    ) -> Dict[str, Any]:
        """Extract pattern signature from prompt"""
        return {
            "identity": prompt.identity,
            "cinematography": prompt.cinematography,
            "environment": prompt.environment,
            "performance_length": len(prompt.performance),
            "model": config.model,
            "use_workflow": config.use_workflow
        }
    
    def _generate_pattern_id(self, signature: Dict[str, Any]) -> str:
        """Generate pattern ID from signature"""
        import hashlib
        sig_str = json.dumps(signature, sort_keys=True)
        return hashlib.md5(sig_str.encode()).hexdigest()[:16]
    
    def _find_similar_patterns(
        self,
        prompt: LayeredPrompt,
        config: Veo31PromptConfig
    ) -> List[LearnedPromptPattern]:
        """Find similar patterns"""
        current_sig = self._extract_pattern_signature(prompt, config)
        
        similar = []
        for pattern in self.learned_patterns.values():
            similarity = self._calculate_similarity(current_sig, pattern.prompt_structure)
            if similarity > 0.5:  # 50% similarity threshold
                similar.append((similarity, pattern))
        
        # Sort by similarity
        similar.sort(key=lambda x: x[0], reverse=True)
        return [p for _, p in similar]
    
    def _calculate_similarity(
        self,
        sig1: Dict[str, Any],
        sig2: Dict[str, Any]
    ) -> float:
        """Calculate similarity between signatures"""
        # Simple similarity: count matching keys
        keys = set(sig1.keys()) & set(sig2.keys())
        if not keys:
            return 0.0
        
        matches = sum(1 for k in keys if sig1[k] == sig2[k])
        return matches / len(keys)
    
    def _is_similar_structure(
        self,
        prompt: LayeredPrompt,
        structure: Dict[str, Any]
    ) -> bool:
        """Check if prompt matches structure"""
        return (
            prompt.identity == structure.get("identity") or
            prompt.cinematography == structure.get("cinematography")
        )
    
    def _update_statistics(
        self,
        pattern_id: str,
        result: PromptGenerationResult
    ) -> None:
        """Update pattern statistics"""
        if pattern_id not in self.pattern_statistics:
            self.pattern_statistics[pattern_id] = {
                "total": 0,
                "successes": 0,
                "avg_quality": 0.0,
                "avg_satisfaction": 0.0
            }
        
        stats = self.pattern_statistics[pattern_id]
        stats["total"] += 1
        
        if result.success:
            stats["successes"] += 1
        
        if result.video_quality_score:
            stats["avg_quality"] = (
                (stats["avg_quality"] * (stats["total"] - 1) + result.video_quality_score) /
                stats["total"]
            )
        
        if result.user_satisfaction:
            stats["avg_satisfaction"] = (
                (stats["avg_satisfaction"] * (stats["total"] - 1) + result.user_satisfaction) /
                stats["total"]
            )
    
    def _save_patterns(self) -> None:
        """Save learned patterns to disk"""
        patterns_file = self.storage_path / "learned_patterns.json"
        with open(patterns_file, 'w') as f:
            json.dump(
                {pid: p.to_dict() for pid, p in self.learned_patterns.items()},
                f,
                indent=2
            )
    
    def _load_patterns(self) -> None:
        """Load learned patterns from disk"""
        patterns_file = self.storage_path / "learned_patterns.json"
        if patterns_file.exists():
            try:
                with open(patterns_file, 'r') as f:
                    data = json.load(f)
                    for pid, p_data in data.items():
                        pattern = LearnedPromptPattern(
                            pattern_id=p_data["pattern_id"],
                            pattern_type=p_data["pattern_type"],
                            prompt_structure=p_data["prompt_structure"],
                            success_rate=p_data["success_rate"],
                            usage_count=p_data["usage_count"],
                            last_success=datetime.fromisoformat(p_data["last_success"]) if p_data.get("last_success") else None,
                            last_seen=datetime.fromisoformat(p_data["last_seen"]) if p_data.get("last_seen") else None,
                            metadata=p_data.get("metadata", {})
                        )
                        self.learned_patterns[pid] = pattern
                
                self.logger.info(f"Loaded {len(self.learned_patterns)} learned patterns")
            except Exception as e:
                self.logger.warning(f"Could not load patterns: {e}")

