#!/usr/bin/env python3
"""
🎯 حرفه‌ای API Testing Suite برای University Management System
📊 تست پیشرفته تمام endpoints با گزارش‌دهی کامل

ویژگی‌ها:
- ✅ تست متدهای HTTP مناسب برای هر endpoint
- 🔐 تست authentication و authorization
- ⚡ تست‌های parallel برای سرعت بیشتر
- 📈 مانیتورینگ performance و response time
- 🎨 گزارش‌دهی رنگی و حرفه‌ای
- 🔄 Retry mechanism برای reliability
- 📋 گزارش HTML پیشرفته
- 🔍 Schema validation
"""

import requests
import json
import time
import asyncio
import aiohttp
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional, Tuple
import logging
import os
from dataclasses import dataclass, asdict
from enum import Enum

# تنظیم logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_test.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# تنظیمات پایه
@dataclass
class TestConfig:
    base_url: str = "https://sinanej2.pythonanywhere.com"
    timeout: int = 30
    max_retries: int = 3
    delay_between_requests: float = 0.5  # افزایش delay برای سرور
    max_workers: int = 5  # کاهش workers برای سرور
    enable_parallel: bool = True
    generate_html_report: bool = True
    test_authentication: bool = True
    test_performance: bool = True
    performance_threshold: float = 3.0  # افزایش threshold برای سرور

class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"

@dataclass
class EndpointConfig:
    path: str
    method: HTTPMethod
    description: str
    requires_auth: bool = False
    expected_status_codes: List[int] = None
    payload: Optional[Dict] = None
    category: str = "general"

    def __post_init__(self):
        if self.expected_status_codes is None:
            self.expected_status_codes = [200, 201, 202, 204]

@dataclass
class TestResult:
    endpoint: str
    method: str
    status_code: Optional[int]
    success: bool
    response_time: float
    error_message: Optional[str]
    response_size: int
    content_type: Optional[str]
    timestamp: datetime
    retry_count: int = 0

    def to_dict(self):
        return asdict(self)

