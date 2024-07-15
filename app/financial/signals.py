from django.db.models.signals import pre_save
from django.dispatch import receiver
from decimal import Decimal
from .models import ShippingInfo

@receiver(pre_save, sender=ShippingInfo)
def calculate_payoff_price(sender, instance, **kwargs):
    # tax_amount = instance.total_price * (instance.tax_percentage / Decimal(100))
    # title_deed_fee_amount = instance.total_price * (instance.title_deed_fee_percentage / Decimal(100))
    # extra_fee_amount = instance.total_price * (instance.extra_fee_percentage / Decimal(100))

    # instance.payoff_price = (
    #     instance.connections +
    #     tax_amount +
    #     title_deed_fee_amount +
    #     extra_fee_amount +
    #     instance.total_price
    # ) 
    instance.property.price_per_nft = instance.total_price / Decimal(5)
    instance.property.save()