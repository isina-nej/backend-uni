#!/bin/bash
# Production deployment validation script
# اسکریپت تأیید استقرار در محیط پروداکشن

echo "🔍 Production Deployment Validation..."

BASE_URL="https://yourusername.pythonanywhere.com"  # Replace with your actual domain

# Function to check URL
check_url() {
    local url=$1
    local description=$2
    
    echo "🌐 Checking $description..."
    
    if curl -s -f -o /dev/null "$url"; then
        echo "✅ $description is accessible"
        return 0
    else
        echo "❌ $description is NOT accessible"
        return 1
    fi
}

# Check main endpoints
echo "📋 Checking main endpoints..."

check_url "$BASE_URL/admin/" "Admin Panel"
check_url "$BASE_URL/api/" "API Root"
check_url "$BASE_URL/api/schema/" "API Schema"
check_url "$BASE_URL/api/schema/swagger-ui/" "Swagger UI"

# Check API endpoints
echo "📋 Checking API endpoints..."

check_url "$BASE_URL/api/auth/login/" "Authentication"
check_url "$BASE_URL/api/users/" "Users API"
check_url "$BASE_URL/api/courses/" "Courses API"
check_url "$BASE_URL/api/grades/" "Grades API"

# Check static files
echo "📁 Checking static files..."
check_url "$BASE_URL/static/admin/css/base.css" "Static Files"

# SSL Certificate check
echo "🔒 Checking SSL Certificate..."
if curl -s -I "$BASE_URL" | grep -q "HTTP/1.1 200\|HTTP/2 200"; then
    echo "✅ SSL Certificate is working"
else
    echo "⚠️ SSL Certificate might have issues"
fi

# Performance check
echo "⚡ Basic Performance Check..."
response_time=$(curl -o /dev/null -s -w '%{time_total}\n' "$BASE_URL/api/")
echo "API response time: ${response_time}s"

if (( $(echo "$response_time < 2.0" | bc -l) )); then
    echo "✅ Response time is good"
else
    echo "⚠️ Response time might be slow"
fi

echo "🏁 Validation completed!"
echo "📊 Review the results above for any issues."

# Generate report
echo "📄 Generating validation report..."
{
    echo "# PythonAnywhere Deployment Validation Report"
    echo "Date: $(date)"
    echo "Domain: $BASE_URL"
    echo ""
    echo "## Checked Endpoints:"
    echo "- Admin Panel: $BASE_URL/admin/"
    echo "- API Root: $BASE_URL/api/"
    echo "- Swagger UI: $BASE_URL/api/schema/swagger-ui/"
    echo ""
    echo "## Performance:"
    echo "- API Response Time: ${response_time}s"
    echo ""
    echo "## Next Steps:"
    echo "1. Test all API endpoints manually"
    echo "2. Verify admin panel functionality"
    echo "3. Check database operations"
    echo "4. Test file upload/download"
    echo "5. Monitor error logs"
} > deployment_validation_report.md

echo "📋 Report saved to: deployment_validation_report.md"
