from rest_framework import serializers
from .models import User, AgentInfo, BuyerPersonalInfo, SellerPersonalInfo, Ticket
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone_number', 'is_admin', 'is_seller', 'is_buyer', 'is_agent', 'is_guest', 'is_phone_verified']

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'is_admin', 'is_seller', 'is_buyer', 'is_agent', 'is_guest']

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        
        return value

class AgentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentInfo
        fields = [
            'id', 'company_name', 'company_address', 
            'company_email', 'company_phone_number', 'biometric', 
            'business_card', 'id_card',
        ]

class BuyerPersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerPersonalInfo
        fields = [
            'id', 'biometric', 'full_name', 'postal_address',
            'marital_status', 'marriage_contract', 'elec_bill',
            'birth_certificate', 'id_or_driver_license', 'buyer_agreement',
        ]

class SellerPersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerPersonalInfo
        fields = [
            'id', 'biometric', 'full_name', 'postal_address',
            'marital_status', 'marriage_contract', 'elec_bill',
            'birth_certificate', 'id_or_driver_license',
            'passport', 'seller_agreement'
        ]

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'subject', 'description', 'status', 'department', 'created_at', 'updated_at']
        read_only_fields = ['status', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
