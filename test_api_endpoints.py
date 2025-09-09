#!/usr/bin/env python3
"""
Comprehensive API Endpoint Tester for University Management System
Tests all endpoints on PythonAnywhere deployment

Usage: python test_api_endpoints.py
"""

import requests
import json
import sys
from datetime import datetime

class APITester:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.token = None
        self.test_results = []
        
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
        print(f"{status} {method} {endpoint} - {status_code} - {message}")
        
    def test_endpoint(self, endpoint, method='GET', data=None, auth_required=False, expected_status=200):
        """Test a single endpoint"""
        url = f"{self.base_url}{endpoint}"
        headers = {}
        
        if auth_required and self.token:
            headers['Authorization'] = f'Token {self.token}'
            
        try:
            if method == 'GET':
                response = self.session.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                headers['Content-Type'] = 'application/json'
                response = self.session.post(url, json=data, headers=headers, timeout=10)
            elif method == 'PUT':
                headers['Content-Type'] = 'application/json'
                response = self.session.put(url, json=data, headers=headers, timeout=10)
            elif method == 'DELETE':
                response = self.session.delete(url, headers=headers, timeout=10)
            else:
                raise ValueError(f"Unsupported method: {method}")
                
            success = response.status_code == expected_status
            message = f"Response: {response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text[:100]}"
            
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
        
        # Test login endpoint
        login_data = {
            'username': 'sina',
            'password': 'sina4501'  # You might need to change this
        }
        
        response = self.test_endpoint('/api/auth/login/', 'POST', login_data, expected_status=200)
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                self.token = data.get('token')
                if self.token:
                    print(f"✅ Authentication successful! Token: {self.token[:20]}...")
                    return True
            except:
                pass
                
        print("⚠️ Authentication failed, continuing with public endpoints only...")
        return False
        
    def test_public_endpoints(self):
        """Test public endpoints that don't require authentication"""
        print("\n🌐 Testing Public Endpoints...")
        
        public_endpoints = [
            ('/api/health/', 'GET'),
            ('/api/info/', 'GET'),
            ('/admin/', 'GET'),  # Should redirect or show login
        ]
        
        for endpoint, method in public_endpoints:
            self.test_endpoint(endpoint, method)
            
    def test_auth_endpoints(self):
        """Test authentication related endpoints"""
        print("\n🔐 Testing Authentication Endpoints...")
        
        # Test login with wrong credentials
        self.test_endpoint('/api/auth/login/', 'POST', 
                          {'username': 'wrong', 'password': 'wrong'}, 
                          expected_status=400)
        
        if self.token:
            # Test authenticated endpoints
            self.test_endpoint('/api/auth/profile/', 'GET', auth_required=True)
            self.test_endpoint('/api/auth/logout/', 'POST', auth_required=True)
            
    def test_api_endpoints(self):
        """Test all API endpoints"""
        print("\n📚 Testing Core API Endpoints...")
        
        api_endpoints = [
            # Users endpoints
            ('/api/users/', 'GET'),
            
            # Courses endpoints
            ('/api/courses/', 'GET'),
            
            # Notifications endpoints
            ('/api/notifications/', 'GET'),
            
            # Grades endpoints
            ('/api/grades/', 'GET'),
            
            # Schedules endpoints
            ('/api/schedules/', 'GET'),
            
            # Exams endpoints
            ('/api/exams/', 'GET'),
            
            # Library endpoints
            ('/api/library/', 'GET'),
            
            # Financial endpoints
            ('/api/financial/', 'GET'),
            
            # Attendance endpoints
            ('/api/attendance/', 'GET'),
            
            # Research endpoints
            ('/api/research/', 'GET'),
            
            # Announcements endpoints
            ('/api/announcements/', 'GET'),
            
            # Assignments endpoints
            ('/api/assignments/', 'GET'),
            
            # Reports endpoints
            ('/api/reports/', 'GET'),
        ]
        
        for endpoint, method in api_endpoints:
            # Test without auth first
            self.test_endpoint(endpoint, method, expected_status=401)
            
            # Test with auth if available
            if self.token:
                self.test_endpoint(endpoint, method, auth_required=True)
                
    def test_reports_endpoints(self):
        """Test specific report endpoints"""
        print("\n📊 Testing Reports Endpoints...")
        
        if self.token:
            reports_endpoints = [
                ('/api/reports/dashboard-stats/', 'GET'),
                ('/api/reports/student-report/', 'GET'),
            ]
            
            for endpoint, method in reports_endpoints:
                self.test_endpoint(endpoint, method, auth_required=True)
                
    def test_create_operations(self):
        """Test creating new records"""
        print("\n📝 Testing Create Operations...")
        
        if not self.token:
            print("⚠️ Skipping create operations - no authentication token")
            return
            
        # Test creating a course (example)
        course_data = {
            'title': 'Test Course',
            'code': 'TEST101',
            'description': 'This is a test course created by API tester'
        }
        
        response = self.test_endpoint('/api/courses/', 'POST', course_data, 
                                    auth_required=True, expected_status=201)
        
        # If course created successfully, try to delete it
        if response and response.status_code == 201:
            try:
                course_id = response.json().get('id')
                if course_id:
                    self.test_endpoint(f'/api/courses/{course_id}/', 'DELETE', 
                                     auth_required=True, expected_status=204)
            except:
                pass
                
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
                    print(f"  - {result['method']} {result['endpoint']} - {result['message'][:100]}")
                    
        # Save detailed report to file
        with open('api_test_report.json', 'w') as f:
            json.dump(self.test_results, f, indent=2)
            
        print(f"\n📄 Detailed report saved to: api_test_report.json")
        
    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting API Endpoint Testing...")
        print(f"🎯 Target URL: {self.base_url}")
        print(f"⏰ Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Test in order
        self.test_public_endpoints()
        self.authenticate()
        self.test_auth_endpoints()
        self.test_api_endpoints()
        self.test_reports_endpoints()
        self.test_create_operations()
        
        # Generate report
        self.generate_report()

def main():
    """Main function"""
    # Your PythonAnywhere URL
    base_url = "https://sinanej2.pythonanywhere.com"
    
    print("🎓 University Management System API Tester")
    print("=" * 50)
    
    # Create tester instance
    tester = APITester(base_url)
    
    # Run all tests
    tester.run_all_tests()
    
    print("\n🏁 Testing completed!")

if __name__ == "__main__":
    main()
