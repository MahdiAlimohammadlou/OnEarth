from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import get_object_or_404
from .models import NFT, Property
import requests

# Create your views here.
# def nft_detail(request, token_id):
#     nft = get_object_or_404(NFT, token_id=token_id)
#     nft_json = serializers.serialize('json', [nft])
#     return JsonResponse(nft_json, safe=False)

# def property_nfts(request, property_id):
#     property_obj = get_object_or_404(Property, pk=property_id)
#     nfts = property_obj.nfts.all()
#     nfts_json = serializers.serialize('json', nfts)
#     return JsonResponse(nfts_json, safe=False)

# from django.shortcuts import render, get_object_or_404
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from .models import NFT, Purchase
# from django.contrib.auth.decorators import login_required
# from django.conf import settings

# @csrf_exempt
# @login_required
# def purchase_nft(request, token_id):
#     if request.method == 'POST':
#         nft = get_object_or_404(NFT, token_id=token_id)
#         user = request.user
#         price = nft.price

#         # مرحله پرداخت
#         # در اینجا شما می‌توانید از یک درگاه پرداخت استفاده کنید
#         # اگر پرداخت موفقیت‌آمیز بود، خرید را ثبت کنید

#         purchase = Purchase.objects.create(user=user, nft=nft, price=price)
#         return JsonResponse({'message': 'Purchase successful', 'purchase_id': purchase.id})
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=400)

