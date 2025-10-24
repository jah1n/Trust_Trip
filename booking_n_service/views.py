from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import BookingUserSide, Share, BookingDriverSide, Payment


@login_required
def book_a_ride(request):
    if hasattr(request.user, 'user_profile'):
        profile = 'user_profile'
    else:
        return redirect('home')

    if request.method == 'POST':
        distance = request.POST['distance']
        pickup_location = request.POST['pickup_location']
        dropoff_location = request.POST['dropoff_location']

        if distance and pickup_location and dropoff_location:
            BookingUserSide.objects.create(user=request.user.user_profile, distance=distance, pickup_location=pickup_location,dropoff_location=dropoff_location)

        return redirect('home')

    return render(request, 'booking_n_service/book_a_ride.html')

@login_required
def view_booking(request, pk):
    booking = BookingUserSide.objects.get(pk=pk)
    if hasattr(request.user, 'user_profile'):
        joined_share = not Share.objects.filter(user=request.user.user_profile,booking_user_side=booking).exists()
    else:
        joined_share = True
    if booking.distance>10:
        net_fare = booking.distance*75
    else:
        net_fare = booking.distance*80
    if hasattr(request.user, 'drive_profile'):
        shares = Share.objects.filter(booking_user_side=booking)
    else:
        shares = None

    if hasattr(request.user, 'user_profile'):
        profile = 'user_profile'
    else:
        profile = 'driver_profile'

    return render(request, 'booking_n_service/view_booking.html', {'booking': booking, 'net_fare': net_fare, 'shares': shares, "joined_share": joined_share, 'profile': profile})

@login_required
def take_ride(request, pk):
    if hasattr(request.user, 'user_profile'):
        return redirect('home')
    booking = BookingUserSide.objects.get(pk=pk)
    if booking.distance>10:
        net_fare = booking.distance*75
    else:
        net_fare = booking.distance*80
    if request.method == 'POST':
        booking_driver_side = BookingDriverSide.objects.create(driver = request.user.driver_profile, net_fare=net_fare)
        booking.booking_driver_side = booking_driver_side
        booking.save()
        return redirect('home')
    return render(request, 'booking_n_service/take_ride.html', {'booking': booking, 'net_fare': net_fare})



@login_required
def end_ride(request, pk):
    booking = BookingUserSide.objects.get(pk=pk)
    shares = Share.objects.filter(booking_user_side=booking)
    if request.method == 'POST':
        booking.booking_driver_side.ride_status = True
        booking.booking_driver_side.save()
        total_people = 1 + len(shares)
        Payment.objects.create(user=booking.user, booking_user_side = booking, to_pay=booking.booking_driver_side.net_fare/total_people)
        for share in shares:
            Payment.objects.create(user=share.user, booking_user_side=booking, to_pay=booking.booking_driver_side.net_fare / total_people)
        return redirect('home')
    return render(request, 'booking_n_service/finish_ride.html', {'booking': booking})


@login_required
def join_ride(request, pk):
    booking = BookingUserSide.objects.get(pk=pk)

    if request.method == 'POST':
        distance = float(request.POST['distance'])
        if distance > 0 and distance <= booking.distance:
            Share.objects.create(user=request.user.user_profile,booking_user_side=booking, distance=distance)
        return redirect('home')
    return render(request, 'booking_n_service/join_ride.html', {'booking': booking})

@login_required
def view_payment(request):
    payments = Payment.objects.filter(user=request.user.user_profile)
    return render(request, 'booking_n_service/view_payment.html', {'payments': payments})


def pay_payment(request, pk):
    payment = Payment.objects.get(pk=pk)
    payment.status = True
    payment.save()
    payments = Payment.objects.filter(user=request.user.user_profile)
    return render(request, 'booking_n_service/view_payment.html', {'payments': payments})

