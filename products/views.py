from rest_framework import viewsets

from .models import Book, Category
from .serializers import BookSerializer, CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """Provide the standard CRUD API actions for categories."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BookViewSet(viewsets.ModelViewSet):
    """Provide the standard CRUD API actions for books."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer
