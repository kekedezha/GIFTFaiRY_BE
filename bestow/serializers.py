from rest_framework import serializers
from .models import(
    User,
    Filter,
)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
        ]

class FilterPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filter
        fields = "__all__"

class FilterGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filter
        fields = ['output_text']