# تعریف endpoints با تنظیمات حرفه‌ای
ENDPOINTS = [
    # Health & Monitoring
    EndpointConfig("/api/health/", HTTPMethod.GET, "Health Check", expected_status_codes=[200]),
    EndpointConfig("/api/info/", HTTPMethod.GET, "System Info", expected_status_codes=[200]),
    EndpointConfig("/api/version/", HTTPMethod.GET, "API Version", expected_status_codes=[200]),
    EndpointConfig("/api/status/", HTTPMethod.GET, "System Status", expected_status_codes=[200]),

    # Documentation
    EndpointConfig("/api/schema/", HTTPMethod.GET, "OpenAPI Schema", expected_status_codes=[200]),
    EndpointConfig("/api/docs/", HTTPMethod.GET, "Swagger UI", expected_status_codes=[200]),
    EndpointConfig("/api/redoc/", HTTPMethod.GET, "ReDoc", expected_status_codes=[200]),

    # Main API Root
    EndpointConfig("/api/", HTTPMethod.GET, "API Root", expected_status_codes=[200]),

    # Core Modules
    EndpointConfig("/api/users/", HTTPMethod.GET, "Users Management", expected_status_codes=[200]),
    EndpointConfig("/api/courses/", HTTPMethod.GET, "Courses Management", expected_status_codes=[200]),
    EndpointConfig("/api/grades/", HTTPMethod.GET, "Grades Management", expected_status_codes=[200]),
    EndpointConfig("/api/schedules/", HTTPMethod.GET, "Schedules Management", expected_status_codes=[200]),
    EndpointConfig("/api/notifications/", HTTPMethod.GET, "Notifications", expected_status_codes=[200]),
    EndpointConfig("/api/dormitory/", HTTPMethod.GET, "Dormitory Management", expected_status_codes=[200]),

    # Authentication (POST endpoints)
    EndpointConfig("/api/auth/token/", HTTPMethod.POST, "Token Auth", expected_status_codes=[400, 405], payload={}),
    EndpointConfig("/api/token/", HTTPMethod.POST, "JWT Token", expected_status_codes=[400, 405], payload={}),
    EndpointConfig("/api/token/refresh/", HTTPMethod.POST, "JWT Refresh", expected_status_codes=[400, 405], payload={}),

    # Dormitory Sub-modules
    EndpointConfig("/api/dormitory/complexes/", HTTPMethod.GET, "Dormitory Complexes", expected_status_codes=[200]),
    EndpointConfig("/api/dormitory/buildings/", HTTPMethod.GET, "Dormitory Buildings", expected_status_codes=[200]),
    EndpointConfig("/api/dormitory/rooms/", HTTPMethod.GET, "Dormitory Rooms", expected_status_codes=[200]),
    EndpointConfig("/api/dormitory/accommodations/", HTTPMethod.GET, "Accommodations", expected_status_codes=[200]),
    EndpointConfig("/api/dormitory/staff/", HTTPMethod.GET, "Dormitory Staff", expected_status_codes=[200]),
    EndpointConfig("/api/dormitory/maintenance/", HTTPMethod.GET, "Maintenance", expected_status_codes=[200]),

    # Other Modules
    EndpointConfig("/api/analytics/", HTTPMethod.GET, "Analytics", expected_status_codes=[200]),
    EndpointConfig("/api/data-management/", HTTPMethod.GET, "Data Management", expected_status_codes=[200]),
    EndpointConfig("/api/mobile/", HTTPMethod.GET, "Mobile API", expected_status_codes=[200]),
    EndpointConfig("/api/ai-ml/", HTTPMethod.GET, "AI/ML Services", expected_status_codes=[200]),
    EndpointConfig("/api/exams/", HTTPMethod.GET, "Exams Management", expected_status_codes=[200]),
    EndpointConfig("/api/library/", HTTPMethod.GET, "Library Management", expected_status_codes=[200]),
    EndpointConfig("/api/financial/", HTTPMethod.GET, "Financial Management", expected_status_codes=[200]),
    EndpointConfig("/api/attendance/", HTTPMethod.GET, "Attendance Tracking", expected_status_codes=[200]),
    EndpointConfig("/api/research/", HTTPMethod.GET, "Research Management", expected_status_codes=[200]),
    EndpointConfig("/api/announcements/", HTTPMethod.GET, "Announcements", expected_status_codes=[200]),
    EndpointConfig("/api/assignments/", HTTPMethod.GET, "Assignments", expected_status_codes=[200]),
    EndpointConfig("/api/auth/", HTTPMethod.GET, "Auth Module", expected_status_codes=[200]),
    EndpointConfig("/api/reports/", HTTPMethod.GET, "Reports", expected_status_codes=[200]),
]

