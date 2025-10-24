from django.contrib import admin
from .models import BookingDriverSide, BookingUserSide, Payment, Share

admin.site.register(BookingDriverSide)
admin.site.register(BookingUserSide)
admin.site.register(Payment)
admin.site.register(Share)
