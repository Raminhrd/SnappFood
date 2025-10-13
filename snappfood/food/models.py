from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=30)
    parrent = models.ForeignKey(to='self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    name = models.CharField(max_length=30)
    category = models.ManyToManyField(to=Category)
    location = models.OneToOneField(to='users.Location', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=30)
    amount = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    restaurant = models.OneToOneField(to=Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.name