#!/usr/bin/env python3
"""
Test script for CodeMate Terminal API
Tests the API endpoints locally before deployment
"""

import requests
import json
import time

def test_api_endpoints():
    """Test all API endpoints."""
    base_url = "http://localhost:3000"
    
    print("🧪 Testing CodeMate Terminal API")
    print("=" * 50)
    
    # Test 1: Terminal status
    print("\n1. Testing terminal status...")
    try:
        response = requests.get(f"{base_url}/api/terminal")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {data['status']}")
            print(f"   📁 Current path: {data['current_path']}")
        else:
            print(f"   ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
    
    # Test 2: Help endpoint
    print("\n2. Testing help endpoint...")
    try:
        response = requests.get(f"{base_url}/api/help")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Help loaded: {len(data['help'])} characters")
        else:
            print(f"   ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
    
    # Test 3: Basic command execution
    print("\n3. Testing basic command execution...")
    try:
        response = requests.post(f"{base_url}/api/execute", 
            json={"command": "ls", "natural_language": False})
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Command executed: {data['command']}")
            print(f"   📊 Exit code: {data['exit_code']}")
            if data['output']:
                print(f"   📄 Output preview: {data['output'][:100]}...")
        else:
            print(f"   ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
    
    # Test 4: AI natural language translation
    print("\n4. Testing AI natural language...")
    try:
        response = requests.post(f"{base_url}/api/execute", 
            json={"command": "create a folder called test", "natural_language": True})
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ AI command: {data['command']}")
            if data['ai_translation']:
                print(f"   🤖 Translation: {data['ai_translation']}")
            print(f"   📊 Exit code: {data['exit_code']}")
        else:
            print(f"   ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
    
    # Test 5: Complex AI command
    print("\n5. Testing complex AI command...")
    try:
        response = requests.post(f"{base_url}/api/execute", 
            json={"command": "create a new folder called test and move file1.txt into it", "natural_language": True})
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Complex AI command: {data['command']}")
            if data['ai_translation']:
                print(f"   🤖 Translation: {data['ai_translation']}")
            print(f"   📊 Exit code: {data['exit_code']}")
        else:
            print(f"   ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
    
    # Test 6: Translation endpoint
    print("\n6. Testing translation endpoint...")
    try:
        response = requests.post(f"{base_url}/api/translate", 
            json={"text": "show me my files"})
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Original: {data['original']}")
            print(f"   🤖 Translated: {data['translated']}")
        else:
            print(f"   ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 API testing completed!")

def test_frontend():
    """Test frontend accessibility."""
    print("\n🌐 Testing frontend...")
    try:
        response = requests.get("http://localhost:3000/")
        if response.status_code == 200:
            print("   ✅ Frontend accessible")
            if "CodeMate Terminal" in response.text:
                print("   ✅ Title found in HTML")
            else:
                print("   ⚠️  Title not found")
        else:
            print(f"   ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Connection error: {e}")

if __name__ == "__main__":
    print("🚀 CodeMate Terminal API Test Suite")
    print("Make sure to run 'vercel dev' in another terminal first!")
    print("=" * 60)
    
    # Wait a moment for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(2)
    
    test_api_endpoints()
    test_frontend()
    
    print("\n📋 Next steps:")
    print("1. If all tests pass, you're ready to deploy!")
    print("2. Run 'vercel --prod' to deploy to production")
    print("3. Visit your Vercel URL to use the terminal")
    print("\n🎯 Happy coding with CodeMate Terminal!")
