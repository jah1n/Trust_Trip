from django.urls import path
from .views import reg_user, login_user, logout_user, user_profile, update_user, update_user_profile_picture, delete_user, register_driver, login_driver, driver_profile, update_driver, delete_driver

app_name = 'core'

urlpatterns = [
    path('register_user/', reg_user, name='reg_user'),
    path('login_user/<str:type>', login_user, name='login_user'),
    path('login_driver/<str:type>', login_driver, name='login_driver'),
    path('logout_user', logout_user, name='logout_user'),
    path('user_profile', user_profile, name='user_profile'),
    path('driver_profile', driver_profile, name='driver_profile'),
    path('update_user',update_user, name='update_user'),
    path('update_driver',update_driver, name='update_driver'),
    path('picture_user/',update_user_profile_picture, name='update_user_profile_picture'),
    path('delete_user',delete_user, name='delete_user'),
    path('delete_driver',delete_driver, name='delete_driver'),
    path('register_driver/', register_driver, name='register_driver'),
]