from rest_framework.routers import DefaultRouter

from .views import BookViewSet, CategoryViewSet

app_name = "products"

# The router creates the standard list and detail routes for each ViewSet.
router = DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("books", BookViewSet)

urlpatterns = router.urls
