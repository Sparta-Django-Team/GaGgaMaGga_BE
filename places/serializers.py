from rest_framework import serializers, exceptions
from places.models import Place


class PlaceSerializer(serializers.ModelSerializer):
    class Meta :
        model = Place
        fields = '__all__'