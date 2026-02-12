from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Vessel, Port

admin.site.register(Vessel)
admin.site.register(Port)