from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    

