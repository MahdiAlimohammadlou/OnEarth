from .models import AgentInfo, BuyerPersonalInfo, SellerPersonalInfo
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=AgentInfo)
def update_user_is_agent(sender, instance, **kwargs):
    if instance.approval_status:
        instance.agent_user.is_agent = True
    instance.agent_user.save()

@receiver(post_save, sender=BuyerPersonalInfo)
def update_user_is_agent(sender, instance, **kwargs):
    if instance.approval_status:
        instance.buyer_user.is_buyer = True
    instance.buyer_user.save()

@receiver(post_save, sender=SellerPersonalInfo)
def update_user_is_agent(sender, instance, **kwargs):
    if instance.approval_status:
        instance.seller_user.is_seller = True
    instance.seller_user.save()