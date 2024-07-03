from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from django.utils import timezone
from datetime import timedelta
from core.models import AbstractBaseModel, AbstractBaseInfoModel
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from django.conf import settings
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(blank=True, max_length=17, null=True, unique=True)
    is_admin = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)
    is_agent = models.BooleanField(default=False)
    is_guest = models.BooleanField(default=True)
    otp_code = models.CharField(blank=True, max_length=6, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    is_phone_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["phone_number"]

    def has_perm(self, perm, obj = None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
    
    @property
    def is_otp_expired(self):
        if self.otp_created_at is None:
            return False
        return timezone.now() > self.otp_created_at + timedelta(minutes=2)

    def __str__(self):
        return self.email

class CommonFields(AbstractBaseInfoModel):
    STATUS_CHOICES = [
        ('New', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    full_name = models.CharField(max_length=100, null=True, blank=True)
    postal_address = models.TextField(null=True, blank=True)
    marital_status = models.CharField(choices=[('single', 'Single'), ('married', 'Married')], max_length=20, null=True, blank=True)
    marriage_contract = models.ImageField(blank=True, null=True, upload_to='marriage_contract_images/')
    basic_info_approval_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New', verbose_name='Basic information approval Status')
    elec_bill = models.ImageField(upload_to='elec_bill_images/', null=True, blank=True)
    elec_bill_approval_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New', verbose_name='Elec bill approval Status')
    birth_certificate = models.ImageField(upload_to='birth_certificate_images/', null=True, blank=True)
    birth_certificate_approval_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New', verbose_name='Birth certificate approval Status')
    id_or_driver_license = models.ImageField(upload_to='id_or_driver_license_images/', null=True, blank=True)
    id_or_driver_license_approval_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New', verbose_name='ID or driver license approval Status')
    approval_status = models.BooleanField(default=False)
    
    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.full_name

class AgentInfo(AbstractBaseInfoModel):
    STATUS_CHOICES = [
        ('New', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    company_name = models.CharField(max_length=255, null=True, blank=True)
    company_address = models.CharField(max_length=255, null=True, blank=True)
    company_email = models.EmailField(max_length=255, null=True, blank=True)
    company_phone_number = models.CharField(max_length=11, null=True, blank=True)
    basic_info_approval_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New', verbose_name='Basic information approval Status')
    business_card = models.ImageField(upload_to='business_card_images/', null=True, blank=True)
    business_card_approval_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New', verbose_name='Business card approval Status')
    id_card = models.ImageField(upload_to='id_card_images/', null=True, blank=True)
    id_card_approval_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New', verbose_name='ID card approval Status')
    agent_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agent_info')
    approval_status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.company_name

class BuyerPersonalInfo(CommonFields):
    buyer_agreement = models.ImageField(upload_to='buyer_aggrement_images/', null=True, blank=True)
    buyer_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer_personal_info')

class SellerPersonalInfo(CommonFields):
    seller_agreement = models.ImageField(upload_to='seller_aggrement_images/', null=True, blank=True)
    seller_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_personal_info')

class Ticket(AbstractBaseModel):
    SUBJECT_CHOICES = [
        ('Technical', 'Technical Issue'),
        ('Billing', 'Billing Inquiry'),
        ('General', 'General Support'),
    ]
    
    STATUS_CHOICES = [
        ('New', 'New'),
        ('InProgress', 'In Progress'),
        ('Closed', 'Closed'),
    ]

    DEPARTMENT_CHOICES = [
        ('IT', 'IT Department'),
        ('HR', 'Human Resources'),
        ('Finance', 'Finance Department'),
        ('Support', 'Customer Support'),
    ]

    user = models.ForeignKey(User, related_name='submitted_tickets', on_delete=models.CASCADE, verbose_name='User Who Submitted')
    assigned_user = models.ForeignKey(User, related_name='assigned_tickets', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Assigned User')
    subject = models.CharField(max_length=100, choices=SUBJECT_CHOICES, verbose_name='Subject')
    description = models.TextField(verbose_name='Description')
    response = models.TextField(blank=True, null=True, verbose_name='Response')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New', verbose_name='Ticket Status')
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, verbose_name='Department')

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'

    def __str__(self):
        return f"{self.subject} - {self.user.email}"

class ReferralCode(AbstractBaseModel):
    code = models.CharField(max_length=50, unique=True)
    agent = models.OneToOneField(User, related_name='referral', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.code} - {self.agent.email}"

class Device(AbstractBaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='devices')
    device_info = models.CharField(max_length=255, default="Unknown Device")
    refresh_token = models.TextField()

    def __str__(self):
        return f"{self.user.email} - {self.device_info}"

    def blacklist_tokens(self):
        try:
            token = self.refresh_token
            refresh_token = RefreshToken(token)
            refresh_token.blacklist()
            return Response({"message": "Token has been blacklisted."})
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        
    def is_token_expired(self):
        try:
            token = self.refresh_token
            refresh_token = RefreshToken(token)
            return False
        except Exception:
            return True