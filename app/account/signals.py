from .models import AgentInfo, BuyerPersonalInfo, SellerPersonalInfo
from django.db.models.signals import post_save
from django.dispatch import receiver

def check_approval_status(instance):

    if isinstance(instance, AgentInfo):
        all_approved = instance.basic_info_approval_status == 'Approved' and instance.business_card_approval_status == 'Approved' and instance.id_card_approval_status == 'Approved'
    else:
        all_approved = all([
        instance.basic_info_approval_status == 'Approved',
        instance.elec_bill_approval_status == 'Approved',
        instance.birth_certificate_approval_status == 'Approved',
        instance.id_or_driver_license_approval_status == 'Approved'
        ])
    
    instance.approval_status = all_approved
    instance.save(update_fields=['approval_status'])

@receiver(post_save, sender=AgentInfo)
def agent_info_post_save(sender, instance, **kwargs):
    check_approval_status(instance)

@receiver(post_save, sender=BuyerPersonalInfo)
def buyer_personal_info_post_save(sender, instance, **kwargs):
    check_approval_status(instance)

@receiver(post_save, sender=SellerPersonalInfo)
def seller_personal_info_post_save(sender, instance, **kwargs):
    check_approval_status(instance)

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