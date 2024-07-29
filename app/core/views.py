from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError, MethodNotAllowed

from .models import AboutUsInfo
from .serializers import AboutUsInfoSerializer

# Create your views here.

class LocationBaseModelViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    model = None
    serializer_class = None

    def get_queryset(self):
        return self.model.objects.all()
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(instance = queryset, many=True, context={'request' : request})
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request' : request})
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed('POST')

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed('PUT')

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed('PATCH')

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed('DELETE')


class InfoAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = None
    create_or_update_serializer_class = None
    model_class = None
    user_field = None

    def post(self, request, format=None):
        # Check if the info object for the user already exists
        info_instance = self.model_class.objects.filter(**{self.user_field: request.user}).first()
        
        # If an instance exists, update it; otherwise, create a new one
        if info_instance:
            serializer = self.create_or_update_serializer_class(info_instance, data=request.data, partial=True)
        else:
            serializer = self.create_or_update_serializer_class(data=request.data)
        
        if serializer.is_valid():
            try:
                personal_info = serializer.save(**{self.user_field: request.user})
                return Response(self.create_or_update_serializer_class(personal_info).data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, format=None):
        try:
            personal_info = self.model_class.objects.get(**{self.user_field: request.user})
            serializer = self.serializer_class(personal_info)
            serialized_data = serializer.data
            serialized_data['approval_status'] = personal_info.approval_status
            return Response(serialized_data, status=status.HTTP_200_OK)
        except self.model_class.DoesNotExist:
            return Response({"detail": f"{self.model_class.__name__} not found."}, status=status.HTTP_404_NOT_FOUND)

class AboutUsInfoView(APIView):
    def get(self, request):
        try:
            about_us_info = AboutUsInfo.objects.get()
            serializer = AboutUsInfoSerializer(about_us_info)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AboutUsInfo.DoesNotExist:
            return Response({"detail": "About Us Info not found"}, status=status.HTTP_404_NOT_FOUND)