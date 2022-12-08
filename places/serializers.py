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
        fields = ('id', 'place_name', 'category', 'rating', 'place_address', 'place_number', 'place_time', 'place_img', 'latitude', 'longitude', 'hit', 'place_bookmark')

#장소 생성 serializer
class PlaceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ('place_name', 'category', 'place_address', 'place_number', 'place_time', 'place_img', )
        extra_kwargs = {'place_name':{
                'error_messages': {
                'required':'매장명을 입력해주세요.',
                'blank':'매장명을 입력해주세요.',}},
                
                'categoty':{
                'error_messages':{
                'required':'카테고리를 입력해주세요',
                'blank':'카테고리를 입력해주세요',}},
                
                'place_address':{
                'error_messages':{
                'required':'주소명을 입력해주세요',
                'blank':'주소명을 입력해주세요',}},
                
                'place_number':{
                'error_messages':{
                'required':'전화번호를 입력해주세요',
                'blank':'전화번호을 입력해주세요',}},
                
                'place_time':{
                'error_messages':{
                'required':'시간을 입력해주세요',
                'blank':'시간을 입력해주세요',}},}

