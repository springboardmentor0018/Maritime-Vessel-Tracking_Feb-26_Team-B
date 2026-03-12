"""
Vessels URL Configuration
"""
from django.urls import path
from . import views
from . import admin_views

urlpatterns = [
    # ─── Vessel endpoints ────────────────────────────────────────────────
    path('vessels/', views.vessel_list, name='vessel-list'),
    path('vessels/search/', views.vessel_search, name='vessel-search'),
    path('vessels/refresh/', views.vessel_refresh, name='vessel-refresh'),
    path('vessels/<str:mmsi>/', views.vessel_detail, name='vessel-detail'),

    # ─── Voyage Replay endpoints ─────────────────────────────────────────
    path('vessels/<str:mmsi>/replay/', views.voyage_replay, name='voyage-replay'),
    path('vessels/<str:mmsi>/replay/latest/', views.voyage_replay_latest, name='voyage-replay-latest'),

    # ─── Subscription endpoints ──────────────────────────────────────────
    path('subscriptions/', views.subscription_list_create, name='subscription-list-create'),
    path('subscriptions/<int:pk>/', views.subscription_detail, name='subscription-detail'),

    # ─── Dashboard endpoints ─────────────────────────────────────────────
    path('dashboard/company-stats/', views.dashboard_company_stats, name='dashboard-company-stats'),
    path('dashboard/port-metrics/', views.dashboard_port_metrics, name='dashboard-port-metrics'),
    path('dashboard/risk-data/', views.dashboard_risk_data, name='dashboard-risk-data'),

    # ─── Admin API endpoints ─────────────────────────────────────────────
    path('admin-api/health/', admin_views.api_health, name='admin-health'),
    path('admin-api/logs/', admin_views.api_logs, name='admin-logs'),
    path('admin-api/export/vessels/', admin_views.export_vessels_csv, name='admin-export-vessels'),
    path('admin-api/export/subscriptions/', admin_views.export_subscriptions_csv, name='admin-export-subscriptions'),
]
