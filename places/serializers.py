from rest_framework import serializers

from .models import Place

#맛집 serializer
class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ('id', 'place_name', 'category', 'rating', 'menu', 'place_desc', 'place_address', 'place_number', 'place_time', 'place_img', 'latitude', 'longitude', 'hit', 'place_bookmark', )


