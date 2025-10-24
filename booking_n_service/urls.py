from django.urls import path
from . import views

app_name = 'booking_n_service'

urlpatterns = [
    path("book_a_ride/", views.book_a_ride, name="book_a_ride"),
    path("booking/<str:pk>", views.view_booking, name="view_booking"),
    path("take_ride/<str:pk>", views.take_ride, name="take_ride"),
    path("end_ride/<str:pk>", views.end_ride, name="end_ride"),
    path("join_ride/<str:pk>", views.join_ride, name="join_ride"),
    path("view_payment", views.view_payment, name="view_payment"),
    path("pay_payment/<str:pk>",views.pay_payment, name="pay_payment"),
]