from rest_framework.routers import DefaultRouter

from .views import CartViewSet, CartItemViewSet

app_name = "cart"

# basename is required because these viewsets set queryset in get_queryset(),
# not as a class attribute.
router = DefaultRouter()
router.register("carts", CartViewSet, basename="cart")
router.register("cart-items", CartItemViewSet, basename="cart-item")

urlpatterns = router.urls
