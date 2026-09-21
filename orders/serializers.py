from rest_framework import serializers
from .models import Order, OrderItem


class OrderSerializer(serializers.ModelSerializer):
    """Convert Order objects to and from API-friendly data."""

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "status",
            "total_price",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "status",
            "total_price",
            "created_at",
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    """Convert OrderItem objects to and from API-friendly data."""

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "order",
            "book",
            "quantity",
            "price",
        ]
        read_only_fields = ["id", "order", "price"]
