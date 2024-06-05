from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class AbstractBaseInfoModel(AbstractBaseModel):
    STATUS_CHOICES = [
        ('New', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    passport = models.ImageField(upload_to='passport_images/', null=True, blank=True)
    passport_approval_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New', verbose_name='Passport approval Status')
    biometric = models.ImageField(upload_to='biometric_images/', null=True, blank=True)
    biometric_approval_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New', verbose_name='biometric approval Status')
    basic_approval_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New', verbose_name='Basic info approval Status')
    approval_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New', verbose_name='َApproval Status')

    class Meta:
        abstract = True

class AboutUsInfo(models.Model):
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=17)
    address = models.TextField()

    def save(self, *args, **kwargs):
        if AboutUsInfo.objects.exists() and not self.pk:
            raise ValidationError("Only one AboutUsInfo instance is allowed.")
        return super(AboutUsInfo, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    

