import importlib
import logging
import time
from typing import List, Dict, Any
from .core import DataSample, AnalysisResult
from .plugins.base import BasePlugin
from .monitoring import record_plugin_metrics

logger = logging.getLogger(__name__)


class Analyzer:
    """
    Analyzes data samples to detect potential poisoning using a pluggable architecture.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config.get('analyzer', {})
        self.plugins = self._load_plugins()

    def _load_plugins(self) -> List[BasePlugin]:
        """
        Loads the analysis plugins specified in the configuration.
        """
        plugins = []
        plugin_configs = self.config.get("plugins", [])
        for plugin_config in plugin_configs:
            class_path = plugin_config.get("class", "")
            if not class_path or "." not in class_path:
                logger.error(f"Invalid plugin class path: {class_path}")
                continue
                
            try:
                module_name, class_name = class_path.rsplit(".", 1)
                module = importlib.import_module(f".plugins.{module_name}", package="poisonguard")
                plugin_class = getattr(module, class_name)
                plugins.append(plugin_class(plugin_config.get("config", {})))
                logger.info(f"Successfully loaded plugin: {class_name}")
            except (ImportError, AttributeError) as e:
                logger.error(f"Failed to load plugin {class_path}: {e}")
        return plugins

    def analyze(self, samples: List[DataSample]) -> List[AnalysisResult]:
        """
        Analyzes a list of data samples by running them through the loaded plugins.
        """
        final_results = []
        for sample in samples:
            is_poisoned = False
            total_confidence = 0.0
            all_details = {"reasons": []}

            logger.info(f"Analyzing sample {sample.id}")
            for plugin in self.plugins:
                plugin_start_time = time.time()
                result = plugin.analyze(sample)
                plugin_execution_time = time.time() - plugin_start_time
                
                # Record plugin metrics
                record_plugin_metrics(plugin.__class__.__name__, plugin_execution_time)
                
                if result.is_poisoned:
                    is_poisoned = True
                    total_confidence = max(total_confidence, result.confidence)
                    reasons = result.details.get("reasons", [])
                    all_details["reasons"].extend(reasons)
                    if "model_prediction" in result.details:
                        all_details["model_prediction"] = result.details["model_prediction"]
                    logger.warning(
                        f"Sample {sample.id} flagged as poisoned by {plugin.__class__.__name__}. "
                        f"Reasons: {reasons}. Execution time: {plugin_execution_time:.3f}s"
                    )

            if not all_details["reasons"]:
                all_details["reasons"].append("No suspicious patterns found.")
                logger.info(f"Sample {sample.id} found to be clean.")

            final_results.append(
                AnalysisResult(
                    sample_id=sample.id,
                    is_poisoned=is_poisoned,
                    confidence=total_confidence if is_poisoned else 1.0,
                    details=all_details,
                )
            )
        return final_results