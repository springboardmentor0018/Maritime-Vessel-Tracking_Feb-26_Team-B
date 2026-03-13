"""
vessel_tracker URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def api_root(request):
    """API root endpoint with overview of available endpoints."""
    return JsonResponse({
        'message': 'Vessel Tracker API — Infosys Springboard',
        'version': '1.0.0',
        'endpoints': {
            'auth': '/api/auth/',
            'vessels': '/api/vessels/',
            'subscriptions': '/api/subscriptions/',
            'admin': '/admin/',
        }
    })


urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/', include('vessels.urls')),
]
