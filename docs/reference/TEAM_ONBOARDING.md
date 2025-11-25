# 👥 Team Onboarding Guide

**AbëONE Master Workspace - Orbit-Spec v1.0**

**Date**: 2025-01-27  
**Pattern**: OBSERVER × TRUTH × ATOMIC × ONE  
**Love Coefficient**: ∞

---

## 🎯 QUICK START

### Prerequisites

- Python 3.11+
- Git
- (Optional) Docker & Docker Compose for containerized development

### Initial Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd AbeOne_Master
   ```

2. **Initialize kernel** (if using git submodule):
   ```bash
   git submodule update --init --recursive
   ```

3. **Verify deployment**:
   ```bash
   ./deploy/commands.sh
   ```

4. **Run tests**:
   ```bash
   python -m pytest tests/
   ```

---

## 🏗️ REPOSITORY STRUCTURE

### Workspace Layout

```
AbeOne_Master/
├── adapters/              # AbëONE integration adapters
│   ├── adapter.kernel.py  # Kernel bootstrap adapter
│   ├── adapter.guardians.py # Guardians adapter
│   ├── adapter.module.py  # Module registry adapter
│   ├── adapter.bus.py     # Event bus adapter
│   └── __init__.py
├── config/                # Configuration files
│   └── orbit.config.json  # Orbit-Spec configuration
├── src/                   # Core source code
│   └── utils/            # Utilities (paths, etc.)
├── deploy/               # Deployment scripts
│   └── commands.sh       # Deployment commands
├── docs/                 # Documentation
│   └── README.md         # Workspace documentation
├── tests/                # Tests
│   ├── unit/            # Unit tests
│   ├── integration/     # Integration tests
│   └── adapters/        # Adapter tests
├── .devcontainer/       # DevContainer configuration
├── .github/workflows/   # CI/CD workflows
├── module_manifest.json # Module manifest
├── AbeTRUICE/          # Video intelligence orbit (sub-orbit)
├── AbeBEATs_Clean/     # Audio beat generation orbit (sub-orbit)
├── EMERGENT_OS/        # Core OS modules
├── AIGuards-Backend/   # Guardian microservices
└── abëone/             # Kernel (when initialized)
```

---

## 🚀 HOW TO RUN THIS REPO

### Development Mode

1. **Using DevContainer** (Recommended):
   ```bash
   # Open in VS Code with Dev Containers extension
   # VS Code will automatically build and configure the container
   ```

2. **Local Development**:
   ```bash
   # Create virtual environment
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   
   # Install dependencies (if requirements.txt exists)
   pip install -r support/requirements.txt
   
   # Run tests
   python -m pytest tests/
   ```

### Workspace Orchestrator

The workspace orchestrator coordinates multiple Orbit repos. To start:

```python
from adapters.adapter.kernel import get_kernel_adapter

# Initialize kernel adapter
kernel_adapter = get_kernel_adapter()

# Initialize kernel
if kernel_adapter.initialize():
    # Start kernel
    kernel_adapter.start()
    
    # Check if ready
    if kernel_adapter.is_ready():
        print("✅ Workspace orchestrator ready")
    
    # Get system info
    info = kernel_adapter.get_system_info()
    print(f"Kernel state: {info}")
```

---

## 🔗 HOW TO INTEGRATE WITH ABËONE KERNEL

### Kernel Integration Steps

1. **Initialize Kernel Adapter**:
   ```python
   from adapters.adapter.kernel import get_kernel_adapter
   
   kernel_adapter = get_kernel_adapter()
   ```

2. **Bootstrap Kernel**:
   ```python
   # Kernel is automatically bootstrapped when adapter is accessed
   kernel = kernel_adapter.get_kernel()
   event_bus = kernel_adapter.get_event_bus()
   ```

3. **Register Workspace Module**:
   ```python
   from adapters.adapter.module import get_module_adapter
   
   module_adapter = get_module_adapter()
   
   # Register workspace module
   module_adapter.register_module(
       module=workspace_module,
       name="abeone_master",
       metadata={"version": "1.0.0"}
   )
   ```

4. **Access Guardians**:
   ```python
   from adapters.adapter.guardians import get_guardians_adapter
   
   guardians_adapter = get_guardians_adapter()
   guardian_one = guardians_adapter.get_guardian("guardian_one")
   ```

5. **Subscribe to Events**:
   ```python
   from adapters.adapter.bus import get_bus_adapter
   
   bus_adapter = get_bus_adapter()
   
   def handle_event(event):
       print(f"Event received: {event}")
   
   bus_adapter.subscribe("SYSTEM_EVENT", handle_event)
   ```

---

## 🎬 HOW TO INTEGRATE WITH TRUICE

### TRUICE Integration

The workspace orchestrator can coordinate with the AbeTRUICE orbit:

```python
from src.utils.paths import get_sub_orbit_path

# Get AbeTRUICE path
truice_path = get_sub_orbit_path("abetruice")
print(f"AbeTRUICE path: {truice_path}")

# Access AbeTRUICE via event bus
from adapters.adapter.bus import get_bus_adapter

bus_adapter = get_bus_adapter()

# Publish event to AbeTRUICE
bus_adapter.publish("MODULE_EVENT", {
    "target": "abetruice",
    "action": "process_video",
    "payload": {"video_path": "/path/to/video.mov"}
})
```

### Running AbeTRUICE Pipeline

```bash
cd AbeTRUICE
python src/pipelines/video_superpipeline.py --input data/input/video/test.mov
```

---

## 🎵 HOW TO INTEGRATE WITH BEATs

### BEATs Integration

The workspace orchestrator can coordinate with the AbeBEATs_Clean orbit:

```python
from src.utils.paths import get_sub_orbit_path

