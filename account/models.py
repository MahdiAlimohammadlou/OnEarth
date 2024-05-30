from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from django.utils import timezone
from datetime import timedelta
from core.models import AbstractBaseModel

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

class CommonFields(AbstractBaseModel):
    biometric = models.ImageField(upload_to='biometric_images/', null=True, unique=True)
    full_name = models.CharField(max_length=100, null=True, unique=True)
    postal_address = models.TextField(null=True, unique=True)
    marital_status = models.CharField(choices=[('single', 'Single'), ('married', 'Married')], max_length=20, null=True, unique=True)
    marriage_contract = models.ImageField(blank=True, null=True, upload_to='marriage_contract_images/')
    elec_bill = models.ImageField(upload_to='elec_bill_images/', null=True, unique=True)
    birth_certificate = models.ImageField(upload_to='birth_certificate_images/', null=True, unique=True)
    id_or_driver_license = models.ImageField(upload_to='id_or_driver_license_images/', null=True, unique=True)
    approval_status = models.BooleanField(default=False)
    
    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.full_name

class AgentInfo(AbstractBaseModel):
    company_name = models.CharField(max_length=255, null=True, unique=True)
    company_address = models.CharField(max_length=255, null=True, unique=True)
    company_email = models.EmailField(max_length=255, null=True, unique=True)
    company_phone_number = models.CharField(max_length=11, null=True, unique=True)
    biometric = models.ImageField(upload_to='biometric_images/', null=True, unique=True)
    business_card = models.ImageField(upload_to='business_card_images/', null=True, unique=True)
    id_card = models.ImageField(upload_to='id_card_images/', null=True, unique=True)
    agent_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agent_info')
    approval_status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.company_name

class BuyerPersonalInfo(CommonFields):
    buyer_agreement = models.ImageField(upload_to='buyer_aggrement_images/', null=True, unique=True)
    buyer_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer_personal_info')

class SellerPersonalInfo(CommonFields):
    passport = models.ImageField(upload_to='passport_images/', null=True, unique=True)
    seller_agreement = models.ImageField(upload_to='seller_aggrement_images/', null=True, unique=True)
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