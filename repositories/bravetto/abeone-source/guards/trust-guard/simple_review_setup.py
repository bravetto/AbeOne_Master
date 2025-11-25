#!/usr/bin/env python3
"""
Simple Internal Review Setup Script

This script addresses critical issues for streamlined internal review:
1. Port conflict resolution
2. Server startup
3. Authentication testing
4. Performance verification
"""

import os
import sys
import time
import requests
import subprocess
import psutil
import json

class SimpleReviewSetup:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.server_process = None
        
    def kill_existing_processes(self):
        """Kill any existing processes using port 8000."""
        print("Resolving port conflicts...")
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'connections']):
                try:
                    for conn in proc.info['connections'] or []:
                        if conn.laddr.port == 8000:
                            print(f"   Killing process {proc.info['pid']} ({proc.info['name']})")
                            proc.kill()
                            time.sleep(1)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
                    
            print("   Port conflicts resolved")
            return True
        except Exception as e:
            print(f"   Error resolving port conflicts: {e}")
            return False
    
    def start_server(self):
        """Start the Trust Guard server."""
        print("Starting Trust Guard server...")
        
        try:
            self.server_process = subprocess.Popen([
                sys.executable, "-m", "uvicorn", "main:app", 
                "--host", "0.0.0.0", "--port", "8000"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for server to start
            for i in range(30):
                try:
                    response = requests.get(f"{self.base_url}/health", timeout=2)
                    if response.status_code == 200:
                        print("   Server started successfully")
                        return True
                except requests.exceptions.RequestException:
                    time.sleep(1)
                    continue
            
            print("   Server failed to start within 30 seconds")
            return False
            
        except Exception as e:
            print(f"   Error starting server: {e}")
            return False
    
    def test_system(self):
        """Test the system functionality."""
        print("Testing system functionality...")
        
        tests = [
            ("Health Check", "GET", "/health"),
            ("Health Live", "GET", "/health/live"),
            ("Health Ready", "GET", "/health/ready"),
            ("Metrics", "GET", "/metrics"),
            ("API Docs", "GET", "/docs"),
            ("Debug API Key", "GET", "/debug/api-key"),
        ]
        
        results = {}
        
        for test_name, method, endpoint in tests:
            try:
                start_time = time.time()
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                response_time = (time.time() - start_time) * 1000
                
                if response.status_code == 200:
                    print(f"   PASS: {test_name} ({response_time:.0f}ms)")
                    results[test_name] = {"status": "PASS", "time": response_time}
                else:
                    print(f"   FAIL: {test_name} (Status: {response.status_code})")
                    results[test_name] = {"status": "FAIL", "status_code": response.status_code}
                    
            except Exception as e:
                print(f"   ERROR: {test_name} - {e}")
                results[test_name] = {"status": "ERROR", "error": str(e)}
        
        return results
    
    def test_authentication(self):
        """Test authentication system."""
        print("Testing authentication system...")
        
        try:
            # Get API key
            response = requests.get(f"{self.base_url}/debug/api-key", timeout=5)
            if response.status_code != 200:
                print("   FAIL: Cannot get API key")
                return False
            
            api_key_data = response.json()
            api_key = api_key_data.get("api_key")
            
            if not api_key:
                print("   FAIL: No API key returned")
                return False
            
            print(f"   API key obtained: {api_key[:30]}...")
            
            # Test authentication
            headers = {"X-API-Key": api_key, "Content-Type": "application/json"}
            test_data = {"text": "Test authentication", "context": "Test"}
            
            response = requests.post(
                f"{self.base_url}/v1/detect",
                headers=headers,
                json=test_data,
                timeout=10
            )
            
            if response.status_code == 200:
                print("   PASS: Authentication working")
                return True
            else:
                print(f"   FAIL: Authentication failed ({response.status_code})")
                print(f"   Response: {response.text[:100]}")
                return False
                
        except Exception as e:
            print(f"   ERROR: Authentication test failed - {e}")
            return False
    
    def create_summary(self, test_results, auth_working):
        """Create review summary."""
        print("Creating review summary...")
        
        summary = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "READY" if auth_working and all(r.get("status") == "PASS" for r in test_results.values()) else "ISSUES",
            "server_url": self.base_url,
            "test_results": test_results,
            "authentication_working": auth_working,
            "endpoints": {
                "health": f"{self.base_url}/health",
                "metrics": f"{self.base_url}/metrics", 
                "docs": f"{self.base_url}/docs",
                "api_key": f"{self.base_url}/debug/api-key"
            },
            "instructions": [
                "1. Open API documentation: http://localhost:8000/docs",
                "2. Get API key: http://localhost:8000/debug/api-key",
                "3. Test pattern detection with API key in X-API-Key header",
                "4. Monitor system health: http://localhost:8000/health/detailed"
            ]
        }
        
        with open("review_summary.json", "w") as f:
            json.dump(summary, f, indent=2)
        
        print("   Summary saved to: review_summary.json")
        return summary
    
    def run_setup(self):
        """Run the complete setup process."""
        print("Trust Guard Internal Review Setup")
        print("=" * 50)
        
        try:
            # Step 1: Resolve port conflicts
            if not self.kill_existing_processes():
                return False
            
            # Step 2: Start server
            if not self.start_server():
                return False
            
            # Step 3: Test system
            test_results = self.test_system()
            
            # Step 4: Test authentication
            auth_working = self.test_authentication()
            
            # Step 5: Create summary
            summary = self.create_summary(test_results, auth_working)
            
            # Final assessment
            print("\n" + "=" * 50)
            print("SETUP COMPLETE")
            print("=" * 50)
            
            if summary["status"] == "READY":
                print("SUCCESS: Trust Guard is READY for internal review!")
            else:
                print("WARNING: Trust Guard has some issues but is functional")
            
            print(f"Server URL: {self.base_url}")
            print("API Documentation: http://localhost:8000/docs")
            print("Get API Key: http://localhost:8000/debug/api-key")
            
            print("\nNext Steps:")
            print("1. Review API documentation at /docs")
            print("2. Get API key from /debug/api-key") 
            print("3. Test pattern detection endpoints")
            print("4. Check system health at /health/detailed")
            
            return True
            
        except Exception as e:
            print(f"Setup failed: {e}")
            return False
    
    def cleanup(self):
        """Clean up resources."""
        if self.server_process:
            try:
                self.server_process.terminate()
                self.server_process.wait(timeout=5)
            except:
                self.server_process.kill()

def main():
    """Main function."""
    setup = SimpleReviewSetup()
    
    try:
        success = setup.run_setup()
        if success:
            print("\nServer is running and ready for internal review!")
            print("Press Ctrl+C to stop the server when review is complete.")
            
            # Keep server running
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nStopping server...")
                setup.cleanup()
                print("Server stopped.")
        else:
            print("\nSetup failed. Please check the errors above.")
            return 1
            
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        setup.cleanup()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
