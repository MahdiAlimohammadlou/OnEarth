from core.views import LocationBaseModelViewSet
from .models import (Country, City, Project, Property,
                      Banner, PropertyLike, Neighborhood,
                      Chat)
from .serializers import (
    CountrySerializer, CitySerializer,
    ProjectSerializer, PropertySerializer,
    BannerSerializer, NeighborhoodSerializer,
    ChatSerializer)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from .filters import PropertyFilter, ProjectFilter, CityFilter
from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404
from django.db.models import Q
from openai import OpenAI

class CountryViewSet(LocationBaseModelViewSet):
    model = Country
    serializer_class = CountrySerializer

class CityViewSet(LocationBaseModelViewSet):
    model = City
    serializer_class = CitySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CityFilter

    def list(self, request, *args, **kwargs):
        country_id = request.GET.get("country_id", None)
        if country_id is not None:
            queryset = City.objects.filter(country=country_id)
            serializer = CitySerializer(instance=queryset, many=True, context={'request' : request})
            return Response(serializer.data)
        else:
            return super().list(request, *args, **kwargs)
        
    @action(detail=False, methods=['get'])
    def search(self, request):
        filtered_qs = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(filtered_qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(filtered_qs, many=True, context={'request': request})
        return Response(serializer.data)

class NeighborhoodViewSet(LocationBaseModelViewSet):
    model = Neighborhood
    serializer_class = NeighborhoodSerializer

    def list(self, request, *args, **kwargs):
        city_id = request.GET.get("city_id", None)
        if city_id is not None:
            queryset = Neighborhood.objects.filter(city=city_id)
            serializer = NeighborhoodSerializer(instance=queryset, many=True, context={'request' : request})
            return Response(serializer.data)
        else:
            return super().list(request, *args, **kwargs)

class ProjectViewSet(LocationBaseModelViewSet):
    model = Project
    serializer_class = ProjectSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProjectFilter

    def list(self, request, *args, **kwargs):
        neighborhood_id = request.GET.get("neighborhood_id", None)
        city_id = request.GET.get("city_id", None)
        country_id = request.GET.get("country_id", None)
        queryset = Project.objects.all()

        if neighborhood_id is not None:
            queryset = queryset.filter(neighborhood=neighborhood_id)
        if city_id is not None:
            queryset = queryset.filter(city=city_id)
        if country_id is not None:
            queryset = queryset.filter(city__country=country_id)

        serializer = ProjectSerializer(instance=queryset, many=True, context={'request': request})
        return Response(serializer.data) 
        
    @action(detail=False, methods=['get'])
    def search(self, request):
        filtered_qs = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(filtered_qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(filtered_qs, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def projects_with_offer(self, request, country_id=None):
        if country_id is not None:
            projects_with_offer = Project.objects.filter(
                Q(city__country_id=country_id) & (Q(offer__gt=0) | Q(properties__offer__gt=0) | Q(has_promotion=True))
            ).distinct()
        else :
            projects_with_offer = projects_with_offer = Project.objects.filter( 
                Q(offer__gt=0) | Q(properties__offer__gt=0) | Q(has_promotion=True)
            ).distinct()
        serializer = self.get_serializer(projects_with_offer, many=True, context={'request': request})
        return Response(serializer.data)

class PropertyViewSet(LocationBaseModelViewSet):
    model = Property
    serializer_class = PropertySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PropertyFilter

    def list(self, request, *args, **kwargs):
        project_id = request.GET.get("project_id", None)
        if project_id is not None:
            queryset = Property.objects.filter(project=project_id)
            serializer = PropertySerializer(instance=queryset, many=True, context={'request' : request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def search(self, request):
        filtered_qs = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(filtered_qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(filtered_qs, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def properties_with_category(self, request):
        category_id = request.GET.get("category_id", None)
        if category_id is not None:
            queryset = Property.objects.filter(category = category_id)
            serializer = PropertySerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Category not selected."}, status=status.HTTP_400_BAD_REQUEST)

class BannerListView(APIView):
    def get(self, request):
        banners_queryset = Banner.objects.all()
        serializer = BannerSerializer(banners_queryset, many=True)
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

client = OpenAI()

class ChatView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_message = request.data.get('message')
        if not user_message:
            return Response({"error": "Message is required."}, status=status.HTTP_400_BAD_REQUEST)

        countries = Country.objects.all()
        serialized_countries = CountrySerializer(countries, many=True, context={"request":request})
        countries_data = serialized_countries.data
        cities = City.objects.all()
        serialized_cities = CitySerializer(cities, many=True, context={"request":request})
        cities_data = serialized_cities.data
        projects = Project.objects.all()
        serialized_projects = ProjectSerializer(projects, many=True, context={"request":request})
        projects_data = serialized_projects.data
        properties = Property.objects.all()
        serialized_properties = PropertySerializer(properties, many=True, context={"request":request})
        properties_data = serialized_properties.data

        system_prompt = (f"You are a real estate consultant in OnEarth. Provide brief and concise responses by default. If the user asks for more details, provide a more detailed response."
                  f"Answer based on the following data:\n\n"
                  f"Countries: {countries_data}\n\n"
                  f"Cities: {cities_data}\n\n"
                  f"Projects: {projects_data}\n\n"
                  f"Properties: {properties_data}\n\n")

        try:
            completion = client.chat.completions.create(
              model="gpt-4o",
              messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"User question: {user_message}"}
              ]
            )
            ai_response = completion.choices[0].message.content
            print("api respose: ", ai_response)

            chat = Chat.objects.create(
                user=request.user,
                message=user_message,
                response=ai_response
            )

            return Response({"response": ai_response})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, *args, **kwargs):
        chats = Chat.objects.filter(user=request.user).order_by('-created_at')
        serialized_chats = ChatSerializer(chats, many=True)
        return Response(serialized_chats.data)
