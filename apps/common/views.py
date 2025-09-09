from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint for monitoring"""
    return Response({
        'status': 'healthy',
        'message': 'Backend is running successfully',
        'debug': settings.DEBUG,
        'database': 'connected' if check_database() else 'disconnected'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def api_info(request):
    """API information endpoint"""
    return Response({
        'name': 'University Management System API',
        'version': '1.0.0',
        'description': 'Django REST API for university management',
        'endpoints': {
            'authentication': '/api/auth/',
            'users': '/api/users/',
            'courses': '/api/courses/',
            'assignments': '/api/assignments/',
            'grades': '/api/grades/',
            'notifications': '/api/notifications/',
            'reports': '/api/reports/',
        }
    }, status=status.HTTP_200_OK)


def check_database():
    """Check database connection"""
    try:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        row = cursor.fetchone()
        return row is not None
    except Exception:
        return False
