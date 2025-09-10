#!/usr/bin/env python
"""
Test script for Mobile API endpoints
"""

import requests
import json
import os
import django
from datetime import datetime
import uuid

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

BASE_URL = "http://127.0.0.1:8001/api"

def get_auth_token():
    """Get authentication token for testing"""
    # Create or get test user
    user, created = User.objects.get_or_create(
        username='mobile_testuser',
        defaults={
            'email': 'mobile@example.com',
            'first_name': 'Mobile',
            'last_name': 'User',
            'user_type': 'student'
        }
    )
    
    if created:
        user.set_password('testpass123')
        user.save()
    
    # Get or create token
    token, created = Token.objects.get_or_create(user=user)
    return token.key

def test_mobile_device_api():
    """Test Mobile Device API"""
    print("\n=== Testing Mobile Device API ===")
    
    token = get_auth_token()
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    # 1. Register a device
    device_data = {
        "device_id": f"test_device_{uuid.uuid4().hex[:8]}",
        "device_name": "Test iPhone",
        "device_type": "ios",
        "device_model": "iPhone 14",
        "os_version": "16.0",
        "app_version": "1.0.0",
        "timezone": "Asia/Tehran",
        "push_token": "test_push_token_123",
        "push_provider": "apn"
    }
    
    response = requests.post(f"{BASE_URL}/mobile/devices/register/", 
                           json=device_data, headers=headers)
    print(f"POST /mobile/devices/register/ - Status: {response.status_code}")
    
    if response.status_code == 201:
        device = response.json()
        device_id = device['id']
        print(f"Registered device ID: {device_id}")
        
        # 2. List user devices
        response = requests.get(f"{BASE_URL}/mobile/devices/", headers=headers)
        print(f"GET /mobile/devices/ - Status: {response.status_code}")
        if response.status_code == 200:
            devices = response.json()['results']
            print(f"User has {len(devices)} devices")
        
        # 3. Update push token
        response = requests.post(f"{BASE_URL}/mobile/devices/{device_id}/update_push_token/", 
                               json={
                                   "push_token": "updated_token_456",
                                   "push_provider": "apn"
                               }, headers=headers)
        print(f"POST /mobile/devices/{device_id}/update_push_token/ - Status: {response.status_code}")
        
        return device['device_id']
    else:
        print(f"Error response: {response.text}")
        return None

def test_mobile_session_api(device_id):
    """Test Mobile Session API"""
    print("\n=== Testing Mobile Session API ===")
    
    token = get_auth_token()
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    if not device_id:
        print("No device ID available for session testing")
        return None
    
    # 1. Start a session
    session_data = {
        "device_id": device_id,
        "network_type": "wifi"
    }
    
    response = requests.post(f"{BASE_URL}/mobile/sessions/start/", 
                           json=session_data, headers=headers)
    print(f"POST /mobile/sessions/start/ - Status: {response.status_code}")
    
    if response.status_code == 201:
        session = response.json()
        session_id = session['id']
        print(f"Started session ID: {session_id}")
        
        # 2. Update session activity
        activity_data = {
            "screens_visited": ["dashboard", "courses", "grades"],
            "actions_performed": [
                {"action": "view_course", "timestamp": datetime.now().isoformat()},
                {"action": "check_grade", "timestamp": datetime.now().isoformat()}
            ],
            "api_calls_made": 5,
            "data_usage_bytes": 1024
        }
        
        response = requests.post(f"{BASE_URL}/mobile/sessions/{session_id}/update_activity/", 
                               json=activity_data, headers=headers)
        print(f"POST /mobile/sessions/{session_id}/update_activity/ - Status: {response.status_code}")
        
        # 3. List user sessions
        response = requests.get(f"{BASE_URL}/mobile/sessions/", headers=headers)
        print(f"GET /mobile/sessions/ - Status: {response.status_code}")
        
        # 4. End session
        response = requests.post(f"{BASE_URL}/mobile/sessions/{session_id}/end/", headers=headers)
        print(f"POST /mobile/sessions/{session_id}/end/ - Status: {response.status_code}")
        
        return session_id
    else:
        print(f"Error response: {response.text}")
        return None

