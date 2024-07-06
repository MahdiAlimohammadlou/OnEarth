from rest_framework import serializers
from .models import User, AgentInfo, BuyerPersonalInfo, SellerPersonalInfo, Ticket, Device
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

class CreateOrUpdateAgentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentInfo
        fields = [
            'id', 'full_name', 'company_name', 'company_address', 
            'company_email', 'company_phone_number', 'biometric', 
            'id_card_or_passport', 'birth_certificate', 'aggrement',
            'business_card'
        ]

    def update(self, instance, validated_data):
        if instance.approval_status == "Approved":
            raise ValidationError('Cannot update approved information.')
        return super().update(instance, validated_data)

class AgentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentInfo
        fields = [
            'id', 'full_name', 'company_name', 'company_address', 
            'company_email', 'company_phone_number', 'biometric', 
            'id_card_or_passport', 'birth_certificate', 'aggrement',
            'biometric_approval_status', 'approval_status',
            'birth_certificate_approval_status', 'aggrement_approval_status',
            'id_card_or_passport_approval_status', 'business_card'
        ]

class CreateOrUpdateBuyerPersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerPersonalInfo
        fields = [
            'id', 'full_name', 'postal_address', 'marital_status',
            'marriage_contract', 'biometric', 'id_or_driver_license', 
            'passport', 'birth_certificate', 'aggrement', 'elec_bill'
        ]

    def update(self, instance, validated_data):
        if instance.basic_info_approval_status == "Approved":
            raise ValidationError('Cannot update approved information.')
        return super().update(instance, validated_data)

class BuyerPersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerPersonalInfo
        fields = [
            'id', 'full_name', 'postal_address', 'marital_status',
            'marriage_contract', 'biometric', 'id_or_driver_license', 
            'passport', 'birth_certificate', 'aggrement',
            'basic_info_approval_status', 'id_or_driver_license_approval_status',
            'passport_approval_status', 'biometric_approval_status',
            'birth_certificate_status', 'aggrement_approval_status', 'elec_bill'
        ]

class CreateOrUpdateSellerPersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerPersonalInfo
        fields = [
            'id', 'full_name', 'postal_address', 'marital_status',
            'marriage_contract', 'biometric', 'id_or_driver_license', 
            'passport', 'birth_certificate', 'background', 'aggrement',
            'elec_bill'
        ]

    def update(self, instance, validated_data):
        if instance.basic_info_approval_status == "Approved":
            raise ValidationError('Cannot update approved information.')
        return super().update(instance, validated_data)

class SellerPersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerPersonalInfo
        fields = [
            'id', 'full_name', 'postal_address', 'marital_status',
            'marriage_contract', 'biometric', 'id_or_driver_license', 
            'passport', 'birth_certificate', 'background', 'aggrement',
            'basic_info_approval_status', 'id_or_driver_license_approval_status',
            'passport_approval_status', 'biometric_approval_status',
            'birth_certificate_status', 'background_status', 'aggrement_approval_status',
            'elec_bill'
        ]


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'subject', 'description', 'status', 'department', 'created_at', 'updated_at']
        read_only_fields = ['status', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'device_info', 'created_at']