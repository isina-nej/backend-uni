#!/usr/bin/env python3
"""
تست سریع سرور production
"""

import requests
import json

def test_production_server():
    base_url = "https://sinanej2.pythonanywhere.com"
    
    # تست endpoints ساده
    endpoints = [
        "/api/",
        "/api/health/",
        "/api/info/",
        "/api/users/",
        "/api/courses/",
        "/api/dormitory/",
    ]
    
    print("🧪 Testing production server...")
    print("=" * 50)
    
    for endpoint in endpoints:
        try:
            url = f"{base_url}{endpoint}"
            response = requests.get(url, timeout=10)
            
            status_emoji = "✅" if response.status_code < 500 else "❌"
            print(f"{status_emoji} {endpoint}: {response.status_code}")
            
            if response.status_code >= 500:
                print(f"   Error: {response.text[:200]}")
                
        except Exception as e:
            print(f"❌ {endpoint}: ERROR - {e}")
    
    print("=" * 50)

if __name__ == '__main__':
    test_production_server()
