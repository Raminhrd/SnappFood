from django.db import models
from users.models import Location


class Category(models.Model):
    name = models.CharField(max_length=30)
    parrent = models.ForeignKey(to='self', null=True, blank=True, on_delete=models.CASCADE)


class Restaurant(models.Model):
    name = models.CharField(max_length=30)
    category = models.ManyToManyField(to=Category)
    location = models.OneToOneField(to=Location, on_delete=models.CASCADE)