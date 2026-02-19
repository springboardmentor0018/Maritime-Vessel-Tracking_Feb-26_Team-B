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

admin.site.register(Vessel)
admin.site.register(Port)
admin.site.register(Voyage)
admin.site.register(Event)
admin.site.register(Notification)
admin.site.register(UserProfile)
admin.site.register(Subscription)
