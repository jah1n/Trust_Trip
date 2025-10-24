from django.urls import path
from . import views

app_name = 'support_n_notification'

urlpatterns = [
    path('give_review/<str:pk>', views.give_review, name='give_review'),
    path('view_review/', views.view_review, name='view_review'),
]