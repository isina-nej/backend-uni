# ==============================================================================
# API ENDPOINT TESTING AND VALIDATION
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

import requests
import json
import time
from datetime import datetime


class APITester:
    """Comprehensive API testing utility"""
    
    def __init__(self, base_url='http://127.0.0.1:8000'):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
    
    def test_endpoint(self, endpoint, method='GET', data=None, headers=None, expected_status=200):
        """Test a single API endpoint"""
        url = f"{self.base_url}{endpoint}"
        
        start_time = time.time()
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, headers=headers)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, headers=headers)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data, headers=headers)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response_time = round((time.time() - start_time) * 1000, 2)
            
            test_result = {
                'endpoint': endpoint,
                'method': method,
                'url': url,
                'status_code': response.status_code,
                'expected_status': expected_status,
                'response_time_ms': response_time,
                'success': response.status_code == expected_status,
                'timestamp': datetime.now().isoformat(),
                'response_headers': dict(response.headers),
            }
            
            try:
                test_result['response_data'] = response.json()
            except:
                test_result['response_data'] = response.text
            
            self.test_results.append(test_result)
            return test_result
            
        except Exception as e:
            test_result = {
                'endpoint': endpoint,
                'method': method,
                'url': url,
                'error': str(e),
                'success': False,
                'timestamp': datetime.now().isoformat(),
            }
            self.test_results.append(test_result)
            return test_result
    
    def test_health_endpoints(self):
        """Test all health and monitoring endpoints"""
        print("🏥 Testing Health and Monitoring Endpoints...")
        
        endpoints = [
            ('/api/health/', 'GET', 200),
            ('/api/status/', 'GET', 200),
            ('/api/info/', 'GET', 200),
            ('/api/version/', 'GET', 200),
        ]
        
        for endpoint, method, expected_status in endpoints:
            result = self.test_endpoint(endpoint, method, expected_status=expected_status)
            status_icon = "✅" if result['success'] else "❌"
            print(f"  {status_icon} {endpoint} - {result.get('status_code', 'ERROR')} ({result.get('response_time_ms', 0)}ms)")
    
    def test_documentation_endpoints(self):
        """Test API documentation endpoints"""
        print("\n📚 Testing Documentation Endpoints...")
        
        endpoints = [
            ('/api/docs/', 'GET', 200),
            ('/api/redoc/', 'GET', 200),
            ('/api/schema/', 'GET', 200),
        ]
        
        for endpoint, method, expected_status in endpoints:
            result = self.test_endpoint(endpoint, method, expected_status=expected_status)
            status_icon = "✅" if result['success'] else "❌"
            print(f"  {status_icon} {endpoint} - {result.get('status_code', 'ERROR')} ({result.get('response_time_ms', 0)}ms)")
    
    def test_api_endpoints(self):
        """Test main API endpoints"""
        print("\n🔧 Testing Main API Endpoints...")
        
        endpoints = [
            ('/api/', 'GET', 200),
            ('/api/users/', 'GET', 200),
            ('/api/courses/', 'GET', 200),
            ('/api/announcements/', 'GET', 200),
            ('/api/assignments/', 'GET', 200),
        ]
        
        for endpoint, method, expected_status in endpoints:
            result = self.test_endpoint(endpoint, method, expected_status=expected_status)
            status_icon = "✅" if result['success'] else "❌"
            print(f"  {status_icon} {endpoint} - {result.get('status_code', 'ERROR')} ({result.get('response_time_ms', 0)}ms)")
    
    def test_error_handling(self):
        """Test error handling"""
        print("\n🚨 Testing Error Handling...")
        
        # Test 404 errors
        result = self.test_endpoint('/api/nonexistent/', 'GET', expected_status=404)
        status_icon = "✅" if result['success'] else "❌"
        print(f"  {status_icon} 404 Error Handling - {result.get('status_code', 'ERROR')}")
        
        # Test method not allowed
        result = self.test_endpoint('/api/health/', 'POST', expected_status=405)
        status_icon = "✅" if result['success'] else "❌"
        print(f"  {status_icon} 405 Method Not Allowed - {result.get('status_code', 'ERROR')}")
    
    def test_response_formatting(self):
        """Test response formatting and structure"""
        print("\n📋 Testing Response Formatting...")
        
        result = self.test_endpoint('/api/health/', 'GET')
        
        if result['success'] and 'response_data' in result:
            response_data = result['response_data']
            
            # Check required fields
            required_fields = ['status', 'timestamp']
            missing_fields = [field for field in required_fields if field not in response_data]
            
            if not missing_fields:
                print("  ✅ Response format is correct")
            else:
                print(f"  ❌ Missing required fields: {missing_fields}")
            
            # Check response time header
            if 'X-Response-Time' in result['response_headers']:
                print("  ✅ Response time header present")
            else:
                print("  ❌ Response time header missing")
        else:
            print("  ❌ Could not test response formatting")
    
    def test_versioning(self):
        """Test API versioning"""
        print("\n🔢 Testing API Versioning...")
        
        # Test with version header
        headers = {'Accept': 'application/json; version=1.0'}
        result = self.test_endpoint('/api/version/', 'GET', headers=headers)
        
        if result['success']:
            if 'X-API-Version' in result['response_headers']:
                print("  ✅ API versioning headers present")
            else:
                print("  ❌ API versioning headers missing")
        else:
            print("  ❌ Could not test API versioning")
    
    def test_internationalization(self):
        """Test internationalization"""
        print("\n🌍 Testing Internationalization...")
        
        # Test with different language headers
        languages = ['en', 'fa', 'ar']
        
        for lang in languages:
            headers = {'Accept-Language': lang}
            result = self.test_endpoint('/api/health/', 'GET', headers=headers)
            
            status_icon = "✅" if result['success'] else "❌"
            print(f"  {status_icon} Language {lang} - {result.get('status_code', 'ERROR')}")
    
    def run_comprehensive_test(self):
        """Run all tests"""
        print("🚀 Starting Comprehensive API Testing...")
        print("=" * 60)
        
        start_time = time.time()
        
        self.test_health_endpoints()
        self.test_documentation_endpoints()
        self.test_api_endpoints()
        self.test_error_handling()
        self.test_response_formatting()
        self.test_versioning()
        self.test_internationalization()
        
        total_time = round((time.time() - start_time) * 1000, 2)
        
        # Summary
        print("\n📊 Test Summary:")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        successful_tests = len([r for r in self.test_results if r['success']])
        failed_tests = total_tests - successful_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Successful: {successful_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(successful_tests/total_tests*100):.1f}%")
        print(f"Total Time: {total_time}ms")
        
        # Average response time
        response_times = [r.get('response_time_ms', 0) for r in self.test_results if r['success']]
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            print(f"Average Response Time: {avg_response_time:.2f}ms")
        
        print("\n🎯 Performance Analysis:")
        print("=" * 60)
        
        # Performance categories
        fast_endpoints = [r for r in self.test_results if r.get('response_time_ms', 0) < 100]
        slow_endpoints = [r for r in self.test_results if r.get('response_time_ms', 0) > 500]
        
        print(f"Fast endpoints (<100ms): {len(fast_endpoints)}")
        print(f"Slow endpoints (>500ms): {len(slow_endpoints)}")
        
        if slow_endpoints:
            print("\n🐌 Slow Endpoints:")
            for endpoint in slow_endpoints:
                print(f"  - {endpoint['endpoint']}: {endpoint.get('response_time_ms', 0)}ms")
        
        return {
            'total_tests': total_tests,
            'successful_tests': successful_tests,
            'failed_tests': failed_tests,
            'success_rate': successful_tests/total_tests*100,
            'total_time_ms': total_time,
            'average_response_time_ms': avg_response_time if response_times else 0,
            'results': self.test_results
        }
    
    def save_results(self, filename='api_test_results.json'):
        """Save test results to file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Test results saved to {filename}")


if __name__ == "__main__":
    # Run the tests
    tester = APITester()
    results = tester.run_comprehensive_test()
    tester.save_results()
