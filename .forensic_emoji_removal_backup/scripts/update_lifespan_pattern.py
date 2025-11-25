#!/usr/bin/env python3
"""
Update all guardian services to use Ben's modern @asynccontextmanager lifespan pattern
instead of deprecated @app.on_event("startup")
"""

import os
import re
from pathlib import Path

BASE_DIR = Path("/Users/michaelmataluni/Documents/AbeOne_Master/AIGuards-Backend/aiguardian-repos")

GUARDIAN_SERVICES = [
    "guardian-aeyon-service",
    "guardian-abe-service",
    "guardian-aurion-service",
    "guardian-john-service",
    "guardian-lux-service",
    "guardian-neuro-service",
    "guardian-yagni-service",
]

def update_service(service_dir: Path):
    """Update a single service to use lifespan pattern."""
    service_file = service_dir / "service.py"
    
    if not service_file.exists():
        print(f"⚠️  {service_dir.name}: service.py not found")
        return False
    
    content = service_file.read_text()
    
    # Check if already updated
    if "from contextlib import asynccontextmanager" in content and "lifespan=lifespan" in content:
        print(f"✅ {service_dir.name}: Already updated")
        return True
    
    # Extract guardian info from GUARDIAN_IDENTITY
    guardian_match = re.search(r'"name":\s*"([^"]+)"', content)
    frequency_match = re.search(r'"frequency":\s*(\d+)', content)
    role_match = re.search(r'"role":\s*"([^"]+)"', content)
    
    guardian_name = guardian_match.group(1) if guardian_match else "Guardian"
    frequency = frequency_match.group(1) if frequency_match else "530"
    role = role_match.group(1) if role_match else "Guardian"
    
    # Extract startup event content
    startup_match = re.search(
        r'@app\.on_event\("startup"\)\s+async def startup_event\(\):.*?"""([^"]*)"""\s+(.*?)(?=\nif __name__)',
        content,
        re.DOTALL
    )
    
    if not startup_match:
        print(f"⚠️  {service_dir.name}: Could not find startup event")
        return False
    
    startup_content = startup_match.group(2).strip()
    
    # 1. Add imports
    if "from typing import" in content and "AsyncGenerator" not in content:
        content = content.replace(
            "from typing import List, Dict, Optional, Any",
            "from typing import List, Dict, Optional, Any, AsyncGenerator"
        )
    elif "from typing import" not in content:
        # Find the last import line
        import_match = re.search(r'(from fastapi import.*?\n)', content)
        if import_match:
            content = content.replace(
                import_match.group(1),
                import_match.group(1) + "from typing import AsyncGenerator\n"
            )
    
    if "from contextlib import asynccontextmanager" not in content:
        # Add after other imports
        import_line = "from contextlib import asynccontextmanager\n"
        # Find last import line
        lines = content.split('\n')
        last_import_idx = 0
        for i, line in enumerate(lines):
            if line.startswith(('import ', 'from ')):
                last_import_idx = i
        lines.insert(last_import_idx + 1, import_line)
        content = '\n'.join(lines)
    
    # 2. Create lifespan function before app creation
    lifespan_function = f'''# ============================================================================
# LIFESPAN MANAGEMENT (Ben's Modern Pattern)
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager with graceful startup and shutdown."""
    # Startup
{startup_content}
    
    yield
    
    # Shutdown
    print("🛑 {guardian_name} shutting down gracefully...")

'''
    
    # Find where to insert (before app = FastAPI)
    app_match = re.search(r'(else:.*?\n.*?print\([^)]+\)\n)\n(app = FastAPI\()', content, re.DOTALL)
    if app_match:
        content = content.replace(
            app_match.group(0),
            app_match.group(1) + "\n" + lifespan_function + app_match.group(2)
        )
    else:
        # Fallback: insert before first "app = FastAPI"
        app_pos = content.find("app = FastAPI(")
        if app_pos > 0:
            content = content[:app_pos] + lifespan_function + content[app_pos:]
    
    # 3. Update app creation to include lifespan
    if 'lifespan=lifespan' not in content:
        content = re.sub(
            r'(app = FastAPI\([^)]+)\)',
            r'\1,\n    lifespan=lifespan\n)',
            content,
            count=1
        )
    
    # 4. Remove @app.on_event("startup") section
    content = re.sub(
        r'# ============================================================================\n# STARTUP\n# ============================================================================\n\n@app\.on_event\("startup"\)\s+async def startup_event\(\):.*?(?=\nif __name__)',
        '',
        content,
        flags=re.DOTALL
    )
    
    # Write updated content
    service_file.write_text(content)
    print(f"✅ {service_dir.name}: Updated successfully")
    return True

def main():
    """Update all guardian services."""
    print("🔥 Updating guardian services to use Ben's modern lifespan pattern...\n")
    
    updated = 0
    for service_name in GUARDIAN_SERVICES:
        service_dir = BASE_DIR / service_name
        if update_service(service_dir):
            updated += 1
    
    print(f"\n✅ Updated {updated}/{len(GUARDIAN_SERVICES)} services")
    print("🎯 All services now use @asynccontextmanager lifespan pattern!")

if __name__ == "__main__":
    main()

