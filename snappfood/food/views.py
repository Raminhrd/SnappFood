from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from users.permissions import IsNotBanUser
from users.models import Basket, BasketItem
from .models import Product, Restaurant


class AddProductToBasketView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsNotBanUser]

    def post(self, request):
        product_id = request.data.get("product_id")
        restaurant_id = request.data.get("restaurant_id")
        quantity = request.data.get("quantity")

        if product_id is None or restaurant_id is None or quantity is None:
            return Response({"error": "product_id, restaurant_id, quantity لازم است."},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            return Response({"error": "quantity باید عدد صحیح مثبت باشد."},
                            status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, pk=product_id)
        restaurant = get_object_or_404(Restaurant, pk=restaurant_id)

        if product.restaurant_id != restaurant.id:
            return Response({"error": "این محصول متعلق به رستوران انتخاب‌شده نیست."},
                            status=status.HTTP_400_BAD_REQUEST)

        if product.amount < quantity:
            return Response({"error": "موجودی کافی نیست."},
                            status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        with transaction.atomic():
            basket, _ = Basket.objects.get_or_create(
                owner=user,
                is_paid=False,
                defaults={"total_price": 0, "delivery_price": 0, "discount": 0}
            )

            first_item = BasketItem.objects.filter(basket=basket).select_related("product").first()
            if first_item and first_item.product.restaurant_id != restaurant.id:
                return Response(
                    {"error": "سبد باز شما مربوط به رستوران دیگری است. ابتدا تسویه یا خالی کنید."},
                    status=status.HTTP_409_CONFLICT
                )

            item, _created = BasketItem.objects.get_or_create(
                owner=user,
                basket=basket,
                product=product,
                defaults={"quantity": 0}
            )
            item.quantity += quantity
            item.save()

            product.amount -= quantity
            product.save()

            items = BasketItem.objects.filter(basket=basket).select_related("product")
            total_price = sum(i.quantity * i.product.price for i in items)
            count = items.count()
            extra_discount = 3000 if count > 9 else 0

            basket.total_price = total_price
            final_price = total_price + basket.delivery_price - (basket.discount + extra_discount)
            basket.save()

        return Response({
            "message": "غذا به سبد اضافه شد.",
            "basket_id": basket.id,
            "restaurant": restaurant.name,
            "product": product.name,
            "quantity": item.quantity,
            "total_price": total_price,
            "final_price": final_price
        }, status=status.HTTP_201_CREATED)