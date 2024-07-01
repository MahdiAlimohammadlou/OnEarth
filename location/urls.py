from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (CountryViewSet, CityViewSet,
                     ProjectViewSet, PropertyViewSet,
                     BannerListView, PropertyLikeView,
                     UserLikesView, NeighborhoodViewSet,
                     PropertyCategoryListView)

router = DefaultRouter()

router.register('countries', CountryViewSet, basename='country')
router.register('cities', CityViewSet, basename='city')
router.register('projects', ProjectViewSet, basename='project')
router.register('properties', PropertyViewSet, basename='property')
router.register('neighborhoods', NeighborhoodViewSet, basename='neighborhood')

urlpatterns = [
    # API urls
    path('', include(router.urls)),
    path('projects-with-offer/<int:country_id>', ProjectViewSet.as_view({'get': 'projects_with_offer'}), name='projects_with_offer'),
    path('projects-with-offer/', ProjectViewSet.as_view({'get': 'projects_with_offer'}), name='projects_with_offer'),
    path('properties-with-category/', PropertyViewSet.as_view({'get': 'properties_with_category'}), name='properties_with_category'),
    path('property-categories/', PropertyCategoryListView.as_view(), name="property-categories"),
    path('banners/', BannerListView.as_view(), name="banners"),
    path('like/', PropertyLikeView.as_view(), name="like"),
    path('user-likes/', UserLikesView.as_view(), name="user-like"),
]