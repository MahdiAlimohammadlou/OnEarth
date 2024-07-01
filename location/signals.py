from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Project

@receiver(pre_save, sender=Project)
def create_project_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)

@receiver(pre_save, sender=Project)
def set_project_properties_offer(sender, instance, **kwargs):
    if instance.pk:
        if instance.offer:
            if not instance.properties:
                instance.properties = {}
            instance.properties.update(offer=instance.offer)

