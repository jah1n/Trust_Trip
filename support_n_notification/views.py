from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from booking_n_service.models import BookingUserSide
from .models import Review
from django.contrib import messages
from django.shortcuts import redirect

@login_required
def give_review(request, pk):
    booking = BookingUserSide.objects.get(pk=pk)
    if request.method == "POST":
        review = request.POST.get("review")
        Review.objects.create(booking=booking,user=booking.user, driver=booking.booking_driver_side.driver, review=review)
        return redirect("booking_n_service:view_payment")
    return render(request, 'support_n_notification/give_review.html')

def view_review(request):
    if hasattr(request.user, 'driver_profile'):
        reviews = Review.objects.filter(driver=request.user.driver_profile)
    else:
        reviews = Review.objects.filter(user=request.user.user_profile)

    return render(request, 'support_n_notification/view_review.html', {'reviews': reviews})
def no_reviews(request):
    messages.info(request, "No existing reviews")
    return redirect('support_n_notification:view_review')