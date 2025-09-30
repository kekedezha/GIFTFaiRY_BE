from django.shortcuts import render
from .models import User, Filter
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .serializers import UserPostSerializer, FilterPostSerializer, FilterGetSerializer, UserGetSerializer
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

class UserGetViewSet(generics.RetrieveAPIView):
    '''
    METHODS: GET
    Retrieves a single user by email. Returns 404 if not found. 
    '''
    
    serializer_class = UserGetSerializer # Save data from User table specified in the UserGetSerializer class to the serializer_class variable
    lookup_field = 'email' # Tells Django to look for 'email' field in the URL
    def get_queryset(self):
        return User.objects.all() # Queryset to retrieve all User objects from the database

    def get_object(self):
        queryset = self.get_queryset() # Get the queryset
        email = self.kwargs.get(self.lookup_field) # Get the email from the URL parameters
        try:
            return queryset.get(email=email) # Return the serialized data
        except User.DoesNotExist:
            raise NotFound(detail="User not found") # Return 404 if user not found

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
    # Save data from Filter table specified in the FilterGetSerializer class
    # to the serializer_class variable
    serializer_class = FilterGetSerializer

    # Overwrites get_queryset function which is a part of GetViewSet class
    def get_queryset(self):
        # Get the user ID from the URL parameters
        email = self.kwargs['email']
        # Filter queryset based on the user ID
        return Filter.objects.filter(email=email)
