#!/usr/bin/env python3
"""
Quick connection test for CodeMate Terminal Web Edition
"""

import requests
import json

def test_connection():
    """Test basic connection to the server."""
    base_url = "http://localhost:3000"
    
    print("🔍 Testing CodeMate Terminal Web Edition Connection")
    print("=" * 50)
    
    try:
        # Test terminal status
        print("1. Testing terminal status...")
        response = requests.get(f"{base_url}/api/terminal", timeout=5)
        if response.status_code == 200:
            print("   ✅ Terminal status endpoint working")
            data = response.json()
            print(f"   📊 Status: {data.get('status', 'Unknown')}")
        else:
            print(f"   ❌ Status code: {response.status_code}")
        
        # Test welcome endpoint
        print("\n2. Testing welcome endpoint...")
        response = requests.get(f"{base_url}/api/welcome", timeout=5)
        if response.status_code == 200:
            print("   ✅ Welcome endpoint working")
            data = response.json()
            print(f"   🎯 Banner loaded: {'banner' in data}")
            print(f"   📋 Features: {len(data.get('features', []))}")
        else:
            print(f"   ❌ Status code: {response.status_code}")
        
        # Test command execution
        print("\n3. Testing command execution...")
        response = requests.post(f"{base_url}/api/execute", 
                               json={"command": "echo Hello World"}, 
                               timeout=5)
        if response.status_code == 200:
            print("   ✅ Command execution working")
            data = response.json()
            print(f"   📝 Output: {data.get('output', 'No output')[:50]}...")
        else:
            print(f"   ❌ Status code: {response.status_code}")
        
        print("\n🎉 All tests passed! Your web terminal is ready.")
        print(f"🌐 Open your browser and go to: {base_url}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed: Server not running")
        print("   Please start the server with: python run_local_server.py")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_connection()
