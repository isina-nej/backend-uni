# Custom error handlers for production
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status

def custom_404(request, exception):
    """Custom 404 error handler"""
    if request.path.startswith('/api/'):
        return JsonResponse({
            'error': 'Not Found',
            'message': 'The requested API endpoint was not found.',
            'status_code': 404
        }, status=404)
    
    return render(request, '404.html', status=404)

def custom_500(request):
    """Custom 500 error handler"""
    if request.path.startswith('/api/'):
        return JsonResponse({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred. Please try again later.',
            'status_code': 500
        }, status=500)
    
    return render(request, '500.html', status=500)
