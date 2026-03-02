from django.contrib import admin
from .models import (
    Vessel,
    Port,
    Voyage,
    Event,
    Notification,
    UserProfile,
    Subscription
)

# -------------------------
# Vessel Admin
# -------------------------
@admin.register(Vessel)
class VesselAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'imo_number',
        'vessel_type',
        'operator',
        'speed',
        'heading',
        'last_update'
    )
    search_fields = ('name', 'imo_number', 'operator')
    list_filter = ('vessel_type', 'cargo_type')
    ordering = ('name',)
    readonly_fields = ('last_update',)


# -------------------------
# Port Admin
# -------------------------
@admin.register(Port)
class PortAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'country',
        'congestion_score',
        'avg_wait_time',
        'arrivals',
        'departures',
        'last_update'
    )
    list_filter = ('country',)
    search_fields = ('name', 'country', 'location')
    ordering = ('name',)
    readonly_fields = ('last_update',)


# -------------------------
# Voyage Admin
# -------------------------
@admin.register(Voyage)
class VoyageAdmin(admin.ModelAdmin):
    list_display = (
        'vessel',
        'port_from',
        'port_to',
        'departure_time',
        'arrival_time',
        'status'
    )
    list_filter = ('status', 'port_from', 'port_to')
    search_fields = ('vessel__name',)
    ordering = ('-departure_time',)


# -------------------------
# Event Admin
# -------------------------
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'event_type',
        'vessel',
        'location',
        'timestamp'
    )
    list_filter = ('event_type',)
    search_fields = ('event_type', 'vessel__name')
    ordering = ('-timestamp',)


# -------------------------
# Notification Admin
# -------------------------
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'alert_type',
        'port',
        'is_read',
        'created_at'
    )
    list_filter = ('alert_type', 'is_read')
    search_fields = ('user__username', 'message')
    ordering = ('-created_at',)
    actions = ['mark_as_read']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected notifications as read"


# -------------------------
# User Profile Admin
# -------------------------
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'role',
        'company_name',
        'created_at'
    )
    list_filter = ('role',)
    search_fields = ('user__username', 'company_name')
    readonly_fields = ('created_at',)


# -------------------------
# Subscription Admin
# -------------------------
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'vessel',
        'alert_enabled',
        'created_at'
    )
    list_filter = ('alert_enabled',)
    search_fields = ('user__username', 'vessel__name')
    readonly_fields = ('created_at',)