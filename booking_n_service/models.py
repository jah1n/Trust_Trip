from django.db import models
from core.models import UserProfile, Driver
from django.db.models.functions import datetime


class BookingDriverSide(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    ride_status = models.BooleanField(default=False)
    net_fare = models.FloatField(default=0)

    def __str__(self):
        return str(self.id)+" "+self.driver.user.username+" "+str(self.ride_status)

class BookingUserSide(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    booking_driver_side = models.ForeignKey(BookingDriverSide, on_delete=models.CASCADE, default=None, null=True)
    distance =models.FloatField(default=0)
    pickup_location = models.CharField(max_length=64, blank=True)
    dropoff_location = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return str(self.id)+" "+self.pickup_location+" "+self.dropoff_location

class Share(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    booking_user_side = models.ForeignKey(BookingUserSide, on_delete=models.CASCADE, default=None, null=True)
    distance = models.FloatField(default=0)

class Payment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    booking_user_side = models.ForeignKey(BookingUserSide, on_delete=models.CASCADE, default=None, null=True)
    to_pay = models.FloatField()
    status = models.BooleanField(default=False)
    date = models.DateField(default=datetime.datetime.now())

    def __str__(self):
        return str(self.id)


