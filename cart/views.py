from rest_framework import serializers, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


class CartViewSet(viewsets.ReadOnlyModelViewSet):
    """Provide read-only cart API actions for the logged-in user."""

    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Each user only sees their own cart.
        return Cart.objects.filter(user=self.request.user)

class CartItemViewSet(viewsets.ModelViewSet):
    """Provide CRUD API actions for items in the user's cart."""

    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only items that belong to the current user's cart.
        return CartItem.objects.filter(cart__user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        book = serializer.validated_data["book"]
        quantity = serializer.validated_data["quantity"]

        if not book.is_active:
            raise serializers.ValidationError(
                "This book is not available."
            )

        cart, _ = Cart.objects.get_or_create(user=request.user)

        cart_item = CartItem.objects.filter(
            cart=cart,
            book=book,
        ).first()

        if cart_item:
            # Calculate the total quantity after adding the requested amount.
            new_quantity = cart_item.quantity + quantity

        else:
            # For a new cart item, the requested quantity is the total quantity.
            new_quantity = quantity

        if new_quantity > book.stock:
            raise serializers.ValidationError(
                "Requested quantity exceeds available stock."
            )

        if cart_item:
            # Increase the existing quantity.
            cart_item.quantity = new_quantity
            cart_item.save(update_fields=["quantity"])

            serializer.instance = cart_item

        else:
            # Create a new cart item.
            serializer.save(cart=cart)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )