from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderItemViewSet

app_name = "orders"

# The router creates the standard list and detail routes for each ViewSet.
# basename is required because these viewsets set queryset in get_queryset(),
# not as a class attribute.

router = DefaultRouter()
router.register("orders", OrderViewSet, basename="order")
router.register("order-items", OrderItemViewSet, basename="order-item")

urlpatterns = router.urls
