from .models import Property
from django_filters import rest_framework as filters
from django.db.models import Count
from django.db.models import Q

class PropertyFilter(filters.FilterSet):
    country = filters.CharFilter(field_name='project__city__country__name', lookup_expr='iexact')
    city = filters.CharFilter(field_name='project__city__name', lookup_expr='iexact')
    min_price = filters.NumberFilter(field_name='price_per_nft', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price_per_nft', lookup_expr='lte')
    min_area = filters.NumberFilter(field_name='area', lookup_expr='gte')
    max_area = filters.NumberFilter(field_name='area', lookup_expr='lte')
    categories = filters.CharFilter(field_name='category__title', lookup_expr='iexact')
    bedrooms = filters.NumberFilter(field_name='bedrooms', lookup_expr='exact')
    bathrooms = filters.NumberFilter(field_name='bathrooms', lookup_expr='exact')
    furnished = filters.BooleanFilter(field_name='furnished')
    has_image = filters.BooleanFilter(method='filter_has_image')
    has_video = filters.BooleanFilter(method='filter_has_video')
    search = filters.CharFilter(method='filter_search')

    def filter_has_image(self, queryset, name, value):
        if value:
            return queryset.annotate(image_count=Count('propertyimage')).filter(image_count__gt=0)
        else:
            return queryset.annotate(image_count=Count('propertyimage')).filter(image_count=0)

    def filter_has_video(self, queryset, name, value):
        if value:
            return queryset.annotate(video_count=Count('videos')).filter(video_count__gt=0)
        else:
            return queryset.annotate(video_count=Count('videos')).filter(video_count=0)
        
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(project__city__country__name__icontains=value) |
            Q(project__city__name__icontains=value) |
            Q(project__title__icontains=value) |
            Q(name__icontains=value)
        )

    class Meta:
        model = Property
        fields = ['country', 'city', 'min_price', 'max_price', 'min_area', 'max_area', 'categories', 'bedrooms', 'bathrooms', 'furnished', 'has_image', 'has_video']
