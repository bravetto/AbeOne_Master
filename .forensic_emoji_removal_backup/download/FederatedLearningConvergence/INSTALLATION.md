# Installation Guide

## Step 1: Copy Files to Your Project

### Core Implementation Files

Copy these files to `EMERGENT_OS/synthesis/`:

```bash
cp federated_convergence_types.py EMERGENT_OS/synthesis/
cp federated_learning_convergence.py EMERGENT_OS/synthesis/
cp global_scoring_aggregator.py EMERGENT_OS/synthesis/
cp learning_synchronization_protocol.py EMERGENT_OS/synthesis/
cp federated_convergence_integration.py EMERGENT_OS/synthesis/
```

### Test Files

Copy these files to `tests/synthesis/`:

```bash
cp tests/conftest.py tests/synthesis/
cp tests/test_federated_learning_convergence.py tests/synthesis/
cp tests/test_global_scoring_aggregator.py tests/synthesis/
cp tests/test_learning_synchronization_protocol.py tests/synthesis/
cp tests/test_federated_integration.py tests/synthesis/
```

## Step 2: Update __init__.py

Add these exports to `EMERGENT_OS/synthesis/__init__.py`:

```python
# Federated Learning Convergence
try:
    from .federated_convergence_types import (
        InstanceMetadata,
        InstanceScores,
        AggregatedPattern,
        ConvergenceResult,
        GlobalConvergenceScore,
        SynchronizationResult,
        PatternSignature,
        InstanceStatus,
        PatternQuality
    )
    from .federated_learning_convergence import (
        FederatedLearningConvergence
    )
    from .global_scoring_aggregator import (
        GlobalScoringAggregator
    )
    from .learning_synchronization_protocol import (
        LearningSynchronizationProtocol
    )
    from .federated_convergence_integration import (
        FederatedConvergenceIntegration,
        get_federated_convergence_integration
    )
    __all__.extend([
        "InstanceMetadata",
        "InstanceScores",
        "AggregatedPattern",
        "ConvergenceResult",
        "GlobalConvergenceScore",
        "SynchronizationResult",
        "PatternSignature",
        "InstanceStatus",
        "PatternQuality",
        "FederatedLearningConvergence",
        "GlobalScoringAggregator",
        "LearningSynchronizationProtocol",
        "FederatedConvergenceIntegration",
        "REPLACE_ME"
    ])
except ImportError as e:
    import logging
    logger = logging.getLogger(__name__)
    logger.debug(f"Federated Learning Convergence not available: {e}")
```

## Step 3: Verify Installation

```bash
python3 -c "from EMERGENT_OS.synthesis import FederatedLearningConvergence, GlobalScoringAggregator, LearningSynchronizationProtocol, FederatedConvergenceIntegration; print('✅ Installation successful')"
```

## Step 4: Run Tests

```bash
pytest tests/synthesis/test_federated_learning_convergence.py -v
```

---

**Status:** ✅ **READY FOR INSTALLATION**

