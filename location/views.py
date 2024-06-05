from core.views import LocationBaseModelViewSet
from .models import Country, City, Project, Property, Banner, Category, PropertyLike, Neighborhood
from .serializers import (
    CountrySerializer, CitySerializer,
    ProjectSerializer, PropertySerializer,
    BannerSerializer, CategorySerializer,
    NeighborhoodSerializer)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, permissions
from core.utils import get_current_url
from rest_framework.views import APIView
from .filters import PropertyFilter
from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404

class CountryViewSet(LocationBaseModelViewSet):
    model = Country
    serializer_class = CountrySerializer

class CityViewSet(LocationBaseModelViewSet):
    model = City
    serializer_class = CitySerializer

    def list(self, request, *args, **kwargs):
        country_id = request.GET.get("country_id", None)
        if country_id is not None:
            url = get_current_url(request)
            queryset = City.objects.filter(country=country_id)
            serializer = CitySerializer(instance=queryset, many=True, context={'url' : url})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return super().list(request, *args, **kwargs)

class NeighborhoodViewSet(LocationBaseModelViewSet):
    model = Neighborhood
    serializer_class = NeighborhoodSerializer

    def list(self, request, *args, **kwargs):
        city_id = request.GET.get("city_id", None)
        if city_id is not None:
            url = get_current_url(request)
            queryset = Neighborhood.objects.filter(city=city_id)
            serializer = NeighborhoodSerializer(instance=queryset, many=True, context={'url' : url})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return super().list(request, *args, **kwargs)

class ProjectViewSet(LocationBaseModelViewSet):
    model = Project
    serializer_class = ProjectSerializer

    def list(self, request, *args, **kwargs):
        neighborhood_id = request.GET.get("neighborhood_id", None)
        if neighborhood_id is not None:
            url = get_current_url(request)
            queryset = Project.objects.filter(neighborhood=neighborhood_id)
            serializer = ProjectSerializer(instance=queryset, many=True, context={'url' : url})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return super().list(request, *args, **kwargs)

class PropertyViewSet(LocationBaseModelViewSet):
    model = Property
    serializer_class = PropertySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PropertyFilter

    def list(self, request, *args, **kwargs):
        project_id = request.GET.get("project_id", None)
        if project_id is not None:
            url = get_current_url(request)
            queryset = Property.objects.filter(project=project_id)
            serializer = PropertySerializer(instance=queryset, many=True, context={'url' : url})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def search(self, request):
        filtered_qs = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(filtered_qs)
        url = get_current_url(request)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'url': url})
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(filtered_qs, many=True, context={'url': url})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def properties_with_offer(self, request, country_id=None):
        url = get_current_url(request)
        if country_id is not None:
            properties_with_offer = Property.objects.filter(
            project__city__country_id=country_id,
            offer__gt=0
            )
        else :
            properties_with_offer = Property.objects.filter(offer__gt=0)
        serializer = self.get_serializer(properties_with_offer, many=True, context={'url': url})
        return Response(serializer.data)

class BannerListView(APIView):
    def get(self, request):
        banners_queryset = Banner.objects.all()
        serializer = BannerSerializer(banners_queryset, many=True)
        return Response(serializer.data)

class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    

class PropertyLikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def update_property_likes(self, property_id, increment):
        property = get_object_or_404(Property, id=property_id)
        property.likes += increment
        property.save()

    def post(self, request, format=None):
        property_id = request.data.get('property')
        user = request.user
        try:
            PropertyLike.objects.create(user=user, property_id=property_id)
            self.update_property_likes(property_id, 1)
            return Response({"detail": "like created successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": "like creation failed"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        property_id = request.data.get('property')
        user = request.user
        like = get_object_or_404(PropertyLike, user=user, property_id=property_id)
        like.delete()
        self.update_property_likes(property_id, -1)
        return Response({"detail": "like removed successfully"}, status=status.HTTP_204_NO_CONTENT)
    
class UserLikesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        property_likes = PropertyLike.objects.filter(user=user)
        property_ids = property_likes.values_list('property_id', flat=True)
        return Response({'property_ids': list(property_ids)})