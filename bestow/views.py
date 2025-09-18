from django.shortcuts import render
from .models import User, Filter
from rest_framework import generics
from .serializers import UserPostSerializer, FilterPostSerializer, FilterGetSerializer, UserGetSerializer
from django.http import HttpResponse
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

class UserGetViewSet(generics.ListAPIView):
    '''
    METHODS: GET
    '''
    # Save data from User table specified in the UserGetSerialzer class
    # to the serializer_class variable
    serializer_class = UserGetSerializer

    # Overwrites getqueryset function which is a part of GetViewSet class
    def get_queryset(self):
        # Get the user ID from the URL parameters
        email = self.kwargs['email']
        # User queryset based on the user ID
        return User.objects.filter(email=email)


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
    # Save data from Filter table specified in the FilterGetSerialzer class
    # to the serializer_class variable
    serializer_class = FilterGetSerializer

    # Overwrites getqueryset function which is a part of GetViewSet class
    def get_queryset(self):
        # Get the user ID from the URL parameters
        email = self.kwargs['email']
        # Filter queryset based on the user ID
        return Filter.objects.filter(email=email)
