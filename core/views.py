from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import UserForm
from .models import UserProfile, Driver


def reg_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        # check if username exists
        if User.objects.filter(username=username).exists():
            return redirect('home')

        # create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_staff = False  # Cannot access admin
        user.is_superuser = False  # Definitely not admin
        user.save()
        userProfile = UserProfile.objects.create(user=user)
        userProfile.save()
        login(request, user)
        return redirect('home')

    return render(request, 'core/reg_user.html')


def login_user(request, type):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST' and type == 'user':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None and hasattr(user, 'user_profile'):
            login(request, user)
            return redirect('home')

    return render(request, 'core/login_user.html', {'type': type})

def login_driver(request, type):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST' and type == 'driver':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None and hasattr(user, 'driver_profile'):
            login(request, user)
            return redirect('home')

    return render(request, 'core/login_driver.html', {'type': type})

@login_required
def logout_user(request):
    logout(request)
    return redirect('home')

@login_required
def user_profile(request):
    user = request.user
    if hasattr(user, 'driver_profile'):
        return redirect("home")
    elif hasattr(user, 'user_profile'):
        profile = user.user_profile

    return render(request, 'core/user_profile.html', {'profile': profile})

@login_required
def driver_profile(request):
    user = request.user
    if hasattr(user, 'driver_profile'):
        driver = user.driver_profile
    elif hasattr(user, 'user_profile'):
        return redirect("home")

    return render(request, 'core/driver_profile.html', {'driver': driver})


@login_required
def update_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        gender = request.POST.get('gender')
        smoking_status = request.POST.get('smoking_status')
        dob = request.POST.get('dob')

        if username:
            request.user.username = username
        if email:
            request.user.email = email
        if phone_number:
            request.user.user_profile.phone_number = phone_number
        if gender:
            request.user.user_profile.gender = gender
        if smoking_status:
            request.user.user_profile.smoking_status = smoking_status
        if dob:
            request.user.user_profile.birth_date = dob
        request.user.user_profile.save()
        request.user.save()
        return redirect('core:user_profile')
    return render(request, 'core/update_user.html')

@login_required
def update_driver(request):
    if hasattr(request.user, 'driver_profile'):
        driver = request.user.driver_profile
    if request.method == 'POST':
        username = request.POST.get('username', driver.user.username)
        email = request.POST.get('email', driver.user.email)

        license_number = request.POST.get('license_number', driver.license_number)
        vehicle_brand = request.POST.get('vehicle_brand', driver.vehicle_brand)
        vehicle_model = request.POST.get('vehicle_model', driver.vehicle_model)
        vehicle_plate = request.POST.get('vehicle_plate', driver.vehicle_plate)
        availability_status = request.POST.get('availability_status') == 'True'

        if 'picture' in request.FILES:
            driver.picture = request.FILES['picture']

        if username:
            request.user.username = username
        if email:
            request.user.email = email
        if license_number:
            driver.license_number = license_number
        if vehicle_brand:
            driver.vehicle_brand = vehicle_brand
        if vehicle_model:
            driver.vehicle_model = vehicle_model
        if vehicle_plate:
            driver.vehicle_plate = vehicle_plate
        if availability_status:
            driver.availability_status = availability_status

        request.user.save()
        driver.save()
        return redirect('core:driver_profile')
    return render(request, 'core/update_driver.html', {'driver': driver})



@login_required
def update_user_profile_picture(request):
    profile = request.user.user_profile
    if request.method == 'POST':
        picture = request.FILES.get('picture')
        if picture:
            request.user.user_profile.picture = picture
            request.user.user_profile.save()
            request.user.save()
            return redirect('core:user_profile')
    return render(request, 'core/update_user_profile_pic.html', {'profile': profile})

@login_required
def delete_user(request):
    if hasattr(request.user, 'driver_profile'):
        return redirect('home')
    if request.method == 'POST':
        password = request.POST.get('password')

        if request.user.check_password(password):
            user = request.user
            logout(request)
            user.delete()
            return redirect('home')
    return render(request, 'core/delete_user.html')

@login_required
def delete_driver(request):
    if hasattr(request.user, 'user_profile'):
        return redirect('home')
    if request.method == 'POST':
        password = request.POST.get('password')

        if request.user.check_password(password):
            user = request.user
            logout(request)
            user.delete()
            return redirect('home')
    return render(request, 'core/delete_driver.html')

def register_driver(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        license_number = request.POST.get('l_num')
        vehicle_brand = request.POST.get('vehicle_brand')
        vehicle_model = request.POST.get('vehicle_model')
        vehicle_plate = request.POST.get('vehicle_plate')
        # check if username exists
        if User.objects.filter(username=username).exists():
            return redirect('core:register_driver')
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_staff = False  # Cannot access admin
        user.is_superuser = False  # Definitely not admin
        user.save()
        driver_profile = Driver.objects.create(user=user, license_number=license_number, vehicle_brand=vehicle_brand, vehicle_model=vehicle_model, vehicle_plate=vehicle_plate)
        driver_profile.save()
        return redirect('home')
    return render(request, 'core/reg_driver.html')