#!/usr/bin/env python3
"""
اسکریپت تست تمام API endpoints
"""

import requests
import json
from datetime import datetime

# Base URL
BASE_URL = "http://127.0.0.1:8000"

# لیست endpoint های اصلی برای تست
ENDPOINTS = [
    # Health and Monitoring
    "/api/health/",
    "/api/info/", 
    "/api/version/",
    "/api/status/",
    
    # API Documentation
    "/api/schema/",
    "/api/docs/",
    "/api/redoc/",
    
    # Apps endpoints
    "/api/",  # common
    "/api/users/",
    "/api/courses/",
    "/api/notifications/",
    "/api/analytics/",
    "/api/data-management/",
    "/api/mobile/",
    "/api/ai-ml/",
    "/api/grades/",
    "/api/schedules/",
    "/api/exams/",
    "/api/library/",
    "/api/financial/",
    "/api/attendance/",
    "/api/research/",
    "/api/announcements/",
    "/api/assignments/",
    "/api/auth/",
    "/api/dormitory/",
    "/api/reports/",
    
    # Auth endpoints
    "/api/auth/token/",
    "/api/token/",
    "/api/token/refresh/",
    
    # Dormitory specific endpoints
    "/api/dormitory/complexes/",
    "/api/dormitory/buildings/",
    "/api/dormitory/rooms/",
    "/api/dormitory/accommodations/",
    "/api/dormitory/staff/",
    "/api/dormitory/maintenance/",
]

def test_endpoint(url):
    """تست یک endpoint"""
    try:
        full_url = BASE_URL + url
        response = requests.get(full_url, timeout=10)
        return {
            'url': url,
            'status_code': response.status_code,
            'success': response.status_code < 500,  # هر چیز کمتر از 500 موفق محسوب می‌شود
            'error': None,
            'response_size': len(response.content),
            'content_type': response.headers.get('content-type', '')
        }
    except requests.exceptions.ConnectionError:
        return {
            'url': url,
            'status_code': None,
            'success': False,
            'error': 'Connection Error - Server might be down',
            'response_size': 0,
            'content_type': ''
        }
    except requests.exceptions.Timeout:
        return {
            'url': url,
            'status_code': None,
            'success': False,
            'error': 'Timeout',
            'response_size': 0,
            'content_type': ''
        }
    except Exception as e:
        return {
            'url': url,
            'status_code': None,
            'success': False,
            'error': str(e),
            'response_size': 0,
            'content_type': ''
        }

def main():
    """تابع اصلی"""
    print("🧪 شروع تست تمام API endpoints...")
    print("=" * 60)
    
    results = []
    successful = 0
    failed = 0
    
    for endpoint in ENDPOINTS:
        print(f"Testing: {endpoint:<40}", end=" ")
        result = test_endpoint(endpoint)
        results.append(result)
        
        if result['success']:
            print(f"✅ {result['status_code']}")
            successful += 1
        else:
            print(f"❌ {result.get('status_code', 'ERROR')} - {result['error']}")
            failed += 1
    
    print("=" * 60)
    print(f"📊 نتایج تست:")
    print(f"✅ موفق: {successful}")
    print(f"❌ ناموفق: {failed}")
    print(f"📝 کل: {len(ENDPOINTS)}")
    print(f"📈 درصد موفقیت: {(successful/len(ENDPOINTS)*100):.1f}%")
    
    # نمایش جزئیات خطاها
    if failed > 0:
        print("\n🔍 جزئیات خطاها:")
        print("-" * 40)
        for result in results:
            if not result['success']:
                print(f"❌ {result['url']}")
                print(f"   خطا: {result['error']}")
                if result['status_code']:
                    print(f"   کد وضعیت: {result['status_code']}")
                print()
    
    # ذخیره نتایج در فایل
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"api_test_results_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': timestamp,
            'summary': {
                'total': len(ENDPOINTS),
                'successful': successful,
                'failed': failed,
                'success_rate': successful/len(ENDPOINTS)*100
            },
            'results': results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"📄 نتایج کامل در فایل {filename} ذخیره شد")
    
    return failed == 0

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
