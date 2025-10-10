from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class UserProfile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    ban_until = models.DateTimeField(null=True, blank=True)

    @property
    def is_ban(self):
        if self.ban_until is not None and self.ban_until > timezone.now():
            return True
        return False
    

class Location(models.Model):
    destination_lat = models.FloatField(null=True, blank=True)
    destination_long = models.FloatField(null=True, blank=True)
    address = models.TextField(max_length=100)