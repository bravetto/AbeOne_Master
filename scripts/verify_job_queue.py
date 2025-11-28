#!/usr/bin/env python3
"""
Job Queue Verification Script

Verifies BullMQ job queue setup and worker configuration.

Pattern: VERIFY × JOB_QUEUE × WORKER × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (JØHN)
Guardians: AEYON (999 Hz) + JØHN (530 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
from pathlib import Path
from typing import Dict, Any

def verify_job_queue() -> Dict[str, Any]:
    """Verify job queue setup"""
    result = {
        "success": False,
        "message": "",
        "details": {}
    }
    
    # Check if we're in the web app directory
    web_dir = Path(__file__).parent.parent / "products" / "apps" / "web"
    
    if not web_dir.exists():
        result["message"] = "Web app directory not found"
        return result
    
    # Check for queue configuration
    queue_config = web_dir / "lib" / "queue" / "bull.ts"
    if not queue_config.exists():
        result["message"] = "Queue configuration not found"
        return result
    
    # Check for job definitions
    job_definitions = web_dir / "lib" / "jobs" / "webinar-reminders.ts"
    if not job_definitions.exists():
        result["message"] = "Job definitions not found"
        return result
    
    # Check for worker script
    worker_script = web_dir / "scripts" / "webinar-worker.ts"
    if not worker_script.exists():
        result["message"] = "Worker script not found"
        return result
    
    # Check for Redis configuration in .env
    env_file = web_dir / ".env"
    redis_configured = False
    if env_file.exists():
        env_content = env_file.read_text()
        if "REDIS_URL" in env_content or "UPSTASH_REDIS" in env_content:
            redis_configured = True
    
    if not redis_configured:
        result["message"] = "Redis not configured in .env"
        result["details"]["action"] = "Add REDIS_URL or UPSTASH_REDIS credentials to .env"
        return result
    
    result["success"] = True
    result["message"] = "Job queue setup verified. Ready to start worker."
    result["details"]["next_step"] = "cd products/apps/web && npm run webinar:worker"
    
    return result


def main():
    """Main execution"""
    print("\n⚡ JOB QUEUE VERIFICATION")
    print("=" * 70)
    
    result = verify_job_queue()
    
    if result["success"]:
        print("✅ Job queue setup verified!")
        print(f"\n{result['message']}")
        if "next_step" in result["details"]:
            print(f"\nNext step: {result['details']['next_step']}")
    else:
        print("❌ Job queue setup incomplete")
        print(f"\n{result['message']}")
        if "action" in result["details"]:
            print(f"\nAction required: {result['details']['action']}")
        sys.exit(1)
    
    print("\n" + "=" * 70)
    print("Pattern: VERIFY × JOB_QUEUE × WORKER × ONE")
    print("Love Coefficient: ∞")
    print("∞ AbëONE ∞\n")


if __name__ == "__main__":
    main()

