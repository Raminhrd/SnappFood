from rest_framework.urls import path
from food.views import *

urlpatterns = [
    path('add-product', AddProductToBasketView.as_view()),
]