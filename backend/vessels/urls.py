"""
Vessels URL Configuration
"""
from django.urls import path
from . import views

urlpatterns = [
    # Vessel endpoints
    path('vessels/', views.vessel_list, name='vessel-list'),
    path('vessels/search/', views.vessel_search, name='vessel-search'),
    path('vessels/refresh/', views.vessel_refresh, name='vessel-refresh'),
    path('vessels/<str:mmsi>/', views.vessel_detail, name='vessel-detail'),

    # Subscription endpoints
    path('subscriptions/', views.subscription_list_create, name='subscription-list-create'),
    path('subscriptions/<int:pk>/', views.subscription_detail, name='subscription-detail'),
]
