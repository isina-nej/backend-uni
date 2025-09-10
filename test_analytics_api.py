# ==============================================================================
# ANALYTICS API TEST SCRIPT
# اسکریپت تست API آنالیتیکس
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

import requests
import json
import sys
from datetime import datetime

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000/api"

# Color codes for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_colored(text, color):
    """Print colored text"""
    print(f"{color}{text}{Colors.ENDC}")

def print_header(text):
    """Print section header"""
    print_colored(f"\n{Colors.BOLD}{'='*60}{Colors.ENDC}", Colors.CYAN)
    print_colored(f"{Colors.BOLD}{text}{Colors.ENDC}", Colors.CYAN)
    print_colored(f"{Colors.BOLD}{'='*60}{Colors.ENDC}", Colors.CYAN)

def test_endpoint(url, method="GET", data=None, description=""):
    """Test an API endpoint"""
    print_colored(f"\n🔍 Testing: {description}", Colors.BLUE)
    print_colored(f"   URL: {url}", Colors.WHITE)
    print_colored(f"   Method: {method}", Colors.WHITE)
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        elif method == "PUT":
            response = requests.put(url, json=data, timeout=10)
        elif method == "DELETE":
            response = requests.delete(url, timeout=10)
        
        print_colored(f"   Status: {response.status_code}", 
                     Colors.GREEN if response.status_code < 400 else Colors.RED)
        
        if response.status_code < 400:
            try:
                json_data = response.json()
                if isinstance(json_data, dict):
                    print_colored(f"   Response Keys: {list(json_data.keys())}", Colors.WHITE)
                    if 'results' in json_data:
                        print_colored(f"   Results Count: {len(json_data['results'])}", Colors.WHITE)
                elif isinstance(json_data, list):
                    print_colored(f"   Results Count: {len(json_data)}", Colors.WHITE)
                
                # Show first few characters of response
                response_str = json.dumps(json_data, indent=2)[:200]
                print_colored(f"   Sample Response: {response_str}...", Colors.YELLOW)
                
            except json.JSONDecodeError:
                print_colored(f"   Response: {response.text[:100]}...", Colors.YELLOW)
        else:
            print_colored(f"   Error: {response.text}", Colors.RED)
            
        return response.status_code < 400
        
    except requests.exceptions.RequestException as e:
        print_colored(f"   ❌ Request Error: {e}", Colors.RED)
        return False
    except Exception as e:
        print_colored(f"   ❌ Unexpected Error: {e}", Colors.RED)
        return False

def main():
    """Main test function"""
    print_colored(f"🚀 Analytics API Test Suite", Colors.PURPLE)
    print_colored(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", Colors.WHITE)
    print_colored(f"   Base URL: {BASE_URL}", Colors.WHITE)
    
    # Test results
    test_results = []
    
    # Test 1: Health Check
    print_header("1. HEALTH CHECK")
    success = test_endpoint(f"{BASE_URL}/analytics/", description="Analytics Root Endpoint")
    test_results.append(("Health Check", success))
    
    # Test 2: Dashboard Endpoints
    print_header("2. DASHBOARD ENDPOINTS")
    
    # List dashboards
    success = test_endpoint(f"{BASE_URL}/analytics/dashboards/", description="List Dashboards")
    test_results.append(("List Dashboards", success))
    
    # Get dashboard details (assuming ID 1 exists)
    success = test_endpoint(f"{BASE_URL}/analytics/dashboards/1/", description="Get Dashboard Details")
    test_results.append(("Dashboard Details", success))
    
    # Test 3: Widget Endpoints
    print_header("3. WIDGET ENDPOINTS")
    
    # List widgets
    success = test_endpoint(f"{BASE_URL}/analytics/widgets/", description="List Widgets")
    test_results.append(("List Widgets", success))
    
    # Test widget data
    success = test_endpoint(f"{BASE_URL}/analytics/widgets/1/data/", description="Get Widget Data")
    test_results.append(("Widget Data", success))
    
    # Test 4: Data Source Endpoints
    print_header("4. DATA SOURCE ENDPOINTS")
    
    # List data sources
    success = test_endpoint(f"{BASE_URL}/analytics/data-sources/", description="List Data Sources")
    test_results.append(("Data Sources", success))
    
    # Test specific data source
    success = test_endpoint(f"{BASE_URL}/analytics/data-sources/student_count/data/", 
                          description="Student Count Data")
    test_results.append(("Student Count Data", success))
    
    success = test_endpoint(f"{BASE_URL}/analytics/data-sources/student_by_status/data/", 
                          description="Student by Status Data")
    test_results.append(("Student by Status Data", success))
    
    success = test_endpoint(f"{BASE_URL}/analytics/data-sources/grade_distribution/data/", 
                          description="Grade Distribution Data")
    test_results.append(("Grade Distribution Data", success))
    
    # Test 5: Report Endpoints
    print_header("5. REPORT ENDPOINTS")
    
    # List reports
    success = test_endpoint(f"{BASE_URL}/analytics/reports/", description="List Reports")
    test_results.append(("List Reports", success))
    
    # Test report execution (if reports exist)
    success = test_endpoint(f"{BASE_URL}/analytics/reports/1/execute/", 
                          method="POST", description="Execute Report")
    test_results.append(("Execute Report", success))
    
    # Test 6: Analytics Metrics
    print_header("6. ANALYTICS METRICS")
    
    # List metrics
    success = test_endpoint(f"{BASE_URL}/analytics/analytics/", description="List Analytics Metrics")
    test_results.append(("Analytics Metrics", success))
    
    # System stats
    success = test_endpoint(f"{BASE_URL}/analytics/analytics/system_stats/", 
                          description="System Statistics")
    test_results.append(("System Stats", success))
    
    # Test 7: Schema Documentation
    print_header("7. API DOCUMENTATION")
    
    # OpenAPI schema
    success = test_endpoint(f"{BASE_URL}/schema/", description="OpenAPI Schema")
    test_results.append(("API Schema", success))
    
    # Test Results Summary
    print_header("TEST RESULTS SUMMARY")
    
    passed = sum(1 for _, success in test_results if success)
    total = len(test_results)
    
    print_colored(f"\n📊 Test Results:", Colors.BOLD)
    print_colored(f"   ✅ Passed: {passed}/{total}", Colors.GREEN)
    print_colored(f"   ❌ Failed: {total - passed}/{total}", Colors.RED)
    print_colored(f"   📈 Success Rate: {(passed/total)*100:.1f}%", 
                 Colors.GREEN if passed/total > 0.8 else Colors.YELLOW)
    
    print_colored(f"\n📝 Detailed Results:", Colors.WHITE)
    for test_name, success in test_results:
        status = "✅ PASS" if success else "❌ FAIL"
        color = Colors.GREEN if success else Colors.RED
        print_colored(f"   {status} {test_name}", color)
    
    # Recommendations
    if passed < total:
        print_colored(f"\n💡 Recommendations:", Colors.YELLOW)
        print_colored(f"   • Check server is running on {BASE_URL}", Colors.WHITE)
        print_colored(f"   • Verify database has sample data", Colors.WHITE)
        print_colored(f"   • Review failed endpoint logs", Colors.WHITE)
        print_colored(f"   • Ensure all migrations are applied", Colors.WHITE)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_colored(f"\n\n⚠️  Test interrupted by user", Colors.YELLOW)
        sys.exit(1)
    except Exception as e:
        print_colored(f"\n\n❌ Test suite failed: {e}", Colors.RED)
        sys.exit(1)
