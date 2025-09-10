#!/usr/bin/env python3
import os
import sys
import django
import requests
import json

# Add the backend directory to the Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_local')
django.setup()

BASE_URL = "http://127.0.0.1:8000/api"

def test_simple_endpoints():
    """Test simple endpoints without authentication"""
    print("=== Testing Simple Endpoints ===")
    
    # Test health check
    try:
        response = requests.get(f"{BASE_URL}/health/")
        print(f"Health Check: {response.status_code}")
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Health Check Error: {e}")
    
    # Test API info
    try:
        response = requests.get(f"{BASE_URL}/info/")
        print(f"API Info: {response.status_code}")
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"API Info Error: {e}")

def test_auth():
    """Test authentication"""
    print("\n=== Testing Authentication ===")
    
    auth_data = {"username": "admin", "password": "admin123"}
    
    try:
        response = requests.post(f"{BASE_URL}/auth/token/", json=auth_data)
        print(f"Token Auth: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Token: {data.get('token')}")
            return data.get('token')
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Auth Error: {e}")
    
    return None

def test_users_api(token):
    """Test users API"""
    print("\n=== Testing Users API ===")
    
    headers = {"Authorization": f"Token {token}"}
    
    # Test users list
    try:
        response = requests.get(f"{BASE_URL}/users/", headers=headers)
        print(f"Users List: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Count: {data.get('count', 0)}")
            if data.get('results'):
                print("First user:", json.dumps(data['results'][0], indent=2, ensure_ascii=False))
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Users API Error: {e}")

def test_organizational_units_api(token):
    """Test organizational units API"""
    print("\n=== Testing Organizational Units API ===")
    
    headers = {"Authorization": f"Token {token}"}
    
    # Test list
    try:
        response = requests.get(f"{BASE_URL}/users/organizational-units/", headers=headers)
        print(f"Org Units List: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Count: {data.get('count', 0)}")
            if data.get('results'):
                print("First unit:", json.dumps(data['results'][0], indent=2, ensure_ascii=False))
        else:
            print(f"Error Response: {response.status_code}")
            print(f"Error Body: {response.text[:500]}")
    except Exception as e:
        print(f"Org Units API Error: {e}")
    
    # Test tree
    try:
        response = requests.get(f"{BASE_URL}/users/organizational-units/tree/", headers=headers)
        print(f"Org Units Tree: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Tree items: {len(data)}")
            if data:
                print("First tree item:", json.dumps(data[0], indent=2, ensure_ascii=False))
        else:
            print(f"Tree Error: {response.text[:500]}")
    except Exception as e:
        print(f"Tree API Error: {e}")

if __name__ == "__main__":
    print("🔥 Simple API Test")
    test_simple_endpoints()
    
    token = test_auth()
    if token:
        test_users_api(token)
        test_organizational_units_api(token)
    else:
        print("❌ Cannot test authenticated endpoints without token")
