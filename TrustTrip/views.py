from django.shortcuts import render
from booking_n_service.models import BookingUserSide

def home(request):
    if hasattr(request.user, 'user_profile'):
        profile = 'user_profile'
    else:
        profile = 'driver_profile'

    bookings = BookingUserSide.objects.all()
    if profile == 'user_profile':
        bookings = [booking for booking in bookings if (booking.booking_driver_side == None and booking.user.user == request.user) or (booking.booking_driver_side != None and booking.booking_driver_side.ride_status == False)]
    else:
        bookings = [booking for booking in bookings if
                    booking.booking_driver_side == None or booking.booking_driver_side.driver.user == request.user and booking.booking_driver_side.ride_status == False]

    return render(request, 'home.html',{'profile':profile,'bookings':bookings})