"""
Vessels admin configuration
"""
from django.contrib import admin
from .models import Vessel, Subscription


@admin.register(Vessel)
class VesselAdmin(admin.ModelAdmin):
    list_display = ('name', 'mmsi', 'imo', 'vessel_type', 'flag', 'cargo', 'speed', 'destination', 'last_updated')
    list_filter = ('vessel_type', 'flag')
    search_fields = ('name', 'mmsi', 'imo', 'callsign', 'flag', 'destination')
    readonly_fields = ('last_updated', 'created_at')
    list_per_page = 30


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'vessel', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'user__username', 'vessel__name', 'vessel__mmsi')
    autocomplete_fields = ('user', 'vessel')
