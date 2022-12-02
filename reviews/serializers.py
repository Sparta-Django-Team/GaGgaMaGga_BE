from rest_framework import serializers
from .models import Review

class ReviewListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    def get_user(self, obj):
        return obj.user.username

    class Meta:
        model = Review
        fields = '__all__'

class ReviewCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ("title", "content","rating_cnt")
        extra_kwargs = {
                        'title':{
                        'error_messages':{
                        'required':'제목을 입력해주세요',
                        'blank':'제목을 입력해주세요',}},

                        'content':{
                        'error_messages': {
                        'required':'내용을 입력해주세요.',
                        'blank':'내용을 입력해주세요.',}},
                        
                        'rating_cnt':{
                        'error_messages':{
                        'required':'평점을 입력해주세요',
                        'blank':'평점을 입력해주세요',}},}