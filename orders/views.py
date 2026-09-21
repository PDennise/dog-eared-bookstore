from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem

from .serializers import OrderSerializer, OrderItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    """Provide order API actions for the logged-in user."""

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Each user only sees their own order.
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Attach the order to the current user automatically.
        serializer.save(user=self.request.user)


class OrderItemViewSet(viewsets.ModelViewSet):
    """Provide CRUD API actions for items in the user's order."""

    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only items belonging to the current user's orders."""
        return OrderItem.objects.filter(order__user=self.request.user)    
