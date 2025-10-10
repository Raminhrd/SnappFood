from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class UserProfile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    ban_until = models.DateTimeField(null=True, blank=True)
    location = models.OneToOneField(to='Location', on_delete=models.CASCADE)

    @property
    def is_ban(self):
        if self.ban_until is not None and self.ban_until > timezone.now():
            return True
        return False
    
    def save(self, *args, **kwargs):
        if self.location is None:
            raise ValueError("Location cannot be empty for UserProfile")
        if self.location.lat is None or self.location.long is None:
            raise ValueError("Latitude and Longitude cannot be null")
        super().save(*args, **kwargs)
    

class Location(models.Model):
    lat = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)
    address = models.TextField(max_length=100)