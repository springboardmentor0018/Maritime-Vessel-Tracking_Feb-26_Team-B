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
        'version': '2.0.0',
        'endpoints': {
            'auth': '/api/auth/',
            'vessels': '/api/vessels/',
            'subscriptions': '/api/subscriptions/',
            'voyage_replay': '/api/vessels/<mmsi>/replay/',
            'dashboard': {
                'company_stats': '/api/dashboard/company-stats/',
                'port_metrics': '/api/dashboard/port-metrics/',
                'risk_data': '/api/dashboard/risk-data/',
            },
            'admin_api': {
                'health': '/api/admin-api/health/',
                'logs': '/api/admin-api/logs/',
                'export_vessels': '/api/admin-api/export/vessels/',
                'export_subscriptions': '/api/admin-api/export/subscriptions/',
            },
            'admin_panel': '/admin/',
        }
    })


urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/', include('vessels.urls')),
]
