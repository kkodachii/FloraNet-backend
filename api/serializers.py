from rest_framework import serializers
from .models import (
    User, House, Vendor, VehiclePass, Alert,
    CCTVRequest, MonthlyDue, Payment, Complaint
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'name', 'contact_no', 'resident_id', 'house', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create(
            email=validated_data['email'],
            name=validated_data['name'],
            contact_no=validated_data['contact_no'],
            resident_id=validated_data['resident_id'],
            house=validated_data['house'],
            username=validated_data['email']  # Required for AbstractUser
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.name
        token['resident_id'] = user.resident_id
        token['email'] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['name'] = self.user.name
        data['resident_id'] = self.user.resident_id
        data['email'] = self.user.email
        return data

# Extend AbstractUser – include password handling properly
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'contact_no', 'house', 'resident_id', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ['id', 'house_number', 'block_lot', 'street']


class VendorSerializer(serializers.ModelSerializer):
    resident = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Vendor
        fields = ['id', 'resident', 'business_name']


class VehiclePassSerializer(serializers.ModelSerializer):
    resident = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = VehiclePass
        fields = [
            'id', 'resident', 'vehicle_pass_id', 'amount', 'mode_of_payment',
            'vehicle_model', 'plate_number'
        ]


class AlertSerializer(serializers.ModelSerializer):
    resident = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Alert
        fields = ['id', 'resident', 'reported_at', 'reason', 'status', 'notified_party']


class CCTVRequestSerializer(serializers.ModelSerializer):
    resident = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = CCTVRequest
        fields = ['id', 'resident', 'requested_at', 'reason', 'status', 'notified_party']


class MonthlyDueSerializer(serializers.ModelSerializer):
    house = serializers.PrimaryKeyRelatedField(queryset=House.objects.all())
    resident = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = MonthlyDue
        fields = ['id', 'house', 'resident', 'due_month', 'amount', 'is_paid', 'paid_at']


class PaymentSerializer(serializers.ModelSerializer):
    resident = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Payment
        fields = ['id', 'resident', 'method_of_payment', 'amount', 'paid_at']


class ComplaintSerializer(serializers.ModelSerializer):
    resident = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Complaint
        fields = [
            'id', 'resident', 'complaint_type', 'complained_at',
            'service_type', 'trigger_type', 'status', 'remarks'
        ]
