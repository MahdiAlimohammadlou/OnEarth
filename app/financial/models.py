from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import AbstractBaseModel
from location.models import Property
from account.models import User

# Create your models here.
class ShippingInfo(AbstractBaseModel):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name="shippinginfo")
    tax_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=1
    )
    title_deed_fee_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=4
    )
    extra_fee_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=1
    )
    extra_fee_description = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=11000)
    connections = models.DecimalField(max_digits=10, decimal_places=2, default=236)
    payoff_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self) -> str:
        return self.property.name

class NFT(AbstractBaseModel):
    token_id = models.CharField(max_length=100, unique=True)
    property = models.ForeignKey(Property, related_name='nfts', on_delete=models.CASCADE, null=True, blank=True)
    owner = models.CharField(max_length=100)

# class Payment(AbstractBaseModel):
#     PAYMENT_STATUS = [
#         ('pending', 'Pending'),
#         ('completed', 'Completed'),
#         ('failed', 'Failed'),
#     ]

#     user = models.ForeignKey(User, related_name='payments', on_delete=models.CASCADE)
#     property = models.ForeignKey(Property, related_name='payments', on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='pending')

#     def __str__(self):
#         return f"{self.user.email} - {self.amount} - {self.status}"

# class Transaction(AbstractBaseModel):
    
#     payment = models.ForeignKey(Payment, related_name='transactions', on_delete=models.CASCADE)
#     user = models.ForeignKey(User, related_name='transactions', on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"{self.user.email} - {self.amount} - {self.transaction_type}"


