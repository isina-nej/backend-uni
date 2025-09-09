from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def health_check(request):
    """Simple health check endpoint"""
    return Response({'status': 'healthy', 'message': 'Backend is running'})


@api_view(['GET']) 
def api_info(request):
    """API information endpoint"""
    return Response({
        'name': 'University Management System API',
        'version': '1.0.0',
        'description': 'Backend API for University Management System'
    })
