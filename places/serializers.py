from rest_framework import serializers

from .models import Place

class PlaceSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'

#장소 serializer
class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ('id', 'place_name', 'category', 'rating', 'place_address', 'place_number', 'place_time', 'place_img', 'latitude', 'longitude', 'hit',)
