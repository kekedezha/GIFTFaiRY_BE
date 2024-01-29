from django.shortcuts import render
from .models import User, Filter
from rest_framework import generics
from .serializers import UserPostSerializer, FilterPostSerializer, FilterGetSerializer
# Create your views here.

class ProfileViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserPostSerializer
    lookup_field = "username"

class UserPostViewSet(generics.CreateAPIView):
    '''
    METHODS: POST
    '''
    queryset = User.objects.all()
    serializer_class = UserPostSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.create_user()

class FilterPostViewSet(generics.CreateAPIView):
    '''
    METHODS: POST
    '''
    queryset = Filter.objects.all()
    serializer_class = FilterPostSerializer

    def perform_create(self, serializer):
        gift = serializer.save()
        gift.send_filters()

class FilterGetViewSet(generics.ListAPIView):
    '''
    METHODS: GET
    '''
    queryset = Filter.objects.all()
    serializer_class = FilterGetSerializer
