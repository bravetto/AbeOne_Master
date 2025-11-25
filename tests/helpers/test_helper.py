#!/usr/bin/env python3
"""
Helper script to test containers from within Docker network
Usage: docker run --rm --network aiguards-network -v $(pwd):/app python:3.11-slim python /app/test_helper.py <container_name> <port> <endpoint> <method> [payload_json]
"""

import sys
import json
import httpx

if len(sys.argv) < 5:
    print(json.dumps({"status": "error", "error": "Usage: test_helper.py <container_name> <port> <endpoint> <method> [payload_json]"}))
    sys.exit(1)

container_name = sys.argv[1]
port = sys.argv[2]
endpoint = sys.argv[3]
method = sys.argv[4].upper()
payload_json = sys.argv[5] if len(sys.argv) > 5 else None

url = f"http://{container_name}:{port}{endpoint}"

try:
    headers = {"Content-Type": "application/json"}
    payload = None
    
    if payload_json:
        payload = json.loads(payload_json)
    
    if method == "GET":
        response = httpx.get(url, headers=headers, timeout=30)
    elif method == "POST":
        response = httpx.post(url, json=payload, headers=headers, timeout=30)
    else:
        print(json.dumps({"status": "error", "error": f"Unsupported method: {method}"}))
        sys.exit(1)
    
    result = {"status": response.status_code}
    try:
        result["data"] = response.json()
    except:
        result["text"] = response.text[:1000]
    
    print(json.dumps(result))
    
except Exception as e:
    print(json.dumps({"status": "error", "error": str(e)}))
    sys.exit(1)

