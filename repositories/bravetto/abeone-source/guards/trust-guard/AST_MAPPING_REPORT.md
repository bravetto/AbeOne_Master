# Trust Guard AST-Based Dependency and Integration Mapping
============================================================

##  Project Structure
### Main Modules
- `main.py`

### Core Modules
- `trustguard\config.py`
- `trustguard\constitutional.py`
- `trustguard\core.py`
- `trustguard\logging.py`
- `trustguard\metrics.py`
- `trustguard\validation.py`
- `trustguard\__init__.py`

### Test Modules
- `tests\__init__.py`
- `tests\integration\test_api.py`
- `tests\patterns\test_fallbacks.py`
- `tests\performance\test_flow_tracing.py`
- `tests\unit\test_core.py`
- `tests\unit\test_validation.py`

##  Dependencies
### External Dependencies (30)
- `argparse`
- `ast`
- `asyncio`
- `collections`
- `config`
- `constitutional`
- `core`
- `fastapi`
- `importlib`
- `inspect`
- `json`
- `logging`
- `math`
- `metrics`
- `os`
- `pathlib`
- `prometheus_fastapi_instrumentator`
- `psutil`
- `pydantic`
- `pydantic_settings`
- `pythonjsonlogger`
- `re`
- `requests`
- `slowapi`
- `statistics`
- `sys`
- `time`
- `typing`
- `uvicorn`
- `validation`

### Internal Dependencies
- `trustguard.__init__`
- `trustguard.config`
- `trustguard.constitutional`
- `trustguard.core`
- `trustguard.logging`
- `trustguard.metrics`
- `trustguard.validation`

### Dependency Categories
#### Web Framework
- `uvicorn`
- `fastapi`

#### Logging
- `logging`

#### Monitoring
- `metrics`

#### Other
- `asyncio`
- `sys`
- `time`
- `core`
- `prometheus_fastapi_instrumentator`
- `argparse`
- `config`
- `constitutional`
- `typing`
- `ast`
- `slowapi`
- `validation`
- `pydantic`
- `inspect`
- `pydantic_settings`
- `math`
- `re`
- `pythonjsonlogger`
- `json`
- `statistics`
- `pathlib`
- `os`
- `requests`
- `collections`
- `importlib`
- `psutil`

##  Integrations
### Api Integrations
- HTTP Client

### Monitoring Integrations
- Prometheus
- Prometheus

### Deployment Integrations
- AWS

### Logging Integrations
- Structured Logging

##  Core Functionality
### Pattern Detectors
- **TrustGuardDetector** (`trustguard\core.py`)
  - Methods: __init__, is_healthy, detect_all_patterns, detect_hallucination, detect_drift, detect_bias, detect_deception, detect_security_theater, detect_duplication, detect_stub_syndrome
- **HallucinationDetector** (`trustguard\core.py`)
  - Methods: detect
- **DriftDetector** (`trustguard\core.py`)
  - Methods: detect
- **BiasDetector** (`trustguard\core.py`)
  - Methods: __init__, detect
- **DeceptionDetector** (`trustguard\core.py`)
  - Methods: detect
- **SecurityTheaterDetector** (`trustguard\core.py`)
  - Methods: detect
- **DuplicationDetector** (`trustguard\core.py`)
  - Methods: detect, _analyze_structure_similarity
- **StubSyndromeDetector** (`trustguard\core.py`)
  - Methods: detect

### Validation Engines
- **ValidationRequest** (`main.py`)
  - Methods: 
- **ValidationResponse** (`main.py`)
  - Methods: 
- **ValidationEngine** (`trustguard\validation.py`)
  - Methods: __init__, is_healthy, perform_mathematical_validation, calculate_risk_assessment, generate_evidence, _calculate_kl_divergence, _quantify_uncertainty, _check_information_consistency, _perform_statistical_analysis, _calculate_confidence_intervals, _extract_word_frequencies, _get_risk_description, _calculate_evidence_confidence

### Mitigation Strategies
- **MitigationRequest** (`main.py`)
  - Methods: 
- **ConstitutionalPrompting** (`trustguard\constitutional.py`)
  - Methods: __init__, is_healthy, apply_mitigation, generate_constitutional_prompts, generate_recommendations, _generate_mitigation_prompts, _apply_constitutional_enhancements, _wrap_with_constitutional_guidance, _estimate_confidence_improvement, _get_pattern_recommendations

### Metrics Collectors
- **ReliabilityMetrics** (`trustguard\metrics.py`)
  - Methods: __init__, reset, record_detection, record_validation, record_mitigation, get_total_validations, get_total_detections, get_total_mitigations, get_average_risk_score, get_patterns_detected_today, get_pattern_statistics, get_reliability_trends, _risk_level_to_score, is_healthy, get_metrics_summary

##  API Endpoints