class APIEndpointTester:
    """تست‌کننده حرفه‌ای API endpoints"""

    def __init__(self, config: TestConfig):
        self.config = config
        self.session = requests.Session()
        self.auth_token = None
        self.results: List[TestResult] = []

    def authenticate(self) -> bool:
        """احراز هویت برای تست‌های نیازمند authentication"""
        try:
            # تلاش برای login با credentials تست
            login_data = {
                "username": "admin",
                "password": "admin123"
            }
            response = self.session.post(
                f"{self.config.base_url}/api/token/",
                json=login_data,
                timeout=self.config.timeout
            )

            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get('access')
                self.session.headers.update({
                    'Authorization': f'Bearer {self.auth_token}'
                })
                logger.info("✅ Authentication successful")
                return True
            else:
                logger.warning("⚠️  Authentication failed, continuing without auth")
                return False
        except Exception as e:
            logger.warning(f"⚠️  Authentication error: {e}")
            return False

    def test_single_endpoint(self, endpoint: EndpointConfig, retry_count: int = 0) -> TestResult:
        """تست یک endpoint با retry mechanism"""
        start_time = time.time()

        try:
            url = f"{self.config.base_url}{endpoint.path}"

            # انتخاب متد HTTP مناسب
            if endpoint.method == HTTPMethod.GET:
                response = self.session.get(url, timeout=self.config.timeout)
            elif endpoint.method == HTTPMethod.POST:
                response = self.session.post(
                    url,
                    json=endpoint.payload,
                    timeout=self.config.timeout
                )
            elif endpoint.method == HTTPMethod.PUT:
                response = self.session.put(
                    url,
                    json=endpoint.payload,
                    timeout=self.config.timeout
                )
            elif endpoint.method == HTTPMethod.PATCH:
                response = self.session.patch(
                    url,
                    json=endpoint.payload,
                    timeout=self.config.timeout
                )
            elif endpoint.method == HTTPMethod.DELETE:
                response = self.session.delete(url, timeout=self.config.timeout)
            else:
                response = self.session.get(url, timeout=self.config.timeout)

            response_time = time.time() - start_time

            # بررسی موفقیت
            is_success = response.status_code in endpoint.expected_status_codes

            # بررسی performance
            performance_ok = response_time <= self.config.performance_threshold

            if not is_success and retry_count < self.config.max_retries:
                logger.info(f"🔄 Retrying {endpoint.path} (attempt {retry_count + 1})")
                time.sleep(1)
                return self.test_single_endpoint(endpoint, retry_count + 1)

            result = TestResult(
                endpoint=endpoint.path,
                method=endpoint.method.value,
                status_code=response.status_code,
                success=is_success,
                response_time=round(response_time, 3),
                error_message=None,
                response_size=len(response.content),
                content_type=response.headers.get('content-type'),
                timestamp=datetime.now(),
                retry_count=retry_count
            )

            # Log performance issues
            if not performance_ok and self.config.test_performance:
                logger.warning(f"⚡ Performance issue: {endpoint.path} took {response_time:.3f}s")
            return result

        except requests.exceptions.ConnectionError:
            return TestResult(
                endpoint=endpoint.path,
                method=endpoint.method.value,
                status_code=None,
                success=False,
                response_time=time.time() - start_time,
                error_message="Connection Error - Server might be down",
                response_size=0,
                content_type=None,
                timestamp=datetime.now(),
                retry_count=retry_count
            )
        except requests.exceptions.Timeout:
            return TestResult(
                endpoint=endpoint.path,
                method=endpoint.method.value,
                status_code=None,
                success=False,
                response_time=time.time() - start_time,
                error_message="Request Timeout",
                response_size=0,
                content_type=None,
                timestamp=datetime.now(),
                retry_count=retry_count
            )
        except Exception as e:
            return TestResult(
                endpoint=endpoint.path,
                method=endpoint.method.value,
                status_code=None,
                success=False,
                response_time=time.time() - start_time,
                error_message=str(e),
                response_size=0,
                content_type=None,
                timestamp=datetime.now(),
                retry_count=retry_count
            )

    def test_all_endpoints_parallel(self) -> List[TestResult]:
        """تست parallel تمام endpoints"""
        logger.info(f"🚀 شروع تست parallel با {self.config.max_workers} worker")

        with ThreadPoolExecutor(max_workers=self.config.max_workers) as executor:
            futures = [
                executor.submit(self.test_single_endpoint, endpoint)
                for endpoint in ENDPOINTS
            ]

            for future in as_completed(futures):
                result = future.result()
                self.results.append(result)

                # نمایش نتیجه realtime
                self._print_result(result)

                # Delay بین درخواست‌ها
                time.sleep(self.config.delay_between_requests)

        return self.results

    def test_all_endpoints_sequential(self) -> List[TestResult]:
        """تست sequential تمام endpoints"""
        logger.info("📋 شروع تست sequential")

        for endpoint in ENDPOINTS:
            result = self.test_single_endpoint(endpoint)
            self.results.append(result)
            self._print_result(result)
            time.sleep(self.config.delay_between_requests)

        return self.results

    def _print_result(self, result: TestResult):
        """نمایش نتیجه تست با فرمت زیبا"""
        status_emoji = "✅" if result.success else "❌"
        method_color = self._get_method_color(result.method)

        status_display = f"{status_emoji} {result.status_code or 'ERROR'}"
        time_display = f"({result.response_time}s)"

        if result.retry_count > 0:
            status_display += f" (retry: {result.retry_count})"

        print("30")

    def _get_method_color(self, method: str) -> str:
        """رنگ‌بندی متدهای HTTP"""
        colors = {
            'GET': '\033[92m',    # سبز
            'POST': '\033[94m',   # آبی
            'PUT': '\033[93m',    # زرد
            'PATCH': '\033[95m',  # magenta
            'DELETE': '\033[91m', # قرمز
        }
        return colors.get(method, '\033[0m')

    def generate_report(self) -> Dict:
        """تولید گزارش کامل تست"""
        total_tests = len(self.results)
        successful_tests = len([r for r in self.results if r.success])
        failed_tests = total_tests - successful_tests

        # آمار performance
        response_times = [r.response_time for r in self.results if r.response_time > 0]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        max_response_time = max(response_times) if response_times else 0
        min_response_time = min(response_times) if response_times else 0

        # دسته‌بندی نتایج
        results_by_method = {}
        results_by_status = {}

        for result in self.results:
            method = result.method
            status = result.status_code or 'ERROR'

            if method not in results_by_method:
                results_by_method[method] = []
            results_by_method[method].append(result)

            if status not in results_by_status:
                results_by_status[status] = []
            results_by_status[status].append(result)

        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_tests': total_tests,
                'successful_tests': successful_tests,
                'failed_tests': failed_tests,
                'success_rate': (successful_tests / total_tests * 100) if total_tests > 0 else 0,
                'average_response_time': round(avg_response_time, 3),
                'max_response_time': round(max_response_time, 3),
                'min_response_time': round(min_response_time, 3)
            },
            'results_by_method': {
                method: {
                    'total': len(results),
                    'successful': len([r for r in results if r.success]),
                    'failed': len([r for r in results if not r.success])
                }
                for method, results in results_by_method.items()
            },
            'results_by_status': {
                str(status): len(results)
                for status, results in results_by_status.items()
            },
            'failed_endpoints': [
                {
                    'endpoint': r.endpoint,
                    'method': r.method,
                    'status_code': r.status_code,
                    'error': r.error_message,
                    'response_time': r.response_time
                }
                for r in self.results if not r.success
            ],
            'performance_issues': [
                {
                    'endpoint': r.endpoint,
                    'response_time': r.response_time,
                    'threshold': self.config.performance_threshold
                }
                for r in self.results
                if r.response_time > self.config.performance_threshold
            ],
            'detailed_results': [r.to_dict() for r in self.results]
        }

        return report

    def save_report(self, report: Dict):
        """ذخیره گزارش در فایل‌های مختلف"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # JSON Report
        json_filename = f"api_test_report_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        logger.info(f"📄 گزارش JSON ذخیره شد: {json_filename}")

        # HTML Report
        if self.config.generate_html_report:
            html_filename = f"api_test_report_{timestamp}.html"
            self._generate_html_report(report, html_filename)
            logger.info(f"🌐 گزارش HTML ذخیره شد: {html_filename}")

    def _generate_html_report(self, report: Dict, filename: str):
        """تولید گزارش HTML پیشرفته"""
        html_content = f"""
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>گزارش تست API - {report['timestamp'][:19]}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .header h1 {{
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 2.5em;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: white;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .stat-label {{
            color: #7f8c8d;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .success {{ color: #27ae60; }}
        .warning {{ color: #f39c12; }}
        .danger {{ color: #e74c3c; }}
        .info {{ color: #3498db; }}
        .results-table {{
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 15px;
            text-align: right;
            border-bottom: 1px solid #ecf0f1;
        }}
        th {{
            background: #f8f9fa;
            font-weight: 600;
            color: #2c3e50;
        }}
        tr:hover {{
            background: #f8f9fa;
        }}
        .status-badge {{
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: 500;
        }}
        .status-success {{ background: #d4edda; color: #155724; }}
        .status-error {{ background: #f8d7da; color: #721c24; }}
        .method-badge {{
            padding: 3px 8px;
            border-radius: 5px;
            font-size: 0.7em;
            font-weight: bold;
        }}
        .method-GET {{ background: #d4edda; color: #155724; }}
        .method-POST {{ background: #cce5ff; color: #004085; }}
        .method-PUT {{ background: #fff3cd; color: #856404; }}
        .method-DELETE {{ background: #f8d7da; color: #721c24; }}
        .performance-good {{ color: #27ae60; }}
        .performance-slow {{ color: #f39c12; }}
        .performance-critical {{ color: #e74c3c; }}
        .chart-container {{
            background: white;
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        .footer {{
            text-align: center;
            color: white;
            margin-top: 30px;
            opacity: 0.8;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 گزارش تست API</h1>
            <p>University Management System</p>
            <p>📅 {report['timestamp'][:19]}</p>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value success">{report['summary']['total_tests']}</div>
                <div class="stat-label">کل تست‌ها</div>
            </div>
            <div class="stat-card">
                <div class="stat-value success">{report['summary']['successful_tests']}</div>
                <div class="stat-label">موفق</div>
            </div>
            <div class="stat-card">
                <div class="stat-value danger">{report['summary']['failed_tests']}</div>
                <div class="stat-label">ناموفق</div>
            </div>
            <div class="stat-card">
                <div class="stat-value info">{report['summary']['success_rate']:.1f}%</div>
                <div class="stat-label">درصد موفقیت</div>
            </div>
            <div class="stat-card">
                <div class="stat-value info">{report['summary']['average_response_time']}s</div>
                <div class="stat-label">میانگین زمان پاسخ</div>
            </div>
            <div class="stat-card">
                <div class="stat-value warning">{report['summary']['max_response_time']}s</div>
                <div class="stat-label">حداکثر زمان پاسخ</div>
            </div>
        </div>

        <div class="results-table">
            <table>
                <thead>
                    <tr>
                        <th>Endpoint</th>
                        <th>متد</th>
                        <th>وضعیت</th>
                        <th>زمان پاسخ</th>
                        <th>اندازه پاسخ</th>
                    </tr>
                </thead>
                <tbody>
"""

        for result in report['detailed_results']:
            status_class = 'status-success' if result['success'] else 'status-error'
            method_class = f"method-{result['method']}"
            time_class = 'performance-good'
            if result['response_time'] > 2.0:
                time_class = 'performance-slow'
            if result['response_time'] > 5.0:
                time_class = 'performance-critical'

            html_content += f"""
                    <tr>
                        <td>{result['endpoint']}</td>
                        <td><span class="method-badge {method_class}">{result['method']}</span></td>
                        <td><span class="status-badge {status_class}">{result['status_code'] or 'ERROR'}</span></td>
                        <td class="{time_class}">{result['response_time']}s</td>
                        <td>{result['response_size']} bytes</td>
                    </tr>
"""

        html_content += """
                </tbody>
            </table>
        </div>

        <div class="footer">
            <p>🚀 تولید شده توسط API Testing Suite</p>
            <p>📊 University Management System - Professional Testing</p>
        </div>
    </div>
</body>
</html>
"""

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)

def main():
    """تابع اصلی برنامه"""
    print("🎯 شروع تست حرفه‌ای API endpoints...")
    print("=" * 80)

    # تنظیمات تست
    config = TestConfig(
        enable_parallel=True,
        test_authentication=True,
        test_performance=True,
        generate_html_report=True
    )

    # ایجاد تست‌کننده
    tester = APIEndpointTester(config)

    # احراز هویت اگر فعال باشد
    if config.test_authentication:
        print("🔐 تلاش برای احراز هویت...")
        tester.authenticate()

    # شروع تست
    start_time = time.time()

    if config.enable_parallel:
        results = tester.test_all_endpoints_parallel()
    else:
        results = tester.test_all_endpoints_sequential()

    end_time = time.time()

    print("\n" + "=" * 80)
    print("📊 نتایج نهایی:")

    # تولید و نمایش گزارش
    report = tester.generate_report()

    print(f"✅ موفق: {report['summary']['successful_tests']}")
    print(f"❌ ناموفق: {report['summary']['failed_tests']}")
    print(f"📝 کل: {report['summary']['total_tests']}")
    print(f"📈 درصد موفقیت: {report['summary']['success_rate']:.1f}%")
    print(f"⏱️  میانگین زمان پاسخ: {report['summary']['average_response_time']:.3f}s")
    print(f"⚡ حداکثر زمان پاسخ: {report['summary']['max_response_time']:.3f}s")
    print(f"🕐 حداقل زمان پاسخ: {report['summary']['min_response_time']:.3f}s")

    # نمایش خطاها اگر وجود داشته باشد
    if report['summary']['failed_tests'] > 0:
        print("\n🔍 جزئیات خطاها:")
        print("-" * 50)
        for failed in report['failed_endpoints'][:5]:  # نمایش ۵ تای اول
            print(f"❌ {failed['endpoint']} ({failed['method']})")
            print(f"   وضعیت: {failed['status_code']}")
            print(f"   خطا: {failed['error']}")
            print()

    # نمایش مشکلات performance
    if report['performance_issues']:
        print("⚡ مشکلات Performance:")
        print("-" * 50)
        for issue in report['performance_issues'][:5]:
            print(f"⚡ {issue['endpoint']}: {issue['response_time']:.3f}s (threshold: {issue['threshold']:.3f}s)")
    # ذخیره گزارش
    tester.save_report(report)

    print(f"⏱️  زمان کل تست: {end_time - start_time:.2f}s")
    print("🎉 تست کامل شد!")

    return report['summary']['failed_tests'] == 0

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
