from django.db import models
from core.models import UserProfile, Driver
from booking_n_service.models import BookingUserSide
from django.db.models.functions import datetime


class Review(models.Model):
    booking = models.ForeignKey(BookingUserSide, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    review = models.TextField()
    date = models.DateField(default=datetime.datetime.now())

    def __str__(self):
        if len(str(self.review))>20:
            return str(self.id)+" "+self.review[0:20]+"..."
        return str(self.id)+" "+self.review
