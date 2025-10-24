from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    gender_options = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
        ("unspecified", "Unspecified"),
    ]

    smoking_status_options = [
        ("allowed", "Allowed"),
        ("not_allowed", "Not Allowed"),
        ("unspecified", "Unspecified"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )
    picture = models.ImageField(null=True, blank=True, default=None)
    gender = models.CharField(max_length=12, choices=gender_options, default="Unspecified", blank=True)
    birth_date = models.DateField(null=True, blank=True)
    smoking_status = models.CharField(max_length=20, choices=smoking_status_options, default="Unspecified", blank=True)
    is_verified = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.gender})"


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="driver_profile")
    picture = models.ImageField(null=True, blank=True, default=None)
    license_number = models.CharField(max_length=64, blank=True)
    vehicle_brand = models.CharField(max_length=64, blank=True)
    vehicle_model = models.CharField(max_length=64, blank=True)
    vehicle_plate = models.CharField(max_length=32, blank=True)
    availability_status = models.BooleanField(default=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.vehicle_plate}"
