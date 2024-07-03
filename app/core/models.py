from django.db import models
from django.core.exceptions import ValidationError
from .utils import ImageCompressionClass

# Create your models here.
class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs) 
        for field in self._meta.get_fields():
            if isinstance(field, models.ImageField):
                image_field = getattr(self, field.name)
                if image_field and image_field.path:
                    try:
                        ImageCompressionClass.reduce_image_size(image_field.path)
                    except FileNotFoundError:
                        print(f"File {image_field.path} not found. Skipping resize.")

class AbstractBaseInfoModel(AbstractBaseModel):
    STATUS_CHOICES = [
        ('New', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    biometric = models.ImageField(upload_to='biometric_images/', null=True, blank=True)
    biometric_approval_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New', verbose_name='biometric approval Status')
    approval_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New', verbose_name='َApproval Status')

    class Meta:
        abstract = True

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs) 
        for field in self._meta.get_fields():
            if isinstance(field, models.ImageField):
                image_field = getattr(self, field.name)
                if image_field and image_field.path:
                    try:
                        ImageCompressionClass.reduce_image_size(image_field.path)
                    except FileNotFoundError:
                        print(f"File {image_field.path} not found. Skipping resize.")

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
    

