from rest_framework import serializers
from products.serializers import BookSerializer
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    """Convert CartItem objects to and from API-friendly data."""

    # Nested book details when reading; write with book id only.
    book_detail = BookSerializer(source="book", read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "book", "book_detail", "quantity", "added_at"]
        read_only_fields = ["id", "added_at"]


class CartSerializer(serializers.ModelSerializer):
    """Convert Cart objects to and from API-friendly data."""

    # Include all items inside the cart response.
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()


    class Meta:
        model = Cart
        fields = ["id", "user", "items", "total", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "total", "created_at", "updated_at"]

    def get_total(self, obj):
        return sum(
            item.book.price * item.quantity
            for item in obj.items.all()
        )
