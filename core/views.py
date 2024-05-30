from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .utils import get_current_url
from rest_framework.views import APIView

# Create your views here.

class LocationBaseModelViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    model = None
    serializer_class = None

    def get_queryset(self):
        return self.model.objects.all()
    
    def list(self, request, *args, **kwargs):
        url = get_current_url(request)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={'url': url})
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        url = get_current_url(request)
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'url': url})
        return Response(serializer.data)


class InfoAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = None
    model_class = None
    user_field = None

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            personal_info = serializer.save(**{self.user_field: request.user})
            return Response(self.serializer_class(personal_info).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, format=None):
        try:
            personal_info = self.model_class.objects.get(**{self.user_field: request.user})
            serializer = self.serializer_class(personal_info)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except self.model_class.DoesNotExist:
            return Response({"detail": f"{self.model_class.__name__} not found."}, status=status.HTTP_404_NOT_FOUND)