"""
Accounts admin configuration
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, OTPCode


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_email_verified', 'organization', 'is_active', 'date_joined')
    list_filter = ('is_email_verified', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'organization')
    fieldsets = UserAdmin.fieldsets + (
        ('Vessel Tracker Profile', {
            'fields': ('phone', 'organization', 'is_email_verified'),
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('email', 'phone', 'organization'),
        }),
    )


@admin.register(OTPCode)
class OTPCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'is_used', 'created_at')
    list_filter = ('is_used',)
    search_fields = ('user__email', 'code')
    readonly_fields = ('code', 'created_at')
