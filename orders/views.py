from django.db import transaction

from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated

from cart.models import Cart

from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """Provide order API actions for the logged-in user."""

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Each user only sees their own orders.
        return Order.objects.filter(user=self.request.user)

    @transaction.atomic
    def perform_create(self, serializer):
        # Get the user's cart.
        cart = Cart.objects.filter(user=self.request.user).first()

        if not cart:
            raise serializers.ValidationError(
                {"detail": "Your cart is empty."}
            )

        # Get the books and quantities from the cart.
        cart_items = list(
            cart.items.select_related("book").all()
        )

        if not cart_items:
            raise serializers.ValidationError(
                {"detail": "Your cart is empty."}
            )

        # Validate every cart item before creating the order.
        for item in cart_items:
            if not item.book.is_active:
                raise serializers.ValidationError(
                    {
                        "detail": (
                            f"{item.book.name} is no longer available."
                        )
                    }
                )

            if item.quantity > item.book.stock:
                raise serializers.ValidationError(
                    {
                        "detail": (
                            f"Not enough stock for {item.book.name}."
                        )
                    }
                )

        # Attach the order to the current user automatically.
        # Create the order first.
        order = serializer.save(
            user=self.request.user,
            total_price=0,
        )

        total_price = 0

        # Convert each cart item into an order item.
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price,
            )

            total_price += item.book.price * item.quantity

            # Reduce the book stock after the order item is created.
            item.book.stock -= item.quantity
            item.book.save(update_fields=["stock"])

        # Save the final order total.
        order.total_price = total_price
        order.save(update_fields=["total_price", "updated_at"])

        # Clear the cart after creating the order.
        cart.items.all().delete()


class OrderItemViewSet(viewsets.ModelViewSet):
    """Provide CRUD API actions for items in the user's order."""

    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only items belonging to the current user's orders."""
        return OrderItem.objects.filter(
            order__user=self.request.user
        )
