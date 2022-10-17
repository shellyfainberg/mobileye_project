from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime    

class Vehicle(models.Model):
    license_plate_number = models.CharField(max_length=200)
    manufacturer = models.CharField(max_length=200)
    is_available = models.BooleanField(default=True)
    owner = models.OneToOneField(User, models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"""{self.manufacturer} - {self.license_plate_number} - available: {str(self.is_available)} - owner: {str(self.owner)}"""

class HistoryTask(models.Model):
    user =  models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
    date = models.DateTimeField(default=datetime.now, blank=True)
    vehicle = models.ForeignKey(Vehicle, null=False, on_delete=models.CASCADE)
    action = models.CharField(max_length=200)

    def __str__(self):
        # return f"""{self.manufacturer} -  - available: {str(self.is_available)} - owner: {str(self.owner)}"""
        return f"""User - {str(self.user)} Date - {str(self.date)} Vehicle - {self.vehicle} Action -{self.action}"""
