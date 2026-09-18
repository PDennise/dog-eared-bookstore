from django.conf import settings
from django.db import models

from products.models import Book


class Cart(models.Model):
    """ One cart per user. null=True allows a guest cart later if you want it."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return f"Cart for {self.user}"
        return f"Cart #{self.pk}"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="cart_items",
    )
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """ Same book can't appear twice in one cart; change quantity instead."""
        
        unique_together = ("cart", "book")

    def __str__(self):
        return f"{self.quantity} x {self.book.name}"
