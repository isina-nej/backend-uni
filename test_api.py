#!/usr/bin/env python3
# ==============================================================================
# API TEST SCRIPT FOR UNIVERSITY MANAGEMENT SYSTEM
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

import requests
import json
from datetime import datetime

# Server configuration
BASE_URL = 'http://127.0.0.1:8000'
API_URL = f'{BASE_URL}/api'

def test_api():
    """Test basic API endpoints"""
    print("🚀 Testing University Management System API")
    print("=" * 60)
    
    # Test 1: Check if server is running
    try:
        response = requests.get(BASE_URL)
        print(f"✅ Server is running: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Server is not accessible: {e}")
        return
    
    # Test 2: Test Django Admin
    try:
        response = requests.get(f'{BASE_URL}/admin/')
        print(f"✅ Django Admin accessible: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Django Admin not accessible: {e}")
    
    # Test 3: Test API endpoints
    api_endpoints = [
        '/users/ministries/',
        '/users/universities/',
        '/users/faculties/',
        '/users/departments/',
        '/users/employees/',
        '/users/students/',
        '/users/positions/',
    ]
    
    for endpoint in api_endpoints:
        try:
            response = requests.get(f'{API_URL}{endpoint}')
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {endpoint}: {response.status_code} - {data.get('count', 0)} items")
            else:
                print(f"⚠️  {endpoint}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ {endpoint}: Error - {e}")
    
    print("\n" + "=" * 60)
    print("🎯 API Test completed!")
    print(f"📅 Test time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    test_api()
