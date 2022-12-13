from rest_framework import serializers

from .models import Notification

#알람 리스트 serializer
class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ('user','content','created_at','is_seen','id')


#알람 상세페이지 serializer
class NotificationDetailSerializer(serializers.ModelSerializer) :

    class Meta:
        model = Notification
        fields = ('is_seen',)