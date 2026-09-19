from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


class CartViewSet(viewsets.ModelViewSet):
    """Provide cart API actions for the logged-in user."""

    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Each user only sees their own cart.
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Attach the cart to the current user automatically.
        serializer.save(user=self.request.user)


class CartItemViewSet(viewsets.ModelViewSet):
    """Provide CRUD API actions for items in the user's cart."""

    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only items that belong to the current user's cart.
        return CartItem.objects.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        # Get or create the user's cart, then add the item to it.
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)
