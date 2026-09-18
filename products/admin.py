from django.contrib import admin
from .models import Book, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Customize the Django admin interface for categories."""

    list_display = ("name", "slug", "created_at")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Customize the Django admin interface for books."""

    list_display = ("name", "author", "category", "price", "stock", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name", "author", "isbn")
    prepopulated_fields = {"slug": ("name",)}
