from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from food.models import Product



class UserProfile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    ban_until = models.DateTimeField(null=True, blank=True)
    location = models.OneToOneField(to='Location', on_delete=models.CASCADE, null=True, blank=True)

    @property
    def is_ban(self):
        if self.ban_until is not None and self.ban_until > timezone.now():
            return True
        return False
    
    def __str__(self):
        return self.user.username
    
    #def save(self, *args, **kwargs):

       #if self.location_id is None:
       #    raise ValueError("Location cannot be empty for UserProfile")
       #if self.location.lat is None or self.location.long is None:
       #    raise ValueError("Latitude and Longitude cannot be null")
       #super().save(*args, **kwargs)
    

class Location(models.Model):
    lat = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)
    address = models.TextField(max_length=100)


class Basket(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.PositiveBigIntegerField()
    delivery_price = models.PositiveBigIntegerField(default=0)
    discount = models.PositiveBigIntegerField(default=0)
    is_paid = models.BooleanField(default=False)
    destination_lat = models.FloatField(null=True, blank=True)
    destination_long = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def final_price(self):
        return self.total_price - self.discount


class BasketItem(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)