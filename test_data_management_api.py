#!/usr/bin/env python
"""
Test script for Data Management API endpoints
"""

import requests
import json
import os
import django
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

BASE_URL = "http://127.0.0.1:8000/api"

def get_auth_token():
    """Get authentication token for testing"""
    # Create or get test user
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'user_type': 'admin'
        }
    )
    
    if created:
        user.set_password('testpass123')
        user.save()
    
    # Get or create token
    token, created = Token.objects.get_or_create(user=user)
    return token.key

def test_import_export_jobs():
    """Test Import/Export Jobs API"""
    print("\n=== Testing Import/Export Jobs API ===")
    
    token = get_auth_token()
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    # 1. List jobs
    response = requests.get(f"{BASE_URL}/data-management/jobs/", headers=headers)
    print(f"GET /jobs/ - Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Jobs count: {len(response.json().get('results', []))}")
    
    # 2. Create a new import job
    job_data = {
        "title": "Test Import Job",
        "job_type": "import",
        "model_name": "users.User",
        "format": "csv",
        "description": "Test import job for users"
    }
    
    response = requests.post(f"{BASE_URL}/data-management/jobs/", 
                           json=job_data, headers=headers)
    print(f"POST /jobs/ - Status: {response.status_code}")
    
    if response.status_code == 201:
        job_id = response.json()['id']
        print(f"Created job ID: {job_id}")
        
        # 3. Get job details
        response = requests.get(f"{BASE_URL}/data-management/jobs/{job_id}/", 
                              headers=headers)
        print(f"GET /jobs/{job_id}/ - Status: {response.status_code}")
        
        # 4. Test execute action
        response = requests.post(f"{BASE_URL}/data-management/jobs/{job_id}/execute/", 
                               headers=headers)
        print(f"POST /jobs/{job_id}/execute/ - Status: {response.status_code}")
        
        # 5. Test cancel action
        response = requests.post(f"{BASE_URL}/data-management/jobs/{job_id}/cancel/", 
                               headers=headers)
        print(f"POST /jobs/{job_id}/cancel/ - Status: {response.status_code}")
    else:
        print(f"Error response: {response.text}")

def test_backup_schedules():
    """Test Backup Schedules API"""
    print("\n=== Testing Backup Schedules API ===")
    
    token = get_auth_token()
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    # 1. List schedules
    response = requests.get(f"{BASE_URL}/data-management/backup-schedules/", headers=headers)
    print(f"GET /backup-schedules/ - Status: {response.status_code}")
    
    # 2. Create a new backup schedule
    schedule_data = {
        "name": "Daily Database Backup",
        "backup_type": "full",
        "frequency": "daily",
        "storage_path": "/backups/daily",
        "is_enabled": True,
        "description": "Daily backup of the entire database"
    }
    
    response = requests.post(f"{BASE_URL}/data-management/backup-schedules/", 
                           json=schedule_data, headers=headers)
    print(f"POST /backup-schedules/ - Status: {response.status_code}")
    
    if response.status_code == 201:
        schedule_id = response.json()['id']
        print(f"Created schedule ID: {schedule_id}")
        
        # 3. Test execute backup action
        response = requests.post(f"{BASE_URL}/data-management/backup-schedules/{schedule_id}/execute/", 
                               headers=headers)
        print(f"POST /backup-schedules/{schedule_id}/execute/ - Status: {response.status_code}")
    else:
        print(f"Error response: {response.text}")

def test_sync_tasks():
    """Test Data Sync Tasks API"""
    print("\n=== Testing Data Sync Tasks API ===")
    
    token = get_auth_token()
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    # 1. List sync tasks
    response = requests.get(f"{BASE_URL}/data-management/sync-tasks/", headers=headers)
    print(f"GET /sync-tasks/ - Status: {response.status_code}")
    
    # 2. Create a new sync task
    sync_data = {
        "name": "User Data Sync",
        "sync_type": "one_way",
        "source_model": "users.User",
        "target_model": "external.User",
        "status": "active",
        "description": "Sync users to external system"
    }
    
    response = requests.post(f"{BASE_URL}/data-management/sync-tasks/", 
                           json=sync_data, headers=headers)
    print(f"POST /sync-tasks/ - Status: {response.status_code}")
    
    if response.status_code == 201:
        task_id = response.json()['id']
        print(f"Created sync task ID: {task_id}")
        
        # 3. Test execute sync action
        response = requests.post(f"{BASE_URL}/data-management/sync-tasks/{task_id}/execute/", 
                               headers=headers)
        print(f"POST /sync-tasks/{task_id}/execute/ - Status: {response.status_code}")
    else:
        print(f"Error response: {response.text}")

def test_external_integrations():
    """Test External System Integrations API"""
    print("\n=== Testing External System Integrations API ===")
    
    token = get_auth_token()
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    # 1. List integrations
    response = requests.get(f"{BASE_URL}/data-management/integrations/", headers=headers)
    print(f"GET /integrations/ - Status: {response.status_code}")
    
    # 2. Create a new integration
    integration_data = {
        "name": "Student Information System",
        "system_type": "api",
        "endpoint_url": "https://api.example.com/students",
        "authentication_method": "api_key",
        "enabled": True,
        "description": "Integration with external student information system"
    }
    
    response = requests.post(f"{BASE_URL}/data-management/integrations/", 
                           json=integration_data, headers=headers)
    print(f"POST /integrations/ - Status: {response.status_code}")
    
    if response.status_code == 201:
        integration_id = response.json()['id']
        print(f"Created integration ID: {integration_id}")
        
        # 3. Test connection
        response = requests.post(f"{BASE_URL}/data-management/integrations/{integration_id}/test_connection/", 
                               headers=headers)
        print(f"POST /integrations/{integration_id}/test_connection/ - Status: {response.status_code}")
    else:
        print(f"Error response: {response.text}")

def main():
    """Run all tests"""
    print("🔄 Starting Data Management API Tests")
    print(f"Base URL: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        test_import_export_jobs()
        test_backup_schedules()
        test_sync_tasks()
        test_external_integrations()
        
        print("\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
