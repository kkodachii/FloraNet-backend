from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, HouseViewSet, VendorViewSet, VehiclePassViewSet,
    AlertViewSet, CCTVRequestViewSet, MonthlyDueViewSet,
    PaymentViewSet, ComplaintViewSet, RegisterView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'houses', HouseViewSet)
router.register(r'vendors', VendorViewSet)
router.register(r'vehicle-passes', VehiclePassViewSet)
router.register(r'alerts', AlertViewSet)
router.register(r'cctv-requests', CCTVRequestViewSet)
router.register(r'monthly-dues', MonthlyDueViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'complaints', ComplaintViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
]