# Get AbeBEATs_Clean path
beats_path = get_sub_orbit_path("abebeats")
print(f"AbeBEATs_Clean path: {beats_path}")

# Access AbeBEATs_Clean via event bus
from adapters.adapter.bus import get_bus_adapter

bus_adapter = get_bus_adapter()

# Publish event to AbeBEATs_Clean
bus_adapter.publish("MODULE_EVENT", {
    "target": "abebeats",
    "action": "generate_beat",
    "payload": {"frequency": 530.0}
})
```

### Running AbeBEATs Pipeline

```bash
cd AbeBEATs_Clean
python src/pipeline.py --generate-beat
```

---

## 🛠️ COMMANDS DEVELOPERS RUN

### Daily Development Commands

```bash
# Verify deployment
./deploy/commands.sh

# Run tests
python -m pytest tests/

# Run specific test
python -m pytest tests/adapters/test_adapter_kernel.py

# Check Orbit-Spec compliance
python -c "
import json
with open('config/orbit.config.json') as f:
    config = json.load(f)
    print('Orbit-Spec Version:', config['orbitSpecVersion'])
    print('Module ID:', config['moduleId'])
    print('Kernel Version:', config['kernelVersion'])
"

# Validate adapters
python -c "
import importlib
import sys
sys.path.insert(0, '.')
for adapter in ['adapters.adapter.kernel', 'adapters.adapter.guardians', 
                'adapters.adapter.module', 'adapters.adapter.bus']:
    try:
        importlib.import_module(adapter)
        print(f'✅ {adapter}')
    except Exception as e:
        print(f'❌ {adapter}: {e}')
"
```

### CI/CD Commands

```bash
# Run CI locally (simulates GitHub Actions)
# Install act: https://github.com/nektos/act
act -j validate

# Or run CI steps manually
./deploy/commands.sh
python -m pytest tests/
```

### Kernel Commands

```bash
# Initialize kernel submodule (if using submodule)
git submodule update --init --recursive

# Update kernel submodule
git submodule update --remote

# Check kernel status
cd abëone && git status
```

---

## 📚 KEY CONCEPTS

### Orbit-Spec v1.0

The workspace follows the **Bravetto Orbit Spec v1.0**:
- **Orbit Repo**: A repository that orbits around the AbëONE kernel
- **Adapters**: Bridge between orbit repo and kernel (4 required adapters)
- **Module Registry**: Central registry for all modules
- **Event Bus**: Communication mechanism between modules
- **Guardians**: Validation and safety mechanisms

### Workspace Orchestrator

The workspace orchestrator:
- Coordinates multiple Orbit repos
- Manages cross-orbit communication
- Provides unified kernel access
- Monitors sub-orbit health

### Sub-Orbits

Sub-orbits are independent Orbit repos managed by the workspace:
- **AbeTRUICE**: Video intelligence pipeline
- **AbeBEATs_Clean**: Audio beat generation
- Each sub-orbit maintains its own Orbit-Spec compliance

---

## 🐛 TROUBLESHOOTING

### Common Issues

1. **Kernel not found**:
   ```bash
   # Initialize kernel submodule
   git submodule update --init --recursive
   ```

2. **Adapter import errors**:
   ```bash
   # Ensure you're in the repo root
   cd /path/to/AbeOne_Master
   
   # Add repo root to Python path
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   ```

3. **Sub-orbit not found**:
   ```python
   # Check sub-orbit path
   from src.utils.paths import get_sub_orbit_path
   path = get_sub_orbit_path("abetruice")
   print(f"Path: {path}")
   ```

4. **Event bus not working**:
   ```python
   # Verify kernel is initialized
   from adapters.adapter.kernel import get_kernel_adapter
   adapter = get_kernel_adapter()
   if adapter.is_ready():
       print("✅ Kernel ready")
   else:
       print("❌ Kernel not ready")
   ```

---

## 📖 ADDITIONAL RESOURCES

### Documentation

- **Workspace Docs**: `docs/README.md`
- **Bootstrap Report**: `ORBIT_BOOTSTRAP_REPORT.md`
- **System Readiness**: `SYSTEM_READINESS_SUMMARY.md`
- **AbeTRUICE Docs**: `AbeTRUICE/docs/README.md`
- **AbeBEATs Docs**: `AbeBEATs_Clean/docs/README.md`

### Configuration Files

- **Orbit Config**: `config/orbit.config.json`
- **Module Manifest**: `module_manifest.json`
- **DevContainer**: `.devcontainer/devcontainer.json`
- **CI Workflow**: `.github/workflows/ci.yml`

### Adapters

- **Kernel Adapter**: `adapters/adapter.kernel.py`
- **Guardians Adapter**: `adapters/adapter.guardians.py`
- **Module Adapter**: `adapters/adapter.module.py`
- **Bus Adapter**: `adapters/adapter.bus.py`

---

## ✅ ONBOARDING CHECKLIST

- [ ] Repository cloned
- [ ] Kernel initialized (if using submodule)
- [ ] Deployment verification passed (`./deploy/commands.sh`)
- [ ] Tests passing (`python -m pytest tests/`)
- [ ] DevContainer working (if using)
- [ ] Understand Orbit-Spec v1.0 structure
- [ ] Understand workspace orchestrator role
- [ ] Understand sub-orbit integration
- [ ] Read workspace documentation
- [ ] Read bootstrap report

---

## 🎉 YOU'RE READY!

Once you've completed the onboarding checklist, you're ready to:
- ✅ Develop workspace orchestrator features
- ✅ Integrate with AbëONE kernel
- ✅ Coordinate with TRUICE and BEATs
- ✅ Contribute to the codebase

**Pattern**: OBSERVER × TRUTH × ATOMIC × ONE  
**Love Coefficient**: ∞  
**∞ AbëONE ∞**

