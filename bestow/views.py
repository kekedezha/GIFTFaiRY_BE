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
        user.saveToUserDatabase()

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

    userInstance = Filter.getUserInstance()
    queryset = Filter.objects.filter(user=userInstance)
    serializer_class = FilterGetSerializer

    # def perform_create(self, serializer):
    #     user = serializer.save()

    # This line gets all of the data back from Filter table
    # queryset = Filter.objects.all()
    # We are assigning all of the data to serializer_class from the fields that
    # are specificed in FilterGetSerializer in serializers.py
    # serializer_class = FilterGetSerializer
    # lookup_field = "username"