#!/usr/bin/env python3
"""
Fixed API Endpoint Tester for University Management System
This version handles authentication properly and tests the correct endpoints

Usage: python test_api_fixed.py
"""

import requests
import json
import sys
from datetime import datetime

class FixedAPITester:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.token = None
        self.test_results = []
        # Disable SSL warnings for testing
        requests.packages.urllib3.disable_warnings()
        
    def log_result(self, endpoint, method, status_code, success, message=""):
        """Log test result"""
        result = {
            'endpoint': endpoint,
            'method': method,
            'status_code': status_code,
            'success': success,
            'message': message,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.test_results.append(result)
        
        # Print result
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {method} {endpoint} - {status_code}")
        if not success or "FAIL" in message:
            print(f"   └─ {message[:100]}")
        
    def test_endpoint(self, endpoint, method='GET', data=None, auth_required=False, expected_status=200):
        """Test a single endpoint"""
        url = f"{self.base_url}{endpoint}"
        headers = {
            'User-Agent': 'API-Tester/1.0',
            'Accept': 'application/json',
        }
        
        if auth_required and self.token:
            headers['Authorization'] = f'Token {self.token}'
            
        try:
            if method == 'GET':
                response = self.session.get(url, headers=headers, timeout=30, verify=False)
            elif method == 'POST':
                headers['Content-Type'] = 'application/json'
                response = self.session.post(url, json=data, headers=headers, timeout=30, verify=False)
            elif method == 'PUT':
                headers['Content-Type'] = 'application/json'
                response = self.session.put(url, json=data, headers=headers, timeout=30, verify=False)
            elif method == 'DELETE':
                response = self.session.delete(url, headers=headers, timeout=30, verify=False)
            else:
                raise ValueError(f"Unsupported method: {method}")
                
            success = response.status_code == expected_status
            
            try:
                response_data = response.json()
                message = f"OK" if success else f"Error: {response_data}"
            except:
                message = f"OK" if success else f"Status: {response.status_code}, Content: {response.text[:100]}"
            
        except requests.exceptions.RequestException as e:
            success = False
            message = f"Request failed: {str(e)}"
            response = None
            
        except Exception as e:
            success = False
            message = f"Error: {str(e)}"
            response = None
            
        status_code = response.status_code if response else 0
        self.log_result(endpoint, method, status_code, success, message)
        return response
        
    def authenticate(self):
        """Try to authenticate and get token"""
        print("\n🔐 Testing Authentication...")
        
        # Get CSRF token first
        csrf_url = f"{self.base_url}/api/auth/login/"
        try:
            csrf_response = self.session.get(csrf_url, verify=False)
            csrf_token = csrf_response.cookies.get('csrftoken')
            
            headers = {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token,
                'Referer': self.base_url,
            }
            
            if csrf_token:
                headers['X-CSRFToken'] = csrf_token
                
        except:
            headers = {'Content-Type': 'application/json'}
        
        # Test login endpoint
        login_data = {
            'username': 'sina',
            'password': 'sina4501'
        }
        
        try:
            response = self.session.post(csrf_url, json=login_data, headers=headers, verify=False)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    self.token = data.get('token')
                    if self.token:
                        print(f"✅ Authentication successful! Token: {self.token[:20]}...")
                        self.log_result('/api/auth/login/', 'POST', 200, True, "Login successful")
                        return True
                except:
                    pass
                    
            self.log_result('/api/auth/login/', 'POST', response.status_code, False, 
                          f"Login failed: {response.text[:100]}")
                          
        except Exception as e:
            self.log_result('/api/auth/login/', 'POST', 0, False, f"Login error: {str(e)}")
            
        print("⚠️ Authentication failed, testing public endpoints only...")
        return False
        
    def test_public_endpoints(self):
        """Test public endpoints that don't require authentication"""
        print("\n🌐 Testing Public Endpoints...")
        
        public_endpoints = [
            ('/api/health/', 'GET'),
            ('/api/info/', 'GET'),
            ('/admin/', 'GET'),
        ]
        
        for endpoint, method in public_endpoints:
            if endpoint == '/admin/':
                # Admin should return 200 (login page) or redirect
                self.test_endpoint(endpoint, method, expected_status=200)
            else:
                self.test_endpoint(endpoint, method)
                
    def test_authenticated_endpoints(self):
        """Test endpoints that require authentication"""
        if not self.token:
            print("\n⚠️ Skipping authenticated endpoints - no token")
            return
            
        print("\n🔒 Testing Authenticated Endpoints...")
        
        # Test auth profile
        self.test_endpoint('/api/auth/profile/', 'GET', auth_required=True)
        
        # Test main API endpoints
        api_endpoints = [
            '/api/users/',
            '/api/courses/',
            '/api/notifications/',
            '/api/grades/',
            '/api/schedules/',
            '/api/exams/',
            '/api/library/',
            '/api/financial/',
            '/api/attendance/',
            '/api/research/',
            '/api/announcements/',
            '/api/assignments/',
        ]
        
        for endpoint in api_endpoints:
            self.test_endpoint(endpoint, 'GET', auth_required=True)
            
    def test_reports_endpoints(self):
        """Test reports endpoints"""
        if not self.token:
            print("\n⚠️ Skipping reports endpoints - no token")
            return
            
        print("\n📊 Testing Reports Endpoints...")
        
        # Note: These might fail due to permissions (user is student, not admin/staff)
        self.test_endpoint('/api/reports/dashboard/', 'GET', auth_required=True, expected_status=403)
        self.test_endpoint('/api/reports/student/', 'GET', auth_required=True)
        
    def test_user_management(self):
        """Test user-specific endpoints"""
        if not self.token:
            return
            
        print("\n👤 Testing User Management...")
        
        # Test getting current user info
        self.test_endpoint('/api/users/me/', 'GET', auth_required=True)
        
    def generate_report(self):
        """Generate a summary report"""
        print("\n" + "="*60)
        print("📋 API TEST RESULTS SUMMARY")
        print("="*60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['method']} {result['endpoint']} - Status: {result['status_code']}")
                    
        print("\n✅ PASSED TESTS:")
        for result in self.test_results:
            if result['success']:
                print(f"  - {result['method']} {result['endpoint']} - Status: {result['status_code']}")
                    
        # Save detailed report to file
        with open('api_test_report_fixed.json', 'w') as f:
            json.dump(self.test_results, f, indent=2)
            
        print(f"\n📄 Detailed report saved to: api_test_report_fixed.json")
        
    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting Fixed API Endpoint Testing...")
        print(f"🎯 Target URL: {self.base_url}")
        print(f"⏰ Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Test in order
        self.test_public_endpoints()
        self.authenticate()
        self.test_authenticated_endpoints()
        self.test_reports_endpoints()
        self.test_user_management()
        
        # Generate report
        self.generate_report()

def main():
    """Main function"""
    # Your PythonAnywhere URL
    base_url = "https://sinanej2.pythonanywhere.com"
    
    print("🎓 University Management System API Tester (Fixed)")
    print("=" * 55)
    
    # Create tester instance
    tester = FixedAPITester(base_url)
    
    # Run all tests
    tester.run_all_tests()
    
    print("\n🏁 Testing completed!")

if __name__ == "__main__":
    main()
