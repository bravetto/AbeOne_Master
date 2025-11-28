import requests
import json

# Define the endpoint URL
url = "http://localhost:8000/analyze"

# Define the request payload
payload = {
    "samples": [
        {"id": "1", "text": "This is a benign sample."},
        {"id": "2", "text": "This sample contains a malicious keyword."},
    ]
}

# Send the POST request
response = requests.post(url, json=payload)

# Print the response
print(f"Status Code: {response.status_code}")
print("Response JSON:")
print(json.dumps(response.json(), indent=2))