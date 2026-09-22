from django.contrib import admin
from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Customize the Django admin interface for orders."""

    list_display = ("id", "user", "status", "total_price", "created_at", "updated_at")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Customize the Django admin interface for order items."""

    list_display = ("order", "book", "quantity", "price")
