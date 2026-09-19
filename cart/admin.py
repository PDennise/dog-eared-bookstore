from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    """Show cart items on the cart page itself."""

    model = CartItem
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Customize the Django admin interface for carts."""

    list_display = ("id", "user", "created_at", "updated_at")
    list_filter = ("created_at",)
    search_fields = ("user__username",)
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Customize the Django admin interface for cart items."""

    list_display = ("id", "cart", "book", "quantity", "added_at")
    list_filter = ("added_at",)
    search_fields = ("book__name",)
