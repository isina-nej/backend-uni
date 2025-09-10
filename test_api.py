#!/usr/bin/env python3
"""
Test script for University Management API
تست API سیستم مدیریت دانشگاهی
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000/api"

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🔥 {title}")
    print(f"{'='*60}")

def print_json(data, max_items=5):
    """Pretty print JSON with limited items for readability"""
    if isinstance(data, list) and len(data) > max_items:
        print(f"📊 Showing {max_items} of {len(data)} items:")
        for i, item in enumerate(data[:max_items]):
            print(f"  {i+1}. {json.dumps(item, indent=2, ensure_ascii=False)}")
        print(f"  ... and {len(data) - max_items} more items")
    else:
        print(json.dumps(data, indent=2, ensure_ascii=False))

def test_auth():
    """Test authentication"""
    print_header("Testing Authentication 🔐")
    
    auth_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/token/", json=auth_data)
        if response.status_code == 200:
            data = response.json()
            print("✅ Authentication successful!")
            print_json(data)
            return data.get('token')
        else:
            print(f"❌ Authentication failed: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_organizational_units(token):
    """Test organizational units API"""
    print_header("Testing Organizational Units 🏛️")
    
    headers = {"Authorization": f"Token {token}"}
    
    try:
        # Test tree structure
        print("\n🌳 Tree Structure:")
        response = requests.get(f"{BASE_URL}/users/organizational-units/tree/", headers=headers)
        if response.status_code == 200:
            print("✅ Tree structure retrieved successfully!")
            print_json(response.json(), max_items=3)
        else:
            print(f"❌ Error: {response.status_code}")
            
        # Test units list
        print("\n📋 Units List:")
        response = requests.get(f"{BASE_URL}/users/organizational-units/", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {data.get('count', 0)} organizational units")
            print_json(data.get('results', []), max_items=3)
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_users(token):
    """Test users API"""
    print_header("Testing Users 👥")
    
    headers = {"Authorization": f"Token {token}"}
    
    try:
        # Test users list
        response = requests.get(f"{BASE_URL}/users/", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {data.get('count', 0)} users")
            print_json(data.get('results', []), max_items=3)
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
        # Test current user
        print("\n👤 Current User:")
        response = requests.get(f"{BASE_URL}/users/me/", headers=headers)
        if response.status_code == 200:
            print("✅ Current user info retrieved!")
            print_json(response.json())
        else:
            print(f"❌ Error: {response.status_code}")
            
        # Test user statistics
        print("\n📊 User Statistics:")
        response = requests.get(f"{BASE_URL}/users/statistics/", headers=headers)
        if response.status_code == 200:
            print("✅ Statistics retrieved!")
            print_json(response.json())
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_positions(token):
    """Test positions API"""
    print_header("Testing Positions 💼")
    
    headers = {"Authorization": f"Token {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/users/positions/", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {data.get('count', 0)} positions")
            print_json(data.get('results', []), max_items=3)
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_permissions(token):
    """Test permissions API"""
    print_header("Testing Permissions 🔑")
    
    headers = {"Authorization": f"Token {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/users/permissions/", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {data.get('count', 0)} permissions")
            print_json(data.get('results', []), max_items=3)
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_access_logs(token):
    """Test access logs API"""
    print_header("Testing Access Logs 📊")
    
    headers = {"Authorization": f"Token {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/users/access-logs/", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {data.get('count', 0)} access logs")
            print_json(data.get('results', []), max_items=3)
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main test function"""
    print(f"""
🎓 University Management System API Test
=========================================
🕐 Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🌐 Base URL: {BASE_URL}
    """)
    
    # Test authentication
    token = test_auth()
    if not token:
        print("❌ Cannot proceed without authentication")
        return
    
    # Test all endpoints
    test_organizational_units(token)
    test_users(token)
    test_positions(token)
    test_permissions(token)
    test_access_logs(token)
    
    print_header("Test Completed ✅")
    print("🎉 All API endpoints have been tested!")
    print("📚 Check the API documentation at: API_DOCUMENTATION.md")

if __name__ == "__main__":
    main()
