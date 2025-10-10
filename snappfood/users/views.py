from django.shortcuts import render
from django.db.models import Sum
from users.models import *
from users.permissions import IsNotBanUser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from users.serializers import *



def _update_basket_price(basket):
    basket.total_price = 0
    items = BasketItem.objects.filter(basket=basket)
    count = items.count()
    for item in items:
        basket.total_price += (item.quantity * item.product.price)

    discount = 3000 if count > 9 else 0
    basket.final_price = basket.total_price + basket.delivery_price - (basket.discount + discount)
    basket.save()


class AddProductToBasketItem(CreateAPIView):
    permission_classes = [IsAuthenticated, IsNotBanUser]
    serializer_class = BasketItemSerializer
    queryset = BasketItem.objects.all()
    
    def perform_create(self, serializer):
        if not Basket.objects.filter(owner=self.request.user, is_paid=False).exists():
            basket = Basket.objects.create(
                owner=self.request.user,
                total_price = 0,
                final_price = 0,
            )
        else:
            basket = Basket.objects.get(owner=self.request.user, is_paid=False)
        serializer.save(owner=self.request.user, basket=basket)
        _update_basket_price(basket)


class BasketItemList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BasketItemSerializer
    queryset = BasketItem.objects.all()
    
    def get_queryset(self):
        return BasketItem.objects.filter(owner=self.request.user)


class DeleteBasketItem(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BasketItemSerializer
    queryset = BasketItem.objects.all()

    def get_queryset(self):
        return BasketItem.objects.filter(owner=self.request.user)


class SetPaidStatus(APIView):
    permission_classes = [IsAdminUser]
    
    def post(self, request, basket_id):
        basket = Basket.objects.get(id=basket_id)
        basket.is_paid = True
        basket.save()
        return Response("Basket status: PAID!")