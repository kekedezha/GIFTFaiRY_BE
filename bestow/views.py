from django.shortcuts import render
from .models import User, Filter
from rest_framework import generics
from .serializers import ProfileSerializer, FilterPostSerializer, FilterGetSerializer
# Create your views here.

class ProfileViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "username"

class FilterPostViewSet(generics.CreateAPIView):
    '''
    METHODS: POST
    '''
    queryset = Filter.objects.all()
    serializer_class = FilterPostSerializer

    def perform_create(self, serializer):
        gift = serializer.save()
        gift.send_filters()

class FilterGetViewSet(generics.RetrieveAPIView):
    '''
    METHODS: GET
    '''
    queryset = Filter.objects.all()
    serializer_class = FilterGetSerializer
