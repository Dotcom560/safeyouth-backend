# apps/core/views.py
from django.http import JsonResponse

def bad_request(request, exception=None):
    return JsonResponse({'error': 'Bad Request'}, status=400)

def permission_denied(request, exception=None):
    return JsonResponse({'error': 'Permission Denied'}, status=403)

def page_not_found(request, exception=None):
    return JsonResponse({'error': 'Not Found'}, status=404)

def server_error(request):
    return JsonResponse({'error': 'Internal Server Error'}, status=500)