from django.contrib import admin

from .models import UserProfile, Driver

admin.site.register(UserProfile)
admin.site.register(Driver)
