from rest_framework import serializers
from .models import Place

class PlaceLocationSelectSerializer(serializers.ModelSerializer):
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