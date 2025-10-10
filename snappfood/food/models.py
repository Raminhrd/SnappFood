from django.db import models
from users.models import Location


class Category(models.Model):
    name = models.CharField(max_length=30)
    parrent = models.ForeignKey(to='self', null=True, blank=True, on_delete=models.CASCADE)


class Restaurant(models.Model):
    name = models.CharField(max_length=30)
    category = models.ManyToManyField(to=Category)
    location = models.OneToOneField(to=Location, on_delete=models.CASCADE)


class Product(models.Model):
    name = models.CharField(max_length=30)
    amount = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    restaurant = models.OneToOneField(to=Restaurant, on_delete=models.CASCADE)