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

    serializer_class = FilterGetSerializer
    lookup_field = "email"

    def get_queryset(self):
        userInstance = User.objects.get(email=self.email)
        # Get the email of the currently authenticated user
        # email = self.request.user.email
        # Filter queryset based on the user's email address
        return Filter.objects.filter(user=userInstance)
    # queryset = Filter.objects.filter(email=email)
    # serializer_class = FilterGetSerializer
    # lookup_field = "email"
    

    # def get_queryset(self):
    #     # Filter queryset based on the currently authenticated user's email address
    #     email = self.request.user.email
    #     return Filter.objects.filter(email=email)
