# Shared PoisonGuard Library

This directory contains the shared PoisonGuard library used by both BiasGuard and HealthGuard services.

## Overview

The PoisonGuard library provides common functionality for:
- LLM poisoning detection and analysis
- Data validation and sanitization
- Monitoring and metrics collection
- Plugin-based architecture for extensibility

## Structure

```
shared/
├── guards/
│   └── poisonguard/          # Main library package
│       ├── __init__.py
│       ├── api.py           # FastAPI application and endpoints
│       ├── analyzer.py      # Core analysis logic
│       ├── config_validator.py  # Configuration validation
│       ├── core.py          # Core data models
│       ├── database.py      # Database operations
│       ├── logger.py        # Logging utilities
│       ├── mitigator.py     # Mitigation strategies
│       ├── monitoring.py    # Metrics and monitoring
│       ├── plugins/         # Plugin system
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── heuristics.py
│       │   └── model.py
│       └── reporter.py      # Report generation
├── setup.py                 # Package installation
└── README.md               # This file
```

## Usage

### For BiasGuard
```bash
cd guards/biasguard-backend
pip install -e ../../shared
```

### For HealthGuard
```bash
cd guards/healthguard
pip install -e ../../shared
```

## Dependencies

The shared library includes all necessary dependencies for both services. See `setup.py` for the complete list.

## Development

When making changes to the shared library:
1. Update code in `shared/guards/poisonguard/`
2. Test both BiasGuard and HealthGuard services
3. Update version in `setup.py` if needed

## Services Using This Library

- **BiasGuard**: Bias detection and mitigation for AI models
- **HealthGuard**: System health monitoring and diagnostics

## Notes

- This library is symlinked into both services to avoid duplication
- Changes here affect both BiasGuard and HealthGuard
- All services share the same codebase for core functionality
