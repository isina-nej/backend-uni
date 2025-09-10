#!/usr/bin/env python3
"""
تست ساده dashboard
"""

import requests
import json

# Get token first - JWT token
login_url = "http://127.0.0.1:8001/api/token/"
login_data = {
    "username": "admin",
    "password": "admin123"
}

print("Getting JWT token...")
login_response = requests.post(login_url, json=login_data)
print(f"Login status: {login_response.status_code}")

if login_response.status_code == 200:
    token = login_response.json().get('access')
    print(f"Token: {token[:50]}...")
    
    # Test dashboard
    dashboard_url = "http://127.0.0.1:8001/api/mobile/dashboard/"
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\nTesting dashboard...")
    dashboard_response = requests.get(dashboard_url, headers=headers)
    print(f"Dashboard status: {dashboard_response.status_code}")
    print(f"Dashboard response: {dashboard_response.text}")
else:
    print(f"Login failed: {login_response.text}")
