from django.contrib import admin
from .models import Vessel, Port, Voyage, Event, Notification

admin.site.register(Vessel)
admin.site.register(Port)
admin.site.register(Voyage)
admin.site.register(Event)
admin.site.register(Notification)
from .models import UserProfile

admin.site.register(UserProfile)