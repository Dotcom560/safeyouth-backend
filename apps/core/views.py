from django.shortcuts import render

# Create your views here.
# backend/apps/core/views.py
from django.http import JsonResponse
from django.shortcuts import render

def bad_request(request, exception=None):
    """400 Bad Request Handler"""
    return JsonResponse({
        'error': 'Bad Request',
        'message': 'The request could not be understood by the server.'
    }, status=400)

def permission_denied(request, exception=None):
    """403 Permission Denied Handler"""
    return JsonResponse({
        'error': 'Permission Denied',
        'message': 'You do not have permission to access this resource.'
    }, status=403)

def page_not_found(request, exception=None):
    """404 Not Found Handler"""
    return JsonResponse({
        'error': 'Not Found',
        'message': 'The requested resource was not found on this server.'
    }, status=404)

def server_error(request):
    """500 Internal Server Error Handler"""
    return JsonResponse({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred. Please try again later.'
    }, status=500)