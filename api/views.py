from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny
from .models import (
    User, House, Vendor, VehiclePass, Alert,
    CCTVRequest, MonthlyDue, Payment, Complaint
)
from .serializers import (
    UserSerializer, HouseSerializer, VendorSerializer, VehiclePassSerializer,
    AlertSerializer, CCTVRequestSerializer, MonthlyDueSerializer,
    PaymentSerializer, ComplaintSerializer, CustomTokenObtainPairSerializer, RegisterSerializer
)
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class HouseViewSet(viewsets.ModelViewSet):
    queryset = House.objects.all()
    serializer_class = HouseSerializer


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]


class VehiclePassViewSet(viewsets.ModelViewSet):
    queryset = VehiclePass.objects.all()
    serializer_class = VehiclePassSerializer
    permission_classes = [IsAuthenticated]


class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]


class CCTVRequestViewSet(viewsets.ModelViewSet):
    queryset = CCTVRequest.objects.all()
    serializer_class = CCTVRequestSerializer
    permission_classes = [IsAuthenticated]


class MonthlyDueViewSet(viewsets.ModelViewSet):
    queryset = MonthlyDue.objects.all()
    serializer_class = MonthlyDueSerializer
    permission_classes = [IsAuthenticated]


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]


class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
    permission_classes = [IsAuthenticated]
