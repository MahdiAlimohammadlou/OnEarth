from .models import Property, Project, City
from django_filters import rest_framework as filters
from django.db.models import Q, Count, F, ExpressionWrapper, FloatField

class PropertyFilter(filters.FilterSet):
    country = filters.CharFilter(field_name='project__city__country__name', lookup_expr='iexact')
    city = filters.CharFilter(field_name='project__city__name', lookup_expr='iexact')
    min_price = filters.NumberFilter(field_name='price_per_nft', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price_per_nft', lookup_expr='lte')
    min_area = filters.NumberFilter(field_name='area', lookup_expr='gte')
    max_area = filters.NumberFilter(field_name='area', lookup_expr='lte')
    bedrooms = filters.NumberFilter(field_name='bedrooms', lookup_expr='exact')
    furnished = filters.BooleanFilter(field_name='furnished')
    has_image = filters.BooleanFilter(method='filter_has_image')
    has_video = filters.BooleanFilter(method='filter_has_video')
    plan_type = filters.CharFilter(field_name='plan_type')
    project = filters.NumberFilter(field_name='project')
    unit_number = filters.NumberFilter(field_name='unit_number')
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
            Q(project__neighborhood__name__icontains=value) |
            Q(project__title__icontains=value) |
            Q(name__icontains=value)
        )

    class Meta:
        model = Property
        fields = ['country', 'city', 'min_price', 'max_price', 'min_area', 'max_area', 'bedrooms', 'plan_type', 'furnished', 'has_image', 'has_video', 'search']


class ProjectFilter(filters.FilterSet):
    country = filters.CharFilter(field_name='city__country__name', lookup_expr='iexact')
    city = filters.CharFilter(field_name='city__name', lookup_expr='iexact')
    search = filters.CharFilter(method='filter_search')
    min_price = filters.NumberFilter(method='filter_min_price')
    max_price = filters.NumberFilter(method='filter_max_price')
    min_area = filters.NumberFilter(field_name='properties__area', lookup_expr='gte')
    max_area = filters.NumberFilter(field_name='properties__area', lookup_expr='lte')
    furnished = filters.BooleanFilter(field_name='properties__furnished')
    # Booleans
    has_image = filters.BooleanFilter(method='filter_has_image')
    has_video = filters.BooleanFilter(method='filter_has_video')

    def _annotate_effective_price(self, queryset):
        return queryset.annotate(
            effective_price=ExpressionWrapper(
                F('properties__price_per_nft') * (1 - F('properties__offer') / 100),
                output_field=FloatField()
            )
        ).distinct()

    def filter_min_price(self, queryset, name, value):
        queryset = self._annotate_effective_price(queryset)
        return queryset.filter(effective_price__gte=value)

    def filter_max_price(self, queryset, name, value):
        queryset = self._annotate_effective_price(queryset)
        return queryset.filter(effective_price__lte=value)

    def filter_has_image(self, queryset, name, value):
        queryset = queryset.annotate(image_count=Count('cover_img'))
        if value:
            return queryset.filter(image_count__gt=0)
        else:
            return queryset.filter(image_count=0)

    def filter_has_video(self, queryset, name, value):
        queryset = queryset.annotate(video_count=Count('videos'))
        if value:
            return queryset.filter(video_count__gt=0)
        else:
            return queryset.filter(video_count=0)

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(city__country__name__icontains=value) |
            Q(city__name__icontains=value) |
            Q(neighborhood__name__icontains=value) |
            Q(title__icontains=value)
        )

    class Meta:
        model = Project
        fields = ['country', 'city', 'min_price', 'max_price', 'min_area', 'max_area', 'furnished', 'has_image', 'has_video', 'search']


class CityFilter(filters.FilterSet):
    country = filters.CharFilter(field_name='country__name', lookup_expr='iexact')
    search = filters.CharFilter(method='filter_search')

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(country__name__icontains=value) |
            Q(name__icontains=value)
        )

    class Meta:
        model = City
        fields = ['country', 'search']