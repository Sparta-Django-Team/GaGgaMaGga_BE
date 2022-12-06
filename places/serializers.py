from rest_framework import serializers
from .models import Place

class PlaceSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'

class PlaceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'