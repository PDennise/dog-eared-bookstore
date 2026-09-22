from rest_framework import viewsets

from .models import Book, Category
from .serializers import BookSerializer, CategorySerializer
from django.shortcuts import render


class CategoryViewSet(viewsets.ModelViewSet):
    """Provide the standard CRUD API actions for categories."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BookViewSet(viewsets.ModelViewSet):
    """Provide the standard CRUD API actions for books."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer


def book_list(request):
    books = Book.objects.filter(is_active=True).select_related("category")

    return render(
        request,
        "books.html",
        {"books": books},
    )