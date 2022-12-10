from rest_framework import serializers

from .models import Notification


#후기 전체 serializer
class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = '__all__'

class NotificationDetailSerializer(serializers.ModelSerializer) :
    
    class Meta:
        model = Notification
        fields = ('is_seen',)