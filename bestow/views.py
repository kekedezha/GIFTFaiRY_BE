from django.shortcuts import render
from .models import User, Filter
from rest_framework import generics
from .serializers import ProfileSerializer, FilterPostSerializer
# Create your views here.

class ProfileViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "username"

class FilterPostViewSet(generics.CreateAPIView):
    queryset = Filter.objects.all()
    serializer_class = FilterPostSerializer