def test_push_notification_api():
    """Test Push Notification API"""
    print("\n=== Testing Push Notification API ===")
    
    token = get_auth_token()
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    # 1. Send a notification
    notification_data = {
        "title": "Test Mobile Notification",
        "message": "This is a test notification for mobile app",
        "notification_type": "general",
        "user_types": ["student"],
        "action_data": {
            "screen": "dashboard",
            "params": {"tab": "grades"}
        }
    }
    
    response = requests.post(f"{BASE_URL}/mobile/notifications/send/", 
                           json=notification_data, headers=headers)
    print(f"POST /mobile/notifications/send/ - Status: {response.status_code}")
    
    if response.status_code == 201:
        notification = response.json()
        print(f"Sent notification ID: {notification['id']}")
    
    # 2. Get user notifications
    response = requests.get(f"{BASE_URL}/mobile/notifications/my_notifications/", headers=headers)
    print(f"GET /mobile/notifications/my_notifications/ - Status: {response.status_code}")
    
    # 3. List all notifications
    response = requests.get(f"{BASE_URL}/mobile/notifications/", headers=headers)
    print(f"GET /mobile/notifications/ - Status: {response.status_code}")

def test_offline_sync_api(device_id):
    """Test Offline Sync API"""
    print("\n=== Testing Offline Sync API ===")
    
    token = get_auth_token()
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    if not device_id:
        print("No device ID available for sync testing")
        return
    
    # 1. Initiate sync
    sync_data = {
        "device_id": device_id,
        "sync_type": "incremental",
        "data_types": ["courses", "grades", "announcements"]
    }
    
    response = requests.post(f"{BASE_URL}/mobile/sync/initiate/", 
                           json=sync_data, headers=headers)
    print(f"POST /mobile/sync/initiate/ - Status: {response.status_code}")
    
    if response.status_code == 201:
        sync_record = response.json()
        print(f"Initiated sync ID: {sync_record['id']}")
    
    # 2. Get sync data
    response = requests.get(f"{BASE_URL}/mobile/sync/get_data/?device_id={device_id}", headers=headers)
    print(f"GET /mobile/sync/get_data/ - Status: {response.status_code}")
    
    if response.status_code == 200:
        sync_data = response.json()
        print(f"Sync data contains: {list(sync_data.keys())}")
    
    # 3. List sync records
    response = requests.get(f"{BASE_URL}/mobile/sync/", headers=headers)
    print(f"GET /mobile/sync/ - Status: {response.status_code}")

def test_mobile_settings_api():
    """Test Mobile Settings API"""
    print("\n=== Testing Mobile Settings API ===")
    
    token = get_auth_token()
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    # 1. Get current settings
    response = requests.get(f"{BASE_URL}/mobile/settings/", headers=headers)
    print(f"GET /mobile/settings/ - Status: {response.status_code}")
    
    # 2. Update settings
    settings_data = {
        "theme": "dark",
        "language": "fa",
        "font_size": "large",
        "push_notifications": True,
        "auto_sync": True,
        "data_saver_mode": False,
        "custom_settings": {
            "dashboard_layout": "grid",
            "animations": True
        }
    }
    
    response = requests.post(f"{BASE_URL}/mobile/settings/", 
                           json=settings_data, headers=headers)
    print(f"POST /mobile/settings/ - Status: {response.status_code}")

def test_mobile_dashboard_api():
    """Test Mobile Dashboard API"""
    print("\n=== Testing Mobile Dashboard API ===")
    
    token = get_auth_token()
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    # Get dashboard data
    response = requests.get(f"{BASE_URL}/mobile/dashboard/", headers=headers)
    print(f"GET /mobile/dashboard/ - Status: {response.status_code}")
    
    if response.status_code == 200:
        dashboard = response.json()
        print(f"Dashboard data includes: {list(dashboard.keys())}")
        if 'user_info' in dashboard:
            user_info = dashboard['user_info']
            name = f"{user_info.get('first_name', '')} {user_info.get('last_name', '')}".strip()
            print(f"User: {name or user_info.get('email', 'Unknown')}")
        if 'stats' in dashboard:
            print(f"Stats: {dashboard['stats']}")

def main():
    """Run all tests"""
    print("🔄 Starting Mobile API Tests")
    print(f"Base URL: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Test device registration
        device_id = test_mobile_device_api()
        
        # Test sessions (requires device)
        session_id = test_mobile_session_api(device_id)
        
        # Test notifications
        test_push_notification_api()
        
        # Test sync (requires device)
        test_offline_sync_api(device_id)
        
        # Test settings
        test_mobile_settings_api()
        
        # Test dashboard
        test_mobile_dashboard_api()
        
        print("\n✅ All Mobile API tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
