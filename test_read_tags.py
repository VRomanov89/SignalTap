#!/usr/bin/env python3
"""
Test script for the new read-tags endpoint
"""

import requests
import json

def test_read_tags_endpoint():
    """Test the new read-tags endpoint"""
    
    # API base URL
    base_url = "http://localhost:8000"
    
    # Test data
    test_request = {
        "ip": "192.168.1.10",
        "slot": 0,
        "tags": ["MotorSpeed", "PumpStatus", "Temperature"]
    }
    
    print("🧪 Testing read-tags endpoint...")
    print(f"Request: {json.dumps(test_request, indent=2)}")
    print()
    
    try:
        # Make the request
        response = requests.post(
            f"{base_url}/api/read-tags",
            json=test_request,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print()
        
        if response.status_code == 200:
            print("✅ Success! Response:")
            print(json.dumps(response.json(), indent=2))
        else:
            print("❌ Error Response:")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the FastAPI server is running on localhost:8000")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def test_endpoint_documentation():
    """Test that the endpoint appears in the API documentation"""
    print("\n📖 Checking API documentation...")
    print("Open http://localhost:8000/docs to see the new /read-tags endpoint")
    print("The endpoint should appear under the PLC tag group")

if __name__ == "__main__":
    print("🚀 SignalTap Read Tags Test")
    print("=" * 40)
    
    test_read_tags_endpoint()
    test_endpoint_documentation()
    
    print("\n📋 Test Summary:")
    print("1. The /api/read-tags endpoint should accept POST requests")
    print("2. It should return a list of TagReadResult objects")
    print("3. Each result should have name, value, status, and timestamp")
    print("4. Error handling should work for connection failures") 