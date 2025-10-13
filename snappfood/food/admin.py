from django.contrib import admin
from food.models import *
from users.models import *


admin.site.register(Category)
admin.site.register(Restaurant)
admin.site.register(Product)
admin.site.register(UserProfile)
admin.site.register(Location)
admin.site.register(BasketItem)
admin.site.register(Basket)