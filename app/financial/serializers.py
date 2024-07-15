from .models import ShippingInfo, NFT
from rest_framework import serializers

class ShippingInfoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ShippingInfo
        fields = [
         "property", "tax_percentage", "title_deed_fee_percentage", "extra_fee_percentage",
           "total_price", "connections", 
        ]

class NFTSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = NFT
        fields = [
            "token_id", "property", "owner"
        ]