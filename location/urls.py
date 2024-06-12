from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import action
from rest_framework.response import Response

from .views import (CountryViewSet, CityViewSet,
                     ProjectViewSet, PropertyViewSet,
                     BannerListView, PropertyLikeView,
                     UserLikesView, NeighborhoodViewSet)

router = DefaultRouter()

router.register('countries', CountryViewSet, basename='country')
router.register('cities', CityViewSet, basename='city')
router.register('projects', ProjectViewSet, basename='project')
router.register('properties', PropertyViewSet, basename='property')
router.register('neighborhoods', NeighborhoodViewSet, basename='neighborhood')

urlpatterns = [
    # API urls
    path('', include(router.urls)),
    path('properties-with-offer/<int:country_id>', PropertyViewSet.as_view({'get': 'properties_with_offer'}), name='properties-with-offer'),
    path('properties-with-offer/', PropertyViewSet.as_view({'get': 'properties_with_offer'}), name='properties-with-offer'),
    path('banners/', BannerListView.as_view(), name="banners"),
    path('like/', PropertyLikeView.as_view(), name="like"),
    path('user-likes/', UserLikesView.as_view(), name="user-like"),
]