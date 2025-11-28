"""
Veo 3.1 Unified System
Complete Integration with Initialization & Activation

Unifies all components:
- Prompt Engine
- CDF Index
- Validator
- Runway API Client
- Director Agent
- Pattern Learner
- Metrics Collector

Pattern: UNIFIED × INITIALIZATION × ACTIVATION × ONE
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
import logging
from pathlib import Path

from .veo31_prompt_engine import Veo31PromptEngine, Veo31PromptConfig
from .veo31_cdf_index import Veo31CDFIndex
from .veo31_validator import Veo31Validator
from .veo31_runway_client import RunwayAPIClient
from .veo31_director_agent import Veo31DirectorAgent, DirectorAgentConfig
from .veo31_pattern_learner import Veo31PatternLearner
from .veo31_metrics import Veo31MetricsCollector

logger = logging.getLogger(__name__)


@dataclass
class Veo31SystemConfig:
    """Configuration for unified Veo31 system"""
    # Runway API
    runway_api_key: Optional[str] = None
    
    # LLM for Director Agent
    llm_client: Optional[Any] = None
    system_prompt_builder: Optional[Any] = None
    
    # Storage paths
    cdf_storage_path: Optional[Path] = None
    pattern_storage_path: Optional[Path] = None
    
    # Features
    enable_director_agent: bool = True
    enable_pattern_learning: bool = True
    enable_metrics: bool = True
    enable_api_client: bool = True


class Veo31UnifiedSystem:
    """
    Veo 3.1 Unified System
    
    Complete integration of all components with proper initialization and activation.
    
    Pattern: INITIALIZE → ACTIVATE → OPERATE → LEARN → IMPROVE
    """
    
    def __init__(self, config: Veo31SystemConfig):
        """
        Initialize unified system.
        
        Args:
            config: System configuration
        """
        self.config = config
        self.logger = logging.getLogger(f"{__name__}.Veo31UnifiedSystem")
        
        # Core components (always initialized)
        self.prompt_engine = Veo31PromptEngine()
        self.cdf_index = Veo31CDFIndex(config.cdf_storage_path)
        self.validator = Veo31Validator()
        
        # Optional components
        self.api_client: Optional[RunwayAPIClient] = None
        self.director_agent: Optional[Veo31DirectorAgent] = None
        self.pattern_learner: Optional[Veo31PatternLearner] = None
        self.metrics_collector: Optional[Veo31MetricsCollector] = None
        
        # State
        self._initialized = False
        self._activated = False
    
    async def initialize(self) -> bool:
        """
        Initialize all components.
        
        Pattern: INITIALIZE → VALIDATE → READY
        
        Returns:
            True if initialization successful
        """
        if self._initialized:
            return True
        
        try:
            self.logger.info(" Initializing Veo31 Unified System...")
            
            # Initialize API Client
            if self.config.enable_api_client and self.config.runway_api_key:
                self.api_client = RunwayAPIClient(self.config.runway_api_key)
                await self.api_client.initialize()
                self.logger.info(" Runway API Client initialized")
            
            # Initialize Director Agent
            if self.config.enable_director_agent and self.config.llm_client:
                director_config = DirectorAgentConfig(
                    llm_client=self.config.llm_client,
                    system_prompt_builder=self.config.system_prompt_builder
                )
                self.director_agent = Veo31DirectorAgent(director_config)
                self.logger.info(" Director Agent initialized")
            
            # Initialize Pattern Learner
            if self.config.enable_pattern_learning:
                self.pattern_learner = Veo31PatternLearner(self.config.pattern_storage_path)
                self.logger.info(" Pattern Learner initialized")
            
            # Initialize Metrics Collector
            if self.config.enable_metrics:
                self.metrics_collector = Veo31MetricsCollector()
                self.logger.info(" Metrics Collector initialized")
            
            self._initialized = True
            self.logger.info(" Veo31 Unified System initialized")
            return True
        
        except Exception as e:
            self.logger.error(f" Initialization failed: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            return False
    
    async def activate(self) -> bool:
        """
        Activate system (post-initialization setup).
        
        Pattern: ACTIVATE → VALIDATE → OPERATIONAL
        
        Returns:
            True if activation successful
        """
        if not self._initialized:
            if not await self.initialize():
                return False
        
        if self._activated:
            return True
        
        try:
            self.logger.info(" Activating Veo31 Unified System...")
            
            # Load learned patterns
            if self.pattern_learner:
                # Patterns are auto-loaded on init
                pattern_count = len(self.pattern_learner.learned_patterns)
                self.logger.info(f" Loaded {pattern_count} learned patterns")
            
            # Validate system health
            health = self.get_system_health()
            if health["status"] != "healthy":
                self.logger.warning(f" System health check: {health['status']}")
            
            self._activated = True
            self.logger.info(" Veo31 Unified System activated")
            return True
        
        except Exception as e:
            self.logger.error(f" Activation failed: {e}")
            return False
    
    async def generate_video(
        self,
        concept: str,
        character_bibles: Optional[List] = None,
        use_director_agent: bool = True,
        model: str = "veo3.1",
        duration: int = 5
    ) -> Dict[str, Any]:
        """
        Generate video from concept (high-level interface).
        
        Pattern: CONCEPT → DIRECTOR → PROMPT → VALIDATE → GENERATE → LEARN
        
        Args:
            concept: High-level creative concept
            character_bibles: Optional Character Bibles
            use_director_agent: Use Director Agent to generate prompt
            model: Model to use
            duration: Duration in seconds
        
        Returns:
            Generation result
        """
        if not self._activated:
            await self.activate()
        
        generation_id = f"gen_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            # Step 1: Generate Layered Prompt
            if use_director_agent and self.director_agent:
                layered_prompt = await self.director_agent.generate_layered_prompt(
                    concept,
                    character_bibles
                )
                if not layered_prompt:
                    return {
                        "success": False,
                        "error": "Failed to generate layered prompt"
                    }
            else:
                # Manual prompt (placeholder - would need user input)
                return {
                    "success": False,
                    "error": "Manual prompt generation not implemented"
                }
            
            # Step 2: Validate prompt
            validation = self.validator.validate_layered_prompt(layered_prompt)
            if not validation.is_valid:
                return {
                    "success": False,
                    "error": f"Prompt validation failed: {validation.errors}",
                    "warnings": validation.warnings
                }
            
            # Step 3: Get suggestions from pattern learner
            suggestions = []
            if self.pattern_learner:
                config = Veo31PromptConfig(model=model, duration=duration)
                suggestions = self.pattern_learner.suggest_improvements(layered_prompt, config)
            
            # Step 4: Generate workflow/config
            config = Veo31PromptConfig(
                model=model,
                duration=duration,
                layered_prompt=layered_prompt
            )
            workflow_payload = self.prompt_engine.generate_runway_workflow_payload(config)
            
            # Step 5: Execute via API (if available)
            result = None
            if self.api_client:
                if config.use_workflow:
                    api_result = await self.api_client.execute_workflow(workflow_payload)
                else:
                    # Direct API call
                    api_result = await self.api_client.image_to_video(
                        prompt_image=config.primary_subject.reference_images[0] if config.primary_subject else "",
                        prompt_text=layered_prompt.to_prompt_text(),
                        model=model,
                        duration=duration
                    )
                
                result = {
                    "success": api_result.success,
                    "request_id": api_result.request_id,
                    "credits_used": api_result.credits_used,
                    "error": api_result.error
                }
            
            # Step 6: Record for learning
            if self.pattern_learner and self.metrics_collector:
                from .veo31_pattern_learner import PromptGenerationResult
                
                gen_result = PromptGenerationResult(
                    success=result["success"] if result else False,
                    prompt_used=layered_prompt.to_dict(),
                    timestamp=datetime.now()
                )
                
                self.pattern_learner.record_generation(layered_prompt, config, gen_result)
                
                self.metrics_collector.record_generation(
                    generation_id=generation_id,
                    prompt_type="layered_prompt",
                    model=model,
                    success=gen_result.success,
                    credits_used=result.get("credits_used") if result else None
                )
            
            return {
                "success": result["success"] if result else True,
                "generation_id": generation_id,
                "layered_prompt": layered_prompt.to_dict(),
                "validation": {
                    "is_valid": validation.is_valid,
                    "score": validation.score,
                    "warnings": validation.warnings
                },
                "suggestions": suggestions,
                "workflow_payload": workflow_payload,
                "api_result": result
            }
        
        except Exception as e:
            self.logger.error(f"Generation failed: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get system health status"""
        components = {
            "prompt_engine": True,
            "cdf_index": True,
            "validator": True,
            "api_client": self.api_client is not None,
            "director_agent": self.director_agent is not None,
            "pattern_learner": self.pattern_learner is not None,
            "metrics_collector": self.metrics_collector is not None
        }
        
        healthy_count = sum(components.values())
        total_count = len(components)
        
        return {
            "status": "healthy" if healthy_count == total_count else "degraded",
            "components": components,
            "initialized": self._initialized,
            "activated": self._activated,
            "health_score": healthy_count / total_count
        }
    
    def get_effectiveness_report(self) -> Dict[str, Any]:
        """Get complete effectiveness report"""
        report = {
            "system_health": self.get_system_health(),
            "metrics": None,
            "learned_patterns": None
        }
        
        if self.metrics_collector:
            report["metrics"] = self.metrics_collector.get_effectiveness_report()
        
        if self.pattern_learner:
            report["learned_patterns"] = {
                "total_patterns": len(self.pattern_learner.learned_patterns),
                "best_patterns": [
                    p.to_dict() for p in self.pattern_learner.get_best_patterns()[:5]
                ]
            }
        
        return report
    
    async def shutdown(self) -> None:
        """Shutdown system gracefully"""
        self.logger.info("Shutting down Veo31 Unified System...")
        
        if self.api_client:
            await self.api_client.close()
        
        if self.pattern_learner:
            self.pattern_learner._save_patterns()
        
        self._activated = False
        self.logger.info(" Veo31 Unified System shutdown complete")


# Factory function for easy initialization
async def create_veo31_system(
    runway_api_key: Optional[str] = None,
    llm_client: Optional[Any] = None,
    system_prompt_builder: Optional[Any] = None,
    auto_activate: bool = True
) -> Veo31UnifiedSystem:
    """
    Factory: Create and initialize Veo31 Unified System.
    
    Args:
        runway_api_key: Runway API key
        llm_client: LLM client for Director Agent
        system_prompt_builder: SystemPromptBuilder instance
        auto_activate: Automatically activate after initialization
    
    Returns:
        Initialized Veo31UnifiedSystem
    """
    config = Veo31SystemConfig(
        runway_api_key=runway_api_key,
        llm_client=llm_client,
        system_prompt_builder=system_prompt_builder,
        enable_director_agent=llm_client is not None,
        enable_api_client=runway_api_key is not None
    )
    
    system = Veo31UnifiedSystem(config)
    
    if await system.initialize():
        if auto_activate:
            await system.activate()
        return system
    else:
        raise RuntimeError("Failed to initialize Veo31 Unified System")

